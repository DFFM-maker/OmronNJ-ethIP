# Omron NJ/NX EtherNet/IP Collector for SpeeDBee Synapse

This repository provides a high-level Python integration for Omron NJ/NX series PLCs using the EtherNet/IP (CIP) protocol. It is specifically designed to be used as a custom collector within the **SpeeDBee Synapse** data collection platform.

## 🚀 Features
- **Structure Browsing**: Automatically discover and map complex PLC structures (e.g., `ScadaInterface`).
- **Complex Data Support**: Seamlessly read nested structures, arrays, and custom data types.
- **SpeeDBee Ready**: Includes patterns for integration with Synapse's component-based architecture.
- **Optimized for NJ/NX**: Uses advanced CIP services for high-speed data access.

## 🛠 Prerequisites

### Original Library Credits
This project relies on the excellent `aphyt` library created by **Joseph Ryan**.
- **Repository**: [https://github.com/aphyt/aphytcomm](https://github.com/aphyt/aphytcomm)
- **License**: GPLv2 (as per original author)

### Installation
1. Install the base library:
   ```bash
   pip install aphyt
   ```
2. **Critical Fix**: If you are using Python 3.11 or newer, you must apply a syntax fix to the library. See [patches/README.md](./patches/README.md) for details.

## 📂 Project Structure
- `/src`: Main collection logic and structure browser.
- `/docs`: Implementation plans and task tracking.
- `/examples`: Test scripts for connectivity and specific data points.
- `/patches`: Mandatory fixes for Python 3.11+ compatibility.
- `/Manual`: Technical documentation for Omron and Synapse.

## 🚦 Quick Start
To browse your PLC structure:
```bash
python src/omron_structure_browser.py
```

To run the advanced connector:
```bash
python src/omron_advanced_connector.py
```

## 📝 Configuration
The project uses `scada.txt` (tab-separated) to define the tags mapped for local monitoring. For Synapse integration, a JSON configuration file is recommended.

## 🤝 Contributing
Feel free to open issues or pull requests to improve the Omron-Synapse integration.

---
*Created by Giuseppe De France and the Antigravity AI team.*
