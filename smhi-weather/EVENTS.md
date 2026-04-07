# SMHI Weather — Event Catalog

## Topic: `smhi-weather`

Key: `{station_id}`

## Event Types

### SE.Gov.SMHI.Weather.Station

Reference data for an active SMHI meteorological station.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | SMHI station numeric identifier |
| `name` | string | — | Station name |
| `owner` | string | — | Station owner organization |
| `owner_category` | string | — | Owner category (e.g. SMHI, SOL) |
| `measuring_stations` | string | — | Station network classification |
| `height` | float | m | Station elevation above sea level |
| `latitude` | float | ° | WGS84 latitude |
| `longitude` | float | ° | WGS84 longitude |

### SE.Gov.SMHI.Weather.WeatherObservation

Hourly weather observation assembled from per-parameter bulk endpoints.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | SMHI station numeric identifier |
| `station_name` | string | — | Station name at observation time |
| `observation_time` | datetime | — | ISO 8601 UTC timestamp |
| `air_temperature` | float | °C | Instantaneous air temperature |
| `wind_gust` | float | m/s | Maximum wind gust in the last hour |
| `dew_point` | float | °C | Dew point temperature |
| `air_pressure` | float | hPa | Air pressure reduced to sea level |
| `relative_humidity` | int | % | Relative humidity |
| `precipitation_last_hour` | float | mm | Total precipitation in the last hour |
| `quality` | string | — | SMHI quality flag (G=Green/approved, Y=Yellow/suspect) |
