# Environment Canada Weather Observation Bridge Events

Environment Canada Weather publishes current weather observations from Environment and Climate Change Canada (ECCC) for Canadian weather stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{msc_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `environment-canada`. The record key is `{msc_id}`. In plain language, `{msc_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['environment-canada'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `CA.Gov.ECCC.Weather.Station`

#### What it tells you

A reference record published by Environment and Climate Change Canada (ECCC). It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{msc_id}`. `{msc_id}` is MSC station identifier (Meteorological Service of Canada ID), also known as Climate ID. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `environment-canada`, key `{msc_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `msc_id`, `name`.

- **`msc_id`** (string, required): MSC station identifier (Meteorological Service of Canada ID), also known as Climate ID. Used as Kafka key.
- **`name`** (string, required): Station name as listed in the SWOB station registry, e.g. 'TORONTO PEARSON INTL A', 'VANCOUVER INTL A'.
- **`iata_id`** (string, optional): IATA station code, e.g. 'CYYZ' for Toronto Pearson.
- **`wmo_id`** (int32 or null, optional): WMO synoptic station identifier, e.g. 71624 for Toronto Pearson. Null for stations without a WMO assignment.
- **`province_territory`** (string, optional): Canadian province or territory where the station is located, e.g. 'Ontario', 'British Columbia'.
- **`data_provider`** (string, optional): Organization providing the data, typically 'MSC' for Meteorological Service of Canada.
- **`dataset_network`** (string, optional): Network identifier, typically 'CA' for Canadian stations.
- **`auto_man`** (string, optional): Station type: 'AUTO' for automatic, 'MAN' for manual, or combination.
- **`latitude`** (double or null, optional, degree (°)): WGS84 latitude of the station in decimal degrees.
- **`longitude`** (double or null, optional, degree (°)): WGS84 longitude of the station in decimal degrees.
- **`elevation`** (double or null, optional, m): Station elevation above sea level in meters.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "msc_id": "string",
  "name": "string",
  "iata_id": "string",
  "wmo_id": 0,
  "province_territory": "string",
  "data_provider": "string",
  "dataset_network": "string",
  "auto_man": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Weather Observation

CloudEvents type: `CA.Gov.ECCC.Weather.WeatherObservation`

#### What it tells you

A current environmental measurement from Environment and Climate Change Canada (ECCC). It carries current weather observations when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{msc_id}`. `{msc_id}` is MSC station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `environment-canada`, key `{msc_id}` |

#### Payload

`Weather Observation` payloads are JSON object. Required fields: `msc_id`, `station_name`, `observation_time`.

- **`msc_id`** (string, required): MSC station identifier.
- **`station_name`** (string, required): Station name from the SWOB record.
- **`observation_time`** (datetime, required): Observation timestamp in UTC from the obs_date_tm field.
- **`air_temperature`** (double or null, optional, Cel (°C)): Instantaneous air temperature from the air_temp field.
- **`dew_point`** (double or null, optional, Cel (°C)): Dew point temperature from the dwpt_temp field.
- **`relative_humidity`** (int32 or null, optional, percent (%)): Relative humidity from the rel_hum field.
- **`station_pressure`** (double or null, optional, hPa): Station-level atmospheric pressure from the stn_pres field.
- **`wind_speed`** (double or null, optional, km/h): Average wind speed at 10m over the last 1 minute from avg_wnd_spd_10m_pst1mt.
- **`wind_direction`** (int32 or null, optional, degree (°)): Average wind direction at 10m over the last 1 minute from avg_wnd_dir_10m_pst1mt, in degrees clockwise from true north.
- **`wind_gust`** (double or null, optional, km/h): Maximum wind speed at 10m in the last 1 minute from max_wnd_spd_10m_pst1mt.
- **`precipitation_1hr`** (double or null, optional, mm): Total precipitation in the last hour from pcpn_amt_pst1hr.
- **`mean_sea_level_pressure`** (double or null, optional, hPa): Mean sea-level pressure (MSLP) from the mslp field. Available on synoptic and hourly reporting stations. Null on minutely auto-only stations.
- **`visibility`** (double or null, optional, km): Horizontal visibility from the vis field. Primarily available on staffed and NAV CANADA stations.
- **`snow_depth`** (double or null, optional, cm): Snow depth on the ground from the snw_dpth field. Available on stations equipped with ultrasonic snow depth sensors.
- **`total_cloud_cover`** (int32 or null, optional): Total cloud amount code from the tot_cld_amt field. Reports cloud cover in tenths (0-10) or oktas depending on reporting convention. Available on staffed and select automated stations.
- **`pressure_tendency_3hr`** (double or null, optional, hPa): Change in station pressure over the preceding 3 hours from pres_tend_amt_pst3hrs. Positive values indicate rising pressure.
- **`max_temperature_24hr`** (double or null, optional, Cel (°C)): Maximum air temperature in the past 24 hours from max_air_temp_pst24hrs.
- **`min_temperature_24hr`** (double or null, optional, Cel (°C)): Minimum air temperature in the past 24 hours from min_air_temp_pst24hrs.
- **`wind_speed_1hr`** (double or null, optional, km/h): Average wind speed at 10m over the past hour from avg_wnd_spd_10m_pst1hr.
- **`wind_gust_1hr`** (double or null, optional, km/h): Maximum wind speed at 10m in the past hour from max_wnd_spd_10m_pst1hr.
- **`precipitation_24hr`** (double or null, optional, mm): Total precipitation in the past 24 hours from pcpn_amt_pst24hrs.
- **`altimeter_setting`** (double or null, optional, [in_i'Hg] (inHg)): Altimeter setting from the altmetr_setng field. Used in aviation.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "msc_id": "string",
  "station_name": "string",
  "observation_time": "2024-01-01T00:00:00Z",
  "air_temperature": 0,
  "dew_point": 0,
  "relative_humidity": 0,
  "station_pressure": 0,
  "wind_speed": 0,
  "wind_direction": 0,
  "wind_gust": 0,
  "precipitation_1hr": 0,
  "mean_sea_level_pressure": 0,
  "visibility": 0,
  "snow_depth": 0,
  "total_cloud_cover": 0,
  "pressure_tendency_3hr": 0,
  "max_temperature_24hr": 0,
  "min_temperature_24hr": 0,
  "wind_speed_1hr": 0,
  "wind_gust_1hr": 0,
  "precipitation_24hr": 0,
  "altimeter_setting": 0
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

- xRegistry manifest: [`xreg/environment_canada.xreg.json`](xreg/environment_canada.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Environment and Climate Change Canada (ECCC) GeoMet API: <https://api.weather.gc.ca/>
