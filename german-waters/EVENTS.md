# Table of Contents

- [DE.Waters.Hydrology](#message-group-dewatershydrology)
  - [DE.Waters.Hydrology.Station](#message-dewatershydrologystation)
  - [DE.Waters.Hydrology.WaterLevelObservation](#message-dewatershydrologywaterlevelobservation)
- [DE.Waters.Hydrology.mqtt](#message-group-dewatershydrologymqtt)
  - [DE.Waters.Hydrology.mqtt.Station](#message-dewatershydrologymqttstation)
  - [DE.Waters.Hydrology.mqtt.WaterLevelObservation](#message-dewatershydrologymqttwaterlevelobservation)

---

## Message Group: DE.Waters.Hydrology
---
### Message: DE.Waters.Hydrology.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Waters.Hydrology.Station` |
| `source` |  | `` | `False` | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `water_body` | *string* | - | `True` |  |
| `state` | *string* | - | `False` |  |
| `region` | *string* | - | `False` |  |
| `provider` | *string* | - | `True` |  |
| `latitude` | *double* | - | `False` |  |
| `longitude` | *double* | - | `False` |  |
| `river_km` | *double* | - | `False` |  |
| `altitude` | *double* | - | `False` |  |
| `station_type` | *string* | - | `False` |  |
| `warn_level_cm` | *double* | - | `False` |  |
| `alarm_level_cm` | *double* | - | `False` |  |
| `warn_level_m3s` | *double* | - | `False` |  |
| `alarm_level_m3s` | *double* | - | `False` |  |
---
### Message: DE.Waters.Hydrology.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Waters.Hydrology.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `provider` | *string* | - | `True` |  |
| `water_body` | *string* | - | `True` | Name of the water body the station observes (e.g. 'Rhein', 'Donau', 'Elbe'). Sourced by the bridge from the per-provider station catalog (Station.water_body field) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {water_body} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `water_level` | *double* | - | `False` |  |
| `water_level_unit` | *string* | - | `False` |  |
| `water_level_timestamp` | *datetime* | - | `False` |  |
| `discharge` | *double* | - | `False` |  |
| `discharge_unit` | *string* | - | `False` |  |
| `discharge_timestamp` | *datetime* | - | `False` |  |
| `trend` | *int32* | - | `False` |  |
| `situation` | *int32* | - | `False` |  |
## Message Group: DE.Waters.Hydrology.mqtt
---
### Message: DE.Waters.Hydrology.mqtt.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Waters.Hydrology.Station` |
| `source` |  | `` | `False` | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `water_body` | *string* | - | `True` |  |
| `state` | *string* | - | `False` |  |
| `region` | *string* | - | `False` |  |
| `provider` | *string* | - | `True` |  |
| `latitude` | *double* | - | `False` |  |
| `longitude` | *double* | - | `False` |  |
| `river_km` | *double* | - | `False` |  |
| `altitude` | *double* | - | `False` |  |
| `station_type` | *string* | - | `False` |  |
| `warn_level_cm` | *double* | - | `False` |  |
| `alarm_level_cm` | *double* | - | `False` |  |
| `warn_level_m3s` | *double* | - | `False` |  |
| `alarm_level_m3s` | *double* | - | `False` |  |
---
### Message: DE.Waters.Hydrology.mqtt.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.Waters.Hydrology.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `provider` | *string* | - | `True` |  |
| `water_body` | *string* | - | `True` | Name of the water body the station observes (e.g. 'Rhein', 'Donau', 'Elbe'). Sourced by the bridge from the per-provider station catalog (Station.water_body field) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {water_body} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `water_level` | *double* | - | `False` |  |
| `water_level_unit` | *string* | - | `False` |  |
| `water_level_timestamp` | *datetime* | - | `False` |  |
| `discharge` | *double* | - | `False` |  |
| `discharge_unit` | *string* | - | `False` |  |
| `discharge_timestamp` | *datetime* | - | `False` |  |
| `trend` | *int32* | - | `False` |  |
| `situation` | *int32* | - | `False` |  |
