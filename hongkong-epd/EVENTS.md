# Hong Kong EPD AQHI — Event Catalog

## Topic: `hongkong-epd-aqhi`

Key: `{station_id}`

## Event Types

### HK.Gov.EPD.AQHI.Station

Reference data for Hong Kong EPD AQHI monitoring stations.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | Stable snake_case station identifier |
| `station_name` | string | — | Station name from the EPD feed |
| `station_type` | string | — | `General Stations` or `Roadside Stations` |
| `latitude` | float | ° | WGS84 latitude |
| `longitude` | float | ° | WGS84 longitude |

### HK.Gov.EPD.AQHI.AQHIReading

Latest AQHI reading emitted for each station from the 24-hour XML feed.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | Stable snake_case station identifier |
| `station_name` | string | — | Station name from the EPD feed |
| `station_type` | string | — | `General Stations` or `Roadside Stations` |
| `reading_time` | datetime | — | Observation timestamp in ISO 8601 |
| `aqhi` | integer | — | AQHI value, where values above 10 mean `10+` |
| `health_risk_category` | string | — | Derived risk category: Low, Moderate, High, Very High, or Serious |
