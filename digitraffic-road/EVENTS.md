# Digitraffic Road — Finnish Road Sensor Events

The bridge emits CloudEvents in structured JSON format to Kafka-compatible
endpoints. Data is streamed in real time from the Digitraffic MQTT service at
`wss://tie.digitraffic.fi/mqtt`.

## Event Metadata

- `source`: `wss://tie.digitraffic.fi/mqtt`
- `subject`: `{station_id}/{sensor_id}`
- Kafka key: `{station_id}/{sensor_id}`

## Event Types

| Event type | Payload schema | MQTT source topic |
|---|---|---|
| `fi.digitraffic.road.sensors.TmsSensorData` | `TmsSensorData` | `tms-v2/{stationId}/{sensorId}` |
| `fi.digitraffic.road.sensors.WeatherSensorData` | `WeatherSensorData` | `weather-v2/{stationId}/{sensorId}` |

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
