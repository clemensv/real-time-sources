# NOAA NDBC Buoy Observations Bridge Events

This document describes the events emitted by the NOAA NDBC Buoy Observations bridge.

- [Microsoft.OpenData.US.NOAA.NDBC](#message-group-microsoftopendatausnoaandbc)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation](#message-microsoftopendatausnoaandbcbuoyobservation)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyStation](#message-microsoftopendatausnoaandbcbuoystation)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation](#message-microsoftopendatausnoaandbcbuoysolarradiationobservation)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation](#message-microsoftopendatausnoaandbcbuoyoceanographicobservation)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement](#message-microsoftopendatausnoaandbcbuoydartmeasurement)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation](#message-microsoftopendatausnoaandbcbuoycontinuouswindobservation)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement](#message-microsoftopendatausnoaandbcbuoysupplementalmeasurement)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary](#message-microsoftopendatausnoaandbcbuoydetailedwavesummary)
  - [Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement](#message-microsoftopendatausnoaandbcbuoyhourlyrainmeasurement)

---

## Message Group: Microsoft.OpenData.US.NOAA.NDBC
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoyObservation
*Real-time standard meteorological and oceanographic observation from an NDBC buoy, C-MAN station, or partner platform. Sourced from the NDBC latest_obs.txt composite file which is updated every five minutes. Fields cover wind, waves, pressure, temperature, dewpoint, pressure tendency, visibility, and tide.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier. Five-character alphanumeric code assigned by NDBC (e.g. '41001' for deep-ocean buoys, 'BURL1' for C-MAN stations). |
| `latitude` | *double* | - | `True` | Latitude of the observing platform in decimal degrees north. Negative values indicate southern hemisphere. |
| `longitude` | *double* | - | `True` | Longitude of the observing platform in decimal degrees east. Negative values indicate western hemisphere. |
| `timestamp` | *datetime* | - | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC data. |
| `wind_direction` | *double* (optional) | deg (°) | `False` | Wind direction (the direction the wind is coming from) averaged over an 8-minute period for buoys or a 2-minute period for land stations. Unit: degrees true. |
| `wind_speed` | *double* (optional) | m/s | `False` | Average wind speed during the observation period: 8 minutes for buoys, 2 minutes for land stations. Unit: meters per second. |
| `gust` | *double* (optional) | m/s | `False` | Peak 5-second or 8-second gust speed during the observation period. Unit: meters per second. |
| `wave_height` | *double* (optional) | m | `False` | Significant wave height — the average of the highest one-third of all wave heights during a 20-minute sampling period. Unit: meters. |
| `dominant_wave_period` | *double* (optional) | s | `False` | Dominant wave period — the period (in seconds) of the wave band with the maximum energy in the spectral wave analysis. Unit: seconds. |
| `average_wave_period` | *double* (optional) | s | `False` | Average wave period of all waves during the 20-minute sampling period. Unit: seconds. |
| `mean_wave_direction` | *double* (optional) | deg (°) | `False` | Mean wave direction corresponding to the energy at the dominant wave period (DPD). Unit: degrees true. |
| `pressure` | *double* (optional) | hPa | `False` | Sea-level pressure reduced using the standard atmosphere from the station elevation. Unit: hectopascals. |
| `air_temperature` | *double* (optional) | CEL (°C) | `False` | Air temperature measured at the station. Unit: degrees Celsius. |
| `water_temperature` | *double* (optional) | CEL (°C) | `False` | Sea surface temperature. For buoys, measured by a hull-contact sensor near the waterline. Unit: degrees Celsius. |
| `dewpoint` | *double* (optional) | CEL (°C) | `False` | Dewpoint temperature computed from air temperature and relative humidity. Unit: degrees Celsius. |
| `pressure_tendency` | *double* (optional) | hPa | `False` | Pressure tendency — the signed change in sea-level pressure over the preceding 3 hours. A negative value indicates falling pressure; a positive value indicates rising pressure. Unit: hectopascals. |
| `visibility` | *double* (optional) | [nmi_i] (nmi) | `False` | Station visibility as reported by the observing platform. Buoy visibility sensors have a range of 0 to 1.6 nautical miles and are generally only available on C-MAN stations. Unit: nautical miles. |
| `tide` | *double* (optional) | [ft_i] (ft) | `False` | Water level above or below Mean Lower Low Water (MLLW) at coastal and C-MAN stations. Unit: feet. |
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyStation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyStation` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoyStation
*Reference record from the NDBC station table describing the owning agency, platform type, hull class, canonical station name, parsed location, and time-zone code for an observing platform.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier. Five-character alphanumeric code assigned by NDBC and reused across the station table, latest observations, and realtime2 products. |
| `owner` | *string* (optional) | - | `False` | Owning organization as listed in the NDBC station table, such as NDBC, NOS, or another partner agency. |
| `station_type` | *string* (optional) | - | `False` | Platform type from the station table, such as Weather Buoy or C-MAN Station. |
| `hull` | *string* (optional) | - | `False` | Hull or platform class reported in the station table, for example DISCUS or 3-meter. |
| `name` | *string* | - | `True` | Human-readable station name from the NDBC station table. |
| `latitude` | *double* (optional) | deg | `False` | Station latitude in decimal degrees north parsed from the station table LOCATION field. Negative values indicate southern hemisphere. |
| `longitude` | *double* (optional) | deg | `False` | Station longitude in decimal degrees east parsed from the station table LOCATION field. Negative values indicate western hemisphere. |
| `timezone` | *string* (optional) | - | `False` | Single-letter time-zone code carried in the NDBC station table for display and forecast products. |
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoySolarRadiationObservation
*Hourly solar radiation observation from the NDBC .srad realtime2 product. The file reports LI-COR shortwave radiation, Eppley shortwave radiation, and downwelling longwave radiation when those sensors are installed on a station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier. The .srad realtime2 file is published per station and keyed by this identifier. |
| `timestamp` | *datetime* | - | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .srad realtime2 file. |
| `shortwave_radiation_licor` | *double* (optional) | W/m2 | `False` | Average shortwave radiation over the preceding hour from a LI-COR LI-200 pyranometer when the SRAD1 column is present. Unit: watts per square meter. |
| `shortwave_radiation_eppley` | *double* (optional) | W/m2 | `False` | Average shortwave radiation over the preceding hour from an Eppley PSP Precision Spectral Pyranometer when the SWRAD column is present. Unit: watts per square meter. |
| `longwave_radiation` | *double* (optional) | W/m2 | `False` | Average downwelling longwave radiation over the preceding hour from an Eppley PIR Precision Infrared Radiometer when the LWRAD column is present. Unit: watts per square meter. |
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoyOceanographicObservation
*Oceanographic observation from the NDBC .ocean realtime2 product. Each record reports the measurement depth together with direct ocean temperature, conductivity, salinity, dissolved oxygen, chlorophyll, turbidity, pH, and redox potential for one station and timestamp.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier. The .ocean realtime2 file is published per station and keyed by this identifier. |
| `timestamp` | *datetime* | - | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .ocean realtime2 file. |
| `depth` | *double* | m | `True` | Depth in meters at which the oceanographic measurements in this record were taken. |
| `ocean_temperature` | *double* (optional) | CEL (degC) | `False` | Direct ocean temperature measurement from the OTMP column. Unit: degrees Celsius. |
| `conductivity` | *double* (optional) | mS/cm | `False` | Electrical conductivity of seawater from the COND column. Unit: millisiemens per centimeter. |
| `salinity` | *double* (optional) | psu | `False` | Practical salinity computed from conductivity, temperature, and pressure using the Practical Salinity Scale of 1978. Unit: practical salinity units. |
| `oxygen_saturation` | *double* (optional) | % | `False` | Dissolved oxygen saturation percentage from the O2% column. |
| `oxygen_concentration` | *double* (optional) | ppm | `False` | Dissolved oxygen concentration from the O2PPM column. Unit: parts per million. |
| `chlorophyll_concentration` | *double* (optional) | ug/L | `False` | Chlorophyll concentration from the CLCON column. Unit: micrograms per liter. |
| `turbidity` | *double* (optional) | FTU | `False` | Turbidity from the TURB column. Unit: Formazin Turbidity Units. |
| `ph` | *double* (optional) | - | `False` | Acidity or alkalinity of the seawater sample from the PH column. This is dimensionless. |
| `redox_potential` | *double* (optional) | mV | `False` | Oxidation-reduction potential of seawater from the EH column. Unit: millivolts. |
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoyDartMeasurement
*Realtime DART tsunameter measurement from the NDBC .dart product. Each record contains a second-resolution timestamp, the documented NDBC measurement type code, and the measured water-column height for a DART station.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier for the DART tsunameter site publishing the .dart realtime2 file. |
| `timestamp` | *datetime* | - | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm ss columns in the NDBC .dart realtime2 file. |
| `measurement_type_code` | *integer* | - | `True` | Measurement type code from the T column in the DART file. NDBC documents 1 as a 15-minute measurement, 2 as a 1-minute measurement, and 3 as a 15-second measurement. |
| `water_column_height` | *double* | m | `True` | Height of the measured water column from the HEIGHT column in the DART file. Unit: meters. |
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov/data/realtime2/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoyContinuousWindObservation
*Continuous-wind measurement from the NDBC .cwind realtime2 product. Each record reports the latest ten-minute wind average together with the strongest gust observed during the surrounding hourly window and the HHMM code describing when that gust occurred.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier for the station publishing the .cwind realtime2 file. |
| `timestamp` | *datetime* | - | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .cwind realtime2 file. |
| `wind_direction` | *double* (optional) | deg (°) | `False` | Ten-minute average wind direction from the WDIR column, measured clockwise from true north. Unit: degrees true. |
| `wind_speed` | *double* (optional) | m/s | `False` | Ten-minute average wind speed from the WSPD column. Unit: meters per second. |
| `gust_direction` | *double* (optional) | deg (°) | `False` | Direction of the hourly peak gust from the GDR column, measured clockwise from true north. Unit: degrees true. |
| `gust` | *double* (optional) | m/s | `False` | Maximum 5-second peak gust from the GST column during the measurement hour. Unit: meters per second. |
| `gust_time_code` | *string* (optional) | - | `False` | HHMM UTC time code from the GTIME column indicating when the reported gust occurred within the surrounding hourly window. Around midnight the code can refer to the previous UTC day. |
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov/data/realtime2/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoySupplementalMeasurement
*Supplemental hourly extrema from the NDBC .supl realtime2 product. Each record reports the lowest one-minute pressure recorded during the hour and the highest one-minute wind speed with its direction and HHMM occurrence times.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier for the station publishing the .supl realtime2 file. |
| `timestamp` | *datetime* | - | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .supl realtime2 file. |
| `lowest_pressure` | *double* (optional) | hPa | `False` | Lowest one-minute atmospheric pressure recorded during the hour from the PRES column. Unit: hectopascals. |
| `lowest_pressure_time_code` | *string* (optional) | - | `False` | HHMM UTC time code from the PTIME column indicating when the lowest one-minute pressure occurred during the surrounding hourly window. Around midnight the code can refer to the previous UTC day. |
| `highest_wind_speed` | *double* (optional) | m/s | `False` | Highest one-minute wind speed recorded during the hour from the WSPD column. Unit: meters per second. |
| `highest_wind_direction` | *double* (optional) | deg (°) | `False` | Direction associated with the highest one-minute wind speed from the WDIR column, measured clockwise from true north. Unit: degrees true. |
| `highest_wind_time_code` | *string* (optional) | - | `False` | HHMM UTC time code from the WTIME column indicating when the highest one-minute wind speed occurred during the surrounding hourly window. Around midnight the code can refer to the previous UTC day. |
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov/data/realtime2/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoyDetailedWaveSummary
*Detailed wave-summary record from the NDBC .spec realtime2 product. Each record summarizes significant wave height together with swell and wind-wave components, qualitative steepness, and mean wave direction for one station timestamp.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier for the station publishing the .spec realtime2 file. |
| `timestamp` | *datetime* | - | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .spec realtime2 file. |
| `significant_wave_height` | *double* (optional) | m | `False` | Significant wave height from the WVHT column, representing the average height of the highest one-third of waves during the sampling period. Unit: meters. |
| `swell_height` | *double* (optional) | m | `False` | Swell-wave height from the SwH column. Unit: meters. |
| `swell_period` | *double* (optional) | s | `False` | Swell-wave period from the SwP column. Unit: seconds. |
| `wind_wave_height` | *double* (optional) | m | `False` | Wind-wave height from the WWH column. Unit: meters. |
| `wind_wave_period` | *double* (optional) | s | `False` | Wind-wave period from the WWP column. Unit: seconds. |
| `swell_direction` | *string* (optional) | - | `False` | Swell direction from the SwD column. Live NDBC .spec files currently publish this field as a compass code such as E, SE, or ESE rather than a numeric degree value. |
| `wind_wave_direction` | *string* (optional) | - | `False` | Wind-wave direction from the WWD column. Live NDBC .spec files currently publish this field as a compass code such as E, SE, or ESE rather than a numeric degree value. |
| `steepness` | *string* (optional) | - | `False` | Wave steepness category from the STEEPNESS column, for example SWELL, AVERAGE, or VERY_STEEP. |
| `average_wave_period` | *double* (optional) | s | `False` | Average wave period from the APD column. Unit: seconds. |
| `mean_wave_direction` | *double* (optional) | deg (°) | `False` | Mean wave direction from the MWD column, measured clockwise from true north. Unit: degrees true. |
---
### Message: Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement` |
| `source` |  | `` | `False` | `https://www.ndbc.noaa.gov/data/realtime2/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

#### Schema:
##### Object: BuoyHourlyRainMeasurement
*Hourly precipitation total from the NDBC .rain realtime2 product. Each record reports the one-hour rain accumulation for a station timestamp.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `station_id` | *string* | - | `True` | NDBC station identifier for the station publishing the .rain realtime2 file. |
| `timestamp` | *datetime* | - | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .rain realtime2 file. |
| `accumulation` | *double* (optional) | mm | `False` | Hourly rain accumulation from the ACCUM column. This is the total precipitation accumulated during the 60-minute period ending at the reported timestamp. Unit: millimeters. |
