"""
The CAME Integration Component.
For more details about this platform, please refer to the documentation at
https://github.com/StefanoPaoletti/Came_Connect
"""
import logging

from homeassistant.const import CONF_ENTITIES
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .pycame.devices import CameDevice
from .const import ATTRIBUTION, DOMAIN, SIGNAL_DELETE_ENTITY, SIGNAL_UPDATE_ENTITY

_LOGGER = logging.getLogger(__name__)


class CameEntity(Entity):
    """CAME base entity.

    Each CAME device is its own HA device, and this entity is its main entity:
    has_entity_name with name None makes HA show just the device name
    (required by the entity naming rules of HA 2026.11).
    """

    _attr_has_entity_name = True
    _attr_name = None
    _attr_should_poll = False
    _attr_attribution = ATTRIBUTION

    def __init__(self, device: CameDevice):
        """Init."""
        self._device = device
        self._attr_unique_id = self._device.unique_id
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._device.unique_id)},
            "name": self._device.name,
            "manufacturer": "CAME",
            "model": self._device.type,
        }

    async def async_added_to_hass(self):
        """Call when entity is added to hass."""
        self.hass.data[DOMAIN][CONF_ENTITIES][self._device.unique_id] = self.entity_id

        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_UPDATE_ENTITY, self._update_callback
            )
        )
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_DELETE_ENTITY, self._delete_callback
            )
        )

    @callback
    def _update_callback(self):
        """Call update method."""
        self.async_schedule_update_ha_state(True)

    async def _delete_callback(self, dev_id):
        """Remove this entity, and its device when no entities are left."""
        if dev_id != self._device.unique_id:
            return

        entity_registry = er.async_get(self.hass)
        entity_entry = entity_registry.async_get(self.entity_id)
        if entity_entry is None:
            await self.async_remove(force_remove=True)
            return

        entity_registry.async_remove(self.entity_id)
        device_id = entity_entry.device_id
        if device_id and not er.async_entries_for_device(
            entity_registry, device_id, include_disabled_entities=True
        ):
            dr.async_get(self.hass).async_remove_device(device_id)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._device.available
