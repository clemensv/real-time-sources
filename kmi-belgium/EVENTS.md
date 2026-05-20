# KMI Belgium Weather — Event Catalog

## Topic: `kmi-belgium`

Key: `{station_code}`

## Event Types

### BE.Gov.KMI.Weather.Station

Reference data for an active KMI/RMI automatic weather station.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_code` | string | — | KMI/RMI station code from the upstream `code` property |
| `latitude` | double | ° | WGS84 latitude from GeoJSON coordinates |
| `longitude` | double | ° | WGS84 longitude from GeoJSON coordinates |

### BE.Gov.KMI.Weather.WeatherObservation

Ten-minute weather observation from the `aws:aws_10min` feed.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_code` | string | — | KMI/RMI station code from the upstream `code` property |
| `observation_time` | datetime | — | ISO 8601 UTC timestamp from the upstream `timestamp` property |
| `precip_quantity` | double \| null | mm | Precipitation quantity during the 10-minute period |
| `temp_dry_shelter_avg` | double \| null | °C | Average air temperature in the dry shelter |
| `temp_grass_pt100_avg` | double \| null | °C | Average grass-level temperature measured by the Pt100 sensor |
| `temp_soil_avg` | double \| null | °C | Average soil surface temperature |
| `temp_soil_avg_5cm` | double \| null | °C | Average soil temperature at 5 cm depth |
| `temp_soil_avg_10cm` | double \| null | °C | Average soil temperature at 10 cm depth |
| `temp_soil_avg_20cm` | double \| null | °C | Average soil temperature at 20 cm depth |
| `temp_soil_avg_50cm` | double \| null | °C | Average soil temperature at 50 cm depth |
| `wind_speed_10m` | double \| null | m/s | Wind speed at 10 m height |
| `wind_speed_avg_30m` | double \| null | m/s | Average wind speed at 30 m height |
| `wind_direction` | double \| null | ° | Wind direction in degrees |
| `wind_gusts_speed` | double \| null | m/s | Maximum wind gust speed during the period |
| `humidity_rel_shelter_avg` | double \| null | % | Average relative humidity |
| `pressure` | double \| null | hPa | Station-level atmospheric pressure |
| `sun_duration` | double \| null | min | Sunshine duration in the 10-minute period |
| `short_wave_from_sky_avg` | double \| null | W/m² | Average shortwave downward radiation from the sky |
| `sun_int_avg` | double \| null | W/m² | Average direct sunshine intensity |
