# Came Connect

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Home Assistant integration for CAME ETI/Domo home automation systems - optimized version.

Based on original work by [Den901](https://github.com/Den901/ha_came).

> **Note:** This is a personal fork - Pull requests are not accepted. See [CONTRIBUTING.md](CONTRIBUTING.md)

## Key Changes from Original

- Fixed Home Assistant freeze during uninstallation
- Corrected uninstallation procedure with timeout
- Simplified unique IDs: `{platform}.{device_name}_{act_id}` (e.g., `light.kitchen_59`)
- UI-only configuration (YAML support removed)
- Removed authentication token dependency
- Energy sensors now retain values after Home Assistant restart

**Important:** Device ID migration must be done manually. Devices will have new unique IDs based on original CAME names.

## Supported Devices

Tested successfully with:
- On/off lights
- Thermostats (climate and heating)
- Generic relays (switches)
- Energy sensors (consumption monitoring)
- Digital inputs (binary sensors)


## Support

- Report bugs: [Issues](https://github.com/StefanoPaoletti/Came_Connect/issues)
- Original project: [Den901/ha_came](https://github.com/Den901/ha_came)

## License

MIT License - See [LICENSE](LICENSE) for details
