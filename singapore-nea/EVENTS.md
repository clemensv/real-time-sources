# Singapore NEA Weather and Air Quality Bridge Events

This bridge fetches real-time weather observations and regional air quality data from the [Singapore National Environment Agency (NEA)](https://data.gov.sg/datasets?topics=environment) and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `SG.Gov.NEA.Weather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`SG.Gov.NEA.Weather`](#messagegroup-sggovneaweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `singapore-nea` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `SG.Gov.NEA.AirQuality.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`SG.Gov.NEA.AirQuality`](#messagegroup-sggovneaairquality) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `singapore-nea-airquality` |
| Kafka key | `{region}` |
| Deployed | False |

## Messagegroups

### Messagegroup `SG.Gov.NEA.Weather`
<a id="messagegroup-sggovneaweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `SG.Gov.NEA.Weather.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `SG.Gov.NEA.Weather.Station`
<a id="message-sggovneaweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SG.Gov.NEA.Weather.jstruct/schemas/SG.Gov.NEA.Weather.Station`](#schema-sggovneaweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SG.Gov.NEA.Weather.Station` |
| `source` |  | `string` | `False` | `https://api.data.gov.sg` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SG.Gov.NEA.Weather.Kafka` | `KAFKA` | topic `singapore-nea`; key `{station_id}` |

#### Message `SG.Gov.NEA.Weather.WeatherObservation`
<a id="message-sggovneaweatherweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SG.Gov.NEA.Weather.jstruct/schemas/SG.Gov.NEA.Weather.WeatherObservation`](#schema-sggovneaweatherweatherobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SG.Gov.NEA.Weather.WeatherObservation` |
| `source` |  | `string` | `False` | `https://api.data.gov.sg` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SG.Gov.NEA.Weather.Kafka` | `KAFKA` | topic `singapore-nea`; key `{station_id}` |

### Messagegroup `SG.Gov.NEA.AirQuality`
<a id="messagegroup-sggovneaairquality"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `SG.Gov.NEA.AirQuality.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `SG.Gov.NEA.AirQuality.Region`
<a id="message-sggovneaairqualityregion"></a>

| Field | Value |
| --- | --- |
| Name | Region |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SG.Gov.NEA.AirQuality.jstruct/schemas/SG.Gov.NEA.AirQuality.Region`](#schema-sggovneaairqualityregion) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SG.Gov.NEA.AirQuality.Region` |
| `source` |  | `string` | `False` | `https://api.data.gov.sg` |
| `subject` |  | `uritemplate` | `False` | `{region}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SG.Gov.NEA.AirQuality.Kafka` | `KAFKA` | topic `singapore-nea-airquality`; key `{region}` |

#### Message `SG.Gov.NEA.AirQuality.PSIReading`
<a id="message-sggovneaairqualitypsireading"></a>

| Field | Value |
| --- | --- |
| Name | PSIReading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SG.Gov.NEA.AirQuality.jstruct/schemas/SG.Gov.NEA.AirQuality.PSIReading`](#schema-sggovneaairqualitypsireading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SG.Gov.NEA.AirQuality.PSIReading` |
| `source` |  | `string` | `False` | `https://api.data.gov.sg` |
| `subject` |  | `uritemplate` | `False` | `{region}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SG.Gov.NEA.AirQuality.Kafka` | `KAFKA` | topic `singapore-nea-airquality`; key `{region}` |

#### Message `SG.Gov.NEA.AirQuality.PM25Reading`
<a id="message-sggovneaairqualitypm25reading"></a>

| Field | Value |
| --- | --- |
| Name | PM25Reading |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/SG.Gov.NEA.AirQuality.jstruct/schemas/SG.Gov.NEA.AirQuality.PM25Reading`](#schema-sggovneaairqualitypm25reading) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `SG.Gov.NEA.AirQuality.PM25Reading` |
| `source` |  | `string` | `False` | `https://api.data.gov.sg` |
| `subject` |  | `uritemplate` | `False` | `{region}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `SG.Gov.NEA.AirQuality.Kafka` | `KAFKA` | topic `singapore-nea-airquality`; key `{region}` |

## Schemagroups

### Schemagroup `SG.Gov.NEA.Weather.jstruct`
<a id="schemagroup-sggovneaweatherjstruct"></a>

#### Schema `SG.Gov.NEA.Weather.Station`
<a id="schema-sggovneaweatherstation"></a>

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
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/Weather/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data for a Singapore NEA weather observation station. Stations are identified by a stable device ID (e.g. S109) and include location coordinates. The data_types field indicates which parameters this station reports.

| Field | Value |
| --- | --- |
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/Weather/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NEA station identifier, e.g. 'S109', 'S50'. Matches the device_id field in the NEA API metadata. | - | - | - |
| `device_id` | `string` | `False` | Device identifier, typically identical to station_id. | - | - | - |
| `name` | `string` | `True` | Human-readable station name describing the location, e.g. 'Ang Mo Kio Avenue 5', 'Changi'. | - | - | - |
| `latitude` | `double` | `True` | WGS84 latitude of the station. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | WGS84 longitude of the station. | unit=`degree` symbol=`°` | - | - |
| `data_types` | `string` | `False` | Comma-separated list of observation types this station reports. Values: 'air_temperature', 'rainfall', 'relative_humidity', 'wind_speed', 'wind_direction'. | - | - | - |

#### Schema `SG.Gov.NEA.Weather.WeatherObservation`
<a id="schema-sggovneaweatherweatherobservation"></a>

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
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/Weather/WeatherObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherObservation`
<a id="schema-node-weatherobservation"></a>

Real-time weather observation from a Singapore NEA station assembled from multiple endpoints. Temperature updates every minute, rainfall every 5 minutes, humidity and wind every minute. Fields are null when the station does not report that parameter.

| Field | Value |
| --- | --- |
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/Weather/WeatherObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | NEA station identifier. | - | - | - |
| `station_name` | `string` | `True` | Station location name. | - | - | - |
| `observation_time` | `datetime` | `True` | Timestamp of the observation in ISO 8601 with Singapore timezone (+08:00). | - | - | - |
| `air_temperature` | `union` | `False` | Air temperature from the air-temperature endpoint. | unit=`Cel` symbol=`°C` | - | - |
| `rainfall` | `union` | `False` | Rainfall amount in the last 5 minutes from the rainfall endpoint. | unit=`mm` symbol=`mm` | - | - |
| `relative_humidity` | `union` | `False` | Relative humidity from the relative-humidity endpoint. | unit=`percent` symbol=`%` | - | - |
| `wind_speed` | `union` | `False` | Wind speed from the wind-speed endpoint. | unit=`kn` symbol=`kn` | - | - |
| `wind_direction` | `union` | `False` | Wind direction in degrees clockwise from true north, from the wind-direction endpoint. | unit=`degree` symbol=`°` | - | - |

### Schemagroup `SG.Gov.NEA.AirQuality.jstruct`
<a id="schemagroup-sggovneaairqualityjstruct"></a>

#### Schema `SG.Gov.NEA.AirQuality.Region`
<a id="schema-sggovneaairqualityregion"></a>

| Field | Value |
| --- | --- |
| Name | Region |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/AirQuality/Region` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Region`
<a id="schema-node-region"></a>

Reference data for a Singapore NEA air quality monitoring region. NEA divides Singapore into five geographic regions for PSI and PM2.5 reporting.

| Field | Value |
| --- | --- |
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/AirQuality/Region` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `region` | `string` | `True` | Region identifier. One of: west, east, central, south, north. | altenums=`["west", "east", "central", "south", "north"]` | - | - |
| `latitude` | `double` | `True` | WGS84 latitude of the region label location as published by the NEA API. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | WGS84 longitude of the region label location as published by the NEA API. | unit=`degree` symbol=`°` | - | - |

#### Schema `SG.Gov.NEA.AirQuality.PSIReading`
<a id="schema-sggovneaairqualitypsireading"></a>

| Field | Value |
| --- | --- |
| Name | PSIReading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/AirQuality/PSIReading` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PSIReading`
<a id="schema-node-psireading"></a>

Pollutant Standards Index (PSI) reading for a Singapore NEA air quality region. PSI is a composite index calculated from six pollutant sub-indices. Published hourly by the NEA via data.gov.sg.

| Field | Value |
| --- | --- |
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/AirQuality/PSIReading` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `region` | `string` | `True` | Region identifier (west/east/central/south/north). | altenums=`["west", "east", "central", "south", "north"]` | - | - |
| `timestamp` | `datetime` | `True` | Observation period start timestamp in ISO 8601 with timezone. | - | - | - |
| `update_timestamp` | `datetime` | `True` | Timestamp when the NEA API last updated this reading. | - | - | - |
| `psi_twenty_four_hourly` | `union` | `True` | 24-hour PSI value. The overall Pollutant Standards Index for the region. Scale: 0-50 Good, 51-100 Moderate, 101-200 Unhealthy, 201-300 Very Unhealthy, above 300 Hazardous. | - | minimum=`0` | - |
| `o3_sub_index` | `union` | `False` | Ozone (O3) sub-index component of PSI. | - | minimum=`0` | - |
| `pm10_sub_index` | `union` | `False` | PM10 sub-index component of PSI. | - | minimum=`0` | - |
| `pm10_twenty_four_hourly` | `union` | `False` | PM10 24-hour concentration used to calculate the PM10 PSI sub-index. | unit=`ug/m3` symbol=`µg/m³` | minimum=`0` | - |
| `pm25_sub_index` | `union` | `False` | PM2.5 sub-index component of PSI. | - | minimum=`0` | - |
| `pm25_twenty_four_hourly` | `union` | `False` | PM2.5 24-hour concentration. | unit=`ug/m3` symbol=`µg/m³` | minimum=`0` | - |
| `co_sub_index` | `union` | `False` | Carbon monoxide (CO) sub-index component of PSI. | - | minimum=`0` | - |
| `co_eight_hour_max` | `union` | `False` | CO 8-hour maximum concentration. | unit=`mg/m3` symbol=`mg/m³` | minimum=`0` | - |
| `so2_sub_index` | `union` | `False` | Sulphur dioxide (SO2) sub-index component of PSI. | - | minimum=`0` | - |
| `so2_twenty_four_hourly` | `union` | `False` | SO2 24-hour concentration. | unit=`ug/m3` symbol=`µg/m³` | minimum=`0` | - |
| `no2_one_hour_max` | `union` | `False` | Nitrogen dioxide (NO2) 1-hour maximum concentration. | unit=`ug/m3` symbol=`µg/m³` | minimum=`0` | - |
| `o3_eight_hour_max` | `union` | `False` | Ozone (O3) 8-hour maximum concentration. | unit=`ug/m3` symbol=`µg/m³` | minimum=`0` | - |

#### Schema `SG.Gov.NEA.AirQuality.PM25Reading`
<a id="schema-sggovneaairqualitypm25reading"></a>

| Field | Value |
| --- | --- |
| Name | PM25Reading |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/AirQuality/PM25Reading` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PM25Reading`
<a id="schema-node-pm25reading"></a>

Hourly PM2.5 concentration reading for a Singapore NEA air quality region. Fine particulate matter with aerodynamic diameter less than or equal to 2.5 micrometres. Published hourly by NEA.

| Field | Value |
| --- | --- |
| $id | `https://api.data.gov.sg/schemas/SG/Gov/NEA/AirQuality/PM25Reading` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `region` | `string` | `True` | Region identifier (west/east/central/south/north). | altenums=`["west", "east", "central", "south", "north"]` | - | - |
| `timestamp` | `datetime` | `True` | Observation period start timestamp in ISO 8601 with timezone. | - | - | - |
| `update_timestamp` | `datetime` | `True` | Timestamp when the NEA API last updated this reading. | - | - | - |
| `pm25_one_hourly` | `union` | `True` | PM2.5 1-hour concentration for the region. | unit=`ug/m3` symbol=`µg/m³` | minimum=`0` | - |
