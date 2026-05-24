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

---

## Message Group: US.EPA.UVIndex.mqtt

MQTT/5.0 transport variants for EPA UV Index forecasts. Topics are retained QoS-1 UV forecast leaves under uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/..., where {state} is lowercase US state, {city_slug} is lowercase kebab-case city, and {location_id} preserves the existing Kafka/CloudEvents entity id intentionally for subject/key compatibility even though it is derivable from state+city. Hourly slots use topic-safe {forecast_hour}=YYYYMMDDTHH; daily slots use {forecast_date}=YYYY-MM-DD. Message expiry bounds retained forecast slots so stale forecasts age out.

The MQTT transport uses MQTT 5.0 binary-mode CloudEvents: the payload is the JSON body for the referenced message schema, and CloudEvents metadata is carried as MQTT user properties. The MQTT messagegroup references the transport-neutral Kafka/CloudEvents message definitions through `basemessageurl`, so the schemas above remain authoritative.

### MQTT topics

| Topic pattern | Bound message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/hourly/{forecast_hour}` | `US.EPA.UVIndex.HourlyForecast` | `true` | `1` | `172800` |
| `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/daily/{forecast_date}` | `US.EPA.UVIndex.DailyForecast` | `true` | `1` | `1209600` |
