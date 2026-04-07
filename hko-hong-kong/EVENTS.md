# HKO Hong Kong Weather — Event Catalog

## Topic: `hko-hong-kong`

Key: `{place_id}`

## Event Types

### HK.Gov.HKO.Weather.Station

Reference data for weather observation places in Hong Kong.

| Field | Type | Description |
|---|---|---|
| `place_id` | string | URL-safe slug identifier (e.g. `kings-park`, `central-and-western-district`) |
| `name` | string | Original English place name from HKO |
| `data_types` | string | Comma-separated data types: `temperature`, `rainfall`, `humidity`, `uvindex` |

### HK.Gov.HKO.Weather.WeatherObservation

Current weather observation for a place from the HKO rhrread endpoint.

| Field | Type | Unit | Description |
|---|---|---|---|
| `place_id` | string | — | URL-safe slug identifier |
| `place_name` | string | — | Original English place name |
| `observation_time` | datetime | — | ISO 8601 with Hong Kong offset (+08:00) |
| `temperature` | float | °C | Air temperature (weather stations only) |
| `rainfall_max` | float | mm | Maximum rainfall in past hour (districts only) |
| `humidity` | int | % | Relative humidity (HKO headquarters only) |
| `uv_index` | float | — | UV index (King's Park only) |
| `uv_description` | string | — | UV level: low, moderate, high, very high, extreme |
