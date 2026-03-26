# Events

This document describes the CloudEvents messages produced by the RWS Waterwebservices bridge.

## Message Group: NL.RWS.Waterwebservices

### NL.RWS.Waterwebservices.Station

Reference data for monitoring stations.

- **CloudEvents Type**: `NL.RWS.Waterwebservices.Station`
- **CloudEvents Source**: `https://waterwebservices.rijkswaterstaat.nl`
- **Schema**: JSON
- **Frequency**: Sent once at startup

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | Station code (e.g., "HOlv") |
| `name` | string | Station name (e.g., "Hoek van Holland") |
| `latitude` | number | Latitude (Y coordinate) |
| `longitude` | number | Longitude (X coordinate) |
| `coordinate_system` | string | Coordinate reference system |

### NL.RWS.Waterwebservices.WaterLevelObservation

Real-time water level measurements.

- **CloudEvents Type**: `NL.RWS.Waterwebservices.WaterLevelObservation`
- **CloudEvents Source**: `https://waterwebservices.rijkswaterstaat.nl`
- **Schema**: JSON
- **Frequency**: Every 10 minutes

| Field | Type | Description |
|-------|------|-------------|
| `location_code` | string | Location code |
| `location_name` | string | Location name |
| `timestamp` | string (date-time) | Measurement timestamp in ISO 8601 |
| `value` | number | Measured water level value in cm relative to NAP |
| `unit` | string | Unit of measurement (e.g., "cm") |
| `quality_code` | string | Quality value code (00=good, 99=gap) |
| `status` | string | Status (e.g., "Ongecontroleerd") |
| `compartment` | string | Compartment code (OW=surface water) |
| `parameter` | string | Parameter code (WATHTE=water height) |
