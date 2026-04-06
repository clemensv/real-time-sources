# Digitraffic Road — Finnish Road Traffic Events

The bridge emits CloudEvents in structured JSON format to Kafka-compatible
endpoints. Data is streamed in real time from the Digitraffic MQTT service at
`wss://tie.digitraffic.fi/mqtt`.

## Endpoints & Kafka Topics

| Kafka topic | Key template | Message group |
|---|---|---|
| `digitraffic-road-sensors` | `{station_id}/{sensor_id}` | Sensor readings (TMS + weather) |
| `digitraffic-road-messages` | `{situation_id}` | Traffic messages (announcements, road works, restrictions) |
| `digitraffic-road-maintenance` | `{domain}` | Maintenance vehicle tracking |

## Event Types

### Sensors

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

### Maintenance

| Event type | Payload schema | MQTT source topic |
|---|---|---|
| `fi.digitraffic.road.maintenance.MaintenanceTracking` | `MaintenanceTracking` | `maintenance-v2/routes/{domain}` |

## Payload Shapes

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
