# ČHMÚ Hydrological Data Bridge Events

This document describes the events that are emitted by the ČHMÚ Hydrological Data Bridge.

- [CZ.Gov.CHMI.Hydro](#message-group-czgovchmihydro)
  - [CZ.Gov.CHMI.Hydro.Station](#message-czgovchmihydrostation)
  - [CZ.Gov.CHMI.Hydro.WaterLevelObservation](#message-czgovchmihydrowaterlevelobservation)

---

## Message Group: CZ.Gov.CHMI.Hydro

---

### Message: CZ.Gov.CHMI.Hydro.Station

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `CZ.Gov.CHMI.Hydro.Station` |
| `source` | Source Feed URL | `uritemplate` | `True` | `https://opendata.chmi.cz` |

#### Schema:

##### Record: Station

*A hydrological station from ČHMÚ.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | Unique station identifier (e.g. 0-203-1-001000) |
| `dbc` | *string* | Station database code |
| `station_name` | *string* | Station name |
| `stream_name` | *string* | River or stream name |
| `latitude` | *number* | Latitude in WGS84 |
| `longitude` | *number* | Longitude in WGS84 |
| `flood_level_1` | *number* (nullable) | 1st degree flood warning water level in cm |
| `flood_level_2` | *number* (nullable) | 2nd degree flood warning water level in cm |
| `flood_level_3` | *number* (nullable) | 3rd degree flood warning water level in cm |
| `flood_level_4` | *number* (nullable) | Extreme flood warning water level in cm |
| `has_forecast` | *boolean* | Whether the station provides forecast data |

---

### Message: CZ.Gov.CHMI.Hydro.WaterLevelObservation

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `CZ.Gov.CHMI.Hydro.WaterLevelObservation` |
| `source` | Source Feed URL | `uritemplate` | `True` | `https://opendata.chmi.cz` |

#### Schema:

##### Record: WaterLevelObservation

*A water level observation from ČHMÚ.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `station_id` | *string* | Station identifier |
| `station_name` | *string* | Station name |
| `stream_name` | *string* | River or stream name |
| `water_level` | *number* (nullable) | Water level in cm |
| `water_level_timestamp` | *string* (nullable) | Water level measurement timestamp (ISO 8601) |
| `discharge` | *number* (nullable) | Discharge (flow rate) in m³/s |
| `discharge_timestamp` | *string* (nullable) | Discharge measurement timestamp (ISO 8601) |
| `water_temperature` | *number* (nullable) | Water temperature in °C |
| `water_temperature_timestamp` | *string* (nullable) | Water temperature measurement timestamp (ISO 8601) |
