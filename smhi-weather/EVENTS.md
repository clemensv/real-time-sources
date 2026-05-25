# SMHI Weather Observation Bridge Events

SMHI Weather publishes weather observations from the Swedish Meteorological and Hydrological Institute (SMHI) for Swedish weather stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{station_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `smhi-weather`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['smhi-weather'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `SE.Gov.SMHI.Weather.Station`

#### What it tells you

A reference record published by the Swedish Meteorological and Hydrological Institute (SMHI). It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is SMHI numeric station identifier, unique within the SMHI observation network. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `smhi-weather`, key `{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `name`, `latitude`, `longitude`.

- **`station_id`** (string, required): SMHI numeric station identifier, unique within the SMHI observation network.
- **`name`** (string, required): Human-readable station name as assigned by SMHI, e.g. 'Abisko Aut' or 'Stockholm-Arlanda'.
- **`owner`** (string, optional): Organization or entity that owns and operates the station, e.g. 'SMHI' or 'Polarforskningssekretariatet'.
- **`owner_category`** (string, optional): Category of station ownership, e.g. 'CLIMATE' for long-running climate stations or 'AVIATION' for airport stations.
- **`measuring_stations`** (string, optional): Station classification within SMHI's measuring station network, e.g. 'CORE' for primary network stations.
- **`height`** (double, optional, m): Sensor height above ground in meters.
- **`latitude`** (double, required, degree (°)): Geographic latitude of the station in decimal degrees.
- **`longitude`** (double, required, degree (°)): Geographic longitude of the station in decimal degrees.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "owner": "string",
  "owner_category": "string",
  "measuring_stations": "string",
  "height": 0,
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Weather Observation

CloudEvents type: `SE.Gov.SMHI.Weather.WeatherObservation`

#### What it tells you

A current environmental measurement from the Swedish Meteorological and Hydrological Institute (SMHI). It carries weather observations when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is SMHI station identifier for the reporting station. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `smhi-weather`, key `{station_id}` |

#### Payload

`Weather Observation` payloads are JSON object. Required fields: `station_id`, `station_name`, `observation_time`.

- **`station_id`** (string, required): SMHI station identifier for the reporting station.
- **`station_name`** (string, required): Human-readable name of the reporting station.
- **`observation_time`** (datetime, required): Timestamp of the observation in UTC, derived from the SMHI epoch millisecond value.
- **`air_temperature`** (double or null, optional, Cel (°C)): Instantaneous air temperature, reported hourly (SMHI parameter 1).
- **`wind_gust`** (double or null, optional, m/s): Maximum wind gust speed, reported hourly (SMHI parameter 21).
- **`dew_point`** (double or null, optional, Cel (°C)): Dew point temperature, reported hourly (SMHI parameter 39).
- **`air_pressure`** (double or null, optional, hPa): Atmospheric pressure reduced to mean sea level, reported hourly (SMHI parameter 9).
- **`relative_humidity`** (int32 or null, optional, percent (%)): Relative humidity as a percentage, reported hourly (SMHI parameter 6).
- **`precipitation_last_hour`** (double or null, optional, mm): Total precipitation in the last hour, reported hourly (SMHI parameter 7).
- **`wind_direction`** (double or null, optional, degree (°)): Wind direction in degrees from which the wind is blowing, measured at 10 m height, reported hourly (SMHI parameter 3).
- **`wind_speed`** (double or null, optional, m/s): Mean wind speed over 10 minutes measured at 10 m height, reported hourly (SMHI parameter 4).
- **`max_wind_speed`** (double or null, optional, m/s): Maximum of 10-minute mean wind speed during the hour, measured at 10 m height (SMHI parameter 25).
- **`visibility`** (double or null, optional, km): Horizontal visibility, reported hourly (SMHI parameter 12).
- **`total_cloud_cover`** (int32 or null, optional, okta): Total cloud cover in oktas (eighths of sky covered), reported hourly (SMHI parameter 16).
- **`present_weather`** (int32 or null, optional): WMO present weather code (ww table 4677) describing current weather phenomena at the time of observation (SMHI parameter 13). Values range from 0 (clear) to 99 (thunderstorm with hail).
- **`sunshine_duration`** (double or null, optional, s): Duration of sunshine during the last hour in seconds (SMHI parameter 10).
- **`global_irradiance`** (double or null, optional, W/m2 (W/m²)): Global solar irradiance (direct + diffuse), average over the hour, measured by pyranometer (SMHI parameter 11).
- **`precipitation_intensity`** (double or null, optional, mm/h): Instantaneous precipitation intensity measured by optical or weighing gauge (SMHI parameter 38).
- **`quality`** (string, optional): Quality flag for the observation as assigned by SMHI: 'G' for approved, 'Y' for suspect.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "observation_time": "2024-01-01T00:00:00Z",
  "air_temperature": 0,
  "wind_gust": 0,
  "dew_point": 0,
  "air_pressure": 0,
  "relative_humidity": 0,
  "precipitation_last_hour": 0,
  "wind_direction": 0,
  "wind_speed": 0,
  "max_wind_speed": 0,
  "visibility": 0,
  "total_cloud_cover": 0,
  "present_weather": 0,
  "sunshine_duration": 0,
  "global_irradiance": 0,
  "precipitation_intensity": 0,
  "quality": "string"
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

- xRegistry manifest: [`xreg/smhi_weather.xreg.json`](xreg/smhi_weather.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- SMHI Open Data Meteorological Observations API: <https://opendata.smhi.se/apidocs/metobs/>
