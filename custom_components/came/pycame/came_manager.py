"""Python client for Came Connect.

Versione ottimizzata da Stefano Paoletti
Based on original work by Danny Mauro (Den901)
For more details: https://github.com/StefanoPaoletti/Came_Connect
"""

import json
import logging
from typing import TYPE_CHECKING, List, Optional

import requests

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

from .const import DEBUG_DEEP, VERSION
from .devices import get_featured_devices
from .devices.base import CameDevice, DeviceState
from .devices.came_scenarios import ScenarioManager
from .exceptions import (
    ETIDomoConnectionError,
    ETIDomoConnectionTimeoutError,
    ETIDomoError,
)
from .models import Floor, Room

_LOGGER = logging.getLogger(__name__)

# HTTP timeouts (seconds). Without them a request to a CAME that was switched
# off abruptly can hang forever and block the status listener.
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 10
# status_update_req is a long poll: the CAME holds it open until something
# changes, so it gets a longer read timeout. If the CAME holds it longer, the
# request simply times out and is repeated, keeping the same session.
STATUS_UPDATE_READ_TIMEOUT = 60

# sl_data_ack_reason codes meaning the session is unknown to the CAME
# (e.g. after the CAME restarted): log in again and repeat the request.
SESSION_LOST_ERRNOS = (7, 8)


