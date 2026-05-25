# Seattle Fire 911 Bridge Events

MQTT/5.0 transport variant for Seattle Fire 911 dispatch incidents. Topics are non-retained QoS-1 event messages under civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}. The incident_type_slug field is the deterministic lowercase kebab-case routing key derived from the display incident_type; incident_number preserves the CloudEvents subject/Kafka key for per-incident subscriptions. Message expiry is 86400 seconds for queued/offline delivery only; this event stream does not use retained MQTT state.

## At a glance

- **Event types:** 1 documented event type (2 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{incident_number}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `seattle-911`. The record key is `{incident_number}`. In plain language, `{incident_number}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['seattle-911'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `civic-events/us/wa/seattle/public-safety/fire-dispatch/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('civic-events/us/wa/seattle/public-safety/fire-dispatch/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Incident

CloudEvents type: `US.WA.Seattle.Fire911.Incident`

#### What it tells you

Seattle Fire Department 911 dispatch record from the City of Seattle real-time fire calls dataset.

#### Identity

Each event identifies the real-world resource with `{incident_number}`. `{incident_number}` is stable Seattle Fire Department incident identifier for the dispatch record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `seattle-911`, key `{incident_number}` |
| `MQTT/5.0` | topic `civic-events/us/wa/seattle/public-safety/fire-dispatch/{incident_type_slug}/{incident_number}`, retain `false`, QoS `1` |

#### Payload

`Incident` payloads are JSON object. Required fields: `incident_number`, `incident_type`, `incident_datetime`, `incident_type_slug`, `incident_datetime_utc`.

- **`incident_number`** (string, required): Stable Seattle Fire Department incident identifier for the dispatch record.
- **`incident_type`** (string, required): Seattle Fire Department response type display string for the incident, such as Aid Response or Medic Response.
- **`incident_datetime`** (string, required): Date and time of the call as published by the Seattle Open Data dataset, in local dataset timestamp form without an explicit UTC offset.
- **`address`** (string or null, optional): Incident location text as published by the dataset.
- **`latitude`** (double or null, optional): Latitude of the incident location in decimal degrees north.
- **`longitude`** (double or null, optional): Longitude of the incident location in decimal degrees east of Greenwich; Seattle values are negative because they lie west of Greenwich.
- **`incident_type_slug`** (string, required): Deterministic lowercase kebab-case routing slug derived from incident_type by lowercasing ASCII alphanumerics, replacing every run of non-alphanumeric characters with a single hyphen, and trimming leading/trailing hyphens (example: Aid Response - 7 per Unit -> aid-response-7-per-unit). Constraints: pattern `^[a-z0-9]+(-[a-z0-9]+)*$`.
- **`incident_datetime_utc`** (datetime, required): Incident timestamp normalized to RFC 3339 UTC using America/Los_Angeles for the upstream local dataset timestamp.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "incident_number": "string",
  "incident_type": "string",
  "incident_datetime": "string",
  "address": "string",
  "latitude": 0,
  "longitude": 0,
  "incident_type_slug": "string",
  "incident_datetime_utc": "2024-01-01T00:00:00Z"
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/seattle_911.xreg.json`](xreg/seattle_911.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
