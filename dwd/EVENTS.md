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
- [DE.DWD.Radar](#message-group-dedwdradar)
  - [DE.DWD.Radar.RadarProductCatalog](#message-dedwdradarradarproductcatalog)
  - [DE.DWD.Radar.RadarFileProduct](#message-dedwdradarradarfileproduct)
- [DE.DWD.Forecast](#message-group-dedwdforecast)
  - [DE.DWD.Forecast.ForecastModelCatalog](#message-dedwdforecastforecastmodelcatalog)
  - [DE.DWD.Forecast.IconD2ForecastFile](#message-dedwdforecasticond2forecastfile)

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
## Message Group: DE.DWD.Radar
---
### Message: DE.DWD.Radar.RadarProductCatalog
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Radar.RadarProductCatalog` |
| `source` |  | `` | `False` | `https://opendata.dwd.de/weather/radar` |
| `subject` |  | `uritemplate` | `False` | `{file_path}` |

#### Schema:
##### Object: RadarProductCatalog
*Catalog metadata for a DWD radar product family emitted as reference data.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `product` | *string* | - | `True` | Radar product identifier derived from the first-level directory under weather/radar/composite. |
| `directory_path` | *string* | - | `True` | Relative DWD Open Data directory path for the radar product feed. |
| `description` | *string* | - | `False` | Human-readable product description configured by the bridge. |
| `file_path` | *string* | - | `True` | Relative path key for the radar product catalog record, typically the product directory path. |
---
### Message: DE.DWD.Radar.RadarFileProduct
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Radar.RadarFileProduct` |
| `source` |  | `` | `False` | `https://opendata.dwd.de/weather/radar` |
| `subject` |  | `uritemplate` | `False` | `{file_path}` |

#### Schema:
##### Object: RadarFileProduct
*Metadata event for a newly discovered or updated DWD radar product file.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `file_path` | *string* | - | `True` | Relative path of the emitted radar file under opendata.dwd.de used as Kafka key and CloudEvents subject. |
| `product` | *string* | - | `True` | Radar product identifier derived from the directory name. |
| `file_name` | *string* | - | `True` | Radar file name as listed in the DWD directory index. |
| `modified` | *string* | - | `True` | UTC last-modified timestamp from the directory listing in ISO-8601 format. |
| `size_bytes` | *int64* (optional) | - | `False` | File size in bytes parsed from the DWD listing, or null when size is unavailable. |
| `download_url` | *string* | - | `True` | Absolute HTTPS URL from which the radar product file can be downloaded. |
## Message Group: DE.DWD.Forecast
---
### Message: DE.DWD.Forecast.ForecastModelCatalog
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Forecast.ForecastModelCatalog` |
| `source` |  | `` | `False` | `https://opendata.dwd.de/weather/nwp/icon-d2` |
| `subject` |  | `uritemplate` | `False` | `{file_path}` |

#### Schema:
##### Object: ForecastModelCatalog
*Reference metadata describing a forecast model family exposed by DWD Open Data.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `model` | *string* | - | `True` | Forecast model identifier. For this bridge extension this value is icon-d2. |
| `base_path` | *string* | - | `True` | Relative DWD Open Data base path used to enumerate ICON-D2 GRIB products. |
| `description` | *string* | - | `False` | Human-readable description for the forecast model emitted as reference data. |
| `file_path` | *string* | - | `True` | Relative path key for the forecast model catalog record, typically the model base directory path. |
---
### Message: DE.DWD.Forecast.IconD2ForecastFile
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Forecast.IconD2ForecastFile` |
| `source` |  | `` | `False` | `https://opendata.dwd.de/weather/nwp/icon-d2` |
| `subject` |  | `uritemplate` | `False` | `{file_path}` |

#### Schema:
##### Object: IconD2ForecastFile
*Metadata event for a newly discovered or updated ICON-D2 forecast file from DWD Open Data.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `file_path` | *string* | - | `True` | Relative path of the ICON-D2 forecast file under opendata.dwd.de used as Kafka key and CloudEvents subject. |
| `model` | *string* | - | `True` | Forecast model identifier, currently icon-d2. |
| `file_name` | *string* | - | `True` | ICON-D2 file name as listed by the DWD directory index. |
| `run` | *string* (optional) | - | `False` | Model run cycle timestamp parsed from the file name (YYYYMMDDHH) when available. |
| `forecast_hour` | *int32* (optional) | - | `False` | Forecast lead time in hours parsed from the file name when available. |
| `parameter` | *string* (optional) | - | `False` | Forecast parameter token parsed from the file name when available. |
| `level_type` | *string* (optional) | - | `False` | Vertical level type token parsed from the file name when available. |
| `level` | *string* (optional) | - | `False` | Vertical level value token parsed from the file name when available. |
| `modified` | *string* | - | `True` | UTC last-modified timestamp from the directory listing in ISO-8601 format. |
| `size_bytes` | *int64* (optional) | - | `False` | File size in bytes parsed from the DWD listing, or null when size is unavailable. |
| `download_url` | *string* | - | `True` | Absolute HTTPS URL from which the forecast file can be downloaded. |
