# DWD Open Data Bridge Usage Guide Events

**DWD Open Data Bridge** polls the [Deutscher Wetterdienst (DWD) Climate Data Center](https://opendata.dwd.de/) open-data file server for weather observations, station metadata, and weather alerts from ~1,450 stations across Germany. The data is forwarded to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 4 |
| Messagegroups | 4 |
| Schemagroups | 3 |

## Endpoints

### Endpoint `DE.DWD.CDC.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`DE.DWD.CDC`](#messagegroup-dedwdcdc) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `dwd` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `DE.DWD.Weather.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`DE.DWD.Weather`](#messagegroup-dedwdweather) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `dwd` |
| Kafka key | `{identifier}` |
| Deployed | False |

### Endpoint `DE.DWD.Radar.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`DE.DWD.Radar`](#messagegroup-dedwdradar) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `dwd` |
| Kafka key | `{file_url}` |
| Deployed | False |

### Endpoint `DE.DWD.Forecast.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`DE.DWD.Forecast`](#messagegroup-dedwdforecast) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `dwd` |
| Kafka key | `{file_url}` |
| Deployed | False |

## Messagegroups

### Messagegroup `DE.DWD.CDC`
<a id="messagegroup-dedwdcdc"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `DE.DWD.CDC.Kafka` (KAFKA) |
| Messages | 8 |

#### Message `DE.DWD.CDC.StationMetadata`
<a id="message-dedwdcdcstationmetadata"></a>

| Field | Value |
| --- | --- |
| Name | StationMetadata |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.CDC.StationMetadata`](#schema-dedwdcdcstationmetadata) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.CDC.StationMetadata` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.CDC.Kafka` | `KAFKA` | topic `dwd`; key `{station_id}` |

#### Message `DE.DWD.CDC.AirTemperature10Min`
<a id="message-dedwdcdcairtemperature10min"></a>

| Field | Value |
| --- | --- |
| Name | AirTemperature10Min |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.CDC.AirTemperature10Min`](#schema-dedwdcdcairtemperature10min) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.CDC.AirTemperature10Min` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.CDC.Kafka` | `KAFKA` | topic `dwd`; key `{station_id}` |

#### Message `DE.DWD.CDC.Precipitation10Min`
<a id="message-dedwdcdcprecipitation10min"></a>

| Field | Value |
| --- | --- |
| Name | Precipitation10Min |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.CDC.Precipitation10Min`](#schema-dedwdcdcprecipitation10min) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.CDC.Precipitation10Min` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.CDC.Kafka` | `KAFKA` | topic `dwd`; key `{station_id}` |

#### Message `DE.DWD.CDC.Wind10Min`
<a id="message-dedwdcdcwind10min"></a>

| Field | Value |
| --- | --- |
| Name | Wind10Min |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.CDC.Wind10Min`](#schema-dedwdcdcwind10min) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.CDC.Wind10Min` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.CDC.Kafka` | `KAFKA` | topic `dwd`; key `{station_id}` |

#### Message `DE.DWD.CDC.Solar10Min`
<a id="message-dedwdcdcsolar10min"></a>

| Field | Value |
| --- | --- |
| Name | Solar10Min |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.CDC.Solar10Min`](#schema-dedwdcdcsolar10min) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.CDC.Solar10Min` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.CDC.Kafka` | `KAFKA` | topic `dwd`; key `{station_id}` |

#### Message `DE.DWD.CDC.HourlyObservation`
<a id="message-dedwdcdchourlyobservation"></a>

| Field | Value |
| --- | --- |
| Name | HourlyObservation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.CDC.HourlyObservation`](#schema-dedwdcdchourlyobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.CDC.HourlyObservation` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.CDC.Kafka` | `KAFKA` | topic `dwd`; key `{station_id}` |

#### Message `DE.DWD.CDC.ExtremeWind10Min`
<a id="message-dedwdcdcextremewind10min"></a>

| Field | Value |
| --- | --- |
| Name | ExtremeWind10Min |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.CDC.ExtremeWind10Min`](#schema-dedwdcdcextremewind10min) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.CDC.ExtremeWind10Min` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.CDC.Kafka` | `KAFKA` | topic `dwd`; key `{station_id}` |

#### Message `DE.DWD.CDC.ExtremeTemperature10Min`
<a id="message-dedwdcdcextremetemperature10min"></a>

| Field | Value |
| --- | --- |
| Name | ExtremeTemperature10Min |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.CDC.ExtremeTemperature10Min`](#schema-dedwdcdcextremetemperature10min) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.CDC.ExtremeTemperature10Min` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.CDC.Kafka` | `KAFKA` | topic `dwd`; key `{station_id}` |

### Messagegroup `DE.DWD.Weather`
<a id="messagegroup-dedwdweather"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `DE.DWD.Weather.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `DE.DWD.Weather.Alert`
<a id="message-dedwdweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | Alert |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.CDC.jstruct/schemas/DE.DWD.Weather.Alert`](#schema-dedwdweatheralert) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.Weather.Alert` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de` |
| `subject` |  | `uritemplate` | `False` | `{identifier}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.Weather.Kafka` | `KAFKA` | topic `dwd`; key `{identifier}` |

### Messagegroup `DE.DWD.Radar`
<a id="messagegroup-dedwdradar"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `DE.DWD.Radar.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `DE.DWD.Radar.RadarProductCatalog`
<a id="message-dedwdradarradarproductcatalog"></a>

| Field | Value |
| --- | --- |
| Name | RadarProductCatalog |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.Radar.jstruct/schemas/DE.DWD.Radar.RadarProductCatalog`](#schema-dedwdradarradarproductcatalog) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.Radar.RadarProductCatalog` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de/weather/radar` |
| `subject` |  | `uritemplate` | `False` | `{file_url}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.Radar.Kafka` | `KAFKA` | topic `dwd`; key `{file_url}` |

#### Message `DE.DWD.Radar.RadarFileProduct`
<a id="message-dedwdradarradarfileproduct"></a>

| Field | Value |
| --- | --- |
| Name | RadarFileProduct |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.Radar.jstruct/schemas/DE.DWD.Radar.RadarFileProduct`](#schema-dedwdradarradarfileproduct) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.Radar.RadarFileProduct` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de/weather/radar` |
| `subject` |  | `uritemplate` | `False` | `{file_url}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.Radar.Kafka` | `KAFKA` | topic `dwd`; key `{file_url}` |

### Messagegroup `DE.DWD.Forecast`
<a id="messagegroup-dedwdforecast"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `DE.DWD.Forecast.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `DE.DWD.Forecast.ForecastModelCatalog`
<a id="message-dedwdforecastforecastmodelcatalog"></a>

| Field | Value |
| --- | --- |
| Name | ForecastModelCatalog |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.Forecast.jstruct/schemas/DE.DWD.Forecast.ForecastModelCatalog`](#schema-dedwdforecastforecastmodelcatalog) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.Forecast.ForecastModelCatalog` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de/weather/nwp/icon-d2` |
| `subject` |  | `uritemplate` | `False` | `{file_url}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.Forecast.Kafka` | `KAFKA` | topic `dwd`; key `{file_url}` |

#### Message `DE.DWD.Forecast.IconD2ForecastFile`
<a id="message-dedwdforecasticond2forecastfile"></a>

| Field | Value |
| --- | --- |
| Name | IconD2ForecastFile |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/DE.DWD.Forecast.jstruct/schemas/DE.DWD.Forecast.IconD2ForecastFile`](#schema-dedwdforecasticond2forecastfile) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `DE.DWD.Forecast.IconD2ForecastFile` |
| `source` |  | `string` | `False` | `https://opendata.dwd.de/weather/nwp/icon-d2` |
| `subject` |  | `uritemplate` | `False` | `{file_url}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `DE.DWD.Forecast.Kafka` | `KAFKA` | topic `dwd`; key `{file_url}` |

## Schemagroups

### Schemagroup `DE.DWD.CDC.jstruct`
<a id="schemagroup-dedwdcdcjstruct"></a>

#### Schema `DE.DWD.CDC.StationMetadata`
<a id="schema-dedwdcdcstationmetadata"></a>

| Field | Value |
| --- | --- |
| Name | StationMetadata |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/StationMetadata` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `StationMetadata`
<a id="schema-node-stationmetadata"></a>

StationMetadata

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/StationMetadata` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:de": "STATIONS_ID"}` | - | - |
| `station_name` | `string` | `True` |  | - | - | - |
| `latitude` | `double` | `True` |  | - | - | - |
| `longitude` | `double` | `True` |  | - | - | - |
| `elevation` | `double` | `True` |  | - | - | - |
| `state` | `string` | `False` |  | - | - | - |
| `from_date` | `string` | `False` |  | - | - | - |
| `to_date` | `string` | `False` |  | - | - | - |

#### Schema `DE.DWD.CDC.AirTemperature10Min`
<a id="schema-dedwdcdcairtemperature10min"></a>

| Field | Value |
| --- | --- |
| Name | AirTemperature10Min |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/AirTemperature10Min` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AirTemperature10Min`
<a id="schema-node-airtemperature10min"></a>

AirTemperature10Min

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/AirTemperature10Min` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:de": "STATIONS_ID"}` | - | - |
| `timestamp` | `string` | `True` |  | altnames=`{"lang:de": "MESS_DATUM"}` | - | - |
| `quality_level` | `int32` | `False` |  | altnames=`{"lang:de": "QN"}` | - | - |
| `pressure_station_level` | `double` | `False` |  | altnames=`{"lang:de": "PP_10"}` | - | - |
| `air_temperature_2m` | `double` | `False` |  | altnames=`{"lang:de": "TT_10"}` | - | - |
| `air_temperature_5cm` | `double` | `False` |  | altnames=`{"lang:de": "TM5_10"}` | - | - |
| `relative_humidity` | `double` | `False` |  | altnames=`{"lang:de": "RF_10"}` | - | - |
| `dew_point_temperature` | `double` | `False` |  | altnames=`{"lang:de": "TD_10"}` | - | - |

#### Schema `DE.DWD.CDC.Precipitation10Min`
<a id="schema-dedwdcdcprecipitation10min"></a>

| Field | Value |
| --- | --- |
| Name | Precipitation10Min |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/Precipitation10Min` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Precipitation10Min`
<a id="schema-node-precipitation10min"></a>

Precipitation10Min

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/Precipitation10Min` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:de": "STATIONS_ID"}` | - | - |
| `timestamp` | `string` | `True` |  | altnames=`{"lang:de": "MESS_DATUM"}` | - | - |
| `quality_level` | `int32` | `False` |  | altnames=`{"lang:de": "QN"}` | - | - |
| `precipitation_height` | `double` | `False` |  | altnames=`{"lang:de": "RWS_10"}` | - | - |
| `precipitation_indicator` | `int32` | `False` |  | altnames=`{"lang:de": "RWS_IND_10"}` | - | - |

#### Schema `DE.DWD.CDC.Wind10Min`
<a id="schema-dedwdcdcwind10min"></a>

| Field | Value |
| --- | --- |
| Name | Wind10Min |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/Wind10Min` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Wind10Min`
<a id="schema-node-wind10min"></a>

Wind10Min

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/Wind10Min` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:de": "STATIONS_ID"}` | - | - |
| `timestamp` | `string` | `True` |  | altnames=`{"lang:de": "MESS_DATUM"}` | - | - |
| `quality_level` | `int32` | `False` |  | altnames=`{"lang:de": "QN"}` | - | - |
| `wind_speed` | `double` | `False` |  | altnames=`{"lang:de": "FF_10"}` | - | - |
| `wind_direction` | `double` | `False` |  | altnames=`{"lang:de": "DD_10"}` | - | - |

#### Schema `DE.DWD.CDC.Solar10Min`
<a id="schema-dedwdcdcsolar10min"></a>

| Field | Value |
| --- | --- |
| Name | Solar10Min |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/Solar10Min` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Solar10Min`
<a id="schema-node-solar10min"></a>

Solar10Min

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/Solar10Min` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:de": "STATIONS_ID"}` | - | - |
| `timestamp` | `string` | `True` |  | altnames=`{"lang:de": "MESS_DATUM"}` | - | - |
| `quality_level` | `int32` | `False` |  | altnames=`{"lang:de": "QN"}` | - | - |
| `global_radiation` | `double` | `False` |  | altnames=`{"lang:de": "GS_10"}` | - | - |
| `sunshine_duration` | `double` | `False` |  | altnames=`{"lang:de": "SD_10"}` | - | - |
| `diffuse_radiation` | `double` | `False` |  | altnames=`{"lang:de": "DS_10"}` | - | - |
| `longwave_radiation` | `double` | `False` |  | altnames=`{"lang:de": "LS_10"}` | - | - |

#### Schema `DE.DWD.CDC.HourlyObservation`
<a id="schema-dedwdcdchourlyobservation"></a>

| Field | Value |
| --- | --- |
| Name | HourlyObservation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/HourlyObservation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `HourlyObservation`
<a id="schema-node-hourlyobservation"></a>

HourlyObservation

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/HourlyObservation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:de": "STATIONS_ID"}` | - | - |
| `timestamp` | `string` | `True` |  | altnames=`{"lang:de": "MESS_DATUM"}` | - | - |
| `quality_level` | `int32` | `False` |  | altnames=`{"lang:de": "QN"}` | - | - |
| `parameter` | `string` | `True` |  | - | - | - |
| `value` | `double` | `False` |  | - | - | - |
| `unit` | `string` | `False` |  | - | - | - |

#### Schema `DE.DWD.Weather.Alert`
<a id="schema-dedwdweatheralert"></a>

| Field | Value |
| --- | --- |
| Name | Alert |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/DE/DWD/Weather.schema.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Alert`
<a id="schema-node-alert"></a>

Alert

| Field | Value |
| --- | --- |
| $id | `https://example.com/DE/DWD/Weather.schema.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `identifier` | `string` | `True` |  | - | - | - |
| `sender` | `string` | `True` |  | - | - | - |
| `sent` | `string` | `True` |  | - | - | - |
| `status` | `string` | `False` |  | - | - | - |
| `msg_type` | `string` | `False` |  | - | - | - |
| `severity` | `string` | `True` |  | - | - | - |
| `urgency` | `string` | `False` |  | - | - | - |
| `certainty` | `string` | `False` |  | - | - | - |
| `event` | `string` | `True` |  | - | - | - |
| `headline` | `string` | `False` |  | - | - | - |
| `description` | `string` | `False` |  | - | - | - |
| `effective` | `string` | `False` |  | - | - | - |
| `onset` | `string` | `False` |  | - | - | - |
| `expires` | `string` | `False` |  | - | - | - |
| `area_desc` | `string` | `False` |  | - | - | - |
| `geocodes` | `string` | `False` |  | - | - | - |

#### Schema `DE.DWD.CDC.ExtremeWind10Min`
<a id="schema-dedwdcdcextremewind10min"></a>

| Field | Value |
| --- | --- |
| Name | ExtremeWind10Min |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/ExtremeWind10Min` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ExtremeWind10Min`
<a id="schema-node-extremewind10min"></a>

ExtremeWind10Min

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/ExtremeWind10Min` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:de": "STATIONS_ID"}` | - | - |
| `timestamp` | `string` | `True` |  | altnames=`{"lang:de": "MESS_DATUM"}` | - | - |
| `quality_level` | `int32` | `False` |  | altnames=`{"lang:de": "QN"}` | - | - |
| `wind_speed_maximum` | `double` | `False` |  | altnames=`{"lang:de": "FX_10"}` | - | - |
| `wind_speed_minimum` | `double` | `False` |  | altnames=`{"lang:de": "FNX_10"}` | - | - |
| `wind_direction_at_maximum` | `double` | `False` |  | altnames=`{"lang:de": "DX_10"}` | - | - |

#### Schema `DE.DWD.CDC.ExtremeTemperature10Min`
<a id="schema-dedwdcdcextremetemperature10min"></a>

| Field | Value |
| --- | --- |
| Name | ExtremeTemperature10Min |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/ExtremeTemperature10Min` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ExtremeTemperature10Min`
<a id="schema-node-extremetemperature10min"></a>

ExtremeTemperature10Min

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/DE/DWD/CDC/ExtremeTemperature10Min` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` |  | altnames=`{"lang:de": "STATIONS_ID"}` | - | - |
| `timestamp` | `string` | `True` |  | altnames=`{"lang:de": "MESS_DATUM"}` | - | - |
| `quality_level` | `int32` | `False` |  | altnames=`{"lang:de": "QN"}` | - | - |
| `air_temperature_maximum_2m` | `double` | `False` |  | altnames=`{"lang:de": "TX_10"}` | - | - |
| `air_temperature_minimum_5cm` | `double` | `False` |  | altnames=`{"lang:de": "TN_10"}` | - | - |

### Schemagroup `DE.DWD.Radar.jstruct`
<a id="schemagroup-dedwdradarjstruct"></a>

#### Schema `DE.DWD.Radar.RadarProductCatalog`
<a id="schema-dedwdradarradarproductcatalog"></a>

| Field | Value |
| --- | --- |
| Name | RadarProductCatalog |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Radar/RadarProductCatalog` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `RadarProductCatalog`
<a id="schema-node-radarproductcatalog"></a>

Reference (catalog) event describing a single DWD radar composite product family. One event is emitted per product directory the first time the bridge observes it, so consumers can build a catalog of available products and the URLs from which their files can be discovered.

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Radar/RadarProductCatalog` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `product` | `string` | `True` | Short identifier of the DWD radar composite product family (for example 'wn', 'rv', 'rs', 'dmax', 'hg', 'hx', 'pg', 'vii', 'hymecng'). Derived from the first-level directory name under https://opendata.dwd.de/weather/radar/composite/. All RadarFileProduct events for files inside this directory carry the same product value. | - | - | - |
| `file_url` | `string` | `True` | Absolute HTTPS URL of the DWD Open Data directory that holds all files for this radar product. The URL is publicly fetchable with an unauthenticated HTTP GET and returns an Apache autoindex HTML listing, so consumers can enumerate current and historical product files without credentials. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key for catalog events. Example: 'https://opendata.dwd.de/weather/radar/composite/wn/'. | - | - | - |
| `description` | `string` | `False` | Optional human-readable description of the radar product as configured by the bridge. Intended for catalog browsers, documentation, and operator UIs; not derived from upstream metadata. | - | - | - |

#### Schema `DE.DWD.Radar.RadarFileProduct`
<a id="schema-dedwdradarradarfileproduct"></a>

| Field | Value |
| --- | --- |
| Name | RadarFileProduct |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Radar/RadarFileProduct` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `RadarFileProduct`
<a id="schema-node-radarfileproduct"></a>

Telemetry-style event announcing that a single DWD radar composite product file has appeared or been updated on the Open Data server. The event carries enough metadata to fetch the file directly via an unauthenticated HTTPS GET against file_url; it does not embed the file payload.

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Radar/RadarFileProduct` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `file_url` | `string` | `True` | Absolute HTTPS URL of a single DWD radar product file on the DWD Open Data server. The URL is publicly fetchable with an unauthenticated HTTP GET and supports HTTP Range and If-Modified-Since/ETag conditional requests, so handlers can dereference the event by performing a plain GET against this URL. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key, which guarantees per-file ordering. Example: 'https://opendata.dwd.de/weather/radar/composite/wn/composite_wn_20260517_2005-hd5'. | - | - | - |
| `product` | `string` | `True` | Short identifier of the radar product family this file belongs to (for example 'wn', 'rv', 'dmax'); matches the 'product' field of the corresponding RadarProductCatalog event. | - | - | - |
| `file_name` | `string` | `True` | Bare file name (no directory component) as listed in the DWD Apache directory index. Convenient for parsing the embedded product code and observation timestamp without having to split file_url. | - | - | - |
| `modified` | `string` | `True` | Upstream Last-Modified timestamp of the file as reported by the DWD Apache directory listing, expressed as an ISO 8601 UTC string. The bridge emits a new RadarFileProduct event whenever this value changes for a known file_url, so consumers can use it for change detection and de-duplication. | - | - | - |
| `size_bytes` | `union` | `False` | File size in bytes as parsed from the DWD directory listing, or null when the listing does not expose a size. Indicative only; for an authoritative size consumers should rely on the Content-Length header returned by the actual GET on file_url. Radar composite files typically range from tens of KB (BUFR products) up to roughly 10 MB (large HDF5 composites). | - | - | - |

### Schemagroup `DE.DWD.Forecast.jstruct`
<a id="schemagroup-dedwdforecastjstruct"></a>

#### Schema `DE.DWD.Forecast.ForecastModelCatalog`
<a id="schema-dedwdforecastforecastmodelcatalog"></a>

| Field | Value |
| --- | --- |
| Name | ForecastModelCatalog |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Forecast/ForecastModelCatalog` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ForecastModelCatalog`
<a id="schema-node-forecastmodelcatalog"></a>

Reference (catalog) event describing a single NWP forecast model family published by DWD Open Data. One event is emitted per model the first time the bridge observes it, so consumers can build a catalog of available models and the URLs from which their forecast files can be discovered.

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Forecast/ForecastModelCatalog` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `model` | `string` | `True` | Identifier of the numerical weather prediction (NWP) model. For this bridge release the value is 'icon-d2', referring to the DWD ICON-D2 convection-permitting regional model covering Germany and surrounding areas with ~2 km horizontal resolution and forecast lead times up to 48 hours. | - | - | - |
| `file_url` | `string` | `True` | Absolute HTTPS URL of the DWD Open Data root directory under which all GRIB2 files for this forecast model are published. The URL is publicly fetchable with an unauthenticated HTTP GET and returns an Apache autoindex HTML listing. Run-hour subdirectories (e.g. '00/', '03/', '06/', ...) and per-variable subdirectories live below this URL. Also used verbatim as the CloudEvents 'subject' and the Kafka partition key for catalog events. Example: 'https://opendata.dwd.de/weather/nwp/icon-d2/grib/'. | - | - | - |
| `description` | `string` | `False` | Optional human-readable description of the forecast model emitted as reference data. Intended for catalog browsers, documentation, and operator UIs; not derived from upstream metadata. | - | - | - |

#### Schema `DE.DWD.Forecast.IconD2ForecastFile`
<a id="schema-dedwdforecasticond2forecastfile"></a>

| Field | Value |
| --- | --- |
| Name | IconD2ForecastFile |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Forecast/IconD2ForecastFile` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `IconD2ForecastFile`
<a id="schema-node-icond2forecastfile"></a>

Telemetry-style event announcing that a single ICON-D2 GRIB2 forecast file has appeared or been updated on the DWD Open Data server. The event carries enough metadata to fetch the file directly via an unauthenticated HTTPS GET against file_url; it does not embed the file payload.

| Field | Value |
| --- | --- |
| $id | `https://opendata.dwd.de/schemas/DE/DWD/Forecast/IconD2ForecastFile` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `file_url` | `string` | `True` | Absolute HTTPS URL of a single ICON-D2 GRIB2 forecast file on the DWD Open Data server. The file is bzip2-compressed GRIB2 (.grib2.bz2) and can be fetched with an unauthenticated HTTP GET; the server supports HTTP Range and If-Modified-Since/ETag conditional requests, so handlers can dereference the event with a plain GET against this URL. Each file holds a single variable at a single vertical level for a single forecast lead hour, which keeps per-file payloads small (typically a few hundred KB compressed). Also used verbatim as the CloudEvents 'subject' and the Kafka partition key. Example: 'https://opendata.dwd.de/weather/nwp/icon-d2/grib/00/t/icon-d2_germany_icosahedral_model-level_2026051700_003_10_t.grib2.bz2'. | - | - | - |
| `model` | `string` | `True` | Identifier of the source forecast model; matches the 'model' field of the corresponding ForecastModelCatalog event. Currently always 'icon-d2'. | - | - | - |
| `file_name` | `string` | `True` | Bare file name as listed in the DWD Apache directory index, following the DWD convention 'icon-d2_<grid>_<level_type>_<run>_<lead>_<level>_<parameter>.grib2.bz2'. Convenient for parsing without splitting file_url. | - | - | - |
| `run` | `union` | `False` | Model run cycle in 'YYYYMMDDHH' UTC form, parsed from file_name (e.g. '2026051700' for the 00 UTC run on 2026-05-17). ICON-D2 is run every three hours. Null when the file name does not match the expected pattern (for example time-invariant or auxiliary files). | - | - | - |
| `forecast_hour` | `union` | `False` | Forecast lead time in whole hours from the start of the run, parsed from file_name. For ICON-D2 this ranges from 0 to 48. Null when the file name does not match the expected pattern. | - | - | - |
| `parameter` | `union` | `False` | Short ICON-D2 parameter identifier parsed from file_name (for example 't' for temperature, 'u'/'v' for wind components, 'tot_prec' for total precipitation, 'clct' for total cloud cover, 'alb_rad' for shortwave albedo). | - | - | - |
| `level_type` | `union` | `False` | Vertical level encoding parsed from file_name. Common values are 'single-level' (surface and 2D fields), 'model-level' (native ICON hybrid levels indexed 1..65 from top to bottom), 'pressure-level' (interpolated to fixed pressure surfaces, in hPa), and 'time-invariant' (constant fields such as orography). | - | - | - |
| `level` | `union` | `False` | Vertical level value token parsed from file_name. The interpretation depends on level_type: model-level uses an integer level index, pressure-level uses pressure in hPa, single-level may carry a short surface tag or be omitted. | - | - | - |
| `modified` | `string` | `True` | Upstream Last-Modified timestamp from the DWD Apache directory listing, expressed as an ISO 8601 UTC string. The bridge emits a new IconD2ForecastFile event whenever this value changes for a known file_url, enabling change detection and de-duplication. | - | - | - |
| `size_bytes` | `union` | `False` | File size in bytes as parsed from the DWD directory listing, or null when the listing does not expose a size. Indicative only; for an authoritative size rely on the Content-Length header from the actual GET on file_url. Individual ICON-D2 .grib2.bz2 files are typically well below 1 MB compressed. | - | - | - |
