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
| `district` | string | — | Hong Kong 18-district area (snake_case), e.g. `central-and-western` |
| `latitude` | float | ° | WGS84 latitude |
| `longitude` | float | ° | WGS84 longitude |

### HK.Gov.EPD.AQHI.AQHIReading

Latest AQHI reading emitted for each station from the 24-hour XML feed.

| Field | Type | Unit | Description |
|---|---|---|---|
| `station_id` | string | — | Stable snake_case station identifier |
| `station_name` | string | — | Station name from the EPD feed |
| `station_type` | string | — | `General Stations` or `Roadside Stations` |
| `district` | string | — | Hong Kong 18-district area (snake_case), e.g. `central-and-western` |
| `reading_time` | datetime | — | Observation timestamp in ISO 8601 |
| `aqhi` | integer | — | AQHI value, where values above 10 mean `10+` |
| `health_risk_category` | string | — | Derived risk category: Low, Moderate, High, Very High, or Serious |

## MQTT/UNS Topics

Topic tree: `air-quality/hk/epd/hongkong-epd/{district}/{station_id}/{event}`

| Leaf | CloudEvents Type | Description |
|---|---|---|
| `info` | `HK.Gov.EPD.AQHI.Station` | Station reference data |
| `aqhi` | `HK.Gov.EPD.AQHI.AQHIReading` | Latest AQHI reading |

All messages are published with QoS 1, retain=true, and CloudEvents binary
content mode (attributes as MQTT 5 user properties).
