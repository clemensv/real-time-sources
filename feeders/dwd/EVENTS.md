# DWD Events

DWD Weather publishes weather observations, warnings, and forecast product updates from Germany's Deutscher Wetterdienst (DWD) for German weather stations, alerts, radar, and forecast products. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 13 documented event types (39 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 12 telemetry event types.
- **Identity:** `{station_id}`, `{identifier}`, `{file_url}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `dwd`. The record key is `{station_id}`, `{identifier}`, `{file_url}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['dwd'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/de/dwd/dwd/+/+/info`, `weather/de/dwd/dwd/+/+/air-temperature-10min`, `weather/de/dwd/dwd/+/+/precipitation-10min`, `weather/de/dwd/dwd/+/+/wind-10min`, `weather/de/dwd/dwd/+/+/solar-10min`, `weather/de/dwd/dwd/+/+/hourly-observation`, `weather/de/dwd/dwd/+/+/extreme-wind-10min`, `weather/de/dwd/dwd/+/+/extreme-temperature-10min`, `alerts/de/dwd/dwd/+/+/+/alert`, `weather/de/dwd/dwd/catalogs/+/catalog`, `weather/de/dwd/dwd/products/radar/+/+/file`, `weather/de/dwd/dwd/products/icon-d2/+/+/file`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/de/dwd/dwd/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `dwd`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/dwd')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station Metadata

CloudEvents type: `DE.DWD.CDC.StationMetadata`

#### What it tells you

A reference record published by Germany's Deutscher Wetterdienst (DWD). It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the station or monitoring site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/{state}/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{station_id}` |

#### Payload

`Station Metadata` payloads are JSON object. Required fields: `station_id`, `station_name`, `latitude`, `longitude`, `elevation`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the station or monitoring site.
- **`station_name`** (string, required): Human-readable name of the station or monitoring site.
- **`latitude`** (double, required): Latitude of the station or site in WGS 84 coordinates.
- **`longitude`** (double, required): Longitude of the station or site in WGS 84 coordinates.
- **`elevation`** (double, required): Elevation of the station above mean sea level or the provider datum.
- **`state`** (string, optional): State, province, or administrative region for the station or area.
- **`from_date`** (string, optional): Start date when the station, product, or metadata record is valid.
- **`to_date`** (string, optional): End date when the station, product, or metadata record is valid, when known.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation": 0,
  "state": "string",
  "from_date": "string",
  "to_date": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Air Temperature10 Min

CloudEvents type: `DE.DWD.CDC.AirTemperature10Min`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the station or monitoring site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/{state}/{station_id}/air-temperature-10min`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{station_id}` |

#### Payload

`Air Temperature10 Min` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the station or monitoring site.
- **`timestamp`** (string, required): Time when the provider recorded or published the value.
- **`quality_level`** (int32, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`pressure_station_level`** (null or double, optional): Reference details for a station, monitoring site, or reporting area in the DWD Weather source.
- **`air_temperature_2m`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`air_temperature_5cm`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`relative_humidity`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`dew_point_temperature`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "quality_level": 0,
  "pressure_station_level": 0,
  "air_temperature_2m": 0,
  "air_temperature_5cm": 0,
  "relative_humidity": 0,
  "dew_point_temperature": 0,
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Precipitation10 Min

CloudEvents type: `DE.DWD.CDC.Precipitation10Min`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the station or monitoring site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/{state}/{station_id}/precipitation-10min`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{station_id}` |

#### Payload

`Precipitation10 Min` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the station or monitoring site.
- **`timestamp`** (string, required): Time when the provider recorded or published the value.
- **`quality_level`** (int32, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`precipitation_height`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`precipitation_indicator`** (null or int32, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "quality_level": 0,
  "precipitation_height": 0,
  "precipitation_indicator": 0,
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Wind10 Min

CloudEvents type: `DE.DWD.CDC.Wind10Min`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the station or monitoring site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/{state}/{station_id}/wind-10min`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{station_id}` |

#### Payload

`Wind10 Min` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the station or monitoring site.
- **`timestamp`** (string, required): Time when the provider recorded or published the value.
- **`quality_level`** (int32, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`wind_speed`** (null or double, optional): Wind speed reported by the station.
- **`wind_direction`** (null or double, optional): Wind direction reported by the station.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "quality_level": 0,
  "wind_speed": 0,
  "wind_direction": 0,
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Solar10 Min

CloudEvents type: `DE.DWD.CDC.Solar10Min`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the station or monitoring site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/{state}/{station_id}/solar-10min`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{station_id}` |

#### Payload

`Solar10 Min` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the station or monitoring site.
- **`timestamp`** (string, required): Time when the provider recorded or published the value.
- **`quality_level`** (int32, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`global_radiation`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`sunshine_duration`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`diffuse_radiation`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`longwave_radiation`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "quality_level": 0,
  "global_radiation": 0,
  "sunshine_duration": 0,
  "diffuse_radiation": 0,
  "longwave_radiation": 0,
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Hourly Observation

CloudEvents type: `DE.DWD.CDC.HourlyObservation`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the station or monitoring site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/{state}/{station_id}/hourly-observation`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{station_id}` |

#### Payload

`Hourly Observation` payloads are JSON object. Required fields: `station_id`, `timestamp`, `parameter`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the station or monitoring site.
- **`timestamp`** (string, required): Time when the provider recorded or published the value.
- **`quality_level`** (int32, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`parameter`** (string, required): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`value`** (double, optional): Measured or forecast value reported by the upstream provider.
- **`unit`** (string, optional): Unit used for the reported value.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "quality_level": 0,
  "parameter": "string",
  "value": 0,
  "unit": "string",
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Extreme Wind10 Min

CloudEvents type: `DE.DWD.CDC.ExtremeWind10Min`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the station or monitoring site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/{state}/{station_id}/extreme-wind-10min`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{station_id}` |

#### Payload

`Extreme Wind10 Min` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the station or monitoring site.
- **`timestamp`** (string, required): Time when the provider recorded or published the value.
- **`quality_level`** (int32, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`wind_speed_maximum`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`wind_speed_minimum`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`wind_direction_at_maximum`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "quality_level": 0,
  "wind_speed_maximum": 0,
  "wind_speed_minimum": 0,
  "wind_direction_at_maximum": 0,
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Extreme Temperature10 Min

CloudEvents type: `DE.DWD.CDC.ExtremeTemperature10Min`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable identifier assigned by the upstream provider for the station or monitoring site. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/{state}/{station_id}/extreme-temperature-10min`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{station_id}` |

#### Payload

`Extreme Temperature10 Min` payloads are JSON object. Required fields: `station_id`, `timestamp`.

- **`station_id`** (string, required): Stable identifier assigned by the upstream provider for the station or monitoring site.
- **`timestamp`** (string, required): Time when the provider recorded or published the value.
- **`quality_level`** (int32, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`air_temperature_maximum_2m`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`air_temperature_minimum_5cm`** (null or double, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "timestamp": "string",
  "quality_level": 0,
  "air_temperature_maximum_2m": 0,
  "air_temperature_minimum_5cm": 0,
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Alert

CloudEvents type: `DE.DWD.Weather.Alert`

#### What it tells you

A weather or environmental alert from Germany's Deutscher Wetterdienst (DWD). It fires when the upstream source publishes or updates a warning that may affect the covered area.

#### Identity

Each event identifies the real-world resource with `{identifier}`. `{identifier}` is measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{identifier}` |
| `MQTT/5.0` | topic `alerts/de/dwd/dwd/{state}/{severity}/{identifier}/alert`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{state}/{severity}/{identifier}` |

#### Payload

`Alert` payloads are JSON object. Required fields: `identifier`, `sender`, `sent`, `severity`, `event`.

- **`identifier`** (string, required): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`sender`** (string, required): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`sent`** (string, required): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`status`** (string, optional): Provider status value for the station, product, warning, or measurement.
- **`msg_type`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`severity`** (string, required): Provider severity level for a warning or alert.
- **`urgency`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`certainty`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`event`** (string, required): Provider event type, warning type, or product event category.
- **`headline`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`description`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`effective`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`onset`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`expires`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`area_desc`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`geocodes`** (string, optional): Measurement payload for weather observations, warnings, and forecast product updates in the DWD Weather source.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "identifier": "string",
  "sender": "string",
  "sent": "string",
  "status": "string",
  "msg_type": "string",
  "severity": "string",
  "urgency": "string",
  "certainty": "string",
  "event": "string",
  "headline": "string",
  "description": "string",
  "effective": "string",
  "onset": "string",
  "expires": "string",
  "area_desc": "string",
  "geocodes": "string",
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Radar Product Catalog

CloudEvents type: `DE.DWD.Radar.RadarProductCatalog`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{file_url}`. `{file_url}` is absolute HTTPS URL of the DWD Open Data directory that holds all files for this radar product. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{file_url}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/catalogs/{kind}/catalog`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{kind}` |

#### Payload

`Radar Product Catalog` payloads are JSON object. Required fields: `product`, `file_url`.

- **`product`** (string, required): Short identifier of the DWD radar composite product family (for example 'wn', 'rv', 'rs', 'dmax', 'hg', 'hx', 'pg', 'vii', 'hymecng'). Derived from the first-level directory name under https://opendata.dwd.de/weather/radar/composite/. All RadarFileProduct events for files inside this directory carry the same product value.
- **`file_url`** (string, required): Absolute HTTPS URL of the DWD Open Data directory that holds all files for this radar product. The URL is publicly fetchable with an unauthenticated HTTP GET and returns an Apache autoindex HTML listing, so consumers can enumerate current and historical product files without credentials. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key for catalog events. Example: 'https://opendata.dwd.de/weather/radar/composite/wn/'.
- **`description`** (string, optional): Optional human-readable description of the radar product as configured by the bridge. Intended for catalog browsers, documentation, and operator UIs; not derived from upstream metadata.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
- **`kind`** (null or string, optional): Normalized routing field 'kind' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "product": "string",
  "file_url": "string",
  "description": "string",
  "state": "string",
  "kind": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Radar File Product

CloudEvents type: `DE.DWD.Radar.RadarFileProduct`

#### What it tells you

A current environmental measurement from Germany's Deutscher Wetterdienst (DWD). It carries weather observations, warnings, and forecast product updates when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{file_url}`. `{file_url}` is absolute HTTPS URL of a single DWD radar product file on the DWD Open Data server. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{file_url}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/products/radar/{product_type}/{file_id}/file`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{product_type}/{file_id}` |

#### Payload

`Radar File Product` payloads are JSON object. Required fields: `file_url`, `product`, `file_name`, `modified`.

- **`file_url`** (string, required): Absolute HTTPS URL of a single DWD radar product file on the DWD Open Data server. The URL is publicly fetchable with an unauthenticated HTTP GET and supports HTTP Range and If-Modified-Since/ETag conditional requests, so handlers can dereference the event by performing a plain GET against this URL. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key, which guarantees per-file ordering. Example: 'https://opendata.dwd.de/weather/radar/composite/wn/composite_wn_20260517_2005-hd5'.
- **`product`** (string, required): Short identifier of the radar product family this file belongs to (for example 'wn', 'rv', 'dmax'); matches the 'product' field of the corresponding RadarProductCatalog event.
- **`file_name`** (string, required): Bare file name (no directory component) as listed in the DWD Apache directory index. Convenient for parsing the embedded product code and observation timestamp without having to split file_url.
- **`modified`** (string, required): Upstream Last-Modified timestamp of the file as reported by the DWD Apache directory listing, expressed as an ISO 8601 UTC string. The bridge emits a new RadarFileProduct event whenever this value changes for a known file_url, so consumers can use it for change detection and de-duplication.
- **`size_bytes`** (int64 or null, optional): File size in bytes as parsed from the DWD directory listing, or null when the listing does not expose a size. Indicative only; for an authoritative size consumers should rely on the Content-Length header returned by the actual GET on file_url. Radar composite files typically range from tens of KB (BUFR products) up to roughly 10 MB (large HDF5 composites).
- **`file_id`** (string, optional): Normalized routing field 'file_id' added for MQTT/AMQP subscriber filtering.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
- **`product_type`** (string, optional): Normalized routing field 'product_type' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "file_url": "string",
  "product": "string",
  "file_name": "string",
  "modified": "string",
  "size_bytes": 0,
  "file_id": "string",
  "state": "string",
  "product_type": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Forecast Model Catalog

CloudEvents type: `DE.DWD.Forecast.ForecastModelCatalog`

#### What it tells you

A forecast from Germany's Deutscher Wetterdienst (DWD) for one area or station. It carries weather observations, warnings, and forecast product updates for the period published by the upstream source.

#### Identity

Each event identifies the real-world resource with `{file_url}`. `{file_url}` is absolute HTTPS URL of the DWD Open Data root directory under which all GRIB2 files for this forecast model are published. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{file_url}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/catalogs/{kind}/catalog`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{kind}` |

#### Payload

`Forecast Model Catalog` payloads are JSON object. Required fields: `model`, `file_url`.

- **`model`** (string, required): Identifier of the numerical weather prediction (NWP) model. For this bridge release the value is 'icon-d2', referring to the DWD ICON-D2 convection-permitting regional model covering Germany and surrounding areas with ~2 km horizontal resolution and forecast lead times up to 48 hours.
- **`file_url`** (string, required): Absolute HTTPS URL of the DWD Open Data root directory under which all GRIB2 files for this forecast model are published. The URL is publicly fetchable with an unauthenticated HTTP GET and returns an Apache autoindex HTML listing. Run-hour subdirectories (e.g. '00/', '03/', '06/', ...) and per-variable subdirectories live below this URL. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key for catalog events. Example: 'https://opendata.dwd.de/weather/nwp/icon-d2/grib/'.
- **`description`** (string, optional): Optional human-readable description of the forecast model emitted as reference data. Intended for catalog browsers, documentation, and operator UIs; not derived from upstream metadata.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
- **`kind`** (null or string, optional): Normalized routing field 'kind' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "model": "string",
  "file_url": "string",
  "description": "string",
  "state": "string",
  "kind": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Icon D2 Forecast File

CloudEvents type: `DE.DWD.Forecast.IconD2ForecastFile`

#### What it tells you

A forecast from Germany's Deutscher Wetterdienst (DWD) for one area or station. It carries weather observations, warnings, and forecast product updates for the period published by the upstream source.

#### Identity

Each event identifies the real-world resource with `{file_url}`. `{file_url}` is absolute HTTPS URL of a single ICON-D2 GRIB2 forecast file on the DWD Open Data server. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `dwd`, key `{file_url}` |
| `MQTT/5.0` | topic `weather/de/dwd/dwd/products/icon-d2/{variable}/{file_id}/file`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/dwd`, message subject `{variable}/{file_id}` |

#### Payload

`Icon D2 Forecast File` payloads are JSON object. Required fields: `file_url`, `model`, `file_name`, `modified`.

- **`file_url`** (string, required): Absolute HTTPS URL of a single ICON-D2 GRIB2 forecast file on the DWD Open Data server. The file is bzip2-compressed GRIB2 (.grib2.bz2) and can be fetched with an unauthenticated HTTP GET; the server supports HTTP Range and If-Modified-Since/ETag conditional requests, so handlers can dereference the event with a plain GET against this URL. Each file holds a single variable at a single vertical level for a single forecast lead hour, which keeps per-file payloads small (typically a few hundred KB compressed). Also used verbatim as the CloudEvents 'subject' and the Kafka partition key. Example: 'https://opendata.dwd.de/weather/nwp/icon-d2/grib/00/t/icon-d2_germany_icosahedral_model-level_2026051700_003_10_t.grib2.bz2'.
- **`model`** (string, required): Identifier of the source forecast model; matches the 'model' field of the corresponding ForecastModelCatalog event. Currently always 'icon-d2'.
- **`file_name`** (string, required): Bare file name as listed in the DWD Apache directory index, following the DWD convention 'icon-d2_<grid>_<level_type>_<run>_<lead>_<level>_<parameter>.grib2.bz2'. Convenient for parsing without splitting file_url.
- **`run`** (string or null, optional): Model run cycle in 'YYYYMMDDHH' UTC form, parsed from file_name (e.g. '2026051700' for the 00 UTC run on 2026-05-17). ICON-D2 is run every three hours. Null when the file name does not match the expected pattern (for example time-invariant or auxiliary files).
- **`forecast_hour`** (int32 or null, optional): Forecast lead time in whole hours from the start of the run, parsed from file_name. For ICON-D2 this ranges from 0 to 48. Null when the file name does not match the expected pattern.
- **`parameter`** (string or null, optional): Short ICON-D2 parameter identifier parsed from file_name (for example 't' for temperature, 'u'/'v' for wind components, 'tot_prec' for total precipitation, 'clct' for total cloud cover, 'alb_rad' for shortwave albedo).
- **`level_type`** (string or null, optional): Vertical level encoding parsed from file_name. Common values are 'single-level' (surface and 2D fields), 'model-level' (native ICON hybrid levels indexed 1..65 from top to bottom), 'pressure-level' (interpolated to fixed pressure surfaces, in hPa), and 'time-invariant' (constant fields such as orography).
- **`level`** (string or null, optional): Vertical level value token parsed from file_name. The interpretation depends on level_type: model-level uses an integer level index, pressure-level uses pressure in hPa, single-level may carry a short surface tag or be omitted.
- **`modified`** (string, required): Upstream Last-Modified timestamp from the DWD Apache directory listing, expressed as an ISO 8601 UTC string. The bridge emits a new IconD2ForecastFile event whenever this value changes for a known file_url, enabling change detection and de-duplication.
- **`size_bytes`** (int64 or null, optional): File size in bytes as parsed from the DWD directory listing, or null when the listing does not expose a size. Indicative only; for an authoritative size rely on the Content-Length header from the actual GET on file_url. Individual ICON-D2 .grib2.bz2 files are typically well below 1 MB compressed.
- **`state`** (null or string, optional): Normalized routing field 'state' added for MQTT/AMQP subscriber filtering.
- **`variable`** (string, optional): Normalized routing field 'variable' added for MQTT/AMQP subscriber filtering.
- **`file_id`** (string, optional): Normalized routing field 'file_id' added for MQTT/AMQP subscriber filtering.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "file_url": "string",
  "model": "string",
  "file_name": "string",
  "run": "string",
  "forecast_hour": 0,
  "parameter": "string",
  "level_type": "string",
  "level": "string",
  "modified": "string",
  "size_bytes": 0,
  "state": "string",
  "variable": "string",
  "file_id": "string"
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/dwd.xreg.json`](xreg/dwd.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
- opendata.dwd.de: <https://opendata.dwd.de/>
- Azure Service Bus emulator: <https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator>
