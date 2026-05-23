# CHMI Hydrology Bridge Events

This document describes the events emitted by the Czech CHMI HYDRO bridge.

- [CZ.Gov.CHMI.Hydro](#message-group-czgovchmihydro)
  - [CZ.Gov.CHMI.Hydro.Station](#message-czgovchmihydrostation)
  - [CZ.Gov.CHMI.Hydro.WaterLevelObservation](#message-czgovchmihydrowaterlevelobservation)
- [CZ.Gov.CHMI.Hydro.mqtt](#message-group-czgovchmihydromqtt)
  - [CZ.Gov.CHMI.Hydro.mqtt.Station](#message-czgovchmihydromqttstation)
  - [CZ.Gov.CHMI.Hydro.mqtt.WaterLevelObservation](#message-czgovchmihydromqttwaterlevelobservation)

---

## Message Group: CZ.Gov.CHMI.Hydro
---
### Message: CZ.Gov.CHMI.Hydro.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `CZ.Gov.CHMI.Hydro.Station` |
| `source` |  | `` | `False` | `https://opendata.chmi.cz` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `dbc` | *string* (optional) | - | `False` |  |
| `station_name` | *string* | - | `True` |  |
| `stream_name` | *string* | - | `True` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
| `flood_level_1` | *double* (optional) | - | `False` |  |
| `flood_level_2` | *double* (optional) | - | `False` |  |
| `flood_level_3` | *double* (optional) | - | `False` |  |
| `flood_level_4` | *double* (optional) | - | `False` |  |
| `has_forecast` | *boolean* (optional) | - | `False` |  |
---
### Message: CZ.Gov.CHMI.Hydro.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `CZ.Gov.CHMI.Hydro.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://opendata.chmi.cz` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `stream_name` | *string* | - | `True` | Name of the watercourse / stream the station observes (Czech: 'tok', e.g. 'Vltava', 'Labe', 'Morava'). Sourced by the bridge from the CHMI hydrology station catalog and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {stream_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `water_level` | *double* (optional) | - | `False` |  |
| `water_level_timestamp` | *datetime* (optional) | - | `False` |  |
| `discharge` | *double* (optional) | - | `False` |  |
| `discharge_timestamp` | *datetime* (optional) | - | `False` |  |
| `water_temperature` | *double* (optional) | - | `False` |  |
| `water_temperature_timestamp` | *datetime* (optional) | - | `False` |  |
## Message Group: CZ.Gov.CHMI.Hydro.mqtt
---
### Message: CZ.Gov.CHMI.Hydro.mqtt.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `CZ.Gov.CHMI.Hydro.Station` |
| `source` |  | `` | `False` | `https://opendata.chmi.cz` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `dbc` | *string* (optional) | - | `False` |  |
| `station_name` | *string* | - | `True` |  |
| `stream_name` | *string* | - | `True` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
| `flood_level_1` | *double* (optional) | - | `False` |  |
| `flood_level_2` | *double* (optional) | - | `False` |  |
| `flood_level_3` | *double* (optional) | - | `False` |  |
| `flood_level_4` | *double* (optional) | - | `False` |  |
| `has_forecast` | *boolean* (optional) | - | `False` |  |
---
### Message: CZ.Gov.CHMI.Hydro.mqtt.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `CZ.Gov.CHMI.Hydro.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://opendata.chmi.cz` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `stream_name` | *string* | - | `True` | Name of the watercourse / stream the station observes (Czech: 'tok', e.g. 'Vltava', 'Labe', 'Morava'). Sourced by the bridge from the CHMI hydrology station catalog and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {stream_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `water_level` | *double* (optional) | - | `False` |  |
| `water_level_timestamp` | *datetime* (optional) | - | `False` |  |
| `discharge` | *double* (optional) | - | `False` |  |
| `discharge_timestamp` | *datetime* (optional) | - | `False` |  |
| `water_temperature` | *double* (optional) | - | `False` |  |
| `water_temperature_timestamp` | *datetime* (optional) | - | `False` |  |
