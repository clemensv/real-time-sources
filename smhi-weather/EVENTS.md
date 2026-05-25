# SMHI Weather Observation Bridge Events

This bridge fetches real-time meteorological observations from the [Swedish Meteorological and Hydrological Institute (SMHI)](https://opendata.smhi.se/apidocs/metobs/) and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

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
| Schemagroups | 1 |

## Endpoints

### Endpoint `SE.Gov.SMHI.Weather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`SE.Gov.SMHI.Weather`](#messagegroup-segovsmhiweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `smhi-weather` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `SE.Gov.SMHI.Weather`
<a id="messagegroup-segovsmhiweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `SE.Gov.SMHI.Weather.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `SE.Gov.SMHI.Weather.Station`
<a id="message-segovsmhiweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SE.Gov.SMHI.Weather.jstruct/schemas/SE.Gov.SMHI.Weather.Station`](#schema-segovsmhiweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SE.Gov.SMHI.Weather.Station` |
| `source` |  | `string` | `False` | `https://opendata-download-metobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SE.Gov.SMHI.Weather.Kafka` | `KAFKA` | topic `smhi-weather`; key `{station_id}` |

#### Message `SE.Gov.SMHI.Weather.WeatherObservation`
<a id="message-segovsmhiweatherweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SE.Gov.SMHI.Weather.jstruct/schemas/SE.Gov.SMHI.Weather.WeatherObservation`](#schema-segovsmhiweatherweatherobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SE.Gov.SMHI.Weather.WeatherObservation` |
| `source` |  | `string` | `False` | `https://opendata-download-metobs.smhi.se` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SE.Gov.SMHI.Weather.Kafka` | `KAFKA` | topic `smhi-weather`; key `{station_id}` |

## Schemagroups

### Schemagroup `SE.Gov.SMHI.Weather.jstruct`
<a id="schemagroup-segovsmhiweatherjstruct"></a>

#### Schema `SE.Gov.SMHI.Weather.Station`
<a id="schema-segovsmhiweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata-download-metobs.smhi.se/schemas/SE/Gov/SMHI/Weather/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference metadata for a SMHI meteorological observation station. Stations report hourly surface observations of temperature, wind, pressure, humidity, precipitation, and other parameters across Sweden.

| Field | Value |
| --- | --- |
| $id | `https://opendata-download-metobs.smhi.se/schemas/SE/Gov/SMHI/Weather/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | SMHI numeric station identifier, unique within the SMHI observation network. | - | - | - |
| `name` | `string` | `True` | Human-readable station name as assigned by SMHI, e.g. 'Abisko Aut' or 'Stockholm-Arlanda'. | - | - | - |
| `owner` | `string` | `False` | Organization or entity that owns and operates the station, e.g. 'SMHI' or 'Polarforskningssekretariatet'. | - | - | - |
| `owner_category` | `string` | `False` | Category of station ownership, e.g. 'CLIMATE' for long-running climate stations or 'AVIATION' for airport stations. | - | - | - |
| `measuring_stations` | `string` | `False` | Station classification within SMHI's measuring station network, e.g. 'CORE' for primary network stations. | - | - | - |
| `height` | `double` | `False` | Sensor height above ground in meters. | unit=`m` symbol=`m` | - | - |
| `latitude` | `double` | `True` | Geographic latitude of the station in decimal degrees. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | Geographic longitude of the station in decimal degrees. | unit=`degree` symbol=`°` | - | - |

#### Schema `SE.Gov.SMHI.Weather.WeatherObservation`
<a id="schema-segovsmhiweatherweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata-download-metobs.smhi.se/schemas/SE/Gov/SMHI/Weather/WeatherObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherObservation`
<a id="schema-node-weatherobservation"></a>

Hourly weather observation from a SMHI meteorological station. Multi-parameter observations are assembled from the per-parameter latest-hour API endpoints. Each record contains the most recent values for temperature, wind, pressure, humidity, precipitation, visibility, cloud cover, irradiance, and present weather.

| Field | Value |
| --- | --- |
| $id | `https://opendata-download-metobs.smhi.se/schemas/SE/Gov/SMHI/Weather/WeatherObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | SMHI station identifier for the reporting station. | - | - | - |
| `station_name` | `string` | `True` | Human-readable name of the reporting station. | - | - | - |
| `observation_time` | `datetime` | `True` | Timestamp of the observation in UTC, derived from the SMHI epoch millisecond value. | - | - | - |
| `air_temperature` | `union` | `False` | Instantaneous air temperature, reported hourly (SMHI parameter 1). | unit=`Cel` symbol=`°C` | - | - |
| `wind_gust` | `union` | `False` | Maximum wind gust speed, reported hourly (SMHI parameter 21). | unit=`m/s` symbol=`m/s` | - | - |
| `dew_point` | `union` | `False` | Dew point temperature, reported hourly (SMHI parameter 39). | unit=`Cel` symbol=`°C` | - | - |
| `air_pressure` | `union` | `False` | Atmospheric pressure reduced to mean sea level, reported hourly (SMHI parameter 9). | unit=`hPa` symbol=`hPa` | - | - |
| `relative_humidity` | `union` | `False` | Relative humidity as a percentage, reported hourly (SMHI parameter 6). | unit=`percent` symbol=`%` | - | - |
| `precipitation_last_hour` | `union` | `False` | Total precipitation in the last hour, reported hourly (SMHI parameter 7). | unit=`mm` symbol=`mm` | - | - |
| `wind_direction` | `union` | `False` | Wind direction in degrees from which the wind is blowing, measured at 10 m height, reported hourly (SMHI parameter 3). | unit=`degree` symbol=`°` | - | - |
| `wind_speed` | `union` | `False` | Mean wind speed over 10 minutes measured at 10 m height, reported hourly (SMHI parameter 4). | unit=`m/s` symbol=`m/s` | - | - |
| `max_wind_speed` | `union` | `False` | Maximum of 10-minute mean wind speed during the hour, measured at 10 m height (SMHI parameter 25). | unit=`m/s` symbol=`m/s` | - | - |
| `visibility` | `union` | `False` | Horizontal visibility, reported hourly (SMHI parameter 12). | unit=`km` symbol=`km` | - | - |
| `total_cloud_cover` | `union` | `False` | Total cloud cover in oktas (eighths of sky covered), reported hourly (SMHI parameter 16). | unit=`okta` symbol=`okta` | - | - |
| `present_weather` | `union` | `False` | WMO present weather code (ww table 4677) describing current weather phenomena at the time of observation (SMHI parameter 13). Values range from 0 (clear) to 99 (thunderstorm with hail). | - | - | - |
| `sunshine_duration` | `union` | `False` | Duration of sunshine during the last hour in seconds (SMHI parameter 10). | unit=`s` symbol=`s` | - | - |
| `global_irradiance` | `union` | `False` | Global solar irradiance (direct + diffuse), average over the hour, measured by pyranometer (SMHI parameter 11). | unit=`W/m2` symbol=`W/m²` | - | - |
| `precipitation_intensity` | `union` | `False` | Instantaneous precipitation intensity measured by optical or weighing gauge (SMHI parameter 38). | unit=`mm/h` symbol=`mm/h` | - | - |
| `quality` | `string` | `False` | Quality flag for the observation as assigned by SMHI: 'G' for approved, 'Y' for suspect. | - | - | - |
