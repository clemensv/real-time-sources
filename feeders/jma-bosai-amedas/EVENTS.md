# JMA Bosai AMeDAS feeder Events

MQTT 5 variant of jma-bosai-amedas events with UNS topic routing.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 1 telemetry event type.
- **Identity:** `jp.jma.amedas/{station_code}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `jma-bosai-amedas`. The record key is `jp.jma.amedas/{station_code}`. In plain language, `jp.jma.amedas/{station_code}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['jma-bosai-amedas'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `weather/jp/jma/jma-bosai-amedas/+/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('weather/jp/jma/jma-bosai-amedas/+/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `jma-bosai-amedas`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/jma-bosai-amedas')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Station

CloudEvents type: `JP.JMA.Amedas.Station`

#### What it tells you

Reference event for one JMA AMeDAS station from the Bosai amedastable.json station table, including names, geodetic position, elevation, station capability tier, and measurement capability bitmask.

#### Identity

Each event identifies the real-world resource with `jp.jma.amedas/{station_code}`. `{station_code}` is JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-amedas`, key `jp.jma.amedas/{station_code}` |
| `MQTT/5.0` | topic `weather/jp/jma/jma-bosai-amedas/{prefecture}/{station_code}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-amedas`, message subject `jp.jma.amedas/{station_code}`; application properties prefecture `{prefecture}`, event `{event}` |

#### Payload

`Station` payloads are JSON object. Required fields: `station_code`, `kj_name`, `kana`, `en_name`, `latitude`, `longitude`, `altitude_m`, `station_type`, `elems_bitmask`, `enabled_measurements`, `prefecture`, `event`.

- **`station_code`** (string, required): JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. Constraints: pattern `^[0-9]{5}$`.
- **`kj_name`** (string, required): Japanese kanji station name from the JMA AMeDAS station table (kjName), used by the Bosai web application for Japanese display labels.
- **`kana`** (string, required): Japanese kana station reading from the JMA AMeDAS station table (knName in live payloads, kana in older examples), used by the Bosai web application for phonetic Japanese display.
- **`en_name`** (string, required): English station name from the JMA AMeDAS station table.
- **`latitude`** (double, required, degree (°)): Station latitude in WGS84 decimal degrees. The JMA station table publishes latitude as [degrees, minutes]; the bridge converts it with degrees + minutes/60. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, degree (°)): Station longitude in WGS84 decimal degrees. The JMA station table publishes longitude as [degrees, minutes]; the bridge converts it with degrees + minutes/60. Constraints: minimum `-180`, maximum `180`.
- **`altitude_m`** (double, required, meter): Station elevation above sea level in meters from the JMA station table alt field.
- **`station_type`** (enum, required): JMA AMeDAS station capability tier as published in the station table. The tier controls which measurements may be emitted for a station.
- **`elems_bitmask`** (string, required): JMA Bosai AMeDAS element bitmask string from the station table. Each non-zero character indicates that the corresponding station capability is enabled in the Bosai web application.
- **`enabled_measurements`** (array of string, required): Measurement capability names derived by the bridge from the JMA elems_bitmask. The values describe which observation families the station can emit, such as precipitation, wind, temperature, sunshine_duration, snow_depth, humidity, pressure, or visibility.
- **`prefecture`** (string, required): ASCII-safe Japanese prefecture or region slug used as a MQTT and AMQP routing axis. The bridge derives this from JMA station/volcano metadata when available, otherwise emits unknown. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`event`** (enum, required): Fixed topic event segment for Station messages.
##### `station_type` values

- `A`: JMA AMeDAS capability tier A station, typically a major station with pressure and broader meteorological observations.
- `B`: JMA AMeDAS capability tier B station.
- `C`: JMA AMeDAS capability tier C station, commonly an automated regional station with a smaller measurement set.
##### `event` values

- `info`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_code": "string",
  "kj_name": "string",
  "kana": "string",
  "en_name": "string",
  "latitude": 0,
  "longitude": 0,
  "altitude_m": 0,
  "station_type": "A",
  "elems_bitmask": "string",
  "enabled_measurements": [
    "string"
  ],
  "prefecture": "string",
  "event": "info"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Observation

CloudEvents type: `JP.JMA.Amedas.Observation`

#### What it tells you

Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability.

#### Identity

Each event identifies the real-world resource with `jp.jma.amedas/{station_code}`. `{station_code}` is JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `jma-bosai-amedas`, key `jp.jma.amedas/{station_code}` |
| `MQTT/5.0` | topic `weather/jp/jma/jma-bosai-amedas/{prefecture}/{station_code}/{event}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/jma-bosai-amedas`, message subject `jp.jma.amedas/{station_code}`; application properties prefecture `{prefecture}`, event `{event}` |

