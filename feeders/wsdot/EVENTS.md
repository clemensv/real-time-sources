# WSDOT Events

WSDOT publishes traffic, travel, bridge, toll, pass, ferry, and border-wait updates from Washington State Department of Transportation for Washington road, bridge, pass, ferry, and border resources. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 16 documented event types (48 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 5 reference/catalog event types and 11 telemetry event types.
- **Identity:** `{flow_data_id}`, `{travel_time_id}`, `{mountain_pass_id}`, `{station_id}`, `{trip_name}`, `{state_route_id}/{bridge_number}`, `{crossing_name}`, `{vessel_id}`, `{alert_id}`, `{camera_id}`, `{crossing_location_id}`, `{terminal_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `wsdot`. The record key is `{flow_data_id}`, `{travel_time_id}`, `{mountain_pass_id}`, `{station_id}`, `{trip_name}`, `{state_route_id}/{bridge_number}`, `{crossing_name}`, `{vessel_id}`, `{alert_id}`, `{camera_id}`, `{crossing_location_id}`, `{terminal_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['wsdot'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/us/wsdot/wsdot/+/flow/+/info`, `traffic/us/wsdot/wsdot/+/flow/+/reading`, `traffic/us/wsdot/wsdot/+/travel-times/+/info`, `traffic/us/wsdot/wsdot/+/mountain-passes/+/info`, `traffic/us/wsdot/wsdot/+/flow-stations/+/info`, `traffic/us/wsdot/wsdot/+/flow-stations/+/reading`, `traffic/us/wsdot/wsdot/+/tolls/+/rate`, `traffic/us/wsdot/wsdot/+/bridges/+/+/info`, `traffic/us/wsdot/wsdot/+/border-crossings/+/info`, `traffic/us/wsdot/wsdot/+/vessels/+/location`, `traffic/us/wsdot/wsdot/road-weather-stations/+/info`, `traffic/us/wsdot/wsdot/road-weather-stations/+/reading`, `traffic/us/wsdot/wsdot/alerts/+/info`, `traffic/us/wsdot/wsdot/cameras/+/info`, `traffic/us/wsdot/wsdot/bridge-clearances/+/info`, `traffic/us/wsdot/wsdot/ferry-terminals/+/sailing-space`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/us/wsdot/wsdot/+/flow/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `broker-configured address`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/events')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Traffic Flow Station

CloudEvents type: `us.wa.wsdot.traffic.TrafficFlowStation`

#### What it tells you

Metadata for a traffic flow sensor station in the Washington State DOT network. WSDOT deploys approximately 1,400 inductive loop sensors embedded in highway pavement across four geographic regions.

#### Identity

Each event identifies the real-world resource with `{flow_data_id}`. `{flow_data_id}` is unique numeric identifier for this traffic flow sensor station, stringified from upstream FlowDataID. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{flow_data_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/flow/{flow_data_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{flow_data_id}` |

#### Payload

`Traffic Flow Station` payloads are JSON object. Required fields: `flow_data_id`, `station_name`, `region`, `description`, `road_name`, `direction`, `milepost`, `latitude`, `longitude`.

- **`flow_data_id`** (string, required): Unique numeric identifier for this traffic flow sensor station, stringified from upstream FlowDataID.
- **`station_name`** (string, required): Descriptive name of the flow sensor station.
- **`region`** (enum, required): WSDOT geographic coverage region.
- **`description`** (string or null, required): Location description. Null if not provided.
- **`road_name`** (string, required): Road designation where the sensor is installed.
- **`direction`** (string or null, required): Direction of travel monitored. Examples: NB, SB, EB, WB.
- **`milepost`** (double or null, required): Milepost marker along the roadway.
- **`latitude`** (double, required, deg (°)): Latitude in WGS84 decimal degrees.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84 decimal degrees.
##### `region` values

- `Eastern`
- `Northwest`
- `Olympic`
- `Southwest`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "flow_data_id": "string",
  "station_name": "string",
  "region": "Eastern",
  "description": "string",
  "road_name": "string",
  "direction": "string",
  "milepost": 0,
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Traffic Flow Reading

CloudEvents type: `us.wa.wsdot.traffic.TrafficFlowReading`

#### What it tells you

A traffic flow reading from a WSDOT sensor station. Updated approximately every 90 seconds, each reading reports the current Level of Service.

#### Identity

Each event identifies the real-world resource with `{flow_data_id}`. `{flow_data_id}` is sensor station identifier, stringified from upstream FlowDataID. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{flow_data_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/flow/{flow_data_id}/reading`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{flow_data_id}` |

#### Payload

`Traffic Flow Reading` payloads are JSON object. Required fields: `flow_data_id`, `station_name`, `region`, `flow_reading`, `reading_time`.

- **`flow_data_id`** (string, required): Sensor station identifier, stringified from upstream FlowDataID.
- **`station_name`** (string, required): Station name.
- **`region`** (enum, required): WSDOT region.
- **`flow_reading`** (enum, required): Current traffic Level of Service. Converted from upstream FlowReadingValue byte.
- **`reading_time`** (string, required): ISO 8601 UTC timestamp of the reading.
##### `region` values

- `Eastern`
- `Northwest`
- `Olympic`
- `Southwest`
##### `flow_reading` values

- `Unknown`
- `WideOpen`
- `Moderate`
- `Heavy`
- `StopAndGo`
- `NoData`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "flow_data_id": "string",
  "station_name": "string",
  "region": "Eastern",
  "flow_reading": "Unknown",
  "reading_time": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Travel Time Route

CloudEvents type: `us.wa.wsdot.traveltimes.TravelTimeRoute`

#### What it tells you

A named travel time route monitored by WSDOT. Each route has fixed start and end points on Washington State highways with historical average and current real-time travel times.

#### Identity

Each event identifies the real-world resource with `{travel_time_id}`. `{travel_time_id}` is unique route identifier, stringified from upstream TravelTimeID. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{travel_time_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/travel-times/{travel_time_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{travel_time_id}` |

#### Payload

`Travel Time Route` payloads are JSON object. Required fields: `travel_time_id`, `name`, `description`, `distance`, `average_time`, `current_time`, `time_updated`, `start_description`, `start_road_name`, `start_direction`, `start_milepost`, `start_latitude`, `start_longitude`, `end_description`, `end_road_name`, `end_direction`, `end_milepost`, `end_latitude`, `end_longitude`.

- **`travel_time_id`** (string, required): Unique route identifier, stringified from upstream TravelTimeID.
- **`name`** (string, required): Short route segment name.
- **`description`** (string, required): Longer description including lane type.
- **`distance`** (double, required, mi): Route distance in miles.
- **`average_time`** (int32, required, min): Historical average travel time in minutes.
- **`current_time`** (int32, required, min): Current real-time travel time in minutes.
- **`time_updated`** (string, required): ISO 8601 UTC timestamp of last update.
- **`start_description`** (string or null, required): Start point description.
- **`start_road_name`** (string or null, required): Road at start point.
- **`start_direction`** (string or null, required): Direction at start point.
- **`start_milepost`** (double or null, required): Milepost at start.
- **`start_latitude`** (double, required, deg (°)): Start latitude in WGS84.
- **`start_longitude`** (double, required, deg (°)): Start longitude in WGS84.
- **`end_description`** (string or null, required): End point description.
- **`end_road_name`** (string or null, required): Road at end point.
- **`end_direction`** (string or null, required): Direction at end point.
- **`end_milepost`** (double or null, required): Milepost at end.
- **`end_latitude`** (double, required, deg (°)): End latitude in WGS84.
- **`end_longitude`** (double, required, deg (°)): End longitude in WGS84.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "travel_time_id": "string",
  "name": "string",
  "description": "string",
  "distance": 0,
  "average_time": 0,
  "current_time": 0,
  "time_updated": "string",
  "start_description": "string",
  "start_road_name": "string",
  "start_direction": "string",
  "start_milepost": 0,
  "start_latitude": 0,
  "start_longitude": 0,
  "end_description": "string",
  "end_road_name": "string",
  "end_direction": "string",
  "end_milepost": 0,
  "end_latitude": 0,
  "end_longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Mountain Pass Condition

CloudEvents type: `us.wa.wsdot.mountainpass.MountainPassCondition`

#### What it tells you

Current conditions at a Washington State mountain pass including temperature, weather, road conditions, travel advisories, and directional restrictions.

#### Identity

Each event identifies the real-world resource with `{mountain_pass_id}`. `{mountain_pass_id}` is unique pass identifier, stringified from upstream MountainPassId. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{mountain_pass_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/mountain-passes/{mountain_pass_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{mountain_pass_id}` |

#### Payload

`Mountain Pass Condition` payloads are JSON object. Required fields: `mountain_pass_id`, `mountain_pass_name`, `elevation_in_feet`, `latitude`, `longitude`, `temperature_in_fahrenheit`, `weather_condition`, `road_condition`, `travel_advisory_active`, `restriction_one_direction`, `restriction_one_text`, `restriction_two_direction`, `restriction_two_text`, `date_updated`.

- **`mountain_pass_id`** (string, required): Unique pass identifier, stringified from upstream MountainPassId.
- **`mountain_pass_name`** (string, required): Pass name with highway designation.
- **`elevation_in_feet`** (int32, required, ft): Summit elevation in feet above sea level.
- **`latitude`** (double, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84.
- **`temperature_in_fahrenheit`** (int32 or null, required, degF (°F)): Temperature at the summit in Fahrenheit. Null if not reporting.
- **`weather_condition`** (string, required): Current weather condition text. Examples: Clear, Rain, Snow, Fog.
- **`road_condition`** (string, required): Road surface condition text. Examples: Dry, Wet, Compact Snow, Ice.
- **`travel_advisory_active`** (boolean, required): True if a travel advisory is in effect.
- **`restriction_one_direction`** (string or null, required): Direction for first restriction.
- **`restriction_one_text`** (string or null, required): First restriction text.
- **`restriction_two_direction`** (string or null, required): Direction for second restriction.
- **`restriction_two_text`** (string or null, required): Second restriction text.
- **`date_updated`** (string, required): ISO 8601 UTC timestamp of last update.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mountain_pass_id": "string",
  "mountain_pass_name": "string",
  "elevation_in_feet": 0,
  "latitude": 0,
  "longitude": 0,
  "temperature_in_fahrenheit": 0,
  "weather_condition": "string",
  "road_condition": "string",
  "travel_advisory_active": false,
  "restriction_one_direction": "string",
  "restriction_one_text": "string",
  "restriction_two_direction": "string",
  "restriction_two_text": "string",
  "date_updated": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Weather Station

CloudEvents type: `us.wa.wsdot.weather.WeatherStation`

#### What it tells you

Metadata for a WSDOT road weather information system (RWIS) station. WSDOT operates approximately 134 stations across Washington State highways.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is station identifier from upstream StationID. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{station_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/flow-stations/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{station_id}` |

#### Payload

`Weather Station` payloads are JSON object. Required fields: `station_id`, `station_name`, `latitude`, `longitude`.

- **`station_id`** (string, required): Station identifier from upstream StationID. The WeatherStation reference event is synthesized from the current-readings payload (the legacy WeatherStations endpoint was decommissioned), so this is the same numeric station identifier carried by WeatherReading.
- **`station_name`** (string, required): Station name with highway and milepost.
- **`latitude`** (double, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Weather Reading

CloudEvents type: `us.wa.wsdot.weather.WeatherReading`

#### What it tells you

A current weather reading from a WSDOT road weather station including temperature, wind, precipitation, pressure, humidity, visibility, and sky coverage.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is station identifier from upstream StationID. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{station_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/flow-stations/{station_id}/reading`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{station_id}` |

#### Payload

`Weather Reading` payloads are JSON object. Required fields: `station_id`, `station_name`, `reading_time`, `temperature_in_fahrenheit`, `precipitation_in_inches`, `wind_speed_in_mph`, `wind_gust_speed_in_mph`, `wind_direction`, `wind_direction_cardinal`, `barometric_pressure`, `relative_humidity`, `visibility`, `sky_coverage`, `latitude`, `longitude`.

- **`station_id`** (string, required): Station identifier from upstream StationID.
- **`station_name`** (string, required): Station name.
- **`reading_time`** (string, required): ISO 8601 UTC timestamp.
- **`temperature_in_fahrenheit`** (double or null, required, degF (°F)): Air temperature in Fahrenheit.
- **`precipitation_in_inches`** (double or null, required, in): Precipitation in inches.
- **`wind_speed_in_mph`** (double or null, required, mi/h (mph)): Wind speed in mph.
- **`wind_gust_speed_in_mph`** (double or null, required, mi/h (mph)): Wind gust speed in mph.
- **`wind_direction`** (int32 or null, required, deg (°)): Wind direction in degrees from true north.
- **`wind_direction_cardinal`** (string or null, required): Wind direction as cardinal abbreviation.
- **`barometric_pressure`** (double or null, required, hPa): Barometric pressure in hPa.
- **`relative_humidity`** (int32 or null, required, %): Relative humidity percentage.
- **`visibility`** (double or null, required): Visibility distance.
- **`sky_coverage`** (string or null, required): Sky coverage description.
- **`latitude`** (double, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "reading_time": "string",
  "temperature_in_fahrenheit": 0,
  "precipitation_in_inches": 0,
  "wind_speed_in_mph": 0,
  "wind_gust_speed_in_mph": 0,
  "wind_direction": 0,
  "wind_direction_cardinal": "string",
  "barometric_pressure": 0,
  "relative_humidity": 0,
  "visibility": 0,
  "sky_coverage": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Toll Rate

CloudEvents type: `us.wa.wsdot.tolls.TollRate`

#### What it tells you

Current toll rate for a WSDOT tolled route segment. WSDOT operates dynamic tolling on SR 99, I-405, and SR 167.

#### Identity

Each event identifies the real-world resource with `{trip_name}`. `{trip_name}` is tolled route segment identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{trip_name}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/tolls/{trip_name}/rate`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{trip_name}` |

#### Payload

`Toll Rate` payloads are JSON object. Required fields: `trip_name`, `state_route`, `travel_direction`, `current_toll`, `current_message`, `time_updated`, `start_location_name`, `start_latitude`, `start_longitude`, `start_milepost`, `end_location_name`, `end_latitude`, `end_longitude`, `end_milepost`.

- **`trip_name`** (string, required): Tolled route segment identifier.
- **`state_route`** (string, required): State route number.
- **`travel_direction`** (string, required): Travel direction: N, S, E, W.
- **`current_toll`** (int32, required): Current toll in cents.
- **`current_message`** (string or null, required): Optional status message.
- **`time_updated`** (string, required): ISO 8601 UTC timestamp.
- **`start_location_name`** (string, required): Start location name.
- **`start_latitude`** (double, required, deg (°)): Start latitude.
- **`start_longitude`** (double, required, deg (°)): Start longitude.
- **`start_milepost`** (double, required): Start milepost.
- **`end_location_name`** (string, required): End location name.
- **`end_latitude`** (double, required, deg (°)): End latitude.
- **`end_longitude`** (double, required, deg (°)): End longitude.
- **`end_milepost`** (double, required): End milepost.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "trip_name": "string",
  "state_route": "string",
  "travel_direction": "string",
  "current_toll": 0,
  "current_message": "string",
  "time_updated": "string",
  "start_location_name": "string",
  "start_latitude": 0,
  "start_longitude": 0,
  "start_milepost": 0,
  "end_location_name": "string",
  "end_latitude": 0,
  "end_longitude": 0,
  "end_milepost": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Commercial Vehicle Restriction

CloudEvents type: `us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction`

#### What it tells you

A commercial vehicle restriction on a Washington State highway bridge or road segment. Restrictions limit vehicle weight, height, length, or width.

#### Identity

Each event identifies the real-world resource with `{state_route_id}/{bridge_number}`. `{state_route_id}` is state route identifier, first part of composite key; `{bridge_number}` is bridge or structure number, second part of composite key. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{state_route_id}/{bridge_number}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/bridges/{state_route_id}/{bridge_number}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{state_route_id}/{bridge_number}` |

#### Payload

`Commercial Vehicle Restriction` payloads are JSON object. Required fields: `state_route_id`, `bridge_number`, `bridge_name`, `location_name`, `location_description`, `latitude`, `longitude`, `state`, `restriction_type`, `vehicle_type`, `restriction_weight_in_pounds`, `maximum_gross_vehicle_weight_in_pounds`, `restriction_height_in_inches`, `restriction_width_in_inches`, `restriction_length_in_inches`, `is_permanent_restriction`, `is_warning`, `is_detour_available`, `is_exceptions_allowed`, `restriction_comment`, `date_posted`, `date_effective`, `date_expires`.

- **`state_route_id`** (string, required): State route identifier, first part of composite key.
- **`bridge_number`** (string, required): Bridge or structure number, second part of composite key.
- **`bridge_name`** (string or null, required): Bridge or structure name.
- **`location_name`** (string or null, required): Location relative to landmarks.
- **`location_description`** (string or null, required): Detailed location description.
- **`latitude`** (double, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84.
- **`state`** (string or null, required): State abbreviation, typically WA.
- **`restriction_type`** (string or null, required): Type: BridgeRestriction, RoadRestriction.
- **`vehicle_type`** (string or null, required): Affected vehicle type.
- **`restriction_weight_in_pounds`** (int32 or null, required, lb (lbs)): Axle weight limit in pounds.
- **`maximum_gross_vehicle_weight_in_pounds`** (int32 or null, required, lb (lbs)): GVW limit in pounds.
- **`restriction_height_in_inches`** (int32 or null, required, in): Height limit in inches.
- **`restriction_width_in_inches`** (int32 or null, required, in): Width limit in inches.
- **`restriction_length_in_inches`** (int32 or null, required, in): Length limit in inches.
- **`is_permanent_restriction`** (boolean, required): True if permanent.
- **`is_warning`** (boolean, required): True if warning only.
- **`is_detour_available`** (boolean, required): True if detour exists.
- **`is_exceptions_allowed`** (boolean, required): True if permits available.
- **`restriction_comment`** (string or null, required): Additional details.
- **`date_posted`** (string or null, required): ISO 8601 UTC date posted.
- **`date_effective`** (string or null, required): ISO 8601 UTC date effective.
- **`date_expires`** (string or null, required): ISO 8601 UTC date expires.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "state_route_id": "string",
  "bridge_number": "string",
  "bridge_name": "string",
  "location_name": "string",
  "location_description": "string",
  "latitude": 0,
  "longitude": 0,
  "state": "string",
  "restriction_type": "string",
  "vehicle_type": "string",
  "restriction_weight_in_pounds": 0,
  "maximum_gross_vehicle_weight_in_pounds": 0,
  "restriction_height_in_inches": 0,
  "restriction_width_in_inches": 0,
  "restriction_length_in_inches": 0,
  "is_permanent_restriction": false,
  "is_warning": false,
  "is_detour_available": false,
  "is_exceptions_allowed": false,
  "restriction_comment": "string",
  "date_posted": "string",
  "date_effective": "string",
  "date_expires": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Border Crossing

CloudEvents type: `us.wa.wsdot.border.BorderCrossing`

#### What it tells you

Current wait time at a US-Canada border crossing lane in Washington State. Wait times are in minutes, updated approximately every 5 minutes.

#### Identity

Each event identifies the real-world resource with `{crossing_name}`. `{crossing_name}` is crossing lane identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{crossing_name}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/border-crossings/{crossing_name}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{crossing_name}` |

#### Payload

`Border Crossing` payloads are JSON object. Required fields: `crossing_name`, `wait_time`, `time`, `description`, `road_name`, `latitude`, `longitude`.

- **`crossing_name`** (string, required): Crossing lane identifier.
- **`wait_time`** (int32 or null, required, min): Wait time in minutes.
- **`time`** (string, required): ISO 8601 UTC measurement timestamp.
- **`description`** (string or null, required): Lane description.
- **`road_name`** (string or null, required): Road designation.
- **`latitude`** (double, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "crossing_name": "string",
  "wait_time": 0,
  "time": "string",
  "description": "string",
  "road_name": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Vessel Location

CloudEvents type: `us.wa.wsdot.ferries.VesselLocation`

#### What it tells you

Real-time location and status of a Washington State Ferries vessel. WSF operates approximately 21 vessels across Puget Sound routes.

#### Identity

Each event identifies the real-world resource with `{vessel_id}`. `{vessel_id}` is vessel identifier, stringified from upstream VesselID. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{vessel_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/{region}/vessels/{vessel_id}/location`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{vessel_id}` |

#### Payload

`Vessel Location` payloads are JSON object. Required fields: `vessel_id`, `vessel_name`, `mmsi`, `in_service`, `at_dock`, `latitude`, `longitude`, `speed`, `heading`, `departing_terminal_id`, `departing_terminal_name`, `departing_terminal_abbrev`, `arriving_terminal_id`, `arriving_terminal_name`, `arriving_terminal_abbrev`, `scheduled_departure`, `left_dock`, `eta`, `eta_basis`, `route_abbreviation`, `timestamp`.

- **`vessel_id`** (string, required): Vessel identifier, stringified from upstream VesselID.
- **`vessel_name`** (string, required): Ferry vessel name.
- **`mmsi`** (int32 or null, required): Maritime Mobile Service Identity for AIS.
- **`in_service`** (boolean, required): True if in active service.
- **`at_dock`** (boolean, required): True if docked.
- **`latitude`** (double, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84.
- **`speed`** (double or null, required, kn): Speed in knots.
- **`heading`** (int32 or null, required, deg (°)): Heading in degrees.
- **`departing_terminal_id`** (int32 or null, required): Departure terminal ID.
- **`departing_terminal_name`** (string or null, required): Departure terminal name.
- **`departing_terminal_abbrev`** (string or null, required): Departure terminal abbreviation.
- **`arriving_terminal_id`** (int32 or null, required): Arrival terminal ID.
- **`arriving_terminal_name`** (string or null, required): Arrival terminal name.
- **`arriving_terminal_abbrev`** (string or null, required): Arrival terminal abbreviation.
- **`scheduled_departure`** (string or null, required): ISO 8601 UTC scheduled departure.
- **`left_dock`** (string or null, required): ISO 8601 UTC actual departure.
- **`eta`** (string or null, required): ISO 8601 UTC estimated arrival.
- **`eta_basis`** (string or null, required): ETA calculation description.
- **`route_abbreviation`** (string or null, required): Current route abbreviation.
- **`timestamp`** (string, required): ISO 8601 UTC position timestamp.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "vessel_id": "string",
  "vessel_name": "string",
  "mmsi": 0,
  "in_service": false,
  "at_dock": false,
  "latitude": 0,
  "longitude": 0,
  "speed": 0,
  "heading": 0,
  "departing_terminal_id": 0,
  "departing_terminal_name": "string",
  "departing_terminal_abbrev": "string",
  "arriving_terminal_id": 0,
  "arriving_terminal_name": "string",
  "arriving_terminal_abbrev": "string",
  "scheduled_departure": "string",
  "left_dock": "string",
  "eta": "string",
  "eta_basis": "string",
  "route_abbreviation": "string",
  "timestamp": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Road Weather Station

CloudEvents type: `us.wa.wsdot.roadweather.RoadWeatherStation`

#### What it tells you

Metadata for a WSDOT Scanweb road weather information system (RWIS) station, including position and elevation. WSDOT operates roughly 105 Scanweb stations reporting pavement and atmospheric conditions across Washington State highways.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable station identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{station_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/road-weather-stations/{station_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{station_id}` |

#### Payload

`Road Weather Station` payloads are JSON object. Required fields: `station_id`, `station_name`, `latitude`, `longitude`, `elevation`.

- **`station_id`** (string, required): Stable station identifier. From upstream StationId; when StationId is blank (a few Scanweb stations report a blank id) the bridge copies the unique StationName into this field so every station has a stable, non-empty key.
- **`station_name`** (string, required): Station name (unique across the Scanweb network).
- **`latitude`** (double, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84.
- **`elevation`** (int32 or null, required, m): Station elevation above sea level.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Road Weather Reading

CloudEvents type: `us.wa.wsdot.roadweather.RoadWeatherReading`

#### What it tells you

A current Scanweb road weather reading including air temperature, humidity, wind, visibility, precipitation totals, and per-sensor road surface and sub-surface measurements.

#### Identity

Each event identifies the real-world resource with `{station_id}`. `{station_id}` is stable station identifier, matching the RoadWeatherStation key (StationId, or StationName when StationId is blank). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{station_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/road-weather-stations/{station_id}/reading`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{station_id}` |

#### Payload

`Road Weather Reading` payloads are JSON object. Required fields: `station_id`, `station_name`, `latitude`, `longitude`, `elevation`, `reading_time`, `air_temperature`, `relative_humidity`, `average_wind_speed`, `average_wind_direction`, `wind_gust`, `visibility`, `precipitation_intensity`, `precipitation_type`, `precipitation_past_1_hour`, `precipitation_past_3_hours`, `precipitation_past_6_hours`, `precipitation_past_12_hours`, `precipitation_past_24_hours`, `precipitation_accumulation`, `barometric_pressure`, `snow_depth`, `surface_measurements`, `sub_surface_measurements`.

- **`station_id`** (string, required): Stable station identifier, matching the RoadWeatherStation key (StationId, or StationName when StationId is blank).
- **`station_name`** (string, required): Station name.
- **`latitude`** (double, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double, required, deg (°)): Longitude in WGS84.
- **`elevation`** (int32 or null, required, m): Station elevation above sea level.
- **`reading_time`** (string, required): Observation time as reported by Scanweb (ISO 8601, without timezone offset; interpreted as the station's local reporting clock).
- **`air_temperature`** (double or null, required, Cel (°C)): Air temperature.
- **`relative_humidity`** (int32 or null, required, %): Relative humidity percentage. Upstream key is misspelled 'RelativeHumidty'.
- **`average_wind_speed`** (double or null, required, m/s): Average wind speed.
- **`average_wind_direction`** (int32 or null, required, deg (°)): Average wind direction in degrees from true north.
- **`wind_gust`** (double or null, required, m/s): Peak wind gust speed.
- **`visibility`** (int32 or null, required, m): Visibility distance.
- **`precipitation_intensity`** (int32 or null, required): Coded precipitation intensity as an opaque integer reported by the upstream Scanweb feed; WSDOT does not publish the code dictionary, so the value is passed through unmodified. Null when not reported.
- **`precipitation_type`** (int32 or null, required): Coded precipitation type as an opaque integer reported by the upstream Scanweb feed (commonly none, rain, or snow); WSDOT does not publish the full code dictionary, so the value is passed through unmodified. Null when not reported.
- **`precipitation_past_1_hour`** (double or null, required, mm): Liquid-equivalent precipitation accumulated in the past 1 hour.
- **`precipitation_past_3_hours`** (double or null, required, mm): Liquid-equivalent precipitation accumulated in the past 3 hours.
- **`precipitation_past_6_hours`** (double or null, required, mm): Liquid-equivalent precipitation accumulated in the past 6 hours.
- **`precipitation_past_12_hours`** (double or null, required, mm): Liquid-equivalent precipitation accumulated in the past 12 hours.
- **`precipitation_past_24_hours`** (double or null, required, mm): Liquid-equivalent precipitation accumulated in the past 24 hours.
- **`precipitation_accumulation`** (double or null, required, mm): Cumulative precipitation accumulation reported by the gauge, or null.
- **`barometric_pressure`** (double or null, required, hPa): Barometric pressure, or null when the station has no pressure sensor.
- **`snow_depth`** (double or null, required, cm): Measured snow depth, or null when the station has no snow sensor.
- **`surface_measurements`** (array of object, required): Per-sensor road surface measurements (temperature, freezing point, surface condition).
- **`sub_surface_measurements`** (array of object, required): Per-sensor sub-surface (in-pavement) temperature measurements.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "station_id": "string",
  "station_name": "string",
  "latitude": 0,
  "longitude": 0,
  "elevation": 0,
  "reading_time": "string",
  "air_temperature": 0,
  "relative_humidity": 0,
  "average_wind_speed": 0,
  "average_wind_direction": 0,
  "wind_gust": 0,
  "visibility": 0,
  "precipitation_intensity": 0,
  "precipitation_type": 0,
  "precipitation_past_1_hour": 0,
  "precipitation_past_3_hours": 0,
  "precipitation_past_6_hours": 0,
  "precipitation_past_12_hours": 0,
  "precipitation_past_24_hours": 0,
  "precipitation_accumulation": 0,
  "barometric_pressure": 0,
  "snow_depth": 0,
  "surface_measurements": [
    {
      "sensor_id": 0,
      "surface_temperature": 0,
      "road_freezing_temperature": 0,
      "road_surface_condition": 0
    }
  ],
  "sub_surface_measurements": [
    {
      "sensor_id": 0,
      "sub_surface_temperature": 0
    }
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Highway Alert

CloudEvents type: `us.wa.wsdot.alerts.HighwayAlert`

#### What it tells you

An active WSDOT highway alert describing an incident, construction, closure, special event, or weather impact, with start and end roadway locations on the Washington State highway network.

#### Identity

Each event identifies the real-world resource with `{alert_id}`. `{alert_id}` is WSDOT alert identifier (stable for the life of the alert). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{alert_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/alerts/{alert_id}/info`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{alert_id}` |

#### Payload

`Highway Alert` payloads are JSON object. Required fields: `alert_id`, `county`, `region`, `priority`, `event_category`, `event_status`, `headline_description`, `extended_description`, `start_time`, `end_time`, `last_updated_time`, `start_description`, `start_direction`, `start_road_name`, `start_milepost`, `start_latitude`, `start_longitude`, `end_description`, `end_direction`, `end_road_name`, `end_milepost`, `end_latitude`, `end_longitude`.

- **`alert_id`** (string, required): WSDOT alert identifier (stable for the life of the alert).
- **`county`** (string or null, required): County in which the alert is located.
- **`region`** (string or null, required): WSDOT region responsible for the alert.
- **`priority`** (string or null, required): Alert priority (Highest, High, Medium, Low, Lowest).
- **`event_category`** (string or null, required): Category of the event (e.g. Collision, Construction, Special Event, Weather).
- **`event_status`** (string or null, required): Current status of the event (Open or Closed).
- **`headline_description`** (string or null, required): Short human-readable headline for the alert.
- **`extended_description`** (string or null, required): Longer human-readable description with full details.
- **`start_time`** (string or null, required): Alert start time as an ISO 8601 UTC timestamp.
- **`end_time`** (string or null, required): Alert end time as an ISO 8601 UTC timestamp, or null if open-ended.
- **`last_updated_time`** (string or null, required): Time the alert was last updated, as an ISO 8601 UTC timestamp.
- **`start_description`** (string or null, required): Description of the start roadway location.
- **`start_direction`** (string or null, required): Travel direction at the start location (e.g. B, N, S, E, W).
- **`start_road_name`** (string or null, required): Road name/route designation at the start location.
- **`start_milepost`** (double or null, required, mi): Milepost of the start location.
- **`start_latitude`** (double or null, required, deg (°)): Latitude of the start location in WGS84.
- **`start_longitude`** (double or null, required, deg (°)): Longitude of the start location in WGS84.
- **`end_description`** (string or null, required): Description of the end roadway location.
- **`end_direction`** (string or null, required): Travel direction at the end location.
- **`end_road_name`** (string or null, required): Road name/route designation at the end location.
- **`end_milepost`** (double or null, required, mi): Milepost of the end location.
- **`end_latitude`** (double or null, required, deg (°)): Latitude of the end location in WGS84.
- **`end_longitude`** (double or null, required, deg (°)): Longitude of the end location in WGS84.
##### `priority` values

- `Highest`
- `High`
- `Medium`
- `Low`
- `Lowest`
##### `event_status` values

- `Open`
- `Closed`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "alert_id": "string",
  "county": "string",
  "region": "string",
  "priority": "Highest",
  "event_category": "string",
  "event_status": "Open",
  "headline_description": "string",
  "extended_description": "string",
  "start_time": "string",
  "end_time": "string",
  "last_updated_time": "string",
  "start_description": "string",
  "start_direction": "string",
  "start_road_name": "string",
  "start_milepost": 0,
  "start_latitude": 0,
  "start_longitude": 0,
  "end_description": "string",
  "end_direction": "string",
  "end_road_name": "string",
  "end_milepost": 0,
  "end_latitude": 0,
  "end_longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Highway Camera

CloudEvents type: `us.wa.wsdot.cameras.HighwayCamera`

#### What it tells you

Reference catalog entry for a WSDOT highway traffic camera, including its location and a claim-check image URL. The image bytes are not transported; consumers fetch the most recent frame from ImageURL on demand.

#### Identity

Each event identifies the real-world resource with `{camera_id}`. `{camera_id}` is WSDOT camera identifier (stable). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{camera_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/cameras/{camera_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{camera_id}` |

#### Payload

`Highway Camera` payloads are JSON object. Required fields: `camera_id`, `title`, `description`, `camera_owner`, `owner_url`, `image_url`, `image_width`, `image_height`, `is_active`, `region`, `sort_order`, `display_latitude`, `display_longitude`, `location_description`, `location_direction`, `location_road_name`, `location_milepost`, `location_latitude`, `location_longitude`.

- **`camera_id`** (string, required): WSDOT camera identifier (stable).
- **`title`** (string or null, required): Human-readable camera title.
- **`description`** (string or null, required): Optional camera description.
- **`camera_owner`** (string or null, required): Organization that owns/operates the camera.
- **`owner_url`** (string or null, required): URL with more information from the camera owner.
- **`image_url`** (string, required): Claim-check URL of the current camera image. The image bytes are not transported in the event; consumers fetch the latest frame from this URL on demand.
- **`image_width`** (int32 or null, required, px): Width of the camera image.
- **`image_height`** (int32 or null, required, px): Height of the camera image.
- **`is_active`** (boolean, required): Whether the camera is currently active.
- **`region`** (string or null, required): WSDOT region (or area code) for the camera.
- **`sort_order`** (int32 or null, required): WSDOT display sort order.
- **`display_latitude`** (double or null, required, deg (°)): Latitude used for map display, in WGS84.
- **`display_longitude`** (double or null, required, deg (°)): Longitude used for map display, in WGS84.
- **`location_description`** (string or null, required): Description of the camera roadway location.
- **`location_direction`** (string or null, required): Travel direction the camera faces.
- **`location_road_name`** (string or null, required): Road name/route designation at the camera location.
- **`location_milepost`** (double or null, required, mi): Milepost of the camera location.
- **`location_latitude`** (double or null, required, deg (°)): Latitude of the camera location in WGS84.
- **`location_longitude`** (double or null, required, deg (°)): Longitude of the camera location in WGS84.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "camera_id": "string",
  "title": "string",
  "description": "string",
  "camera_owner": "string",
  "owner_url": "string",
  "image_url": "string",
  "image_width": 0,
  "image_height": 0,
  "is_active": false,
  "region": "string",
  "sort_order": 0,
  "display_latitude": 0,
  "display_longitude": 0,
  "location_description": "string",
  "location_direction": "string",
  "location_road_name": "string",
  "location_milepost": 0,
  "location_latitude": 0,
  "location_longitude": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Bridge Clearance

CloudEvents type: `us.wa.wsdot.bridgeclearances.BridgeClearance`

#### What it tells you

Reference catalog record of the surveyed vertical clearance of a structure crossing a Washington State highway, used for commercial vehicle routing. Largely static; refreshed periodically.

#### Identity

Each event identifies the real-world resource with `{crossing_location_id}`. `{crossing_location_id}` is stable crossing location identifier (CrossingLocationId). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{crossing_location_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/bridge-clearances/{crossing_location_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{crossing_location_id}` |

#### Payload

`Bridge Clearance` payloads are JSON object. Required fields: `crossing_location_id`, `bridge_number`, `state_route_id`, `state_structure_id`, `crossing_description`, `inventory_direction`, `srmp`, `srmp_ahead_back_indicator`, `latitude`, `longitude`, `vertical_clearance_maximum_inches`, `vertical_clearance_maximum_feet_inch`, `vertical_clearance_minimum_inches`, `vertical_clearance_minimum_feet_inch`, `control_entity_guid`, `crossing_record_guid`, `location_guid`, `route_date`, `api_last_update`.

- **`crossing_location_id`** (string, required): Stable crossing location identifier (CrossingLocationId).
- **`bridge_number`** (string or null, required): WSDOT bridge number of the structure.
- **`state_route_id`** (string or null, required): State route identifier the structure crosses, or null.
- **`state_structure_id`** (string or null, required): Statewide structure identifier.
- **`crossing_description`** (string or null, required): Human-readable description of the crossing.
- **`inventory_direction`** (string or null, required): Inventory direction of the structure, or null.
- **`srmp`** (double or null, required, mi): State route milepost of the crossing.
- **`srmp_ahead_back_indicator`** (string or null, required): Ahead/Back indicator disambiguating the milepost, or null.
- **`latitude`** (double or null, required, deg (°)): Latitude in WGS84.
- **`longitude`** (double or null, required, deg (°)): Longitude in WGS84.
- **`vertical_clearance_maximum_inches`** (int32 or null, required, in): Maximum vertical clearance, in inches.
- **`vertical_clearance_maximum_feet_inch`** (string or null, required): Maximum vertical clearance as a feet-and-inches display string (e.g. '14 ft 3 in').
- **`vertical_clearance_minimum_inches`** (int32 or null, required, in): Minimum vertical clearance, in inches.
- **`vertical_clearance_minimum_feet_inch`** (string or null, required): Minimum vertical clearance as a feet-and-inches display string.
- **`control_entity_guid`** (string or null, required): GUID of the controlling entity record.
- **`crossing_record_guid`** (string or null, required): GUID of the crossing record.
- **`location_guid`** (string or null, required): GUID of the location record.
- **`route_date`** (string or null, required): Effective route date as an ISO 8601 UTC timestamp.
- **`api_last_update`** (string or null, required): Time the clearance record was last updated upstream, as an ISO 8601 UTC timestamp.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "crossing_location_id": "string",
  "bridge_number": "string",
  "state_route_id": "string",
  "state_structure_id": "string",
  "crossing_description": "string",
  "inventory_direction": "string",
  "srmp": 0,
  "srmp_ahead_back_indicator": "string",
  "latitude": 0,
  "longitude": 0,
  "vertical_clearance_maximum_inches": 0,
  "vertical_clearance_maximum_feet_inch": "string",
  "vertical_clearance_minimum_inches": 0,
  "vertical_clearance_minimum_feet_inch": "string",
  "control_entity_guid": "string",
  "crossing_record_guid": "string",
  "location_guid": "string",
  "route_date": "string",
  "api_last_update": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity. MQTT may retain the latest copy so late subscribers can build local context immediately.

### Terminal Sailing Space

CloudEvents type: `us.wa.wsdot.ferryterminals.TerminalSailingSpace`

#### What it tells you

Real-time drive-up and reservable vehicle space availability for upcoming Washington State Ferries departures from a terminal, broken down by sailing and arrival terminal.

#### Identity

Each event identifies the real-world resource with `{terminal_id}`. `{terminal_id}` is washington State Ferries terminal identifier (stable). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wsdot`, key `{terminal_id}` |
| `MQTT/5.0` | topic `traffic/us/wsdot/wsdot/ferry-terminals/{terminal_id}/sailing-space`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{terminal_id}` |

#### Payload

`Terminal Sailing Space` payloads are JSON object. Required fields: `terminal_id`, `terminal_subject_id`, `region_id`, `terminal_name`, `terminal_abbrev`, `sort_seq`, `departing_spaces`, `is_no_fare_collected`, `no_fare_collected_msg`.

- **`terminal_id`** (string, required): Washington State Ferries terminal identifier (stable).
- **`terminal_subject_id`** (int32 or null, required): WSF terminal subject identifier.
- **`region_id`** (int32 or null, required): WSF region identifier.
- **`terminal_name`** (string or null, required): Terminal name.
- **`terminal_abbrev`** (string or null, required): Terminal abbreviation code.
- **`sort_seq`** (int32 or null, required): WSF display sort sequence.
- **`departing_spaces`** (array of object, required): Upcoming departures from this terminal with per-sailing vehicle space availability.
- **`is_no_fare_collected`** (boolean or null, required): Whether no fare is collected at this terminal for the relevant sailings, or null when not applicable.
- **`no_fare_collected_msg`** (string or null, required): Message explaining the no-fare-collected status, or null.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "terminal_id": "string",
  "terminal_subject_id": 0,
  "region_id": 0,
  "terminal_name": "string",
  "terminal_abbrev": "string",
  "sort_seq": 0,
  "departing_spaces": [
    {
      "departure": "string",
      "is_cancelled": false,
      "vessel_id": 0,
      "vessel_name": "string",
      "max_space_count": 0,
      "space_for_arrival_terminals": [
        {
          "terminal_id": 0,
          "terminal_name": "string",
          "vessel_id": 0,
          "vessel_name": "string",
          "display_reservable_space": false,
          "reservable_space_count": 0,
          "reservable_space_hex_color": "string",
          "display_drive_up_space": false,
          "drive_up_space_count": 0,
          "drive_up_space_hex_color": "string",
          "max_space_count": 0,
          "arrival_terminal_ids": [
            0
          ]
        }
      ]
    }
  ],
  "is_no_fare_collected": false,
  "no_fare_collected_msg": "string"
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

## References

- xRegistry manifest: [`xreg/wsdot.xreg.json`](xreg/wsdot.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Washington State DOT traveler and ferry APIs: <https://www.wsdot.wa.gov/traffic/api/>
