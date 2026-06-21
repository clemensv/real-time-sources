# OpenAQ generalized air-quality feeder Events

[📑 Events](EVENTS.md) · [🐳 Container](CONTAINER.md) · [↗ OpenAQ API docs](https://docs.openaq.org/)

## At a glance

- **Event types:** 3 documented event types (12 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 2 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{location_id}`, `{location_id}/{sensor_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `openaq`. The record key is `{location_id}`, `{location_id}/{sensor_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['openaq'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `air-quality/global/openaq/+/+/info`, `air-quality/global/openaq/+/+/+/+/sensor`, `air-quality/global/openaq/+/+/+/+/measurement`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('air-quality/global/openaq/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `openaq`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/openaq')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Location

CloudEvents type: `org.openaq.Location`

#### What it tells you

Reference catalog metadata for one OpenAQ monitoring location from API v3 `GET /v3/locations`. It identifies a physical or mobile air-quality monitoring site, its WGS 84 coordinates, country, ownership/provider context, monitor/mobile flags, license attribution, and first/last observation dates. Emitted before measurement events and refreshed periodically so consumers can interpret measurements without separately calling OpenAQ.

#### Identity

Each event identifies the real-world resource with `{location_id}`. `{location_id}` is stable integer OpenAQ location identifier from upstream `id` or `locationsId`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `openaq`, key `{location_id}` |
| `MQTT/5.0` | topic `air-quality/global/openaq/{country_iso}/{location_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/openaq`, message subject `{location_id}` |

#### Payload

`Location` payloads are JSON object. Required fields: `location_id`, `timezone`, `country_iso`, `country_name`, `is_mobile`, `is_monitor`, `sensor_count`.

- **`location_id`** (int64, required): Stable integer OpenAQ location identifier from upstream `id` or `locationsId`. Used as the first CloudEvents subject, Kafka key, MQTT topic, and AMQP partition-key segment. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `1`.
- **`name`** (string or null, optional): Human-readable OpenAQ location name from upstream `name`; can be null. Mutable label for display only, never a key. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`locality`** (string or null, optional): Locality/city label from OpenAQ `locality`; can be null and is not a stable identifier. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`timezone`** (string, required): IANA timezone name for interpreting local operational context at the location, from OpenAQ `timezone`. Timestamps emitted by this feeder remain UTC/offset-aware. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`country_iso`** (string, required): ISO 3166-1 alpha-2 country code supplied by OpenAQ `country.iso`; used for configuration, routing, MQTT hierarchy, and consumer filtering. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: pattern `^[A-Z]{2}$`.
- **`country_name`** (string, required): Country name from the nested OpenAQ country object. Used for dashboards and attribution, not as a key. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`owner_id`** (int64 or null, optional): OpenAQ owner id from nested `owner.id`; identifies the data owner/contact where provided. Null when upstream omits it. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`owner_name`** (string or null, optional): Data owner display name from nested `owner.name`; mutable attribution label. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`provider_id`** (int64 or null, optional): OpenAQ provider id from nested `provider.id`; identifies the ingestion provider/source platform. Null when absent. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`provider_name`** (string or null, optional): OpenAQ provider display name from nested `provider.name`; useful for attribution and provider-specific quality triage. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`is_mobile`** (boolean, required): Boolean OpenAQ `isMobile` flag indicating whether the location represents a mobile platform rather than a fixed station. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`is_monitor`** (boolean, required): Boolean OpenAQ `isMonitor` flag indicating whether OpenAQ considers this location a reference monitor. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`latitude`** (double or null, optional, deg (°)): WGS 84 latitude in decimal degrees from `coordinates.latitude`; null when unavailable. Unit: degrees north. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double or null, optional, deg (°)): WGS 84 longitude in decimal degrees from `coordinates.longitude`; null when unavailable. Unit: degrees east. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `-180`, maximum `180`.
- **`datetime_first`** (datetime or null, optional): Earliest measurement timestamp known for this location from `datetimeFirst.utc` when present. Used to understand historical coverage. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`datetime_last`** (datetime or null, optional): Most recent measurement timestamp known for this location from `datetimeLast.utc` when present. Used to prioritize active feeds. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`license`** (string or null, optional): Semicolon-separated license names/attribution strings from OpenAQ `licenses`; preserve for downstream attribution and compliance. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`sensor_count`** (int32, required): Number of parameter-specific sensors listed in the location payload. Useful for completeness checks and dashboard summaries. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `0`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "location_id": 0,
  "name": "string",
  "locality": "string",
  "timezone": "string",
  "country_iso": "string",
  "country_name": "string",
  "owner_id": 0,
  "owner_name": "string",
  "provider_id": 0,
  "provider_name": "string",
  "is_mobile": false,
  "is_monitor": false,
  "latitude": 0,
  "longitude": 0,
  "datetime_first": "2024-01-01T00:00:00Z",
  "datetime_last": "2024-01-01T00:00:00Z",
  "license": "string",
  "sensor_count": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Sensor

CloudEvents type: `org.openaq.Sensor`

#### What it tells you

Reference catalog metadata for one OpenAQ sensor from API v3 `GET /v3/locations/{locations_id}/sensors`. A sensor represents one parameter-specific measurement stream at a location, carrying the stable sensor id, sensor name, parameter id/name/units, date coverage, and most recent value metadata when OpenAQ exposes it. Reference metadata for one OpenAQ sensor from API v3 `GET /v3/locations/{locations_id}/sensors`.

#### Identity

Each event identifies the real-world resource with `{location_id}/{sensor_id}`. `{location_id}` is stable integer OpenAQ location identifier from upstream `id` or `locationsId`; `{sensor_id}` is stable integer OpenAQ sensor identifier from upstream `id` or `sensorsId`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `openaq`, key `{location_id}/{sensor_id}` |
| `MQTT/5.0` | topic `air-quality/global/openaq/{country_iso}/{location_id}/{parameter_name}/{sensor_id}/sensor`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/openaq`, message subject `{location_id}/{sensor_id}` |

#### Payload

`Sensor` payloads are JSON object. Required fields: `location_id`, `sensor_id`, `country_iso`, `sensor_name`, `parameter_id`, `parameter_name`, `parameter_units`.

- **`location_id`** (int64, required): Stable integer OpenAQ location identifier from upstream `id` or `locationsId`. Used as the first CloudEvents subject, Kafka key, MQTT topic, and AMQP partition-key segment. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `1`.
- **`sensor_id`** (int64, required): Stable integer OpenAQ sensor identifier from upstream `id` or `sensorsId`. Identifies one parameter-specific stream at a location. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `1`.
- **`country_iso`** (string, required): ISO 3166-1 alpha-2 country code supplied by OpenAQ `country.iso`; used for configuration, routing, MQTT hierarchy, and consumer filtering. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: pattern `^[A-Z]{2}$`.
- **`sensor_name`** (string, required): OpenAQ sensor name from upstream `name`; typically derived from parameter and location. Mutable label, not a key. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`parameter_id`** (int64, required): OpenAQ parameter identifier from the parameter object. Joins to `/v3/parameters`; stable across locations and sensors. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `1`.
- **`parameter_name`** (enum, required): OpenAQ machine-readable parameter name, for example pm25, pm10, o3, no2, so2, co, bc, temperature, relativehumidity, pressure, or windspeed. Used as a routing segment; not localized. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`parameter_units`** (string, required): Unit string as published by OpenAQ `/v3/parameters` or nested parameter metadata, commonly µg/m³ for particulate and gas mass concentrations and ppm/ppb for some gas feeds. Preserve exactly for consumers that need unit-aware conversions. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`parameter_display_name`** (string or null, optional): Human-friendly parameter label from `parameter.displayName`; may be null. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`datetime_first`** (datetime or null, optional): Earliest timestamp for this sensor stream from `datetimeFirst.utc`; null when OpenAQ has no coverage metadata. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`datetime_last`** (datetime or null, optional): Latest timestamp for this sensor stream from `datetimeLast.utc`; used with measurement dedupe. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`latest_value`** (double or null, optional): Latest value embedded in the sensor reference payload when present. Unit is `parameter_units`; telemetry consumers should use Measurement events for time-series values. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`latest_datetime`** (datetime or null, optional): Timestamp of `latest_value` from nested `latest.datetime.utc`; null when the sensor reference does not include latest data. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`latitude`** (double or null, optional, deg (°)): WGS 84 latitude of the latest sensor value when present in nested `latest.coordinates`; unit degrees north. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double or null, optional, deg (°)): WGS 84 longitude of the latest sensor value when present in nested `latest.coordinates`; unit degrees east. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `-180`, maximum `180`.
##### `parameter_name` values

- `pm25` — Fine particulate matter with aerodynamic diameter <= 2.5 µm; commonly reported by OpenAQ in µg/m³.
- `pm10` — Particulate matter with aerodynamic diameter <= 10 µm; commonly reported by OpenAQ in µg/m³.
- `o3` — Ozone concentration; commonly reported by OpenAQ in µg/m³, ppb, or ppm depending on provider.
- `no2` — Nitrogen dioxide concentration; commonly reported by OpenAQ in µg/m³, ppb, or ppm depending on provider.
- `so2` — Sulfur dioxide concentration; commonly reported by OpenAQ in µg/m³, ppb, or ppm depending on provider.
- `co` — Carbon monoxide concentration; commonly reported by OpenAQ in µg/m³, ppm, or ppb depending on provider.
- `bc` — Black carbon concentration; commonly reported by OpenAQ in µg/m³.
- `no` — Nitric oxide concentration; units are carried in parameter_units exactly as OpenAQ publishes them.
- `nox` — Nitrogen oxides concentration; units are carried in parameter_units exactly as OpenAQ publishes them.
- `pm1` — Particulate matter with aerodynamic diameter <= 1 µm; commonly reported in µg/m³.
- `co2` — Carbon dioxide concentration; units are carried in parameter_units exactly as OpenAQ publishes them.
- `temperature` — Ambient temperature measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `relativehumidity` — Relative humidity measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `pressure` — Atmospheric pressure measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `windspeed` — Wind speed measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `winddirection` — Wind direction measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `um003` — Ultrafine particle count channel for particles >= 0.03 µm; units are carried in parameter_units.
- `um005` — Ultrafine particle count channel for particles >= 0.05 µm; units are carried in parameter_units.
- `um010` — Ultrafine particle count channel for particles >= 0.10 µm; units are carried in parameter_units.
- `um025` — Ultrafine particle count channel for particles >= 0.25 µm; units are carried in parameter_units.
- `um050` — Ultrafine particle count channel for particles >= 0.50 µm; units are carried in parameter_units.
- `um100` — Ultrafine particle count channel for particles >= 1.00 µm; units are carried in parameter_units.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "location_id": 0,
  "sensor_id": 0,
  "country_iso": "string",
  "sensor_name": "string",
  "parameter_id": 0,
  "parameter_name": "pm25",
  "parameter_units": "string",
  "parameter_display_name": "string",
  "datetime_first": "2024-01-01T00:00:00Z",
  "datetime_last": "2024-01-01T00:00:00Z",
  "latest_value": 0,
  "latest_datetime": "2024-01-01T00:00:00Z",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Measurement

CloudEvents type: `org.openaq.Measurement`

#### What it tells you

Latest air-quality measurement for one OpenAQ sensor/location pair from API v3 `GET /v3/locations/{locations_id}/latest`. It carries the observed concentration or meteorological value, parameter metadata and units, timestamp, and coordinates. The bridge polls latest values and emits only changed timestamps/values per sensor.

#### Identity

Each event identifies the real-world resource with `{location_id}/{sensor_id}`. `{location_id}` is stable integer OpenAQ location identifier from upstream `id` or `locationsId`; `{sensor_id}` is stable integer OpenAQ sensor identifier from upstream `id` or `sensorsId`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `openaq`, key `{location_id}/{sensor_id}` |
| `MQTT/5.0` | topic `air-quality/global/openaq/{country_iso}/{location_id}/{parameter_name}/{sensor_id}/measurement`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/openaq`, message subject `{location_id}/{sensor_id}` |

#### Payload

`Measurement` payloads are JSON object. Required fields: `location_id`, `sensor_id`, `country_iso`, `parameter_id`, `parameter_name`, `parameter_units`, `datetime`, `poll_time`.

- **`location_id`** (int64, required): Stable integer OpenAQ location identifier from upstream `id` or `locationsId`. Used as the first CloudEvents subject, Kafka key, MQTT topic, and AMQP partition-key segment. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `1`.
- **`sensor_id`** (int64, required): Stable integer OpenAQ sensor identifier from upstream `id` or `sensorsId`. Identifies one parameter-specific stream at a location. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `1`.
- **`country_iso`** (string, required): ISO 3166-1 alpha-2 country code supplied by OpenAQ `country.iso`; used for configuration, routing, MQTT hierarchy, and consumer filtering. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: pattern `^[A-Z]{2}$`.
- **`parameter_id`** (int64, required): OpenAQ parameter identifier from the parameter object. Joins to `/v3/parameters`; stable across locations and sensors. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `1`.
- **`parameter_name`** (enum, required): OpenAQ machine-readable parameter name, for example pm25, pm10, o3, no2, so2, co, bc, temperature, relativehumidity, pressure, or windspeed. Used as a routing segment; not localized. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`parameter_units`** (string, required): Unit string as published by OpenAQ `/v3/parameters` or nested parameter metadata, commonly µg/m³ for particulate and gas mass concentrations and ppm/ppb for some gas feeds. Preserve exactly for consumers that need unit-aware conversions. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`datetime`** (datetime, required): Observation timestamp from OpenAQ `datetime.utc` for the latest measurement. This is the time the value represents, not the bridge polling time. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`value`** (double or null, optional): Measured concentration or meteorological value from OpenAQ `value`. Unit is carried in `parameter_units`; common air pollutant units include µg/m³ for pm25, pm10, o3, no2, so2, co, and bc, with ppm/ppb appearing for some providers. Null values are preserved when upstream flags a record without a numeric value. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`latitude`** (double or null, optional, deg (°)): WGS 84 latitude attached to the measurement from `coordinates.latitude`; unit degrees north. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double or null, optional, deg (°)): WGS 84 longitude attached to the measurement from `coordinates.longitude`; unit degrees east. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/). Constraints: minimum `-180`, maximum `180`.
- **`is_valid`** (boolean or null, optional): Boolean validity summary derived from OpenAQ `flagInfo.hasFlags` when the `/v3/locations/{locations_id}/latest` payload includes that optional extension: false when flags are present, true when no flags are present, null when the latest endpoint omits flag info. Definitive historical flag detail is available from OpenAQ flag/measurement endpoints outside this real-time latest-feed scope. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`has_flags`** (boolean or null, optional): OpenAQ flag summary from `flagInfo.hasFlags` when the `/v3/locations/{locations_id}/latest` payload includes that optional extension; null when the latest endpoint omits flag metadata. Full flag windows are intentionally out of scope for the real-time latest poller. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
- **`poll_time`** (datetime, required): UTC time when the bridge fetched and emitted this latest measurement. This supports latency monitoring and replay diagnostics; it is not an upstream observation time. Source: bridge runtime.
##### `parameter_name` values

- `pm25` — Fine particulate matter with aerodynamic diameter <= 2.5 µm; commonly reported by OpenAQ in µg/m³.
- `pm10` — Particulate matter with aerodynamic diameter <= 10 µm; commonly reported by OpenAQ in µg/m³.
- `o3` — Ozone concentration; commonly reported by OpenAQ in µg/m³, ppb, or ppm depending on provider.
- `no2` — Nitrogen dioxide concentration; commonly reported by OpenAQ in µg/m³, ppb, or ppm depending on provider.
- `so2` — Sulfur dioxide concentration; commonly reported by OpenAQ in µg/m³, ppb, or ppm depending on provider.
- `co` — Carbon monoxide concentration; commonly reported by OpenAQ in µg/m³, ppm, or ppb depending on provider.
- `bc` — Black carbon concentration; commonly reported by OpenAQ in µg/m³.
- `no` — Nitric oxide concentration; units are carried in parameter_units exactly as OpenAQ publishes them.
- `nox` — Nitrogen oxides concentration; units are carried in parameter_units exactly as OpenAQ publishes them.
- `pm1` — Particulate matter with aerodynamic diameter <= 1 µm; commonly reported in µg/m³.
- `co2` — Carbon dioxide concentration; units are carried in parameter_units exactly as OpenAQ publishes them.
- `temperature` — Ambient temperature measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `relativehumidity` — Relative humidity measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `pressure` — Atmospheric pressure measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `windspeed` — Wind speed measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `winddirection` — Wind direction measurement; units are carried in parameter_units exactly as OpenAQ publishes them.
- `um003` — Ultrafine particle count channel for particles >= 0.03 µm; units are carried in parameter_units.
- `um005` — Ultrafine particle count channel for particles >= 0.05 µm; units are carried in parameter_units.
- `um010` — Ultrafine particle count channel for particles >= 0.10 µm; units are carried in parameter_units.
- `um025` — Ultrafine particle count channel for particles >= 0.25 µm; units are carried in parameter_units.
- `um050` — Ultrafine particle count channel for particles >= 0.50 µm; units are carried in parameter_units.
- `um100` — Ultrafine particle count channel for particles >= 1.00 µm; units are carried in parameter_units.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "location_id": 0,
  "sensor_id": 0,
  "country_iso": "string",
  "parameter_id": 0,
  "parameter_name": "pm25",
  "parameter_units": "string",
  "datetime": "2024-01-01T00:00:00Z",
  "value": 0,
  "latitude": 0,
  "longitude": 0,
  "is_valid": false,
  "has_flags": false,
  "poll_time": "2024-01-01T00:00:00Z"
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

- xRegistry manifest: [`xreg/openaq.xreg.json`](xreg/openaq.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- ↗ OpenAQ API docs: <https://docs.openaq.org/>
