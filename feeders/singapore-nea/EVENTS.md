# Singapore NEA feeder Events

Singapore NEA Environment publishes weather observations, air-quality readings, and environmental indexes from Singapore's National Environment Agency (NEA) for Singapore weather and air-quality regions and stations. These events help consumers build monitoring, alerting, analytics, and dashboards without polling the upstream API directly.

## At a glance

- **Event types:** 5 documented event types (15 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 5 telemetry event types.
- **Identity:** `{station_id}`, `{region}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `singapore-nea`, `singapore-nea-airquality`. The record key is `{station_id}`, `{region}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['singapore-nea', 'singapore-nea-airquality'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/sg/nea/singapore-nea/+/+/+`, `air-quality/sg/nea/singapore-nea/+/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/sg/nea/singapore-nea/+/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `singapore-nea`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/singapore-nea')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `SG.Gov.NEA.Weather.Station`

#### What it tells you

A reference record published by Singapore's National Environment Agency (NEA). It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NEA station identifier, e.g. 'S109', 'S50'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `singapore-nea`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/sg/nea/singapore-nea/{region}/{station_id}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/singapore-nea`, message subject `{station_id}`; application properties region `{region}`, event `{event}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_id`, `name`, `latitude`, `longitude`.

- **`station_id`** (string, required): NEA station identifier, e.g. 'S109', 'S50'. Matches the device_id field in the NEA API metadata.
- **`device_id`** (string, optional): Device identifier, typically identical to station_id.
- **`name`** (string, required): Human-readable station name describing the location, e.g. 'Ang Mo Kio Avenue 5', 'Changi'.
- **`latitude`** (double, required, degree (°)): WGS84 latitude of the station.
- **`longitude`** (double, required, degree (°)): WGS84 longitude of the station.
- **`data_types`** (string, optional): Comma-separated list of observation types this station reports. Values: 'air_temperature', 'rainfall', 'relative_humidity', 'wind_speed', 'wind_direction'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "device_id": "string",
  "name": "string",
  "latitude": 0,
  "longitude": 0,
  "data_types": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Weather Observation

CloudEvents type: `SG.Gov.NEA.Weather.WeatherObservation`

#### What it tells you

A current environmental measurement from Singapore's National Environment Agency (NEA). It carries weather observations, air-quality readings, and environmental indexes when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is NEA station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `singapore-nea`, key `{station_id}` |
| `MQTT/5.0` | topic `weather/sg/nea/singapore-nea/{region}/{station_id}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/singapore-nea`, message subject `{station_id}`; application properties region `{region}`, event `{event}` |

#### Payload

`Weather Observation` payloads are JSON object. Required fields: `station_id`, `station_name`, `observation_time`.

- **`station_id`** (string, required): NEA station identifier.
- **`station_name`** (string, required): Station location name.
- **`observation_time`** (datetime, required): Timestamp of the observation in ISO 8601 with Singapore timezone (+08:00).
- **`air_temperature`** (double or null, optional, Cel (°C)): Air temperature from the air-temperature endpoint.
- **`rainfall`** (double or null, optional, mm): Rainfall amount in the last 5 minutes from the rainfall endpoint.
- **`relative_humidity`** (double or null, optional, percent (%)): Relative humidity from the relative-humidity endpoint.
- **`wind_speed`** (double or null, optional, kn): Wind speed from the wind-speed endpoint.
- **`wind_direction`** (double or null, optional, degree (°)): Wind direction in degrees clockwise from true north, from the wind-direction endpoint.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "observation_time": "2024-01-01T00:00:00Z",
  "air_temperature": 0,
  "rainfall": 0,
  "relative_humidity": 0,
  "wind_speed": 0,
  "wind_direction": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Region

CloudEvents type: `SG.Gov.NEA.AirQuality.Region`

#### What it tells you

A reference record published by Singapore's National Environment Agency (NEA). It lets consumers label, group, and route the live measurement or forecast events.

#### Identity

Each event identifies the real-world resource with `{region}`. `{region}` is region identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `singapore-nea-airquality`, key `{region}` |
| `MQTT/5.0` | topic `air-quality/sg/nea/singapore-nea/{region}/{station_id}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/singapore-nea`, message subject `{region}`; application properties station_id `{station_id}`, event `{event}` |

#### Payload

`Region` payloads are JSON object. Required fields: `region`, `latitude`, `longitude`.

- **`region`** (string, required): Region identifier. One of: west, east, central, south, north.
- **`latitude`** (double, required, degree (°)): WGS84 latitude of the region label location as published by the NEA API.
- **`longitude`** (double, required, degree (°)): WGS84 longitude of the region label location as published by the NEA API.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "region": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Psireading

CloudEvents type: `SG.Gov.NEA.AirQuality.PSIReading`

#### What it tells you

A current environmental measurement from Singapore's National Environment Agency (NEA). It carries weather observations, air-quality readings, and environmental indexes when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{region}`. `{region}` is region identifier (west/east/central/south/north). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `singapore-nea-airquality`, key `{region}` |
| `MQTT/5.0` | topic `air-quality/sg/nea/singapore-nea/{region}/{station_id}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/singapore-nea`, message subject `{region}`; application properties station_id `{station_id}`, event `{event}` |

#### Payload

`Psireading` payloads are JSON object. Required fields: `region`, `timestamp`, `update_timestamp`, `psi_twenty_four_hourly`.

- **`region`** (string, required): Region identifier (west/east/central/south/north).
- **`timestamp`** (datetime, required): Observation period start timestamp in ISO 8601 with timezone.
- **`update_timestamp`** (datetime, required): Timestamp when the NEA API last updated this reading.
- **`psi_twenty_four_hourly`** (integer or null, required): 24-hour PSI value. The overall Pollutant Standards Index for the region. Scale: 0-50 Good, 51-100 Moderate, 101-200 Unhealthy, 201-300 Very Unhealthy, above 300 Hazardous. Constraints: minimum `0`.
- **`o3_sub_index`** (integer or null, optional): Ozone (O3) sub-index component of PSI. Constraints: minimum `0`.
- **`pm10_sub_index`** (integer or null, optional): PM10 sub-index component of PSI. Constraints: minimum `0`.
- **`pm10_twenty_four_hourly`** (integer or null, optional, ug/m3 (µg/m³)): PM10 24-hour concentration used to calculate the PM10 PSI sub-index. Constraints: minimum `0`.
- **`pm25_sub_index`** (integer or null, optional): PM2.5 sub-index component of PSI. Constraints: minimum `0`.
- **`pm25_twenty_four_hourly`** (integer or null, optional, ug/m3 (µg/m³)): PM2.5 24-hour concentration. Constraints: minimum `0`.
- **`co_sub_index`** (integer or null, optional): Carbon monoxide (CO) sub-index component of PSI. Constraints: minimum `0`.
- **`co_eight_hour_max`** (integer or null, optional, mg/m3 (mg/m³)): CO 8-hour maximum concentration. Constraints: minimum `0`.
- **`so2_sub_index`** (integer or null, optional): Sulphur dioxide (SO2) sub-index component of PSI. Constraints: minimum `0`.
- **`so2_twenty_four_hourly`** (integer or null, optional, ug/m3 (µg/m³)): SO2 24-hour concentration. Constraints: minimum `0`.
- **`no2_one_hour_max`** (integer or null, optional, ug/m3 (µg/m³)): Nitrogen dioxide (NO2) 1-hour maximum concentration. Constraints: minimum `0`.
- **`o3_eight_hour_max`** (integer or null, optional, ug/m3 (µg/m³)): Ozone (O3) 8-hour maximum concentration. Constraints: minimum `0`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "region": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "update_timestamp": "2024-01-01T00:00:00Z",
  "psi_twenty_four_hourly": 0,
  "o3_sub_index": 0,
  "pm10_sub_index": 0,
  "pm10_twenty_four_hourly": 0,
  "pm25_sub_index": 0,
  "pm25_twenty_four_hourly": 0,
  "co_sub_index": 0,
  "co_eight_hour_max": 0,
  "so2_sub_index": 0,
  "so2_twenty_four_hourly": 0,
  "no2_one_hour_max": 0,
  "o3_eight_hour_max": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### PM25 Reading

CloudEvents type: `SG.Gov.NEA.AirQuality.PM25Reading`

#### What it tells you

A current environmental measurement from Singapore's National Environment Agency (NEA). It carries weather observations, air-quality readings, and environmental indexes when the upstream feed reports a new or refreshed value.

#### Identity

Each event identifies the real-world resource with `{region}`. `{region}` is region identifier (west/east/central/south/north). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `singapore-nea-airquality`, key `{region}` |
| `MQTT/5.0` | topic `air-quality/sg/nea/singapore-nea/{region}/{station_id}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/singapore-nea`, message subject `{region}`; application properties station_id `{station_id}`, event `{event}` |

#### Payload

`PM25 Reading` payloads are JSON object. Required fields: `region`, `timestamp`, `update_timestamp`, `pm25_one_hourly`.

- **`region`** (string, required): Region identifier (west/east/central/south/north).
- **`timestamp`** (datetime, required): Observation period start timestamp in ISO 8601 with timezone.
- **`update_timestamp`** (datetime, required): Timestamp when the NEA API last updated this reading.
- **`pm25_one_hourly`** (integer or null, required, ug/m3 (µg/m³)): PM2.5 1-hour concentration for the region. Constraints: minimum `0`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "region": "string",
  "timestamp": "2024-01-01T00:00:00Z",
  "update_timestamp": "2024-01-01T00:00:00Z",
  "pm25_one_hourly": 0
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

- xRegistry manifest: [`xreg/singapore_nea.xreg.json`](xreg/singapore_nea.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
