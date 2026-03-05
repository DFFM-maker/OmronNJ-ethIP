# Implementation Plan: SpeedBee Synapse Collector for Omron NJ/NX

## Goal Description
Develop a high-performance data collector for SpeeDBee Synapse that communicates with Omron NJ/NX PLCs via EtherNet/IP (CIP) using the `aphyt` library. This collector will be capable of reading both simple variables and complex nested structures (e.g., `ScadaInterface`).

## Library Requirements
- **Repository**: [https://github.com/aphyt/aphytcomm](https://github.com/aphyt/aphytcomm)
- **Installation**: Use `pip install aphyt`. For SpeedBee, ensure the library is accessible in the environment's `site-packages`.
- **Author**: Joseph Ryan (aphyt).

## Critical Compatibility Fix (Python 3.11+)
> [!IMPORTANT]
> A manual fix is required for the `aphyt` library when running on Python 3.11+ due to a syntax error in f-strings.

### Fix details in `aphyt/cip/cip.py`:
In the `get_message` method (lines ~89-98), change the outer f-string quotes to double quotes to avoid collisions with the inner `'utf-8'` string:
```python
# Before (Error)
message = (f'\nCIP reply contained a general status code {binascii.hexlify(self.status).decode('utf-8')}\n'
           f'{cip_status_dictionary[self.status][0]}\n{cip_status_dictionary[self.status][1]}\n')

# After (Fixed)
message = (f"\nCIP reply contained a general status code {binascii.hexlify(self.status).decode('utf-8')}\n"
           f"{cip_status_dictionary[self.status][0]}\n{cip_status_dictionary[self.status][1]}\n")
```

## Proposed Changes

### [Core Logic]
The collector will be implemented as a Python class inheriting from the SpeedBee Synapse component base.

#### [NEW] [omron_synapse_collector.py](file:///c:/Users/giuseppe.defrance/EthIP/omron_synapse_collector.py)
This file will contain the main execution loop:
- **Connection Management**: Persistent session handling with the PLC at `172.16.224.111`.
- **Data Discovery**: Optional recursive browsing of the `ScadaInterface` structure to map all members.
- **Polling Loop**: Scheduled reading of specified tags and structures.
- **Data Transformation**: Converting `aphyt` custom types (`CIPStructure`, `CIPArray`, `CIPString`) into standard Python types for Synapse ingestion.

### [Configuration]
The component will require a JSON configuration defining the device parameters.

#### [NEW] [omron_collector_config.json](file:///c:/Users/giuseppe.defrance/EthIP/omron_collector_config.json)
- `PLC_IP`: 172.16.224.111
- `Root_Tag`: "ScadaInterface"
- `Polling_Interval_ms`: 1000
- `Complex_Type_Parsing`: true

## Verification Plan

### Automated Tests
- **Unit Testing**: Validate the `to_standard_type()` conversion logic with dummy data.
- **Integration Testing**: Run the collector against the live PLC (if available) and verify the output using the existing `omron_structure_browser.py` results as a baseline.

### Manual Verification
- Deploy the `.py` and `.json` files to the SpeedBee Synapse `source/python` directory.
- Verify the component appears in the Synapse Collector list.
- Check the Synapse dashboard/logs to ensure `ScadaInterface.Egress` values are updating correctly.
