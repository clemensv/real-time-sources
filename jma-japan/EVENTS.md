# JMA Japan Weather Bulletins Poller Events

JMA Japan Bulletins publishes official bulletin messages from the Japan Meteorological Agency for Japanese bulletin feeds. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{bulletin_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `jma-japan`. The record key is `{bulletin_id}`. In plain language, `{bulletin_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['jma-japan'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Weather Bulletin

CloudEvents type: `jp.go.jma.WeatherBulletin`

#### What it tells you

An official alert or bulletin from the Japan Meteorological Agency. It carries official bulletin messages for the affected area and validity period published by the upstream source.

#### Identity

Each event identifies the real-world resource with `{bulletin_id}`. `{bulletin_id}` is unique identifier for the bulletin, derived from the Atom entry ID (typically a URL to the full XML document). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-japan`, key `{bulletin_id}` |

#### Payload

`Weather Bulletin` payloads are JSON object. Required fields: `bulletin_id`, `title`, `updated`.

- **`bulletin_id`** (string, required): Unique identifier for the bulletin, derived from the Atom entry ID (typically a URL to the full XML document).
- **`title`** (string, required): Title of the weather bulletin in Japanese, e.g. '気象特別警報・警報・注意報' (Special weather warnings/advisories).
- **`author`** (string or null, optional): Issuing authority name in Japanese, e.g. '気象庁' (JMA) or a regional observatory name like '松江地方気象台'.
- **`updated`** (datetime, required): UTC timestamp when the bulletin was last updated.
- **`link`** (string or null, optional): URL to the full XML document for this bulletin on the JMA data server.
- **`content`** (string or null, optional): Brief text summary of the bulletin content in Japanese.
- **`feed_type`** (enum, optional): Which JMA Atom feed this bulletin originated from.
##### `feed_type` values

- `regular`: Provider value `regular` for this coded alert field.
- `extra`: Provider value `extra` for this coded alert field.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "bulletin_id": "string",
  "title": "string",
  "author": "string",
  "updated": "2024-01-01T00:00:00Z",
  "link": "string",
  "content": "string",
  "feed_type": "regular"
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

- xRegistry manifest: [`xreg/jma_japan.xreg.json`](xreg/jma_japan.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
