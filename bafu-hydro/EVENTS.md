# BAFU Hydrology Bridge Events

This document describes the events emitted by the Swiss BAFU/FOEN Hydrology bridge.

- [CH.BAFU.Hydrology](#message-group-chbafuhydrology)
  - [CH.BAFU.Hydrology.Station](#message-chbafuhydrologystation)
  - [CH.BAFU.Hydrology.WaterLevelObservation](#message-chbafuhydrologywaterlevelobservation)
- [CH.BAFU.Hydrology.mqtt](#message-group-chbafuhydrologymqtt)
  - [CH.BAFU.Hydrology.mqtt.Station](#message-chbafuhydrologymqttstation)
  - [CH.BAFU.Hydrology.mqtt.WaterLevelObservation](#message-chbafuhydrologymqttwaterlevelobservation)

---

## Message Group: CH.BAFU.Hydrology
---
### Message: CH.BAFU.Hydrology.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `CH.BAFU.Hydrology.Station` |
| `source` |  | `` | `False` | `https://www.hydrodaten.admin.ch` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `name` | *string* | - | `True` |  |
| `water_body_name` | *string* | - | `False` |  |
| `water_body_type` | *string* | - | `False` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
---
### Message: CH.BAFU.Hydrology.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `CH.BAFU.Hydrology.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://www.hydrodaten.admin.ch` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `water_body_name` | *string* | - | `True` | Name of the water body the station observes (BAFU/FOEN 'water-body-name' field, e.g. 'Rhein', 'Aare', 'Bodensee'). Sourced by the bridge from the station catalog (existenz.ch /apiv1/hydro/locations endpoint, details.water-body-name) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river / lake. Used as the {water_body_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `water_level` | *double* | - | `False` |  |
| `water_level_unit` | *string* | - | `False` |  |
| `water_level_timestamp` | *datetime* | - | `False` |  |
| `discharge` | *double* | - | `False` |  |
| `discharge_unit` | *string* | - | `False` |  |
| `discharge_timestamp` | *datetime* | - | `False` |  |
| `water_temperature` | *double* | - | `False` |  |
| `water_temperature_unit` | *string* | - | `False` |  |
| `water_temperature_timestamp` | *datetime* | - | `False` |  |
## Message Group: CH.BAFU.Hydrology.mqtt
---
### Message: CH.BAFU.Hydrology.mqtt.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `CH.BAFU.Hydrology.Station` |
| `source` |  | `` | `False` | `https://www.hydrodaten.admin.ch` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `name` | *string* | - | `True` |  |
| `water_body_name` | *string* | - | `False` |  |
| `water_body_type` | *string* | - | `False` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
---
### Message: CH.BAFU.Hydrology.mqtt.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `CH.BAFU.Hydrology.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://www.hydrodaten.admin.ch` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `water_body_name` | *string* | - | `True` | Name of the water body the station observes (BAFU/FOEN 'water-body-name' field, e.g. 'Rhein', 'Aare', 'Bodensee'). Sourced by the bridge from the station catalog (existenz.ch /apiv1/hydro/locations endpoint, details.water-body-name) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river / lake. Used as the {water_body_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `water_level` | *double* | - | `False` |  |
| `water_level_unit` | *string* | - | `False` |  |
| `water_level_timestamp` | *datetime* | - | `False` |  |
| `discharge` | *double* | - | `False` |  |
| `discharge_unit` | *string* | - | `False` |  |
| `discharge_timestamp` | *datetime* | - | `False` |  |
| `water_temperature` | *double* | - | `False` |  |
| `water_temperature_unit` | *string* | - | `False` |  |
| `water_temperature_timestamp` | *datetime* | - | `False` |  |
