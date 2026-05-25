# BOM Australia Weather Observations Events

Real-time weather observations from the [Australian Bureau of Meteorology](http://www.bom.gov.au/) (BOM).

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

### Endpoint `AU.Gov.BOM.Weather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`AU.Gov.BOM.Weather`](#messagegroup-augovbomweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `bom-australia` |
| Kafka key | `{station_wmo}` |
| Deployed | False |

### Endpoint `AU.Gov.BOM.Warning.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`AU.Gov.BOM.Warning`](#messagegroup-augovbomwarning) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `bom-australia` |
| Kafka key | `{warning_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `AU.Gov.BOM.Weather`
<a id="messagegroup-augovbomweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `AU.Gov.BOM.Weather.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `AU.Gov.BOM.Weather.Station`
<a id="message-augovbomweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/AU.Gov.BOM.Weather.jstruct/schemas/AU.Gov.BOM.Weather.Station`](#schema-augovbomweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `AU.Gov.BOM.Weather.Station` |
| `source` |  | `string` | `False` | `http://reg.bom.gov.au/fwo` |
| `subject` |  | `uritemplate` | `False` | `{station_wmo}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `AU.Gov.BOM.Weather.Kafka` | `KAFKA` | topic `bom-australia`; key `{station_wmo}` |

#### Message `AU.Gov.BOM.Weather.WeatherObservation`
<a id="message-augovbomweatherweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/AU.Gov.BOM.Weather.jstruct/schemas/AU.Gov.BOM.Weather.WeatherObservation`](#schema-augovbomweatherweatherobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `AU.Gov.BOM.Weather.WeatherObservation` |
| `source` |  | `string` | `False` | `http://reg.bom.gov.au/fwo` |
| `subject` |  | `uritemplate` | `False` | `{station_wmo}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `AU.Gov.BOM.Weather.Kafka` | `KAFKA` | topic `bom-australia`; key `{station_wmo}` |

### Messagegroup `AU.Gov.BOM.Warning`
<a id="messagegroup-augovbomwarning"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `AU.Gov.BOM.Warning.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `AU.Gov.BOM.Warning.WarningBulletin`
<a id="message-augovbomwarningwarningbulletin"></a>

| Field | Value |
| --- | --- |
| Name | WarningBulletin |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/AU.Gov.BOM.Warning.jstruct/schemas/AU.Gov.BOM.Warning.WarningBulletin`](#schema-augovbomwarningwarningbulletin) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `AU.Gov.BOM.Warning.WarningBulletin` |
| `source` |  | `string` | `False` | `https://www.bom.gov.au/rss/` |
| `subject` |  | `uritemplate` | `False` | `{warning_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `AU.Gov.BOM.Warning.Kafka` | `KAFKA` | topic `bom-australia`; key `{warning_id}` |

## Schemagroups

### Schemagroup `AU.Gov.BOM.Weather.jstruct`
<a id="schemagroup-augovbomweatherjstruct"></a>

#### Schema `AU.Gov.BOM.Weather.Station`
<a id="schema-augovbomweatherstation"></a>

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
| $id | `https://bom.gov.au/schemas/AU/Gov/BOM/Weather/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference metadata for a BOM weather observation station identified by its WMO station number. Stations report half-hourly surface observations covering temperature, wind, pressure, rainfall, humidity, cloud, and visibility.

| Field | Value |
| --- | --- |
| $id | `https://bom.gov.au/schemas/AU/Gov/BOM/Weather/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_wmo` | `int32` | `True` | WMO station number assigned by the World Meteorological Organization, used as the stable identity for this station across all BOM products. | - | - | - |
| `name` | `string` | `True` | Human-readable station name as assigned by the Bureau of Meteorology, e.g. 'Sydney Airport' or 'Melbourne Airport'. | - | - | - |
| `product_id` | `string` | `False` | BOM product code identifying the observation product this station belongs to, e.g. 'IDN60901' for NSW capital city observations. | - | - | - |
| `state` | `string` | `False` | Australian state or territory the station is located in, as reported by BOM, e.g. 'New South Wales', 'Victoria'. | - | - | - |
| `time_zone` | `string` | `False` | Abbreviation of the local time zone for the station, e.g. 'EST' for Eastern Standard Time, 'CST' for Central Standard Time. | - | - | - |
| `latitude` | `double` | `True` | Geographic latitude of the station in decimal degrees (negative for Southern Hemisphere). | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | Geographic longitude of the station in decimal degrees. | unit=`degree` symbol=`°` | - | - |

#### Schema `AU.Gov.BOM.Weather.WeatherObservation`
<a id="schema-augovbomweatherweatherobservation"></a>

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
| $id | `https://bom.gov.au/schemas/AU/Gov/BOM/Weather/WeatherObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherObservation`
<a id="schema-node-weatherobservation"></a>

Half-hourly surface weather observation from a BOM automatic weather station. Each record contains temperature, wind, pressure, humidity, rainfall, cloud, and visibility measurements as reported in the station's 72-hour observation product.

| Field | Value |
| --- | --- |
| $id | `https://bom.gov.au/schemas/AU/Gov/BOM/Weather/WeatherObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_wmo` | `int32` | `True` | WMO station number identifying the reporting station. | - | - | - |
| `station_name` | `string` | `True` | Human-readable name of the reporting station. | - | - | - |
| `observation_time_utc` | `datetime` | `True` | Timestamp of the observation in UTC, derived from the BOM 'aifstime_utc' field in YYYYMMDDHHmmss format. | - | - | - |
| `local_time` | `string` | `False` | Local date and time string as provided by BOM in 'local_date_time_full' format (YYYYMMDDHHmmss). | - | - | - |
| `air_temp` | `union` | `False` | Air temperature measured at the station. | unit=`Cel` symbol=`°C` | - | - |
| `apparent_temp` | `union` | `False` | Apparent (feels-like) temperature combining air temperature, humidity, and wind chill effects. | unit=`Cel` symbol=`°C` | - | - |
| `dewpt` | `union` | `False` | Dew point temperature at the station. | unit=`Cel` symbol=`°C` | - | - |
| `rel_hum` | `union` | `False` | Relative humidity as a percentage. | unit=`percent` symbol=`%` | - | - |
| `delta_t` | `union` | `False` | Wet bulb depression (difference between dry and wet bulb temperatures), used for bushfire danger calculations. | unit=`Cel` symbol=`°C` | - | - |
| `wind_dir` | `union` | `False` | Compass direction the wind is blowing from, e.g. 'N', 'NNE', 'SSW', 'CALM'. | - | - | - |
| `wind_spd_kmh` | `union` | `False` | Sustained wind speed in kilometres per hour. | unit=`km/h` symbol=`km/h` | - | - |
| `wind_spd_kt` | `union` | `False` | Sustained wind speed in knots (nautical miles per hour). | unit=`knot` symbol=`kt` | - | - |
| `gust_kmh` | `union` | `False` | Maximum wind gust speed recorded in the observation period in kilometres per hour. | unit=`km/h` symbol=`km/h` | - | - |
| `gust_kt` | `union` | `False` | Maximum wind gust speed recorded in the observation period in knots. | unit=`knot` symbol=`kt` | - | - |
| `press` | `union` | `False` | Atmospheric pressure at station level. | unit=`hPa` symbol=`hPa` | - | - |
| `press_qnh` | `union` | `False` | QNH pressure — atmospheric pressure adjusted to mean sea level using the International Standard Atmosphere, used in aviation altimetry. | unit=`hPa` symbol=`hPa` | - | - |
| `press_msl` | `union` | `False` | Mean sea level pressure — station pressure reduced to sea level, used for synoptic weather analysis. | unit=`hPa` symbol=`hPa` | - | - |
| `press_tend` | `union` | `False` | Pressure tendency description indicating whether pressure is rising, falling, or steady over the past 3 hours. May be a numeric code or textual description. | - | - | - |
| `rain_trace` | `union` | `False` | Rainfall since 9am local time as reported by BOM. Value is a string that may be '0.0', a numeric amount in mm, or 'Trace' for very small amounts. | - | - | - |
| `cloud` | `union` | `False` | Textual cloud cover description, e.g. 'Partly cloudy', 'Clear', 'Overcast'. | - | - | - |
| `cloud_oktas` | `union` | `False` | Cloud cover in oktas (eighths of sky covered), ranging from 0 (clear) to 8 (overcast). | - | - | - |
| `cloud_base_m` | `union` | `False` | Height of the lowest cloud base above ground level. | unit=`m` symbol=`m` | - | - |
| `cloud_type` | `union` | `False` | Cloud type classification as reported by the station, e.g. 'Cu', 'Cb', 'St'. May be '-' when not reported. | - | - | - |
| `vis_km` | `union` | `False` | Horizontal visibility in kilometres. Reported as a string as BOM may include qualifiers. | - | - | - |
| `weather` | `union` | `False` | Present weather description, e.g. 'Rain', 'Fog', 'Thunderstorm'. May be '-' when no significant weather. | - | - | - |
| `sea_state` | `union` | `False` | Sea state description for coastal stations, e.g. 'Smooth', 'Slight', 'Moderate'. | - | - | - |
| `swell_dir_worded` | `union` | `False` | Dominant swell direction as a compass bearing word for coastal stations. | - | - | - |
| `swell_height` | `union` | `False` | Dominant swell height for coastal stations. | unit=`m` symbol=`m` | - | - |
| `swell_period` | `union` | `False` | Dominant swell period for coastal stations. | unit=`s` symbol=`s` | - | - |
| `latitude` | `double` | `False` | Latitude of the station at observation time. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `False` | Longitude of the station at observation time. | unit=`degree` symbol=`°` | - | - |

### Schemagroup `AU.Gov.BOM.Warning.jstruct`
<a id="schemagroup-augovbomwarningjstruct"></a>

#### Schema `AU.Gov.BOM.Warning.WarningBulletin`
<a id="schema-augovbomwarningwarningbulletin"></a>

| Field | Value |
| --- | --- |
| Name | WarningBulletin |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://bom.gov.au/schemas/AU/Gov/BOM/Warning/WarningBulletin` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WarningBulletin`
<a id="schema-node-warningbulletin"></a>

Current weather warning bulletin item from a Bureau of Meteorology RSS warnings feed. Each item points to the published warning product page and carries the update timestamp and headline text from the feed.

| Field | Value |
| --- | --- |
| $id | `https://bom.gov.au/schemas/AU/Gov/BOM/Warning/WarningBulletin` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `warning_id` | `string` | `True` | Stable BOM warning product identifier derived from the linked product page path, for example 'IDN21037'. | - | - | - |
| `warning_url` | `string` | `True` | Absolute BOM URL of the warning product page linked from the RSS item. | - | - | - |
| `feed_url` | `string` | `True` | Absolute BOM RSS feed URL that published this warning item. | - | - | - |
| `feed_title` | `string` | `True` | Title of the RSS feed channel publishing this warning bulletin. | - | - | - |
| `title` | `string` | `True` | Normalized warning headline text from the RSS item title with line breaks collapsed to spaces. | - | - | - |
| `published_at` | `datetime` | `True` | UTC timestamp when the RSS item was created or updated, taken from the item's pubDate field. | - | - | - |
| `issued_local_time_text` | `union` | `False` | Local issuance time prefix embedded in the RSS headline, for example '08/16:29 EST', when present. | - | - | - |
| `warning_type` | `union` | `False` | Warning headline extracted from the RSS title before the trailing affected-area clause, for example 'Severe Weather Warning'. | - | - | - |
| `affected_area_text` | `union` | `False` | Affected area clause extracted from the RSS title after the word 'for', for example 'parts of Snowy Mountains Forecast District.'. | - | - | - |
