# DMI Events

<sub>meteorological observations, sea level, lightning strikes · Kafka · MQTT · AMQP · <a href="https://www.dmi.dk/">upstream</a> · <a href="https://opendatadocs.dmi.govcloud.dk/">API docs</a></sub>

## At a glance

- **Event types:** 8 documented event types (30 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 3 reference/catalog event types and 5 telemetry event types.
- **Identity:** `{station_id}`, `{station_id}/{parameter_id}`, `{sensor_id}`, `{strike_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `dmi`. The record key is not declared. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['dmi'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/dk/dmi/met-obs/+/info`, `weather/dk/dmi/met-obs/+/+`, `ocean/dk/dmi/ocean-obs/+/info`, `ocean/dk/dmi/tidewater/+/info`, `ocean/dk/dmi/ocean-obs/+/+`, `ocean/dk/dmi/tidewater/+/prediction`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/dk/dmi/met-obs/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `dmi`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/dmi')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `dk.dmi.metObs.MetObsStation`

#### What it tells you

Reference data for a DMI meteorological observation station. Emitted at feeder startup and refreshed daily. Stations cover Denmark, Greenland (DNK/GRL) and the Faroe Islands (FRO).

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable DMI station identifier (e.g. '06030', '04202' for Pituffik in Greenland). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dmi`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/dk/dmi/met-obs/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dmi`, message subject `{station_id}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `name`, `country`, `latitude`, `longitude`.

- **`station_id`** (string, required): Stable DMI station identifier (e.g. '06030', '04202' for Pituffik in Greenland). Used as the Kafka partition key and CloudEvent subject.
- **`wmo_station_id`** (string or null, optional): World Meteorological Organization (WMO) station identifier when registered with WMO.
- **`wmo_country_code`** (string or null, optional): WMO country code as an integer string (e.g. '06' for Denmark).
- **`name`** (string, required): Human-readable station name.
- **`country`** (enum, required): ISO 3166-1 alpha-3 country code: 'DNK' (Denmark), 'GRL' (Greenland), 'FRO' (Faroe Islands).
- **`owner`** (string or null, optional): Organisation that owns/operates the station (typically 'DMI').
- **`region_id`** (string or null, optional): DMI region identifier within the country.
- **`type`** (string or null, optional): Station type as classified by DMI (e.g. 'Synop', 'PluvioSync').
- **`status`** (string or null, optional): Operational status (e.g. 'Active', 'Inactive').
- **`parameter_id`** (array of string, optional): List of DMI parameterId values this station reports (e.g. ['temp_dry','wind_speed','humidity']).
- **`latitude`** (double, required, deg): Station latitude in decimal degrees (WGS84). Derived from GeoJSON geometry.coordinates[1]. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, deg): Station longitude in decimal degrees (WGS84). Derived from GeoJSON geometry.coordinates[0]. Constraints: minimum `-180`, maximum `180`.
- **`station_height`** (double or null, optional, m): Height of the station above mean sea level.
- **`barometer_height`** (double or null, optional, m): Height of the barometer above mean sea level.
- **`anemometer_height`** (double or null, optional, m): Height of the anemometer above ground level.
- **`valid_from`** (datetime or null, optional): Timestamp from which this station-metadata version is valid.
- **`valid_to`** (datetime or null, optional): Timestamp after which this station-metadata version is no longer valid; null while current.
- **`operation_from`** (datetime or null, optional): Timestamp from which the station began operating.
- **`operation_to`** (datetime or null, optional): Timestamp at which the station stopped operating; null while operational.
- **`created`** (datetime or null, optional): Timestamp when this metadata row was created by DMI.
- **`updated`** (datetime or null, optional): Timestamp when this metadata row was last updated by DMI.
##### `country` values

- `DNK` — Denmark
- `GRL` — Greenland
- `FRO` — Faroe Islands
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "wmo_station_id": "string",
  "wmo_country_code": "string",
  "name": "string",
  "country": "DNK",
  "owner": "string",
  "region_id": "string",
  "type": "string",
  "status": "string",
  "parameter_id": [
    "string"
  ],
  "latitude": 0,
  "longitude": 0,
  "station_height": 0,
  "barometer_height": 0,
  "anemometer_height": 0,
  "valid_from": "2024-01-01T00:00:00Z",
  "valid_to": "2024-01-01T00:00:00Z",
  "operation_from": "2024-01-01T00:00:00Z",
  "operation_to": "2024-01-01T00:00:00Z",
  "created": "2024-01-01T00:00:00Z",
  "updated": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Observation

CloudEvents type: `dk.dmi.metObs.MetObsObservation`

#### What it tells you

A single meteorological observation value reported by a station for one parameter at a specific observed time. Cadence depends on parameter (10-minute or hourly). A single meteorological observation: one parameter, one station, one timestamp.

#### Identity

Each event identifies the real-world resource with `{station_id}/{parameter_id}`. `{station_id}` is reporting station identifier (foreign key to Station); `{parameter_id}` is DMI parameter identifier (e.g. 'temp_dry', 'wind_speed', 'humidity', 'pressure_at_sea'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dmi`, key `{station_id}/{parameter_id}` |
| `MQTT/5.0` | topic `weather/dk/dmi/met-obs/{station_id}/{parameter_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dmi`, message subject `{station_id}/{parameter_id}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `station_id`, `parameter_id`, `observed`, `value`.

- **`observation_id`** (string or null, optional): DMI-assigned per-row identifier. Not stable across re-ingestions; use (station_id, parameter_id, observed) for idempotency.
- **`station_id`** (string, required): Reporting station identifier (foreign key to Station).
- **`parameter_id`** (enum, required): DMI parameter identifier (e.g. 'temp_dry', 'wind_speed', 'humidity', 'pressure_at_sea').
- **`observed`** (datetime, required): Timestamp at which the value was observed (UTC, ISO 8601).
- **`value`** (double, required): Numeric measurement value. Units depend on parameter_id (see DMI documentation).
- **`latitude`** (double or null, optional, deg): Station latitude (decimal degrees, WGS84) at observation time. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double or null, optional, deg): Station longitude (decimal degrees, WGS84) at observation time. Constraints: minimum `-180`, maximum `180`.
##### `parameter_id` values

- `temp_dry`
- `temp_dew`
- `temp_grass`
- `temp_soil_10cm`
- `temp_mean_past1h`
- `temp_max_past1h`
- `temp_min_past1h`
- `humidity`
- `humidity_past1h`
- `pressure`
- `pressure_at_sea`
- `wind_dir`
- `wind_dir_past1h`
- `wind_speed`
- `wind_speed_past1h`
- `wind_max`
- `wind_min`
- `wind_max_per10min_past1h`
- `wind_min_past1h`
- `gust_always_past1h`
- `precip_past1h`
- `precip_past10min`
- `precip_past24h`
- `snow_depth_man`
- `snow_cover_man`
- `visibility`
- `visib_mean_last10min`
- `cloud_cover`
- `cloud_height`
- `weather`
- `leav_hum_dur_past10min`
- `radia_glob`
- `radia_glob_past1h`
- `sun_last10min_glob`
- `sun_last1h_glob`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "observation_id": "string",
  "station_id": "string",
  "parameter_id": "temp_dry",
  "observed": "2024-01-01T00:00:00Z",
  "value": 0,
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Ocean Station

CloudEvents type: `dk.dmi.oceanObs.OceanStation`

#### What it tells you

Reference data for an oceanographic observation station (tide gauge or other coastal sensor). Owners include DMI and Kystdirektoratet (Danish Coastal Authority). An oceanographic observation station (typically a tide gauge).

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable DMI ocean station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dmi`, key `{station_id}` |
| `MQTT/5.0` | topic `ocean/dk/dmi/ocean-obs/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dmi`, message subject `{station_id}` |

#### Payload

`Ocean Station` payloads are JSON object. Required fields: `station_id`, `name`, `latitude`, `longitude`.

- **`station_id`** (string, required): Stable DMI ocean station identifier.
- **`name`** (string, required): Human-readable station name.
- **`country`** (string or null, optional): ISO 3166-1 alpha-3 country code (DNK, GRL, FRO).
- **`owner`** (string or null, optional): Operating agency (e.g. 'DMI', 'Kystdirektoratet').
- **`type`** (string or null, optional): Station type (e.g. 'Tide-gauge-primary').
- **`status`** (string or null, optional): Operational status.
- **`parameter_id`** (array of string, optional): Parameter IDs supported by this station (subset of {sealev_dvr, sealev_ln, sea_reg, tw}).
- **`latitude`** (double, required, deg): Station latitude (decimal degrees, WGS84). Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, deg): Station longitude (decimal degrees, WGS84). Constraints: minimum `-180`, maximum `180`.
- **`valid_from`** (datetime or null, optional): Metadata-validity start.
- **`valid_to`** (datetime or null, optional): Metadata-validity end.
- **`operation_from`** (datetime or null, optional): No description provided.
- **`operation_to`** (datetime or null, optional): No description provided.
- **`created`** (datetime or null, optional): No description provided.
- **`updated`** (datetime or null, optional): No description provided.
##### `country` values

