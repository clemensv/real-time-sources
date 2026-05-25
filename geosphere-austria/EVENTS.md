# GeoSphere Austria — TAWES Weather Observations Events

This bridge polls 10-minute weather observations from the [GeoSphere Austria](https://geosphere.at) TAWES (Teilautomatische Wetterstationen) automatic station network and emits them as CloudEvents into Apache Kafka.

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

### Endpoint `at.geosphere.tawes.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`at.geosphere.tawes`](#messagegroup-atgeospheretawes) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `geosphere-austria-tawes` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `at.geosphere.tawes`
<a id="messagegroup-atgeospheretawes"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `at.geosphere.tawes.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `at.geosphere.tawes.WeatherStation`
<a id="message-atgeospheretawesweatherstation"></a>

Reference data for a GeoSphere Austria TAWES automatic weather station, including location, elevation, and federal state.

| Field | Value |
| --- | --- |
| Name | WeatherStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/at.geosphere.tawes.jstruct/schemas/at.geosphere.tawes.WeatherStation`](#schema-atgeospheretawesweatherstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `at.geosphere.tawes.WeatherStation` |
| `source` |  | `uritemplate` | `False` | `https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min/metadata` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `at.geosphere.tawes.Kafka` | `KAFKA` | topic `geosphere-austria-tawes`; key `{station_id}` |

#### Message `at.geosphere.tawes.WeatherObservation`
<a id="message-atgeospheretawesweatherobservation"></a>

10-minute weather observation from a GeoSphere Austria TAWES station, including temperature, humidity, precipitation, wind, pressure, sunshine duration, and global radiation.

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/at.geosphere.tawes.jstruct/schemas/at.geosphere.tawes.WeatherObservation`](#schema-atgeospheretawesweatherobservation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `at.geosphere.tawes.WeatherObservation` |
| `source` |  | `uritemplate` | `False` | `https://dataset.api.hub.geosphere.at/v1/station/current/tawes-v1-10min` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `at.geosphere.tawes.Kafka` | `KAFKA` | topic `geosphere-austria-tawes`; key `{station_id}` |

## Schemagroups

### Schemagroup `at.geosphere.tawes.jstruct`
<a id="schemagroup-atgeospheretawesjstruct"></a>

#### Schema `at.geosphere.tawes.WeatherStation`
<a id="schema-atgeospheretawesweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://geosphere.at/schemas/at/geosphere/tawes/WeatherStation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/at/geosphere/tawes/WeatherStation` |
| Type | `object` |

###### Object `WeatherStation`
<a id="schema-node-weatherstation"></a>

Reference data for a GeoSphere Austria TAWES (Teilautomatische Wetterstationen) automatic weather station. The station identifier is the GeoSphere numeric station ID. Metadata is sourced from the TAWES v1 10-minute current dataset metadata endpoint.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable GeoSphere Austria numeric station identifier used as the Kafka key and CloudEvents subject. Mapped from the upstream 'id' field in the station metadata. | - | pattern=`^[0-9]+$` | - |
| `station_name` | `string` | `True` | Station name from the GeoSphere metadata, for example 'WIEN HOHE WARTE' or 'INNSBRUCK FLUGHAFEN'. Mapped from the upstream 'name' field. | - | - | - |
| `latitude` | `double` | `True` | WGS84 latitude of the station in decimal degrees, sourced from the GeoSphere metadata 'lat' field. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | WGS84 longitude of the station in decimal degrees, sourced from the GeoSphere metadata 'lon' field. | unit=`degree` symbol=`°` | - | - |
| `altitude` | `double` | `True` | Station altitude above sea level in meters, sourced from the GeoSphere metadata 'altitude' field. | unit=`meter` symbol=`m` | - | - |
| `state` | `union` | `True` | Austrian federal state (Bundesland) where the station is located, for example 'Wien', 'Tirol', 'Steiermark'. Sourced from the GeoSphere metadata 'state' field. Null when the metadata does not include a state. | - | - | - |

#### Schema `at.geosphere.tawes.WeatherObservation`
<a id="schema-atgeospheretawesweatherobservation"></a>

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
| $id | `https://geosphere.at/schemas/at/geosphere/tawes/WeatherObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/at/geosphere/tawes/WeatherObservation` |
| Type | `object` |

###### Object `WeatherObservation`
<a id="schema-node-weatherobservation"></a>

10-minute weather observation from a GeoSphere Austria TAWES station. Each event contains the latest observation for a single station with all requested meteorological parameters. Values are null when the station does not report a parameter or the measurement is missing for the current interval.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | GeoSphere Austria numeric station identifier for the observing station. Mapped from the upstream 'station' property in the GeoJSON features. | - | pattern=`^[0-9]+$` | - |
| `observation_time` | `string` | `True` | Observation timestamp in UTC from the GeoSphere API 'timestamps' array, formatted as an ISO-8601 instant such as '2024-01-15T13:00:00+00:00'. | - | - | - |
| `temperature` | `union` | `True` | Air temperature (Lufttemperatur) in degrees Celsius over the 10-minute interval, from the GeoSphere TL parameter. Null when the station does not report this parameter. | unit=`degree Celsius` symbol=`°C`<br>altnames=`{"json": "TL"}` | - | - |
| `humidity` | `union` | `True` | Relative humidity (Relative Feuchte) as a percentage over the 10-minute interval, from the GeoSphere RF parameter. Null when not reported. | unit=`percent` symbol=`%`<br>altnames=`{"json": "RF"}` | - | - |
| `precipitation` | `union` | `True` | Precipitation (Niederschlag) in millimeters accumulated during the 10-minute interval, from the GeoSphere RR parameter. Null when not reported. | unit=`millimeter` symbol=`mm`<br>altnames=`{"json": "RR"}` | - | - |
| `wind_direction` | `union` | `True` | Wind direction (Windrichtung) in degrees over the 10-minute interval, from the GeoSphere DD parameter. 0 indicates north, 90 east, 180 south, 270 west. Null when not reported. | unit=`degree` symbol=`°`<br>altnames=`{"json": "DD"}` | - | - |
| `wind_speed` | `union` | `True` | Wind speed (Windgeschwindigkeit) in meters per second over the 10-minute interval, from the GeoSphere FF parameter. Null when not reported. | unit=`meter per second` symbol=`m/s`<br>altnames=`{"json": "FF"}` | - | - |
| `pressure` | `union` | `True` | Atmospheric pressure (Luftdruck) in hectopascals at station level over the 10-minute interval, from the GeoSphere P parameter. Null when not reported. | unit=`hectopascal` symbol=`hPa`<br>altnames=`{"json": "P"}` | - | - |
| `sunshine_duration` | `union` | `True` | Sunshine duration (Sonnenscheindauer) in seconds during the 10-minute interval, from the GeoSphere SO parameter. Null when the station does not have a sunshine sensor (has_sunshine=false) or the value is missing. | unit=`second` symbol=`s`<br>altnames=`{"json": "SO"}` | - | - |
| `global_radiation` | `union` | `True` | Global radiation (Globalstrahlung) in watts per square meter during the 10-minute interval, from the GeoSphere GLOW parameter. Null when the station does not have a radiation sensor (has_global_radiation=false) or the value is missing. | unit=`watt per square meter` symbol=`W/m²`<br>altnames=`{"json": "GLOW"}` | - | - |

### Schemagroup `at.geosphere.tawes.avro`
<a id="schemagroup-atgeospheretawesavro"></a>

#### Schema `at.geosphere.tawes.WeatherStation`
<a id="schema-atgeospheretawesweatherstation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherStation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WeatherStation |
| Namespace | at.geosphere.tawes |
| Type | `record` |
| Doc | Reference data for a GeoSphere Austria TAWES automatic weather station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Stable GeoSphere Austria numeric station identifier. | `-` |
| `station_name` | `string` | Station name from the GeoSphere metadata. | `-` |
| `latitude` | `double` | WGS84 latitude of the station in decimal degrees. | `-` |
| `longitude` | `double` | WGS84 longitude of the station in decimal degrees. | `-` |
| `altitude` | `double` | Station altitude above sea level in meters. | `-` |
| `state` | `null` \| `string` | Austrian federal state (Bundesland) where the station is located. | `-` |

#### Schema `at.geosphere.tawes.WeatherObservation`
<a id="schema-atgeospheretawesweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Namespace | at.geosphere.tawes |
| Type | `record` |
| Doc | 10-minute weather observation from a GeoSphere Austria TAWES station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | GeoSphere Austria numeric station identifier for the observing station. | `-` |
| `observation_time` | `string` | Observation timestamp in UTC from the GeoSphere API timestamps array. | `-` |
| `temperature` | `null` \| `double` | Air temperature in degrees Celsius over the 10-minute interval. | `-` |
| `humidity` | `null` \| `double` | Relative humidity as a percentage over the 10-minute interval. | `-` |
| `precipitation` | `null` \| `double` | Precipitation in millimeters accumulated during the 10-minute interval. | `-` |
| `wind_direction` | `null` \| `double` | Wind direction in degrees over the 10-minute interval. | `-` |
| `wind_speed` | `null` \| `double` | Wind speed in meters per second over the 10-minute interval. | `-` |
| `pressure` | `null` \| `double` | Atmospheric pressure in hectopascals at station level. | `-` |
| `sunshine_duration` | `null` \| `double` | Sunshine duration in seconds during the 10-minute interval. | `-` |
| `global_radiation` | `null` \| `double` | Global radiation in watts per square meter during the 10-minute interval. | `-` |
