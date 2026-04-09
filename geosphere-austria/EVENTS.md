# Events for `at.geosphere.tawes`

## Message Group: `at.geosphere.tawes`

**Topic:** `geosphere-austria-tawes`
**Key:** `{station_id}`

### `at.geosphere.tawes.WeatherStation`

Reference data for a GeoSphere Austria TAWES automatic weather station,
including location, elevation, and federal state.

- **CloudEvents type:** `at.geosphere.tawes.WeatherStation`
- **CloudEvents source:** `https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min/metadata`
- **Subject:** `{station_id}`

| Field | Type | Description |
|---|---|---|
| `station_id` | string | Stable GeoSphere Austria numeric station identifier |
| `station_name` | string | Station name from metadata |
| `latitude` | double | WGS84 latitude in decimal degrees |
| `longitude` | double | WGS84 longitude in decimal degrees |
| `altitude` | double | Altitude above sea level in meters |
| `state` | string ∣ null | Austrian federal state (Bundesland) |

### `at.geosphere.tawes.WeatherObservation`

10-minute weather observation from a GeoSphere Austria TAWES station.

- **CloudEvents type:** `at.geosphere.tawes.WeatherObservation`
- **CloudEvents source:** `https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min`
- **Subject:** `{station_id}`

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | GeoSphere station identifier |
| `observation_time` | string | — | ISO-8601 timestamp |
| `temperature` | double ∣ null | °C | Air temperature (TL) |
| `humidity` | double ∣ null | % | Relative humidity (RF) |
| `precipitation` | double ∣ null | mm | Precipitation 10-min (RR) |
| `wind_direction` | double ∣ null | ° | Wind direction (DD) |
| `wind_speed` | double ∣ null | m/s | Wind speed (FF) |
| `pressure` | double ∣ null | hPa | Atmospheric pressure (P) |
| `sunshine_duration` | double ∣ null | s | Sunshine duration (SO) |
| `global_radiation` | double ∣ null | W/m² | Global radiation (GLOW) |
