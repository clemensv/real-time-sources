# Digitraffic Road — Finnish Road Traffic Data Events

Real-time road traffic data from the Finnish national road network operated by Fintraffic. Telemetry is streamed via the Digitraffic MQTT service at `wss://tie.digitraffic.fi/mqtt` and includes TMS sensor readings, road weather sensor readings, traffic messages (incidents, road works, weight restrictions, exempted transports), and maintenance vehicle tracking. Station metadata and maintenance task type catalogs are fetched as reference data from the Digitraffic REST API at startup.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 5 |
| Messagegroups | 5 |
| Schemagroups | 5 |

## Endpoints

### Endpoint `fi.digitraffic.road.sensors.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.road.sensors`](#messagegroup-fidigitrafficroadsensors) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-road-sensors` |
| Kafka key | `{station_id}/{sensor_id}` |
| Deployed | False |

### Endpoint `fi.digitraffic.road.messages.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.road.messages`](#messagegroup-fidigitrafficroadmessages) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-road-messages` |
| Kafka key | `{situation_id}` |
| Deployed | False |

### Endpoint `fi.digitraffic.road.maintenance.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.road.maintenance`](#messagegroup-fidigitrafficroadmaintenance) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-road-maintenance` |
| Kafka key | `{domain}` |
| Deployed | False |

