# NOAA NWS Weather Alerts Poller Events

**NOAA NWS Weather Alerts Poller** polls the National Weather Service (NWS) Weather Alerts API for active weather alerts across the United States and sends them to a Kafka topic as CloudEvents. The tool tracks previously seen alert IDs to avoid sending duplicates.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 3 |
| Messagegroups | 3 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `Microsoft.OpenData.US.NOAA.NWS.Alerts.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.NWS.Alerts`](#messagegroup-microsoftopendatausnoaanwsalerts) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-nws` |
| Kafka key | `{alert_id}` |
| Deployed | False |

### Endpoint `Microsoft.OpenData.US.NOAA.NWS.Zones.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.NWS.Zones`](#messagegroup-microsoftopendatausnoaanwszones) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-nws` |
| Kafka key | `{zone_id}` |
| Deployed | False |

### Endpoint `Microsoft.OpenData.US.NOAA.NWS.Observations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA.NWS.Observations`](#messagegroup-microsoftopendatausnoaanwsobservations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-nws` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Microsoft.OpenData.US.NOAA.NWS.Alerts`
<a id="messagegroup-microsoftopendatausnoaanwsalerts"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.NWS.Alerts.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Microsoft.OpenData.US.NOAA.NWS.WeatherAlert`
<a id="message-microsoftopendatausnoaanwsweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | WeatherAlert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NWS.jstruct/schemas/Microsoft.OpenData.US.NOAA.NWS.WeatherAlert`](#schema-microsoftopendatausnoaanwsweatheralert) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NWS.WeatherAlert` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{alert_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NWS.Alerts.Kafka` | `KAFKA` | topic `noaa-nws`; key `{alert_id}` |

### Messagegroup `Microsoft.OpenData.US.NOAA.NWS.Zones`
<a id="messagegroup-microsoftopendatausnoaanwszones"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.NWS.Zones.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Microsoft.OpenData.US.NOAA.NWS.Zone`
<a id="message-microsoftopendatausnoaanwszone"></a>

| Field | Value |
| --- | --- |
| Name | Zone |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NWS.jstruct/schemas/Microsoft.OpenData.US.NOAA.NWS.Zone`](#schema-microsoftopendatausnoaanwszone) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NWS.Zone` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{zone_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NWS.Zones.Kafka` | `KAFKA` | topic `noaa-nws`; key `{zone_id}` |

### Messagegroup `Microsoft.OpenData.US.NOAA.NWS.Observations`
<a id="messagegroup-microsoftopendatausnoaanwsobservations"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.NWS.Observations.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `Microsoft.OpenData.US.NOAA.NWS.ObservationStation`
<a id="message-microsoftopendatausnoaanwsobservationstation"></a>

| Field | Value |
| --- | --- |
| Name | ObservationStation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NWS.jstruct/schemas/Microsoft.OpenData.US.NOAA.NWS.ObservationStation`](#schema-microsoftopendatausnoaanwsobservationstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NWS.ObservationStation` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NWS.Observations.Kafka` | `KAFKA` | topic `noaa-nws`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.NWS.WeatherObservation`
<a id="message-microsoftopendatausnoaanwsweatherobservation"></a>

| Field | Value |
| --- | --- |
| Name | WeatherObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.NWS.jstruct/schemas/Microsoft.OpenData.US.NOAA.NWS.WeatherObservation`](#schema-microsoftopendatausnoaanwsweatherobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.NWS.WeatherObservation` |
| `source` |  | `string` | `False` | `https://api.weather.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.NWS.Observations.Kafka` | `KAFKA` | topic `noaa-nws`; key `{station_id}` |

## Schemagroups

### Schemagroup `Microsoft.OpenData.US.NOAA.NWS.jstruct`
<a id="schemagroup-microsoftopendatausnoaanwsjstruct"></a>

#### Schema `Microsoft.OpenData.US.NOAA.NWS.WeatherAlert`
<a id="schema-microsoftopendatausnoaanwsweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | WeatherAlert |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/Microsoft/OpenData/US/NOAA/NWS/WeatherAlert` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherAlert`
<a id="schema-node-weatheralert"></a>

Active weather alert from the NWS Common Alerting Protocol (CAP) feed. Alerts cover severe weather warnings, watches, advisories, and statements issued by NWS Weather Forecast Offices.

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/Microsoft/OpenData/US/NOAA/NWS/WeatherAlert` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `alert_id` | `string` | `True` |  | - | - | - |
| `area_desc` | `string` | `True` |  | - | - | - |
| `sent` | `datetime` | `True` |  | - | - | - |
| `effective` | `datetime` | `True` |  | - | - | - |
| `expires` | `datetime` | `True` |  | - | - | - |
| `status` | enum `['Actual', 'Exercise', 'System', 'Test', 'Draft']` | `True` |  | - | - | - |
| `message_type` | enum `['Alert', 'Update', 'Cancel']` | `True` |  | - | - | - |
| `category` | enum `['Met', 'Geo', 'Safety', 'Security', 'Rescue', 'Fire', 'Health', 'Env', 'Transport', 'Infra', 'CBRNE', 'Other']` | `False` |  | - | - | - |
| `severity` | enum `['Extreme', 'Severe', 'Moderate', 'Minor', 'Unknown']` | `True` |  | - | - | - |
| `certainty` | enum `['Observed', 'Likely', 'Possible', 'Unlikely', 'Unknown']` | `True` |  | - | - | - |
| `urgency` | enum `['Immediate', 'Expected', 'Future', 'Past', 'Unknown']` | `True` |  | - | - | - |
| `event` | `string` | `True` |  | - | - | - |
| `sender_name` | `string` | `False` |  | - | - | - |
| `headline` | `union` | `False` |  | - | - | - |
| `description` | `string` | `False` |  | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NWS.Zone`
<a id="schema-microsoftopendatausnoaanwszone"></a>

| Field | Value |
| --- | --- |
| Name | Zone |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/Microsoft/OpenData/US/NOAA/NWS/Zone` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Zone`
<a id="schema-node-zone"></a>

NWS forecast zone reference data. Zones partition the US into geographic areas for which forecasts and warnings are issued.

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/Microsoft/OpenData/US/NOAA/NWS/Zone` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `zone_id` | `string` | `True` | NWS zone identifier, e.g. 'NYZ072' for New York City. | - | - | - |
| `name` | `string` | `True` | Human-readable zone name. | - | - | - |
| `type` | `string` | `False` | Zone type: 'forecast', 'county', 'fire', 'coastal', or 'offshore'. | - | - | - |
| `state` | `string` | `True` | Two-letter US state or territory abbreviation. | - | - | - |
| `forecast_office` | `string` | `False` | NWS Weather Forecast Office (WFO) responsible for this zone, e.g. 'OKX'. | - | - | - |
| `timezone` | `string` | `False` | IANA timezone name for the zone, e.g. 'America/New_York'. | - | - | - |
| `radar_station` | `union` | `False` | Nearest NEXRAD radar station identifier, or null if none assigned. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NWS.ObservationStation`
<a id="schema-microsoftopendatausnoaanwsobservationstation"></a>

| Field | Value |
| --- | --- |
| Name | ObservationStation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/Microsoft/OpenData/US/NOAA/NWS/ObservationStation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ObservationStation`
<a id="schema-node-observationstation"></a>

NWS surface weather observation station reference data from the api.weather.gov /stations endpoint. Each station represents a fixed automated or manual observing site in the US.

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/Microsoft/OpenData/US/NOAA/NWS/ObservationStation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Station identifier, typically a 4-character ICAO code such as 'KJFK' or a cooperative observer ID. | - | - | - |
| `name` | `string` | `True` | Human-readable station name, e.g. 'New York, Kennedy International Airport'. | - | - | - |
| `elevation_m` | `union` | `False` | Station elevation above mean sea level. | unit=`m` symbol=`m` | - | - |
| `time_zone` | `union` | `False` | IANA timezone of the station, e.g. 'America/New_York'. | - | - | - |
| `forecast_zone` | `union` | `False` | NWS forecast zone identifier associated with this station. | - | - | - |
| `county` | `union` | `False` | NWS county zone identifier for the station's location. | - | - | - |
| `fire_weather_zone` | `union` | `False` | NWS fire weather zone identifier for the station's location. | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.NWS.WeatherObservation`
<a id="schema-microsoftopendatausnoaanwsweatherobservation"></a>

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
| $id | `https://api.weather.gov/schemas/Microsoft/OpenData/US/NOAA/NWS/WeatherObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `WeatherObservation`
<a id="schema-node-weatherobservation"></a>

Latest weather observation from a NWS surface station. Observations are fetched from the api.weather.gov /stations/{stationId}/observations/latest endpoint. Measurement values are extracted from NWS quantity objects (unitCode + value + qualityControl).

| Field | Value |
| --- | --- |
| $id | `https://api.weather.gov/schemas/Microsoft/OpenData/US/NOAA/NWS/WeatherObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | ICAO or cooperative observer station identifier. | - | - | - |
| `timestamp` | `datetime` | `True` | UTC timestamp of the observation. | - | - | - |
| `text_description` | `union` | `False` | Brief text summary of current conditions, e.g. 'Clear', 'Mostly Cloudy', 'Rain'. | - | - | - |
| `temperature` | `union` | `False` | Air temperature at the time of observation. | unit=`Cel` symbol=`°C` | - | - |
| `dewpoint` | `union` | `False` | Dew point temperature. | unit=`Cel` symbol=`°C` | - | - |
| `wind_direction` | `union` | `False` | Wind direction in degrees from which the wind is blowing. | unit=`degree` symbol=`°` | - | - |
| `wind_speed` | `union` | `False` | Sustained wind speed. | unit=`km/h` symbol=`km/h` | - | - |
| `wind_gust` | `union` | `False` | Peak wind gust speed, null if no gusts observed. | unit=`km/h` symbol=`km/h` | - | - |
| `barometric_pressure` | `union` | `False` | Station barometric pressure (not reduced to sea level). | unit=`Pa` symbol=`Pa` | - | - |
| `sea_level_pressure` | `union` | `False` | Atmospheric pressure reduced to mean sea level. | unit=`Pa` symbol=`Pa` | - | - |
| `visibility` | `union` | `False` | Horizontal visibility. | unit=`m` symbol=`m` | - | - |
| `relative_humidity` | `union` | `False` | Relative humidity percentage. | unit=`percent` symbol=`%` | - | - |
| `wind_chill` | `union` | `False` | Calculated wind chill temperature, null when conditions do not warrant it. | unit=`Cel` symbol=`°C` | - | - |
| `heat_index` | `union` | `False` | Calculated heat index temperature, null when conditions do not warrant it. | unit=`Cel` symbol=`°C` | - | - |

### Schemagroup `Microsoft.OpenData.US.NOAA.NWS.avro`
<a id="schemagroup-microsoftopendatausnoaanwsavro"></a>

#### Schema `Microsoft.OpenData.US.NOAA.NWS.WeatherAlert`
<a id="schema-microsoftopendatausnoaanwsweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | WeatherAlert |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WeatherAlert |
| Namespace | Microsoft.OpenData.US.NOAA.NWS |
| Type | `record` |
| Doc | WeatherAlert |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `alert_id` | `string` |  | `-` |
| `area_desc` | `string` |  | `-` |
| `sent` | `string` |  | `-` |
| `effective` | `string` |  | `-` |
| `expires` | `string` |  | `-` |
| `status` | `string` |  | `-` |
| `message_type` | `string` |  | `-` |
| `category` | `null` \| `string` |  | `-` |
| `severity` | `string` |  | `-` |
| `certainty` | `string` |  | `-` |
| `urgency` | `string` |  | `-` |
| `event` | `string` |  | `-` |
| `sender_name` | `null` \| `string` |  | `-` |
| `headline` | `null` \| `string` |  | `-` |
| `description` | `null` \| `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.NWS.Zone`
<a id="schema-microsoftopendatausnoaanwszone"></a>

| Field | Value |
| --- | --- |
| Name | Zone |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Zone |
| Namespace | Microsoft.OpenData.US.NOAA.NWS |
| Type | `record` |
| Doc | Zone |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `zone_id` | `string` |  | `-` |
| `name` | `string` |  | `-` |
| `type` | `null` \| `string` |  | `-` |
| `state` | `string` |  | `-` |
| `forecast_office` | `null` \| `string` |  | `-` |
| `timezone` | `null` \| `string` |  | `-` |
| `radar_station` | `null` \| `string` |  | `-` |
