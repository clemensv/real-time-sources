# FMI Finland Air Quality Bridge Events

FMI Finland Weather publishes weather observations from the Finnish Meteorological Institute (FMI) for Finnish weather observation stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `{fmisid}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `fmi-finland-airquality`. The record key is `{fmisid}`. In plain language, `{fmisid}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['fmi-finland-airquality'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `fi.fmi.opendata.airquality.Station`

#### What it tells you

Reference data for a Finnish Meteorological Institute air quality monitoring station.

#### Identity

Each event identifies the real-world resource with `{fmisid}`. `{fmisid}` is stable FMI station identifier (fmisid) used as the Kafka key and CloudEvents subject. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `fmi-finland-airquality`, key `{fmisid}` |

#### Payload

`Station` payloads are JSON object. Required fields: `fmisid`, `station_name`, `latitude`, `longitude`, `municipality`.

- **`fmisid`** (string, required): Stable FMI station identifier (fmisid) used as the Kafka key and CloudEvents subject. Constraints: pattern `^[0-9]+$`.
- **`station_name`** (string, required): Air quality station name from the FMI station metadata, for example 'Helsinki Kallio 2'.
- **`latitude`** (double, required, degree (°)): WGS84 latitude of the station representative point in decimal degrees.
- **`longitude`** (double, required, degree (°)): WGS84 longitude of the station representative point in decimal degrees.
- **`municipality`** (string or null, required): Municipality or region name from the station metadata if FMI publishes it. Null when it is not available in the station record.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fmisid": "string",
  "station_name": "string",
  "latitude": 0,
  "longitude": 0,
  "municipality": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Observation

CloudEvents type: `fi.fmi.opendata.airquality.Observation`

#### What it tells you

Hourly air quality observation aggregated per station and timestamp from FMI OGC WFS simple query results.

#### Identity

Each event identifies the real-world resource with `{fmisid}`. `{fmisid}` is stable FMI station identifier (fmisid) for the observing station. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `fmi-finland-airquality`, key `{fmisid}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `fmisid`, `station_name`, `observation_time`, `aqindex`, `pm10_ug_m3`, `pm2_5_ug_m3`, `no2_ug_m3`, `o3_ug_m3`, `so2_ug_m3`, `co_mg_m3`.

- **`fmisid`** (string, required): Stable FMI station identifier (fmisid) for the observing station. Constraints: pattern `^[0-9]+$`.
- **`station_name`** (string, required): Station name resolved from station metadata or, if metadata lookup fails, the station identifier string.
- **`observation_time`** (string, required): Observation timestamp in UTC, formatted as an ISO-8601 instant such as 2024-01-15T13:00:00Z. Constraints: pattern `^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$`.
- **`aqindex`** (double or null, required): Finnish Air Quality Index 1-hour average from the AQINDEX_PT1H_avg parameter. Null when FMI reports the parameter as missing or not available.
- **`pm10_ug_m3`** (double or null, required, µg/m³): PM10 particulate matter concentration 1-hour average in micrograms per cubic meter from the PM10_PT1H_avg parameter. Null when the value is missing.
- **`pm2_5_ug_m3`** (double or null, required, µg/m³): PM2.5 particulate matter concentration 1-hour average in micrograms per cubic meter from the PM25_PT1H_avg parameter. Null when the value is missing.
- **`no2_ug_m3`** (double or null, required, µg/m³): Nitrogen dioxide concentration 1-hour average in micrograms per cubic meter from the NO2_PT1H_avg parameter. Null when the value is missing.
- **`o3_ug_m3`** (double or null, required, µg/m³): Ozone concentration 1-hour average in micrograms per cubic meter from the O3_PT1H_avg parameter. Null when the value is missing.
- **`so2_ug_m3`** (double or null, required, µg/m³): Sulfur dioxide concentration 1-hour average in micrograms per cubic meter from the SO2_PT1H_avg parameter. Null when the value is missing.
- **`co_mg_m3`** (double or null, required, mg/m³): Carbon monoxide concentration 1-hour average in milligrams per cubic meter from the CO_PT1H_avg parameter. Null when the value is missing.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "fmisid": "string",
  "station_name": "string",
  "observation_time": "string",
  "aqindex": 0,
  "pm10_ug_m3": 0,
  "pm2_5_ug_m3": 0,
  "no2_ug_m3": 0,
  "o3_ug_m3": 0,
  "so2_ug_m3": 0,
  "co_mg_m3": 0
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

## References

- xRegistry manifest: [`xreg/fmi-finland.xreg.json`](xreg/fmi-finland.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
