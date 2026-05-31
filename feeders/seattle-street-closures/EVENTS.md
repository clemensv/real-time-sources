# Seattle Street Closures feeder Events

MQTT 5 UNS topic bindings for seattle-street-closures.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{closure_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `seattle-street-closures`. The record key is `{closure_id}`. In plain language, `{closure_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['seattle-street-closures'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/us/seattle/seattle-street-closures/+/+/closure`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/us/seattle/seattle-street-closures/+/+/closure', 1))
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

### Street Closure

CloudEvents type: `US.WA.Seattle.StreetClosures.StreetClosure`

#### What it tells you

Street closure row from the Seattle Department of Transportation street closures dataset, describing one closed street segment and its active occurrence window.

#### Identity

Each event identifies the real-world resource with `{closure_id}`. `{closure_id}` is derived stable identity for the closure row, composed from permit number, street segment key, start date, and end date. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `seattle-street-closures`, key `{closure_id}` |
| `MQTT/5.0` | topic `traffic/us/seattle/seattle-street-closures/{neighborhood}/{closure_id}/closure`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{closure_id}` |

#### Payload

`Street Closure` payloads are JSON object. Required fields: `closure_id`, `permit_number`, `permit_type`, `start_date`, `end_date`.

- **`closure_id`** (string, required): Derived stable identity for the closure row, composed from permit number, street segment key, start date, and end date.
- **`permit_number`** (string, required): Identifier for the permit record granting authorization to close the street.
- **`permit_type`** (string, required): Type of permit, such as Block Party, Play Street, Farmers Market, or Temporary Activation.
- **`project_name`** (string or null, optional): Short title used by Seattle to quickly identify the closure permit.
- **`project_description`** (string or null, optional): Longer description of the permit, including issuance notes and closure details.
- **`start_date`** (string, required): Date on which the closure event begins, normalized to YYYY-MM-DD.
- **`end_date`** (string, required): Date on which the closure event ends, normalized to YYYY-MM-DD.
- **`sunday`** (string or null, optional): Time period, if any, during which the closure occurs on Sundays between the start and end dates.
- **`monday`** (string or null, optional): Time period, if any, during which the closure occurs on Mondays between the start and end dates.
- **`tuesday`** (string or null, optional): Time period, if any, during which the closure occurs on Tuesdays between the start and end dates.
- **`wednesday`** (string or null, optional): Time period, if any, during which the closure occurs on Wednesdays between the start and end dates.
- **`thursday`** (string or null, optional): Time period, if any, during which the closure occurs on Thursdays between the start and end dates.
- **`friday`** (string or null, optional): Time period, if any, during which the closure occurs on Fridays between the start and end dates.
- **`saturday`** (string or null, optional): Time period, if any, during which the closure occurs on Saturdays between the start and end dates.
- **`street_on`** (string or null, optional): Street name of the closed street segment.
- **`street_from`** (string or null, optional): Name of the intersecting street at the low end of the closed segment.
- **`street_to`** (string or null, optional): Name of the intersecting street at the high end of the closed segment.
- **`segkey`** (string or null, optional): Identifier for the street segment that is closed.
- **`geometry_json`** (string or null, optional): Serialized GeoJSON LineString geometry for the closed street block.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "closure_id": "string",
  "permit_number": "string",
  "permit_type": "string",
  "project_name": "string",
  "project_description": "string",
  "start_date": "string",
  "end_date": "string",
  "sunday": "string",
  "monday": "string",
  "tuesday": "string",
  "wednesday": "string",
  "thursday": "string",
  "friday": "string",
  "saturday": "string",
  "street_on": "string",
  "street_from": "string",
  "street_to": "string",
  "segkey": "string",
  "geometry_json": "string"
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

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.

## References

- xRegistry manifest: [`xreg/seattle-street-closures.xreg.json`](xreg/seattle-street-closures.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
