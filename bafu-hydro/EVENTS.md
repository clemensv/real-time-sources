# BAFU Hydrology Bridge Usage Guide Events

MQTT/5.0 transport variants of the BAFU Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/... The {water_body_name} placeholder is sourced from the upstream existenz.ch station catalog (BAFU/FOEN field 'water-body-name', e.g. 'Rhein', 'Aare') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole rivers / lakes (e.g. hydro/ch/bafu/bafu-hydro/rhein/+/water-level).

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

### Endpoint `CH.BAFU.Hydrology.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`CH.BAFU.Hydrology`](#messagegroup-chbafuhydrology) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `bafu-hydro` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `CH.BAFU.Hydrology.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`CH.BAFU.Hydrology.mqtt`](#messagegroup-chbafuhydrologymqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `CH.BAFU.Hydrology`
<a id="messagegroup-chbafuhydrology"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `CH.BAFU.Hydrology.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `CH.BAFU.Hydrology.Station`
<a id="message-chbafuhydrologystation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CH.BAFU.Hydrology.jstruct/schemas/CH.BAFU.Hydrology.Station`](#schema-chbafuhydrologystation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CH.BAFU.Hydrology.Station` |
| `source` |  | `string` | `False` | `https://www.hydrodaten.admin.ch` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CH.BAFU.Hydrology.Kafka` | `KAFKA` | topic `bafu-hydro`; key `{station_id}` |

#### Message `CH.BAFU.Hydrology.WaterLevelObservation`
<a id="message-chbafuhydrologywaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CH.BAFU.Hydrology.jstruct/schemas/CH.BAFU.Hydrology.WaterLevelObservation`](#schema-chbafuhydrologywaterlevelobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CH.BAFU.Hydrology.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://www.hydrodaten.admin.ch` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CH.BAFU.Hydrology.Kafka` | `KAFKA` | topic `bafu-hydro`; key `{station_id}` |

### Messagegroup `CH.BAFU.Hydrology.mqtt`
<a id="messagegroup-chbafuhydrologymqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants of the BAFU Hydrology CloudEvents, mapping each message to a retained, QoS-1 Unified Namespace topic under hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/... The {water_body_name} placeholder is sourced from the upstream existenz.ch station catalog (BAFU/FOEN field 'water-body-name', e.g. 'Rhein', 'Aare') and normalized by the bridge to lowercase kebab-case before publishing so subscribers can wildcard whole rivers / lakes (e.g. hydro/ch/bafu/bafu-hydro/rhein/+/water-level). |
| Transport bindings | `CH.BAFU.Hydrology.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `CH.BAFU.Hydrology.mqtt.Station`
<a id="message-chbafuhydrologymqttstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CH.BAFU.Hydrology.jstruct/schemas/CH.BAFU.Hydrology.Station`](#schema-chbafuhydrologystation) |
| Base message chain | `/messagegroups/CH.BAFU.Hydrology/messages/CH.BAFU.Hydrology.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CH.BAFU.Hydrology.Station` |
| `source` |  | `string` | `False` | `https://www.hydrodaten.admin.ch` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CH.BAFU.Hydrology.Mqtt` | `MQTT/5.0` | topic `hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `CH.BAFU.Hydrology.mqtt.WaterLevelObservation`
<a id="message-chbafuhydrologymqttwaterlevelobservation"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevelObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CH.BAFU.Hydrology.jstruct/schemas/CH.BAFU.Hydrology.WaterLevelObservation`](#schema-chbafuhydrologywaterlevelobservation) |
| Base message chain | `/messagegroups/CH.BAFU.Hydrology/messages/CH.BAFU.Hydrology.WaterLevelObservation` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CH.BAFU.Hydrology.WaterLevelObservation` |
| `source` |  | `string` | `False` | `https://www.hydrodaten.admin.ch` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CH.BAFU.Hydrology.Mqtt` | `MQTT/5.0` | topic `hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/water-level` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `hydro/ch/bafu/bafu-hydro/{water_body_name}/{station_id}/water-level` |
| QoS | 1 |
| Retain | True |

## Schemagroups

### Schemagroup `CH.BAFU.Hydrology.jstruct`
<a id="schemagroup-chbafuhydrologyjstruct"></a>

#### Schema `CH.BAFU.Hydrology.Station`
<a id="schema-chbafuhydrologystation"></a>

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
| $id | `https://example.com/schemas/CH/BAFU/Hydrology/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Station

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/CH/BAFU/Hydrology/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `name` | `string` | `True` |  | - | - | - |
| `water_body_name` | `string` | `False` |  | - | - | - |
| `water_body_type` | `string` | `False` |  | - | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |

#### Schema `CH.BAFU.Hydrology.WaterLevelObservation`
<a id="schema-chbafuhydrologywaterlevelobservation"></a>

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
| $id | `https://example.com/schemas/CH/BAFU/Hydrology/WaterLevelObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WaterLevelObservation`
<a id="schema-node-waterlevelobservation"></a>

WaterLevelObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/CH/BAFU/Hydrology/WaterLevelObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | - | - | - |
| `water_body_name` | `string` | `True` | Name of the water body the station observes (BAFU/FOEN 'water-body-name' field, e.g. 'Rhein', 'Aare', 'Bodensee'). Sourced by the bridge from the station catalog (existenz.ch /apiv1/hydro/locations endpoint, details.water-body-name) and propagated onto every observation so subscribers do not need an out-of-band catalog join to route by river / lake. Used as the {water_body_name} segment of the MQTT/UNS topic and normalized to lowercase kebab-case before publishing. | - | - | - |
| `water_level` | `double` | `False` |  | - | - | - |
| `water_level_unit` | `string` | `False` |  | - | - | - |
| `water_level_timestamp` | `datetime` | `False` |  | - | - | - |
| `discharge` | `double` | `False` |  | - | - | - |
| `discharge_unit` | `string` | `False` |  | - | - | - |
| `discharge_timestamp` | `datetime` | `False` |  | - | - | - |
| `water_temperature` | `double` | `False` |  | - | - | - |
| `water_temperature_unit` | `string` | `False` |  | - | - | - |
| `water_temperature_timestamp` | `datetime` | `False` |  | - | - | - |

### Schemagroup `CH.BAFU.Hydrology.avro`
<a id="schemagroup-chbafuhydrologyavro"></a>

#### Schema `CH.BAFU.Hydrology.Station`
<a id="schema-chbafuhydrologystation"></a>

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
| Namespace | CH.BAFU.Hydrology |
| Type | `record` |
| Doc | Station |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `name` | `string` |  | `-` |
| `water_body_name` | `null` \| `string` |  | `-` |
| `water_body_type` | `null` \| `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |

#### Schema `CH.BAFU.Hydrology.WaterLevelObservation`
<a id="schema-chbafuhydrologywaterlevelobservation"></a>

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
| Namespace | CH.BAFU.Hydrology |
| Type | `record` |
| Doc | WaterLevelObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `water_body_name` | `string` | Name of the water body the station observes (BAFU/FOEN 'water-body-name', e.g. 'Rhein'). Sourced by the bridge from the station catalog and propagated to telemetry so consumers can route by river/lake without a separate catalog join. | `-` |
| `water_level` | `null` \| `double` |  | `-` |
| `water_level_unit` | `null` \| `string` |  | `-` |
| `water_level_timestamp` | `null` \| `string` |  | `-` |
| `discharge` | `null` \| `double` |  | `-` |
| `discharge_unit` | `null` \| `string` |  | `-` |
| `discharge_timestamp` | `null` \| `string` |  | `-` |
| `water_temperature` | `null` \| `double` |  | `-` |
| `water_temperature_unit` | `null` \| `string` |  | `-` |
| `water_temperature_timestamp` | `null` \| `string` |  | `-` |
