# SYKE Hydrology API Bridge Events

This document describes the events emitted by the SYKE Hydrology API Bridge.

- [FI.SYKE.Hydrology](#message-group-fisykehydrology)
  - [FI.SYKE.Hydrology.Station](#message-fisykehydrologystation)
  - [FI.SYKE.Hydrology.WaterLevelObservation](#message-fisykehydrologywaterlevelobservation)

---

## Message Group: FI.SYKE.Hydrology
---
### Message: FI.SYKE.Hydrology.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `FI.SYKE.Hydrology.Station` |
| `source` |  | `` | `False` | `https://rajapinnat.ymparisto.fi` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `name` | *string* | - | `True` |  |
| `river_name` | *string* | - | `False` |  |
| `water_area_name` | *string* | - | `False` |  |
| `municipality` | *string* | - | `False` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
---
### Message: FI.SYKE.Hydrology.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `FI.SYKE.Hydrology.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://rajapinnat.ymparisto.fi` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `water_level` | *double* (optional) | - | `False` | Water level reading value in centimetres. Null when the station does not report a water level in the current polling window. |
| `water_level_unit` | *string* (optional) | - | `False` | Unit of measurement for water_level. Constant 'cm' when present, null when water_level is null. |
| `water_level_timestamp` | *datetime* (optional) | - | `False` | RFC3339 UTC timestamp (with 'Z' suffix) of the water level observation, derived from the SYKE 'Aika' field. Null when no water level is available. |
| `discharge` | *double* (optional) | - | `False` | Discharge (flow) reading value in cubic metres per second. Null for stations that do not measure discharge. |
| `discharge_unit` | *string* (optional) | - | `False` | Unit of measurement for discharge. Constant 'm3/s' when present, null when discharge is null. |
| `discharge_timestamp` | *datetime* (optional) | - | `False` | RFC3339 UTC timestamp (with 'Z' suffix) of the discharge observation, derived from the SYKE 'Aika' field. Null when no discharge is available. |
