# Mode-S Data Poller Usage Guide Events

MQTT/5.0 non-retained per-record Mode-S firehose. Each Downlink Format family (DF17/18 ADS-B, DF4 altitude reply, DF5 identity reply, DF11 all-call/acquisition reply, DF20/21 Comm-B) gets a dedicated topic so subscribers can wildcard per family. QoS 0, retain=false.

## At a glance

- **Event types:** 12 documented event types (18 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 12 telemetry event types.
- **Identity:** `{icao24}/{receiver_id}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `mode-s`. The record key is `{stationid}`. In plain language, `{stationid}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['mode-s'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to the topic filters documented per event below. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('#', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `mode-s`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/mode-s')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### ADSB

CloudEvents type: `Mode_S.ADSB`

#### What it tells you

Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.

#### Identity

Each event identifies the real-world resource with `{icao24}/{receiver_id}`. `{icao24}` is ICAO 24-bit address (lowercase hex); `{receiver_id}` is stable identifier of the receiver/station that decoded this message. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `mode-s`, key `{stationid}` |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}`; application properties msg_type `{msg_type}` |

#### Payload

`ADSB` payloads are JSON object. Required fields: `icao24`, `receiver_id`, `msg_type`, `ts`, `df`.

- **`icao24`** (string, required): ICAO 24-bit address (lowercase hex).
- **`receiver_id`** (string, required): Stable identifier of the receiver/station that decoded this message.
- **`msg_type`** (string, required): Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b).
- **`ts`** (int64, required): Reception timestamp (epoch millis).
- **`df`** (int32, required): Downlink Format value.
- **`tc`** (int32, optional): Type Code (ADS-B only).
- **`bcode`** (string, optional): BDS code (Comm-B only).
- **`alt`** (int32, optional): Barometric altitude (ft).
- **`cs`** (string, optional): Aircraft callsign.
- **`sq`** (string, optional): Squawk code.
- **`lat`** (double, optional): Latitude (deg).
- **`lon`** (double, optional): Longitude (deg).
- **`spd`** (float, optional): Speed (kn).
- **`ang`** (float, optional): Heading angle (deg).
- **`vr`** (int32, optional): Vertical rate (ft/min).
- **`rssi`** (float, optional): RSSI (dBFS).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao24": "string",
  "receiver_id": "string",
  "msg_type": "string",
  "ts": 0,
  "df": 0,
  "tc": 0,
  "bcode": "string",
  "alt": 0,
  "cs": "string",
  "sq": "string",
  "lat": 0,
  "lon": 0,
  "spd": 0,
  "ang": 0,
  "vr": 0,
  "rssi": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Altitude Reply

CloudEvents type: `Mode_S.AltitudeReply`

#### What it tells you

Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.

#### Identity

Each event identifies the real-world resource with `{icao24}/{receiver_id}`. `{icao24}` is ICAO 24-bit address (lowercase hex); `{receiver_id}` is stable identifier of the receiver/station that decoded this message. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `mode-s`, key `{stationid}` |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}`; application properties msg_type `{msg_type}` |

#### Payload

`Altitude Reply` payloads are JSON object. Required fields: `icao24`, `receiver_id`, `msg_type`, `ts`, `df`.

- **`icao24`** (string, required): ICAO 24-bit address (lowercase hex).
- **`receiver_id`** (string, required): Stable identifier of the receiver/station that decoded this message.
- **`msg_type`** (string, required): Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b).
- **`ts`** (int64, required): Reception timestamp (epoch millis).
- **`df`** (int32, required): Downlink Format value.
- **`tc`** (int32, optional): Type Code (ADS-B only).
- **`bcode`** (string, optional): BDS code (Comm-B only).
- **`alt`** (int32, optional): Barometric altitude (ft).
- **`cs`** (string, optional): Aircraft callsign.
- **`sq`** (string, optional): Squawk code.
- **`lat`** (double, optional): Latitude (deg).
- **`lon`** (double, optional): Longitude (deg).
- **`spd`** (float, optional): Speed (kn).
- **`ang`** (float, optional): Heading angle (deg).
- **`vr`** (int32, optional): Vertical rate (ft/min).
- **`rssi`** (float, optional): RSSI (dBFS).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao24": "string",
  "receiver_id": "string",
  "msg_type": "string",
  "ts": 0,
  "df": 0,
  "tc": 0,
  "bcode": "string",
  "alt": 0,
  "cs": "string",
  "sq": "string",
  "lat": 0,
  "lon": 0,
  "spd": 0,
  "ang": 0,
  "vr": 0,
  "rssi": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Identity Reply

CloudEvents type: `Mode_S.IdentityReply`

#### What it tells you

Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.

#### Identity

Each event identifies the real-world resource with `{icao24}/{receiver_id}`. `{icao24}` is ICAO 24-bit address (lowercase hex); `{receiver_id}` is stable identifier of the receiver/station that decoded this message. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `mode-s`, key `{stationid}` |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}`; application properties msg_type `{msg_type}` |

#### Payload

`Identity Reply` payloads are JSON object. Required fields: `icao24`, `receiver_id`, `msg_type`, `ts`, `df`.

- **`icao24`** (string, required): ICAO 24-bit address (lowercase hex).
- **`receiver_id`** (string, required): Stable identifier of the receiver/station that decoded this message.
- **`msg_type`** (string, required): Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b).
- **`ts`** (int64, required): Reception timestamp (epoch millis).
- **`df`** (int32, required): Downlink Format value.
- **`tc`** (int32, optional): Type Code (ADS-B only).
- **`bcode`** (string, optional): BDS code (Comm-B only).
- **`alt`** (int32, optional): Barometric altitude (ft).
- **`cs`** (string, optional): Aircraft callsign.
- **`sq`** (string, optional): Squawk code.
- **`lat`** (double, optional): Latitude (deg).
- **`lon`** (double, optional): Longitude (deg).
- **`spd`** (float, optional): Speed (kn).
- **`ang`** (float, optional): Heading angle (deg).
- **`vr`** (int32, optional): Vertical rate (ft/min).
- **`rssi`** (float, optional): RSSI (dBFS).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao24": "string",
  "receiver_id": "string",
  "msg_type": "string",
  "ts": 0,
  "df": 0,
  "tc": 0,
  "bcode": "string",
  "alt": 0,
  "cs": "string",
  "sq": "string",
  "lat": 0,
  "lon": 0,
  "spd": 0,
  "ang": 0,
  "vr": 0,
  "rssi": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Acquisition Reply

CloudEvents type: `Mode_S.AcquisitionReply`

#### What it tells you

Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.

#### Identity

Each event identifies the real-world resource with `{icao24}/{receiver_id}`. `{icao24}` is ICAO 24-bit address (lowercase hex); `{receiver_id}` is stable identifier of the receiver/station that decoded this message. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `mode-s`, key `{stationid}` |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}`; application properties msg_type `{msg_type}` |

