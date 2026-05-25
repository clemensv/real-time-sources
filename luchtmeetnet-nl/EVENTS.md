# Luchtmeetnet Netherlands Air Quality Bridge Events

Luchtmeetnet NL publishes pollutant concentration measurements from the Dutch national air-quality monitoring network for Dutch air-quality monitoring stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 4 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 3 telemetry event types.
- **Identity:** `{station_number}`, `{formula}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `luchtmeetnet-nl`. The record key is `{station_number}`, `{formula}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['luchtmeetnet-nl'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `nl.rivm.luchtmeetnet.Station`

#### What it tells you

Luchtmeetnet station metadata with location, operator, coordinates, and the formulas measured at the station.

#### Identity

Each event identifies the real-world resource with `{station_number}`. `{station_number}` is stable Luchtmeetnet station code, such as NL01491, used in station, measurement, and LKI requests. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `luchtmeetnet-nl`, key `{station_number}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_number`, `location`, `type`, `organisation`, `municipality`, `province`, `longitude`, `latitude`, `year_start`, `components`.

- **`station_number`** (string, required): Stable Luchtmeetnet station code, such as NL01491, used in station, measurement, and LKI requests.
- **`location`** (string, required): Human-readable station location label published by Luchtmeetnet.
- **`type`** (string, required): Station classification returned by the detail endpoint, for example Traffic, Industrial, Background, or Regional.
- **`organisation`** (string, required): Organisation operating or publishing the station in the Luchtmeetnet network, such as RIVM or a regional environmental agency.
- **`municipality`** (string or null, required): Municipality name for the station location when present in the detail response; null when the API does not provide one.
- **`province`** (string or null, required): Province name for the station location when present in the detail response; null when the API omits it.
- **`longitude`** (double, required): Longitude of the station in WGS84 decimal degrees, taken from geometry.coordinates[0].
- **`latitude`** (double, required): Latitude of the station in WGS84 decimal degrees, taken from geometry.coordinates[1].
- **`year_start`** (string, required): Year in which the station became operational according to the detail response. The upstream can return an empty string when the start year is not populated.
- **`components`** (array of string, required): Ordered list of formula codes measured at the station, as returned by the station detail endpoint.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_number": "string",
  "location": "string",
  "type": "string",
  "organisation": "string",
  "municipality": "string",
  "province": "string",
  "longitude": 0,
  "latitude": 0,
  "year_start": "string",
  "components": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Measurement

CloudEvents type: `nl.rivm.luchtmeetnet.Measurement`

#### What it tells you

Hourly Luchtmeetnet measurement for a station and component formula.

#### Identity

Each event identifies the real-world resource with `{station_number}`. `{station_number}` is stable Luchtmeetnet station code identifying where the measurement was taken. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `luchtmeetnet-nl`, key `{station_number}` |

#### Payload

`Measurement` payloads are JSON object. Required fields: `station_number`, `formula`, `value`, `timestamp_measured`.

- **`station_number`** (string, required): Stable Luchtmeetnet station code identifying where the measurement was taken.
- **`formula`** (string, required): Component formula code identifying what was measured, for example NO2, O3, PM10, or FN.
- **`value`** (double, required, ugm-3): Numeric measurement value published by the API for the station and formula at the given timestamp. Standard gaseous and particulate concentration formulas are expressed in micrograms per cubic meter; some specialised formulas such as particle counts or black-carbon indicators may use different domain-specific units, so consumers should interpret the formula-specific semantics together with the component catalog.
- **`timestamp_measured`** (string, required): Timestamp at which the value was measured, encoded as an ISO 8601 date-time string with timezone offset.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_number": "string",
  "formula": "string",
  "value": 0,
  "timestamp_measured": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### LKI

CloudEvents type: `nl.rivm.luchtmeetnet.LKI`

#### What it tells you

Hourly Dutch Luchtkwaliteitsindex value for a station.

#### Identity

Each event identifies the real-world resource with `{station_number}`. `{station_number}` is stable Luchtmeetnet station code identifying the station for which the LKI value was calculated. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `luchtmeetnet-nl`, key `{station_number}` |

#### Payload

`LKI` payloads are JSON object. Required fields: `station_number`, `value`, `timestamp_measured`.

- **`station_number`** (string, required): Stable Luchtmeetnet station code identifying the station for which the LKI value was calculated.
- **`value`** (integer, required, 1): Luchtkwaliteitsindex value on the Dutch 1 to 11 scale, where 1 to 3 is good, 4 to 6 is moderate, 7 to 9 is bad, and 10 to 11 is very bad.
- **`timestamp_measured`** (string, required): Timestamp for the hourly LKI value, encoded as an ISO 8601 date-time string with timezone offset.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_number": "string",
  "value": 0,
  "timestamp_measured": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Component

CloudEvents type: `nl.rivm.luchtmeetnet.components.Component`

#### What it tells you

Reference definition for a monitored component formula in the Luchtmeetnet network.

#### Identity

Each event identifies the real-world resource with `{formula}`. `{formula}` is stable component formula code used in measurement queries and in station component lists, such as NO2, PM25, O3, or BCWB. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `luchtmeetnet-nl`, key `{formula}` |

#### Payload

`Component` payloads are JSON object. Required fields: `formula`, `name_nl`, `name_en`.

- **`formula`** (string, required): Stable component formula code used in measurement queries and in station component lists, such as NO2, PM25, O3, or BCWB.
- **`name_nl`** (string, required): Dutch display name for the component from the component catalog.
- **`name_en`** (string, required): English display name for the component from the component catalog.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "formula": "string",
  "name_nl": "string",
  "name_en": "string"
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
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/luchtmeetnet_nl.xreg.json`](xreg/luchtmeetnet_nl.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
