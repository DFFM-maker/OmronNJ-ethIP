# Task: SpeedBee Synapse Collector for Omron NJ/NX

## Objective
Establish a reliable data collection bridge between Omron NJ/NX PLCs and the SpeeDBee Synapse platform using the `aphyt` EtherNet/IP library.

## Status
- [x] Connectivity Research: Verified `aphyt` works for simple and complex (Structure/Array) tags.
    - [x] Repository: [aphyt/aphytcomm](https://github.com/aphyt/aphytcomm)
    - [x] Patch: Applied Python 3.11+ f-string fix to `aphyt/cip/cip.py`.
- [x] Structure Browsing: Implemented a recursive browser for `ScadaInterface`.
- [x] Documentation: Created implementation plan and task list in `docs/`. [DONE]
- [ ] Development: Create the SpeeDBee Synapse Python component (`.py` + `.json` config).
- [ ] Integration: Map `ScadaInterface` members to Synapse data points.
- [ ] Verification: Test data throughput and stability in the Synapse environment.