- `DNK` — Denmark
- `GRL` — Greenland
- `FRO` — Faroe Islands
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "country": "DNK",
  "owner": "string",
  "type": "string",
  "status": "string",
  "parameter_id": [
    "string"
  ],
  "latitude": 0,
  "longitude": 0,
  "valid_from": "2024-01-01T00:00:00Z",
  "valid_to": "2024-01-01T00:00:00Z",
  "operation_from": "2024-01-01T00:00:00Z",
  "operation_to": "2024-01-01T00:00:00Z",
  "created": "2024-01-01T00:00:00Z",
  "updated": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Tidewater Station

CloudEvents type: `dk.dmi.oceanObs.TidewaterStation`

#### What it tells you

Reference data for a station/grid-point at which DMI publishes tidewater (sea-level) predictions. The set partially overlaps physical tide gauges but also includes prediction-only grid points (e.g. Faroes).

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier of the tidewater prediction station/grid-point. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dmi`, key `{station_id}` |
| `MQTT/5.0` | topic `ocean/dk/dmi/tidewater/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dmi`, message subject `{station_id}` |

#### Payload

`Tidewater Station` payloads are JSON object. Required fields: `station_id`, `latitude`, `longitude`.

- **`station_id`** (string, required): Stable identifier of the tidewater prediction station/grid-point.
- **`name`** (string or null, optional): Human-readable station name where available.
- **`country`** (string or null, optional): ISO 3166-1 alpha-3 country code.
- **`owner`** (string or null, optional): Operating agency.
- **`latitude`** (double, required, deg): Prediction-point latitude (decimal degrees, WGS84). Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, deg): Prediction-point longitude (decimal degrees, WGS84). Constraints: minimum `-180`, maximum `180`.
- **`valid_from`** (datetime or null, optional): No description provided.
- **`valid_to`** (datetime or null, optional): No description provided.
##### `country` values

- `DNK` — Denmark
- `GRL` — Greenland
- `FRO` — Faroe Islands
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "name": "string",
  "country": "DNK",
  "owner": "string",
  "latitude": 0,
  "longitude": 0,
  "valid_from": "2024-01-01T00:00:00Z",
  "valid_to": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Ocean Observation

CloudEvents type: `dk.dmi.oceanObs.OceanObservation`

#### What it tells you

A single oceanographic observation. Parameters are sealev_dvr (sea level vs DVR90 datum, cm), sealev_ln (sea level vs local zero, cm), sea_reg (registered sea level by Kystdirektoratet, cm), and tw (water temperature, deg C). 10-minute cadence.

#### Identity

Each event identifies the real-world resource with `{station_id}/{parameter_id}`. `{station_id}` is a payload field with the same name; `{parameter_id}` is one of sealev_dvr, sealev_ln, sea_reg, tw. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dmi`, key `{station_id}/{parameter_id}` |
| `MQTT/5.0` | topic `ocean/dk/dmi/ocean-obs/{station_id}/{parameter_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dmi`, message subject `{station_id}/{parameter_id}` |

