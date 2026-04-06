# Digitraffic Road — Finnish Road Traffic Events

The bridge emits CloudEvents in structured JSON format to Kafka-compatible
endpoints. Telemetry is streamed in real time from the Digitraffic MQTT service
at `wss://tie.digitraffic.fi/mqtt`. Reference data — station metadata and
maintenance task type catalogs — is fetched from the Digitraffic REST API at
startup and emitted before the telemetry stream begins.

## Endpoints & Kafka Topics

| Kafka topic | Key template | Message group | Data kind |
|---|---|---|---|
| `digitraffic-road-sensors` | `{station_id}/{sensor_id}` | Sensor readings (TMS + weather) | Telemetry |
| `digitraffic-road-sensors` | `{station_id}` | Station metadata (TMS + weather) | Reference |
| `digitraffic-road-messages` | `{situation_id}` | Traffic messages (announcements, road works, restrictions) | Telemetry |
| `digitraffic-road-maintenance` | `{domain}` | Maintenance vehicle tracking | Telemetry |
| `digitraffic-road-maintenance` | `{task_id}` | Maintenance task type catalog | Reference |

## Event Types

### Station Reference Data

| Event type | Payload schema | REST source |
|---|---|---|
| `fi.digitraffic.road.stations.TmsStation` | `TmsStation` | `/api/tms/v1/stations` |
| `fi.digitraffic.road.stations.WeatherStation` | `WeatherStation` | `/api/weather/v1/stations` |

### Sensor Telemetry

| Event type | Payload schema | MQTT source topic |
|---|---|---|
| `fi.digitraffic.road.sensors.TmsSensorData` | `TmsSensorData` | `tms-v2/{stationId}/{sensorId}` |
| `fi.digitraffic.road.sensors.WeatherSensorData` | `WeatherSensorData` | `weather-v2/{stationId}/{sensorId}` |

### Traffic Messages

| Event type | Payload schema | MQTT source topic |
|---|---|---|
| `fi.digitraffic.road.messages.TrafficAnnouncement` | `TrafficMessage` | `traffic-message-v3/simple/TRAFFIC_ANNOUNCEMENT` |
| `fi.digitraffic.road.messages.RoadWork` | `TrafficMessage` | `traffic-message-v3/simple/ROAD_WORK` |
| `fi.digitraffic.road.messages.WeightRestriction` | `TrafficMessage` | `traffic-message-v3/simple/WEIGHT_RESTRICTION` |
| `fi.digitraffic.road.messages.ExemptedTransport` | `TrafficMessage` | `traffic-message-v3/simple/EXEMPTED_TRANSPORT` |

### Maintenance Telemetry

| Event type | Payload schema | MQTT source topic |
|---|---|---|
| `fi.digitraffic.road.maintenance.MaintenanceTracking` | `MaintenanceTracking` | `maintenance-v2/routes/{domain}` |

### Maintenance Reference Data

| Event type | Payload schema | REST source |
|---|---|---|
| `fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType` | `MaintenanceTaskType` | `/api/maintenance/v1/tracking/tasks` |

## Payload Shapes

### TmsStation (reference)

TMS station metadata. Over 500 TMS stations measure traffic volumes and
speeds across the Finnish road network. Contextualizes TmsSensorData telemetry.

| Field | Type | Description |
|---|---|---|
| `station_id` | int | TMS station identifier |
| `name` | string | Internal station name |
| `tms_number` | int or null | Legacy TMS numbering |
| `names_fi` | string | Finnish display name |
| `names_sv` | string or null | Swedish display name |
| `names_en` | string or null | English display name |
| `longitude` | double | WGS84 longitude |
| `latitude` | double | WGS84 latitude |
| `altitude` | double or null | Altitude (meters) |
| `municipality` | string | Municipality name |
| `municipality_code` | int | Finnish municipality code |
| `province` | string | Province name |
| `province_code` | int | Province code |
| `road_number` | int | Road number |
| `road_section` | int | Road section number |
| `distance_from_section_start` | int | Distance from section start (meters) |
| `carriageway` | string or null | Carriageway type |
| `side` | string or null | Road side |
| `station_type` | string | Hardware type code (e.g. `DSL_6`) |
| `collection_status` | string | `GATHERING`, `REMOVED_TEMPORARILY`, or `REMOVED_PERMANENTLY` |
| `state` | string or null | Operational state (`OK`, `FAULT`, `DISABLED`) |
| `free_flow_speed_1` | double or null | Direction 1 free-flow speed (km/h) |
| `free_flow_speed_2` | double or null | Direction 2 free-flow speed (km/h) |
| `bearing` | int or null | Road bearing (degrees) |
| `start_time` | string | ISO 8601 data collection start date |
| `livi_id` | string or null | Legacy Fintraffic identifier |
| `sensors` | array of int | Available sensor identifiers |
| `data_updated_time` | string or null | ISO 8601 last metadata update |

### WeatherStation (reference)

Road weather station metadata. Over 350 stations measure atmospheric and road
surface conditions. Contextualizes WeatherSensorData telemetry.

