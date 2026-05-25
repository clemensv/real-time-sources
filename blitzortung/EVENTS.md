# Blitzortung live lightning bridge Events

MQTT/5.0 non-retained UNS variant of the Blitzortung LightningStroke CloudEvent. Topic carries the source-scoped stroke id plus geohash5 (~5 km) and geohash7 (~150 m) cells so subscribers can wildcard by location at two zoom levels. QoS 0, retain=false — no LKV slot for a firehose.

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

### Endpoint `Blitzortung.Lightning.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Blitzortung.Lightning`](#messagegroup-blitzortunglightning) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `blitzortung` |
| Kafka key | `{source_id}/{stroke_id}` |
| Deployed | False |

### Endpoint `Blitzortung.Lightning.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`Blitzortung.Lightning.mqtt`](#messagegroup-blitzortunglightningmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |

## Messagegroups

### Messagegroup `Blitzortung.Lightning`
<a id="messagegroup-blitzortunglightning"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Blitzortung.Lightning.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Blitzortung.Lightning.LightningStroke`
<a id="message-blitzortunglightninglightningstroke"></a>

Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed. Each event represents one source-scoped stroke identifier with its observation time, coordinates, upstream delay and accuracy values, and optionally the detector participation flags carried in the public sta object.

| Field | Value |
| --- | --- |
| Name | LightningStroke |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Blitzortung.Lightning.jstruct/schemas/Blitzortung.Lightning.LightningStroke`](#schema-blitzortunglightninglightningstroke) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Blitzortung.Lightning.LightningStroke` |
| `source` |  | `string` | `False` | `wss://live.lightningmaps.org/` |
| `subject` |  | `uritemplate` | `False` | `{source_id}/{stroke_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Blitzortung.Lightning.Kafka` | `KAFKA` | topic `blitzortung`; key `{source_id}/{stroke_id}` |

### Messagegroup `Blitzortung.Lightning.mqtt`
<a id="messagegroup-blitzortunglightningmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 non-retained UNS variant of the Blitzortung LightningStroke CloudEvent. Topic carries the source-scoped stroke id plus geohash5 (~5 km) and geohash7 (~150 m) cells so subscribers can wildcard by location at two zoom levels. QoS 0, retain=false — no LKV slot for a firehose. |
| Transport bindings | `Blitzortung.Lightning.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `Blitzortung.Lightning.mqtt.LightningStroke`
<a id="message-blitzortunglightningmqttlightningstroke"></a>

Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed. Each event represents one source-scoped stroke identifier with its observation time, coordinates, upstream delay and accuracy values, and optionally the detector participation flags carried in the public sta object.

| Field | Value |
| --- | --- |
| Name | LightningStroke |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Blitzortung.Lightning.jstruct/schemas/Blitzortung.Lightning.LightningStroke`](#schema-blitzortunglightninglightningstroke) |
| Base message chain | `/messagegroups/Blitzortung.Lightning/messages/Blitzortung.Lightning.LightningStroke` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Blitzortung.Lightning.LightningStroke` |
| `source` |  | `string` | `False` | `wss://live.lightningmaps.org/` |
| `subject` |  | `uritemplate` | `False` | `{source_id}/{stroke_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Blitzortung.Lightning.Mqtt` | `MQTT/5.0` | topic `weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke` |
| Retain | False |

## Schemagroups

### Schemagroup `Blitzortung.Lightning.jstruct`
<a id="schemagroup-blitzortunglightningjstruct"></a>

#### Schema `Blitzortung.Lightning.LightningStroke`
<a id="schema-blitzortunglightninglightningstroke"></a>

| Field | Value |
| --- | --- |
| Name | LightningStroke |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Normalized live lightning-stroke payload from the public LightningMaps / Blitzortung websocket feed. The public websocket batches stroke objects keyed by a source-scoped id; this schema renames the compact upstream fields to explicit English names while preserving detector participation flags when they are requested from the feed. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/Blitzortung/Lightning/LightningStroke` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `LightningStroke`
<a id="schema-node-lightningstroke"></a>

One located lightning stroke from the public LightningMaps / Blitzortung live websocket feed. The stroke identity is the tuple of source_id and stroke_id because the upstream browser client tracks the last seen stroke id separately for each source stream.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/Blitzortung/Lightning/LightningStroke` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `source_id` | `int32` | `True` | Upstream live-source identifier from the src field. The public LightningMaps websocket treats stroke ids as source-scoped, so this field is part of the stable event identity. | altnames=`{"lightningmaps-live": "src"}` | minimum=`0` | - |
| `stroke_id` | `string` | `True` | Source-scoped stroke identifier from the upstream id field, stringified so the Kafka key and CloudEvents subject can be resolved directly from the payload. | altnames=`{"lightningmaps-live": "id"}` | - | - |
| `event_time` | `string` | `True` | ISO-8601 UTC timestamp derived from the upstream time field, which the public live websocket emits in Unix epoch milliseconds. | - | - | - |
| `event_timestamp_ms` | `int64` | `True` | Original upstream time value in Unix epoch milliseconds from the public live websocket. | altnames=`{"lightningmaps-live": "time"}` | minimum=`0` | - |
| `latitude` | `double` | `True` | Latitude of the located lightning stroke in decimal degrees from the upstream lat field. | altnames=`{"lightningmaps-live": "lat"}` | maximum=`90.0`<br>minimum=`-90.0` | - |
| `longitude` | `double` | `True` | Longitude of the located lightning stroke in decimal degrees from the upstream lon field. | altnames=`{"lightningmaps-live": "lon"}` | maximum=`180.0`<br>minimum=`-180.0` | - |
| `server_id` | `union` | `False` | Upstream server identifier from the srv field that produced the current live batch. The public documentation reviewed during implementation does not publish a stable human-readable enumeration for these ids. | altnames=`{"lightningmaps-live": "srv"}` | minimum=`0` | - |
| `server_delay_ms` | `union` | `False` | Delay between the upstream server receiving or computing the stroke and sending it to the live client, in milliseconds, from the public del field. | unit=`millisecond` symbol=`ms`<br>altnames=`{"lightningmaps-live": "del"}` | minimum=`0` | - |
| `accuracy_diameter_m` | `union` | `False` | Estimated accuracy diameter in meters from the upstream dev field. The public LightningMaps client renders an accuracy circle with radius dev/2, which indicates the value is expressed as a diameter rather than a raw algorithm score. | unit=`meter` symbol=`m`<br>altnames=`{"lightningmaps-live": "dev"}` | minimum=`0.0` | - |
| `detector_participations` | array of `schema` | `True` | Detector participation entries expanded from the upstream sta object when the client asks the public live feed to include station details. An empty array means the upstream batch did not include detector participation details for this stroke. | altnames=`{"lightningmaps-live": "sta"}` | - | - |
| `geohash5` | `string` | `True` | 5-character geohash of the located stroke (~40 km cell at the equator), derived in the bridge from latitude and longitude. Used as the {geohash5} MQTT topic segment for geographic wildcards. | - | pattern=`^[0-9b-hjkmnp-z]{5}$` | - |
| `geohash7` | `string` | `True` | 7-character geohash of the located stroke (~153 m cell), derived from latitude and longitude. Used as the {geohash7} MQTT topic segment for fine-grained geographic wildcards. | - | pattern=`^[0-9b-hjkmnp-z]{7}$` | - |

### Schemagroup `Blitzortung.Lightning.avro`
<a id="schemagroup-blitzortunglightningavro"></a>

#### Schema `Blitzortung.Lightning.LightningStroke`
<a id="schema-blitzortunglightninglightningstroke"></a>

| Field | Value |
| --- | --- |
| Name | LightningStroke |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | LightningStroke |
| Namespace | Blitzortung.Lightning |
| Type | `record` |
| Doc | Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `source_id` | `int` | Upstream live-source identifier from the src field. | `-` |
| `stroke_id` | `string` | Source-scoped stroke identifier from the upstream id field, stringified for key and subject resolution. | `-` |
| `event_time` | `string` | ISO-8601 UTC timestamp derived from the upstream time field. | `-` |
| `event_timestamp_ms` | `long` | Original upstream time value in Unix epoch milliseconds. | `-` |
| `latitude` | `double` | Latitude of the located lightning stroke in decimal degrees. | `-` |
| `longitude` | `double` | Longitude of the located lightning stroke in decimal degrees. | `-` |
| `geohash5` | `string` | 5-char geohash of the located stroke, derived by the bridge from lat/lon. | `-` |
| `geohash7` | `string` | 7-char geohash of the located stroke, derived by the bridge from lat/lon. | `-` |
| `server_id` | `null` \| `int` | Upstream server identifier from the srv field. | `-` |
| `server_delay_ms` | `null` \| `int` | Delay between the upstream server computing the stroke and sending it to the live client, in milliseconds. | `-` |
| `accuracy_diameter_m` | `null` \| `double` | Estimated accuracy diameter in meters from the upstream dev field. | `-` |
| `detector_participations` | array of record `DetectorParticipation` | Detector participation entries expanded from the upstream sta object. | `[]` |
