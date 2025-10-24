"""
The CAME Integration Component - Optimized Version
Versione ottimizzata da Stefano Paoletti
Basata sul lavoro originale di Danny Mauro (Den901)
For more details: https://github.com/StefanoPaoletti/ha_came_personale
"""
import json
from pathlib import Path

# Base component constants
NAME = "CAME Connect sp"
DOMAIN = "came"
ATTRIBUTION = "Data provided by CAME ETI/Domo"
ISSUE_URL = "https://github.com/StefanoPaoletti/ha_came_personale/issues"
DATA_YAML = f"{DOMAIN}__yaml"


def get_version() -> str:
    """Get version from manifest.json"""
    try:
        manifest_path = Path(__file__).parent / "manifest.json"
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
        return manifest.get("version", "unknown")
    except Exception:
        return "unknown"


# Lazy load version for startup message
_VERSION = None

def _get_version_cached() -> str:
    """Get cached version (read only once)"""
    global _VERSION
    if _VERSION is None:
        _VERSION = get_version()
    return _VERSION


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {{version}}
Versione ottimizzata per impianto personale
Basata sul progetto originale di Den901
Per problemi o suggerimenti:
{ISSUE_URL}
-------------------------------------------------------------------
"""

def get_startup_message() -> str:
    """Get startup message with current version"""
    return STARTUP_MESSAGE.format(version=_get_version_cached())


# Icons
# Device classes
# Signals
SIGNAL_DISCOVERY_NEW = DOMAIN + "_discovery_{}"
SIGNAL_DELETE_ENTITY = DOMAIN + "_delete"
SIGNAL_UPDATE_ENTITY = DOMAIN + "_update"

# Services
SERVICE_PULL_DEVICES = "pull_devices"
SERVICE_FORCE_UPDATE = "force_update"

# Configuration and options
CONF_MANAGER = "manager"
CONF_CAME_LISTENER = "came_listener"
CONF_ENTRY_IS_SETUP = "entry_is_setup"
CONF_PENDING = "pending"

# Defaults
# Attributes
