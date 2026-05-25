# GIOŚ Poland Air Quality Poller Events

GIOŚ Poland Air Quality publishes sensor readings and air-quality index values from Poland's Chief Inspectorate of Environmental Protection (GIOŚ) for Polish air-quality monitoring stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 4 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 1 reference/catalog event type and 3 telemetry event types.
- **Identity:** `{station_id}`, `{station_id}/{sensor_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `gios-poland`. The record key is `{station_id}`. In plain language, `{station_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['gios-poland'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Station

CloudEvents type: `pl.gov.gios.airquality.Station`

#### What it tells you

Reference data for a GIOŚ air quality monitoring station, including its geographic location, city, commune, district, and voivodeship.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is unique numeric identifier of the monitoring station assigned by GIOŚ. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gios-poland`, key `{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `station_code`, `name`.

- **`station_id`** (integer, required): Unique numeric identifier of the monitoring station assigned by GIOŚ. Mapped from the Polish field 'Identyfikator stacji'.
- **`station_code`** (string, required): Short alphanumeric code uniquely identifying the station, e.g. 'DsLegAlRzecz'. Mapped from 'Kod stacji'.
- **`name`** (string, required): Human-readable name of the monitoring station, typically including city and street. Mapped from 'Nazwa stacji'.
- **`latitude`** (double or null, optional, deg (°N)): Latitude of the station in decimal degrees north (WGS84). Mapped from 'WGS84 φ N'.
- **`longitude`** (double or null, optional, deg (°E)): Longitude of the station in decimal degrees east (WGS84). Mapped from 'WGS84 λ E'.
- **`city_id`** (integer or null, optional): Numeric identifier of the city where the station is located. Mapped from 'Identyfikator miasta'.
- **`city_name`** (string or null, optional): Name of the city where the station is located. Mapped from 'Nazwa miasta'.
- **`commune`** (string or null, optional): Name of the commune (gmina) where the station is located. Mapped from 'Gmina'.
- **`district`** (string or null, optional): Name of the district (powiat) where the station is located. Mapped from 'Powiat'.
- **`voivodeship`** (string or null, optional): Name of the voivodeship (province) where the station is located, in uppercase Polish. Mapped from 'Województwo'.
- **`street`** (string or null, optional): Street address of the station, if available. Mapped from 'Ulica'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "station_code": "string",
  "name": "string",
  "latitude": 0,
  "longitude": 0,
  "city_id": 0,
  "city_name": "string",
  "commune": "string",
  "district": "string",
  "voivodeship": "string",
  "street": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Sensor

CloudEvents type: `pl.gov.gios.airquality.Sensor`

#### What it tells you

Reference data for a sensor (measurement point) installed at a GIOŚ station, identifying the pollutant it measures.

#### Identity

Each event identifies the real-world resource with `{station_id}/{sensor_id}`. `{station_id}` is numeric identifier of the parent monitoring station; `{sensor_id}` is unique numeric identifier of the sensor (measurement point) assigned by GIOŚ. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gios-poland`, key `{station_id}` |

#### Payload

`Sensor` payloads are JSON object. Required fields: `sensor_id`, `station_id`, `parameter_name`, `parameter_code`.

- **`sensor_id`** (integer, required): Unique numeric identifier of the sensor (measurement point) assigned by GIOŚ. Mapped from 'Identyfikator stanowiska'.
- **`station_id`** (integer, required): Numeric identifier of the parent monitoring station. Mapped from 'Identyfikator stacji'.
- **`parameter_name`** (string, required): Polish-language name of the measured pollutant, e.g. 'pył zawieszony PM10', 'dwutlenek azotu'. Mapped from 'Wskaźnik'.
- **`parameter_formula`** (string or null, optional): Chemical formula of the measured pollutant, e.g. 'PM10', 'NO2', 'SO2', 'O3', 'CO', 'C6H6', 'PM2.5'. Mapped from 'Wskaźnik - wzór'.
- **`parameter_code`** (string, required): Short code identifying the pollutant parameter, e.g. 'PM10', 'NO2'. Mapped from 'Wskaźnik - kod'.
- **`parameter_id`** (integer or null, optional): Numeric identifier of the pollutant parameter in the GIOŚ system. Mapped from 'Id wskaźnika'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sensor_id": 0,
  "station_id": 0,
  "parameter_name": "string",
  "parameter_formula": "string",
  "parameter_code": "string",
  "parameter_id": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Measurement

CloudEvents type: `pl.gov.gios.airquality.Measurement`

#### What it tells you

Hourly air quality measurement from a single sensor, reporting the concentration of the monitored pollutant in µg/m³.

#### Identity

Each event identifies the real-world resource with `{station_id}/{sensor_id}`. `{station_id}` is numeric identifier of the monitoring station that owns this sensor; `{sensor_id}` is numeric identifier of the sensor that produced this measurement. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gios-poland`, key `{station_id}` |

#### Payload

`Measurement` payloads are JSON object. Required fields: `station_id`, `sensor_id`, `sensor_code`, `timestamp`.

- **`station_id`** (integer, required): Numeric identifier of the monitoring station that owns this sensor.
- **`sensor_id`** (integer, required): Numeric identifier of the sensor that produced this measurement.
- **`sensor_code`** (string, required): Code identifying the sensor and its aggregation period, e.g. 'DsLegAlRzecz-NO2-1g'. Mapped from 'Kod stanowiska'.
- **`timestamp`** (datetime, required): Measurement timestamp in local Polish time (ISO 8601 format). Mapped from 'Data'.
- **`value`** (double or null, optional, ug/m3 (µg/m³)): Measured pollutant concentration. Unit: micrograms per cubic meter (µg/m³). Null when the measurement is missing or invalid. Mapped from 'Wartość'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "sensor_id": 0,
  "sensor_code": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "value": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Air Quality Index

CloudEvents type: `pl.gov.gios.airquality.AirQualityIndex`

#### What it tells you

Current Polish Air Quality Index for a station, including the overall index and sub-indices for individual pollutants (SO₂, NO₂, PM10, PM2.5, O₃).

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is numeric identifier of the monitoring station. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gios-poland`, key `{station_id}` |

#### Payload

`Air Quality Index` payloads are JSON object. Required fields: `station_id`, `calculation_timestamp`.

- **`station_id`** (integer, required): Numeric identifier of the monitoring station. Mapped from 'Identyfikator stacji pomiarowej'.
- **`calculation_timestamp`** (datetime, required): Timestamp when the overall index was calculated (ISO 8601 in local Polish time). Mapped from 'Data wykonania obliczeń indeksu'.
- **`index_value`** (integer or null, optional): Overall air quality index value: 0=Bardzo dobry (Very good), 1=Dobry (Good), 2=Umiarkowany (Moderate), 3=Dostateczny (Sufficient), 4=Zły (Bad), 5=Bardzo zły (Very bad). Mapped from 'Wartość indeksu'.
- **`index_category`** (string or null, optional): Polish-language category name of the overall index, e.g. 'Bardzo dobry', 'Dobry', 'Umiarkowany'. Mapped from 'Nazwa kategorii indeksu'.
- **`source_data_timestamp`** (datetime or null, optional): Timestamp of the source measurement data used for the overall index calculation. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika st'.
- **`so2_calculation_timestamp`** (datetime or null, optional): Timestamp when the SO₂ sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika SO2'.
- **`so2_index_value`** (integer or null, optional): SO₂ sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika SO2'.
- **`so2_index_category`** (string or null, optional): Polish-language category name for the SO₂ sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika SO2'.
- **`so2_source_data_timestamp`** (datetime or null, optional): Timestamp of the source data used for the SO₂ sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika SO2'.
- **`no2_calculation_timestamp`** (datetime or null, optional): Timestamp when the NO₂ sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika NO2'.
- **`no2_index_value`** (integer or null, optional): NO₂ sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika NO2'.
- **`no2_index_category`** (string or null, optional): Polish-language category name for the NO₂ sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika NO2'.
- **`no2_source_data_timestamp`** (datetime or null, optional): Timestamp of the source data used for the NO₂ sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika NO2'.
- **`pm10_calculation_timestamp`** (datetime or null, optional): Timestamp when the PM10 sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika PM10'.
- **`pm10_index_value`** (integer or null, optional): PM10 sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika PM10'.
- **`pm10_index_category`** (string or null, optional): Polish-language category name for the PM10 sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika PM10'.
- **`pm10_source_data_timestamp`** (datetime or null, optional): Timestamp of the source data used for the PM10 sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM10'.
- **`pm25_calculation_timestamp`** (datetime or null, optional): Timestamp when the PM2.5 sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika PM2.5'.
- **`pm25_index_value`** (integer or null, optional): PM2.5 sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika PM2.5'.
- **`pm25_index_category`** (string or null, optional): Polish-language category name for the PM2.5 sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika PM2.5'.
- **`pm25_source_data_timestamp`** (datetime or null, optional): Timestamp of the source data used for the PM2.5 sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika PM2.5'.
- **`o3_calculation_timestamp`** (datetime or null, optional): Timestamp when the O₃ sub-index was calculated. Mapped from 'Data wykonania obliczeń indeksu dla wskaźnika O3'.
- **`o3_index_value`** (integer or null, optional): O₃ sub-index value (0–5 scale). Mapped from 'Wartość indeksu dla wskaźnika O3'.
- **`o3_index_category`** (string or null, optional): Polish-language category name for the O₃ sub-index. Mapped from 'Nazwa kategorii indeksu dla wskażnika O3'.
- **`o3_source_data_timestamp`** (datetime or null, optional): Timestamp of the source data used for the O₃ sub-index. Mapped from 'Data danych źródłowych, z których policzono wartość indeksu dla wskaźnika O3'.
- **`overall_status`** (boolean or null, optional): Whether the overall air quality index is currently valid for this station. Mapped from 'Status indeksu ogólnego dla stacji pomiarowej'.
- **`critical_pollutant_code`** (string or null, optional): Code of the pollutant that determined the overall index value, e.g. 'OZON', 'PM10'. Mapped from 'Kod zanieczyszczenia krytycznego'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "calculation_timestamp": "2024-01-01T00:00:00Z",
  "index_value": 0,
  "index_category": "string",
  "source_data_timestamp": "2024-01-01T00:00:00Z",
  "so2_calculation_timestamp": "2024-01-01T00:00:00Z",
  "so2_index_value": 0,
  "so2_index_category": "string",
  "so2_source_data_timestamp": "2024-01-01T00:00:00Z",
  "no2_calculation_timestamp": "2024-01-01T00:00:00Z",
  "no2_index_value": 0,
  "no2_index_category": "string",
  "no2_source_data_timestamp": "2024-01-01T00:00:00Z",
  "pm10_calculation_timestamp": "2024-01-01T00:00:00Z",
  "pm10_index_value": 0,
  "pm10_index_category": "string",
  "pm10_source_data_timestamp": "2024-01-01T00:00:00Z",
  "pm25_calculation_timestamp": "2024-01-01T00:00:00Z",
  "pm25_index_value": 0,
  "pm25_index_category": "string",
  "pm25_source_data_timestamp": "2024-01-01T00:00:00Z",
  "o3_calculation_timestamp": "2024-01-01T00:00:00Z",
  "o3_index_value": 0,
  "o3_index_category": "string",
  "o3_source_data_timestamp": "2024-01-01T00:00:00Z",
  "overall_status": false,
  "critical_pollutant_code": "string"
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

- xRegistry manifest: [`xreg/gios_poland.xreg.json`](xreg/gios_poland.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
