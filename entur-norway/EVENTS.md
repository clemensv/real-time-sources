# Entur Norway Events

## Message Group: `no.entur.journeys`

All journey events share the Kafka topic `entur-norway` and use the key format
`journeys/{operating_day}/{service_journey_id}`.

---

### `no.entur.DatedServiceJourney`

Reference data for a dated service journey in the Norwegian public transport
network. Emitted at startup from the SIRI-ET feed to provide timetable context
for subsequent telemetry events.

**CloudEvents Attributes:**
- `type`: `no.entur.DatedServiceJourney`
- `source`: `https://api.entur.io/realtime/v1/rest/et`
- `subject`: `journeys/{operating_day}/{service_journey_id}`

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `service_journey_id` | string | NeTEx ServiceJourney identifier (DatedVehicleJourneyRef). Example: `RUT:ServiceJourney:1-1234` |
| `operating_day` | string | ISO 8601 date for the operating day (DataFrameRef). Example: `2024-01-01` |
| `line_ref` | string | NeTEx Line reference. Example: `RUT:Line:1` |
| `operator_ref` | string | NeTEx Operator or codespace reference. Example: `RUT` |
| `direction_ref` | string? | Direction reference, e.g. `Outbound` or `Inbound` |
| `vehicle_mode` | string? | SIRI VehicleMode: bus, tram, rail, ferry, metro, water, air, coach, taxi |
| `route_ref` | string? | NeTEx Route reference |
| `published_line_name` | string? | Public-facing line number or name displayed to passengers |
| `external_line_ref` | string? | External line reference |
| `origin_name` | string? | Origin stop or place name for this journey |
| `destination_name` | string? | Destination stop or place name for this journey |
| `data_source` | string? | Operator codespace originating this data record |

---

### `no.entur.EstimatedVehicleJourney`

Real-time estimated timetable update for a vehicle journey from the Entur
SIRI-ET feed. Contains updated arrival and departure times for each stop along
the journey.

**CloudEvents Attributes:**
- `type`: `no.entur.EstimatedVehicleJourney`
- `source`: `https://api.entur.io/realtime/v1/rest/et`
- `subject`: `journeys/{operating_day}/{service_journey_id}`

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `service_journey_id` | string | NeTEx ServiceJourney identifier |
| `operating_day` | string | ISO 8601 date for the operating day |
| `line_ref` | string | NeTEx Line reference |
| `operator_ref` | string | Operator codespace |
| `direction_ref` | string? | Direction reference |
| `vehicle_mode` | string? | Transport mode |
| `published_line_name` | string? | Public-facing line name |
| `route_ref` | string? | NeTEx Route reference |
| `origin_name` | string? | Origin stop name |
| `destination_name` | string? | Destination stop name |
| `is_cancellation` | boolean | True if the entire journey is cancelled |
| `is_extra_journey` | boolean? | True if this is an extra journey not in the timetable |
| `is_complete_stop_sequence` | boolean? | True if EstimatedCalls covers all stops |
| `monitored` | boolean? | True if this journey is actively monitored by an AVL system |
| `data_source` | string? | DataSource codespace |
| `recorded_at_time` | string? | ISO 8601 UTC timestamp when this update was recorded |
| `estimated_calls` | array of EstimatedCall | Stop-level arrival/departure predictions |

**EstimatedCall (nested object):**

| Field | Type | Description |
|---|---|---|
| `stop_point_ref` | string | NSR Quay/StopPoint identifier. Example: `NSR:Quay:1234` |
| `order` | int | Sequence order of this call (1-based) |
| `stop_point_name` | string? | Public stop name |
| `aimed_arrival_time` | string? | Timetabled arrival time (ISO 8601) |
| `expected_arrival_time` | string? | Real-time expected arrival time (ISO 8601) |
| `aimed_departure_time` | string? | Timetabled departure time (ISO 8601) |
| `expected_departure_time` | string? | Real-time expected departure time (ISO 8601) |
| `arrival_status` | string? | SIRI ArrivalStatus: onTime, early, delayed, cancelled, arrived, noReport |
| `departure_status` | string? | SIRI DepartureStatus: onTime, early, delayed, cancelled, departed, noReport |
| `departure_platform_name` | string? | Platform or track identifier for departure |
| `arrival_boarding_activity` | string? | SIRI ArrivalBoardingActivity: boarding, noBoarding, passthru |
| `departure_boarding_activity` | string? | SIRI DepartureBoardingActivity: boarding, noBoarding, passthru |
| `is_cancellation` | boolean? | True if this individual stop is cancelled |
| `is_extra_stop` | boolean? | True if this stop was added (ExtraCall) |

