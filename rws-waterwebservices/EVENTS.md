# Table of Contents

- [NL.RWS.Waterwebservices](#message-group-nlrwswaterwebservices)
  - [NL.RWS.Waterwebservices.Station](#message-nlrwswaterwebservicesstation)
  - [NL.RWS.Waterwebservices.WaterLevelObservation](#message-nlrwswaterwebserviceswaterlevelobservation)
- [NL.RWS.Waterwebservices.mqtt](#message-group-nlrwswaterwebservicesmqtt)
  - [NL.RWS.Waterwebservices.mqtt.Station](#message-nlrwswaterwebservicesmqttstation)
  - [NL.RWS.Waterwebservices.mqtt.WaterLevelObservation](#message-nlrwswaterwebservicesmqttwaterlevelobservation)

---

## Message Group: NL.RWS.Waterwebservices
---
### Message: NL.RWS.Waterwebservices.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NL.RWS.Waterwebservices.Station` |
| `source` |  | `` | `False` | `https://waterwebservices.rijkswaterstaat.nl` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_code` | *string* | - | `True` |  |
| `name` | *string* | - | `True` |  |
| `water_body` | *string* | - | `True` | Display name of the water body / monitoring location (RWS catalog Locatie.Naam field, e.g. 'Hoek van Holland', 'IJmuiden Buitenhaven'). Sourced by the bridge from the station catalog and propagated onto every station event so subscribers do not need an out-of-band catalog join. Used as the {water_body} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
| `coordinate_system` | *string* | - | `False` |  |
---
### Message: NL.RWS.Waterwebservices.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NL.RWS.Waterwebservices.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://waterwebservices.rijkswaterstaat.nl` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_code` | *string* | - | `True` |  |
| `water_body` | *string* | - | `True` | Display name of the water body / monitoring location (RWS catalog Locatie.Naam field, e.g. 'Hoek van Holland', 'IJmuiden Buitenhaven'). Sourced by the bridge from the station catalog at startup and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by location. Used as the {water_body} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `location_name` | *string* | - | `False` |  |
| `timestamp` | *datetime* | - | `True` |  |
| `value` | *double* | - | `True` |  |
| `unit` | *string* | - | `False` |  |
| `quality_code` | *string* | - | `False` |  |
| `status` | *string* | - | `False` |  |
| `compartment` | *string* | - | `False` |  |
| `parameter` | *string* | - | `False` |  |
## Message Group: NL.RWS.Waterwebservices.mqtt
---
### Message: NL.RWS.Waterwebservices.mqtt.Station
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NL.RWS.Waterwebservices.Station` |
| `source` |  | `` | `False` | `https://waterwebservices.rijkswaterstaat.nl` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

#### Schema:
##### Object: Station
*Station*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_code` | *string* | - | `True` |  |
| `name` | *string* | - | `True` |  |
| `water_body` | *string* | - | `True` | Display name of the water body / monitoring location (RWS catalog Locatie.Naam field, e.g. 'Hoek van Holland', 'IJmuiden Buitenhaven'). Sourced by the bridge from the station catalog and propagated onto every station event so subscribers do not need an out-of-band catalog join. Used as the {water_body} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
| `coordinate_system` | *string* | - | `False` |  |
---
### Message: NL.RWS.Waterwebservices.mqtt.WaterLevelObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `NL.RWS.Waterwebservices.WaterLevelObservation` |
| `source` |  | `` | `False` | `https://waterwebservices.rijkswaterstaat.nl` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

#### Schema:
##### Object: WaterLevelObservation
*WaterLevelObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_code` | *string* | - | `True` |  |
| `water_body` | *string* | - | `True` | Display name of the water body / monitoring location (RWS catalog Locatie.Naam field, e.g. 'Hoek van Holland', 'IJmuiden Buitenhaven'). Sourced by the bridge from the station catalog at startup and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by location. Used as the {water_body} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. |
| `location_name` | *string* | - | `False` |  |
| `timestamp` | *datetime* | - | `True` |  |
| `value` | *double* | - | `True` |  |
| `unit` | *string* | - | `False` |  |
| `quality_code` | *string* | - | `False` |  |
| `status` | *string* | - | `False` |  |
| `compartment` | *string* | - | `False` |  |
| `parameter` | *string* | - | `False` |  |
