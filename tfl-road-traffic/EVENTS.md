# TfL Road Traffic – Event Reference

This document describes the CloudEvents emitted by the TfL Road Traffic bridge.

All events use the `application/cloudevents+json` content type (structured mode) and are written to the `tfl-road-traffic` Kafka topic.

---

## Event: `uk.gov.tfl.road.RoadCorridor`

**Source:** `https://api.tfl.gov.uk/Road`  
**Subject:** `roads/{road_id}`  
**Kafka key:** `roads/{road_id}`  
**Category:** Reference data  
**Description:** Reference record for a Transport for London (TfL) managed road corridor. Emitted at bridge startup from the GET /Road endpoint and refreshed periodically (default: every hour). Each corridor is a named road segment under TfL operational control, such as the A2, A12, or M25.

### Schema

| Field | Type | Description |
|---|---|---|
| `road_id` | `string` | Unique identifier for the road corridor (e.g. `a2`, `a12`, `m25`). Upstream field: `id`. |
| `display_name` | `string` | Human-readable display name (e.g. `A2`, `A12`, `M25`). Upstream field: `displayName`. |
| `status_severity` | `string\|null` | Current aggregate status severity (e.g. `Good`, `Moderate`, `Serious`). Upstream field: `statusSeverity`. |
| `status_severity_description` | `string\|null` | Human-readable description of the current status (e.g. `Serious Delays`). Upstream field: `statusSeverityDescription`. |
| `bounds` | `string\|null` | Bounding box as a JSON array string in WGS84. |
| `envelope` | `string\|null` | GeoJSON envelope polygon for the corridor geometry. |
| `url` | `string\|null` | TfL API detail URL for this corridor. |
| `status_aggregation_start_date` | `datetime\|null` | Start of the current status aggregation period. Upstream field: `statusAggregationStartDate`. |
| `status_aggregation_end_date` | `datetime\|null` | End of the current status aggregation period. Upstream field: `statusAggregationEndDate`. |

---

## Event: `uk.gov.tfl.road.RoadStatus`

**Source:** `https://api.tfl.gov.uk/Road/all/Status`  
**Subject:** `roads/{road_id}`  
**Kafka key:** `roads/{road_id}`  
**Category:** Telemetry  
**Description:** Real-time status snapshot for a TfL managed road corridor. Fetched from the GET /Road/all/Status endpoint on each polling cycle. Each event represents the current aggregate traffic status for one corridor as computed by TfL from active disruptions.

### Schema

Same fields as `uk.gov.tfl.road.RoadCorridor` above.

---

## Event: `uk.gov.tfl.road.RoadDisruption`

**Source:** `https://api.tfl.gov.uk/Road/all/Disruption`  
**Subject:** `disruptions/{disruption_id}`  
**Kafka key:** `disruptions/{disruption_id}`  
**Category:** Telemetry  
**Description:** Real-time road disruption event on the TfL road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure. Events are deduped by `id` + `lastModifiedTime` so only new or changed disruptions are re-emitted.

### Schema

| Field | Type | Description |
|---|---|---|
| `disruption_id` | `string` | TfL TIMS disruption identifier (e.g. `TIMS-12345`). Upstream field: `id`. |
| `category` | `string\|null` | Top-level category (`RealTime`, `PlannedWork`). |
| `sub_category` | `string\|null` | Sub-category (e.g. `Incident`, `Utility works`). Upstream field: `subCategory`. |
| `severity` | `string\|null` | Severity level (`Serious`, `Moderate`, `Minimal`, `Severe`). |
| `ordinal` | `int32\|null` | Ordinal rank within a severity level. |
| `url` | `string\|null` | TfL API detail URL for this disruption. |
| `point` | `string\|null` | Representative WKT point location. |
| `comments` | `string\|null` | Free-text context comments. |
| `current_update` | `string\|null` | Latest operator update text. Upstream field: `currentUpdate`. |
| `current_update_datetime` | `datetime\|null` | Timestamp of the latest update. Upstream field: `currentUpdateDateTime`. |
| `corridor_ids` | `array\|null` | Affected road corridor identifiers (e.g. `["a2"]`). Upstream field: `corridorIds`. |
| `start_datetime` | `datetime\|null` | Start date/time of the disruption. Upstream field: `startDateTime`. |
| `end_datetime` | `datetime\|null` | End date/time of the disruption (null for open-ended incidents). Upstream field: `endDateTime`. |
| `last_modified_time` | `datetime\|null` | Last modification timestamp in TfL system. Used for deduplication. Upstream field: `lastModifiedTime`. |
| `level_of_interest` | `string\|null` | Public interest level (`Low`, `Medium`, `High`). Upstream field: `levelOfInterest`. |
| `location` | `string\|null` | Free-text location description. |
| `is_provisional` | `boolean\|null` | Whether details are provisional. Upstream field: `isProvisional`. |
| `has_closures` | `boolean\|null` | Whether the disruption includes road closures. Upstream field: `hasClosures`. |
| `streets` | `array\|null` | Array of affected street segments (see Street schema below). |
| `geography` | `string\|null` | GeoJSON geometry as a JSON string. |
| `geometry` | `string\|null` | Secondary database geometry as a JSON string. |
| `status` | `string\|null` | Lifecycle status of the disruption. |
| `is_active` | `boolean\|null` | Whether the disruption is currently active. Upstream field: `isActive`. |

### Street Object (within `streets` array)

| Field | Type | Description |
|---|---|---|
| `name` | `string\|null` | Street name. |
| `closure` | `string\|null` | Closure type (`Full`, `Partial`). |
| `directions` | `string\|null` | Affected travel directions. |
| `source_system_id` | `string\|null` | Source system identifier. Upstream field: `sourceSystemId`. |
| `source_system_key` | `string\|null` | Source system key. Upstream field: `sourceSystemKey`. |