class CameManager:
    """Main class for handling connections with a Came Connect device."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        session: Optional[requests.Session] = None,
        hass: Optional["HomeAssistant"] = None,
    ):
        """Initialize connection with the Came Connect."""
        _LOGGER.debug("Setup Came Connect API for %s@%s", username, host)

        self._host = host
        self._username = username
        self._password = password
        self._session = session or requests.Session()
        self._hass = hass
        self._client_id = None
        self._swver = None
        self._serial = None
        self._keycode = None
        self._features = []
        self._floors = None
        self._rooms = None
        self._devices = None
        self._resync_needed = False
        self.scenario_manager = ScenarioManager(self)

    @property
    def software_version(self) -> Optional[str]:
        """Return software version of Came Connect."""
        return self._swver

    @property
    def serial(self) -> Optional[str]:
        """Return serial number of Came Connect."""
        return self._serial

    @property
    def keycode(self) -> Optional[str]:
        """Return keycode for Came Connect."""
        return self._keycode

    def _request(
        self,
        command: dict,
        resp_command: str = None,
        read_timeout: float = READ_TIMEOUT,
    ) -> dict:
        """Handle a request to a Came Connect device."""
        url = f"http://{self._host}/domo/"
        headers = {
            "User-Agent": f"PythonCameManager-Stefano/{VERSION}",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            if DEBUG_DEEP:
                _LOGGER.debug("Sending API request: %s", command)

            response = self._session.post(
                url,
                data={"command": json.dumps(command)},
                headers=headers,
                timeout=(CONNECT_TIMEOUT, read_timeout),
            )
            response.raise_for_status()

            if DEBUG_DEEP:
                _LOGGER.debug("Response received: %s", response.text)

        except requests.exceptions.Timeout as exception:
            raise ETIDomoConnectionTimeoutError(
                "Timeout occurred while communicating with Came Connect device."
            ) from exception

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.BaseHTTPError,
        ) as exception:
            raise ETIDomoConnectionError(
                "Error occurred while communicating with Came Connect device."
            ) from exception

        try:
            # The CAME may not declare a charset: force UTF-8 so names
            # with accents ("Città") are not garbled
            response.encoding = "utf-8"
            resp_json = response.json()
            ack_reason = resp_json.get("sl_data_ack_reason")

            if ack_reason == 0:
                cmd_name = resp_json.get("sl_cmd")
                if resp_command is not None and cmd_name != resp_command:
                    raise ETIDomoError(
                        "Invalid server response. Expected {}. Actual {}".format(
                            repr(resp_command), repr(cmd_name)
                        )
                    )

                return resp_json

            # Error codes mapping
            errors = {
                1: "Invalid user.",
                3: "Too many sessions during login.",
                4: "Error occurred in JSON Syntax.",
                5: "No session layer command tag.",
                6: "Unrecognized session layer command.",
                7: "No client ID in request.",
                8: "Wrong client ID in request.",
                9: "Wrong application command.",
                10: "No reply to application command, maybe service down.",
                11: "Wrong application data.",
            }

            if ack_reason in errors:
                raise ETIDomoError(errors[ack_reason], errno=ack_reason)

            raise ETIDomoError(
                f"Unknown error (#{ack_reason}).",
                errno=ack_reason,
            )

        except ValueError as ex:
            raise ETIDomoError("Error in sl_data_ack_reason, can't find value.") from ex

    @property
    def connected(self) -> bool:
        """Return True if connected to Came device."""
        return self._client_id is not None

    def login(self) -> None:
        """Login function for access to Came Connect."""
        if self._client_id:
            return

        _LOGGER.debug("Attempting login to Came device")
        response = self._request(
            {
                "sl_cmd": "sl_registration_req",
                "sl_login": self._username,
                "sl_pwd": self._password,
            },
            "sl_registration_ack",
        )

        try:
            if response["sl_client_id"]:
                _LOGGER.debug("Successful authorization to Came device")
                self._client_id = response.get("sl_client_id")
                # Re-login after a disconnection: keep the device objects
                # (HA entities are bound to them) and resync their state.
                if self._devices is not None:
                    self._resync_needed = True
            else:
                raise ETIDomoError("Error in sl_client_id, can't get value.")
        except KeyError as ex:
            raise ETIDomoError("Error in sl_client_id, can't find value.") from ex

    def application_request(
        self,
        command: dict,
        resp_command: str = "generic_reply",
        read_timeout: float = READ_TIMEOUT,
    ) -> dict:
        """Handle a request to application layer of Came Connect."""
        if DEBUG_DEEP:
            _LOGGER.debug("Sending application layer API request: %s", command)

        for attempt in range(2):
            self.login()
            try:
                response = self._request(
                    {
                        "sl_cmd": "sl_data_req",
                        "sl_client_id": self._client_id,
                        "sl_appl_msg": command.copy(),
                    },
                    read_timeout=read_timeout,
                )
                break
            except ETIDomoConnectionError as err:
                # A read timeout means the CAME is reachable but slow (or a
                # long poll ran out): keep the session. Anything else means
                # the CAME went offline: log in again next time.
                if not isinstance(err.__cause__, requests.exceptions.ReadTimeout):
                    _LOGGER.debug("Came server goes offline, resetting client_id")
                    self._client_id = None
                raise
            except ETIDomoError as err:
                if err.errno in SESSION_LOST_ERRNOS and attempt == 0:
                    _LOGGER.info("CAME session lost (%s), logging in again", err)
                    self._client_id = None
                    continue
                raise

        if resp_command is not None and response.get("cmd_name") != resp_command:
            raise ETIDomoError(
                "Invalid server response. Expected {}. Actual {}".format(
                    repr(resp_command), repr(response.get("cmd_name"))
                )
            )

        return response

    def _get_features(self) -> list:
        """Get list of available features from Came device."""
        if self._features:
            return self._features

        cmd = {
            "cmd_name": "feature_list_req",
        }
        response = self.application_request(cmd, "feature_list_resp")
        self._swver = response.get("swver")
        self._serial = response.get("serial")
        self._keycode = response.get("keycode")
        self._features = response.get("list")
        
        _LOGGER.debug(
            "CAME device features loaded: sw_ver=%s, serial=%s",
            self._swver,
            self._serial
        )
        
        return self._features

    def get_all_floors(self) -> List[Floor]:
        """Get list of available floors."""
        if self._floors is not None:
            return self._floors

        cmd = {
            "cmd_name": "floor_list_req",
            "topologic_scope": "plant",
        }
        response = self.application_request(cmd, "floor_list_resp")
        self._floors = []
        for floor in response.get("floor_list", []):
            self._floors.append(Floor.from_dict(floor))
        
        _LOGGER.debug("Loaded %d floor(s) from CAME device", len(self._floors))
        return self._floors

    def get_all_rooms(self) -> List[Room]:
        """Get list of available rooms."""
        if self._rooms is not None:
            return self._rooms

        cmd = {
            "cmd_name": "room_list_req",
            "topologic_scope": "plant",
        }
        response = self.application_request(cmd, "room_list_resp")
        self._rooms = []
        for room in response.get("room_list", []):
            self._rooms.append(Room.from_dict(room))
        
        _LOGGER.debug("Loaded %d room(s) from Came device", len(self._rooms))
        return self._rooms

    def _fetch_devices(self) -> List[CameDevice]:
        """Read the device list from the CAME."""
        devices = []
        for feature in self._get_features():
            devices.extend(get_featured_devices(self, feature))
        return devices

    def _resync_devices(self) -> None:
        """Reload the device list keeping the existing device objects.

        HA entities hold references to these objects: replacing them would
        leave the entities frozen. Known devices get their fresh state,
        new devices are added, devices no longer on the CAME are dropped
        (their entities are removed by the pull_devices service).
        """
        current = {device.unique_id: device for device in self._devices or []}
        devices = []
        for fresh in self._fetch_devices():
            device = current.get(fresh.unique_id)
            if device is None:
                devices.append(fresh)
            else:
                device._device_info = fresh._device_info
                devices.append(device)
        self._devices = devices
        _LOGGER.info("Resynced %d device(s) from Came", len(devices))

    def _update_devices(self) -> Optional[List[CameDevice]]:
        """Update devices info from Came device."""
        if self._devices is None:
            _LOGGER.debug("Updating devices info from CAME")

            self._devices = self._fetch_devices()
            _LOGGER.info(
                "Loaded %d device(s) from Came: %s",
                len(self._devices),
                [d.type for d in self._devices]
            )

        else:
            _LOGGER.debug("Using cached devices data")

        return self._devices

    def get_all_devices(self) -> Optional[List[CameDevice]]:
        """Get list of all discovered devices."""
        return self._update_devices()
        
    def get_device_by_id(self, device_id: str) -> Optional[CameDevice]:
        """Get device by unique ID."""
        for device in self.get_all_devices():
            if device.unique_id == device_id:
                return device

        return None

    def get_device_by_act_id(self, act_id: int) -> Optional[CameDevice]:
        """Get device by device's act ID."""
        for device in self.get_all_devices():
            if device.act_id == act_id:
                return device

        return None

    def get_device_by_name(self, name: str) -> Optional[CameDevice]:
        """Get device by name."""
        for device in self.get_all_devices():
            if device.name == name:
                return device

        return None

    def get_devices_by_floor(self, floor_id: int) -> List[CameDevice]:
        """Get a list of devices on a floor."""
        devices = []
        for device in self.get_all_devices():
            if device.floor_id == floor_id:
                devices.append(device)

        return devices

    def get_devices_by_room(self, room_id: int) -> List[CameDevice]:
        """Get a list of devices in a room."""
        devices = []
        for device in self.get_all_devices():
            if device.room_id == room_id:
                devices.append(device)

        return devices

    def status_update(self, timeout: Optional[int] = None) -> bool:
        """Long polling method which reads status updates from Came device."""
        if self._devices is None:
            self._update_devices()
            return True

        if self._resync_needed:
            # Reconnected: states may have changed while we were away
            self._resync_devices()
            self._resync_needed = False  # only once the resync succeeded
            return True

        cmd = {
            "cmd_name": "status_update_req",
        }
        if timeout is not None:
            cmd["timeout"] = timeout
        
        response = self.application_request(
            cmd, "status_update_resp", read_timeout=STATUS_UPDATE_READ_TIMEOUT
        )
        
        if response and DEBUG_DEEP:
            _LOGGER.debug("Status update response: %s", response)

        updated = False

        for device_info in response.get("result", []):  # type: DeviceState
            cmd_name = device_info.get("cmd_name", "")
            
            if DEBUG_DEEP:
                _LOGGER.debug(
                    "Received cmd_name: %s - content: %s",
                    cmd_name,
                    device_info
                )

            # Delegate scenario updates to scenario manager
            if cmd_name.startswith("scenario_"):
                self.scenario_manager.handle_update(self._hass, device_info)
            
            # Handle plant update (device list changed)
            if cmd_name == "plant_update_ind":
                _LOGGER.info("Plant update detected, reloading devices")
                self._resync_devices()
                return True
            
            # Update individual device state
            act_id = device_info.get("act_id")
            if act_id:
                device = self.get_device_by_act_id(act_id)
                if device is not None:
                    updated |= device.update_state(device_info)
                else:
                    _LOGGER.debug("Device with act_id=%s not found", act_id)

        return updated
