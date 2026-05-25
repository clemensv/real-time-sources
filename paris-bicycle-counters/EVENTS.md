# Paris Bicycle Counters Poller Events

Paris Bicycle Counters publishes bicycle count observations from Paris open-data bicycle counter feeds for Paris bicycle-counting stations. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{counter_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `paris-bicycle-counters`. The record key is `{counter_id}`. In plain language, `{counter_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['paris-bicycle-counters'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/fr/paris/paris-bicycle-counters/+/info`, `traffic/fr/paris/paris-bicycle-counters/+/count`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/fr/paris/paris-bicycle-counters/+/info', 1))
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

### Counter

CloudEvents type: `FR.Paris.OpenData.Velo.Counter`

#### What it tells you

A current transport measurement or status update from Paris open-data bicycle counter feeds. It carries bicycle count observations when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{counter_id}`. `{counter_id}` is unique identifier for the counting channel, combining the site ID and channel ID (mapped from 'id_compteur'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `paris-bicycle-counters`, key `{counter_id}` |
| `MQTT/5.0` | topic `traffic/fr/paris/paris-bicycle-counters/{counter_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{counter_id}` |

#### Payload

`Counter` payloads are JSON object. Required fields: `counter_id`, `counter_name`, `ce_id`.

- **`counter_id`** (string, required): Unique identifier for the counting channel, combining the site ID and channel ID (mapped from 'id_compteur').
- **`counter_name`** (string, required): Human-readable name of the counter including street name and direction (mapped from 'nom_compteur').
- **`channel_name`** (string or null, optional): Directional channel label for the counter, e.g. 'SE-NO' or 'E-O' (mapped from 'channel_name').
- **`installation_date`** (string or null, optional): Date when the counter was installed, in ISO 8601 date format (YYYY-MM-DD).
- **`longitude`** (double or null, optional): Longitude of the counter location in decimal degrees (WGS 84).
- **`latitude`** (double or null, optional): Latitude of the counter location in decimal degrees (WGS 84).
- **`ce_id`** (string, required): Deterministic CloudEvents id for the retained counter reference record.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "counter_id": "string",
  "counter_name": "string",
  "channel_name": "string",
  "installation_date": "string",
  "longitude": 0,
  "latitude": 0,
  "ce_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Bicycle Count

CloudEvents type: `FR.Paris.OpenData.Velo.BicycleCount`

#### What it tells you

A current transport measurement or status update from Paris open-data bicycle counter feeds. It carries bicycle count observations when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{counter_id}`. `{counter_id}` is unique identifier for the counting channel (mapped from 'id_compteur'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `paris-bicycle-counters`, key `{counter_id}` |
| `MQTT/5.0` | topic `traffic/fr/paris/paris-bicycle-counters/{counter_id}/count`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{counter_id}` |

#### Payload

`Bicycle Count` payloads are JSON object. Required fields: `counter_id`, `counter_name`, `date`, `ce_id`.

- **`counter_id`** (string, required): Unique identifier for the counting channel (mapped from 'id_compteur').
- **`counter_name`** (string, required): Human-readable name of the counter including street name and direction (mapped from 'nom_compteur').
- **`count`** (integer or null, optional): Number of bicycles counted during the one-hour window (mapped from 'sum_counts').
- **`date`** (datetime, required): Start of the one-hour counting window in ISO 8601 format with timezone offset.
- **`longitude`** (double or null, optional): Longitude of the counter location in decimal degrees (WGS 84).
- **`latitude`** (double or null, optional): Latitude of the counter location in decimal degrees (WGS 84).
- **`ce_id`** (string, required): Deterministic CloudEvents id composed from counter_id and hourly count date for subscriber deduplication.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "counter_id": "string",
  "counter_name": "string",
  "count": 0,
  "date": "2024-01-01T00:00:00Z",
  "longitude": 0,
  "latitude": 0,
  "ce_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

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

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/paris_bicycle_counters.xreg.json`](xreg/paris_bicycle_counters.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
