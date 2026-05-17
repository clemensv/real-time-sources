# DWD Open Data Bridge Events

This document describes the events emitted by the DWD Open Data bridge.

- [DE.DWD.CDC](#message-group-dedwdcdc)
  - [DE.DWD.CDC.StationMetadata](#message-dedwdcdcstationmetadata)
  - [DE.DWD.CDC.AirTemperature10Min](#message-dedwdcdcairtemperature10min)
  - [DE.DWD.CDC.Precipitation10Min](#message-dedwdcdcprecipitation10min)
  - [DE.DWD.CDC.Wind10Min](#message-dedwdcdcwind10min)
  - [DE.DWD.CDC.Solar10Min](#message-dedwdcdcsolar10min)
  - [DE.DWD.CDC.HourlyObservation](#message-dedwdcdchourlyobservation)
  - [DE.DWD.CDC.ExtremeWind10Min](#message-dedwdcdcextremewind10min)
  - [DE.DWD.CDC.ExtremeTemperature10Min](#message-dedwdcdcextremetemperature10min)
- [DE.DWD.Weather](#message-group-dedwdweather)
  - [DE.DWD.Weather.Alert](#message-dedwdweatheralert)

---

## Message Group: DE.DWD.CDC
---
### Message: DE.DWD.CDC.StationMetadata
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.StationMetadata` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: StationMetadata
*StationMetadata*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `station_name` | *string* | - | `True` |  |
| `latitude` | *double* | - | `True` |  |
| `longitude` | *double* | - | `True` |  |
| `elevation` | *double* | - | `True` |  |
| `state` | *string* | - | `False` |  |
| `from_date` | *string* | - | `False` |  |
| `to_date` | *string* | - | `False` |  |
---
### Message: DE.DWD.CDC.AirTemperature10Min
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.AirTemperature10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: AirTemperature10Min
*AirTemperature10Min*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `timestamp` | *string* | - | `True` |  |
| `quality_level` | *int32* | - | `False` |  |
| `pressure_station_level` | *double* | - | `False` |  |
| `air_temperature_2m` | *double* | - | `False` |  |
| `air_temperature_5cm` | *double* | - | `False` |  |
| `relative_humidity` | *double* | - | `False` |  |
| `dew_point_temperature` | *double* | - | `False` |  |
---
### Message: DE.DWD.CDC.Precipitation10Min
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Precipitation10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Precipitation10Min
*Precipitation10Min*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `timestamp` | *string* | - | `True` |  |
| `quality_level` | *int32* | - | `False` |  |
| `precipitation_height` | *double* | - | `False` |  |
| `precipitation_indicator` | *int32* | - | `False` |  |
---
### Message: DE.DWD.CDC.Wind10Min
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Wind10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Wind10Min
*Wind10Min*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `timestamp` | *string* | - | `True` |  |
| `quality_level` | *int32* | - | `False` |  |
| `wind_speed` | *double* | - | `False` |  |
| `wind_direction` | *double* | - | `False` |  |
---
### Message: DE.DWD.CDC.Solar10Min
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.Solar10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: Solar10Min
*Solar10Min*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `timestamp` | *string* | - | `True` |  |
| `quality_level` | *int32* | - | `False` |  |
| `global_radiation` | *double* | - | `False` |  |
| `sunshine_duration` | *double* | - | `False` |  |
| `diffuse_radiation` | *double* | - | `False` |  |
| `longwave_radiation` | *double* | - | `False` |  |
---
### Message: DE.DWD.CDC.HourlyObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.HourlyObservation` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: HourlyObservation
*HourlyObservation*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `timestamp` | *string* | - | `True` |  |
| `quality_level` | *int32* | - | `False` |  |
| `parameter` | *string* | - | `True` |  |
| `value` | *double* | - | `False` |  |
| `unit` | *string* | - | `False` |  |
---
### Message: DE.DWD.CDC.ExtremeWind10Min
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.ExtremeWind10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: ExtremeWind10Min
*ExtremeWind10Min*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `timestamp` | *string* | - | `True` |  |
| `quality_level` | *int32* | - | `False` |  |
| `wind_speed_maximum` | *double* | - | `False` |  |
| `wind_speed_minimum` | *double* | - | `False` |  |
| `wind_direction_at_maximum` | *double* | - | `False` |  |
---
### Message: DE.DWD.CDC.ExtremeTemperature10Min
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.CDC.ExtremeTemperature10Min` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: ExtremeTemperature10Min
*ExtremeTemperature10Min*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` |  |
| `timestamp` | *string* | - | `True` |  |
| `quality_level` | *int32* | - | `False` |  |
| `air_temperature_maximum_2m` | *double* | - | `False` |  |
| `air_temperature_minimum_5cm` | *double* | - | `False` |  |
## Message Group: DE.DWD.Weather
---
### Message: DE.DWD.Weather.Alert
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Weather.Alert` |
| `source` |  | `` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |

#### Schema:
##### Object: Alert
*Alert*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `identifier` | *string* | - | `True` |  |
| `sender` | *string* | - | `True` |  |
| `sent` | *string* | - | `True` |  |
| `status` | *string* | - | `False` |  |
| `msg_type` | *string* | - | `False` |  |
| `severity` | *string* | - | `True` |  |
| `urgency` | *string* | - | `False` |  |
| `certainty` | *string* | - | `False` |  |
| `event` | *string* | - | `True` |  |
| `headline` | *string* | - | `False` |  |
| `description` | *string* | - | `False` |  |
| `effective` | *string* | - | `False` |  |
| `onset` | *string* | - | `False` |  |
| `expires` | *string* | - | `False` |  |
| `area_desc` | *string* | - | `False` |  |
| `geocodes` | *string* | - | `False` |  |