#### Payload

`Ocean Observation` payloads are JSON object. Required fields: `station_id`, `parameter_id`, `observed`, `value`.

- **`observation_id`** (string or null, optional): DMI-assigned row identifier (not stable across re-ingestions).
- **`station_id`** (string, required): No description provided.
- **`parameter_id`** (enum, required): One of sealev_dvr, sealev_ln, sea_reg, tw.
- **`observed`** (datetime, required): No description provided.
- **`value`** (double, required): Numeric value. cm for sealev_*/sea_reg, deg C for tw.
- **`latitude`** (double or null, optional, deg): No description provided. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double or null, optional, deg): No description provided. Constraints: minimum `-180`, maximum `180`.
##### `parameter_id` values

- `sealev_dvr`
- `sealev_ln`
- `sea_reg`
- `tw`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "observation_id": "string",
  "station_id": "string",
  "parameter_id": "sealev_dvr",
  "observed": "2024-01-01T00:00:00Z",
  "value": 0,
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Tidewater Prediction

CloudEvents type: `dk.dmi.oceanObs.TidewaterPrediction`

#### What it tells you

A deterministic tidewater (sea-level) prediction for one station and one forecast horizon. predictionType is typically '10minutes'; predictions are issued forward ~30 days. Predictions are issued every model cycle and span ~30 days at 10-minute granularity.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dmi`, key `{station_id}` |
| `MQTT/5.0` | topic `ocean/dk/dmi/tidewater/{station_id}/prediction`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dmi`, message subject `{station_id}` |

#### Payload

