# Came Connect

Home Assistant integration for CAME ETI/Domo home automation systems - optimized version.

Based on original work by [Den901](https://github.com/Den901/ha_came).

## Key Changes from Original

- Fixed Home Assistant freeze during uninstallation
- Corrected uninstallation procedure with timeout
- Simplified unique IDs based on original CAME names
- UI-only configuration (YAML support removed)
- Removed authentication token dependency
- Energy sensors now retain values after Home Assistant restart

**Note:** Device ID migration must be done manually.

## Supported Platforms

| Platform | Description |
|----------|-------------|
| `light` | On/off lights, dimmers and RGB |
| `climate` | Thermostats and thermal zones |
| `cover` | Shutters and motorized covers |
| `switch` | Generic relays |
| `sensor` | Analog sensors and energy meters |
| `binary_sensor` | Digital inputs |
| `scene` | CAME scenarios |

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Came Connect"
4. Enter your ETI/Domo IP address

## Debug

Add to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.came: debug
```

Restart Home Assistant to apply changes.

## Support

To report issues or request features:
https://github.com/StefanoPaoletti/Came_Connect/issues

## License

MIT License - see [LICENSE](https://github.com/StefanoPaoletti/Came_Connect/blob/main/LICENSE) for details.
