# KMI Belgium Weather Observation Bridge Events

This bridge fetches real-time automatic weather station observations from the [Royal Meteorological Institute of Belgium (KMI/RMI)](https://opendata.meteo.be/) and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

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

### Endpoint `BE.Gov.KMI.Weather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`BE.Gov.KMI.Weather`](#messagegroup-begovkmiweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `kmi-belgium` |
| Kafka key | `{station_code}` |
| Deployed | False |

## Messagegroups

### Messagegroup `BE.Gov.KMI.Weather`
<a id="messagegroup-begovkmiweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `BE.Gov.KMI.Weather.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `BE.Gov.KMI.Weather.Station`
<a id="message-begovkmiweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BE.Gov.KMI.Weather.jstruct/schemas/BE.Gov.KMI.Weather.Station`](#schema-begovkmiweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `BE.Gov.KMI.Weather.Station` |
| `source` |  | `string` | `False` | `https://opendata.meteo.be` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BE.Gov.KMI.Weather.Kafka` | `KAFKA` | topic `kmi-belgium`; key `{station_code}` |

#### Message `BE.Gov.KMI.Weather.WeatherObservation`
<a id="message-begovkmiweatherweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BE.Gov.KMI.Weather.jstruct/schemas/BE.Gov.KMI.Weather.WeatherObservation`](#schema-begovkmiweatherweatherobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `BE.Gov.KMI.Weather.WeatherObservation` |
| `source` |  | `string` | `False` | `https://opendata.meteo.be` |
| `subject` |  | `uritemplate` | `False` | `{station_code}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BE.Gov.KMI.Weather.Kafka` | `KAFKA` | topic `kmi-belgium`; key `{station_code}` |

## Schemagroups

### Schemagroup `BE.Gov.KMI.Weather.jstruct`
<a id="schemagroup-begovkmiweatherjstruct"></a>

#### Schema `BE.Gov.KMI.Weather.Station`
<a id="schema-begovkmiweatherstation"></a>

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
| $id | `https://opendata.meteo.be/schemas/BE/Gov/KMI/Weather/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference metadata for a KMI/RMI automatic weather station derived from the latest aws:aws_10min observation features published through the public WFS service.

| Field | Value |
| --- | --- |
| $id | `https://opendata.meteo.be/schemas/BE/Gov/KMI/Weather/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_code` | `string` | `True` | KMI/RMI automatic weather station code from the GeoJSON feature property `code`, unique within the Belgian AWS network. | - | - | - |
| `latitude` | `double` | `True` | Geographic latitude of the station in decimal degrees (WGS 84), derived from the second value of the GeoJSON `geometry.coordinates` array. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | Geographic longitude of the station in decimal degrees (WGS 84), derived from the first value of the GeoJSON `geometry.coordinates` array. | unit=`degree` symbol=`°` | - | - |

#### Schema `BE.Gov.KMI.Weather.WeatherObservation`
<a id="schema-begovkmiweatherweatherobservation"></a>

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
| $id | `https://opendata.meteo.be/schemas/BE/Gov/KMI/Weather/WeatherObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherObservation`
<a id="schema-node-weatherobservation"></a>

Ten-minute automatic weather station observation from the KMI/RMI aws:aws_10min feed, containing precipitation, temperature, wind, humidity, pressure, radiation, and soil measurements.

| Field | Value |
| --- | --- |
| $id | `https://opendata.meteo.be/schemas/BE/Gov/KMI/Weather/WeatherObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_code` | `string` | `True` | KMI/RMI automatic weather station code from the `code` property of the reporting observation feature. | - | - | - |
| `observation_time` | `datetime` | `True` | Observation timestamp in UTC from the feature property `timestamp`. | - | - | - |
| `precip_quantity` | `union` | `False` | Precipitation quantity reported for the 10-minute observation period. | unit=`mm` symbol=`mm` | - | - |
| `temp_dry_shelter_avg` | `union` | `False` | Average air temperature measured in the 2 m dry shelter during the observation period. | unit=`Cel` symbol=`°C` | - | - |
| `temp_grass_pt100_avg` | `union` | `False` | Average grass-level temperature measured by the Pt100 sensor during the observation period. | unit=`Cel` symbol=`°C` | - | - |
| `temp_soil_avg` | `union` | `False` | Average soil surface temperature during the observation period. | unit=`Cel` symbol=`°C` | - | - |
| `temp_soil_avg_5cm` | `union` | `False` | Average soil temperature measured at 5 cm depth during the observation period. | unit=`Cel` symbol=`°C` | - | - |
| `temp_soil_avg_10cm` | `union` | `False` | Average soil temperature measured at 10 cm depth during the observation period. | unit=`Cel` symbol=`°C` | - | - |
| `temp_soil_avg_20cm` | `union` | `False` | Average soil temperature measured at 20 cm depth during the observation period. | unit=`Cel` symbol=`°C` | - | - |
| `temp_soil_avg_50cm` | `union` | `False` | Average soil temperature measured at 50 cm depth during the observation period. | unit=`Cel` symbol=`°C` | - | - |
| `wind_speed_10m` | `union` | `False` | Wind speed measured at 10 m above ground level. | unit=`m/s` symbol=`m/s` | - | - |
| `wind_speed_avg_30m` | `union` | `False` | Average wind speed measured at 30 m above ground level. | unit=`m/s` symbol=`m/s` | - | - |
| `wind_direction` | `union` | `False` | Wind direction in degrees from which the wind is blowing. | unit=`degree` symbol=`°` | - | - |
| `wind_gusts_speed` | `union` | `False` | Maximum wind gust speed observed during the 10-minute period. | unit=`m/s` symbol=`m/s` | - | - |
| `humidity_rel_shelter_avg` | `union` | `False` | Average relative humidity measured in the shelter during the observation period. | unit=`percent` symbol=`%` | - | - |
| `pressure` | `union` | `False` | Station-level atmospheric pressure reported by the automatic weather station. | unit=`hPa` symbol=`hPa` | - | - |
| `sun_duration` | `union` | `False` | Sunshine duration accumulated during the 10-minute observation period. | unit=`min` symbol=`min` | - | - |
| `short_wave_from_sky_avg` | `union` | `False` | Average downward shortwave radiation from the sky during the observation period. | unit=`W/m2` symbol=`W/m²` | - | - |
| `sun_int_avg` | `union` | `False` | Average direct sunshine intensity during the observation period. | unit=`W/m2` symbol=`W/m²` | - | - |
