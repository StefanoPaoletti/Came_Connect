# Contributing

This repository is an optimized version of the original CAME integration by [Den901](https://github.com/Den901/ha_came), customized for specific needs.

## Contribution Policy

This project **does not accept pull requests or external contributions**. The code is shared publicly for transparency and as a reference.

## Changes Made

The main changes compared to the original integration include:

- Fixed issue that blocked Home Assistant during uninstallation
- Corrected uninstallation procedure with timeout
- Simplified unique IDs based on original CAME names
- UI-only configuration (removed YAML support)
- Removed authentication token dependency
- Energy sensors now maintain values after Home Assistant restart

## Reporting Issues

To report bugs or issues specific to this version, you can open an issue on this repository:
https://github.com/StefanoPaoletti/Came_Connect/issues

## Contributing to the Original Project

To contribute to the original project or report general CAME integration issues, please refer to the original repository:
https://github.com/Den901/ha_came

## License

This project is released under the MIT License, like the original project.
