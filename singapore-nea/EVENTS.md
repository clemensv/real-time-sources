# Singapore NEA Weather — Event Catalog

## Topic: `singapore-nea`

Key: `{station_id}`

## Event Types

### SG.Gov.NEA.Weather.Station

Reference data for NEA weather observation stations.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | NEA station ID (e.g. S109, S50) |
| `device_id` | string | — | Device identifier |
| `name` | string | — | Station location name |
| `latitude` | float | ° | WGS84 latitude |
| `longitude` | float | ° | WGS84 longitude |
| `data_types` | string | — | Comma-separated: air_temperature, rainfall, relative_humidity, wind_speed, wind_direction |

### SG.Gov.NEA.Weather.WeatherObservation

Real-time weather observation assembled from multiple NEA endpoints.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | NEA station ID |
| `station_name` | string | — | Station location name |
| `observation_time` | datetime | — | ISO 8601 with Singapore offset (+08:00) |
| `air_temperature` | float | °C | Air temperature (1-min update) |
| `rainfall` | float | mm | Rainfall in last 5 minutes |
| `relative_humidity` | float | % | Relative humidity |
| `wind_speed` | float | kn | Wind speed |
| `wind_direction` | float | ° | Wind direction from true north |
