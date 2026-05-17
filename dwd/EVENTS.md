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
| `subject` |  | `uritemplate` | `False` | `{file_url}` |

#### Schema:
##### Object: RadarProductCatalog
*Reference (catalog) event describing a single DWD radar composite product family. One event is emitted per product directory the first time the bridge observes it, so consumers can build a catalog of available products and the URLs from which their files can be discovered.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `product` | *string* | - | `True` | Short identifier of the DWD radar composite product family (for example 'wn', 'rv', 'rs', 'dmax', 'hg', 'hx', 'pg', 'vii', 'hymecng'). Derived from the first-level directory name under https://opendata.dwd.de/weather/radar/composite/. All RadarFileProduct events for files inside this directory carry the same product value. |
| `file_url` | *string* | - | `True` | Absolute HTTPS URL of the DWD Open Data directory that holds all files for this radar product. The URL is publicly fetchable with an unauthenticated HTTP GET and returns an Apache autoindex HTML listing, so consumers can enumerate current and historical product files without credentials. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key for catalog events. Example: 'https://opendata.dwd.de/weather/radar/composite/wn/'. |
| `description` | *string* | - | `False` | Optional human-readable description of the radar product as configured by the bridge. Intended for catalog browsers, documentation, and operator UIs; not derived from upstream metadata. |
---
### Message: DE.DWD.Radar.RadarFileProduct
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Radar.RadarFileProduct` |
| `source` |  | `` | `False` | `https://opendata.dwd.de/weather/radar` |
| `subject` |  | `uritemplate` | `False` | `{file_url}` |

#### Schema:
##### Object: RadarFileProduct
*Telemetry-style event announcing that a single DWD radar composite product file has appeared or been updated on the Open Data server. The event carries enough metadata to fetch the file directly via an unauthenticated HTTPS GET against file_url; it does not embed the file payload.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `file_url` | *string* | - | `True` | Absolute HTTPS URL of a single DWD radar product file on the DWD Open Data server. The URL is publicly fetchable with an unauthenticated HTTP GET and supports HTTP Range and If-Modified-Since/ETag conditional requests, so handlers can dereference the event by performing a plain GET against this URL. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key, which guarantees per-file ordering. Example: 'https://opendata.dwd.de/weather/radar/composite/wn/composite_wn_20260517_2005-hd5'. |
| `product` | *string* | - | `True` | Short identifier of the radar product family this file belongs to (for example 'wn', 'rv', 'dmax'); matches the 'product' field of the corresponding RadarProductCatalog event. |
| `file_name` | *string* | - | `True` | Bare file name (no directory component) as listed in the DWD Apache directory index. Convenient for parsing the embedded product code and observation timestamp without having to split file_url. |
| `modified` | *string* | - | `True` | Upstream Last-Modified timestamp of the file as reported by the DWD Apache directory listing, expressed as an ISO 8601 UTC string. The bridge emits a new RadarFileProduct event whenever this value changes for a known file_url, so consumers can use it for change detection and de-duplication. |
| `size_bytes` | *int64* (optional) | - | `False` | File size in bytes as parsed from the DWD directory listing, or null when the listing does not expose a size. Indicative only; for an authoritative size consumers should rely on the Content-Length header returned by the actual GET on file_url. Radar composite files typically range from tens of KB (BUFR products) up to roughly 10 MB (large HDF5 composites). |
## Message Group: DE.DWD.Forecast
---
### Message: DE.DWD.Forecast.ForecastModelCatalog
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Forecast.ForecastModelCatalog` |
| `source` |  | `` | `False` | `https://opendata.dwd.de/weather/nwp/icon-d2` |
| `subject` |  | `uritemplate` | `False` | `{file_url}` |

