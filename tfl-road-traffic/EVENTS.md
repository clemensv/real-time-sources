# TfL Road Traffic Event Reference

CloudEvents emitted by the TfL Road Traffic Kafka and MQTT/UNS feeders.

- [uk.gov.tfl.road.corridors](#message-group-ukgovtflroadcorridors)
  - [uk.gov.tfl.road.RoadCorridor](#message-ukgovtflroadroadcorridor)
  - [uk.gov.tfl.road.RoadStatus](#message-ukgovtflroadroadstatus)
- [uk.gov.tfl.road.disruptions](#message-group-ukgovtflroaddisruptions)
  - [uk.gov.tfl.road.RoadDisruption](#message-ukgovtflroadroaddisruption)
- [uk.gov.tfl.road.mqtt](#message-group-ukgovtflroadmqtt)
  - [uk.gov.tfl.road.mqtt.Roads](#message-ukgovtflroadmqttroads)
  - [uk.gov.tfl.road.mqtt.RoadDisruptionSerious](#message-ukgovtflroadmqttroaddisruptionserious)
  - [uk.gov.tfl.road.mqtt.RoadDisruptionSevere](#message-ukgovtflroadmqttroaddisruptionsevere)
  - [uk.gov.tfl.road.mqtt.RoadDisruptionModerate](#message-ukgovtflroadmqttroaddisruptionmoderate)
  - [uk.gov.tfl.road.mqtt.RoadDisruptionMinor](#message-ukgovtflroadmqttroaddisruptionminor)
  - [uk.gov.tfl.road.mqtt.RoadDisruptionInformation](#message-ukgovtflroadmqttroaddisruptioninformation)
  - [uk.gov.tfl.road.mqtt.RoadDisruptionClosure](#message-ukgovtflroadmqttroaddisruptionclosure)

---

## Message Group: uk.gov.tfl.road.corridors
---
### Message: uk.gov.tfl.road.RoadCorridor
*Reference record for a TfL managed road corridor fetched from GET /Road.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadCorridor` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road` |
| `subject` |  | `uritemplate` | `False` | `roads/{road_id}` |

#### Schema:
##### Object: RoadCorridor
*Reference record for a Transport for London (TfL) managed road corridor. Fetched from the GET /Road endpoint at bridge startup and refreshed periodically. Each corridor is a named road segment under TfL operational control, such as the A2, A12, or M25, with its current aggregate traffic status.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Unique identifier for the road corridor as used by the TfL Unified API. Corresponds to 'id' in the upstream response. Examples: 'a2', 'a12', 'm25'. Used as the stable domain key. |
| `display_name` | *string* | - | `True` | Human-readable display name for the road corridor as reported by TfL. Corresponds to 'displayName' in the upstream response. Examples: 'A2', 'A12', 'M25'. |
| `status_severity` | *string* (optional) | - | `False` | Current aggregate status severity for this corridor as assessed by TfL. Corresponds to 'statusSeverity' in the upstream response. Common values: 'Good', 'Moderate', 'Serious', 'Severe', 'NoDisruptions'. |
| `status_severity_description` | *string* (optional) | - | `False` | Human-readable description of the current status severity. Corresponds to 'statusSeverityDescription' in the upstream response. Example: 'Serious Delays'. |
| `bounds` | *string* (optional) | - | `False` | Bounding box for the road corridor as a JSON array string. Corresponds to 'bounds' in the upstream response. Format: '[[lon_sw,lat_sw],[lon_ne,lat_ne]]' in WGS84 decimal degrees. |
| `envelope` | *string* (optional) | - | `False` | GeoJSON envelope polygon for the road corridor geometry. Corresponds to 'envelope' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this corridor. Corresponds to 'url' in the upstream response. |
| `status_aggregation_start_date` | *datetime* (optional) | - | `False` | Start date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationStartDate' in the upstream response. |
| `status_aggregation_end_date` | *datetime* (optional) | - | `False` | End date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationEndDate' in the upstream response. |
| `event` | *string* | - | `True` | Lowercase-kebab event leaf used by MQTT/UNS topics. Constant value: 'corridor'. |
---
### Message: uk.gov.tfl.road.RoadStatus
*Real-time status snapshot for a TfL managed road corridor fetched from GET /Road/all/Status.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadStatus` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Status` |
| `subject` |  | `uritemplate` | `False` | `roads/{road_id}` |

#### Schema:
##### Object: RoadStatus
*Real-time status snapshot for a Transport for London (TfL) managed road corridor. Fetched from the GET /Road/all/Status endpoint on each polling cycle. Each event represents the current aggregate traffic status for one corridor as computed by TfL from active disruptions.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Unique identifier for the road corridor as used by the TfL Unified API. Corresponds to 'id' in the upstream response. Examples: 'a2', 'a12', 'm25'. Used as the stable domain key. |
| `display_name` | *string* | - | `True` | Human-readable display name for the road corridor as reported by TfL. Corresponds to 'displayName' in the upstream response. Examples: 'A2', 'A12', 'M25'. |
| `status_severity` | *string* (optional) | - | `False` | Current aggregate status severity for this corridor as assessed by TfL. Corresponds to 'statusSeverity' in the upstream response. Common values: 'Good', 'Moderate', 'Serious', 'Severe', 'NoDisruptions'. |
| `status_severity_description` | *string* (optional) | - | `False` | Human-readable description of the current status severity. Corresponds to 'statusSeverityDescription' in the upstream response. Example: 'Serious Delays'. |
| `bounds` | *string* (optional) | - | `False` | Bounding box for the road corridor as a JSON array string. Corresponds to 'bounds' in the upstream response. Format: '[[lon_sw,lat_sw],[lon_ne,lat_ne]]' in WGS84 decimal degrees. |
| `envelope` | *string* (optional) | - | `False` | GeoJSON envelope polygon for the road corridor geometry. Corresponds to 'envelope' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this corridor. Corresponds to 'url' in the upstream response. |
| `status_aggregation_start_date` | *datetime* (optional) | - | `False` | Start date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationStartDate' in the upstream response. |
| `status_aggregation_end_date` | *datetime* (optional) | - | `False` | End date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationEndDate' in the upstream response. |
| `event` | *string* | - | `True` | Lowercase-kebab event leaf used by MQTT/UNS topics. Constant value: 'status'. |
## Message Group: uk.gov.tfl.road.disruptions
---
### Message: uk.gov.tfl.road.RoadDisruption
*Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}/disruption` |

#### Schema:
##### Object: RoadDisruption
*Real-time road disruption event on the Transport for London (TfL) road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure affecting one or more roads in London. Disruption records are deduped by ID and lastModifiedTime so only changed records are re-emitted.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'. |
| `disruption_id` | *string* | - | `True` | Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix. |
| `category` | *string* (optional) | - | `False` | Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks. |
| `sub_category` | *string* (optional) | - | `False` | More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'. |
| `severity` | *string* | - | `True` | Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab. |
| `ordinal` | *int32* (optional) | - | `False` | Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response. |
| `point` | *string* (optional) | - | `False` | Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response. |
| `comments` | *string* (optional) | - | `False` | Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes. |
| `current_update` | *string* (optional) | - | `False` | Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves. |
| `current_update_datetime` | *datetime* (optional) | - | `False` | Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response. |
| `corridor_ids` | *{'$ref': '#/definitions/CorridorIdArray'}* (optional) | - | `False` | Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor. |
| `start_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response. |
| `end_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents. |
| `last_modified_time` | *datetime* (optional) | - | `False` | Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes. |
| `level_of_interest` | *string* (optional) | - | `False` | TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'. |
| `location` | *string* (optional) | - | `False` | Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response. |
| `is_provisional` | *boolean* (optional) | - | `False` | Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response. |
| `has_closures` | *boolean* (optional) | - | `False` | Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response. |
| `streets` | *{'$ref': '#/definitions/StreetArray'}* (optional) | - | `False` | Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry. |
| `geography` | *string* (optional) | - | `False` | GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption. |
| `geometry` | *string* (optional) | - | `False` | Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation. |
| `status` | *string* (optional) | - | `False` | Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response. |
| `is_active` | *boolean* (optional) | - | `False` | Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response. |
## Message Group: uk.gov.tfl.road.mqtt
---
### Message: uk.gov.tfl.road.mqtt.Roads
*Real-time status snapshot for a TfL managed road corridor fetched from GET /Road/all/Status.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadStatus` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Status` |
| `subject` |  | `uritemplate` | `False` | `roads/{road_id}` |

#### Schema:
##### Object: RoadStatus
*Real-time status snapshot for a Transport for London (TfL) managed road corridor. Fetched from the GET /Road/all/Status endpoint on each polling cycle. Each event represents the current aggregate traffic status for one corridor as computed by TfL from active disruptions.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Unique identifier for the road corridor as used by the TfL Unified API. Corresponds to 'id' in the upstream response. Examples: 'a2', 'a12', 'm25'. Used as the stable domain key. |
| `display_name` | *string* | - | `True` | Human-readable display name for the road corridor as reported by TfL. Corresponds to 'displayName' in the upstream response. Examples: 'A2', 'A12', 'M25'. |
| `status_severity` | *string* (optional) | - | `False` | Current aggregate status severity for this corridor as assessed by TfL. Corresponds to 'statusSeverity' in the upstream response. Common values: 'Good', 'Moderate', 'Serious', 'Severe', 'NoDisruptions'. |
| `status_severity_description` | *string* (optional) | - | `False` | Human-readable description of the current status severity. Corresponds to 'statusSeverityDescription' in the upstream response. Example: 'Serious Delays'. |
| `bounds` | *string* (optional) | - | `False` | Bounding box for the road corridor as a JSON array string. Corresponds to 'bounds' in the upstream response. Format: '[[lon_sw,lat_sw],[lon_ne,lat_ne]]' in WGS84 decimal degrees. |
| `envelope` | *string* (optional) | - | `False` | GeoJSON envelope polygon for the road corridor geometry. Corresponds to 'envelope' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this corridor. Corresponds to 'url' in the upstream response. |
| `status_aggregation_start_date` | *datetime* (optional) | - | `False` | Start date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationStartDate' in the upstream response. |
| `status_aggregation_end_date` | *datetime* (optional) | - | `False` | End date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationEndDate' in the upstream response. |
| `event` | *string* | - | `True` | Lowercase-kebab event leaf used by MQTT/UNS topics. Constant value: 'status'. |
---
### Message: uk.gov.tfl.road.mqtt.RoadDisruptionSerious
*Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}/disruption` |

#### Schema:
##### Object: RoadDisruption
*Real-time road disruption event on the Transport for London (TfL) road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure affecting one or more roads in London. Disruption records are deduped by ID and lastModifiedTime so only changed records are re-emitted.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'. |
| `disruption_id` | *string* | - | `True` | Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix. |
| `category` | *string* (optional) | - | `False` | Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks. |
| `sub_category` | *string* (optional) | - | `False` | More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'. |
| `severity` | *string* | - | `True` | Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab. |
| `ordinal` | *int32* (optional) | - | `False` | Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response. |
| `point` | *string* (optional) | - | `False` | Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response. |
| `comments` | *string* (optional) | - | `False` | Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes. |
| `current_update` | *string* (optional) | - | `False` | Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves. |
| `current_update_datetime` | *datetime* (optional) | - | `False` | Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response. |
| `corridor_ids` | *{'$ref': '#/definitions/CorridorIdArray'}* (optional) | - | `False` | Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor. |
| `start_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response. |
| `end_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents. |
| `last_modified_time` | *datetime* (optional) | - | `False` | Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes. |
| `level_of_interest` | *string* (optional) | - | `False` | TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'. |
| `location` | *string* (optional) | - | `False` | Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response. |
| `is_provisional` | *boolean* (optional) | - | `False` | Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response. |
| `has_closures` | *boolean* (optional) | - | `False` | Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response. |
| `streets` | *{'$ref': '#/definitions/StreetArray'}* (optional) | - | `False` | Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry. |
| `geography` | *string* (optional) | - | `False` | GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption. |
| `geometry` | *string* (optional) | - | `False` | Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation. |
| `status` | *string* (optional) | - | `False` | Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response. |
| `is_active` | *boolean* (optional) | - | `False` | Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response. |
---
### Message: uk.gov.tfl.road.mqtt.RoadDisruptionSevere
*Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}/disruption` |

#### Schema:
##### Object: RoadDisruption
*Real-time road disruption event on the Transport for London (TfL) road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure affecting one or more roads in London. Disruption records are deduped by ID and lastModifiedTime so only changed records are re-emitted.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'. |
| `disruption_id` | *string* | - | `True` | Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix. |
| `category` | *string* (optional) | - | `False` | Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks. |
| `sub_category` | *string* (optional) | - | `False` | More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'. |
| `severity` | *string* | - | `True` | Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab. |
| `ordinal` | *int32* (optional) | - | `False` | Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response. |
| `point` | *string* (optional) | - | `False` | Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response. |
| `comments` | *string* (optional) | - | `False` | Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes. |
| `current_update` | *string* (optional) | - | `False` | Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves. |
| `current_update_datetime` | *datetime* (optional) | - | `False` | Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response. |
| `corridor_ids` | *{'$ref': '#/definitions/CorridorIdArray'}* (optional) | - | `False` | Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor. |
| `start_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response. |
| `end_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents. |
| `last_modified_time` | *datetime* (optional) | - | `False` | Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes. |
| `level_of_interest` | *string* (optional) | - | `False` | TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'. |
| `location` | *string* (optional) | - | `False` | Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response. |
| `is_provisional` | *boolean* (optional) | - | `False` | Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response. |
| `has_closures` | *boolean* (optional) | - | `False` | Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response. |
| `streets` | *{'$ref': '#/definitions/StreetArray'}* (optional) | - | `False` | Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry. |
| `geography` | *string* (optional) | - | `False` | GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption. |
| `geometry` | *string* (optional) | - | `False` | Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation. |
| `status` | *string* (optional) | - | `False` | Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response. |
| `is_active` | *boolean* (optional) | - | `False` | Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response. |
---
### Message: uk.gov.tfl.road.mqtt.RoadDisruptionModerate
*Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}/disruption` |

#### Schema:
##### Object: RoadDisruption
*Real-time road disruption event on the Transport for London (TfL) road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure affecting one or more roads in London. Disruption records are deduped by ID and lastModifiedTime so only changed records are re-emitted.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'. |
| `disruption_id` | *string* | - | `True` | Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix. |
| `category` | *string* (optional) | - | `False` | Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks. |
| `sub_category` | *string* (optional) | - | `False` | More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'. |
| `severity` | *string* | - | `True` | Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab. |
| `ordinal` | *int32* (optional) | - | `False` | Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response. |
| `point` | *string* (optional) | - | `False` | Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response. |
| `comments` | *string* (optional) | - | `False` | Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes. |
| `current_update` | *string* (optional) | - | `False` | Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves. |
| `current_update_datetime` | *datetime* (optional) | - | `False` | Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response. |
| `corridor_ids` | *{'$ref': '#/definitions/CorridorIdArray'}* (optional) | - | `False` | Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor. |
| `start_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response. |
| `end_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents. |
| `last_modified_time` | *datetime* (optional) | - | `False` | Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes. |
| `level_of_interest` | *string* (optional) | - | `False` | TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'. |
| `location` | *string* (optional) | - | `False` | Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response. |
| `is_provisional` | *boolean* (optional) | - | `False` | Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response. |
| `has_closures` | *boolean* (optional) | - | `False` | Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response. |
| `streets` | *{'$ref': '#/definitions/StreetArray'}* (optional) | - | `False` | Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry. |
| `geography` | *string* (optional) | - | `False` | GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption. |
| `geometry` | *string* (optional) | - | `False` | Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation. |
| `status` | *string* (optional) | - | `False` | Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response. |
| `is_active` | *boolean* (optional) | - | `False` | Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response. |
---
### Message: uk.gov.tfl.road.mqtt.RoadDisruptionMinor
*Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}/disruption` |

#### Schema:
##### Object: RoadDisruption
*Real-time road disruption event on the Transport for London (TfL) road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure affecting one or more roads in London. Disruption records are deduped by ID and lastModifiedTime so only changed records are re-emitted.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'. |
| `disruption_id` | *string* | - | `True` | Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix. |
| `category` | *string* (optional) | - | `False` | Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks. |
| `sub_category` | *string* (optional) | - | `False` | More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'. |
| `severity` | *string* | - | `True` | Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab. |
| `ordinal` | *int32* (optional) | - | `False` | Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response. |
| `point` | *string* (optional) | - | `False` | Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response. |
| `comments` | *string* (optional) | - | `False` | Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes. |
| `current_update` | *string* (optional) | - | `False` | Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves. |
| `current_update_datetime` | *datetime* (optional) | - | `False` | Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response. |
| `corridor_ids` | *{'$ref': '#/definitions/CorridorIdArray'}* (optional) | - | `False` | Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor. |
| `start_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response. |
| `end_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents. |
| `last_modified_time` | *datetime* (optional) | - | `False` | Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes. |
| `level_of_interest` | *string* (optional) | - | `False` | TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'. |
| `location` | *string* (optional) | - | `False` | Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response. |
| `is_provisional` | *boolean* (optional) | - | `False` | Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response. |
| `has_closures` | *boolean* (optional) | - | `False` | Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response. |
| `streets` | *{'$ref': '#/definitions/StreetArray'}* (optional) | - | `False` | Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry. |
| `geography` | *string* (optional) | - | `False` | GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption. |
| `geometry` | *string* (optional) | - | `False` | Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation. |
| `status` | *string* (optional) | - | `False` | Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response. |
| `is_active` | *boolean* (optional) | - | `False` | Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response. |
---
### Message: uk.gov.tfl.road.mqtt.RoadDisruptionInformation
*Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}/disruption` |

#### Schema:
##### Object: RoadDisruption
*Real-time road disruption event on the Transport for London (TfL) road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure affecting one or more roads in London. Disruption records are deduped by ID and lastModifiedTime so only changed records are re-emitted.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'. |
| `disruption_id` | *string* | - | `True` | Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix. |
| `category` | *string* (optional) | - | `False` | Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks. |
| `sub_category` | *string* (optional) | - | `False` | More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'. |
| `severity` | *string* | - | `True` | Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab. |
| `ordinal` | *int32* (optional) | - | `False` | Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response. |
| `point` | *string* (optional) | - | `False` | Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response. |
| `comments` | *string* (optional) | - | `False` | Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes. |
| `current_update` | *string* (optional) | - | `False` | Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves. |
| `current_update_datetime` | *datetime* (optional) | - | `False` | Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response. |
| `corridor_ids` | *{'$ref': '#/definitions/CorridorIdArray'}* (optional) | - | `False` | Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor. |
| `start_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response. |
| `end_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents. |
| `last_modified_time` | *datetime* (optional) | - | `False` | Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes. |
| `level_of_interest` | *string* (optional) | - | `False` | TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'. |
| `location` | *string* (optional) | - | `False` | Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response. |
| `is_provisional` | *boolean* (optional) | - | `False` | Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response. |
| `has_closures` | *boolean* (optional) | - | `False` | Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response. |
| `streets` | *{'$ref': '#/definitions/StreetArray'}* (optional) | - | `False` | Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry. |
| `geography` | *string* (optional) | - | `False` | GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption. |
| `geometry` | *string* (optional) | - | `False` | Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation. |
| `status` | *string* (optional) | - | `False` | Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response. |
| `is_active` | *boolean* (optional) | - | `False` | Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response. |
---
### Message: uk.gov.tfl.road.mqtt.RoadDisruptionClosure
*Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}/disruption` |

#### Schema:
##### Object: RoadDisruption
*Real-time road disruption event on the Transport for London (TfL) road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure affecting one or more roads in London. Disruption records are deduped by ID and lastModifiedTime so only changed records are re-emitted.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `road_id` | *string* | - | `True` | Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'. |
| `disruption_id` | *string* | - | `True` | Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix. |
| `category` | *string* (optional) | - | `False` | Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks. |
| `sub_category` | *string* (optional) | - | `False` | More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'. |
| `severity` | *string* | - | `True` | Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab. |
| `ordinal` | *int32* (optional) | - | `False` | Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response. |
| `url` | *string* (optional) | - | `False` | URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response. |
| `point` | *string* (optional) | - | `False` | Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response. |
| `comments` | *string* (optional) | - | `False` | Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes. |
| `current_update` | *string* (optional) | - | `False` | Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves. |
| `current_update_datetime` | *datetime* (optional) | - | `False` | Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response. |
| `corridor_ids` | *{'$ref': '#/definitions/CorridorIdArray'}* (optional) | - | `False` | Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor. |
| `start_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response. |
| `end_datetime` | *datetime* (optional) | - | `False` | Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents. |
| `last_modified_time` | *datetime* (optional) | - | `False` | Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes. |
| `level_of_interest` | *string* (optional) | - | `False` | TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'. |
| `location` | *string* (optional) | - | `False` | Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response. |
| `is_provisional` | *boolean* (optional) | - | `False` | Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response. |
| `has_closures` | *boolean* (optional) | - | `False` | Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response. |
| `streets` | *{'$ref': '#/definitions/StreetArray'}* (optional) | - | `False` | Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry. |
| `geography` | *string* (optional) | - | `False` | GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption. |
| `geometry` | *string* (optional) | - | `False` | Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation. |
| `status` | *string* (optional) | - | `False` | Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response. |
| `is_active` | *boolean* (optional) | - | `False` | Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response. |

## Subscription patterns

MQTT/UNS subscribers can use these wildcard filters:

- All TfL road traffic messages: `traffic/gb/tfl/tfl-road-traffic/#`
- Latest retained status for every TfL road: `traffic/gb/tfl/tfl-road-traffic/roads/+/status`
- All disruptions for one road: `traffic/gb/tfl/tfl-road-traffic/disruptions/a2/+/+/disruption`
- All severe disruptions: `traffic/gb/tfl/tfl-road-traffic/disruptions/+/severe/+/disruption`
- All closure disruptions: `traffic/gb/tfl/tfl-road-traffic/disruptions/+/closure/+/disruption`
