# BOM Australia Weather Observations — Event Catalog

Events use [CloudEvents](https://cloudevents.io/) envelope format. Kafka key and CloudEvents subject both use `{station_wmo}`.

## Event Types

### AU.Gov.BOM.Weather.Station (Reference)

Station metadata emitted at startup for each configured BOM weather station.

| Field | Type | Description |
|-------|------|-------------|
| `station_wmo` | int32 | WMO station number |
| `name` | string | Station name |
| `product_id` | string | BOM product code |
| `state` | string | Australian state or territory |
| `time_zone` | string | Local time zone abbreviation |
| `latitude` | double | Station latitude (°) |
| `longitude` | double | Station longitude (°) |

### AU.Gov.BOM.Weather.WeatherObservation (Telemetry)

Half-hourly surface weather observation from an automatic weather station.

| Field | Type | Unit | Description |
|-------|------|------|-------------|
| `station_wmo` | int32 | | WMO station number |
| `station_name` | string | | Station name |
| `observation_time_utc` | datetime | | Observation timestamp (UTC) |
| `local_time` | string | | Local time (YYYYMMDDHHmmss) |
| `air_temp` | double? | °C | Air temperature |
| `apparent_temp` | double? | °C | Apparent (feels-like) temperature |
| `dewpt` | double? | °C | Dew point temperature |
| `rel_hum` | int32? | % | Relative humidity |
| `delta_t` | double? | °C | Wet bulb depression |
| `wind_dir` | string? | | Wind direction (compass) |
| `wind_spd_kmh` | int32? | km/h | Sustained wind speed |
| `wind_spd_kt` | int32? | kt | Sustained wind speed (knots) |
| `gust_kmh` | int32? | km/h | Maximum gust speed |
| `gust_kt` | int32? | kt | Maximum gust speed (knots) |
| `press` | double? | hPa | Station-level pressure |
| `press_qnh` | double? | hPa | QNH pressure |
| `press_msl` | double? | hPa | Mean sea level pressure |
| `press_tend` | string? | | Pressure tendency |
| `rain_trace` | string? | | Rainfall since 9am |
| `cloud` | string? | | Cloud cover description |
| `cloud_oktas` | int32? | | Cloud cover (0–8 oktas) |
| `cloud_base_m` | int32? | m | Cloud base height |
| `cloud_type` | string? | | Cloud type |
| `vis_km` | string? | | Horizontal visibility |
| `weather` | string? | | Present weather |
| `sea_state` | string? | | Sea state (coastal) |
| `swell_dir_worded` | string? | | Swell direction |
| `swell_height` | double? | m | Swell height |
| `swell_period` | double? | s | Swell period |
| `latitude` | double | ° | Station latitude |
| `longitude` | double | ° | Station longitude |
