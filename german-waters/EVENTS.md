# German Waters Bridge Events

MQTT/5.0 transport variants of the German Waters Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/de/wsv/german-waters/{water_body}/{station_id}/... The {water_body} placeholder is sourced from the per-provider station catalog (Station.water_body field, e.g. 'Rhein', 'Donau', 'Elbe') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole rivers (e.g. hydro/de/wsv/german-waters/rhein/+/water-level).

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `DE.Waters.Hydrology.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`DE.Waters.Hydrology`](#messagegroup-dewatershydrology) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `german-waters` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `DE.Waters.Hydrology.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`DE.Waters.Hydrology.mqtt`](#messagegroup-dewatershydrologymqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `DE.Waters.Hydrology`
<a id="messagegroup-dewatershydrology"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `DE.Waters.Hydrology.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `DE.Waters.Hydrology.Station`
<a id="message-dewatershydrologystation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Waters.Hydrology.jstruct/schemas/DE.Waters.Hydrology.Station`](#schema-dewatershydrologystation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Waters.Hydrology.Station` |
| `source` |  | `string` | `False` | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Waters.Hydrology.Kafka` | `KAFKA` | topic `german-waters`; key `{station_id}` |

#### Message `DE.Waters.Hydrology.WaterLevelObservation`
<a id="message-dewatershydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Waters.Hydrology.jstruct/schemas/DE.Waters.Hydrology.WaterLevelObservation`](#schema-dewatershydrologywaterlevelobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Waters.Hydrology.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Waters.Hydrology.Kafka` | `KAFKA` | topic `german-waters`; key `{station_id}` |

### Messagegroup `DE.Waters.Hydrology.mqtt`
<a id="messagegroup-dewatershydrologymqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the German Waters Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/de/wsv/german-waters/{water_body}/{station_id}/... The {water_body} placeholder is sourced from the per-provider station catalog (Station.water_body field, e.g. 'Rhein', 'Donau', 'Elbe') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole rivers (e.g. hydro/de/wsv/german-waters/rhein/+/water-level). |
| Transport bindings | `DE.Waters.Hydrology.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `DE.Waters.Hydrology.mqtt.Station`
<a id="message-dewatershydrologymqttstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Waters.Hydrology.jstruct/schemas/DE.Waters.Hydrology.Station`](#schema-dewatershydrologystation) |
| Base message chain | `/messagegroups/DE.Waters.Hydrology/messages/DE.Waters.Hydrology.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Waters.Hydrology.Station` |
| `source` |  | `string` | `False` | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Waters.Hydrology.Mqtt` | `MQTT/5.0` | topic `hydro/de/wsv/german-waters/{water_body}/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/de/wsv/german-waters/{water_body}/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `DE.Waters.Hydrology.mqtt.WaterLevelObservation`
<a id="message-dewatershydrologymqttwaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.Waters.Hydrology.jstruct/schemas/DE.Waters.Hydrology.WaterLevelObservation`](#schema-dewatershydrologywaterlevelobservation) |
| Base message chain | `/messagegroups/DE.Waters.Hydrology/messages/DE.Waters.Hydrology.WaterLevelObservation` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.Waters.Hydrology.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://github.com/clemensv/real-time-sources/german-waters` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.Waters.Hydrology.Mqtt` | `MQTT/5.0` | topic `hydro/de/wsv/german-waters/{water_body}/{station_id}/water-level` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/de/wsv/german-waters/{water_body}/{station_id}/water-level` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `DE.Waters.Hydrology.jstruct`
<a id="schemagroup-dewatershydrologyjstruct"></a>

#### Schema `DE.Waters.Hydrology.Station`
<a id="schema-dewatershydrologystation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Waters/Hydrology/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Waters/Hydrology/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `station_name` | `string` | `True` |  | - | - | - |
| `water_body` | `string` | `True` |  | altnames=`{"lang:de": "Gewaesser"}` | - | - |
| `state` | `string` | `False` |  | - | - | - |
| `region` | `string` | `False` |  | - | - | - |
| `provider` | `string` | `True` |  | - | - | - |
| `latitude` | `double` | `False` |  | - | - | - |
| `longitude` | `double` | `False` |  | - | - | - |
| `river_km` | `double` | `False` |  | - | - | - |
| `altitude` | `double` | `False` |  | altnames=`{"lang:de": "Hoehe"}` | - | - |
| `station_type` | `string` | `False` |  | - | - | - |
| `warn_level_cm` | `double` | `False` |  | - | - | - |
| `alarm_level_cm` | `double` | `False` |  | - | - | - |
| `warn_level_m3s` | `double` | `False` |  | - | - | - |
| `alarm_level_m3s` | `double` | `False` |  | - | - | - |

#### Schema `DE.Waters.Hydrology.WaterLevelObservation`
<a id="schema-dewatershydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Waters/Hydrology/WaterLevelObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterLevelObservation`
<a id="schema-node-waterlevelobservation"></a>

WaterLevelObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/Waters/Hydrology/WaterLevelObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `provider` | `string` | `True` |  | - | - | - |
| `water_body` | `string` | `True` | Name of the water body the station observes (e.g. 'Rhein', 'Donau', 'Elbe'). Sourced by the bridge from the per-provider station catalog (Station.water_body field) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {water_body} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. | - | - | - |
| `water_level` | `double` | `False` |  | - | - | - |
| `water_level_unit` | `string` | `False` |  | - | - | - |
| `water_level_timestamp` | `datetime` | `False` |  | - | - | - |
| `discharge` | `double` | `False` |  | - | - | - |
| `discharge_unit` | `string` | `False` |  | - | - | - |
| `discharge_timestamp` | `datetime` | `False` |  | - | - | - |
| `trend` | `int32` | `False` |  | - | - | - |
| `situation` | `int32` | `False` |  | - | - | - |

### Schemagroup `DE.Waters.Hydrology.avro`
<a id="schemagroup-dewatershydrologyavro"></a>

#### Schema `DE.Waters.Hydrology.Station`
<a id="schema-dewatershydrologystation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | DE.Waters.Hydrology |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `water_body` | `string` |  | `-` |
| `state` | `null` \| `string` |  | `-` |
| `region` | `null` \| `string` |  | `-` |
| `provider` | `string` |  | `-` |
| `latitude` | `null` \| `double` |  | `-` |
| `longitude` | `null` \| `double` |  | `-` |
| `river_km` | `null` \| `double` |  | `-` |
| `altitude` | `null` \| `double` |  | `-` |
| `station_type` | `null` \| `string` |  | `-` |
| `warn_level_cm` | `null` \| `double` |  | `-` |
| `alarm_level_cm` | `null` \| `double` |  | `-` |
| `warn_level_m3s` | `null` \| `double` |  | `-` |
| `alarm_level_m3s` | `null` \| `double` |  | `-` |

#### Schema `DE.Waters.Hydrology.WaterLevelObservation`
<a id="schema-dewatershydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Namespace | DE.Waters.Hydrology |
| Type | `record` |
| Doc | WaterLevelObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `provider` | `string` |  | `-` |
| `water_body` | `string` | Name of the water body the station observes (e.g. 'Rhein', 'Donau', 'Elbe'). Mirrored from the JSON Structure WaterLevelObservation schema; sourced by the bridge from the per-provider station catalog and propagated onto every observation. Required non-null string. | `-` |
| `water_level` | `null` \| `double` |  | `-` |
| `water_level_unit` | `null` \| `string` |  | `-` |
| `water_level_timestamp` | `null` \| `string` |  | `-` |
| `discharge` | `null` \| `double` |  | `-` |
| `discharge_unit` | `null` \| `string` |  | `-` |
| `discharge_timestamp` | `null` \| `string` |  | `-` |
| `trend` | `null` \| `int` |  | `-` |
| `situation` | `null` \| `int` |  | `-` |