#### Payload

`Acquisition Reply` payloads are JSON object. Required fields: `icao24`, `receiver_id`, `msg_type`, `ts`, `df`.

- **`icao24`** (string, required): ICAO 24-bit address (lowercase hex).
- **`receiver_id`** (string, required): Stable identifier of the receiver/station that decoded this message.
- **`msg_type`** (string, required): Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b).
- **`ts`** (int64, required): Reception timestamp (epoch millis).
- **`df`** (int32, required): Downlink Format value.
- **`tc`** (int32, optional): Type Code (ADS-B only).
- **`bcode`** (string, optional): BDS code (Comm-B only).
- **`alt`** (int32, optional): Barometric altitude (ft).
- **`cs`** (string, optional): Aircraft callsign.
- **`sq`** (string, optional): Squawk code.
- **`lat`** (double, optional): Latitude (deg).
- **`lon`** (double, optional): Longitude (deg).
- **`spd`** (float, optional): Speed (kn).
- **`ang`** (float, optional): Heading angle (deg).
- **`vr`** (int32, optional): Vertical rate (ft/min).
- **`rssi`** (float, optional): RSSI (dBFS).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao24": "string",
  "receiver_id": "string",
  "msg_type": "string",
  "ts": 0,
  "df": 0,
  "tc": 0,
  "bcode": "string",
  "alt": 0,
  "cs": "string",
  "sq": "string",
  "lat": 0,
  "lon": 0,
  "spd": 0,
  "ang": 0,
  "vr": 0,
  "rssi": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Comm Baltitude

