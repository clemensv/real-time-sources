# Singapore NEA Weather and Air Quality — Event Catalog

## Topic: `singapore-nea`

Key: `{station_id}`

### SG.Gov.NEA.Weather.Station

Reference data for NEA weather observation stations.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | NEA station ID, e.g. `S109` |
| `device_id` | string | — | Device identifier from the metadata feed |
| `name` | string | — | Station location name |
| `latitude` | float | ° | WGS84 latitude |
| `longitude` | float | ° | WGS84 longitude |
| `data_types` | string | — | Comma-separated weather measurement families reported by the station |

### SG.Gov.NEA.Weather.WeatherObservation

Real-time weather observation assembled from multiple NEA endpoints.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | NEA station ID |
| `station_name` | string | — | Station location name |
| `observation_time` | datetime | — | Observation timestamp in ISO 8601 |
| `air_temperature` | float | °C | Air temperature |
| `rainfall` | float | mm | Rainfall in the last 5 minutes |
| `relative_humidity` | float | % | Relative humidity |
| `wind_speed` | float | kn | Wind speed |
| `wind_direction` | float | ° | Wind direction from true north |

## Topic: `singapore-nea-airquality`

Key: `{region}`

### SG.Gov.NEA.AirQuality.Region

Reference data for NEA air-quality reporting regions.

| Field | Type | Unit | Description |
|---|---|---|---|
| `region` | string | — | Region identifier: west, east, central, south, north |
| `latitude` | float | ° | WGS84 latitude of the region label point |
| `longitude` | float | ° | WGS84 longitude of the region label point |

### SG.Gov.NEA.AirQuality.PSIReading

Hourly Pollutant Standards Index reading for one region.

| Field | Type | Unit | Description |
|---|---|---|---|
| `region` | string | — | Region identifier |
| `timestamp` | datetime | — | Reading timestamp in ISO 8601 |
| `update_timestamp` | datetime | — | NEA update timestamp in ISO 8601 |
| `psi_twenty_four_hourly` | integer | — | Overall 24-hour PSI |
| `o3_sub_index` | integer | — | Ozone PSI sub-index |
| `pm10_sub_index` | integer | — | PM10 PSI sub-index |
| `pm10_twenty_four_hourly` | integer | µg/m³ | PM10 24-hour concentration |
| `pm25_sub_index` | integer | — | PM2.5 PSI sub-index |
| `pm25_twenty_four_hourly` | integer | µg/m³ | PM2.5 24-hour concentration |
| `co_sub_index` | integer | — | Carbon monoxide PSI sub-index |
| `co_eight_hour_max` | integer | mg/m³ | Carbon monoxide 8-hour maximum |
| `so2_sub_index` | integer | — | Sulphur dioxide PSI sub-index |
| `so2_twenty_four_hourly` | integer | µg/m³ | Sulphur dioxide 24-hour concentration |
| `no2_one_hour_max` | integer | µg/m³ | Nitrogen dioxide 1-hour maximum |
| `o3_eight_hour_max` | integer | µg/m³ | Ozone 8-hour maximum |

### SG.Gov.NEA.AirQuality.PM25Reading

Hourly PM2.5 concentration for one region.

| Field | Type | Unit | Description |
|---|---|---|---|
| `region` | string | — | Region identifier |
| `timestamp` | datetime | — | Reading timestamp in ISO 8601 |
| `update_timestamp` | datetime | — | NEA update timestamp in ISO 8601 |
| `pm25_one_hourly` | integer | µg/m³ | PM2.5 one-hour concentration |