#### Payload

`Observation` payloads are JSON object. Required fields: `station_code`, `observed_at`, `observed_at_local`, `temp`, `temp_qc_flag`, `humidity`, `humidity_qc_flag`, `pressure`, `pressure_qc_flag`, `normal_pressure`, `normal_pressure_qc_flag`, `wind_speed`, `wind_speed_qc_flag`, `wind_direction`, `wind_direction_qc_flag`, `wind_gust`, `wind_gust_qc_flag`, `wind_gust_direction`, `wind_gust_time`, `max_temp`, `max_temp_time`, `min_temp`, `min_temp_time`, `precipitation10m`, `precipitation10m_qc_flag`, `precipitation1h`, `precipitation1h_qc_flag`, `precipitation3h`, `precipitation3h_qc_flag`, `precipitation24h`, `precipitation24h_qc_flag`, `sun10m`, `sun10m_qc_flag`, `sun1h`, `sun1h_qc_flag`, `snow`, `snow_qc_flag`, `snow1h`, `snow1h_qc_flag`, `snow6h`, `snow6h_qc_flag`, `snow12h`, `snow12h_qc_flag`, `snow24h`, `snow24h_qc_flag`, `visibility`, `visibility_qc_flag`, `cloud`, `cloud_qc_flag`, `weather`, `weather_qc_flag`, `prefecture`, `event`.

- **`station_code`** (string, required): JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map. Constraints: pattern `^[0-9]{5}$`.
- **`observed_at`** (datetime, required): Observation snapshot timestamp converted from JMA latest_time.txt to UTC and serialized as RFC3339. AMeDAS map snapshots are published every ten minutes.
- **`observed_at_local`** (datetime, required): Original JMA latest_time.txt timestamp in Japan Standard Time with +09:00 offset, serialized as RFC3339.
- **`temp`** (double or null, required, celsius): Air temperature observed automatically by AMeDAS, expressed in degrees Celsius. JMA documents temperature as air temperature displayed in 0.1 °C units.
- **`temp_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`humidity`** (double or null, required, percent): Relative humidity of the air observed automatically by AMeDAS, expressed as percent. JMA documents humidity as relative humidity displayed in 1 percent units. Constraints: minimum `0`, maximum `100`.
- **`humidity_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`pressure`** (double or null, required, hectopascal): Station pressure from JMA Bosai AMeDAS where available, expressed in hectopascals.
- **`pressure_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`normal_pressure`** (double or null, required, hectopascal): Sea-level adjusted pressure (normalPressure in the Bosai payload) where available, expressed in hectopascals.
- **`normal_pressure_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`wind_speed`** (double or null, required, meter_per_second): Wind speed averaged over the ten minutes before observation time, expressed in meters per second. JMA documents wind speed as the speed of the wind over the preceding ten minutes.
- **`wind_speed_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`wind_direction`** (double or null, required, degree): Wind direction from which the wind blows, converted by the bridge from JMA 16-direction codes to degrees clockwise from true north. Constraints: minimum `0`, exclusiveMaximum `360`.
- **`wind_direction_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`wind_gust`** (double or null, required, meter_per_second): Maximum instantaneous wind speed (gust) for the observation interval from the JMA Bosai per-station point payload, expressed in meters per second. The bridge enriches map observations with this value only for configured point-detail stations.
- **`wind_gust_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the gust tuple in the Bosai AMeDAS per-station point payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA non-normal quality states as represented by the Bosai web application.
- **`wind_gust_direction`** (double or null, required, degree): Direction from which the maximum instantaneous wind gust blew, converted by the bridge from JMA 16-direction codes in gustDirection to degrees clockwise from true north. The field is present only when point-detail enrichment is configured and JMA publishes a gust direction. Constraints: minimum `0`, exclusiveMaximum `360`.
- **`wind_gust_time`** (datetime or null, required): UTC RFC3339 timestamp for the maximum instantaneous wind gust time from the JMA Bosai per-station gustTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.
- **`max_temp`** (double or null, required, celsius): Maximum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations.
- **`max_temp_time`** (datetime or null, required): UTC RFC3339 timestamp for the maximum air temperature time from the JMA Bosai per-station maxTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.
- **`min_temp`** (double or null, required, celsius): Minimum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations.
- **`min_temp_time`** (datetime or null, required): UTC RFC3339 timestamp for the minimum air temperature time from the JMA Bosai per-station minTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.
- **`precipitation10m`** (double or null, required, millimeter): Precipitation amount for the previous 10 minutes, expressed in millimeters of liquid water equivalent. JMA documents precipitation as rain or snow amount melted to water and displayed in 0.5 mm units.
- **`precipitation10m_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`precipitation1h`** (double or null, required, millimeter): Precipitation amount for the previous 1 hour, expressed in millimeters of liquid water equivalent.
- **`precipitation1h_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`precipitation3h`** (double or null, required, millimeter): Precipitation amount for the previous 3 hours, expressed in millimeters of liquid water equivalent.
- **`precipitation3h_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`precipitation24h`** (double or null, required, millimeter): Precipitation amount for the previous 24 hours, expressed in millimeters of liquid water equivalent.
- **`precipitation24h_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`sun10m`** (double or null, required, minute): Sunshine duration for the previous 10 minutes, expressed in minutes. JMA publishes this ten-minute map field in minutes, so its unit intentionally differs from the hourly sun1h field.
- **`sun10m_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`sun1h`** (double or null, required, hour): Sunshine duration for the previous 1 hour, expressed in hours as published by the Bosai AMeDAS map. JMA publishes this hourly field in hours, so its unit intentionally differs from the ten-minute sun10m field.
- **`sun1h_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`snow`** (double or null, required, centimeter): Snow depth, the height of snow on the ground, expressed in centimeters. JMA documents snow depth as the height from the ground surface to the top of accumulated snow.
- **`snow_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`snow1h`** (double or null, required, centimeter): Change in snow depth over the previous 1 hour, expressed in centimeters.
- **`snow1h_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`snow6h`** (double or null, required, centimeter): Change in snow depth over the previous 6 hours, expressed in centimeters.
- **`snow6h_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`snow12h`** (double or null, required, centimeter): Change in snow depth over the previous 12 hours, expressed in centimeters.
- **`snow12h_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`snow24h`** (double or null, required, centimeter): Change in snow depth over the previous 24 hours, expressed in centimeters.
- **`snow24h_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`visibility`** (double or null, required, meter): Horizontal visibility where published by JMA Bosai AMeDAS, expressed in meters.
- **`visibility_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`cloud`** (double or null, required): Cloud amount code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish cloud information.
- **`cloud_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`weather`** (double or null, required): Present weather code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish weather information.
- **`weather_qc_flag`** (int32 or null, required): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
- **`prefecture`** (string, required): ASCII-safe Japanese prefecture or region slug used as a MQTT and AMQP routing axis. The bridge derives this from JMA station/volcano metadata when available, otherwise emits unknown. Constraints: pattern `^[a-z0-9][a-z0-9-]*$`.
- **`event`** (enum, required): Fixed topic event segment for Observation messages.
##### `event` values

