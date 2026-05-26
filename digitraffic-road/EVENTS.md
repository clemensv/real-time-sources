# Digitraffic Road — Finnish Road Traffic Data Events

Digitraffic Road publishes road traffic measurements and status updates from Fintraffic Digitraffic for Finnish road network sensors and traffic messages. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 10 documented event types (30 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 2 reference/catalog event types and 8 telemetry event types.
- **Identity:** `{station_id}/{sensor_id}`, `{situation_id}`, `{domain}`, `{station_id}`, `{task_id}` identifies the resource each event is about.
- **Operations:** Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `digitraffic-road-sensors`, `digitraffic-road-messages`, `digitraffic-road-maintenance`. The record key is `{station_id}/{sensor_id}`, `{situation_id}`, `{domain}`, `{station_id}`, `{task_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['digitraffic-road-sensors', 'digitraffic-road-messages', 'digitraffic-road-maintenance'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/fi/fintraffic/digitraffic-road/+/+/tms-sensor-data`, `traffic/fi/fintraffic/digitraffic-road/+/+/weather-sensor-data`, `traffic/fi/fintraffic/digitraffic-road/messages/+/traffic-announcement`, `traffic/fi/fintraffic/digitraffic-road/messages/+/road-work`, `traffic/fi/fintraffic/digitraffic-road/messages/+/weight-restriction`, `traffic/fi/fintraffic/digitraffic-road/messages/+/exempted-transport`, `traffic/fi/fintraffic/digitraffic-road/maintenance/+/tracking`, `traffic/fi/fintraffic/digitraffic-road/stations/+/tms-station`, `traffic/fi/fintraffic/digitraffic-road/stations/+/weather-station`, `traffic/fi/fintraffic/digitraffic-road/maintenance-tasks/+/task-type`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/fi/fintraffic/digitraffic-road/+/+/tms-sensor-data', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `digitraffic-road`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/digitraffic-road')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Tms Sensor Data

CloudEvents type: `fi.digitraffic.road.sensors.TmsSensorData`

#### What it tells you

A transport update from Fintraffic Digitraffic. It carries road traffic measurements and status updates for Finnish road network sensors and traffic messages.

#### Identity

