# UK Environment Agency Flood Monitoring API Bridge Events

This project bridges the [UK Environment Agency Flood Monitoring API](https://environment.data.gov.uk/flood-monitoring/doc/reference) to Apache Kafka, Azure Event Hubs, or Microsoft Fabric Event Streams. It provides real-time water level and flow data from approximately 4,000 monitoring stations across England.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{station_reference}` identifies the resource each event is about.
- **Operations:** Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `uk-ea-flood-monitoring`. The record key is `{station_reference}`. In plain language, `{station_reference}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['uk-ea-flood-monitoring'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `UK.Gov.Environment.EA.FloodMonitoring.Station`

#### What it tells you

This event carries station data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_reference}`. `{station_reference}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `uk-ea-flood-monitoring`, key `{station_reference}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_reference`, `label`, `lat`, `long`, `notation`.

- **`station_reference`** (string, required): No description provided.
- **`label`** (string, required): No description provided.
- **`river_name`** (string or null, optional): No description provided.
- **`catchment_name`** (string or null, optional): No description provided.
- **`town`** (string or null, optional): No description provided.
- **`lat`** (double, required): No description provided.
- **`long`** (double, required): No description provided.
- **`notation`** (string, required): No description provided.
- **`status`** (string or null, optional): No description provided.
- **`date_opened`** (string or null, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_reference": "string",
  "label": "string",
  "river_name": "string",
  "catchment_name": "string",
  "town": "string",
  "lat": 0,
  "long": 0,
  "notation": "string",
  "status": "string",
  "date_opened": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Reading

CloudEvents type: `UK.Gov.Environment.EA.FloodMonitoring.Reading`

#### What it tells you

This event carries reading data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{station_reference}`. `{station_reference}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `uk-ea-flood-monitoring`, key `{station_reference}` |

#### Payload

`Reading` payloads are JSON object. Required fields: `station_reference`, `date_time`, `measure`, `value`.

- **`station_reference`** (string, required): No description provided.
- **`date_time`** (datetime, required): No description provided.
- **`measure`** (string, required): No description provided.
- **`value`** (double, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_reference": "string",
  "date_time": "2024-01-01T00:00:00Z",
  "measure": "string",
  "value": 0
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

- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/uk_ea_flood_monitoring.xreg.json`](xreg/uk_ea_flood_monitoring.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- UK Environment Agency Flood Monitoring
API: <https://environment.data.gov.uk/flood-monitoring/doc/reference>
