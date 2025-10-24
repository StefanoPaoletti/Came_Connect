"""Python client for CAME ETI/Domo - Constants.
Versione ottimizzata da Stefano Paoletti
Based on original work by Danny Mauro (Den901)
For more details: https://github.com/StefanoPaoletti/ha_came_personale
"""
import json
from pathlib import Path

# Debug flag - set to True for deep debugging (verbose logs)
DEBUG_DEEP = False

# Issue tracker URL
ISSUE_URL = "https://github.com/StefanoPaoletti/ha_came_personale/issues"


def get_version() -> str:
    """Get version from manifest.json (two levels up)"""
    try:
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
        return manifest.get("version", "unknown")
    except Exception:
        return "unknown"


# Lazy load version
_VERSION = None

def _get_version_cached() -> str:
    """Get cached version (read only once)"""
    global _VERSION
    if _VERSION is None:
        _VERSION = get_version()
    return _VERSION


# Export for backwards compatibility
VERSION = property(lambda self: _get_version_cached())


STARTUP_MESSAGE_TEMPLATE = """
-------------------------------------------------------------------
CAME ETI/Domo API Python Client - Optimized Version
Version: {version}
Based on original work by Den901
For issues or suggestions:
{issue_url}
-------------------------------------------------------------------
"""

def get_startup_message() -> str:
    """Get startup message with current version"""
    return STARTUP_MESSAGE_TEMPLATE.format(
        version=_get_version_cached(),
        issue_url=ISSUE_URL
    )