CloudEvents type: `Mode_S.CommBAltitude`

#### What it tells you

Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.

#### Identity

Each event identifies the real-world resource with `{icao24}/{receiver_id}`. `{icao24}` is ICAO 24-bit address (lowercase hex); `{receiver_id}` is stable identifier of the receiver/station that decoded this message. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `mode-s`, key `{stationid}` |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}`; application properties msg_type `{msg_type}` |

#### Payload

`Comm Baltitude` payloads are JSON object. Required fields: `icao24`, `receiver_id`, `msg_type`, `ts`, `df`.

- **`icao24`** (string, required): ICAO 24-bit address (lowercase hex).
- **`receiver_id`** (string, required): Stable identifier of the receiver/station that decoded this message.
- **`msg_type`** (string, required): Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b).
- **`ts`** (int64, required): Reception timestamp (epoch millis).
- **`df`** (int32, required): Downlink Format value.
- **`tc`** (int32, optional): Type Code (ADS-B only).
- **`bcode`** (string, optional): BDS code (Comm-B only).
- **`alt`** (int32, optional): Barometric altitude (ft).
- **`cs`** (string, optional): Aircraft callsign.
- **`sq`** (string, optional): Squawk code.
- **`lat`** (double, optional): Latitude (deg).
- **`lon`** (double, optional): Longitude (deg).
- **`spd`** (float, optional): Speed (kn).
- **`ang`** (float, optional): Heading angle (deg).
- **`vr`** (int32, optional): Vertical rate (ft/min).
- **`rssi`** (float, optional): RSSI (dBFS).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao24": "string",
  "receiver_id": "string",
  "msg_type": "string",
  "ts": 0,
  "df": 0,
  "tc": 0,
  "bcode": "string",
  "alt": 0,
  "cs": "string",
  "sq": "string",
  "lat": 0,
  "lon": 0,
  "spd": 0,
  "ang": 0,
  "vr": 0,
  "rssi": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Comm Bidentity

CloudEvents type: `Mode_S.CommBIdentity`

#### What it tells you

Single Mode-S record published on the MQTT firehose. Carries the topic axes (icao24, receiver_id, msg_type) and the decoded record fields.

#### Identity

Each event identifies the real-world resource with `{icao24}/{receiver_id}`. `{icao24}` is ICAO 24-bit address (lowercase hex); `{receiver_id}` is stable identifier of the receiver/station that decoded this message. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `mode-s`, key `{stationid}` |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}`; application properties msg_type `{msg_type}` |

#### Payload

`Comm Bidentity` payloads are JSON object. Required fields: `icao24`, `receiver_id`, `msg_type`, `ts`, `df`.

- **`icao24`** (string, required): ICAO 24-bit address (lowercase hex).
- **`receiver_id`** (string, required): Stable identifier of the receiver/station that decoded this message.
- **`msg_type`** (string, required): Kebab-case Mode-S downlink-format family literal (df17-adsb, df4-altitude, df5-identity, df11-acquisition, df20-comm-b, df21-comm-b).
- **`ts`** (int64, required): Reception timestamp (epoch millis).
- **`df`** (int32, required): Downlink Format value.
- **`tc`** (int32, optional): Type Code (ADS-B only).
- **`bcode`** (string, optional): BDS code (Comm-B only).
- **`alt`** (int32, optional): Barometric altitude (ft).
- **`cs`** (string, optional): Aircraft callsign.
- **`sq`** (string, optional): Squawk code.
- **`lat`** (double, optional): Latitude (deg).
- **`lon`** (double, optional): Longitude (deg).
- **`spd`** (float, optional): Speed (kn).
- **`ang`** (float, optional): Heading angle (deg).
- **`vr`** (int32, optional): Vertical rate (ft/min).
- **`rssi`** (float, optional): RSSI (dBFS).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "icao24": "string",
  "receiver_id": "string",
  "msg_type": "string",
  "ts": 0,
  "df": 0,
  "tc": 0,
  "bcode": "string",
  "alt": 0,
  "cs": "string",
  "sq": "string",
  "lat": 0,
  "lon": 0,
  "spd": 0,
  "ang": 0,
  "vr": 0,
  "rssi": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Mqtt

