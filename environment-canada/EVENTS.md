# Environment Canada — Event Catalog

## Topic: `environment-canada`

Key: `{msc_id}`

## Event Types

### CA.Gov.ECCC.Weather.Station

Reference data for a SWOB weather station.

| Field | Type | Unit | Description |
|---|---|---|---|
| `msc_id` | string | — | Meteorological Service of Canada station identifier |
| `name` | string | — | Station name (e.g. OTTAWA INTL A) |
| `iata_id` | string | — | IATA airport code where applicable |
| `wmo_id` | int | — | WMO synoptic station number |
| `province_territory` | string | — | Canadian province/territory code (ON, BC, QC, etc.) |
| `data_provider` | string | — | Data provider organization (MSC, DND, NRC, etc.) |
| `dataset_network` | string | — | Station network classification |
| `auto_man` | string | — | Automation type: Auto or Man |
| `latitude` | float | ° | WGS84 latitude |
| `longitude` | float | ° | WGS84 longitude |
| `elevation` | float | m | Station elevation above sea level |

### CA.Gov.ECCC.Weather.WeatherObservation

Hourly SWOB observation with core weather parameters extracted.

| Field | Type | Unit | Description |
|---|---|---|---|
| `msc_id` | string | — | MSC station identifier |
| `station_name` | string | — | Station name at observation time |
| `observation_time` | datetime | — | ISO 8601 UTC timestamp |
| `air_temperature` | float | °C | Air temperature |
| `dew_point` | float | °C | Dew point temperature |
| `relative_humidity` | int | % | Relative humidity |
| `station_pressure` | float | kPa | Station pressure |
| `wind_speed` | float | km/h | 10-minute average wind speed |
| `wind_direction` | int | ° | 10-minute average wind direction (degrees from true north) |
| `wind_gust` | float | km/h | Maximum wind gust in the past minute |
| `precipitation_1hr` | float | mm | Precipitation in the past hour |
