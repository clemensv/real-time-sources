# Mode-S Data Poller Usage Guide Events

MQTT/5.0 non-retained per-record Mode-S firehose. Each Downlink Format family (DF17/18 ADS-B, DF4 altitude reply, DF5 identity reply, DF11 all-call/acquisition reply, DF20/21 Comm-B) gets a dedicated topic so subscribers can wildcard per family. QoS 0, retain=false.

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

### Endpoint `Mode_S.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Mode_S`](#messagegroup-modes) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `mode-s` |
| Kafka key | `{stationid}` |
| Deployed | False |

### Endpoint `Mode_S.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`Mode_S.mqtt`](#messagegroup-modesmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |

## Messagegroups

### Messagegroup `Mode_S`
<a id="messagegroup-modes"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Mode_S.Kafka` (KAFKA) |
| Messages | 6 |

#### Message `Mode_S.ADSB`
<a id="message-modesadsb"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Mode_S.jstruct/schemas/Mode_S.Record`](#schema-modesrecord) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` |  | `string` | `False` | `1.0` |
| `type` |  | `string` | `False` | `Mode_S.ADSB` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{icao24}/{receiver_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Kafka` | `KAFKA` | topic `mode-s`; key `{stationid}` |

#### Message `Mode_S.AltitudeReply`
<a id="message-modesaltitudereply"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Mode_S.jstruct/schemas/Mode_S.Record`](#schema-modesrecord) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` |  | `string` | `False` | `1.0` |
| `type` |  | `string` | `False` | `Mode_S.AltitudeReply` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{icao24}/{receiver_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Kafka` | `KAFKA` | topic `mode-s`; key `{stationid}` |

#### Message `Mode_S.IdentityReply`
<a id="message-modesidentityreply"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Mode_S.jstruct/schemas/Mode_S.Record`](#schema-modesrecord) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` |  | `string` | `False` | `1.0` |
| `type` |  | `string` | `False` | `Mode_S.IdentityReply` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{icao24}/{receiver_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Kafka` | `KAFKA` | topic `mode-s`; key `{stationid}` |

#### Message `Mode_S.AcquisitionReply`
<a id="message-modesacquisitionreply"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Mode_S.jstruct/schemas/Mode_S.Record`](#schema-modesrecord) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` |  | `string` | `False` | `1.0` |
| `type` |  | `string` | `False` | `Mode_S.AcquisitionReply` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{icao24}/{receiver_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Kafka` | `KAFKA` | topic `mode-s`; key `{stationid}` |

#### Message `Mode_S.CommBAltitude`
<a id="message-modescommbaltitude"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Mode_S.jstruct/schemas/Mode_S.Record`](#schema-modesrecord) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` |  | `string` | `False` | `1.0` |
| `type` |  | `string` | `False` | `Mode_S.CommBAltitude` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{icao24}/{receiver_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Kafka` | `KAFKA` | topic `mode-s`; key `{stationid}` |

#### Message `Mode_S.CommBIdentity`
<a id="message-modescommbidentity"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Mode_S.jstruct/schemas/Mode_S.Record`](#schema-modesrecord) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` |  | `string` | `False` | `1.0` |
| `type` |  | `string` | `False` | `Mode_S.CommBIdentity` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{icao24}/{receiver_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Kafka` | `KAFKA` | topic `mode-s`; key `{stationid}` |

### Messagegroup `Mode_S.mqtt`
<a id="messagegroup-modesmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 non-retained per-record Mode-S firehose. Each Downlink Format family (DF17/18 ADS-B, DF4 altitude reply, DF5 identity reply, DF11 all-call/acquisition reply, DF20/21 Comm-B) gets a dedicated topic so subscribers can wildcard per family. QoS 0, retain=false. |
| Transport bindings | `Mode_S.Mqtt` (MQTT/5.0) |
| Messages | 6 |

#### Message `Mode_S.ADSB.mqtt`
<a id="message-modesadsbmqtt"></a>

| Field | Value |
| --- | --- |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Mqtt` | `MQTT/5.0` | topic `-` |

#### Message `Mode_S.AltitudeReply.mqtt`
<a id="message-modesaltitudereplymqtt"></a>

| Field | Value |
| --- | --- |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Mqtt` | `MQTT/5.0` | topic `-` |

#### Message `Mode_S.IdentityReply.mqtt`
<a id="message-modesidentityreplymqtt"></a>

| Field | Value |
| --- | --- |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Mqtt` | `MQTT/5.0` | topic `-` |

#### Message `Mode_S.AcquisitionReply.mqtt`
<a id="message-modesacquisitionreplymqtt"></a>

| Field | Value |
| --- | --- |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Mqtt` | `MQTT/5.0` | topic `-` |

#### Message `Mode_S.CommBAltitude.mqtt`
<a id="message-modescommbaltitudemqtt"></a>

| Field | Value |
| --- | --- |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Mqtt` | `MQTT/5.0` | topic `-` |

#### Message `Mode_S.CommBIdentity.mqtt`
<a id="message-modescommbidentitymqtt"></a>

| Field | Value |
| --- | --- |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Mode_S.Mqtt` | `MQTT/5.0` | topic `-` |

## Schemagroups

### Schemagroup `Mode_S.jstruct`
<a id="schemagroup-modesjstruct"></a>

#### Schema `Mode_S.Record`
<a id="schema-modesrecord"></a>

| Field | Value |
| --- | --- |
| Name | Record |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/Mode_S/Record` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| Type | `object` |

###### Object `Record`
<a id="schema-node-record"></a>

Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/Mode_S/Record` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `icao24` | `string` | `True` | ICAO 24-bit address (lowercase hex). | - | - | - |
| `receiver_id` | `string` | `True` | Stable identifier of the receiver/station that decoded this message. | - | - | - |
| `msg_type` | `string` | `True` | Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b). | - | - | - |
| `ts` | `int64` | `True` | Reception timestamp (epoch millis). | - | - | - |
| `df` | `int32` | `True` | Downlink Format value. | - | - | - |
| `tc` | `int32` | `False` | Type Code (ADS-B only). | - | - | - |
| `bcode` | `string` | `False` | BDS code (Comm-B only). | - | - | - |
| `alt` | `int32` | `False` | Barometric altitude (ft). | - | - | - |
| `cs` | `string` | `False` | Aircraft callsign. | - | - | - |
| `sq` | `string` | `False` | Squawk code. | - | - | - |
| `lat` | `double` | `False` | Latitude (deg). | - | - | - |
| `lon` | `double` | `False` | Longitude (deg). | - | - | - |
| `spd` | `float` | `False` | Speed (kn). | - | - | - |
| `ang` | `float` | `False` | Heading angle (deg). | - | - | - |
| `vr` | `int32` | `False` | Vertical rate (ft/min). | - | - | - |
| `rssi` | `float` | `False` | RSSI (dBFS). | - | - | - |

### Schemagroup `Mode_S.avro`
<a id="schemagroup-modesavro"></a>

#### Schema `Mode_S.Record`
<a id="schema-modesrecord"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.1 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Record |
| Namespace | Mode_S |
| Type | `record` |
| Doc | Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `icao24` | `string` | ICAO 24-bit address (lowercase hex). | `-` |
| `receiver_id` | `string` | Stable identifier of the receiver/station that decoded this message. | `-` |
| `msg_type` | `string` | Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b). | `-` |
| `ts` | `long` | Reception timestamp (epoch millis). | `-` |
| `df` | `int` | Downlink Format value. | `-` |
| `tc` | `null` \| `int` | Type Code (ADS-B only). | `-` |
| `bcode` | `null` \| `string` | BDS code (Comm-B only). | `-` |
| `alt` | `null` \| `int` | Barometric altitude (ft). | `-` |
| `cs` | `null` \| `string` | Aircraft callsign. | `-` |
| `sq` | `null` \| `string` | Squawk code. | `-` |
| `lat` | `null` \| `double` | Latitude (deg). | `-` |
| `lon` | `null` \| `double` | Longitude (deg). | `-` |
| `spd` | `null` \| `float` | Speed (kn). | `-` |
| `ang` | `null` \| `float` | Heading angle (deg). | `-` |
| `vr` | `null` \| `int` | Vertical rate (ft/min). | `-` |
| `rssi` | `null` \| `float` | RSSI (dBFS). | `-` |