CloudEvents type: `Mode_S.ADSB.mqtt`

#### What it tells you

This event carries mqtt data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `not declared`, retain `not declared`, QoS `not declared` |

#### Payload

`Mqtt` payloads are JSON schema. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
"string"
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Mqtt

CloudEvents type: `Mode_S.AltitudeReply.mqtt`

#### What it tells you

This event carries mqtt data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `not declared`, retain `not declared`, QoS `not declared` |

#### Payload

`Mqtt` payloads are JSON schema. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
"string"
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Mqtt

CloudEvents type: `Mode_S.IdentityReply.mqtt`

#### What it tells you

This event carries mqtt data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `not declared`, retain `not declared`, QoS `not declared` |

#### Payload

`Mqtt` payloads are JSON schema. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
"string"
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Mqtt

CloudEvents type: `Mode_S.AcquisitionReply.mqtt`

#### What it tells you

This event carries mqtt data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `not declared`, retain `not declared`, QoS `not declared` |

#### Payload

`Mqtt` payloads are JSON schema. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
"string"
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Mqtt

CloudEvents type: `Mode_S.CommBAltitude.mqtt`

#### What it tells you

This event carries mqtt data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `not declared`, retain `not declared`, QoS `not declared` |

#### Payload

`Mqtt` payloads are JSON schema. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
"string"
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Mqtt

CloudEvents type: `Mode_S.CommBIdentity.mqtt`

#### What it tells you

This event carries mqtt data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `not declared`, retain `not declared`, QoS `not declared` |

#### Payload

`Mqtt` payloads are JSON schema. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
"string"
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

## Conventions

CloudEvents is the envelope around each JSON payload. It supplies metadata such as `specversion` (`1.0`), `type` (what kind of event this is), `source` (who produced it), `id` (the event occurrence identifier), `time`, and `subject` (the resource the event is about). For this source, `subject` is the stable routing identity described in each event above; the unique event occurrence is identified by CloudEvents `id` together with `source`. This repository convention mirrors the same identity to transport-native routing fields where available: Kafka message key (or the `partitionkey` extension when present), MQTT topic identity segments, and AMQP message `subject` or application properties. Those mirrors are application conventions, not generic CloudEvents binding rules. The AMQP link address identifies the stream as a whole, not an individual station or entity.

Transport bindings carry CloudEvents metadata differently:

| Transport | CloudEvents metadata location | Payload location |
| --- | --- | --- |
| Kafka binary mode | Kafka headers named `ce_<attribute>` for CloudEvents attributes except `datacontenttype`; `datacontenttype` maps to Kafka `content-type` | Kafka record value |
| Kafka structured mode | Inside the JSON CloudEvent envelope, with content type `application/cloudevents+json`; batched mode is not used by this generator | Kafka record value |
| MQTT 5 binary mode | MQTT 5 user properties named by the CloudEvents attribute (`id`, `source`, `type`, `subject`, ...), as defined by the CloudEvents MQTT binding; no `ce_` prefix | PUBLISH payload |
| AMQP 1.0 binary mode | Application properties named `cloudEvents:<attribute>` except `datacontenttype`; `datacontenttype` maps to AMQP `content-type` and must not be duplicated as an application property | AMQP message body |

All payloads documented here are JSON. MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/mode_s.xreg.json`](xreg/mode_s.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