### Endpoint `fi.digitraffic.road.stations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.road.stations`](#messagegroup-fidigitrafficroadstations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-road-sensors` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `fi.digitraffic.road.maintenance.tasks.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`fi.digitraffic.road.maintenance.tasks`](#messagegroup-fidigitrafficroadmaintenancetasks) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `digitraffic-road-maintenance` |
| Kafka key | `{task_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `fi.digitraffic.road.sensors`
<a id="messagegroup-fidigitrafficroadsensors"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.road.sensors.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `fi.digitraffic.road.sensors.TmsSensorData`
<a id="message-fidigitrafficroadsensorstmssensordata"></a>

| Field | Value |
| --- | --- |
| Name | TmsSensorData |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.sensors.jstruct/schemas/fi.digitraffic.road.sensors.TmsSensorData`](#schema-fidigitrafficroadsensorstmssensordata) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.sensors.TmsSensorData` |
| `source` |  | `string` | `False` | `wss://tie.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{station_id}/{sensor_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.sensors.Kafka` | `KAFKA` | topic `digitraffic-road-sensors`; key `{station_id}/{sensor_id}` |

#### Message `fi.digitraffic.road.sensors.WeatherSensorData`
<a id="message-fidigitrafficroadsensorsweathersensordata"></a>

| Field | Value |
| --- | --- |
| Name | WeatherSensorData |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.sensors.jstruct/schemas/fi.digitraffic.road.sensors.WeatherSensorData`](#schema-fidigitrafficroadsensorsweathersensordata) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.sensors.WeatherSensorData` |
| `source` |  | `string` | `False` | `wss://tie.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{station_id}/{sensor_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.sensors.Kafka` | `KAFKA` | topic `digitraffic-road-sensors`; key `{station_id}/{sensor_id}` |

### Messagegroup `fi.digitraffic.road.messages`
<a id="messagegroup-fidigitrafficroadmessages"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.road.messages.Kafka` (KAFKA) |
| Messages | 4 |

#### Message `fi.digitraffic.road.messages.TrafficAnnouncement`
<a id="message-fidigitrafficroadmessagestrafficannouncement"></a>

| Field | Value |
| --- | --- |
| Name | TrafficAnnouncement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.messages.jstruct/schemas/fi.digitraffic.road.messages.TrafficMessage`](#schema-fidigitrafficroadmessagestrafficmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.messages.TrafficAnnouncement` |
| `source` |  | `string` | `False` | `wss://tie.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{situation_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.messages.Kafka` | `KAFKA` | topic `digitraffic-road-messages`; key `{situation_id}` |

#### Message `fi.digitraffic.road.messages.RoadWork`
<a id="message-fidigitrafficroadmessagesroadwork"></a>

| Field | Value |
| --- | --- |
| Name | RoadWork |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.messages.jstruct/schemas/fi.digitraffic.road.messages.TrafficMessage`](#schema-fidigitrafficroadmessagestrafficmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.messages.RoadWork` |
| `source` |  | `string` | `False` | `wss://tie.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{situation_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.messages.Kafka` | `KAFKA` | topic `digitraffic-road-messages`; key `{situation_id}` |

#### Message `fi.digitraffic.road.messages.WeightRestriction`
<a id="message-fidigitrafficroadmessagesweightrestriction"></a>

| Field | Value |
| --- | --- |
| Name | WeightRestriction |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.messages.jstruct/schemas/fi.digitraffic.road.messages.TrafficMessage`](#schema-fidigitrafficroadmessagestrafficmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.messages.WeightRestriction` |
| `source` |  | `string` | `False` | `wss://tie.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{situation_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.messages.Kafka` | `KAFKA` | topic `digitraffic-road-messages`; key `{situation_id}` |

#### Message `fi.digitraffic.road.messages.ExemptedTransport`
<a id="message-fidigitrafficroadmessagesexemptedtransport"></a>

| Field | Value |
| --- | --- |
| Name | ExemptedTransport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.messages.jstruct/schemas/fi.digitraffic.road.messages.TrafficMessage`](#schema-fidigitrafficroadmessagestrafficmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.messages.ExemptedTransport` |
| `source` |  | `string` | `False` | `wss://tie.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{situation_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.messages.Kafka` | `KAFKA` | topic `digitraffic-road-messages`; key `{situation_id}` |

### Messagegroup `fi.digitraffic.road.maintenance`
<a id="messagegroup-fidigitrafficroadmaintenance"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.road.maintenance.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `fi.digitraffic.road.maintenance.MaintenanceTracking`
<a id="message-fidigitrafficroadmaintenancemaintenancetracking"></a>

| Field | Value |
| --- | --- |
| Name | MaintenanceTracking |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.maintenance.jstruct/schemas/fi.digitraffic.road.maintenance.MaintenanceTracking`](#schema-fidigitrafficroadmaintenancemaintenancetracking) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.maintenance.MaintenanceTracking` |
| `source` |  | `string` | `False` | `wss://tie.digitraffic.fi/mqtt` |
| `subject` |  | `uritemplate` | `False` | `{domain}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.maintenance.Kafka` | `KAFKA` | topic `digitraffic-road-maintenance`; key `{domain}` |

### Messagegroup `fi.digitraffic.road.stations`
<a id="messagegroup-fidigitrafficroadstations"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.road.stations.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `fi.digitraffic.road.stations.TmsStation`
<a id="message-fidigitrafficroadstationstmsstation"></a>

| Field | Value |
| --- | --- |
| Name | TmsStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.stations.jstruct/schemas/fi.digitraffic.road.stations.TmsStation`](#schema-fidigitrafficroadstationstmsstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.stations.TmsStation` |
| `source` |  | `string` | `False` | `https://tie.digitraffic.fi/api` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.stations.Kafka` | `KAFKA` | topic `digitraffic-road-sensors`; key `{station_id}` |

#### Message `fi.digitraffic.road.stations.WeatherStation`
<a id="message-fidigitrafficroadstationsweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.stations.jstruct/schemas/fi.digitraffic.road.stations.WeatherStation`](#schema-fidigitrafficroadstationsweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.stations.WeatherStation` |
| `source` |  | `string` | `False` | `https://tie.digitraffic.fi/api` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.stations.Kafka` | `KAFKA` | topic `digitraffic-road-sensors`; key `{station_id}` |

### Messagegroup `fi.digitraffic.road.maintenance.tasks`
<a id="messagegroup-fidigitrafficroadmaintenancetasks"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `fi.digitraffic.road.maintenance.tasks.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType`
<a id="message-fidigitrafficroadmaintenancetasksmaintenancetasktype"></a>

| Field | Value |
| --- | --- |
| Name | MaintenanceTaskType |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/fi.digitraffic.road.maintenance.tasks.jstruct/schemas/fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType`](#schema-fidigitrafficroadmaintenancetasksmaintenancetasktype) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType` |
| `source` |  | `string` | `False` | `https://tie.digitraffic.fi/api` |
| `subject` |  | `uritemplate` | `False` | `{task_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `fi.digitraffic.road.maintenance.tasks.Kafka` | `KAFKA` | topic `digitraffic-road-maintenance`; key `{task_id}` |

## Schemagroups

### Schemagroup `fi.digitraffic.road.sensors.jstruct`
<a id="schemagroup-fidigitrafficroadsensorsjstruct"></a>

#### Schema `fi.digitraffic.road.sensors.TmsSensorData`
<a id="schema-fidigitrafficroadsensorstmssensordata"></a>

| Field | Value |
| --- | --- |
| Name | TmsSensorData |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/sensors/TmsSensorData` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TmsSensorData`
<a id="schema-node-tmssensordata"></a>

Traffic Measurement System (TMS) sensor reading from the Finnish national road network operated by Fintraffic. Each message represents a single computational sensor measurement at a TMS station, delivered in real time via the Digitraffic MQTT stream at wss://tie.digitraffic.fi/mqtt on topic tms-v2/{stationId}/{sensorId}. TMS stations measure vehicle counts (passings) and average speeds aggregated over rolling or fixed time windows. Over 500 stations across the Finnish road network report data every minute. See https://www.digitraffic.fi/en/road-traffic/ and the TMS documentation at https://www.digitraffic.fi/en/road-traffic/lam/ for full sensor descriptions.

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/sensors/TmsSensorData` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `int32` | `True` | TMS station numeric identifier as assigned by Fintraffic. Each station is located at a fixed point on the Finnish road network and identified by a unique integer (e.g. 23001). Station metadata including road address, municipality, and free-flow speeds is available from the /api/tms/v1/stations REST endpoint. | - | - | - |
| `sensor_id` | `int32` | `True` | Computational sensor identifier within the TMS station. Each sensor measures a specific traffic parameter in a given direction and time window. Common sensor families include OHITUKSET (vehicle passings, unit kpl/h), KESKINOPEUS (average speed, unit km/h), and LIUKUVA_NOPEUS (rolling speed per lane, unit km/h). Sensor metadata is available from /api/tms/v1/sensors. | - | - | - |
| `value` | `double` | `True` | Measured value in the sensor's native unit. Units vary by sensor family: kpl/h (vehicles per hour) for OHITUKSET passings sensors, km/h for KESKINOPEUS and LIUKUVA_NOPEUS speed sensors, and dimensionless percentage ratios for traffic situation indicators (VVAPAAS, MS suffixed sensors). | - | - | - |
| `time` | `int32` | `True` | Measurement timestamp as Unix epoch seconds (UTC). Indicates when the sensor reading was taken or the aggregation period was last updated. | - | - | - |
| `start` | `union` | `False` | Start of the fixed time window as Unix epoch seconds (UTC). Present for fixed-window aggregate sensors such as OHITUKSET_5MIN_KIINTEA (5-minute fixed passings), KESKINOPEUS_60MIN_KIINTEA (60-minute fixed average speed), and OHITUKSET_60MIN_KIINTEA. Null or absent for rolling-window sensors (LIUKUVA suffix) and per-lane sensors. | - | - | - |
| `end` | `union` | `False` | End of the fixed time window as Unix epoch seconds (UTC). Present for fixed-window aggregate sensors. Null or absent for rolling-window and per-lane sensors. | - | - | - |

#### Schema `fi.digitraffic.road.sensors.WeatherSensorData`
<a id="schema-fidigitrafficroadsensorsweathersensordata"></a>

| Field | Value |
| --- | --- |
| Name | WeatherSensorData |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/sensors/WeatherSensorData` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherSensorData`
<a id="schema-node-weathersensordata"></a>

Road weather station sensor reading from the Finnish national road network operated by Fintraffic. Each message represents a single sensor measurement at a road weather station, delivered in real time via the Digitraffic MQTT stream at wss://tie.digitraffic.fi/mqtt on topic weather-v2/{stationId}/{sensorId}. Over 350 road weather stations measure parameters including air temperature (ILMA), road surface temperature (TIE_1), ground temperature (MAA_1), dew point (KASTEPISTE), freezing point (JÄÄTYMISPISTE_1), wind speed (KESKITUULI, MAKSIMITUULI), humidity (ILMAN_KOSTEUS), and precipitation. Data is updated every minute. See https://www.digitraffic.fi/en/road-traffic/ for full documentation.

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/sensors/WeatherSensorData` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `int32` | `True` | Road weather station numeric identifier as assigned by Fintraffic (e.g. 1012). Station metadata including road address, municipality, and available sensors is available from the /api/weather/v1/stations REST endpoint. | - | - | - |
| `sensor_id` | `int32` | `True` | Sensor identifier within the road weather station. Each sensor measures a specific weather or road surface parameter. Common sensors: ILMA (id 1, air temperature °C), ILMA_DERIVAATTA (id 2, air temp derivative °C/h), TIE_1 (id 3, road surface temp °C), MAA_1 (id 7, ground temp °C), KASTEPISTE (id 9, dew point °C), JÄÄTYMISPISTE_1 (id 10, freezing point °C), KESKITUULI (id 16, avg wind m/s), MAKSIMITUULI (id 17, max wind m/s), ILMAN_KOSTEUS (id 19, relative humidity %). Full sensor list at /api/weather/v1/sensors. | - | - | - |
| `value` | `double` | `True` | Measured value in the sensor's native unit. Units vary by sensor: °C for temperatures and dew/freezing points, °C/h for temperature derivatives, m/s for wind speed, % for relative humidity, mm for precipitation amounts. | - | - | - |
| `time` | `int32` | `True` | Measurement timestamp as Unix epoch seconds (UTC). Indicates when the sensor reading was taken. | - | - | - |

### Schemagroup `fi.digitraffic.road.messages.jstruct`
<a id="schemagroup-fidigitrafficroadmessagesjstruct"></a>

#### Schema `fi.digitraffic.road.messages.TrafficMessage`
<a id="schema-fidigitrafficroadmessagestrafficmessage"></a>

| Field | Value |
| --- | --- |
| Name | TrafficMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/messages/TrafficMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TrafficMessage`
<a id="schema-node-trafficmessage"></a>

Traffic message from the Finnish national road network operated by Fintraffic, delivered in real time via the Digitraffic MQTT stream at wss://tie.digitraffic.fi/mqtt on topic traffic-message-v3/simple/{situationType}. Traffic messages describe situations such as accidents, road works, weight restrictions, and exempted transports. Each message carries a stable situation identifier (GUID), a version counter, and one or more announcements with location, timing, and descriptive detail. The MQTT payload is gzip-compressed and base64-encoded Simple JSON derived from the GeoJSON-based Digitraffic traffic-message API. See https://www.digitraffic.fi/en/road-traffic/ for the full API documentation and situation type taxonomy.

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/messages/TrafficMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `situation_id` | `string` | `True` | Unique situation identifier assigned by Fintraffic, prefixed with 'GUID' (e.g. 'GUID50455291'). Stable across all version updates for a given situation. | - | - | - |
| `situation_type` | `string` | `True` | Situation category as defined by Fintraffic. Values: 'traffic announcement' (incidents, lane closures, ramp closures), 'road work' (planned and active road works with phases), 'weight restriction' (load-bearing limits on roads or bridges), 'exempted transport' (oversize or heavy transports requiring advance notice). Mapped from the MQTT topic situationType segment. | - | - | - |
| `traffic_announcement_type` | `union` | `False` | Sub-classification for traffic announcements. Values include 'preliminary accident report', 'accident report', 'general', 'unconfirmed observation', and others. Present only when situation_type is 'traffic announcement'; null otherwise. | - | - | - |
| `version` | `int32` | `True` | Monotonically increasing version counter for this situation. Starts at 1 and increments with each update to the situation's announcements, timing, or status. | - | - | - |
| `release_time` | `string` | `True` | ISO 8601 UTC timestamp when the first version of this situation was released (e.g. '2025-10-22T06:39:54.787Z'). | - | - | - |
| `version_time` | `string` | `True` | ISO 8601 UTC timestamp when this version of the situation was published (e.g. '2025-10-22T07:09:57.237Z'). | - | - | - |
| `title` | `union` | `False` | Human-readable title from the first announcement, typically identifying the road, municipality, and situation type in Finnish (e.g. 'Tie 4, eli Ivalontie, Sodankylä. Ensitiedote liikenneonnettomuudesta.'). | - | - | - |
| `language` | `union` | `False` | ISO 639-1 language code for the announcement text. Typically 'fi' (Finnish). | - | - | - |
| `sender` | `union` | `False` | Traffic management center that issued the announcement (e.g. 'Fintraffic Tieliikennekeskus Tampere', 'Fintraffic Tieliikennekeskus Helsinki'). | - | - | - |
| `location_description` | `union` | `False` | Human-readable location description from the first announcement's location object, typically including road number, section, and municipality in Finnish. | - | - | - |
| `start_time` | `union` | `False` | ISO 8601 UTC timestamp for the start of the situation's time-and-duration window from the first announcement. Null if no time window is specified. | - | - | - |
| `end_time` | `union` | `False` | ISO 8601 UTC timestamp for the expected end of the situation. Null if the end time is unknown or the situation is open-ended. | - | - | - |
| `features_json` | `union` | `False` | JSON-serialized array of feature objects from the first announcement. Features describe traffic impacts such as lane closures, detours, or speed reductions. Null if no features are listed. | - | - | - |
| `road_work_phases_json` | `union` | `False` | JSON-serialized array of road work phase objects from the first announcement. Each phase includes work types, restrictions (speed limits, lane narrowing), severity, and independent time windows. Present only for 'road work' situations; null otherwise. | - | - | - |
| `comment` | `union` | `False` | Free-text comment from the first announcement, providing additional context such as detour instructions or situation details. | - | - | - |
| `additional_information` | `union` | `False` | Supplementary information text from the first announcement, often including a link to the Fintraffic traffic situation portal. | - | - | - |
| `contact_phone` | `union` | `False` | Contact telephone number for the issuing traffic management center (e.g. '02002100'). | - | - | - |
| `contact_email` | `union` | `False` | Contact email address for the issuing traffic management center. | - | - | - |
| `announcements_json` | `union` | `False` | JSON-serialized array of all announcement objects in the situation, preserving the full upstream structure including nested location details, road addresses, ALERT-C codes, road work phases, restrictions, and work types. Provided for consumers needing the complete upstream detail beyond the flattened first-announcement fields. | - | - | - |
| `geometry_type` | `union` | `False` | GeoJSON geometry type of the situation's spatial extent (e.g. 'Point', 'LineString', 'MultiLineString'). Null if no geometry is available. | - | - | - |
| `geometry_coordinates_json` | `union` | `False` | JSON-serialized GeoJSON coordinates array for the situation's spatial extent. Coordinates are in [longitude, latitude] order per the GeoJSON specification (WGS84). Null if no geometry is available. | - | - | - |

### Schemagroup `fi.digitraffic.road.maintenance.jstruct`
<a id="schemagroup-fidigitrafficroadmaintenancejstruct"></a>

#### Schema `fi.digitraffic.road.maintenance.MaintenanceTracking`
<a id="schema-fidigitrafficroadmaintenancemaintenancetracking"></a>

| Field | Value |
| --- | --- |
| Name | MaintenanceTracking |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/maintenance/MaintenanceTracking` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `MaintenanceTracking`
<a id="schema-node-maintenancetracking"></a>

Road maintenance vehicle tracking update from the Finnish national road network operated by Fintraffic. Each message represents a position and task report from a maintenance vehicle, delivered in real time via the Digitraffic MQTT stream at wss://tie.digitraffic.fi/mqtt on topic maintenance-v2/routes/{domain}. Data originates from the Finnish Transport Infrastructure Agency's Harja system for state roads and from municipal systems for other domains. Updates arrive approximately every minute. A new tracking event is created when the vehicle's task changes, the gap between consecutive positions exceeds 5 minutes, or the calculated speed exceeds 140 km/h. See https://www.digitraffic.fi/en/road-traffic/ for the full API documentation and task type taxonomy at /api/maintenance/v1/tracking/tasks.

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/maintenance/MaintenanceTracking` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `domain` | `string` | `True` | Data domain identifying the source system. Primary domain is 'state-roads' for data from the Finnish Transport Infrastructure Agency's Harja system. Other domains include municipal systems such as 'autori-kuopio', 'autori-oulu', and 'paikannin-kuopio'. The domain value comes from the MQTT topic path. | - | - | - |
| `time` | `int32` | `True` | Tracking timestamp as Unix epoch seconds (UTC). Indicates when the position and task were recorded by the vehicle. | - | - | - |
| `source` | `union` | `False` | Name of the source system that produced the tracking data (e.g. 'Harja/Väylävirasto' for the state road maintenance system). May be null if the source system is not identified. | - | - | - |
| `tasks` | array of `string` | `True` | Array of maintenance task type identifiers being performed by the vehicle at this position. Task types follow the Fintraffic taxonomy, e.g. 'BRUSHING', 'SALTING', 'PLOUGHING_AND_SLUSH_REMOVAL', 'LEVELLING_GRAVEL_ROAD_SURFACE'. Full task type list with Finnish, English, and Swedish names is available at /api/maintenance/v1/tracking/tasks. | - | - | - |
| `x` | `double` | `True` | Longitude of the vehicle position in WGS84 (EPSG:4326) decimal degrees. | - | - | - |
| `y` | `double` | `True` | Latitude of the vehicle position in WGS84 (EPSG:4326) decimal degrees. | - | - | - |
| `direction` | `union` | `False` | Vehicle heading in degrees (0-360, clockwise from north). May be null or absent if heading information is not available from the tracking device. | - | - | - |

### Schemagroup `fi.digitraffic.road.stations.jstruct`
<a id="schemagroup-fidigitrafficroadstationsjstruct"></a>

#### Schema `fi.digitraffic.road.stations.TmsStation`
<a id="schema-fidigitrafficroadstationstmsstation"></a>

| Field | Value |
| --- | --- |
| Name | TmsStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/stations/TmsStation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `TmsStation`
<a id="schema-node-tmsstation"></a>

Traffic Measurement System (TMS) station metadata from the Finnish national road network operated by Fintraffic. Each TMS station is a fixed roadside installation that measures traffic volumes and speeds. Over 500 TMS stations are deployed across the Finnish road network. Station metadata includes geographic location, road address, municipality, available sensor list, free-flow reference speeds, and collection status. This reference data contextualizes the real-time TmsSensorData telemetry events and is fetched from the Digitraffic REST API at https://tie.digitraffic.fi/api/tms/v1/stations. See https://www.digitraffic.fi/en/road-traffic/lam/ for full TMS station documentation.

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/stations/TmsStation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `int32` | `True` | TMS station numeric identifier as assigned by Fintraffic (e.g. 23001). Unique across all TMS stations in the Finnish road network. Corresponds to the station_id in TmsSensorData telemetry events. | - | - | - |
| `name` | `string` | `True` | Internal station name used by Fintraffic, typically encoding road and location (e.g. "vt7_Rita"). Not intended for display; use names_fi/sv/en for human-readable names. | - | - | - |
| `tms_number` | `union` | `False` | Legacy TMS numbering used in older Fintraffic systems. May differ from station_id. Null if not assigned. | - | - | - |
| `names_fi` | `string` | `False` | Finnish display name for the station, typically including road number, municipality, and local area (e.g. "Tie 7 Porvoo, Rita"). | - | - | - |
| `names_sv` | `union` | `False` | Swedish display name for the station (e.g. "Väg 7 Borgå, Rita"). Null if no Swedish translation is available. | - | - | - |
| `names_en` | `union` | `False` | English display name for the station (e.g. "Road 7 Porvoo, Rita"). Null if no English translation is available. | - | - | - |
| `longitude` | `double` | `True` | Station longitude in WGS84 (EPSG:4326) decimal degrees. | - | - | - |
| `latitude` | `double` | `True` | Station latitude in WGS84 (EPSG:4326) decimal degrees. | - | - | - |
| `altitude` | `union` | `False` | Station altitude in meters above sea level. Null or 0.0 if altitude data is not available. | - | - | - |
| `municipality` | `string` | `True` | Name of the Finnish municipality where the station is located (e.g. "Porvoo", "Espoo"). | - | - | - |
| `municipality_code` | `int32` | `True` | Finnish municipality code as defined by Statistics Finland (e.g. 638 for Porvoo, 49 for Espoo). | - | - | - |
| `province` | `string` | `True` | Name of the Finnish province (maakunta) where the station is located (e.g. "Uusimaa", "Pirkanmaa"). | - | - | - |
| `province_code` | `int32` | `True` | Finnish province code as defined by Statistics Finland (e.g. 1 for Uusimaa). | - | - | - |
| `road_number` | `int32` | `True` | Finnish road number where the station is installed (e.g. 7 for Highway 7 / E18). | - | - | - |
| `road_section` | `int32` | `True` | Road section number within the road, part of the Finnish road addressing system. | - | - | - |
| `distance_from_section_start` | `int32` | `False` | Distance from the start of the road section in meters, part of the Finnish road addressing system. | - | - | - |
| `carriageway` | `union` | `False` | Carriageway type at the station location. Values from the Digitraffic API include "DUAL_CARRIAGEWAY_RIGHT_IN_INCREASING_DIRECTION", "DUAL_CARRIAGEWAY_LEFT_IN_INCREASING_DIRECTION", "ONE_CARRIAGEWAY". Null if not specified. | - | - | - |
| `side` | `union` | `False` | Side of the road where the station is located. Values: "LEFT", "RIGHT", "BETWEEN", "UNKNOWN". Null if not specified. | - | - | - |
| `station_type` | `string` | `True` | TMS station type code indicating the hardware configuration (e.g. "DSL_6" for a 6-loop DSL station). Determines which sensor families are available. | - | - | - |
| `collection_status` | `string` | `True` | Current data collection status of the station. Values: "GATHERING" (actively collecting), "REMOVED_TEMPORARILY", "REMOVED_PERMANENTLY". Only stations with GATHERING status produce telemetry. | - | - | - |
| `state` | `union` | `False` | Operational state of the station hardware. Values include "OK", "FAULT", "DISABLED". Null if state information is not available. | - | - | - |
| `free_flow_speed_1` | `union` | `False` | Reference free-flow speed for traffic direction 1 in km/h. Used to calculate traffic fluency ratios for VVAPAAS-suffixed sensors. Null if not calibrated. | - | - | - |
| `free_flow_speed_2` | `union` | `False` | Reference free-flow speed for traffic direction 2 in km/h. Used to calculate traffic fluency ratios. Null if not calibrated or station is on a one-way road. | - | - | - |
| `bearing` | `union` | `False` | Bearing of the road at the station in degrees (0-360, clockwise from north). Indicates the direction of increasing road section numbering. Null if not measured. | - | - | - |
| `start_time` | `string` | `True` | ISO 8601 UTC timestamp when the station started collecting data (e.g. "2001-11-07T00:00:00Z"). | - | - | - |
| `livi_id` | `union` | `False` | Legacy identifier used by the Finnish Transport Infrastructure Agency (Väylävirasto, formerly Liikennevirasto) for the station (e.g. "Livi968639"). Null if not assigned. | - | - | - |
| `sensors` | array of `int32` | `True` | Array of computational sensor identifiers available at this station. Each ID corresponds to a sensor that produces TmsSensorData telemetry events. Common sensor families: OHITUKSET (passings), KESKINOPEUS (average speed), LIUKUVA_NOPEUS (rolling speed). Sensor metadata is available at /api/tms/v1/sensors. | - | - | - |
| `data_updated_time` | `union` | `False` | ISO 8601 UTC timestamp when the station metadata was last updated in the Digitraffic system. Null if not tracked. | - | - | - |

#### Schema `fi.digitraffic.road.stations.WeatherStation`
<a id="schema-fidigitrafficroadstationsweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/stations/WeatherStation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherStation`
<a id="schema-node-weatherstation"></a>

Road weather station metadata from the Finnish national road network operated by Fintraffic. Over 350 road weather stations measure atmospheric and road surface conditions. Station metadata includes geographic location, road address, municipality, sensor list, collection parameters, and administrative details. This reference data contextualizes the real-time WeatherSensorData telemetry events and is fetched from the Digitraffic REST API at https://tie.digitraffic.fi/api/weather/v1/stations. See https://www.digitraffic.fi/en/road-traffic/ for full documentation.

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/stations/WeatherStation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `int32` | `True` | Road weather station numeric identifier as assigned by Fintraffic (e.g. 1012). Uniqueness scope is road weather stations. Corresponds to the station_id in WeatherSensorData telemetry events. | - | - | - |
| `name` | `string` | `True` | Internal station name used by Fintraffic, typically encoding road type, municipality and area (e.g. "kt51_Espoo_Kivenlahti"). Not intended for display. | - | - | - |
| `names_fi` | `string` | `False` | Finnish display name for the station (e.g. "Tie 51 Espoo, Kivenlahti"). | - | - | - |
| `names_sv` | `union` | `False` | Swedish display name for the station (e.g. "Väg 51 Esbo, Stensvik"). Null if no translation available. | - | - | - |
| `names_en` | `union` | `False` | English display name for the station (e.g. "Road 51 Espoo, Kivenlahti"). Null if no translation available. | - | - | - |
| `longitude` | `double` | `True` | Station longitude in WGS84 (EPSG:4326) decimal degrees. | - | - | - |
| `latitude` | `double` | `True` | Station latitude in WGS84 (EPSG:4326) decimal degrees. | - | - | - |
| `altitude` | `union` | `False` | Station altitude in meters above sea level. Null or 0.0 if altitude data is not available. | - | - | - |
| `municipality` | `string` | `True` | Name of the Finnish municipality where the station is located. | - | - | - |
| `municipality_code` | `int32` | `True` | Finnish municipality code as defined by Statistics Finland. | - | - | - |
| `province` | `string` | `True` | Name of the Finnish province (maakunta) where the station is located. | - | - | - |
| `province_code` | `int32` | `True` | Finnish province code as defined by Statistics Finland. | - | - | - |
| `road_number` | `int32` | `True` | Finnish road number where the station is installed. | - | - | - |
| `road_section` | `int32` | `True` | Road section number within the road. | - | - | - |
| `distance_from_section_start` | `int32` | `False` | Distance from the start of the road section in meters. | - | - | - |
| `carriageway` | `union` | `False` | Carriageway type at the station location. Values include "DUAL_CARRIAGEWAY_RIGHT_IN_INCREASING_DIRECTION", "DUAL_CARRIAGEWAY_LEFT_IN_INCREASING_DIRECTION", "ONE_CARRIAGEWAY". Null if not specified. | - | - | - |
| `side` | `union` | `False` | Side of the road. Values: "LEFT", "RIGHT", "BETWEEN", "UNKNOWN". Null if not specified. | - | - | - |
| `contract_area` | `union` | `False` | Road maintenance contract area name (e.g. "Espoo 19-24"). Identifies the maintenance contract responsible for the road section. Null if not assigned. | - | - | - |
| `contract_area_code` | `union` | `False` | Numeric code for the maintenance contract area (e.g. 142). Null if not assigned. | - | - | - |
| `station_type` | `string` | `True` | Weather station type code indicating the hardware configuration (e.g. "RWS_200" for a Rosa RWS-200 station). Determines available sensor capabilities. | - | - | - |
| `master` | `boolean` | `True` | Whether this is a master station. Master stations are the primary data source; non-master stations may be auxiliary or backup installations at the same location. | - | - | - |
| `collection_status` | `string` | `True` | Current data collection status. Values: "GATHERING" (actively collecting), "REMOVED_TEMPORARILY", "REMOVED_PERMANENTLY". | - | - | - |
| `collection_interval` | `int32` | `True` | Data collection interval in seconds. Typical value is 300 (5 minutes) for road weather stations. | - | - | - |
| `state` | `union` | `False` | Operational state of the station hardware. Null if state information is not available from the upstream API. | - | - | - |
| `start_time` | `string` | `True` | ISO 8601 UTC timestamp when the station started collecting data. | - | - | - |
| `livi_id` | `union` | `False` | Legacy identifier from the Finnish Transport Infrastructure Agency. Null if not assigned. | - | - | - |
| `sensors` | array of `int32` | `True` | Array of sensor identifiers available at this station. Each ID corresponds to a sensor producing WeatherSensorData telemetry. Common sensors: ILMA (1, air temp), TIE_1 (3, road surface temp), KASTEPISTE (9, dew point), KESKITUULI (16, avg wind), ILMAN_KOSTEUS (19, humidity). Full list at /api/weather/v1/sensors. | - | - | - |
| `data_updated_time` | `union` | `False` | ISO 8601 UTC timestamp when the station metadata was last updated. Null if not tracked. | - | - | - |

### Schemagroup `fi.digitraffic.road.maintenance.tasks.jstruct`
<a id="schemagroup-fidigitrafficroadmaintenancetasksjstruct"></a>

#### Schema `fi.digitraffic.road.maintenance.tasks.MaintenanceTaskType`
<a id="schema-fidigitrafficroadmaintenancetasksmaintenancetasktype"></a>

| Field | Value |
| --- | --- |
| Name | MaintenanceTaskType |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/maintenance/tasks/MaintenanceTaskType` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `MaintenanceTaskType`
<a id="schema-node-maintenancetasktype"></a>

Maintenance task type reference from the Finnish road maintenance system operated by Fintraffic. Each task type classifies a specific road maintenance activity such as ploughing, salting, or brush clearing. Task type identifiers appear in the tasks array of MaintenanceTracking telemetry events. This reference data provides multilingual human-readable names for each task identifier and is fetched from the Digitraffic REST API at https://tie.digitraffic.fi/api/maintenance/v1/tracking/tasks. Approximately 40 task types are defined. See https://www.digitraffic.fi/en/road-traffic/ for full documentation.

| Field | Value |
| --- | --- |
| $id | `https://fintraffic.fi/schemas/fi/digitraffic/road/maintenance/tasks/MaintenanceTaskType` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `task_id` | `string` | `True` | Unique task type identifier using SCREAMING_SNAKE_CASE convention (e.g. "PLOUGHING_AND_SLUSH_REMOVAL", "SALTING", "BRUSHING"). This identifier appears in the tasks array of MaintenanceTracking telemetry events. | - | - | - |
| `name_fi` | `string` | `True` | Finnish name for the maintenance task type (e.g. "Auraus ja sohjonpoisto", "Suolaus", "Harjaus"). | - | - | - |
| `name_en` | `string` | `True` | English name for the maintenance task type (e.g. "Ploughing and slush removal", "Salting", "Brushing"). | - | - | - |
| `name_sv` | `string` | `True` | Swedish name for the maintenance task type (e.g. "Plöjning och snöslaskborttagning", "Saltning", "Borstning"). | - | - | - |
| `data_updated_time` | `union` | `False` | ISO 8601 UTC timestamp when this task type definition was last updated in the Digitraffic system (e.g. "2020-03-30T00:00:00Z"). Null if not tracked. | - | - | - |
