# NOAA NDBC Buoy Observations Poller Events

**NOAA NDBC Buoy Observations Poller** polls the National Data Buoy Center (NDBC) station table, the composite `latest_obs.txt` feed, and selected `realtime2` family files, then sends them to a Kafka topic as CloudEvents. The bridge emits station reference data first and tracks previously seen timestamps per station and feed family to avoid sending duplicates.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 1 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `Microsoft.OpenData.US.NOAA.NDBC.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.NDBC`](#messagegroup-microsoftopendatausnoaandbc) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-ndbc` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Microsoft.OpenData.US.NOAA.NDBC`
<a id="messagegroup-microsoftopendatausnoaandbc"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.NDBC.Kafka` (KAFKA) |
| Messages | 9 |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation`
<a id="message-microsoftopendatausnoaandbcbuoyobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation`](#schema-microsoftopendatausnoaandbcbuoyobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoyStation`
<a id="message-microsoftopendatausnoaandbcbuoystation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoyStation`](#schema-microsoftopendatausnoaandbcbuoystation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyStation` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation`
<a id="message-microsoftopendatausnoaandbcbuoysolarradiationobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoySolarRadiationObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation`](#schema-microsoftopendatausnoaandbcbuoysolarradiationobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation`
<a id="message-microsoftopendatausnoaandbcbuoyoceanographicobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyOceanographicObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation`](#schema-microsoftopendatausnoaandbcbuoyoceanographicobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement`
<a id="message-microsoftopendatausnoaandbcbuoydartmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoyDartMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement`](#schema-microsoftopendatausnoaandbcbuoydartmeasurement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation`
<a id="message-microsoftopendatausnoaandbcbuoycontinuouswindobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyContinuousWindObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation`](#schema-microsoftopendatausnoaandbcbuoycontinuouswindobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov/data/realtime2/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement`
<a id="message-microsoftopendatausnoaandbcbuoysupplementalmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoySupplementalMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement`](#schema-microsoftopendatausnoaandbcbuoysupplementalmeasurement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov/data/realtime2/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary`
<a id="message-microsoftopendatausnoaandbcbuoydetailedwavesummary"></a>

| Field | Value |
| --- | --- |
| Name | BuoyDetailedWaveSummary |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary`](#schema-microsoftopendatausnoaandbcbuoydetailedwavesummary) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov/data/realtime2/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement`
<a id="message-microsoftopendatausnoaandbcbuoyhourlyrainmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoyHourlyRainMeasurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NDBC.jstruct/schemas/Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement`](#schema-microsoftopendatausnoaandbcbuoyhourlyrainmeasurement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement` |
| `source` |  | `string` | `False` | `https://www.ndbc.noaa.gov/data/realtime2/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NDBC.Kafka` | `KAFKA` | topic `noaa-ndbc`; key `{station_id}` |

## Schemagroups

### Schemagroup `Microsoft.OpenData.US.NOAA.NDBC.jstruct`
<a id="schemagroup-microsoftopendatausnoaandbcjstruct"></a>

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation`
<a id="schema-microsoftopendatausnoaandbcbuoyobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoyObservation`
<a id="schema-node-buoyobservation"></a>

Real-time standard meteorological and oceanographic observation from an NDBC buoy, C-MAN station, or partner platform. Sourced from the NDBC latest_obs.txt composite file which is updated every five minutes. Fields cover wind, waves, pressure, temperature, dewpoint, pressure tendency, visibility, and tide.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier. Five-character alphanumeric code assigned by NDBC (e.g. '41001' for deep-ocean buoys, 'BURL1' for C-MAN stations). | - | - | - |
| `latitude` | `double` | `True` | Latitude of the observing platform in decimal degrees north. Negative values indicate southern hemisphere. | - | - | - |
| `longitude` | `double` | `True` | Longitude of the observing platform in decimal degrees east. Negative values indicate western hemisphere. | - | - | - |
| `timestamp` | `datetime` | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC data. | - | - | - |
| `wind_direction` | `union` | `False` | Wind direction (the direction the wind is coming from) averaged over an 8-minute period for buoys or a 2-minute period for land stations. Unit: degrees true. | unit=`deg` symbol=`°` | - | - |
| `wind_speed` | `union` | `False` | Average wind speed during the observation period: 8 minutes for buoys, 2 minutes for land stations. Unit: meters per second. | unit=`m/s` symbol=`m/s` | - | - |
| `gust` | `union` | `False` | Peak 5-second or 8-second gust speed during the observation period. Unit: meters per second. | unit=`m/s` symbol=`m/s` | - | - |
| `wave_height` | `union` | `False` | Significant wave height — the average of the highest one-third of all wave heights during a 20-minute sampling period. Unit: meters. | unit=`m` symbol=`m` | - | - |
| `dominant_wave_period` | `union` | `False` | Dominant wave period — the period (in seconds) of the wave band with the maximum energy in the spectral wave analysis. Unit: seconds. | unit=`s` symbol=`s` | - | - |
| `average_wave_period` | `union` | `False` | Average wave period of all waves during the 20-minute sampling period. Unit: seconds. | unit=`s` symbol=`s` | - | - |
| `mean_wave_direction` | `union` | `False` | Mean wave direction corresponding to the energy at the dominant wave period (DPD). Unit: degrees true. | unit=`deg` symbol=`°` | - | - |
| `pressure` | `union` | `False` | Sea-level pressure reduced using the standard atmosphere from the station elevation. Unit: hectopascals. | unit=`hPa` symbol=`hPa` | - | - |
| `air_temperature` | `union` | `False` | Air temperature measured at the station. Unit: degrees Celsius. | unit=`CEL` symbol=`°C` | - | - |
| `water_temperature` | `union` | `False` | Sea surface temperature. For buoys, measured by a hull-contact sensor near the waterline. Unit: degrees Celsius. | unit=`CEL` symbol=`°C` | - | - |
| `dewpoint` | `union` | `False` | Dewpoint temperature computed from air temperature and relative humidity. Unit: degrees Celsius. | unit=`CEL` symbol=`°C` | - | - |
| `pressure_tendency` | `union` | `False` | Pressure tendency — the signed change in sea-level pressure over the preceding 3 hours. A negative value indicates falling pressure; a positive value indicates rising pressure. Unit: hectopascals. | unit=`hPa` symbol=`hPa` | - | - |
| `visibility` | `union` | `False` | Station visibility as reported by the observing platform. Buoy visibility sensors have a range of 0 to 1.6 nautical miles and are generally only available on C-MAN stations. Unit: nautical miles. | unit=`[nmi_i]` symbol=`nmi` | - | - |
| `tide` | `union` | `False` | Water level above or below Mean Lower Low Water (MLLW) at coastal and C-MAN stations. Unit: feet. | unit=`[ft_i]` symbol=`ft` | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyStation`
<a id="schema-microsoftopendatausnoaandbcbuoystation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyStation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoyStation`
<a id="schema-node-buoystation"></a>

Reference record from the NDBC station table describing the owning agency, platform type, hull class, canonical station name, parsed location, and time-zone code for an observing platform.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyStation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier. Five-character alphanumeric code assigned by NDBC and reused across the station table, latest observations, and realtime2 products. | - | - | - |
| `owner` | `union` | `False` | Owning organization as listed in the NDBC station table, such as NDBC, NOS, or another partner agency. | - | - | - |
| `station_type` | `union` | `False` | Platform type from the station table, such as Weather Buoy or C-MAN Station. | - | - | - |
| `hull` | `union` | `False` | Hull or platform class reported in the station table, for example DISCUS or 3-meter. | - | - | - |
| `name` | `string` | `True` | Human-readable station name from the NDBC station table. | - | - | - |
| `latitude` | `union` | `False` | Station latitude in decimal degrees north parsed from the station table LOCATION field. Negative values indicate southern hemisphere. | unit=`deg` symbol=`deg` | - | - |
| `longitude` | `union` | `False` | Station longitude in decimal degrees east parsed from the station table LOCATION field. Negative values indicate western hemisphere. | unit=`deg` symbol=`deg` | - | - |
| `timezone` | `union` | `False` | Single-letter time-zone code carried in the NDBC station table for display and forecast products. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation`
<a id="schema-microsoftopendatausnoaandbcbuoysolarradiationobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoySolarRadiationObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoySolarRadiationObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoySolarRadiationObservation`
<a id="schema-node-buoysolarradiationobservation"></a>

Hourly solar radiation observation from the NDBC .srad realtime2 product. The file reports LI-COR shortwave radiation, Eppley shortwave radiation, and downwelling longwave radiation when those sensors are installed on a station.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoySolarRadiationObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier. The .srad realtime2 file is published per station and keyed by this identifier. | - | - | - |
| `timestamp` | `datetime` | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .srad realtime2 file. | - | - | - |
| `shortwave_radiation_licor` | `union` | `False` | Average shortwave radiation over the preceding hour from a LI-COR LI-200 pyranometer when the SRAD1 column is present. Unit: watts per square meter. | unit=`W/m2` symbol=`W/m2` | - | - |
| `shortwave_radiation_eppley` | `union` | `False` | Average shortwave radiation over the preceding hour from an Eppley PSP Precision Spectral Pyranometer when the SWRAD column is present. Unit: watts per square meter. | unit=`W/m2` symbol=`W/m2` | - | - |
| `longwave_radiation` | `union` | `False` | Average downwelling longwave radiation over the preceding hour from an Eppley PIR Precision Infrared Radiometer when the LWRAD column is present. Unit: watts per square meter. | unit=`W/m2` symbol=`W/m2` | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation`
<a id="schema-microsoftopendatausnoaandbcbuoyoceanographicobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyOceanographicObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyOceanographicObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoyOceanographicObservation`
<a id="schema-node-buoyoceanographicobservation"></a>

Oceanographic observation from the NDBC .ocean realtime2 product. Each record reports the measurement depth together with direct ocean temperature, conductivity, salinity, dissolved oxygen, chlorophyll, turbidity, pH, and redox potential for one station and timestamp.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyOceanographicObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier. The .ocean realtime2 file is published per station and keyed by this identifier. | - | - | - |
| `timestamp` | `datetime` | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .ocean realtime2 file. | - | - | - |
| `depth` | `double` | `True` | Depth in meters at which the oceanographic measurements in this record were taken. | unit=`m` symbol=`m` | - | - |
| `ocean_temperature` | `union` | `False` | Direct ocean temperature measurement from the OTMP column. Unit: degrees Celsius. | unit=`CEL` symbol=`degC` | - | - |
| `conductivity` | `union` | `False` | Electrical conductivity of seawater from the COND column. Unit: millisiemens per centimeter. | unit=`mS/cm` symbol=`mS/cm` | - | - |
| `salinity` | `union` | `False` | Practical salinity computed from conductivity, temperature, and pressure using the Practical Salinity Scale of 1978. Unit: practical salinity units. | unit=`psu` symbol=`psu` | - | - |
| `oxygen_saturation` | `union` | `False` | Dissolved oxygen saturation percentage from the O2% column. | unit=`%` symbol=`%` | - | - |
| `oxygen_concentration` | `union` | `False` | Dissolved oxygen concentration from the O2PPM column. Unit: parts per million. | unit=`ppm` symbol=`ppm` | - | - |
| `chlorophyll_concentration` | `union` | `False` | Chlorophyll concentration from the CLCON column. Unit: micrograms per liter. | unit=`ug/L` symbol=`ug/L` | - | - |
| `turbidity` | `union` | `False` | Turbidity from the TURB column. Unit: Formazin Turbidity Units. | unit=`FTU` symbol=`FTU` | - | - |
| `ph` | `union` | `False` | Acidity or alkalinity of the seawater sample from the PH column. This is dimensionless. | - | - | - |
| `redox_potential` | `union` | `False` | Oxidation-reduction potential of seawater from the EH column. Unit: millivolts. | unit=`mV` symbol=`mV` | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement`
<a id="schema-microsoftopendatausnoaandbcbuoydartmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoyDartMeasurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyDartMeasurement` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoyDartMeasurement`
<a id="schema-node-buoydartmeasurement"></a>

Realtime DART tsunameter measurement from the NDBC .dart product. Each record contains a second-resolution timestamp, the documented NDBC measurement type code, and the measured water-column height for a DART station.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyDartMeasurement` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier for the DART tsunameter site publishing the .dart realtime2 file. | - | - | - |
| `timestamp` | `datetime` | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm ss columns in the NDBC .dart realtime2 file. | - | - | - |
| `measurement_type_code` | `integer` | `True` | Measurement type code from the T column in the DART file. NDBC documents 1 as a 15-minute measurement, 2 as a 1-minute measurement, and 3 as a 15-second measurement. | - | - | - |
| `water_column_height` | `double` | `True` | Height of the measured water column from the HEIGHT column in the DART file. Unit: meters. | unit=`m` symbol=`m` | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation`
<a id="schema-microsoftopendatausnoaandbcbuoycontinuouswindobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyContinuousWindObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyContinuousWindObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoyContinuousWindObservation`
<a id="schema-node-buoycontinuouswindobservation"></a>

Continuous-wind measurement from the NDBC .cwind realtime2 product. Each record reports the latest ten-minute wind average together with the strongest gust observed during the surrounding hourly window and the HHMM code describing when that gust occurred.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyContinuousWindObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier for the station publishing the .cwind realtime2 file. | - | - | - |
| `timestamp` | `datetime` | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .cwind realtime2 file. | - | - | - |
| `wind_direction` | `union` | `False` | Ten-minute average wind direction from the WDIR column, measured clockwise from true north. Unit: degrees true. | unit=`deg` symbol=`°` | - | - |
| `wind_speed` | `union` | `False` | Ten-minute average wind speed from the WSPD column. Unit: meters per second. | unit=`m/s` symbol=`m/s` | - | - |
| `gust_direction` | `union` | `False` | Direction of the hourly peak gust from the GDR column, measured clockwise from true north. Unit: degrees true. | unit=`deg` symbol=`°` | - | - |
| `gust` | `union` | `False` | Maximum 5-second peak gust from the GST column during the measurement hour. Unit: meters per second. | unit=`m/s` symbol=`m/s` | - | - |
| `gust_time_code` | `union` | `False` | HHMM UTC time code from the GTIME column indicating when the reported gust occurred within the surrounding hourly window. Around midnight the code can refer to the previous UTC day. | - | pattern=`^[0-9]{4}$` | - |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement`
<a id="schema-microsoftopendatausnoaandbcbuoysupplementalmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoySupplementalMeasurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoySupplementalMeasurement` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoySupplementalMeasurement`
<a id="schema-node-buoysupplementalmeasurement"></a>

Supplemental hourly extrema from the NDBC .supl realtime2 product. Each record reports the lowest one-minute pressure recorded during the hour and the highest one-minute wind speed with its direction and HHMM occurrence times.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoySupplementalMeasurement` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier for the station publishing the .supl realtime2 file. | - | - | - |
| `timestamp` | `datetime` | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .supl realtime2 file. | - | - | - |
| `lowest_pressure` | `union` | `False` | Lowest one-minute atmospheric pressure recorded during the hour from the PRES column. Unit: hectopascals. | unit=`hPa` symbol=`hPa` | - | - |
| `lowest_pressure_time_code` | `union` | `False` | HHMM UTC time code from the PTIME column indicating when the lowest one-minute pressure occurred during the surrounding hourly window. Around midnight the code can refer to the previous UTC day. | - | pattern=`^[0-9]{4}$` | - |
| `highest_wind_speed` | `union` | `False` | Highest one-minute wind speed recorded during the hour from the WSPD column. Unit: meters per second. | unit=`m/s` symbol=`m/s` | - | - |
| `highest_wind_direction` | `union` | `False` | Direction associated with the highest one-minute wind speed from the WDIR column, measured clockwise from true north. Unit: degrees true. | unit=`deg` symbol=`°` | - | - |
| `highest_wind_time_code` | `union` | `False` | HHMM UTC time code from the WTIME column indicating when the highest one-minute wind speed occurred during the surrounding hourly window. Around midnight the code can refer to the previous UTC day. | - | pattern=`^[0-9]{4}$` | - |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary`
<a id="schema-microsoftopendatausnoaandbcbuoydetailedwavesummary"></a>

| Field | Value |
| --- | --- |
| Name | BuoyDetailedWaveSummary |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyDetailedWaveSummary` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoyDetailedWaveSummary`
<a id="schema-node-buoydetailedwavesummary"></a>

Detailed wave-summary record from the NDBC .spec realtime2 product. Each record summarizes significant wave height together with swell and wind-wave components, qualitative steepness, and mean wave direction for one station timestamp.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyDetailedWaveSummary` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier for the station publishing the .spec realtime2 file. | - | - | - |
| `timestamp` | `datetime` | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .spec realtime2 file. | - | - | - |
| `significant_wave_height` | `union` | `False` | Significant wave height from the WVHT column, representing the average height of the highest one-third of waves during the sampling period. Unit: meters. | unit=`m` symbol=`m` | - | - |
| `swell_height` | `union` | `False` | Swell-wave height from the SwH column. Unit: meters. | unit=`m` symbol=`m` | - | - |
| `swell_period` | `union` | `False` | Swell-wave period from the SwP column. Unit: seconds. | unit=`s` symbol=`s` | - | - |
| `wind_wave_height` | `union` | `False` | Wind-wave height from the WWH column. Unit: meters. | unit=`m` symbol=`m` | - | - |
| `wind_wave_period` | `union` | `False` | Wind-wave period from the WWP column. Unit: seconds. | unit=`s` symbol=`s` | - | - |
| `swell_direction` | `union` | `False` | Swell direction from the SwD column. Live NDBC .spec files currently publish this field as a compass code such as E, SE, or ESE rather than a numeric degree value. | - | - | - |
| `wind_wave_direction` | `union` | `False` | Wind-wave direction from the WWD column. Live NDBC .spec files currently publish this field as a compass code such as E, SE, or ESE rather than a numeric degree value. | - | - | - |
| `steepness` | `union` | `False` | Wave steepness category from the STEEPNESS column, for example SWELL, AVERAGE, or VERY_STEEP. | - | - | - |
| `average_wave_period` | `union` | `False` | Average wave period from the APD column. Unit: seconds. | unit=`s` symbol=`s` | - | - |
| `mean_wave_direction` | `union` | `False` | Mean wave direction from the MWD column, measured clockwise from true north. Unit: degrees true. | unit=`deg` symbol=`°` | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement`
<a id="schema-microsoftopendatausnoaandbcbuoyhourlyrainmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoyHourlyRainMeasurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyHourlyRainMeasurement` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BuoyHourlyRainMeasurement`
<a id="schema-node-buoyhourlyrainmeasurement"></a>

Hourly precipitation total from the NDBC .rain realtime2 product. Each record reports the one-hour rain accumulation for a station timestamp.

| Field | Value |
| --- | --- |
| $id | `https://www.ndbc.noaa.gov/schemas/Microsoft/OpenData/US/NOAA/NDBC/BuoyHourlyRainMeasurement` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NDBC station identifier for the station publishing the .rain realtime2 file. | - | - | - |
| `timestamp` | `datetime` | `True` | Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC .rain realtime2 file. | - | - | - |
| `accumulation` | `union` | `False` | Hourly rain accumulation from the ACCUM column. This is the total precipitation accumulated during the 60-minute period ending at the reported timestamp. Unit: millimeters. | unit=`mm` symbol=`mm` | - | - |

### Schemagroup `Microsoft.OpenData.US.NOAA.NDBC.avro`
<a id="schemagroup-microsoftopendatausnoaandbcavro"></a>

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyObservation`
<a id="schema-microsoftopendatausnoaandbcbuoyobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoyObservation |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | BuoyObservation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `latitude` | `double` |  | `-` |
| `longitude` | `double` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `wind_direction` | `null` \| `double` |  | `-` |
| `wind_speed` | `null` \| `double` |  | `-` |
| `gust` | `null` \| `double` |  | `-` |
| `wave_height` | `null` \| `double` |  | `-` |
| `dominant_wave_period` | `null` \| `double` |  | `-` |
| `average_wave_period` | `null` \| `double` |  | `-` |
| `mean_wave_direction` | `null` \| `double` |  | `-` |
| `pressure` | `null` \| `double` |  | `-` |
| `air_temperature` | `null` \| `double` |  | `-` |
| `water_temperature` | `null` \| `double` |  | `-` |
| `dewpoint` | `null` \| `double` |  | `-` |
| `pressure_tendency` | `null` \| `double` |  | `-` |
| `visibility` | `null` \| `double` |  | `-` |
| `tide` | `null` \| `double` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyStation`
<a id="schema-microsoftopendatausnoaandbcbuoystation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyStation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoyStation |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | BuoyStation |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `owner` | `null` \| `string` |  | `-` |
| `station_type` | `null` \| `string` |  | `-` |
| `hull` | `null` \| `string` |  | `-` |
| `name` | `string` |  | `-` |
| `latitude` | `null` \| `double` |  | `-` |
| `longitude` | `null` \| `double` |  | `-` |
| `timezone` | `null` \| `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoySolarRadiationObservation`
<a id="schema-microsoftopendatausnoaandbcbuoysolarradiationobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoySolarRadiationObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoySolarRadiationObservation |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | Hourly solar radiation observation from the NDBC .srad realtime2 product. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `shortwave_radiation_licor` | `null` \| `double` |  | `-` |
| `shortwave_radiation_eppley` | `null` \| `double` |  | `-` |
| `longwave_radiation` | `null` \| `double` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyOceanographicObservation`
<a id="schema-microsoftopendatausnoaandbcbuoyoceanographicobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyOceanographicObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoyOceanographicObservation |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | Oceanographic observation from the NDBC .ocean realtime2 product. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `depth` | `double` |  | `-` |
| `ocean_temperature` | `null` \| `double` |  | `-` |
| `conductivity` | `null` \| `double` |  | `-` |
| `salinity` | `null` \| `double` |  | `-` |
| `oxygen_saturation` | `null` \| `double` |  | `-` |
| `oxygen_concentration` | `null` \| `double` |  | `-` |
| `chlorophyll_concentration` | `null` \| `double` |  | `-` |
| `turbidity` | `null` \| `double` |  | `-` |
| `ph` | `null` \| `double` |  | `-` |
| `redox_potential` | `null` \| `double` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyDartMeasurement`
<a id="schema-microsoftopendatausnoaandbcbuoydartmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoyDartMeasurement |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoyDartMeasurement |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | Realtime DART tsunameter measurement from the NDBC .dart product. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `measurement_type_code` | `int` |  | `-` |
| `water_column_height` | `double` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyContinuousWindObservation`
<a id="schema-microsoftopendatausnoaandbcbuoycontinuouswindobservation"></a>

| Field | Value |
| --- | --- |
| Name | BuoyContinuousWindObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoyContinuousWindObservation |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | Continuous-wind measurement from the NDBC .cwind realtime2 product. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `wind_direction` | `null` \| `double` |  | `-` |
| `wind_speed` | `null` \| `double` |  | `-` |
| `gust_direction` | `null` \| `double` |  | `-` |
| `gust` | `null` \| `double` |  | `-` |
| `gust_time_code` | `null` \| `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoySupplementalMeasurement`
<a id="schema-microsoftopendatausnoaandbcbuoysupplementalmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoySupplementalMeasurement |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoySupplementalMeasurement |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | Supplemental hourly extrema from the NDBC .supl realtime2 product. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `lowest_pressure` | `null` \| `double` |  | `-` |
| `lowest_pressure_time_code` | `null` \| `string` |  | `-` |
| `highest_wind_speed` | `null` \| `double` |  | `-` |
| `highest_wind_direction` | `null` \| `double` |  | `-` |
| `highest_wind_time_code` | `null` \| `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyDetailedWaveSummary`
<a id="schema-microsoftopendatausnoaandbcbuoydetailedwavesummary"></a>

| Field | Value |
| --- | --- |
| Name | BuoyDetailedWaveSummary |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoyDetailedWaveSummary |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | Detailed wave-summary record from the NDBC .spec realtime2 product. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `significant_wave_height` | `null` \| `double` |  | `-` |
| `swell_height` | `null` \| `double` |  | `-` |
| `swell_period` | `null` \| `double` |  | `-` |
| `wind_wave_height` | `null` \| `double` |  | `-` |
| `wind_wave_period` | `null` \| `double` |  | `-` |
| `swell_direction` | `null` \| `string` |  | `-` |
| `wind_wave_direction` | `null` \| `string` |  | `-` |
| `steepness` | `null` \| `string` |  | `-` |
| `average_wave_period` | `null` \| `double` |  | `-` |
| `mean_wave_direction` | `null` \| `double` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NDBC.BuoyHourlyRainMeasurement`
<a id="schema-microsoftopendatausnoaandbcbuoyhourlyrainmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | BuoyHourlyRainMeasurement |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | BuoyHourlyRainMeasurement |
| Namespace | Microsoft.OpenData.US.NOAA.NDBC |
| Type | `record` |
| Doc | Hourly precipitation total from the NDBC .rain realtime2 product. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` |  | `-` |
| `timestamp` | `string` |  | `-` |
| `accumulation` | `null` \| `double` |  | `-` |
