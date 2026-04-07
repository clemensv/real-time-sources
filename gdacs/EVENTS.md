# GDACS Disaster Alert Events

This document describes the events emitted by the GDACS Disaster Alert bridge.

- [GDACS.Alerts](#message-group-gdacsalerts)
  - [GDACS.DisasterAlert](#message-gdacsdisasteralert)

---

## Message Group: GDACS.Alerts

---

### Message: GDACS.DisasterAlert

*A disaster alert from the Global Disaster Alert and Coordination System (GDACS), covering earthquakes, tropical cyclones, floods, volcanoes, forest fires, and droughts worldwide.*

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `type` | CloudEvent type | `string` | `True` | `GDACS.DisasterAlert` |
| `source` | Source URI | `string` | `True` | `https://www.gdacs.org` |
| `subject` | Event identity | `uritemplate` | `True` | `{event_type}/{event_id}` |

#### Schema: GDACS.DisasterAlert

| **Field** | **Type** | **Required** | **Description** |
|---|---|---|---|
| `event_type` | `string` | Yes | The type of natural disaster. EQ = Earthquake, TC = Tropical Cyclone, FL = Flood, VO = Volcano, FF = Forest Fire, DR = Drought. |
| `event_id` | `string` | Yes | The unique numeric identifier assigned to the disaster event by GDACS. |
| `alert_level` | `string` | Yes | The overall GDACS alert level: Green (low), Orange (moderate), Red (high impact). |
| `latitude` | `double` | Yes | Latitude of the disaster event epicenter or centroid in decimal degrees (WGS84). |
| `longitude` | `double` | Yes | Longitude of the disaster event epicenter or centroid in decimal degrees (WGS84). |
| `from_date` | `datetime` | Yes | Date and time when the disaster event was first detected or began. |
| `severity_value` | `double` | Yes | Numeric severity measure (magnitude for earthquakes, wind speed for cyclones, etc.). |
| `severity_unit` | `string` | Yes | Unit of measurement for the severity value (M, km/h, m, VEI). |
| `episode_id` | `string?` | No | Identifier for a specific episode within an event. |
| `episode_alert_level` | `string?` | No | Alert level specific to this episode. |
| `episode_alert_score` | `double?` | No | Numeric alert score for this episode (0.0–3.0). |
| `alert_score` | `double?` | No | Overall numeric alert score (0.0–3.0). |
| `event_name` | `string?` | No | Human-readable name (e.g. cyclone name). |
| `country` | `string?` | No | Name of the affected country or countries. |
| `iso3` | `string?` | No | ISO 3166-1 alpha-3 country code(s). |
| `to_date` | `datetime?` | No | Date and time when the event ended or was last observed. |
| `population_value` | `double?` | No | Estimated number of people exposed or affected. |
| `population_unit` | `string?` | No | Unit for the population value. |
| `vulnerability` | `double?` | No | GDACS vulnerability score (0.0–3.0). |
| `bbox_min_lon` | `double?` | No | Minimum longitude of the affected-area bounding box. |
| `bbox_max_lon` | `double?` | No | Maximum longitude of the affected-area bounding box. |
| `bbox_min_lat` | `double?` | No | Minimum latitude of the affected-area bounding box. |
| `bbox_max_lat` | `double?` | No | Maximum latitude of the affected-area bounding box. |
| `severity_text` | `string?` | No | Human-readable severity description. |
| `is_current` | `boolean?` | No | Whether the event is currently ongoing. |
| `version` | `int32?` | No | Version number of the event record, incremented on updates. |
| `description` | `string?` | No | Brief summary of the disaster event. |
| `link` | `string?` | No | URL to the full GDACS event report page. |
| `pub_date` | `datetime?` | No | Date and time when this RSS item was published or last updated. |
