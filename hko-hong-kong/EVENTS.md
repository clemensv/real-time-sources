# HKO Hong Kong Weather Observation Bridge Events

This bridge fetches real-time weather observations from the [Hong Kong Observatory (HKO)](https://www.hko.gov.hk/en/abouthko/opendata_intro.htm) and emits them as CloudEvents into Apache Kafka or Azure Event Hubs.

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

### Endpoint `HK.Gov.HKO.Weather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`HK.Gov.HKO.Weather`](#messagegroup-hkgovhkoweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `hko-hong-kong` |
| Kafka key | `{place_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `HK.Gov.HKO.Weather`
<a id="messagegroup-hkgovhkoweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `HK.Gov.HKO.Weather.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `HK.Gov.HKO.Weather.Station`
<a id="message-hkgovhkoweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/HK.Gov.HKO.Weather.jstruct/schemas/HK.Gov.HKO.Weather.Station`](#schema-hkgovhkoweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `HK.Gov.HKO.Weather.Station` |
| `source` |  | `string` | `False` | `https://data.weather.gov.hk` |
| `subject` |  | `uritemplate` | `False` | `{place_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `HK.Gov.HKO.Weather.Kafka` | `KAFKA` | topic `hko-hong-kong`; key `{place_id}` |

#### Message `HK.Gov.HKO.Weather.WeatherObservation`
<a id="message-hkgovhkoweatherweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/HK.Gov.HKO.Weather.jstruct/schemas/HK.Gov.HKO.Weather.WeatherObservation`](#schema-hkgovhkoweatherweatherobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `HK.Gov.HKO.Weather.WeatherObservation` |
| `source` |  | `string` | `False` | `https://data.weather.gov.hk` |
| `subject` |  | `uritemplate` | `False` | `{place_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `HK.Gov.HKO.Weather.Kafka` | `KAFKA` | topic `hko-hong-kong`; key `{place_id}` |

## Schemagroups

### Schemagroup `HK.Gov.HKO.Weather.jstruct`
<a id="schemagroup-hkgovhkoweatherjstruct"></a>

#### Schema `HK.Gov.HKO.Weather.Station`
<a id="schema-hkgovhkoweatherstation"></a>

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
| $id | `https://data.weather.gov.hk/schemas/HK/Gov/HKO/Weather/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data for a HKO weather observation place. Places include automatic weather stations (temperature), rainfall reporting districts, and special measurement locations (humidity at HKO headquarters, UV index at King's Park).

| Field | Value |
| --- | --- |
| $id | `https://data.weather.gov.hk/schemas/HK/Gov/HKO/Weather/Station` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `place_id` | `string` | `True` | URL-safe slug identifier derived from the English place name, e.g. 'kings-park', 'central-western-district'. Used as Kafka key and CloudEvents subject. | - | - | - |
| `name` | `string` | `True` | Original English place name from the HKO rhrread API, e.g. 'King's Park', 'Central & Western District'. | - | - | - |
| `data_types` | `string` | `True` | Comma-separated list of data types reported by this place. Values: 'temperature', 'rainfall', 'humidity', 'uvindex'. | - | - | - |

#### Schema `HK.Gov.HKO.Weather.WeatherObservation`
<a id="schema-hkgovhkoweatherweatherobservation"></a>

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
| $id | `https://data.weather.gov.hk/schemas/HK/Gov/HKO/Weather/WeatherObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherObservation`
<a id="schema-node-weatherobservation"></a>

Current weather observation for a HKO place from the rhrread endpoint. Temperature from automatic weather stations, rainfall from district-level rain gauges, humidity from HKO headquarters, UV index from King's Park. Fields are null when the place does not report that data type.

| Field | Value |
| --- | --- |
| $id | `https://data.weather.gov.hk/schemas/HK/Gov/HKO/Weather/WeatherObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `place_id` | `string` | `True` | URL-safe slug identifier for the place, matching the Kafka key. | - | - | - |
| `place_name` | `string` | `True` | Original English place name from the HKO API. | - | - | - |
| `observation_time` | `datetime` | `True` | ISO 8601 timestamp of the observation including Hong Kong timezone offset (+08:00), from the updateTime field. | - | - | - |
| `temperature` | `union` | `False` | Air temperature from automatic weather stations. | unit=`Cel` symbol=`°C` | - | - |
| `rainfall_max` | `union` | `False` | Maximum rainfall in the past hour from district-level rain gauges. | unit=`mm` symbol=`mm` | - | - |
| `humidity` | `union` | `False` | Relative humidity, currently only from Hong Kong Observatory headquarters. | unit=`percent` symbol=`%` | - | - |
| `uv_index` | `union` | `False` | UV index during the past hour, currently only from King's Park. | unit=`1` | - | - |
| `uv_description` | `union` | `False` | HKO descriptive UV level: 'low', 'moderate', 'high', 'very high', 'extreme'. | - | - | - |
