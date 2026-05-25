# KMI Belgium Weather Observation Bridge Events

KMI Belgium Weather publishes weather observations from the Royal Meteorological Institute of Belgium (KMI/IRM) for Belgian weather stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{station_code}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `kmi-belgium`. The record key is `{station_code}`. In plain language, `{station_code}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['kmi-belgium'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `BE.Gov.KMI.Weather.Station`

#### What it tells you

A reference record published by the Royal Meteorological Institute of Belgium (KMI/IRM). It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{station_code}`. `{station_code}` is KMI/RMI automatic weather station code from the GeoJSON feature property `code`, unique within the Belgian AWS network. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `kmi-belgium`, key `{station_code}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_code`, `latitude`, `longitude`.

- **`station_code`** (string, required): KMI/RMI automatic weather station code from the GeoJSON feature property `code`, unique within the Belgian AWS network.
- **`latitude`** (double, required, degree (°)): Geographic latitude of the station in decimal degrees (WGS 84), derived from the second value of the GeoJSON `geometry.coordinates` array.
- **`longitude`** (double, required, degree (°)): Geographic longitude of the station in decimal degrees (WGS 84), derived from the first value of the GeoJSON `geometry.coordinates` array.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_code": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Weather Observation

CloudEvents type: `BE.Gov.KMI.Weather.WeatherObservation`

#### What it tells you

A current environmental measurement from the Royal Meteorological Institute of Belgium (KMI/IRM). It carries weather observations when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_code}`. `{station_code}` is KMI/RMI automatic weather station code from the `code` property of the reporting observation feature. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `kmi-belgium`, key `{station_code}` |

#### Payload

`Weather Observation` payloads are JSON object. Required fields: `station_code`, `observation_time`.

- **`station_code`** (string, required): KMI/RMI automatic weather station code from the `code` property of the reporting observation feature.
- **`observation_time`** (datetime, required): Observation timestamp in UTC from the feature property `timestamp`.
- **`precip_quantity`** (double or null, optional, mm): Precipitation quantity reported for the 10-minute observation period.
- **`temp_dry_shelter_avg`** (double or null, optional, Cel (°C)): Average air temperature measured in the 2 m dry shelter during the observation period.
- **`temp_grass_pt100_avg`** (double or null, optional, Cel (°C)): Average grass-level temperature measured by the Pt100 sensor during the observation period.
- **`temp_soil_avg`** (double or null, optional, Cel (°C)): Average soil surface temperature during the observation period.
- **`temp_soil_avg_5cm`** (double or null, optional, Cel (°C)): Average soil temperature measured at 5 cm depth during the observation period.
- **`temp_soil_avg_10cm`** (double or null, optional, Cel (°C)): Average soil temperature measured at 10 cm depth during the observation period.
- **`temp_soil_avg_20cm`** (double or null, optional, Cel (°C)): Average soil temperature measured at 20 cm depth during the observation period.
- **`temp_soil_avg_50cm`** (double or null, optional, Cel (°C)): Average soil temperature measured at 50 cm depth during the observation period.
- **`wind_speed_10m`** (double or null, optional, m/s): Wind speed measured at 10 m above ground level.
- **`wind_speed_avg_30m`** (double or null, optional, m/s): Average wind speed measured at 30 m above ground level.
- **`wind_direction`** (double or null, optional, degree (°)): Wind direction in degrees from which the wind is blowing.
- **`wind_gusts_speed`** (double or null, optional, m/s): Maximum wind gust speed observed during the 10-minute period.
- **`humidity_rel_shelter_avg`** (double or null, optional, percent (%)): Average relative humidity measured in the shelter during the observation period.
- **`pressure`** (double or null, optional, hPa): Station-level atmospheric pressure reported by the automatic weather station.
- **`sun_duration`** (double or null, optional, min): Sunshine duration accumulated during the 10-minute observation period.
- **`short_wave_from_sky_avg`** (double or null, optional, W/m2 (W/m²)): Average downward shortwave radiation from the sky during the observation period.
- **`sun_int_avg`** (double or null, optional, W/m2 (W/m²)): Average direct sunshine intensity during the observation period.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_code": "string",
  "observation_time": "2024-01-01T00:00:00Z",
  "precip_quantity": 0,
  "temp_dry_shelter_avg": 0,
  "temp_grass_pt100_avg": 0,
  "temp_soil_avg": 0,
  "temp_soil_avg_5cm": 0,
  "temp_soil_avg_10cm": 0,
  "temp_soil_avg_20cm": 0,
  "temp_soil_avg_50cm": 0,
  "wind_speed_10m": 0,
  "wind_speed_avg_30m": 0,
  "wind_direction": 0,
  "wind_gusts_speed": 0,
  "humidity_rel_shelter_avg": 0,
  "pressure": 0,
  "sun_duration": 0,
  "short_wave_from_sky_avg": 0,
  "sun_int_avg": 0
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

- xRegistry manifest: [`xreg/kmi_belgium.xreg.json`](xreg/kmi_belgium.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- KMI/RMI open data AWS service: <https://opendata.meteo.be/service/aws/ows>

## MQTT and AMQP companion transports

This source now ships Kafka plus dedicated MQTT and AMQP companion containers. MQTT publishes binary-mode CloudEvents into the source-specific UNS topic tree declared in `xreg/`; AMQP publishes the same CloudEvents to the configured queue or topic address (`kmi-belgium`). Docker E2E mock mode is available through `KMI_BELGIUM_MOCK=true`.

- MQTT image: `ghcr.io/clemensv/real-time-sources/kmi-belgium-mqtt`
- AMQP image: `ghcr.io/clemensv/real-time-sources/kmi-belgium-amqp`
- MQTT templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`
- AMQP templates: `azure-template-amqp.json`, `azure-template-with-servicebus.json`
