# LAQN London Air Quality Network Bridge Events

This document describes the CloudEvents emitted by the LAQN London Air Quality
Network bridge.

## Message Group: `uk.kcl.laqn`

### Message: `uk.kcl.laqn.Site`

Monitoring site reference data keyed by `site_code`.

| Attribute | Value |
|---|---|
| `type` | `uk.kcl.laqn.Site` |
| `source` | `http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=All/Json` |
| `subject` | `{site_code}` |
| Kafka key | `{site_code}` |

| Field | Type | Description |
|---|---|---|
| `site_code` | `string` | Stable LAQN site code. |
| `site_name` | `string` | Human-readable site name. |
| `site_type` | `string` | LAQN site classification. |
| `local_authority_code` | `string` | Local authority code. |
| `local_authority_name` | `string` | Local authority name. |
| `latitude` | `double` | WGS84 latitude in decimal degrees. |
| `longitude` | `double` | WGS84 longitude in decimal degrees. |
| `date_opened` | `string` | Opening timestamp in `YYYY-MM-DD HH:MM:SS` format. |
| `date_closed` | `string \| null` | Closure timestamp, or `null` for active sites. |
| `data_owner` | `string` | Organisation owning the data. |
| `data_manager` | `string` | Organisation managing the monitoring site. |

### Message: `uk.kcl.laqn.Measurement`

Hourly pollutant measurement keyed by `site_code`.

| Attribute | Value |
|---|---|
| `type` | `uk.kcl.laqn.Measurement` |
| `source` | `http://api.erg.ic.ac.uk/AirQuality/Data/Site` |
| `subject` | `{site_code}` |
| Kafka key | `{site_code}` |

| Field | Type | Description |
|---|---|---|
| `site_code` | `string` | Stable LAQN site code. |
| `species_code` | `string` | Pollutant code such as `NO2` or `PM10`. |
| `measurement_date_gmt` | `string` | GMT timestamp in `YYYY-MM-DD HH:MM:SS` format. |
| `value` | `double` | Measured pollutant concentration. Empty upstream values are skipped and do not produce events. |

### Message: `uk.kcl.laqn.DailyIndex`

Daily AQI bulletin record keyed by `site_code`.

| Attribute | Value |
|---|---|
| `type` | `uk.kcl.laqn.DailyIndex` |
| `source` | `http://api.erg.ic.ac.uk/AirQuality/Daily/MonitoringIndex/Latest/GroupName=London/Json` |
| `subject` | `{site_code}` |
| Kafka key | `{site_code}` |

| Field | Type | Description |
|---|---|---|
| `site_code` | `string` | Stable LAQN site code. |
| `bulletin_date` | `string` | Bulletin timestamp in `YYYY-MM-DD HH:MM:SS` format. |
| `species_code` | `string` | Pollutant code to which the Daily AQI value applies. |
| `air_quality_index` | `integer` | Daily AQI value from `1` to `10`. |
| `air_quality_band` | `string` | Band name: `Low`, `Moderate`, `High`, or `Very High`. |
| `index_source` | `string` | Source of the AQI value, typically `Measurement` or `Forecast`. |

## Message Group: `uk.kcl.laqn.species`

### Message: `uk.kcl.laqn.Species`

Pollutant catalog reference data keyed by `species_code`.

| Attribute | Value |
|---|---|
| `type` | `uk.kcl.laqn.Species` |
| `source` | `http://api.erg.ic.ac.uk/AirQuality/Information/Species/Json` |
| `subject` | `{species_code}` |
| Kafka key | `{species_code}` |

| Field | Type | Description |
|---|---|---|
| `species_code` | `string` | Stable pollutant code such as `NO2`, `O3`, `PM10`, or `PM25`. |
| `species_name` | `string` | Human-readable pollutant name. |
| `description` | `string` | Pollutant description published by LAQN. |
| `health_effect` | `string` | Health impact guidance published by LAQN. |
| `link` | `string` | HTTP URL to the upstream pollutant guidance page. |
