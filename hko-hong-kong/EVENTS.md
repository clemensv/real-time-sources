# HKO Hong Kong Weather Observation Bridge Events

Hong Kong Observatory Weather publishes weather observations from the Hong Kong Observatory for Hong Kong weather observation locations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{place_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `hko-hong-kong`. The record key is `{place_id}`. In plain language, `{place_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['hko-hong-kong'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `HK.Gov.HKO.Weather.Station`

#### What it tells you

A reference record published by the Hong Kong Observatory. It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{place_id}`. `{place_id}` is URL-safe slug identifier derived from the English place name, e.g. 'kings-park', 'central-western-district'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hko-hong-kong`, key `{place_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `place_id`, `name`, `data_types`.

- **`place_id`** (string, required): URL-safe slug identifier derived from the English place name, e.g. 'kings-park', 'central-western-district'. Used as Kafka key and CloudEvents subject.
- **`name`** (string, required): Original English place name from the HKO rhrread API, e.g. 'King's Park', 'Central & Western District'.
- **`data_types`** (string, required): Comma-separated list of data types reported by this place. Values: 'temperature', 'rainfall', 'humidity', 'uvindex'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "place_id": "string",
  "name": "string",
  "data_types": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Weather Observation

CloudEvents type: `HK.Gov.HKO.Weather.WeatherObservation`

#### What it tells you

A current environmental measurement from the Hong Kong Observatory. It carries weather observations when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{place_id}`. `{place_id}` is URL-safe slug identifier for the place, matching the Kafka key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hko-hong-kong`, key `{place_id}` |

#### Payload

`Weather Observation` payloads are JSON object. Required fields: `place_id`, `place_name`, `observation_time`.

- **`place_id`** (string, required): URL-safe slug identifier for the place, matching the Kafka key.
- **`place_name`** (string, required): Original English place name from the HKO API.
- **`observation_time`** (datetime, required): ISO 8601 timestamp of the observation including Hong Kong timezone offset (+08:00), from the updateTime field.
- **`temperature`** (double or null, optional, Cel (°C)): Air temperature from automatic weather stations.
- **`rainfall_max`** (double or null, optional, mm): Maximum rainfall in the past hour from district-level rain gauges.
- **`humidity`** (int32 or null, optional, percent (%)): Relative humidity, currently only from Hong Kong Observatory headquarters.
- **`uv_index`** (double or null, optional, 1): UV index during the past hour, currently only from King's Park.
- **`uv_description`** (string or null, optional): HKO descriptive UV level: 'low', 'moderate', 'high', 'very high', 'extreme'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "place_id": "string",
  "place_name": "string",
  "observation_time": "2024-01-01T00:00:00Z",
  "temperature": 0,
  "rainfall_max": 0,
  "humidity": 0,
  "uv_index": 0,
  "uv_description": "string"
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
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/hko_hong_kong.xreg.json`](xreg/hko_hong_kong.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- HKO Open Data API: <https://www.hko.gov.hk/en/abouthko/opendata_intro.htm>
