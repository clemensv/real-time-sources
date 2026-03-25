# Events

This document describes the CloudEvents messages produced by the Waterinfo VMM bridge.

## Message Group: BE.Vlaanderen.Waterinfo.VMM

### BE.Vlaanderen.Waterinfo.VMM.Station

Reference data for monitoring stations.

- **CloudEvents Type**: `BE.Vlaanderen.Waterinfo.VMM.Station`
- **CloudEvents Source**: `https://waterinfo.vlaanderen.be`
- **Schema**: JSON
- **Frequency**: Sent once at startup

| Field | Type | Description |
|-------|------|-------------|
| `station_no` | string | Station number/code (e.g., "L04_007") |
| `station_name` | string | Station name (e.g., "Wijnegem/Groot Schijn") |
| `station_id` | string | Numeric station identifier |
| `station_latitude` | number | Latitude in WGS84 |
| `station_longitude` | number | Longitude in WGS84 |
| `river_name` | string | Name of the river or waterway |
| `stationparameter_name` | string | Parameter measured (e.g., H for water level) |
| `ts_id` | string | Time series identifier |
| `ts_unitname` | string | Unit of measurement (e.g., meter) |

### BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading

Real-time water level measurements.

- **CloudEvents Type**: `BE.Vlaanderen.Waterinfo.VMM.WaterLevelReading`
- **CloudEvents Source**: `https://waterinfo.vlaanderen.be`
- **Schema**: JSON
- **Frequency**: Every 15 minutes

| Field | Type | Description |
|-------|------|-------------|
| `ts_id` | string | Time series identifier |
| `station_no` | string | Station number/code |
| `station_name` | string | Station name |
| `timestamp` | string (date-time) | Measurement timestamp in ISO 8601 UTC |
| `value` | number | Measured value in the specified unit |
| `unit_name` | string | Unit of measurement (e.g., "meter") |
| `parameter_name` | string | Parameter code (H = water level) |
