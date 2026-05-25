# CDEC California Reservoirs Bridge Events

CDEC California Reservoirs publishes reservoir storage and elevation observations from the California Data Exchange Center (CDEC) for California reservoirs. These events let consumers build real-time monitoring, alerting, and operational dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 1 documented event type.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{station_id}/{sensor_num}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `cdec-reservoirs`. The record key is `{station_id}/{sensor_num}`. In plain language, `{station_id}/{sensor_num}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['cdec-reservoirs'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Reservoir Reading

CloudEvents type: `gov.ca.water.cdec.ReservoirReading`

#### What it tells you

A current reservoir record from the California Data Exchange Center (CDEC). It reports the latest storage, elevation, capacity, or related reservoir status available for one reservoir. A single sensor reading from a CDEC reservoir station.

#### Identity

Each event identifies the real-world resource with `{station_id}/{sensor_num}`. `{station_id}` is three-letter CDEC station identifier (e.g. SHA for Shasta Dam, ORO for Oroville Dam, FOL for Folsom Dam); `{sensor_num}` is CDEC numeric sensor identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `cdec-reservoirs`, key `{station_id}/{sensor_num}` |

#### Payload

`Reservoir Reading` payloads are JSON object. Required fields: `station_id`, `sensor_num`, `sensor_type`, `value`, `units`, `date`, `dur_code`, `data_flag`.

- **`station_id`** (string, required): Three-letter CDEC station identifier (e.g. SHA for Shasta Dam, ORO for Oroville Dam, FOL for Folsom Dam). This is the primary key for the monitoring station and is immutable.
- **`sensor_num`** (int32, required): CDEC numeric sensor identifier. Standard sensor numbers: 15=STORAGE (acre-feet), 6=RESERVOIR ELEVATION (feet), 76=INFLOW (cubic feet per second), 23=OUTFLOW (cubic feet per second), 1=RIVER STAGE (feet).
- **`sensor_type`** (string, required): Human-readable sensor type label as returned by the CDEC API (e.g. 'STORAGE', 'RES ELE', 'INFLOW', 'OUTFLOW', 'STAGE').
- **`value`** (double or null, required): Observed measurement value in the units specified by the 'units' field. Null when no observation is available or when the upstream reports the sentinel value -9999.
- **`units`** (string, required): Engineering units of the measurement as reported by CDEC (e.g. 'AF' for acre-feet, 'FEET' for feet, 'CFS' for cubic feet per second).
- **`date`** (string, required): Observation timestamp as reported by CDEC in PST (Pacific Standard Time, UTC-8). Format from the API is 'YYYY-M-D H:MM' and is normalized to ISO 8601 format 'YYYY-MM-DDTHH:MM:SS-08:00'. CDEC always reports in PST regardless of daylight saving time.
- **`dur_code`** (string, required): Duration code indicating the measurement interval. 'H' for hourly observations, 'D' for daily observations, 'E' for event-based (15-minute or irregular).
- **`data_flag`** (string, required): Quality flag character applied to the observation by CDEC. A single space ' ' means no flag (normal data). Other values indicate provisional, edited, or suspect data.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "sensor_num": 0,
  "sensor_type": "string",
  "value": 0,
  "units": "string",
  "date": "string",
  "dur_code": "string",
  "data_flag": "string"
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

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/cdec_reservoirs.xreg.json`](xreg/cdec_reservoirs.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
