# SMHI Hydrology API Bridge Events

This document describes the events that are emitted by the SMHI Hydrology API Bridge.

- [SE.Gov.SMHI.Hydro](#message-group-segovsmhihydro)
  - [SE.Gov.SMHI.Hydro.Station](#message-segovsmhihydrostation)
  - [SE.Gov.SMHI.Hydro.DischargeObservation](#message-segovsmhihydrodischargeobservation)
- [SE.Gov.SMHI.Hydro.mqtt](#message-group-segovsmhihydromqtt)
  - [SE.Gov.SMHI.Hydro.mqtt.Station](#message-segovsmhihydromqttstation)
  - [SE.Gov.SMHI.Hydro.mqtt.DischargeObservation](#message-segovsmhihydromqttdischargeobservation)

---

## Message Group: SE.Gov.SMHI.Hydro
---
### Message: SE.Gov.SMHI.Hydro.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `SE.Gov.SMHI.Hydro.Station` |
| `source` |  | `` | `False` | `https://opendata-download-hydroobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `name` | *string* | - | `True` |  |
| `owner` | *string* | - | `False` |  |
| `measuring_stations` | *string* | - | `False` |  |
| `region` | *int32* | - | `False` |  |
| `catchment_name` | *string* | - | `True` | Name of the catchment area the station belongs to (SMHI 'catchmentName' field, e.g. 'Torneälven', 'Dalälven'). Sourced by the bridge from the SMHI bulk API station catalog. When the catalog has no catchmentName for a station the bridge substitutes the lowercase sentinel 'unknown' so the field stays non-null and the {catchment_name} MQTT topic segment remains populated. Normalized to lowercase kebab-case before publishing. |
| `catchment_number` | *int32* | - | `False` |  |
| `catchment_size` | *double* | - | `False` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
---
### Message: SE.Gov.SMHI.Hydro.DischargeObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `SE.Gov.SMHI.Hydro.DischargeObservation` |
| `source` |  | `` | `False` | `https://opendata-download-hydroobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: DischargeObservation
*DischargeObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `catchment_name` | *string* | - | `True` | Name of the catchment area the station belongs to (SMHI 'catchmentName' field, e.g. 'Torneälven', 'Dalälven'). Sourced by the bridge from the SMHI bulk API station catalog and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by catchment. When the catalog has no catchmentName the bridge substitutes the lowercase sentinel 'unknown'. Used as the {catchment_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `timestamp` | *datetime* | - | `True` |  |
| `discharge` | *double* | - | `True` |  |
| `quality` | *string* | - | `False` |  |
## Message Group: SE.Gov.SMHI.Hydro.mqtt
---
### Message: SE.Gov.SMHI.Hydro.mqtt.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `SE.Gov.SMHI.Hydro.Station` |
| `source` |  | `` | `False` | `https://opendata-download-hydroobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `name` | *string* | - | `True` |  |
| `owner` | *string* | - | `False` |  |
| `measuring_stations` | *string* | - | `False` |  |
| `region` | *int32* | - | `False` |  |
| `catchment_name` | *string* | - | `True` | Name of the catchment area the station belongs to (SMHI 'catchmentName' field, e.g. 'Torneälven', 'Dalälven'). Sourced by the bridge from the SMHI bulk API station catalog. When the catalog has no catchmentName for a station the bridge substitutes the lowercase sentinel 'unknown' so the field stays non-null and the {catchment_name} MQTT topic segment remains populated. Normalized to lowercase kebab-case before publishing. |
| `catchment_number` | *int32* | - | `False` |  |
| `catchment_size` | *double* | - | `False` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
---
### Message: SE.Gov.SMHI.Hydro.mqtt.DischargeObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `SE.Gov.SMHI.Hydro.DischargeObservation` |
| `source` |  | `` | `False` | `https://opendata-download-hydroobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: DischargeObservation
*DischargeObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `catchment_name` | *string* | - | `True` | Name of the catchment area the station belongs to (SMHI 'catchmentName' field, e.g. 'Torneälven', 'Dalälven'). Sourced by the bridge from the SMHI bulk API station catalog and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by catchment. When the catalog has no catchmentName the bridge substitutes the lowercase sentinel 'unknown'. Used as the {catchment_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `timestamp` | *datetime* | - | `True` |  |
| `discharge` | *double* | - | `True` |  |
| `quality` | *string* | - | `False` |  |