`Tidewater Prediction` payloads are JSON object. Required fields: `station_id`, `prediction_time`, `value`.

- **`prediction_id`** (string or null, optional): DMI-assigned row identifier.
- **`station_id`** (string, required): No description provided.
- **`prediction_type`** (string or null, optional): Granularity of the prediction series (typically '10minutes').
- **`prediction_time`** (datetime, required): Target time for which the value is predicted.
- **`value`** (double, required, cm): Predicted sea level (cm vs DVR90 unless otherwise noted).
- **`latitude`** (double or null, optional, deg): No description provided. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double or null, optional, deg): No description provided. Constraints: minimum `-180`, maximum `180`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "prediction_id": "string",
  "station_id": "string",
  "prediction_type": "string",
  "prediction_time": "2024-01-01T00:00:00Z",
  "value": 0,
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Lightning Sensor

CloudEvents type: `dk.dmi.lightning.LightningSensor`

#### What it tells you

Reference data for one of DMI's lightning detection sensors. Six DMI-owned sensors cover Denmark; third-party sensor IDs that appear in observation.sensors are not catalogued here. A DMI lightning detection sensor site.

#### Identity

Each event identifies the real-world resource with `{sensor_id}`. `{sensor_id}` is stable sensor identifier (1..6 for DMI-owned sensors). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dmi`, key `{sensor_id}` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dmi`, message subject `{sensor_id}` |

#### Payload

`Lightning Sensor` payloads are JSON object. Required fields: `sensor_id`, `latitude`, `longitude`.

- **`sensor_id`** (string, required): Stable sensor identifier (1..6 for DMI-owned sensors).
- **`name`** (string or null, optional): Human-readable sensor site name.
- **`owner`** (string or null, optional): Operating agency (typically 'DMI').
- **`country`** (string or null, optional): ISO 3166-1 alpha-3 country code (typically 'DNK').
- **`latitude`** (double, required, deg): No description provided. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, deg): No description provided. Constraints: minimum `-180`, maximum `180`.
- **`active_from`** (datetime or null, optional): No description provided.
- **`active_to`** (datetime or null, optional): No description provided.
##### `country` values

- `DNK` — Denmark
- `GRL` — Greenland
- `FRO` — Faroe Islands
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sensor_id": "string",
  "name": "string",
  "owner": "string",
  "country": "DNK",
  "latitude": 0,
  "longitude": 0,
  "active_from": "2024-01-01T00:00:00Z",
  "active_to": "2024-01-01T00:00:00Z"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Lightning Strike

CloudEvents type: `dk.dmi.lightning.LightningStrike`

#### What it tells you

A single triangulated lightning strike. Type 0 = cloud-to-ground negative, 1 = cloud-to-ground positive, 2 = cloud-to-cloud. amp is signed peak current in kA.

#### Identity

Each event identifies the real-world resource with `{strike_id}`. `{strike_id}` is stable DMI-assigned strike identifier (e.g. 'u1xrxj10262553824830001-03'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dmi`, key `{strike_id}` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dmi`, message subject `{strike_id}` |

#### Payload

`Lightning Strike` payloads are JSON object. Required fields: `strike_id`, `observed`, `type`, `latitude`, `longitude`.

- **`strike_id`** (string, required): Stable DMI-assigned strike identifier (e.g. 'u1xrxj10262553824830001-03').
- **`observed`** (datetime, required): Strike timestamp (UTC, microsecond precision).
- **`created`** (datetime or null, optional): Timestamp when DMI ingested the strike.
- **`type`** (integer, required): Strike type code.
- **`amp`** (double or null, optional, kA): Signed peak current.
- **`strokes`** (integer or null, optional): Number of return strokes. Constraints: minimum `1`.
- **`sensors`** (string or null, optional): Comma-separated list of sensor IDs that contributed to triangulation (may include third-party sensors not in the Sensor catalog).
- **`latitude`** (double, required, deg): Strike latitude (decimal degrees, WGS84). Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, deg): Strike longitude (decimal degrees, WGS84). Constraints: minimum `-180`, maximum `180`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "strike_id": "string",
  "observed": "2024-01-01T00:00:00Z",
  "created": "2024-01-01T00:00:00Z",
  "type": 0,
  "amp": 0,
  "strokes": 0,
  "sensors": "string",
  "latitude": 0,
  "longitude": 0
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/dmi.xreg.json`](xreg/dmi.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Danish Meteorological Institute Open Data
API: <https://opendatadocs.dmi.govcloud.dk/>
- https://dmiapi.govcloud.dk/: <https://dmiapi.govcloud.dk/>
