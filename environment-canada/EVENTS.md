# Environment Canada Weather Observation Bridge Events

This bridge fetches real-time Surface Weather Observations (SWOB) from [Environment and Climate Change Canada (ECCC)](https://api.weather.gc.ca/) via the OGC API and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

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

### Endpoint `CA.Gov.ECCC.Weather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`CA.Gov.ECCC.Weather`](#messagegroup-cagovecccweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `environment-canada` |
| Kafka key | `{msc_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `CA.Gov.ECCC.Weather`
<a id="messagegroup-cagovecccweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `CA.Gov.ECCC.Weather.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `CA.Gov.ECCC.Weather.Station`
<a id="message-cagovecccweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CA.Gov.ECCC.Weather.jstruct/schemas/CA.Gov.ECCC.Weather.Station`](#schema-cagovecccweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CA.Gov.ECCC.Weather.Station` |
| `source` |  | `string` | `False` | `https://api.weather.gc.ca` |
| `subject` |  | `uritemplate` | `False` | `{msc_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CA.Gov.ECCC.Weather.Kafka` | `KAFKA` | topic `environment-canada`; key `{msc_id}` |

#### Message `CA.Gov.ECCC.Weather.WeatherObservation`
<a id="message-cagovecccweatherweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/CA.Gov.ECCC.Weather.jstruct/schemas/CA.Gov.ECCC.Weather.WeatherObservation`](#schema-cagovecccweatherweatherobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `CA.Gov.ECCC.Weather.WeatherObservation` |
| `source` |  | `string` | `False` | `https://api.weather.gc.ca` |
| `subject` |  | `uritemplate` | `False` | `{msc_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `CA.Gov.ECCC.Weather.Kafka` | `KAFKA` | topic `environment-canada`; key `{msc_id}` |

## Schemagroups

### Schemagroup `CA.Gov.ECCC.Weather.jstruct`
<a id="schemagroup-cagovecccweatherjstruct"></a>

#### Schema `CA.Gov.ECCC.Weather.Station`
<a id="schema-cagovecccweatherstation"></a>

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
| $id | `https://api.weather.gc.ca/schemas/CA/Gov/ECCC/Weather/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data for an Environment Canada SWOB weather station. Stations are identified by their MSC ID (Meteorological Service of Canada identifier) and include WMO synoptic IDs where available.

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gc.ca/schemas/CA/Gov/ECCC/Weather/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `msc_id` | `string` | `True` | MSC station identifier (Meteorological Service of Canada ID), also known as Climate ID. Used as Kafka key. | - | - | - |
| `name` | `string` | `True` | Station name as listed in the SWOB station registry, e.g. 'TORONTO PEARSON INTL A', 'VANCOUVER INTL A'. | - | - | - |
| `iata_id` | `string` | `False` | IATA station code, e.g. 'CYYZ' for Toronto Pearson. | - | - | - |
| `wmo_id` | `union` | `False` | WMO synoptic station identifier, e.g. 71624 for Toronto Pearson. Null for stations without a WMO assignment. | - | - | - |
| `province_territory` | `string` | `False` | Canadian province or territory where the station is located, e.g. 'Ontario', 'British Columbia'. | - | - | - |
| `data_provider` | `string` | `False` | Organization providing the data, typically 'MSC' for Meteorological Service of Canada. | - | - | - |
| `dataset_network` | `string` | `False` | Network identifier, typically 'CA' for Canadian stations. | - | - | - |
| `auto_man` | `string` | `False` | Station type: 'AUTO' for automatic, 'MAN' for manual, or combination. | - | - | - |
| `latitude` | `union` | `False` | WGS84 latitude of the station in decimal degrees. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `union` | `False` | WGS84 longitude of the station in decimal degrees. | unit=`degree` symbol=`°` | - | - |
| `elevation` | `union` | `False` | Station elevation above sea level in meters. | unit=`m` symbol=`m` | - | - |

#### Schema `CA.Gov.ECCC.Weather.WeatherObservation`
<a id="schema-cagovecccweatherweatherobservation"></a>

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
| $id | `https://api.weather.gc.ca/schemas/CA/Gov/ECCC/Weather/WeatherObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherObservation`
<a id="schema-node-weatherobservation"></a>

Weather observation from an Environment Canada SWOB station. Fields are extracted from the verbose SWOB-ML record (200+ raw fields). The core meteorological parameters retained include temperature, humidity, dew point, pressure (station and sea-level), wind, precipitation, visibility, snow depth, cloud cover, pressure tendency, and 24-hour temperature extremes.

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gc.ca/schemas/CA/Gov/ECCC/Weather/WeatherObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `msc_id` | `string` | `True` | MSC station identifier. | - | - | - |
| `station_name` | `string` | `True` | Station name from the SWOB record. | - | - | - |
| `observation_time` | `datetime` | `True` | Observation timestamp in UTC from the obs_date_tm field. | - | - | - |
| `air_temperature` | `union` | `False` | Instantaneous air temperature from the air_temp field. | unit=`Cel` symbol=`°C` | - | - |
| `dew_point` | `union` | `False` | Dew point temperature from the dwpt_temp field. | unit=`Cel` symbol=`°C` | - | - |
| `relative_humidity` | `union` | `False` | Relative humidity from the rel_hum field. | unit=`percent` symbol=`%` | - | - |
| `station_pressure` | `union` | `False` | Station-level atmospheric pressure from the stn_pres field. | unit=`hPa` symbol=`hPa` | - | - |
| `wind_speed` | `union` | `False` | Average wind speed at 10m over the last 1 minute from avg_wnd_spd_10m_pst1mt. | unit=`km/h` symbol=`km/h` | - | - |
| `wind_direction` | `union` | `False` | Average wind direction at 10m over the last 1 minute from avg_wnd_dir_10m_pst1mt, in degrees clockwise from true north. | unit=`degree` symbol=`°` | - | - |
| `wind_gust` | `union` | `False` | Maximum wind speed at 10m in the last 1 minute from max_wnd_spd_10m_pst1mt. | unit=`km/h` symbol=`km/h` | - | - |
| `precipitation_1hr` | `union` | `False` | Total precipitation in the last hour from pcpn_amt_pst1hr. | unit=`mm` symbol=`mm` | - | - |
| `mean_sea_level_pressure` | `union` | `False` | Mean sea-level pressure (MSLP) from the mslp field. Available on synoptic and hourly reporting stations. Null on minutely auto-only stations. | unit=`hPa` symbol=`hPa`<br>altnames=`{"json": "mslp"}` | - | - |
| `visibility` | `union` | `False` | Horizontal visibility from the vis field. Primarily available on staffed and NAV CANADA stations. | unit=`km` symbol=`km`<br>altnames=`{"json": "vis"}` | - | - |
| `snow_depth` | `union` | `False` | Snow depth on the ground from the snw_dpth field. Available on stations equipped with ultrasonic snow depth sensors. | unit=`cm` symbol=`cm`<br>altnames=`{"json": "snw_dpth"}` | - | - |
| `total_cloud_cover` | `union` | `False` | Total cloud amount code from the tot_cld_amt field. Reports cloud cover in tenths (0-10) or oktas depending on reporting convention. Available on staffed and select automated stations. | altnames=`{"json": "tot_cld_amt"}` | - | - |
| `pressure_tendency_3hr` | `union` | `False` | Change in station pressure over the preceding 3 hours from pres_tend_amt_pst3hrs. Positive values indicate rising pressure. | unit=`hPa` symbol=`hPa`<br>altnames=`{"json": "pres_tend_amt_pst3hrs"}` | - | - |
| `max_temperature_24hr` | `union` | `False` | Maximum air temperature in the past 24 hours from max_air_temp_pst24hrs. | unit=`Cel` symbol=`°C`<br>altnames=`{"json": "max_air_temp_pst24hrs"}` | - | - |
| `min_temperature_24hr` | `union` | `False` | Minimum air temperature in the past 24 hours from min_air_temp_pst24hrs. | unit=`Cel` symbol=`°C`<br>altnames=`{"json": "min_air_temp_pst24hrs"}` | - | - |
| `wind_speed_1hr` | `union` | `False` | Average wind speed at 10m over the past hour from avg_wnd_spd_10m_pst1hr. | unit=`km/h` symbol=`km/h`<br>altnames=`{"json": "avg_wnd_spd_10m_pst1hr"}` | - | - |
| `wind_gust_1hr` | `union` | `False` | Maximum wind speed at 10m in the past hour from max_wnd_spd_10m_pst1hr. | unit=`km/h` symbol=`km/h`<br>altnames=`{"json": "max_wnd_spd_10m_pst1hr"}` | - | - |
| `precipitation_24hr` | `union` | `False` | Total precipitation in the past 24 hours from pcpn_amt_pst24hrs. | unit=`mm` symbol=`mm`<br>altnames=`{"json": "pcpn_amt_pst24hrs"}` | - | - |
| `altimeter_setting` | `union` | `False` | Altimeter setting from the altmetr_setng field. Used in aviation. | unit=`[in_i'Hg]` symbol=`inHg`<br>altnames=`{"json": "altmetr_setng"}` | - | - |