---

### `no.entur.MonitoredVehicleJourney`

Real-time vehicle monitoring update from the Entur SIRI-VM feed. Contains the
current geographic position of a vehicle, its bearing, delay, and occupancy.

**CloudEvents Attributes:**
- `type`: `no.entur.MonitoredVehicleJourney`
- `source`: `https://api.entur.io/realtime/v1/rest/vm`
- `subject`: `journeys/{operating_day}/{service_journey_id}`

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `service_journey_id` | string | NeTEx ServiceJourney identifier |
| `operating_day` | string | ISO 8601 date for the operating day |
| `recorded_at_time` | string | ISO 8601 UTC timestamp from VehicleActivity/RecordedAtTime |
| `line_ref` | string | NeTEx Line reference |
| `operator_ref` | string | Operator codespace |
| `direction_ref` | string? | Direction reference |
| `vehicle_mode` | string? | Transport mode |
| `published_line_name` | string? | Public-facing line name |
| `origin_name` | string? | Origin stop name |
| `destination_name` | string? | Destination stop name |
| `vehicle_ref` | string? | VehicleRef identifier (payload data, not the Kafka key) |
| `latitude` | double? | WGS84 latitude from VehicleLocation |
| `longitude` | double? | WGS84 longitude from VehicleLocation |
| `bearing` | double? | Compass bearing in degrees (0–360) |
| `delay_seconds` | int? | Current delay in seconds, parsed from SIRI Delay ISO 8601 duration |
| `occupancy_status` | string? | OccupancyStatus: full, standingRoomOnly, seatsAvailable, empty, etc. |
| `progress_status` | string? | ProgressStatus: inProgress, notExpected, notRun, cancelled |
| `monitored` | boolean | True if this journey is actively monitored by an AVL system |

---

## Message Group: `no.entur.situations`

All situation events share the Kafka topic `entur-norway` and use the key format
`situations/{situation_number}`.

---

### `no.entur.PtSituationElement`

Real-time transit disruption or service alert from the Entur SIRI-SX feed.

**CloudEvents Attributes:**
- `type`: `no.entur.PtSituationElement`
- `source`: `https://api.entur.io/realtime/v1/rest/sx`
- `subject`: `situations/{situation_number}`

**Schema Fields:**

| Field | Type | Description |
|---|---|---|
| `situation_number` | string | Unique situation identifier (SituationNumber). Example: `RUT:SituationNumber:12345` |
| `version` | string? | Situation version number |
| `creation_time` | string | ISO 8601 UTC creation time (CreationTime) |
| `source_type` | string? | Source type: directReport, email, phone, post, feed, radio, tv, web, pager, text, other |
| `source_name` | string? | Name of originating source or organisation |
| `progress` | string? | Publication progress: open, published, closing, closed |
| `severity` | string? | SIRI Severity: unknown, noImpact, verySlight, slight, normal, severe, verySevere, undefined |
| `keywords` | string? | Space-separated keywords from the SIRI Keywords element |
| `summary` | string? | Short public summary text |
| `description` | string? | Full public description text |
| `validity_periods` | array of ValidityPeriod | Active validity windows |
| `affects_line_refs` | array of string | LineRef values from AffectedLine elements |
| `affects_stop_point_refs` | array of string | StopPointRef values from AffectedStopPoint elements |

**ValidityPeriod (nested object):**

| Field | Type | Description |
|---|---|---|
| `start_time` | string | ISO 8601 UTC start time |
| `end_time` | string? | ISO 8601 UTC end time, null if open-ended |
