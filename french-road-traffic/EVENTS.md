# French Road Traffic — Events

This document describes the CloudEvents emitted by the French Road Traffic bridge.

## Event Types

### `fr.gouv.transport.bison_fute.TrafficFlowMeasurement`

Real-time traffic flow and speed measurement from a DATEX II measurement site
on the French national non-conceded road network. Published by Bison Futé
(TIPI) as a MeasuredDataPublication snapshot every 6 minutes.

**Kafka topic**: `french-road-traffic-flow`
**Kafka key**: `{site_id}`
**CloudEvents subject**: `{site_id}`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `site_id` | string | Yes | Unique identifier of the DATEX II measurement site record (e.g. `MUM76.h1`) |
| `measurement_time` | string | Yes | ISO 8601 timestamp of the measurement |
| `vehicle_flow_rate` | int or null | No | Vehicles per hour at the measurement site |
| `average_speed` | double or null | No | Average speed in km/h |
| `input_values_flow` | int or null | No | Number of vehicle observations for flow |
| `input_values_speed` | int or null | No | Number of vehicle observations for speed |

### `fr.gouv.transport.bison_fute.RoadEvent`

Real-time road situation record from the French national non-conceded road
network DATEX II SituationPublication feed. Each record represents a traffic
incident, construction works, lane management, or other event.

**Kafka topic**: `french-road-traffic-events`
**Kafka key**: `{situation_id}`
**CloudEvents subject**: `{situation_id}`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `situation_id` | string | Yes | DATEX II situation identifier |
| `record_id` | string | Yes | Situation record identifier |
| `version` | string | Yes | Version of the situation |
| `severity` | string or null | No | Overall severity (low, medium, high, highest) |
| `record_type` | string | Yes | DATEX II type (Accident, ConstructionWorks, etc.) |
| `probability` | string or null | No | Probability of occurrence |
| `latitude` | double or null | No | WGS84 latitude |
| `longitude` | double or null | No | WGS84 longitude |
| `road_number` | string or null | No | Road identifier (e.g. N20, A10) |
| `town_name` | string or null | No | Nearest town name |
| `direction` | string or null | No | Traffic direction (bothWays, positive, negative) |
| `description` | string or null | No | Event description |
| `location_description` | string or null | No | Location description |
| `source_name` | string or null | No | Publishing organization |
| `validity_status` | string or null | No | Validity status |
| `overall_start_time` | string or null | No | ISO 8601 validity start |
| `overall_end_time` | string or null | No | ISO 8601 validity end |
| `creation_time` | string | Yes | ISO 8601 creation timestamp |
| `observation_time` | string or null | No | ISO 8601 last observation |

### Known Record Types

- `Accident`
- `AbnormalTraffic`
- `ConstructionWorks`
- `MaintenanceWorks`
- `RoadOrCarriagewayOrLaneManagement`
- `EnvironmentalObstruction`
- `GeneralObstruction`
- `VehicleObstruction`
- `AnimalPresenceObstruction`
- `InfrastructureDamageObstruction`
- `GeneralNetworkManagement`
- `ReroutingManagement`
- `SpeedManagement`
- `WeatherRelatedRoadConditions`
- `OperatorAction`
- `GeneralInstructionOrMessageToRoadUsers`
- `RoadsideServiceDisruption`