#### Schema:
##### Object: ForecastModelCatalog
*Reference (catalog) event describing a single NWP forecast model family published by DWD Open Data. One event is emitted per model the first time the bridge observes it, so consumers can build a catalog of available models and the URLs from which their forecast files can be discovered.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `model` | *string* | - | `True` | Identifier of the numerical weather prediction (NWP) model. For this bridge release the value is 'icon-d2', referring to the DWD ICON-D2 convection-permitting regional model covering Germany and surrounding areas with ~2 km horizontal resolution and forecast lead times up to 48 hours. |
| `file_url` | *string* | - | `True` | Absolute HTTPS URL of the DWD Open Data root directory under which all GRIB2 files for this forecast model are published. The URL is publicly fetchable with an unauthenticated HTTP GET and returns an Apache autoindex HTML listing. Run-hour subdirectories (e.g. '00/', '03/', '06/', ...) and per-variable subdirectories live below this URL. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key for catalog events. Example: 'https://opendata.dwd.de/weather/nwp/icon-d2/grib/'. |
| `description` | *string* | - | `False` | Optional human-readable description of the forecast model emitted as reference data. Intended for catalog browsers, documentation, and operator UIs; not derived from upstream metadata. |
---
### Message: DE.DWD.Forecast.IconD2ForecastFile
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `DE.DWD.Forecast.IconD2ForecastFile` |
| `source` |  | `` | `False` | `https://opendata.dwd.de/weather/nwp/icon-d2` |
| `subject` |  | `uritemplate` | `False` | `{file_url}` |

#### Schema:
##### Object: IconD2ForecastFile
*Telemetry-style event announcing that a single ICON-D2 GRIB2 forecast file has appeared or been updated on the DWD Open Data server. The event carries enough metadata to fetch the file directly via an unauthenticated HTTPS GET against file_url; it does not embed the file payload.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `file_url` | *string* | - | `True` | Absolute HTTPS URL of a single ICON-D2 GRIB2 forecast file on the DWD Open Data server. The file is bzip2-compressed GRIB2 (.grib2.bz2) and can be fetched with an unauthenticated HTTP GET; the server supports HTTP Range and If-Modified-Since/ETag conditional requests, so handlers can dereference the event with a plain GET against this URL. Each file holds a single variable at a single vertical level for a single forecast lead hour, which keeps per-file payloads small (typically a few hundred KB compressed). Also used verbatim as the CloudEvents 'subject' and the Kafka partition key. Example: 'https://opendata.dwd.de/weather/nwp/icon-d2/grib/00/t/icon-d2_germany_icosahedral_model-level_2026051700_003_10_t.grib2.bz2'. |
| `model` | *string* | - | `True` | Identifier of the source forecast model; matches the 'model' field of the corresponding ForecastModelCatalog event. Currently always 'icon-d2'. |
| `file_name` | *string* | - | `True` | Bare file name as listed in the DWD Apache directory index, following the DWD convention 'icon-d2_<grid>_<level_type>_<run>_<lead>_<level>_<parameter>.grib2.bz2'. Convenient for parsing without splitting file_url. |
| `run` | *string* (optional) | - | `False` | Model run cycle in 'YYYYMMDDHH' UTC form, parsed from file_name (e.g. '2026051700' for the 00 UTC run on 2026-05-17). ICON-D2 is run every three hours. Null when the file name does not match the expected pattern (for example time-invariant or auxiliary files). |
| `forecast_hour` | *int32* (optional) | - | `False` | Forecast lead time in whole hours from the start of the run, parsed from file_name. For ICON-D2 this ranges from 0 to 48. Null when the file name does not match the expected pattern. |
| `parameter` | *string* (optional) | - | `False` | Short ICON-D2 parameter identifier parsed from file_name (for example 't' for temperature, 'u'/'v' for wind components, 'tot_prec' for total precipitation, 'clct' for total cloud cover, 'alb_rad' for shortwave albedo). |
| `level_type` | *string* (optional) | - | `False` | Vertical level encoding parsed from file_name. Common values are 'single-level' (surface and 2D fields), 'model-level' (native ICON hybrid levels indexed 1..65 from top to bottom), 'pressure-level' (interpolated to fixed pressure surfaces, in hPa), and 'time-invariant' (constant fields such as orography). |
| `level` | *string* (optional) | - | `False` | Vertical level value token parsed from file_name. The interpretation depends on level_type: model-level uses an integer level index, pressure-level uses pressure in hPa, single-level may carry a short surface tag or be omitted. |
| `modified` | *string* | - | `True` | Upstream Last-Modified timestamp from the DWD Apache directory listing, expressed as an ISO 8601 UTC string. The bridge emits a new IconD2ForecastFile event whenever this value changes for a known file_url, enabling change detection and de-duplication. |
| `size_bytes` | *int64* (optional) | - | `False` | File size in bytes as parsed from the DWD directory listing, or null when the listing does not expose a size. Indicative only; for an authoritative size rely on the Content-Length header from the actual GET on file_url. Individual ICON-D2 .grib2.bz2 files are typically well below 1 MB compressed. |