Each event identifies the real-world resource with `{station_id}/{sensor_id}`. `{station_id}` is TMS station numeric identifier as assigned by Fintraffic; `{sensor_id}` is computational sensor identifier within the TMS station. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-sensors`, key `{station_id}/{sensor_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/{station_id}/{sensor_id}/tms-sensor-data`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{station_id}/{sensor_id}`; application properties station_id `{station_id}`, sensor_id `{sensor_id}` |

#### Payload

`Tms Sensor Data` payloads are JSON object. Required fields: `station_id`, `sensor_id`, `value`, `time`.

- **`station_id`** (int32, required): TMS station numeric identifier as assigned by Fintraffic. Each station is located at a fixed point on the Finnish road network and identified by a unique integer (e.g. 23001). Station metadata including road address, municipality, and free-flow speeds is available from the /api/tms/v1/stations REST endpoint.
- **`sensor_id`** (int32, required): Computational sensor identifier within the TMS station. Each sensor measures a specific traffic parameter in a given direction and time window. Common sensor families include OHITUKSET (vehicle passings, unit kpl/h), KESKINOPEUS (average speed, unit km/h), and LIUKUVA_NOPEUS (rolling speed per lane, unit km/h). Sensor metadata is available from /api/tms/v1/sensors.
- **`value`** (double, required): Measured value in the sensor's native unit. Units vary by sensor family: kpl/h (vehicles per hour) for OHITUKSET passings sensors, km/h for KESKINOPEUS and LIUKUVA_NOPEUS speed sensors, and dimensionless percentage ratios for traffic situation indicators (VVAPAAS, MS suffixed sensors).
- **`time`** (int32, required): Measurement timestamp as Unix epoch seconds (UTC). Indicates when the sensor reading was taken or the aggregation period was last updated.
- **`start`** (int32 or null, optional): Start of the fixed time window as Unix epoch seconds (UTC). Present for fixed-window aggregate sensors such as OHITUKSET_5MIN_KIINTEA (5-minute fixed passings), KESKINOPEUS_60MIN_KIINTEA (60-minute fixed average speed), and OHITUKSET_60MIN_KIINTEA. Null or absent for rolling-window sensors (LIUKUVA suffix) and per-lane sensors.
- **`end`** (int32 or null, optional): End of the fixed time window as Unix epoch seconds (UTC). Present for fixed-window aggregate sensors. Null or absent for rolling-window and per-lane sensors.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "sensor_id": 0,
  "value": 0,
  "time": 0,
  "start": 0,
  "end": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Weather Sensor Data

CloudEvents type: `fi.digitraffic.road.sensors.WeatherSensorData`

#### What it tells you

A transport update from Fintraffic Digitraffic. It carries road traffic measurements and status updates for Finnish road network sensors and traffic messages.

#### Identity

Each event identifies the real-world resource with `{station_id}/{sensor_id}`. `{station_id}` is road weather station numeric identifier as assigned by Fintraffic (e.g. 1012); `{sensor_id}` is sensor identifier within the road weather station. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-sensors`, key `{station_id}/{sensor_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/{station_id}/{sensor_id}/weather-sensor-data`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{station_id}/{sensor_id}`; application properties station_id `{station_id}`, sensor_id `{sensor_id}` |

#### Payload

`Weather Sensor Data` payloads are JSON object. Required fields: `station_id`, `sensor_id`, `value`, `time`.

- **`station_id`** (int32, required): Road weather station numeric identifier as assigned by Fintraffic (e.g. 1012). Station metadata including road address, municipality, and available sensors is available from the /api/weather/v1/stations REST endpoint.
- **`sensor_id`** (int32, required): Sensor identifier within the road weather station. Each sensor measures a specific weather or road surface parameter. Common sensors: ILMA (id 1, air temperature °C), ILMA_DERIVAATTA (id 2, air temp derivative °C/h), TIE_1 (id 3, road surface temp °C), MAA_1 (id 7, ground temp °C), KASTEPISTE (id 9, dew point °C), JÄÄTYMISPISTE_1 (id 10, freezing point °C), KESKITUULI (id 16, avg wind m/s), MAKSIMITUULI (id 17, max wind m/s), ILMAN_KOSTEUS (id 19, relative humidity %). Full sensor list at /api/weather/v1/sensors.
- **`value`** (double, required): Measured value in the sensor's native unit. Units vary by sensor: °C for temperatures and dew/freezing points, °C/h for temperature derivatives, m/s for wind speed, % for relative humidity, mm for precipitation amounts.
- **`time`** (int32, required): Measurement timestamp as Unix epoch seconds (UTC). Indicates when the sensor reading was taken.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "sensor_id": 0,
  "value": 0,
  "time": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Traffic Announcement

CloudEvents type: `fi.digitraffic.road.messages.TrafficAnnouncement`

#### What it tells you

A current transport measurement or status update from Fintraffic Digitraffic. It carries road traffic measurements and status updates when the upstream feed reports a new or refreshed value. A transport update from Fintraffic Digitraffic.

#### Identity

Each event identifies the real-world resource with `{situation_id}`. `{situation_id}` is unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-messages`, key `{situation_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/traffic-announcement`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{situation_id}` |

#### Payload

`Traffic Announcement` payloads are JSON object. Required fields: `situation_id`, `situation_type`, `version`, `release_time`, `version_time`.

- **`situation_id`** (string, required): Unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). Stable across all version updates for a given situation.
- **`situation_type`** (string, required): Situation category as defined by Fintraffic. Values: 'traffic announcement' (incidents, lane closures, ramp closures), 'road work' (planned and active road works with phases), 'weight restriction' (load-bearing limits on roads or bridges), 'exempted transport' (oversize or heavy transports requiring advance notice). Mapped from the MQTT topic situationType segment.
- **`traffic_announcement_type`** (string or null, optional): Sub-classification for traffic announcements. Values include 'preliminary accident report', 'accident report', 'general', 'unconfirmed observation', and others. Present only when situation_type is 'traffic announcement'; null otherwise.
- **`version`** (int32, required): Monotonically increasing version counter for this situation. Starts at 1 and increments with each update to the situation's announcements, timing, or status.
- **`release_time`** (string, required): ISO 8601 UTC timestamp when the first version of this situation was released (e.g. '2025-10-22T06:39:54.787Z').
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this version of the situation was published (e.g. '2025-10-22T07:09:57.237Z').
- **`title`** (string or null, optional): Human-readable title from the first announcement, typically identifying the road, municipality, and situation type in Finnish (e.g. 'Tie 4, eli Ivalontie, Sodankylä. Ensitiedote liikenneonnettomuudesta.').
- **`language`** (string or null, optional): ISO 639-1 language code for the announcement text. Typically 'fi' (Finnish).
- **`sender`** (string or null, optional): Traffic management center that issued the announcement (e.g. 'Fintraffic Tieliikennekeskus Tampere', 'Fintraffic Tieliikennekeskus Helsinki').
- **`location_description`** (string or null, optional): Human-readable location description from the first announcement's location object, typically including road number, section, and municipality in Finnish.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp for the start of the situation's time-and-duration window from the first announcement. Null if no time window is specified.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp for the expected end of the situation. Null if the end time is unknown or the situation is open-ended.
- **`features_json`** (string or null, optional): JSON-serialized array of feature objects from the first announcement. Features describe traffic impacts such as lane closures, detours, or speed reductions. Null if no features are listed.
- **`road_work_phases_json`** (string or null, optional): JSON-serialized array of road work phase objects from the first announcement. Each phase includes work types, restrictions (speed limits, lane narrowing), severity, and independent time windows. Present only for 'road work' situations; null otherwise.
- **`comment`** (string or null, optional): Free-text comment from the first announcement, providing additional context such as detour instructions or situation details.
- **`additional_information`** (string or null, optional): Supplementary information text from the first announcement, often including a link to the Fintraffic traffic situation portal.
- **`contact_phone`** (string or null, optional): Contact telephone number for the issuing traffic management center (e.g. '02002100').
- **`contact_email`** (string or null, optional): Contact email address for the issuing traffic management center.
- **`announcements_json`** (string or null, optional): JSON-serialized array of all announcement objects in the situation, preserving the full upstream structure including nested location details, road addresses, ALERT-C codes, road work phases, restrictions, and work types. Provided for consumers needing the complete upstream detail beyond the flattened first-announcement fields.
- **`geometry_type`** (string or null, optional): GeoJSON geometry type of the situation's spatial extent (e.g. 'Point', 'LineString', 'MultiLineString'). Null if no geometry is available.
- **`geometry_coordinates_json`** (string or null, optional): JSON-serialized GeoJSON coordinates array for the situation's spatial extent. Coordinates are in [longitude, latitude] order per the GeoJSON specification (WGS84). Null if no geometry is available.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_id": "string",
  "situation_type": "string",
  "traffic_announcement_type": "string",
  "version": 0,
  "release_time": "string",
  "version_time": "string",
  "title": "string",
  "language": "string",
  "sender": "string",
  "location_description": "string",
  "start_time": "string",
  "end_time": "string",
  "features_json": "string",
  "road_work_phases_json": "string",
  "comment": "string",
  "additional_information": "string",
  "contact_phone": "string",
  "contact_email": "string",
  "announcements_json": "string",
  "geometry_type": "string",
  "geometry_coordinates_json": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Road Work

CloudEvents type: `fi.digitraffic.road.messages.RoadWork`

#### What it tells you

A transport update from Fintraffic Digitraffic. It carries road traffic measurements and status updates for Finnish road network sensors and traffic messages.

#### Identity

Each event identifies the real-world resource with `{situation_id}`. `{situation_id}` is unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-messages`, key `{situation_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/road-work`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{situation_id}` |

#### Payload

`Road Work` payloads are JSON object. Required fields: `situation_id`, `situation_type`, `version`, `release_time`, `version_time`.

- **`situation_id`** (string, required): Unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). Stable across all version updates for a given situation.
- **`situation_type`** (string, required): Situation category as defined by Fintraffic. Values: 'traffic announcement' (incidents, lane closures, ramp closures), 'road work' (planned and active road works with phases), 'weight restriction' (load-bearing limits on roads or bridges), 'exempted transport' (oversize or heavy transports requiring advance notice). Mapped from the MQTT topic situationType segment.
- **`traffic_announcement_type`** (string or null, optional): Sub-classification for traffic announcements. Values include 'preliminary accident report', 'accident report', 'general', 'unconfirmed observation', and others. Present only when situation_type is 'traffic announcement'; null otherwise.
- **`version`** (int32, required): Monotonically increasing version counter for this situation. Starts at 1 and increments with each update to the situation's announcements, timing, or status.
- **`release_time`** (string, required): ISO 8601 UTC timestamp when the first version of this situation was released (e.g. '2025-10-22T06:39:54.787Z').
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this version of the situation was published (e.g. '2025-10-22T07:09:57.237Z').
- **`title`** (string or null, optional): Human-readable title from the first announcement, typically identifying the road, municipality, and situation type in Finnish (e.g. 'Tie 4, eli Ivalontie, Sodankylä. Ensitiedote liikenneonnettomuudesta.').
- **`language`** (string or null, optional): ISO 639-1 language code for the announcement text. Typically 'fi' (Finnish).
- **`sender`** (string or null, optional): Traffic management center that issued the announcement (e.g. 'Fintraffic Tieliikennekeskus Tampere', 'Fintraffic Tieliikennekeskus Helsinki').
- **`location_description`** (string or null, optional): Human-readable location description from the first announcement's location object, typically including road number, section, and municipality in Finnish.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp for the start of the situation's time-and-duration window from the first announcement. Null if no time window is specified.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp for the expected end of the situation. Null if the end time is unknown or the situation is open-ended.
- **`features_json`** (string or null, optional): JSON-serialized array of feature objects from the first announcement. Features describe traffic impacts such as lane closures, detours, or speed reductions. Null if no features are listed.
- **`road_work_phases_json`** (string or null, optional): JSON-serialized array of road work phase objects from the first announcement. Each phase includes work types, restrictions (speed limits, lane narrowing), severity, and independent time windows. Present only for 'road work' situations; null otherwise.
- **`comment`** (string or null, optional): Free-text comment from the first announcement, providing additional context such as detour instructions or situation details.
- **`additional_information`** (string or null, optional): Supplementary information text from the first announcement, often including a link to the Fintraffic traffic situation portal.
- **`contact_phone`** (string or null, optional): Contact telephone number for the issuing traffic management center (e.g. '02002100').
- **`contact_email`** (string or null, optional): Contact email address for the issuing traffic management center.
- **`announcements_json`** (string or null, optional): JSON-serialized array of all announcement objects in the situation, preserving the full upstream structure including nested location details, road addresses, ALERT-C codes, road work phases, restrictions, and work types. Provided for consumers needing the complete upstream detail beyond the flattened first-announcement fields.
- **`geometry_type`** (string or null, optional): GeoJSON geometry type of the situation's spatial extent (e.g. 'Point', 'LineString', 'MultiLineString'). Null if no geometry is available.
- **`geometry_coordinates_json`** (string or null, optional): JSON-serialized GeoJSON coordinates array for the situation's spatial extent. Coordinates are in [longitude, latitude] order per the GeoJSON specification (WGS84). Null if no geometry is available.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_id": "string",
  "situation_type": "string",
  "traffic_announcement_type": "string",
  "version": 0,
  "release_time": "string",
  "version_time": "string",
  "title": "string",
  "language": "string",
  "sender": "string",
  "location_description": "string",
  "start_time": "string",
  "end_time": "string",
  "features_json": "string",
  "road_work_phases_json": "string",
  "comment": "string",
  "additional_information": "string",
  "contact_phone": "string",
  "contact_email": "string",
  "announcements_json": "string",
  "geometry_type": "string",
  "geometry_coordinates_json": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Weight Restriction

CloudEvents type: `fi.digitraffic.road.messages.WeightRestriction`

#### What it tells you

A transport update from Fintraffic Digitraffic. It carries road traffic measurements and status updates for Finnish road network sensors and traffic messages.

#### Identity

Each event identifies the real-world resource with `{situation_id}`. `{situation_id}` is unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-messages`, key `{situation_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/weight-restriction`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{situation_id}` |

#### Payload

`Weight Restriction` payloads are JSON object. Required fields: `situation_id`, `situation_type`, `version`, `release_time`, `version_time`.

- **`situation_id`** (string, required): Unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). Stable across all version updates for a given situation.
- **`situation_type`** (string, required): Situation category as defined by Fintraffic. Values: 'traffic announcement' (incidents, lane closures, ramp closures), 'road work' (planned and active road works with phases), 'weight restriction' (load-bearing limits on roads or bridges), 'exempted transport' (oversize or heavy transports requiring advance notice). Mapped from the MQTT topic situationType segment.
- **`traffic_announcement_type`** (string or null, optional): Sub-classification for traffic announcements. Values include 'preliminary accident report', 'accident report', 'general', 'unconfirmed observation', and others. Present only when situation_type is 'traffic announcement'; null otherwise.
- **`version`** (int32, required): Monotonically increasing version counter for this situation. Starts at 1 and increments with each update to the situation's announcements, timing, or status.
- **`release_time`** (string, required): ISO 8601 UTC timestamp when the first version of this situation was released (e.g. '2025-10-22T06:39:54.787Z').
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this version of the situation was published (e.g. '2025-10-22T07:09:57.237Z').
- **`title`** (string or null, optional): Human-readable title from the first announcement, typically identifying the road, municipality, and situation type in Finnish (e.g. 'Tie 4, eli Ivalontie, Sodankylä. Ensitiedote liikenneonnettomuudesta.').
- **`language`** (string or null, optional): ISO 639-1 language code for the announcement text. Typically 'fi' (Finnish).
- **`sender`** (string or null, optional): Traffic management center that issued the announcement (e.g. 'Fintraffic Tieliikennekeskus Tampere', 'Fintraffic Tieliikennekeskus Helsinki').
- **`location_description`** (string or null, optional): Human-readable location description from the first announcement's location object, typically including road number, section, and municipality in Finnish.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp for the start of the situation's time-and-duration window from the first announcement. Null if no time window is specified.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp for the expected end of the situation. Null if the end time is unknown or the situation is open-ended.
- **`features_json`** (string or null, optional): JSON-serialized array of feature objects from the first announcement. Features describe traffic impacts such as lane closures, detours, or speed reductions. Null if no features are listed.
- **`road_work_phases_json`** (string or null, optional): JSON-serialized array of road work phase objects from the first announcement. Each phase includes work types, restrictions (speed limits, lane narrowing), severity, and independent time windows. Present only for 'road work' situations; null otherwise.
- **`comment`** (string or null, optional): Free-text comment from the first announcement, providing additional context such as detour instructions or situation details.
- **`additional_information`** (string or null, optional): Supplementary information text from the first announcement, often including a link to the Fintraffic traffic situation portal.
- **`contact_phone`** (string or null, optional): Contact telephone number for the issuing traffic management center (e.g. '02002100').
- **`contact_email`** (string or null, optional): Contact email address for the issuing traffic management center.
- **`announcements_json`** (string or null, optional): JSON-serialized array of all announcement objects in the situation, preserving the full upstream structure including nested location details, road addresses, ALERT-C codes, road work phases, restrictions, and work types. Provided for consumers needing the complete upstream detail beyond the flattened first-announcement fields.
- **`geometry_type`** (string or null, optional): GeoJSON geometry type of the situation's spatial extent (e.g. 'Point', 'LineString', 'MultiLineString'). Null if no geometry is available.
- **`geometry_coordinates_json`** (string or null, optional): JSON-serialized GeoJSON coordinates array for the situation's spatial extent. Coordinates are in [longitude, latitude] order per the GeoJSON specification (WGS84). Null if no geometry is available.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_id": "string",
  "situation_type": "string",
  "traffic_announcement_type": "string",
  "version": 0,
  "release_time": "string",
  "version_time": "string",
  "title": "string",
  "language": "string",
  "sender": "string",
  "location_description": "string",
  "start_time": "string",
  "end_time": "string",
  "features_json": "string",
  "road_work_phases_json": "string",
  "comment": "string",
  "additional_information": "string",
  "contact_phone": "string",
  "contact_email": "string",
  "announcements_json": "string",
  "geometry_type": "string",
  "geometry_coordinates_json": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Exempted Transport

CloudEvents type: `fi.digitraffic.road.messages.ExemptedTransport`

#### What it tells you

A transport update from Fintraffic Digitraffic. It carries road traffic measurements and status updates for Finnish road network sensors and traffic messages.

#### Identity

Each event identifies the real-world resource with `{situation_id}`. `{situation_id}` is unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-messages`, key `{situation_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/messages/{situation_id}/exempted-transport`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{situation_id}` |

#### Payload

`Exempted Transport` payloads are JSON object. Required fields: `situation_id`, `situation_type`, `version`, `release_time`, `version_time`.

- **`situation_id`** (string, required): Unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). Stable across all version updates for a given situation.
- **`situation_type`** (string, required): Situation category as defined by Fintraffic. Values: 'traffic announcement' (incidents, lane closures, ramp closures), 'road work' (planned and active road works with phases), 'weight restriction' (load-bearing limits on roads or bridges), 'exempted transport' (oversize or heavy transports requiring advance notice). Mapped from the MQTT topic situationType segment.
- **`traffic_announcement_type`** (string or null, optional): Sub-classification for traffic announcements. Values include 'preliminary accident report', 'accident report', 'general', 'unconfirmed observation', and others. Present only when situation_type is 'traffic announcement'; null otherwise.
- **`version`** (int32, required): Monotonically increasing version counter for this situation. Starts at 1 and increments with each update to the situation's announcements, timing, or status.
- **`release_time`** (string, required): ISO 8601 UTC timestamp when the first version of this situation was released (e.g. '2025-10-22T06:39:54.787Z').
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this version of the situation was published (e.g. '2025-10-22T07:09:57.237Z').
- **`title`** (string or null, optional): Human-readable title from the first announcement, typically identifying the road, municipality, and situation type in Finnish (e.g. 'Tie 4, eli Ivalontie, Sodankylä. Ensitiedote liikenneonnettomuudesta.').
- **`language`** (string or null, optional): ISO 639-1 language code for the announcement text. Typically 'fi' (Finnish).
- **`sender`** (string or null, optional): Traffic management center that issued the announcement (e.g. 'Fintraffic Tieliikennekeskus Tampere', 'Fintraffic Tieliikennekeskus Helsinki').
- **`location_description`** (string or null, optional): Human-readable location description from the first announcement's location object, typically including road number, section, and municipality in Finnish.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp for the start of the situation's time-and-duration window from the first announcement. Null if no time window is specified.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp for the expected end of the situation. Null if the end time is unknown or the situation is open-ended.
- **`features_json`** (string or null, optional): JSON-serialized array of feature objects from the first announcement. Features describe traffic impacts such as lane closures, detours, or speed reductions. Null if no features are listed.
- **`road_work_phases_json`** (string or null, optional): JSON-serialized array of road work phase objects from the first announcement. Each phase includes work types, restrictions (speed limits, lane narrowing), severity, and independent time windows. Present only for 'road work' situations; null otherwise.
- **`comment`** (string or null, optional): Free-text comment from the first announcement, providing additional context such as detour instructions or situation details.
- **`additional_information`** (string or null, optional): Supplementary information text from the first announcement, often including a link to the Fintraffic traffic situation portal.
- **`contact_phone`** (string or null, optional): Contact telephone number for the issuing traffic management center (e.g. '02002100').
- **`contact_email`** (string or null, optional): Contact email address for the issuing traffic management center.
- **`announcements_json`** (string or null, optional): JSON-serialized array of all announcement objects in the situation, preserving the full upstream structure including nested location details, road addresses, ALERT-C codes, road work phases, restrictions, and work types. Provided for consumers needing the complete upstream detail beyond the flattened first-announcement fields.
- **`geometry_type`** (string or null, optional): GeoJSON geometry type of the situation's spatial extent (e.g. 'Point', 'LineString', 'MultiLineString'). Null if no geometry is available.
- **`geometry_coordinates_json`** (string or null, optional): JSON-serialized GeoJSON coordinates array for the situation's spatial extent. Coordinates are in [longitude, latitude] order per the GeoJSON specification (WGS84). Null if no geometry is available.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_id": "string",
  "situation_type": "string",
  "traffic_announcement_type": "string",
  "version": 0,
  "release_time": "string",
  "version_time": "string",
  "title": "string",
  "language": "string",
  "sender": "string",
  "location_description": "string",
  "start_time": "string",
  "end_time": "string",
  "features_json": "string",
  "road_work_phases_json": "string",
  "comment": "string",
  "additional_information": "string",
  "contact_phone": "string",
  "contact_email": "string",
  "announcements_json": "string",
  "geometry_type": "string",
  "geometry_coordinates_json": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Maintenance Tracking

CloudEvents type: `fi.digitraffic.road.maintenance.MaintenanceTracking`

#### What it tells you

A transport update from Fintraffic Digitraffic. It carries road traffic measurements and status updates for Finnish road network sensors and traffic messages.

#### Identity

Each event identifies the real-world resource with `{domain}`. `{domain}` is data domain identifying the source system. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-maintenance`, key `{domain}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/maintenance/{domain}/tracking`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{domain}`; application properties domain `{domain}` |

#### Payload

`Maintenance Tracking` payloads are JSON object. Required fields: `domain`, `time`, `tasks`, `x`, `y`.

- **`domain`** (string, required): Data domain identifying the source system. Primary domain is 'state-roads' for data from the Finnish Transport Infrastructure Agency's Harja system. Other domains include municipal systems such as 'autori-kuopio', 'autori-oulu', and 'paikannin-kuopio'. The domain value comes from the MQTT topic path.
- **`time`** (int32, required): Tracking timestamp as Unix epoch seconds (UTC). Indicates when the position and task were recorded by the vehicle.
- **`source`** (string or null, optional): Name of the source system that produced the tracking data (e.g. 'Harja/Väylävirasto' for the state road maintenance system). May be null if the source system is not identified.
- **`tasks`** (array of string, required): Array of maintenance task type identifiers being performed by the vehicle at this position. Task types follow the Fintraffic taxonomy, e.g. 'BRUSHING', 'SALTING', 'PLOUGHING_AND_SLUSH_REMOVAL', 'LEVELLING_GRAVEL_ROAD_SURFACE'. Full task type list with Finnish, English, and Swedish names is available at /api/maintenance/v1/tracking/tasks.
- **`x`** (double, required): Longitude of the vehicle position in WGS84 (EPSG:4326) decimal degrees.
- **`y`** (double, required): Latitude of the vehicle position in WGS84 (EPSG:4326) decimal degrees.
- **`direction`** (double or null, optional): Vehicle heading in degrees (0-360, clockwise from north). May be null or absent if heading information is not available from the tracking device.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "domain": "string",
  "time": 0,
  "source": "string",
  "tasks": [
    "string"
  ],
  "x": 0,
  "y": 0,
  "direction": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Tms Station

CloudEvents type: `fi.digitraffic.road.stations.TmsStation`

#### What it tells you

A reference record from Fintraffic Digitraffic for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is TMS station numeric identifier as assigned by Fintraffic (e.g. 23001). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-sensors`, key `{station_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/stations/{station_id}/tms-station`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{station_id}`; application properties station_id `{station_id}` |

#### Payload

`Tms Station` payloads are JSON object. Required fields: `station_id`, `name`, `longitude`, `latitude`, `municipality`, `municipality_code`, `province`, `province_code`, `road_number`, `road_section`, `station_type`, `collection_status`, `start_time`, `sensors`.

- **`station_id`** (int32, required): TMS station numeric identifier as assigned by Fintraffic (e.g. 23001). Unique across all TMS stations in the Finnish road network. Corresponds to the station_id in TmsSensorData telemetry events.
- **`name`** (string, required): Internal station name used by Fintraffic, typically encoding road and location (e.g. "vt7_Rita"). Not intended for display; use names_fi/sv/en for human-readable names.
- **`tms_number`** (int32 or null, optional): Legacy TMS numbering used in older Fintraffic systems. May differ from station_id. Null if not assigned.
- **`names_fi`** (string, optional): Finnish display name for the station, typically including road number, municipality, and local area (e.g. "Tie 7 Porvoo, Rita").
- **`names_sv`** (string or null, optional): Swedish display name for the station (e.g. "Väg 7 Borgå, Rita"). Null if no Swedish translation is available.
- **`names_en`** (string or null, optional): English display name for the station (e.g. "Road 7 Porvoo, Rita"). Null if no English translation is available.
- **`longitude`** (double, required): Station longitude in WGS84 (EPSG:4326) decimal degrees.
- **`latitude`** (double, required): Station latitude in WGS84 (EPSG:4326) decimal degrees.
- **`altitude`** (double or null, optional): Station altitude in meters above sea level. Null or 0.0 if altitude data is not available.
- **`municipality`** (string, required): Name of the Finnish municipality where the station is located (e.g. "Porvoo", "Espoo").
- **`municipality_code`** (int32, required): Finnish municipality code as defined by Statistics Finland (e.g. 638 for Porvoo, 49 for Espoo).
- **`province`** (string, required): Name of the Finnish province (maakunta) where the station is located (e.g. "Uusimaa", "Pirkanmaa").
- **`province_code`** (int32, required): Finnish province code as defined by Statistics Finland (e.g. 1 for Uusimaa).
- **`road_number`** (int32, required): Finnish road number where the station is installed (e.g. 7 for Highway 7 / E18).
- **`road_section`** (int32, required): Road section number within the road, part of the Finnish road addressing system.
- **`distance_from_section_start`** (int32, optional): Distance from the start of the road section in meters, part of the Finnish road addressing system.
- **`carriageway`** (string or null, optional): Carriageway type at the station location. Values from the Digitraffic API include "DUAL_CARRIAGEWAY_RIGHT_IN_INCREASING_DIRECTION", "DUAL_CARRIAGEWAY_LEFT_IN_INCREASING_DIRECTION", "ONE_CARRIAGEWAY". Null if not specified.
- **`side`** (string or null, optional): Side of the road where the station is located. Values: "LEFT", "RIGHT", "BETWEEN", "UNKNOWN". Null if not specified.
- **`station_type`** (string, required): TMS station type code indicating the hardware configuration (e.g. "DSL_6" for a 6-loop DSL station). Determines which sensor families are available.
- **`collection_status`** (string, required): Current data collection status of the station. Values: "GATHERING" (actively collecting), "REMOVED_TEMPORARILY", "REMOVED_PERMANENTLY". Only stations with GATHERING status produce telemetry.
- **`state`** (string or null, optional): Operational state of the station hardware. Values include "OK", "FAULT", "DISABLED". Null if state information is not available.
- **`free_flow_speed_1`** (double or null, optional): Reference free-flow speed for traffic direction 1 in km/h. Used to calculate traffic fluency ratios for VVAPAAS-suffixed sensors. Null if not calibrated.
- **`free_flow_speed_2`** (double or null, optional): Reference free-flow speed for traffic direction 2 in km/h. Used to calculate traffic fluency ratios. Null if not calibrated or station is on a one-way road.
- **`bearing`** (int32 or null, optional): Bearing of the road at the station in degrees (0-360, clockwise from north). Indicates the direction of increasing road section numbering. Null if not measured.
- **`start_time`** (string, required): ISO 8601 UTC timestamp when the station started collecting data (e.g. "2001-11-07T00:00:00Z").
- **`livi_id`** (string or null, optional): Legacy identifier used by the Finnish Transport Infrastructure Agency (Väylävirasto, formerly Liikennevirasto) for the station (e.g. "Livi968639"). Null if not assigned.
- **`sensors`** (array of int32, required): Array of computational sensor identifiers available at this station. Each ID corresponds to a sensor that produces TmsSensorData telemetry events. Common sensor families: OHITUKSET (passings), KESKINOPEUS (average speed), LIUKUVA_NOPEUS (rolling speed). Sensor metadata is available at /api/tms/v1/sensors.
- **`data_updated_time`** (string or null, optional): ISO 8601 UTC timestamp when the station metadata was last updated in the Digitraffic system. Null if not tracked.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "name": "string",
  "tms_number": 0,
  "names_fi": "string",
  "names_sv": "string",
  "names_en": "string",
  "longitude": 0,
  "latitude": 0,
  "altitude": 0,
  "municipality": "string",
  "municipality_code": 0,
  "province": "string",
  "province_code": 0,
  "road_number": 0,
  "road_section": 0,
  "distance_from_section_start": 0,
  "carriageway": "string",
  "side": "string",
  "station_type": "string",
  "collection_status": "string",
  "state": "string",
  "free_flow_speed_1": 0,
  "free_flow_speed_2": 0,
  "bearing": 0,
  "start_time": "string",
  "livi_id": "string",
  "sensors": [
    0
  ],
  "data_updated_time": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Weather Station

CloudEvents type: `fi.digitraffic.road.stations.WeatherStation`

#### What it tells you

A reference record from Fintraffic Digitraffic for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is road weather station numeric identifier as assigned by Fintraffic (e.g. 1012). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-sensors`, key `{station_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/stations/{station_id}/weather-station`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{station_id}`; application properties station_id `{station_id}` |

#### Payload

`Weather Station` payloads are JSON object. Required fields: `station_id`, `name`, `longitude`, `latitude`, `municipality`, `municipality_code`, `province`, `province_code`, `road_number`, `road_section`, `station_type`, `master`, `collection_status`, `collection_interval`, `start_time`, `sensors`.

- **`station_id`** (int32, required): Road weather station numeric identifier as assigned by Fintraffic (e.g. 1012). Uniqueness scope is road weather stations. Corresponds to the station_id in WeatherSensorData telemetry events.
- **`name`** (string, required): Internal station name used by Fintraffic, typically encoding road type, municipality and area (e.g. "kt51_Espoo_Kivenlahti"). Not intended for display.
- **`names_fi`** (string, optional): Finnish display name for the station (e.g. "Tie 51 Espoo, Kivenlahti").
- **`names_sv`** (string or null, optional): Swedish display name for the station (e.g. "Väg 51 Esbo, Stensvik"). Null if no translation available.
- **`names_en`** (string or null, optional): English display name for the station (e.g. "Road 51 Espoo, Kivenlahti"). Null if no translation available.
- **`longitude`** (double, required): Station longitude in WGS84 (EPSG:4326) decimal degrees.
- **`latitude`** (double, required): Station latitude in WGS84 (EPSG:4326) decimal degrees.
- **`altitude`** (double or null, optional): Station altitude in meters above sea level. Null or 0.0 if altitude data is not available.
- **`municipality`** (string, required): Name of the Finnish municipality where the station is located.
- **`municipality_code`** (int32, required): Finnish municipality code as defined by Statistics Finland.
- **`province`** (string, required): Name of the Finnish province (maakunta) where the station is located.
- **`province_code`** (int32, required): Finnish province code as defined by Statistics Finland.
- **`road_number`** (int32, required): Finnish road number where the station is installed.
- **`road_section`** (int32, required): Road section number within the road.
- **`distance_from_section_start`** (int32, optional): Distance from the start of the road section in meters.
- **`carriageway`** (string or null, optional): Carriageway type at the station location. Values include "DUAL_CARRIAGEWAY_RIGHT_IN_INCREASING_DIRECTION", "DUAL_CARRIAGEWAY_LEFT_IN_INCREASING_DIRECTION", "ONE_CARRIAGEWAY". Null if not specified.
- **`side`** (string or null, optional): Side of the road. Values: "LEFT", "RIGHT", "BETWEEN", "UNKNOWN". Null if not specified.
- **`contract_area`** (string or null, optional): Road maintenance contract area name (e.g. "Espoo 19-24"). Identifies the maintenance contract responsible for the road section. Null if not assigned.
- **`contract_area_code`** (int32 or null, optional): Numeric code for the maintenance contract area (e.g. 142). Null if not assigned.
- **`station_type`** (string, required): Weather station type code indicating the hardware configuration (e.g. "RWS_200" for a Rosa RWS-200 station). Determines available sensor capabilities.
- **`master`** (boolean, required): Whether this is a master station. Master stations are the primary data source; non-master stations may be auxiliary or backup installations at the same location.
- **`collection_status`** (string, required): Current data collection status. Values: "GATHERING" (actively collecting), "REMOVED_TEMPORARILY", "REMOVED_PERMANENTLY".
- **`collection_interval`** (int32, required): Data collection interval in seconds. Typical value is 300 (5 minutes) for road weather stations.
- **`state`** (string or null, optional): Operational state of the station hardware. Null if state information is not available from the upstream API.
- **`start_time`** (string, required): ISO 8601 UTC timestamp when the station started collecting data.
- **`livi_id`** (string or null, optional): Legacy identifier from the Finnish Transport Infrastructure Agency. Null if not assigned.
- **`sensors`** (array of int32, required): Array of sensor identifiers available at this station. Each ID corresponds to a sensor producing WeatherSensorData telemetry. Common sensors: ILMA (1, air temp), TIE_1 (3, road surface temp), KASTEPISTE (9, dew point), KESKITUULI (16, avg wind), ILMAN_KOSTEUS (19, humidity). Full list at /api/weather/v1/sensors.
- **`data_updated_time`** (string or null, optional): ISO 8601 UTC timestamp when the station metadata was last updated. Null if not tracked.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": 0,
  "name": "string",
  "names_fi": "string",
  "names_sv": "string",
  "names_en": "string",
  "longitude": 0,
  "latitude": 0,
  "altitude": 0,
  "municipality": "string",
  "municipality_code": 0,
  "province": "string",
  "province_code": 0,
  "road_number": 0,
  "road_section": 0,
  "distance_from_section_start": 0,
  "carriageway": "string",
  "side": "string",
  "contract_area": "string",
  "contract_area_code": 0,
  "station_type": "string",
  "master": false,
  "collection_status": "string",
  "collection_interval": 0,
  "state": "string",
  "start_time": "string",
  "livi_id": "string",
  "sensors": [
    0
  ],
  "data_updated_time": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Maintenance Task Type

CloudEvents type: `fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType`

#### What it tells you

A transport update from Fintraffic Digitraffic. It carries road traffic measurements and status updates for Finnish road network sensors and traffic messages.

#### Identity

Each event identifies the real-world resource with `{task_id}`. `{task_id}` is unique task type identifier using SCREAMING_SNAKE_CASE convention (e.g. "PLOUGHING_AND_SLUSH_REMOVAL", "SALTING", "BRUSHING"). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `digitraffic-road-maintenance`, key `{task_id}` |
| `MQTT/5.0` | topic `traffic/fi/fintraffic/digitraffic-road/maintenance-tasks/{task_id}/task-type`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/digitraffic-road`, message subject `{task_id}`; application properties task_id `{task_id}` |

#### Payload

`Maintenance Task Type` payloads are JSON object. Required fields: `task_id`, `name_fi`, `name_en`, `name_sv`.

- **`task_id`** (string, required): Unique task type identifier using SCREAMING_SNAKE_CASE convention (e.g. "PLOUGHING_AND_SLUSH_REMOVAL", "SALTING", "BRUSHING"). This identifier appears in the tasks array of MaintenanceTracking telemetry events.
- **`name_fi`** (string, required): Finnish name for the maintenance task type (e.g. "Auraus ja sohjonpoisto", "Suolaus", "Harjaus").
- **`name_en`** (string, required): English name for the maintenance task type (e.g. "Ploughing and slush removal", "Salting", "Brushing").
- **`name_sv`** (string, required): Swedish name for the maintenance task type (e.g. "Plöjning och snöslaskborttagning", "Saltning", "Borstning").
- **`data_updated_time`** (string or null, optional): ISO 8601 UTC timestamp when this task type definition was last updated in the Digitraffic system (e.g. "2020-03-30T00:00:00Z"). Null if not tracked.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "task_id": "string",
  "name_fi": "string",
  "name_en": "string",
  "name_sv": "string",
  "data_updated_time": "string"
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

- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/digitraffic_road.xreg.json`](xreg/digitraffic_road.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
