# Mode-S Events

<sub>ADS-B via dump1090 receivers · Kafka · MQTT · AMQP · <a href="https://opensky-network.org/">upstream</a> · <a href="https://opensky-network.org/apidoc/">API docs</a></sub>

## At a glance

- **Event types:** 18 documented event types (72 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 18 telemetry event types.
- **Identity:** `{icao24}/{receiver_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `mode-s`. The record key is `{icao24}/{receiver_id}`. In plain language, `{icao24}/{receiver_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

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

Connect to `mqtt://localhost:1883` and subscribe to `aviation/intl/mode-s/mode-s/+/+/df17-adsb`, `aviation/intl/mode-s/mode-s/+/+/df4-altitude`, `aviation/intl/mode-s/mode-s/+/+/df5-identity`, `aviation/intl/mode-s/mode-s/+/+/df11-acquisition`, `aviation/intl/mode-s/mode-s/+/+/df20-comm-b`, `aviation/intl/mode-s/mode-s/+/+/df21-comm-b`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('aviation/intl/mode-s/mode-s/+/+/df17-adsb', 1))
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
| `KAFKA` | topic `mode-s`, key `{icao24}/{receiver_id}` |

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
| `KAFKA` | topic `mode-s`, key `{icao24}/{receiver_id}` |

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
| `KAFKA` | topic `mode-s`, key `{icao24}/{receiver_id}` |

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
| `KAFKA` | topic `mode-s`, key `{icao24}/{receiver_id}` |

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
| `KAFKA` | topic `mode-s`, key `{icao24}/{receiver_id}` |

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
| `KAFKA` | topic `mode-s`, key `{icao24}/{receiver_id}` |

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
| `MQTT/5.0` | topic `aviation/intl/mode-s/mode-s/{icao24}/{receiver_id}/df17-adsb`, retain `false`, QoS `0` |

#### Payload

`Mqtt` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
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
| `MQTT/5.0` | topic `aviation/intl/mode-s/mode-s/{icao24}/{receiver_id}/df4-altitude`, retain `false`, QoS `0` |

#### Payload

`Mqtt` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
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
| `MQTT/5.0` | topic `aviation/intl/mode-s/mode-s/{icao24}/{receiver_id}/df5-identity`, retain `false`, QoS `0` |

#### Payload

`Mqtt` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
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
| `MQTT/5.0` | topic `aviation/intl/mode-s/mode-s/{icao24}/{receiver_id}/df11-acquisition`, retain `false`, QoS `0` |

#### Payload

`Mqtt` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
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
| `MQTT/5.0` | topic `aviation/intl/mode-s/mode-s/{icao24}/{receiver_id}/df20-comm-b`, retain `false`, QoS `0` |

#### Payload

`Mqtt` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
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
| `MQTT/5.0` | topic `aviation/intl/mode-s/mode-s/{icao24}/{receiver_id}/df21-comm-b`, retain `false`, QoS `0` |

#### Payload

`Mqtt` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### ADSB

CloudEvents type: `Mode_S.amqp.ADSB`

#### What it tells you

This event carries adsb data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}` |

#### Payload

`ADSB` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Altitude Reply

CloudEvents type: `Mode_S.amqp.AltitudeReply`

#### What it tells you

This event carries altitude reply data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}` |

#### Payload

`Altitude Reply` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Identity Reply

CloudEvents type: `Mode_S.amqp.IdentityReply`

#### What it tells you

This event carries identity reply data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}` |

#### Payload

`Identity Reply` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Acquisition Reply

CloudEvents type: `Mode_S.amqp.AcquisitionReply`

#### What it tells you

This event carries acquisition reply data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}` |

#### Payload

`Acquisition Reply` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Comm Baltitude

CloudEvents type: `Mode_S.amqp.CommBAltitude`

#### What it tells you

This event carries comm baltitude data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}` |

#### Payload

`Comm Baltitude` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Comm Bidentity

CloudEvents type: `Mode_S.amqp.CommBIdentity`

#### What it tells you

This event carries comm bidentity data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `AMQP/1.0` | source address `amqps://localhost:5671/mode-s`, message subject `{icao24}/{receiver_id}` |

#### Payload

`Comm Bidentity` payloads are JSON record. No required field list is declared.


#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
null
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

The default payload remains JSON with a JSON Structure schema. The manifest also declares inherited `.avro` groups with Avro schemas and unchanged `application/json` payloads, and `.avro.binary` groups with `application/vnd.apache.org.avro+avro` payloads. These encoding variants retain the same event identities and transport routing. Binary Avro bytes inside structured JSON CloudEvents belong in `data_base64`; payload encoding is independent of the CloudEvents envelope mode.

Binary Avro is declared by the contract but is not yet a supported feeder output. [xregistry/codegen#670](https://github.com/xregistry/codegen/issues/670) tracks the producer-generation defect. The checked-in feeders continue to use their existing JSON producers. Avro schemas preserve RFC3339 strings as strings where no native timestamp mapping was already declared; optional JSON properties without a declared default use null defaults in Avro records.

MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.

## References

- xRegistry manifest: [`xreg/mode-s.xreg.json`](xreg/mode-s.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