| Field | Type | Description |
|---|---|---|
| `station_id` | int | Weather station identifier |
| `name` | string | Internal station name |
| `names_fi` | string | Finnish display name |
| `names_sv` | string or null | Swedish display name |
| `names_en` | string or null | English display name |
| `longitude` | double | WGS84 longitude |
| `latitude` | double | WGS84 latitude |
| `altitude` | double or null | Altitude (meters) |
| `municipality` | string | Municipality name |
| `municipality_code` | int | Finnish municipality code |
| `province` | string | Province name |
| `province_code` | int | Province code |
| `road_number` | int | Road number |
| `road_section` | int | Road section number |
| `distance_from_section_start` | int | Distance from section start (meters) |
| `carriageway` | string or null | Carriageway type |
| `side` | string or null | Road side |
| `contract_area` | string or null | Maintenance contract area name |
| `contract_area_code` | int or null | Contract area code |
| `station_type` | string | Hardware type code (e.g. `RWS_200`) |
| `master` | boolean | Whether this is the primary station |
| `collection_status` | string | Data collection status |
| `collection_interval` | int | Collection interval (seconds) |
| `state` | string or null | Operational state |
| `start_time` | string | ISO 8601 data collection start date |
| `livi_id` | string or null | Legacy Fintraffic identifier |
| `sensors` | array of int | Available sensor identifiers |
| `data_updated_time` | string or null | ISO 8601 last metadata update |

### MaintenanceTaskType (reference)

Maintenance task type definition with multilingual names. Approximately 40
task types classify road maintenance activities. Contextualizes the `tasks`
array in MaintenanceTracking telemetry.

| Field | Type | Description |
|---|---|---|
| `task_id` | string | Task type identifier (e.g. `PLOUGHING_AND_SLUSH_REMOVAL`) |
| `name_fi` | string | Finnish name |
| `name_en` | string | English name |
| `name_sv` | string | Swedish name |
| `data_updated_time` | string or null | ISO 8601 last update timestamp |

### TmsSensorData

Traffic Measurement System sensor reading. Each message is a single
computational sensor measurement at a TMS station. Over 500 TMS stations
across the Finnish road network report vehicle counts and average
speeds aggregated over rolling or fixed time windows.

| Field | Type | Description |
|---|---|---|
| `station_id` | int | TMS station identifier |
| `sensor_id` | int | Sensor identifier within the station |
| `value` | double | Measured value (kpl/h for passings, km/h for speed) |
| `time` | int | Measurement timestamp (Unix epoch seconds, UTC) |
| `start` | int or null | Time window start for fixed-window sensors (epoch seconds) |
| `end` | int or null | Time window end for fixed-window sensors (epoch seconds) |

### WeatherSensorData

Road weather station sensor reading. Each message is a single sensor
measurement at a road weather station. Over 350 stations measure air and
road surface temperatures, wind, humidity, dew point, and precipitation.

| Field | Type | Description |
|---|---|---|
| `station_id` | int | Weather station identifier |
| `sensor_id` | int | Sensor identifier within the station |
| `value` | double | Measured value (°C, m/s, %, mm depending on sensor) |
| `time` | int | Measurement timestamp (Unix epoch seconds, UTC) |

### TrafficMessage

Traffic message describing a road situation (incident, road work, weight
restriction, or exempted transport). The MQTT payload is gzip-compressed and
base64-encoded Simple JSON (GeoJSON). The bridge flattens the first
announcement into first-class fields and preserves full detail in serialized
JSON fields.

| Field | Type | Description |
|---|---|---|
| `situation_id` | string | Unique situation GUID (e.g. `GUID50455291`) |
| `situation_type` | string | `traffic announcement`, `road work`, `weight restriction`, or `exempted transport` |
| `traffic_announcement_type` | string or null | Sub-type for traffic announcements (e.g. `preliminary accident report`) |
| `version` | int | Monotonically increasing version counter |
| `release_time` | string | ISO 8601 UTC first release timestamp |
| `version_time` | string | ISO 8601 UTC timestamp for this version |
| `title` | string or null | Human-readable title (Finnish) |
| `language` | string or null | ISO 639-1 language code (typically `fi`) |
| `sender` | string or null | Issuing traffic management center |
| `location_description` | string or null | Human-readable location description |
| `start_time` | string or null | ISO 8601 start of the situation time window |
| `end_time` | string or null | ISO 8601 expected end of the situation |
| `features_json` | string or null | JSON array of traffic impact features |
| `road_work_phases_json` | string or null | JSON array of road work phases (road work only) |
| `comment` | string or null | Free-text comment |
| `additional_information` | string or null | Supplementary information |
| `contact_phone` | string or null | Contact telephone number |
| `contact_email` | string or null | Contact email address |
| `announcements_json` | string or null | Full JSON array of all announcements |
| `geometry_type` | string or null | GeoJSON geometry type |
| `geometry_coordinates_json` | string or null | JSON array of GeoJSON coordinates |

### MaintenanceTracking

Maintenance vehicle position and task report. Data originates from the
Finnish Transport Infrastructure Agency's Harja system for state roads and
from municipal systems for other domains.

| Field | Type | Description |
|---|---|---|
| `domain` | string | Source domain (e.g. `state-roads`, `autori-kuopio`) |
| `time` | int | Tracking timestamp (Unix epoch seconds, UTC) |
| `source` | string or null | Source system name (e.g. `Harja/Väylävirasto`) |
| `tasks` | array of string | Maintenance task type identifiers (e.g. `SALTING`, `PLOUGHING_AND_SLUSH_REMOVAL`) |
| `x` | double | Longitude (WGS84) |
| `y` | double | Latitude (WGS84) |
| `direction` | double or null | Vehicle heading in degrees (0-360) |
