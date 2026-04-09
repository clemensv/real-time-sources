# EPA UV Bridge Events

This document describes the events emitted by the EPA UV bridge.

- [US.EPA.UVIndex](#message-group-usepauvindex)
  - [US.EPA.UVIndex.HourlyForecast](#message-usepauvindexhourlyforecast)
  - [US.EPA.UVIndex.DailyForecast](#message-usepauvindexdailyforecast)

---

## Message Group: US.EPA.UVIndex
---
### Message: US.EPA.UVIndex.HourlyForecast
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `US.EPA.UVIndex.HourlyForecast` |
| `source` |  | `` | `False` | `https://www.epa.gov/enviro/web-services` |
| `subject` |  | `uritemplate` | `False` | `{location_id}` |

#### Schema:
##### Object: HourlyForecast
*Hourly UV Index forecast for a configured city and state from the EPA Envirofacts UV hourly service.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `location_id` | *string* | - | `True` | Stable slug derived from the configured city and state. |
| `city` | *string* | - | `True` | City for which the hourly UV forecast was requested. |
| `state` | *string* | - | `True` | Two-letter state abbreviation for the requested city. |
| `forecast_datetime` | *string* | - | `True` | Forecast timestamp normalized to ISO local datetime form without an explicit UTC offset. |
| `uv_index` | *integer* | - | `True` | Hourly UV Index forecast value. |
---
### Message: US.EPA.UVIndex.DailyForecast
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `US.EPA.UVIndex.DailyForecast` |
| `source` |  | `` | `False` | `https://www.epa.gov/enviro/web-services` |
| `subject` |  | `uritemplate` | `False` | `{location_id}` |

#### Schema:
##### Object: DailyForecast
*Daily UV Index forecast and alert flag for a configured city and state from the EPA Envirofacts UV daily service.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `location_id` | *string* | - | `True` | Stable slug derived from the configured city and state. |
| `city` | *string* | - | `True` | City for which the daily UV forecast was requested. |
| `state` | *string* | - | `True` | Two-letter state abbreviation for the requested city. |
| `forecast_date` | *string* | - | `True` | Forecast date normalized to YYYY-MM-DD. |
| `uv_index` | *integer* | - | `True` | Daily UV Index forecast value. |
| `uv_alert` | *string* | - | `True` | Character flag indicating whether a UV alert is issued for the forecast day. |
