# NDW Road Traffic Events

NDW Road Traffic publishes traffic flow, signs, travel-time, and situation updates from the Dutch National Data Warehouse for Traffic Information (NDW) for Dutch road network measurement sites and situations. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 13 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 13 telemetry event types.
- **Identity:** `measurement-sites/{measurement_site_id}`, `drips/{vms_controller_id}/{vms_index}`, `msi-signs/{sign_id}`, `situations/{situation_record_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `ndw-road-traffic`. The record key is `measurement-sites/{measurement_site_id}`, `drips/{vms_controller_id}/{vms_index}`, `msi-signs/{sign_id}`, `situations/{situation_record_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['ndw-road-traffic'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Point Measurement Site

CloudEvents type: `NL.NDW.AVG.PointMeasurementSite`

#### What it tells you

Reference record for a point measurement site from the Dutch NDW DATEX II measurement_current feed. Contains location, sensor technology type, and lane configuration for a fixed inductive-loop or microwave sensor.

#### Identity

Each event identifies the real-world resource with `measurement-sites/{measurement_site_id}`. `{measurement_site_id}` is unique identifier of the NDW measurement site, from the DATEX II measurementSiteRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `measurement-sites/{measurement_site_id}` |

#### Payload

`Point Measurement Site` payloads are JSON object. Required fields: `measurement_site_id`.

- **`measurement_site_id`** (string, required): Unique identifier of the NDW measurement site, from the DATEX II measurementSiteRecord id attribute. Example: RWS01_MST_0001-01.
- **`name`** (string or null, optional): Human-readable name of the measurement site from the DATEX II measurementSiteName element.
- **`measurement_site_type`** (string or null, optional): Sensor technology type used at this measurement site, from the DATEX II measurementEquipmentTypeUsed element. Example values: inductionLoop, microwave.
- **`period`** (int32 or null, optional, s): Measurement aggregation period in seconds, from the DATEX II measurementSpecificCharacteristics period element.
- **`latitude`** (double or null, optional, deg): WGS84 latitude of the measurement point in decimal degrees, from the DATEX II pointByCoordinates/pointCoordinates/latitude element.
- **`longitude`** (double or null, optional, deg): WGS84 longitude of the measurement point in decimal degrees, from the DATEX II pointByCoordinates/pointCoordinates/longitude element.
- **`road_name`** (string or null, optional): Road identifier on which the sensor is located, from the DATEX II roadInformation/roadName element. Example values: A1, N205.
- **`lane_count`** (int32 or null, optional): Number of lanes monitored at this measurement site, derived from the number of measurementSpecificCharacteristics elements.
- **`carriageway_type`** (string or null, optional): Carriageway type from the DATEX II carriagewayType element. Example values: mainCarriageway, slipRoad, connectingCarriageway.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "measurement_site_id": "string",
  "name": "string",
  "measurement_site_type": "string",
  "period": 0,
  "latitude": 0,
  "longitude": 0,
  "road_name": "string",
  "lane_count": 0,
  "carriageway_type": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Route Measurement Site

CloudEvents type: `NL.NDW.AVG.RouteMeasurementSite`

#### What it tells you

Reference record for a route (section) measurement site from the Dutch NDW DATEX II measurement_current feed. Covers a road segment between two coordinates used for travel time computation.

#### Identity

Each event identifies the real-world resource with `measurement-sites/{measurement_site_id}`. `{measurement_site_id}` is unique identifier of the NDW route measurement site, from the DATEX II measurementSiteRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `measurement-sites/{measurement_site_id}` |

#### Payload

`Route Measurement Site` payloads are JSON object. Required fields: `measurement_site_id`.

- **`measurement_site_id`** (string, required): Unique identifier of the NDW route measurement site, from the DATEX II measurementSiteRecord id attribute.
- **`name`** (string or null, optional): Human-readable name of the route measurement site from the DATEX II measurementSiteName element.
- **`measurement_site_type`** (string or null, optional): Measurement method type, from the DATEX II measurementEquipmentTypeUsed element. Example values: detectLoop, floatingCar.
- **`period`** (int32 or null, optional, s): Measurement aggregation period in seconds, from the DATEX II measurementSpecificCharacteristics period element.
- **`start_latitude`** (double or null, optional, deg): WGS84 latitude of the route start point in decimal degrees.
- **`start_longitude`** (double or null, optional, deg): WGS84 longitude of the route start point in decimal degrees.
- **`end_latitude`** (double or null, optional, deg): WGS84 latitude of the route end point in decimal degrees.
- **`end_longitude`** (double or null, optional, deg): WGS84 longitude of the route end point in decimal degrees.
- **`road_name`** (string or null, optional): Road identifier for the route section. Example values: A1, A10, N44.
- **`length_metres`** (double or null, optional, m): Length of the route section in metres, from the DATEX II length element.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "measurement_site_id": "string",
  "name": "string",
  "measurement_site_type": "string",
  "period": 0,
  "start_latitude": 0,
  "start_longitude": 0,
  "end_latitude": 0,
  "end_longitude": 0,
  "road_name": "string",
  "length_metres": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Traffic Observation

CloudEvents type: `NL.NDW.AVG.TrafficObservation`

#### What it tells you

Aggregated traffic speed and flow observation from the Dutch NDW DATEX II trafficspeed feed. Each record represents one measurement site with speed averaged and flow summed across all reporting lanes.

#### Identity

Each event identifies the real-world resource with `measurement-sites/{measurement_site_id}`. `{measurement_site_id}` is unique identifier of the NDW measurement site, from the DATEX II measurementSiteReference id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `measurement-sites/{measurement_site_id}` |

#### Payload

`Traffic Observation` payloads are JSON object. Required fields: `measurement_site_id`, `measurement_time`, `number_of_lanes_with_data`.

- **`measurement_site_id`** (string, required): Unique identifier of the NDW measurement site, from the DATEX II measurementSiteReference id attribute.
- **`measurement_time`** (string, required): Timestamp of the measurement in ISO 8601 UTC format, from the DATEX II measurementTimeDefault element.
- **`average_speed`** (double or null, optional, km/h): Average vehicle speed in km/h across all lanes with valid data at this site. Null when no lane reported a valid speed.
- **`vehicle_flow_rate`** (int32 or null, optional, vehicles/h): Total vehicle flow rate in vehicles per hour, summed across all lanes at this measurement site. Null when no valid flow data was reported.
- **`number_of_lanes_with_data`** (int32, required): Number of lanes that reported valid measurement data at this measurement site.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "measurement_site_id": "string",
  "measurement_time": "string",
  "average_speed": 0,
  "vehicle_flow_rate": 0,
  "number_of_lanes_with_data": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Travel Time Observation

CloudEvents type: `NL.NDW.AVG.TravelTimeObservation`

#### What it tells you

Travel time observation for a road segment from the Dutch NDW DATEX II traveltime feed. Contains the actual measured travel time and the static free-flow reference time for a route measurement site.

#### Identity

Each event identifies the real-world resource with `measurement-sites/{measurement_site_id}`. `{measurement_site_id}` is unique identifier of the NDW route measurement site, from the DATEX II measurementSiteReference id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `measurement-sites/{measurement_site_id}` |

#### Payload

`Travel Time Observation` payloads are JSON object. Required fields: `measurement_site_id`, `measurement_time`.

- **`measurement_site_id`** (string, required): Unique identifier of the NDW route measurement site, from the DATEX II measurementSiteReference id attribute.
- **`measurement_time`** (string, required): Timestamp of the measurement in ISO 8601 UTC format, from the DATEX II measurementTimeDefault element.
- **`duration`** (double or null, optional, s): Measured travel time in seconds for the route section, from the DATEX II travelTime/duration element. Null if the upstream value was negative (invalid).
- **`reference_duration`** (double or null, optional, s): Free-flow reference travel time in seconds for the route section, from the DATEX II basicDataReferenceValue/travelTimeData/travelTime/duration extension element. Null if not provided.
- **`accuracy`** (double or null, optional, %): Accuracy percentage of the travel time measurement as a value between 0 and 100, from the DATEX II travelTime accuracy attribute.
- **`data_quality`** (double or null, optional, %): Supplier-calculated data quality score as a value between 0 and 100, from the DATEX II supplierCalculatedDataQuality attribute.
- **`number_of_input_values`** (int32 or null, optional): Number of input observations used to compute the travel time, from the DATEX II numberOfInputValuesUsed attribute.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "measurement_site_id": "string",
  "measurement_time": "string",
  "duration": 0,
  "reference_duration": 0,
  "accuracy": 0,
  "data_quality": 0,
  "number_of_input_values": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Drip Sign

CloudEvents type: `NL.NDW.DRIP.DripSign`

#### What it tells you

Reference record for a Dynamic Route Information Panel (DRIP) sign from the Dutch NDW DATEX II dynamische_route_informatie_paneel feed. Describes the physical installation, location, and type of an individual VMS sign unit.

#### Identity

Each event identifies the real-world resource with `drips/{vms_controller_id}/{vms_index}`. `{vms_controller_id}` is unique identifier of the VMS controller unit, from the DATEX II vmsUnitRecord id attribute; `{vms_index}` is index of the individual VMS sign within the controller unit, from the DATEX II vmsRecord index attribute, converted to string. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `drips/{vms_controller_id}/{vms_index}` |

#### Payload

`Drip Sign` payloads are JSON object. Required fields: `vms_controller_id`, `vms_index`.

- **`vms_controller_id`** (string, required): Unique identifier of the VMS controller unit, from the DATEX II vmsUnitRecord id attribute.
- **`vms_index`** (string, required): Index of the individual VMS sign within the controller unit, from the DATEX II vmsRecord index attribute, converted to string.
- **`vms_type`** (string or null, optional): DRIP sign type, from the DATEX II vmsType element. Example values: presignalling, matrixBoardTwoByTwo, matrixBoardOneByTwo.
- **`latitude`** (double or null, optional, deg): WGS84 latitude of the DRIP sign location in decimal degrees.
- **`longitude`** (double or null, optional, deg): WGS84 longitude of the DRIP sign location in decimal degrees.
- **`road_name`** (string or null, optional): Road identifier where the DRIP sign is located. Example values: A1, A10.
- **`description`** (string or null, optional): Human-readable description of the DRIP sign from the DATEX II description element.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "vms_controller_id": "string",
  "vms_index": "string",
  "vms_type": "string",
  "latitude": 0,
  "longitude": 0,
  "road_name": "string",
  "description": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Drip Display State

CloudEvents type: `NL.NDW.DRIP.DripDisplayState`

#### What it tells you

Current display state of a Dynamic Route Information Panel (DRIP) sign from the Dutch NDW DATEX II dynamische_route_informatie_paneel feed. Captures the active text, pictogram codes, and operational state of the sign.

#### Identity

Each event identifies the real-world resource with `drips/{vms_controller_id}/{vms_index}`. `{vms_controller_id}` is unique identifier of the VMS controller unit, from the DATEX II vmsUnitRecord id attribute; `{vms_index}` is index of the individual VMS sign within the controller unit, converted to string. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `drips/{vms_controller_id}/{vms_index}` |

#### Payload

`Drip Display State` payloads are JSON object. Required fields: `vms_controller_id`, `vms_index`, `publication_time`.

- **`vms_controller_id`** (string, required): Unique identifier of the VMS controller unit, from the DATEX II vmsUnitRecord id attribute.
- **`vms_index`** (string, required): Index of the individual VMS sign within the controller unit, converted to string.
- **`publication_time`** (string, required): ISO 8601 UTC timestamp when this display state was published, from the DATEX II publicationTime element.
- **`active`** (boolean or null, optional): Whether the DRIP sign is currently displaying content. Derived from the DATEX II vmsWorking or displayActive element.
- **`vms_text`** (string or null, optional): Concatenated text from all display panels of the sign, from the DATEX II displayedText/vmsText/vmsTextLine elements.
- **`pictogram_code`** (string or null, optional): Pictogram code displayed on the sign, from the DATEX II pictogramDisplayAreaSettings/vmsPicktogramDisplayCharacteristics/vmsPicktogramDescription element.
- **`state`** (string or null, optional): Operational state of the DRIP sign, from the DATEX II vmsUnitFault or operationalState element. Example values: working, fault, maintenance.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "vms_controller_id": "string",
  "vms_index": "string",
  "publication_time": "string",
  "active": false,
  "vms_text": "string",
  "pictogram_code": "string",
  "state": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Msi Sign

CloudEvents type: `NL.NDW.MSI.MsiSign`

#### What it tells you

Reference record for a Matrix Signal Installation (MSI) sign from the Dutch NDW DATEX II Matrixsignaalinformatie feed. Describes the physical location, lane assignment, and type of a matrix signal sign above a motorway lane.

#### Identity

Each event identifies the real-world resource with `msi-signs/{sign_id}`. `{sign_id}` is unique identifier of the MSI sign, from the DATEX II vmsUnitRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `msi-signs/{sign_id}` |

#### Payload

`Msi Sign` payloads are JSON object. Required fields: `sign_id`.

- **`sign_id`** (string, required): Unique identifier of the MSI sign, from the DATEX II vmsUnitRecord id attribute.
- **`sign_type`** (string or null, optional): MSI sign type, from the DATEX II vmsType element. Example values: matrixBoardOneByOne, matrixBoardTwoByOne.
- **`latitude`** (double or null, optional, deg): WGS84 latitude of the MSI sign location in decimal degrees.
- **`longitude`** (double or null, optional, deg): WGS84 longitude of the MSI sign location in decimal degrees.
- **`road_name`** (string or null, optional): Road identifier where the MSI sign is located. Example values: A1, A2.
- **`lane`** (string or null, optional): Lane designation above which the MSI sign is installed, from the DATEX II laneNumber element.
- **`description`** (string or null, optional): Human-readable description of the MSI sign installation from the DATEX II description element.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sign_id": "string",
  "sign_type": "string",
  "latitude": 0,
  "longitude": 0,
  "road_name": "string",
  "lane": "string",
  "description": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Msi Display State

CloudEvents type: `NL.NDW.MSI.MsiDisplayState`

#### What it tells you

Current display state of a Matrix Signal Installation (MSI) sign from the Dutch NDW DATEX II Matrixsignaalinformatie feed. Captures the displayed image code, operational state, and any speed limit shown.

#### Identity

Each event identifies the real-world resource with `msi-signs/{sign_id}`. `{sign_id}` is unique identifier of the MSI sign, from the DATEX II vmsUnitRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `msi-signs/{sign_id}` |

#### Payload

`Msi Display State` payloads are JSON object. Required fields: `sign_id`, `publication_time`.

- **`sign_id`** (string, required): Unique identifier of the MSI sign, from the DATEX II vmsUnitRecord id attribute.
- **`publication_time`** (string, required): ISO 8601 UTC timestamp when this display state was published, from the DATEX II publicationTime element.
- **`image_code`** (string or null, optional): Code of the image currently displayed on the MSI sign, from the DATEX II imageCode or displayedText element. Example values: blank, closed, 70, 80, 100, arrow_left.
- **`state`** (string or null, optional): Operational state derived from the displayed image. Example values: open, closed, speed_limit.
- **`speed_limit`** (int32 or null, optional, km/h): Speed limit in km/h displayed on the sign when showing a speed limit image. Null when the sign is blank or shows a non-numeric image.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "sign_id": "string",
  "publication_time": "string",
  "image_code": "string",
  "state": "string",
  "speed_limit": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Roadwork

CloudEvents type: `NL.NDW.Situations.Roadwork`

#### What it tells you

Road construction or maintenance work event from the Dutch NDW DATEX II planningsfeed_wegwerkzaamheden_en_evenementen feed. Represents a planned or active roadwork situation on the Dutch national road network.

#### Identity

Each event identifies the real-world resource with `situations/{situation_record_id}`. `{situation_record_id}` is unique identifier of the situation record, from the DATEX II situationRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `situations/{situation_record_id}` |

#### Payload

`Roadwork` payloads are JSON object. Required fields: `situation_record_id`, `version_time`.

- **`situation_record_id`** (string, required): Unique identifier of the situation record, from the DATEX II situationRecord id attribute.
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element.
- **`validity_status`** (string or null, optional): Validity status of the situation record, from the DATEX II validityStatus element. Example values: active, suspended, definedByValidityTimeSpec.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp when the roadwork validity period starts, from the DATEX II overallStartTime element.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp when the roadwork validity period ends, from the DATEX II overallEndTime element. Null for open-ended situations.
- **`road_name`** (string or null, optional): Road name or identifier where the roadwork is located.
- **`description`** (string or null, optional): Human-readable description of the roadwork situation from the DATEX II comment or description element.
- **`location_description`** (string or null, optional): Human-readable description of the roadwork location from the DATEX II locationDescriptor element.
- **`probability`** (string or null, optional): Probability of occurrence for the roadwork, from the DATEX II probabilityOfOccurrence element. Example values: certain, probable, risk.
- **`severity`** (string or null, optional): Overall severity of the roadwork impact, from the DATEX II severity element. Example values: highest, high, medium, low, lowest.
- **`management_type`** (string or null, optional): Type of road management applied, from the DATEX II roadMaintenanceType or managementType element. Example values: laneClosures, carriagewayClosure.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_record_id": "string",
  "version_time": "string",
  "validity_status": "string",
  "start_time": "string",
  "end_time": "string",
  "road_name": "string",
  "description": "string",
  "location_description": "string",
  "probability": "string",
  "severity": "string",
  "management_type": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Bridge Opening

CloudEvents type: `NL.NDW.Situations.BridgeOpening`

#### What it tells you

Bridge opening event from the Dutch NDW DATEX II planningsfeed_brugopeningen feed. Represents a scheduled or active bridge opening that causes temporary road closure.

#### Identity

Each event identifies the real-world resource with `situations/{situation_record_id}`. `{situation_record_id}` is unique identifier of the situation record, from the DATEX II situationRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `situations/{situation_record_id}` |

#### Payload

`Bridge Opening` payloads are JSON object. Required fields: `situation_record_id`, `version_time`.

- **`situation_record_id`** (string, required): Unique identifier of the situation record, from the DATEX II situationRecord id attribute.
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element.
- **`validity_status`** (string or null, optional): Validity status of the bridge opening record from the DATEX II validityStatus element.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp when the bridge opening starts.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp when the bridge opening ends and the road reopens.
- **`bridge_name`** (string or null, optional): Name of the bridge being opened, from the DATEX II bridgeName or locationName element.
- **`road_name`** (string or null, optional): Road identifier that is affected by the bridge opening.
- **`description`** (string or null, optional): Human-readable description of the bridge opening event from the DATEX II comment or description element.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_record_id": "string",
  "version_time": "string",
  "validity_status": "string",
  "start_time": "string",
  "end_time": "string",
  "bridge_name": "string",
  "road_name": "string",
  "description": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Temporary Closure

CloudEvents type: `NL.NDW.Situations.TemporaryClosure`

#### What it tells you

Temporary road closure from the Dutch NDW DATEX II tijdelijke_verkeersmaatregelen_afsluitingen feed. Represents a temporary closure of a road section or lane on the Dutch national road network.

#### Identity

Each event identifies the real-world resource with `situations/{situation_record_id}`. `{situation_record_id}` is unique identifier of the situation record, from the DATEX II situationRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `situations/{situation_record_id}` |

#### Payload

`Temporary Closure` payloads are JSON object. Required fields: `situation_record_id`, `version_time`.

- **`situation_record_id`** (string, required): Unique identifier of the situation record, from the DATEX II situationRecord id attribute.
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element.
- **`validity_status`** (string or null, optional): Validity status of the temporary closure record from the DATEX II validityStatus element.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp when the temporary closure starts.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp when the temporary closure ends.
- **`road_name`** (string or null, optional): Road identifier where the temporary closure applies.
- **`description`** (string or null, optional): Human-readable description of the temporary closure from the DATEX II comment or description element.
- **`location_description`** (string or null, optional): Human-readable description of the closure location from the DATEX II locationDescriptor element.
- **`severity`** (string or null, optional): Overall severity of the closure impact, from the DATEX II severity element.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_record_id": "string",
  "version_time": "string",
  "validity_status": "string",
  "start_time": "string",
  "end_time": "string",
  "road_name": "string",
  "description": "string",
  "location_description": "string",
  "severity": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Temporary Speed Limit

CloudEvents type: `NL.NDW.Situations.TemporarySpeedLimit`

#### What it tells you

Temporary speed limit measure from the Dutch NDW DATEX II tijdelijke_verkeersmaatregelen_maximum_snelheden feed. Represents a temporary reduction in maximum speed on a section of the national road network.

#### Identity

Each event identifies the real-world resource with `situations/{situation_record_id}`. `{situation_record_id}` is unique identifier of the situation record, from the DATEX II situationRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `situations/{situation_record_id}` |

#### Payload

`Temporary Speed Limit` payloads are JSON object. Required fields: `situation_record_id`, `version_time`.

- **`situation_record_id`** (string, required): Unique identifier of the situation record, from the DATEX II situationRecord id attribute.
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element.
- **`validity_status`** (string or null, optional): Validity status of the temporary speed limit record from the DATEX II validityStatus element.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp when the temporary speed limit starts.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp when the temporary speed limit ends.
- **`road_name`** (string or null, optional): Road identifier where the temporary speed limit applies.
- **`speed_limit_kmh`** (int32 or null, optional, km/h): Temporary maximum speed limit in km/h, from the DATEX II speedLimit/maximumSpeedLimit element.
- **`description`** (string or null, optional): Human-readable description of the temporary speed limit from the DATEX II comment or description element.
- **`location_description`** (string or null, optional): Human-readable description of the speed limit section location from the DATEX II locationDescriptor element.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_record_id": "string",
  "version_time": "string",
  "validity_status": "string",
  "start_time": "string",
  "end_time": "string",
  "road_name": "string",
  "speed_limit_kmh": 0,
  "description": "string",
  "location_description": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Safety Related Message

CloudEvents type: `NL.NDW.Situations.SafetyRelatedMessage`

#### What it tells you

Safety-related traffic information message from the Dutch NDW DATEX II veiligheidsgerelateerde_berichten_srti feed. Contains urgent safety alerts and hazard notifications on the national road network.

#### Identity

Each event identifies the real-world resource with `situations/{situation_record_id}`. `{situation_record_id}` is unique identifier of the situation record, from the DATEX II situationRecord id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndw-road-traffic`, key `situations/{situation_record_id}` |

#### Payload

`Safety Related Message` payloads are JSON object. Required fields: `situation_record_id`, `version_time`.

- **`situation_record_id`** (string, required): Unique identifier of the situation record, from the DATEX II situationRecord id attribute.
- **`version_time`** (string, required): ISO 8601 UTC timestamp when this situation record version was created, from the DATEX II situationVersionTime element.
- **`validity_status`** (string or null, optional): Validity status of the safety message record from the DATEX II validityStatus element.
- **`start_time`** (string or null, optional): ISO 8601 UTC timestamp when the safety-related situation starts.
- **`end_time`** (string or null, optional): ISO 8601 UTC timestamp when the safety-related situation ends.
- **`road_name`** (string or null, optional): Road identifier where the safety-related event is located.
- **`message_type`** (string or null, optional): Type of safety-related message, from the DATEX II xsi:type attribute on the situationRecord. Example values: RoadOrCarriagewayOrLaneManagement, VehicleObstruction, PoorRoadInfrastructure.
- **`description`** (string or null, optional): Human-readable description of the safety-related message from the DATEX II comment or description element.
- **`urgency`** (string or null, optional): Urgency level of the safety message, from the DATEX II urgency element. Example values: extremelyUrgent, urgent, normalUrgency.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_record_id": "string",
  "version_time": "string",
  "validity_status": "string",
  "start_time": "string",
  "end_time": "string",
  "road_name": "string",
  "message_type": "string",
  "description": "string",
  "urgency": "string"
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
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/ndw-road-traffic.xreg.json`](xreg/ndw-road-traffic.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- https://opendata.ndw.nu/: <https://opendata.ndw.nu/>
