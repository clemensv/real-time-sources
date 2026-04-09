# NDW Netherlands Road Traffic Events

The bridge emits CloudEvents in structured JSON format to Kafka-compatible
endpoints.

## Topics and Keys

| Topic | Key template | Message group | Event types |
|---|---|---|---|
| `ndl-traffic` | `{site_id}` | `NL.NDW.Traffic.Measurements` | `TrafficSpeed`, `TravelTime` |
| `ndl-traffic-situations` | `{situation_id}` | `NL.NDW.Traffic.Situations` | `TrafficSituation` |

## Event Types

### NL.NDW.Traffic.TrafficSpeed

Aggregated traffic speed and flow measurement per road segment from the NDW
DATEX II trafficspeed feed. Speed is averaged and flow summed across all
reporting lanes.

| Field | Type | Description |
|---|---|---|
| `site_id` | string | NDW measurement site ID |
| `measurement_time` | string (ISO 8601) | Measurement timestamp (UTC) |
| `average_speed` | double \| null | Average speed in km/h across valid lanes |
| `vehicle_flow_rate` | int \| null | Total flow in vehicles/hour |
| `number_of_lanes_with_data` | int | Lanes with valid data |

### NL.NDW.Traffic.TravelTime

Travel time measurement per road segment from the NDW DATEX II traveltime feed.

| Field | Type | Description |
|---|---|---|
| `site_id` | string | NDW measurement site ID |
| `measurement_time` | string (ISO 8601) | Measurement timestamp (UTC) |
| `duration` | double \| null | Actual travel time in seconds |
| `reference_duration` | double \| null | Free-flow reference time in seconds |
| `accuracy` | double \| null | Measurement accuracy (0–100%) |
| `data_quality` | double \| null | Supplier data quality score (0–100%) |
| `number_of_input_values` | int \| null | Vehicle count used in calculation |

### NL.NDW.Traffic.TrafficSituation

Current traffic situation from the NDW DATEX II v3 actueel_beeld feed.

| Field | Type | Description |
|---|---|---|
| `situation_id` | string | Situation ID |
| `version_time` | string (ISO 8601) | Last version timestamp (UTC) |
| `severity` | string \| null | low, medium, high, highest, unknown |
| `record_type` | string \| null | DATEX II record type |
| `cause_type` | string \| null | Cause (roadMaintenance, accident, etc.) |
| `start_time` | string \| null | Validity start (ISO 8601) |
| `end_time` | string \| null | Validity end (ISO 8601) |
| `information_status` | string | real, test, or exercise |
