# Nextbus Events

Nextbus / UMOIQ public XML feed CloudEvents.

## At a glance

- **Event types:** 4 documented event types (12 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 4 telemetry event types.
- **Identity:** `{agency_id}/{route_tag}/vehicle/{vehicle_id}`, `{agency_id}/{route_tag}/route-config/{stop_or_vehicle_id}`, `{agency_id}/{route_tag}/schedule/{stop_or_vehicle_id}`, `{agency_id}/{route_tag}/message/{stop_or_vehicle_id}` identifies the resource each event is about.
- **Operations:** The bridge documentation mentions ETag-aware polling, so consumers should expect unchanged upstream responses to be skipped.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `nextbus`. The record key is `{agency_id}/{route_tag}`. In plain language, `{agency_id}/{route_tag}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['nextbus'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `transit/intl/nextbus/nextbus/+/+/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('transit/intl/nextbus/nextbus/+/+/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `broker-configured address`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/events')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Vehicle Position

CloudEvents type: `nextbus.VehiclePosition`

#### What it tells you

Nextbus VehiclePosition event. Nextbus XML feed event payload.

#### Identity

Each event identifies the real-world resource with `{agency_id}/{route_tag}/vehicle/{vehicle_id}`. `{agency_id}` is agency_id value from the Nextbus XML feed; `{route_tag}` is route_tag value from the Nextbus XML feed; `{vehicle_id}` is vehicle_id value from the Nextbus XML feed. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nextbus`, key `{agency_id}/{route_tag}` |
| `MQTT/5.0` | topic `transit/intl/nextbus/nextbus/{agency_id}/{route_tag}/{event_type}/{stop_or_vehicle_id}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{agency_id}/{route_tag}/vehicle/{vehicle_id}` |

#### Payload

`Vehicle Position` payloads are JSON object. Required fields: `agency_id`, `route_tag`, `vehicle_id`, `stop_or_vehicle_id`, `event_type`.

- **`agency_id`** (string, required): agency_id value from the Nextbus XML feed.
- **`route_tag`** (string, required): route_tag value from the Nextbus XML feed.
- **`vehicle_id`** (string, required): vehicle_id value from the Nextbus XML feed.
- **`stop_or_vehicle_id`** (string, required): stop_or_vehicle_id value from the Nextbus XML feed.
- **`event_type`** (string, required): event_type value from the Nextbus XML feed.
- **`lat`** (string, optional): lat value from the Nextbus XML feed.
- **`lon`** (string, optional): lon value from the Nextbus XML feed.
- **`timestamp`** (double, optional): timestamp value from the Nextbus XML feed.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "agency_id": "string",
  "route_tag": "string",
  "vehicle_id": "string",
  "stop_or_vehicle_id": "string",
  "event_type": "string",
  "lat": "string",
  "lon": "string",
  "timestamp": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Route Config

CloudEvents type: `nextbus.RouteConfig`

#### What it tells you

Nextbus RouteConfig event. Nextbus XML feed event payload.

#### Identity

Each event identifies the real-world resource with `{agency_id}/{route_tag}/route-config/{stop_or_vehicle_id}`. `{agency_id}` is agency_id value from the Nextbus XML feed; `{route_tag}` is route_tag value from the Nextbus XML feed; `{stop_or_vehicle_id}` is stop_or_vehicle_id value from the Nextbus XML feed. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nextbus`, key `{agency_id}/{route_tag}` |
| `MQTT/5.0` | topic `transit/intl/nextbus/nextbus/{agency_id}/{route_tag}/{event_type}/{stop_or_vehicle_id}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{agency_id}/{route_tag}/route-config/{stop_or_vehicle_id}` |

#### Payload

`Route Config` payloads are JSON object. Required fields: `agency_id`, `route_tag`, `stop_or_vehicle_id`, `event_type`, `route_config`.

- **`agency_id`** (string, required): agency_id value from the Nextbus XML feed.
- **`route_tag`** (string, required): route_tag value from the Nextbus XML feed.
- **`stop_or_vehicle_id`** (string, required): stop_or_vehicle_id value from the Nextbus XML feed.
- **`event_type`** (string, required): event_type value from the Nextbus XML feed.
- **`route_config`** (string, required): route_config value from the Nextbus XML feed.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "agency_id": "string",
  "route_tag": "string",
  "stop_or_vehicle_id": "string",
  "event_type": "string",
  "route_config": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Schedule

CloudEvents type: `nextbus.Schedule`

#### What it tells you

Nextbus Schedule event. Nextbus XML feed event payload.

#### Identity

Each event identifies the real-world resource with `{agency_id}/{route_tag}/schedule/{stop_or_vehicle_id}`. `{agency_id}` is agency_id value from the Nextbus XML feed; `{route_tag}` is route_tag value from the Nextbus XML feed; `{stop_or_vehicle_id}` is stop_or_vehicle_id value from the Nextbus XML feed. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nextbus`, key `{agency_id}/{route_tag}` |
| `MQTT/5.0` | topic `transit/intl/nextbus/nextbus/{agency_id}/{route_tag}/{event_type}/{stop_or_vehicle_id}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{agency_id}/{route_tag}/schedule/{stop_or_vehicle_id}` |

#### Payload

`Schedule` payloads are JSON object. Required fields: `agency_id`, `route_tag`, `stop_or_vehicle_id`, `event_type`, `schedule`.

- **`agency_id`** (string, required): agency_id value from the Nextbus XML feed.
- **`route_tag`** (string, required): route_tag value from the Nextbus XML feed.
- **`stop_or_vehicle_id`** (string, required): stop_or_vehicle_id value from the Nextbus XML feed.
- **`event_type`** (string, required): event_type value from the Nextbus XML feed.
- **`schedule`** (string, required): schedule value from the Nextbus XML feed.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "agency_id": "string",
  "route_tag": "string",
  "stop_or_vehicle_id": "string",
  "event_type": "string",
  "schedule": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Message

CloudEvents type: `nextbus.Message`

#### What it tells you

Nextbus Message event. Nextbus XML feed event payload.

#### Identity

Each event identifies the real-world resource with `{agency_id}/{route_tag}/message/{stop_or_vehicle_id}`. `{agency_id}` is agency_id value from the Nextbus XML feed; `{route_tag}` is route_tag value from the Nextbus XML feed; `{stop_or_vehicle_id}` is stop_or_vehicle_id value from the Nextbus XML feed. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `nextbus`, key `{agency_id}/{route_tag}` |
| `MQTT/5.0` | topic `transit/intl/nextbus/nextbus/{agency_id}/{route_tag}/{event_type}/{stop_or_vehicle_id}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{agency_id}/{route_tag}/message/{stop_or_vehicle_id}` |

#### Payload

`Message` payloads are JSON object. Required fields: `agency_id`, `route_tag`, `stop_or_vehicle_id`, `event_type`, `message`.

- **`agency_id`** (string, required): agency_id value from the Nextbus XML feed.
- **`route_tag`** (string, required): route_tag value from the Nextbus XML feed.
- **`stop_or_vehicle_id`** (string, required): stop_or_vehicle_id value from the Nextbus XML feed.
- **`event_type`** (string, required): event_type value from the Nextbus XML feed.
- **`message`** (string, required): message value from the Nextbus XML feed.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "agency_id": "string",
  "route_tag": "string",
  "stop_or_vehicle_id": "string",
  "event_type": "string",
  "message": "string"
}
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

- The bridge documentation mentions ETag-aware polling, so consumers should expect unchanged upstream responses to be skipped.
- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.

## References

- xRegistry manifest: [`xreg/nextbus.xreg.json`](xreg/nextbus.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
