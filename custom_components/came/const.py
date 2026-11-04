"""
The CAME Integration Component - Optimized Version
Versione ottimizzata da Stefano Paoletti
Basata sul lavoro originale di Danny Mauro (Den901)
For more details: https://github.com/StefanoPaoletti/Came_Connect
"""
from .pycame.const import VERSION

# Base component constants
NAME = "CAME Connect"
DOMAIN = "came"
ATTRIBUTION = "Data provided by Came Connect"
ISSUE_URL = "https://github.com/StefanoPaoletti/Came_Connect/issues"
DATA_YAML = f"{DOMAIN}__yaml"

# Startup message with version already embedded
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
Versione ottimizzata per impianto personale
Basata sul progetto originale di Den901
Per problemi o suggerimenti:
{ISSUE_URL}
-------------------------------------------------------------------
"""

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
