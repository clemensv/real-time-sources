# NDW Road Traffic Events

## NL.NDW.AVG.PointMeasurementSite

Reference metadata for a fixed-point sensor measurement site. Emitted at startup and refreshed hourly.

**CloudEvent type**: `NL.NDW.AVG.PointMeasurementSite`  
**Subject / Kafka key**: `measurement-sites/{measurement_site_id}`

| Field | Type | Description |
|-------|------|-------------|
| `measurement_site_id` | string (required) | Unique site identifier |
| `name` | string\|null | Human-readable site name |
| `measurement_site_type` | string\|null | Sensor technology type |
| `period` | int32\|null | Aggregation period in seconds |
| `latitude` | double\|null | WGS84 latitude |
| `longitude` | double\|null | WGS84 longitude |
| `road_name` | string\|null | Road identifier (e.g. A1) |
| `lane_count` | int32\|null | Number of monitored lanes |
| `carriageway_type` | string\|null | Carriageway type |

## NL.NDW.AVG.RouteMeasurementSite

Reference metadata for a route (section) measurement site. Emitted at startup and refreshed hourly.

**CloudEvent type**: `NL.NDW.AVG.RouteMeasurementSite`  
**Subject / Kafka key**: `measurement-sites/{measurement_site_id}`

| Field | Type | Description |
|-------|------|-------------|
| `measurement_site_id` | string (required) | Unique site identifier |
| `name` | string\|null | Human-readable site name |
| `measurement_site_type` | string\|null | Measurement method type |
| `period` | int32\|null | Aggregation period in seconds |
| `start_latitude` | double\|null | Route start latitude |
| `start_longitude` | double\|null | Route start longitude |
| `end_latitude` | double\|null | Route end latitude |
| `end_longitude` | double\|null | Route end longitude |
| `road_name` | string\|null | Road identifier |
| `length_metres` | double\|null | Route section length in metres |

## NL.NDW.AVG.TrafficObservation

Live traffic speed and flow measurement. Updated approximately every minute.

**CloudEvent type**: `NL.NDW.AVG.TrafficObservation`  
**Subject / Kafka key**: `measurement-sites/{measurement_site_id}`

| Field | Type | Description |
|-------|------|-------------|
| `measurement_site_id` | string (required) | Measurement site identifier |
| `measurement_time` | string (required) | ISO 8601 UTC timestamp |
| `average_speed` | double\|null | Average speed in km/h |
| `vehicle_flow_rate` | int32\|null | Flow rate in vehicles/h |
| `number_of_lanes_with_data` | int32 (required) | Lanes with valid data |

## NL.NDW.AVG.TravelTimeObservation

Live travel time measurement. Updated approximately every minute.

**CloudEvent type**: `NL.NDW.AVG.TravelTimeObservation`  
**Subject / Kafka key**: `measurement-sites/{measurement_site_id}`

| Field | Type | Description |
|-------|------|-------------|
| `measurement_site_id` | string (required) | Route measurement site identifier |
| `measurement_time` | string (required) | ISO 8601 UTC timestamp |
| `duration` | double\|null | Measured travel time in seconds |
| `reference_duration` | double\|null | Free-flow reference time in seconds |
| `accuracy` | double\|null | Accuracy percentage (0–100) |
| `data_quality` | double\|null | Data quality score (0–100) |
| `number_of_input_values` | int32\|null | Number of input observations |

## NL.NDW.DRIP.DripSign

Reference data for a DRIP (Dynamic Route Information Panel) sign. Emitted at startup and refreshed hourly.

**CloudEvent type**: `NL.NDW.DRIP.DripSign`  
**Subject / Kafka key**: `drips/{vms_controller_id}/{vms_index}`

| Field | Type | Description |
|-------|------|-------------|
| `vms_controller_id` | string (required) | VMS controller unit ID |
| `vms_index` | string (required) | Sign index within controller |
| `vms_type` | string\|null | DRIP sign type |
| `latitude` | double\|null | WGS84 latitude |
| `longitude` | double\|null | WGS84 longitude |
| `road_name` | string\|null | Road identifier |
| `description` | string\|null | Sign description |

## NL.NDW.DRIP.DripDisplayState

Current display state of a DRIP sign.

**CloudEvent type**: `NL.NDW.DRIP.DripDisplayState`  
**Subject / Kafka key**: `drips/{vms_controller_id}/{vms_index}`

| Field | Type | Description |
|-------|------|-------------|
| `vms_controller_id` | string (required) | VMS controller unit ID |
| `vms_index` | string (required) | Sign index |
| `publication_time` | string (required) | ISO 8601 UTC timestamp |
| `active` | boolean\|null | Whether sign is displaying content |
| `vms_text` | string\|null | Displayed text |
| `pictogram_code` | string\|null | Pictogram code |
| `state` | string\|null | Operational state |

## NL.NDW.MSI.MsiSign

Reference data for an MSI (Matrix Signal Installation) sign. Emitted at startup and refreshed hourly.

**CloudEvent type**: `NL.NDW.MSI.MsiSign`  
**Subject / Kafka key**: `msi-signs/{sign_id}`

| Field | Type | Description |
|-------|------|-------------|
| `sign_id` | string (required) | Unique MSI sign ID |
| `sign_type` | string\|null | Sign type |
| `latitude` | double\|null | WGS84 latitude |
| `longitude` | double\|null | WGS84 longitude |
| `road_name` | string\|null | Road identifier |
| `lane` | string\|null | Lane designation |
| `description` | string\|null | Sign description |

## NL.NDW.MSI.MsiDisplayState

Current display state of an MSI lane signal.

**CloudEvent type**: `NL.NDW.MSI.MsiDisplayState`  
**Subject / Kafka key**: `msi-signs/{sign_id}`

| Field | Type | Description |
|-------|------|-------------|
| `sign_id` | string (required) | MSI sign ID |
| `publication_time` | string (required) | ISO 8601 UTC timestamp |
| `image_code` | string\|null | Displayed image code (e.g. 70, blank, closed) |
| `state` | string\|null | Operational state |
| `speed_limit` | int32\|null | Speed limit in km/h when applicable |

## NL.NDW.Situations.Roadwork

Road construction or maintenance work event.

**CloudEvent type**: `NL.NDW.Situations.Roadwork`  
**Subject / Kafka key**: `situations/{situation_record_id}`

## NL.NDW.Situations.BridgeOpening

Bridge opening event causing temporary road closure.

**CloudEvent type**: `NL.NDW.Situations.BridgeOpening`  
**Subject / Kafka key**: `situations/{situation_record_id}`

## NL.NDW.Situations.TemporaryClosure

Temporary road closure.

**CloudEvent type**: `NL.NDW.Situations.TemporaryClosure`  
**Subject / Kafka key**: `situations/{situation_record_id}`

## NL.NDW.Situations.TemporarySpeedLimit

Temporary speed limit measure.

**CloudEvent type**: `NL.NDW.Situations.TemporarySpeedLimit`  
**Subject / Kafka key**: `situations/{situation_record_id}`

## NL.NDW.Situations.SafetyRelatedMessage

Safety-related traffic information message.

**CloudEvent type**: `NL.NDW.Situations.SafetyRelatedMessage`  
**Subject / Kafka key**: `situations/{situation_record_id}`