- `observation`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_code": "string",
  "observed_at": "2024-01-01T00:00:00Z",
  "observed_at_local": "2024-01-01T00:00:00Z",
  "temp": 0,
  "temp_qc_flag": 0,
  "humidity": 0,
  "humidity_qc_flag": 0,
  "pressure": 0,
  "pressure_qc_flag": 0,
  "normal_pressure": 0,
  "normal_pressure_qc_flag": 0,
  "wind_speed": 0,
  "wind_speed_qc_flag": 0,
  "wind_direction": 0,
  "wind_direction_qc_flag": 0,
  "wind_gust": 0,
  "wind_gust_qc_flag": 0,
  "wind_gust_direction": 0,
  "wind_gust_time": "2024-01-01T00:00:00Z",
  "max_temp": 0,
  "max_temp_time": "2024-01-01T00:00:00Z",
  "min_temp": 0,
  "min_temp_time": "2024-01-01T00:00:00Z",
  "precipitation10m": 0,
  "precipitation10m_qc_flag": 0,
  "precipitation1h": 0,
  "precipitation1h_qc_flag": 0,
  "precipitation3h": 0,
  "precipitation3h_qc_flag": 0,
  "precipitation24h": 0,
  "precipitation24h_qc_flag": 0,
  "sun10m": 0,
  "sun10m_qc_flag": 0,
  "sun1h": 0,
  "sun1h_qc_flag": 0,
  "snow": 0,
  "snow_qc_flag": 0,
  "snow1h": 0,
  "snow1h_qc_flag": 0,
  "snow6h": 0,
  "snow6h_qc_flag": 0,
  "snow12h": 0,
  "snow12h_qc_flag": 0,
  "snow24h": 0,
  "snow24h_qc_flag": 0,
  "visibility": 0,
  "visibility_qc_flag": 0,
  "cloud": 0,
  "cloud_qc_flag": 0,
  "weather": 0,
  "weather_qc_flag": 0,
  "prefecture": "string",
  "event": "observation"
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

- xRegistry manifest: [`xreg/jma-bosai-amedas.xreg.json`](xreg/jma-bosai-amedas.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
