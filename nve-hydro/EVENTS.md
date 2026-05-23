# NVE Hydrology Bridge Events

This document describes the events emitted by the Norwegian NVE HydAPI bridge.

- [NO.NVE.Hydrology](#message-group-nonvehydrology)
  - [NO.NVE.Hydrology.Station](#message-nonvehydrologystation)
  - [NO.NVE.Hydrology.WaterLevelObservation](#message-nonvehydrologywaterlevelobservation)
- [NO.NVE.Hydrology.mqtt](#message-group-nonvehydrologymqtt)
  - [NO.NVE.Hydrology.mqtt.Station](#message-nonvehydrologymqttstation)
  - [NO.NVE.Hydrology.mqtt.WaterLevelObservation](#message-nonvehydrologymqttwaterlevelobservation)

---

## Message Group: NO.NVE.Hydrology
---
### Message: NO.NVE.Hydrology.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.NVE.Hydrology.Station` |
| `source` |  | `` | `False` | `https://hydapi.nve.no` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `river_name` | *string* | - | `False` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
| `masl` | *double* | - | `False` |  |
| `council_name` | *string* | - | `False` |  |
| `county_name` | *string* | - | `False` |  |
| `drainage_basin_area` | *double* | - | `False` |  |
---
### Message: NO.NVE.Hydrology.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.NVE.Hydrology.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://hydapi.nve.no` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `river_name` | *string* | - | `True` | Name of the river the station observes (NVE HydAPI 'riverName' field, in Norwegian 'Vassdrag', e.g. 'Glomma', 'Drammenselva'). Sourced by the bridge from the station catalog (https://hydapi.nve.no/api/v1/Stations) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {river_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `water_level` | *double* | - | `False` |  |
| `water_level_unit` | *string* | - | `False` |  |
| `water_level_timestamp` | *datetime* | - | `False` |  |
| `discharge` | *double* | - | `False` |  |
| `discharge_unit` | *string* | - | `False` |  |
| `discharge_timestamp` | *datetime* | - | `False` |  |
## Message Group: NO.NVE.Hydrology.mqtt
---
### Message: NO.NVE.Hydrology.mqtt.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.NVE.Hydrology.Station` |
| `source` |  | `` | `False` | `https://hydapi.nve.no` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `river_name` | *string* | - | `False` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
| `masl` | *double* | - | `False` |  |
| `council_name` | *string* | - | `False` |  |
| `county_name` | *string* | - | `False` |  |
| `drainage_basin_area` | *double* | - | `False` |  |
---
### Message: NO.NVE.Hydrology.mqtt.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NO.NVE.Hydrology.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://hydapi.nve.no` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `river_name` | *string* | - | `True` | Name of the river the station observes (NVE HydAPI 'riverName' field, in Norwegian 'Vassdrag', e.g. 'Glomma', 'Drammenselva'). Sourced by the bridge from the station catalog (https://hydapi.nve.no/api/v1/Stations) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {river_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `water_level` | *double* | - | `False` |  |
| `water_level_unit` | *string* | - | `False` |  |
| `water_level_timestamp` | *datetime* | - | `False` |  |
| `discharge` | *double* | - | `False` |  |
| `discharge_unit` | *string* | - | `False` |  |
| `discharge_timestamp` | *datetime* | - | `False` |  |
