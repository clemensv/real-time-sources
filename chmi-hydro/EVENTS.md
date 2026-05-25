# ČHMÚ Hydrological Data Bridge Events

MQTT/5.0 transport variants of the CHMI Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/... The {stream_name} placeholder is sourced from the CHMI hydrology catalog (Czech: 'tok', e.g. 'Vltava', 'Labe', 'Morava') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole rivers (e.g. hydro/cz/chmi/chmi-hydro/vltava/+/water-level).

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

### Endpoint `CZ.Gov.CHMI.Hydro.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`CZ.Gov.CHMI.Hydro`](#messagegroup-czgovchmihydro) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `chmi-hydro` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `CZ.Gov.CHMI.Hydro.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`CZ.Gov.CHMI.Hydro.mqtt`](#messagegroup-czgovchmihydromqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `CZ.Gov.CHMI.Hydro`
<a id="messagegroup-czgovchmihydro"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `CZ.Gov.CHMI.Hydro.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `CZ.Gov.CHMI.Hydro.Station`
<a id="message-czgovchmihydrostation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CZ.Gov.CHMI.Hydro.jstruct/schemas/CZ.Gov.CHMI.Hydro.Station`](#schema-czgovchmihydrostation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CZ.Gov.CHMI.Hydro.Station` |
| `source` |  | `string` | `False` | `https://opendata.chmi.cz` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CZ.Gov.CHMI.Hydro.Kafka` | `KAFKA` | topic `chmi-hydro`; key `{station_id}` |

#### Message `CZ.Gov.CHMI.Hydro.WaterLevelObservation`
<a id="message-czgovchmihydrowaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CZ.Gov.CHMI.Hydro.jstruct/schemas/CZ.Gov.CHMI.Hydro.WaterLevelObservation`](#schema-czgovchmihydrowaterlevelobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CZ.Gov.CHMI.Hydro.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://opendata.chmi.cz` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CZ.Gov.CHMI.Hydro.Kafka` | `KAFKA` | topic `chmi-hydro`; key `{station_id}` |

### Messagegroup `CZ.Gov.CHMI.Hydro.mqtt`
<a id="messagegroup-czgovchmihydromqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the CHMI Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/... The {stream_name} placeholder is sourced from the CHMI hydrology catalog (Czech: 'tok', e.g. 'Vltava', 'Labe', 'Morava') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole rivers (e.g. hydro/cz/chmi/chmi-hydro/vltava/+/water-level). |
| Transport bindings | `CZ.Gov.CHMI.Hydro.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `CZ.Gov.CHMI.Hydro.mqtt.Station`
<a id="message-czgovchmihydromqttstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CZ.Gov.CHMI.Hydro.jstruct/schemas/CZ.Gov.CHMI.Hydro.Station`](#schema-czgovchmihydrostation) |
| Base message chain | `/messagegroups/CZ.Gov.CHMI.Hydro/messages/CZ.Gov.CHMI.Hydro.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CZ.Gov.CHMI.Hydro.Station` |
| `source` |  | `string` | `False` | `https://opendata.chmi.cz` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CZ.Gov.CHMI.Hydro.Mqtt` | `MQTT/5.0` | topic `hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `CZ.Gov.CHMI.Hydro.mqtt.WaterLevelObservation`
<a id="message-czgovchmihydromqttwaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CZ.Gov.CHMI.Hydro.jstruct/schemas/CZ.Gov.CHMI.Hydro.WaterLevelObservation`](#schema-czgovchmihydrowaterlevelobservation) |
| Base message chain | `/messagegroups/CZ.Gov.CHMI.Hydro/messages/CZ.Gov.CHMI.Hydro.WaterLevelObservation` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CZ.Gov.CHMI.Hydro.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://opendata.chmi.cz` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CZ.Gov.CHMI.Hydro.Mqtt` | `MQTT/5.0` | topic `hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/water-level` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/cz/chmi/chmi-hydro/{stream_name}/{station_id}/water-level` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `CZ.Gov.CHMI.Hydro.jstruct`
<a id="schemagroup-czgovchmihydrojstruct"></a>

#### Schema `CZ.Gov.CHMI.Hydro.Station`
<a id="schema-czgovchmihydrostation"></a>

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
| $id | `https://example.com/schemas/CZ/Gov/CHMI/Hydro/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/CZ/Gov/CHMI/Hydro/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `dbc` | `union` | `False` |  | - | - | - |
| `station_name` | `string` | `True` |  | - | - | - |
| `stream_name` | `string` | `True` |  | - | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |
| `flood_level_1` | `union` | `False` |  | - | - | - |
| `flood_level_2` | `union` | `False` |  | - | - | - |
| `flood_level_3` | `union` | `False` |  | - | - | - |
| `flood_level_4` | `union` | `False` |  | - | - | - |
| `has_forecast` | `union` | `False` |  | - | - | - |

#### Schema `CZ.Gov.CHMI.Hydro.WaterLevelObservation`
<a id="schema-czgovchmihydrowaterlevelobservation"></a>

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
| $id | `https://example.com/schemas/CZ/Gov/CHMI/Hydro/WaterLevelObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterLevelObservation`
<a id="schema-node-waterlevelobservation"></a>

WaterLevelObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/CZ/Gov/CHMI/Hydro/WaterLevelObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `station_name` | `string` | `True` |  | - | - | - |
| `stream_name` | `string` | `True` | Name of the watercourse / stream the station observes (Czech: 'tok', e.g. 'Vltava', 'Labe', 'Morava'). Sourced by the bridge from the CHMI hydrology station catalog and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river. Used as the {stream_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. | - | - | - |
| `water_level` | `union` | `False` |  | - | - | - |
| `water_level_timestamp` | `union` | `False` |  | - | - | - |
| `discharge` | `union` | `False` |  | - | - | - |
| `discharge_timestamp` | `union` | `False` |  | - | - | - |
| `water_temperature` | `union` | `False` |  | - | - | - |
| `water_temperature_timestamp` | `union` | `False` |  | - | - | - |

### Schemagroup `CZ.Gov.CHMI.Hydro.avro`
<a id="schemagroup-czgovchmihydroavro"></a>

#### Schema `CZ.Gov.CHMI.Hydro.Station`
<a id="schema-czgovchmihydrostation"></a>

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
| Namespace | CZ.Gov.CHMI.Hydro |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `dbc` | `null` \| `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `stream_name` | `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |
| `flood_level_1` | `null` \| `double` |  | `-` |
| `flood_level_2` | `null` \| `double` |  | `-` |
| `flood_level_3` | `null` \| `double` |  | `-` |
| `flood_level_4` | `null` \| `double` |  | `-` |
| `has_forecast` | `null` \| `boolean` |  | `-` |

#### Schema `CZ.Gov.CHMI.Hydro.WaterLevelObservation`
<a id="schema-czgovchmihydrowaterlevelobservation"></a>

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
| Namespace | CZ.Gov.CHMI.Hydro |
| Type | `record` |
| Doc | WaterLevelObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `station_name` | `string` |  | `-` |
| `stream_name` | `string` | Name of the watercourse / stream the station observes (Czech: 'tok'). Sourced by the bridge from the station catalog and propagated to telemetry so consumers can route by river without a separate catalog join. | `-` |
| `water_level` | `null` \| `double` |  | `-` |
| `water_level_timestamp` | `null` \| `string` |  | `-` |
| `discharge` | `null` \| `double` |  | `-` |
| `discharge_timestamp` | `null` \| `string` |  | `-` |
| `water_temperature` | `null` \| `double` |  | `-` |
| `water_temperature_timestamp` | `null` \| `string` |  | `-` |
