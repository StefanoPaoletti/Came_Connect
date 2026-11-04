"""Python client for Came Connect - Constants.
Versione ottimizzata da Stefano Paoletti
Based on original work by Danny Mauro (Den901)
For more details: https://github.com/StefanoPaoletti/Came_Connect
"""
import json
from pathlib import Path

# Debug flag - set to True for deep debugging (verbose logs)
DEBUG_DEEP = False


# Read version ONCE at module import (before event loop starts)
def _load_version() -> str:
    """Load version from manifest.json at module import time."""
    try:
        # Go up two directories: pycame -> came -> manifest.json
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
        return manifest.get("version", "unknown")
    except Exception:
        return "unknown"


VERSION = _load_version()
