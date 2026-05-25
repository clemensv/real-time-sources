# NOAA Data Poller Usage Guide Events

**NOAA Data Poller** is a tool designed to interact with the NOAA (National Oceanic and Atmospheric Administration) API to fetch real-time environmental data from various NOAA stations. The tool can retrieve data such as water levels, air temperature, wind, and predictions, and send this data to a Kafka topic using SASL PLAIN authentication, making it suitable for integration with systems like Microsoft Event Hubs or Microsoft Fabric Event Streams.

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

### Endpoint `Microsoft.OpenData.US.NOAA.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.US.NOAA`](#messagegroup-microsoftopendatausnoaa) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `noaa-tides-currents` |
| Kafka key | `{station_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Microsoft.OpenData.US.NOAA`
<a id="messagegroup-microsoftopendatausnoaa"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.US.NOAA.Kafka` (KAFKA) |
| Messages | 13 |

#### Message `Microsoft.OpenData.US.NOAA.WaterLevel`
<a id="message-microsoftopendatausnoaawaterlevel"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevel |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.WaterLevel`](#schema-microsoftopendatausnoaawaterlevel) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.WaterLevel` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.Predictions`
<a id="message-microsoftopendatausnoaapredictions"></a>

| Field | Value |
| --- | --- |
| Name | Predictions |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Predictions`](#schema-microsoftopendatausnoaapredictions) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.Predictions` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.AirPressure`
<a id="message-microsoftopendatausnoaaairpressure"></a>

| Field | Value |
| --- | --- |
| Name | AirPressure |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.AirPressure`](#schema-microsoftopendatausnoaaairpressure) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.AirPressure` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.AirTemperature`
<a id="message-microsoftopendatausnoaaairtemperature"></a>

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.AirTemperature`](#schema-microsoftopendatausnoaaairtemperature) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.AirTemperature` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.WaterTemperature`
<a id="message-microsoftopendatausnoaawatertemperature"></a>

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.WaterTemperature`](#schema-microsoftopendatausnoaawatertemperature) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.WaterTemperature` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.Wind`
<a id="message-microsoftopendatausnoaawind"></a>

| Field | Value |
| --- | --- |
| Name | Wind |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Wind`](#schema-microsoftopendatausnoaawind) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.Wind` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.Humidity`
<a id="message-microsoftopendatausnoaahumidity"></a>

| Field | Value |
| --- | --- |
| Name | Humidity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Humidity`](#schema-microsoftopendatausnoaahumidity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.Humidity` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.Conductivity`
<a id="message-microsoftopendatausnoaaconductivity"></a>

| Field | Value |
| --- | --- |
| Name | Conductivity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Conductivity`](#schema-microsoftopendatausnoaaconductivity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.Conductivity` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.Salinity`
<a id="message-microsoftopendatausnoaasalinity"></a>

| Field | Value |
| --- | --- |
| Name | Salinity |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Salinity`](#schema-microsoftopendatausnoaasalinity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.Salinity` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.Station`
<a id="message-microsoftopendatausnoaastation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Station`](#schema-microsoftopendatausnoaastation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.Station` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.Visibility`
<a id="message-microsoftopendatausnoaavisibility"></a>

| Field | Value |
| --- | --- |
| Name | Visibility |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Visibility`](#schema-microsoftopendatausnoaavisibility) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.Visibility` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `datacontenttype` |  | `string` | `True` | `-` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |
| `time` |  | `string` | `True` | `-` |
| `dataschema` |  | `string` | `True` | `-` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.Currents`
<a id="message-microsoftopendatausnoaacurrents"></a>

| Field | Value |
| --- | --- |
| Name | Currents |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.Currents`](#schema-microsoftopendatausnoaacurrents) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.Currents` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

#### Message `Microsoft.OpenData.US.NOAA.CurrentPredictions`
<a id="message-microsoftopendatausnoaacurrentpredictions"></a>

| Field | Value |
| --- | --- |
| Name | CurrentPredictions |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.US.NOAA.jstruct/schemas/Microsoft.OpenData.US.NOAA.CurrentPredictions`](#schema-microsoftopendatausnoaacurrentpredictions) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.US.NOAA.CurrentPredictions` |
| `source` |  | `string` | `False` | `https://api.tidesandcurrents.noaa.gov` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.US.NOAA.Kafka` | `KAFKA` | topic `noaa-tides-currents`; key `{station_id}` |

## Schemagroups

### Schemagroup `Microsoft.OpenData.US.NOAA.jstruct`
<a id="schemagroup-microsoftopendatausnoaajstruct"></a>

#### Schema `Microsoft.OpenData.US.NOAA.WaterLevel`
<a id="schema-microsoftopendatausnoaawaterlevel"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevel |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/WaterLevel` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/WaterLevel` |
| Type | `object` |

###### Object `WaterLevel`
<a id="schema-node-waterlevel"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the water level measurement"} | - | - | - |
| `value` | `double` | `True` | {"description": "Value of the water level"} | - | - | - |
| `stddev` | `double` | `True` | {"description": "Standard deviation of 1-second samples used to compute the water level height"} | - | - | - |
| `outside_sigma_band` | `boolean` | `True` | {"description": "Flag indicating if the water level is outside a 3-sigma band. Possible values: 'false' (not outside), 'true' (outside)."} | - | - | - |
| `flat_tolerance_limit` | `boolean` | `True` | {"description": "Flag indicating if the flat tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} | - | - | - |
| `rate_of_change_limit` | `boolean` | `True` | {"description": "Flag indicating if the rate of change tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} | - | - | - |
| `max_min_expected_height` | `boolean` | `True` | {"description": "Flag indicating if the max/min expected water level height is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} | - | - | - |
| `quality` | `schema` | `True` |  | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.Predictions`
<a id="schema-microsoftopendatausnoaapredictions"></a>

| Field | Value |
| --- | --- |
| Name | Predictions |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/Predictions` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/Predictions` |
| Type | `object` |

###### Object `Predictions`
<a id="schema-node-predictions"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the prediction"} | - | - | - |
| `value` | `double` | `True` | {"description": "Value of the prediction"} | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.AirPressure`
<a id="schema-microsoftopendatausnoaaairpressure"></a>

| Field | Value |
| --- | --- |
| Name | AirPressure |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/AirPressure` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/AirPressure` |
| Type | `object` |

###### Object `AirPressure`
<a id="schema-node-airpressure"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the air pressure measurement"} | - | - | - |
| `value` | `double` | `True` | {"description": "Value of the air pressure"} | - | - | - |
| `max_pressure_exceeded` | `boolean` | `True` | Flag indicating if the maximum expected air pressure was exceeded | - | - | - |
| `min_pressure_exceeded` | `boolean` | `True` | Flag indicating if the minimum expected air pressure was exceeded | - | - | - |
| `rate_of_change_exceeded` | `boolean` | `True` | Flag indicating if the rate of change tolerance limit was exceeded | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.AirTemperature`
<a id="schema-microsoftopendatausnoaaairtemperature"></a>

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/AirTemperature` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/AirTemperature` |
| Type | `object` |

###### Object `AirTemperature`
<a id="schema-node-airtemperature"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the air temperature measurement"} | - | - | - |
| `value` | `double` | `True` | {"description": "Value of the air temperature"} | - | - | - |
| `max_temp_exceeded` | `boolean` | `True` | Flag indicating if the maximum expected air temperature was exceeded | - | - | - |
| `min_temp_exceeded` | `boolean` | `True` | Flag indicating if the minimum expected air temperature was exceeded | - | - | - |
| `rate_of_change_exceeded` | `boolean` | `True` | Flag indicating if the rate of change tolerance limit was exceeded | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.WaterTemperature`
<a id="schema-microsoftopendatausnoaawatertemperature"></a>

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/WaterTemperature` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/WaterTemperature` |
| Type | `object` |

###### Object `WaterTemperature`
<a id="schema-node-watertemperature"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the water temperature measurement"} | - | - | - |
| `value` | `double` | `True` | {"description": "Value of the water temperature"} | - | - | - |
| `max_temp_exceeded` | `boolean` | `True` | Flag indicating if the maximum expected water temperature was exceeded | - | - | - |
| `min_temp_exceeded` | `boolean` | `True` | Flag indicating if the minimum expected water temperature was exceeded | - | - | - |
| `rate_of_change_exceeded` | `boolean` | `True` | Flag indicating if the rate of change tolerance limit was exceeded | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.Wind`
<a id="schema-microsoftopendatausnoaawind"></a>

| Field | Value |
| --- | --- |
| Name | Wind |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/Wind` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/Wind` |
| Type | `object` |

###### Object `Wind`
<a id="schema-node-wind"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the wind measurement"} | - | - | - |
| `speed` | `double` | `True` | {"description": "Wind speed"} | - | - | - |
| `direction_degrees` | `string` | `True` | {"description": "Wind direction"} | - | - | - |
| `direction_text` | `string` | `True` | {"description": "Direction - wind direction in text."} | - | - | - |
| `gusts` | `double` | `True` | {"description": "Wind gust speed"} | - | - | - |
| `max_wind_speed_exceeded` | `boolean` | `True` | Flag indicating if the maximum wind speed was exceeded | - | - | - |
| `rate_of_change_exceeded` | `boolean` | `True` | Flag indicating if the rate of change tolerance limit was exceeded | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.Humidity`
<a id="schema-microsoftopendatausnoaahumidity"></a>

| Field | Value |
| --- | --- |
| Name | Humidity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/Humidity` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/Humidity` |
| Type | `object` |

###### Object `Humidity`
<a id="schema-node-humidity"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the humidity measurement"} | - | - | - |
| `value` | `double` | `True` | {"description": "Value of the humidity"} | - | - | - |
| `max_humidity_exceeded` | `boolean` | `True` | Flag indicating if the maximum expected humidity was exceeded | - | - | - |
| `min_humidity_exceeded` | `boolean` | `True` | Flag indicating if the minimum expected humidity was exceeded | - | - | - |
| `rate_of_change_exceeded` | `boolean` | `True` | Flag indicating if the rate of change tolerance limit was exceeded | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.Conductivity`
<a id="schema-microsoftopendatausnoaaconductivity"></a>

| Field | Value |
| --- | --- |
| Name | Conductivity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/Conductivity` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/Conductivity` |
| Type | `object` |

###### Object `Conductivity`
<a id="schema-node-conductivity"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the conductivity measurement"} | - | - | - |
| `value` | `double` | `True` | {"description": "Value of the conductivity"} | - | - | - |
| `max_conductivity_exceeded` | `boolean` | `True` | Flag indicating if the maximum expected conductivity was exceeded | - | - | - |
| `min_conductivity_exceeded` | `boolean` | `True` | Flag indicating if the minimum expected conductivity was exceeded | - | - | - |
| `rate_of_change_exceeded` | `boolean` | `True` | Flag indicating if the rate of change tolerance limit was exceeded | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.Salinity`
<a id="schema-microsoftopendatausnoaasalinity"></a>

| Field | Value |
| --- | --- |
| Name | Salinity |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/Salinity` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/Salinity` |
| Type | `object` |

###### Object `Salinity`
<a id="schema-node-salinity"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the salinity measurement"} | - | - | - |
| `salinity` | `double` | `True` | {"description": "Value of the salinity"} | - | - | - |
| `grams_per_kg` | `double` | `True` | {"description": "Grams of salt per kilogram of water"} | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.Station`
<a id="schema-microsoftopendatausnoaastation"></a>

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
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/Station` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `tidal` | `boolean` | `True` | {"description": "Indicates whether the station measures tidal data."} | - | - | - |
| `greatlakes` | `boolean` | `True` | {"description": "Indicates whether the station is located in the Great Lakes region."} | - | - | - |
| `shefcode` | `string` | `True` | {"description": "Standard Hydrologic Exchange Format code for the station."} | - | - | - |
| `details` | `schema` | `True` |  | - | - | - |
| `sensors` | `schema` | `True` |  | - | - | - |
| `floodlevels` | `schema` | `True` |  | - | - | - |
| `datums` | `schema` | `True` |  | - | - | - |
| `supersededdatums` | `schema` | `True` |  | - | - | - |
| `harmonicConstituents` | `schema` | `True` |  | - | - | - |
| `benchmarks` | `schema` | `True` |  | - | - | - |
| `tidePredOffsets` | `schema` | `True` |  | - | - | - |
| `ofsMapOffsets` | `schema` | `True` |  | - | - | - |
| `state` | `string` | `True` | {"description": "State where the station is located."} | - | - | - |
| `timezone` | `string` | `True` | {"description": "Timezone of the station."} | - | - | - |
| `timezonecorr` | `int32` | `True` | {"description": "Timezone correction in minutes for the station."} | - | - | - |
| `observedst` | `boolean` | `True` | {"description": "Indicates whether the station observes Daylight Saving Time."} | - | - | - |
| `stormsurge` | `boolean` | `True` | {"description": "Indicates whether the station measures storm surge data."} | - | - | - |
| `nearby` | `schema` | `True` |  | - | - | - |
| `forecast` | `boolean` | `True` | {"description": "Indicates whether the station provides forecast data."} | - | - | - |
| `outlook` | `boolean` | `True` | {"description": "Indicates whether the station provides outlook data."} | - | - | - |
| `HTFhistorical` | `boolean` | `True` | {"description": "Indicates whether the station has historical High Tide Flooding data."} | - | - | - |
| `nonNavigational` | `boolean` | `True` | {"description": "Indicates whether the station is non-navigational."} | - | - | - |
| `station_id` | `string` | `True` | {"description": "Unique identifier for the station."} | - | - | - |
| `name` | `string` | `True` | {"description": "Name of the station."} | - | - | - |
| `lat` | `double` | `True` | {"description": "Latitude of the station."} | - | - | - |
| `lng` | `double` | `True` | {"description": "Longitude of the station."} | - | - | - |
| `affiliations` | `string` | `True` | {"description": "Affiliations of the station."} | - | - | - |
| `portscode` | `string` | `True` | {"description": "PORTS code for the station."} | - | - | - |
| `products` | `schema` | `True` |  | - | - | - |
| `disclaimers` | `schema` | `True` |  | - | - | - |
| `notices` | `schema` | `True` |  | - | - | - |
| `self` | `string` | `True` | {"description": "URL to the station's data."} | - | - | - |
| `expand` | `string` | `True` | {"description": "URL to expanded information about the station."} | - | - | - |
| `tideType` | `string` | `True` | {"description": "Type of tide measured by the station."} | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.Visibility`
<a id="schema-microsoftopendatausnoaavisibility"></a>

| Field | Value |
| --- | --- |
| Name | Visibility |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/Visibility` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/Visibility` |
| Type | `object` |

###### Object `Visibility`
<a id="schema-node-visibility"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the visibility measurement"} | - | - | - |
| `value` | `double` | `True` | {"description": "Value of the visibility"} | - | - | - |
| `max_visibility_exceeded` | `boolean` | `True` | A flag that indicates whether the maximum expected visibility was exceeded | - | - | - |
| `min_visibility_exceeded` | `boolean` | `True` | A flag that indicates whether the minimum expected visibility was exceeded | - | - | - |
| `rate_of_change_exceeded` | `boolean` | `True` | A flag that indicates whether the rate of change tolerance limit was exceeded | - | - | - |
| `station_id` | `string` | `True` |  | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.Currents`
<a id="schema-microsoftopendatausnoaacurrents"></a>

| Field | Value |
| --- | --- |
| Name | Currents |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/Currents` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/Currents` |
| Type | `object` |

###### Object `Currents`
<a id="schema-node-currents"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the currents measurement"} | - | - | - |
| `speed` | `double` | `True` | {"description": "Current speed"} | - | - | - |
| `direction_degrees` | `double` | `True` | {"description": "Current direction in degrees"} | - | - | - |
| `bin` | `string` | `True` | {"description": "Bin number"} | - | - | - |

#### Schema `Microsoft.OpenData.US.NOAA.CurrentPredictions`
<a id="schema-microsoftopendatausnoaacurrentpredictions"></a>

| Field | Value |
| --- | --- |
| Name | CurrentPredictions |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/US/NOAA/CurrentPredictions` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/US/NOAA/CurrentPredictions` |
| Type | `object` |

###### Object `CurrentPredictions`
<a id="schema-node-currentpredictions"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | {"description": "7 character station ID, or a currents station ID."} | - | - | - |
| `timestamp` | `string` | `True` | {"description": "Timestamp of the current prediction"} | - | - | - |
| `velocity_major` | `double` | `True` | {"description": "Major axis velocity"} | - | - | - |
| `mean_flood_dir` | `double` | `True` | {"description": "Mean flood direction in degrees"} | - | - | - |
| `mean_ebb_dir` | `double` | `True` | {"description": "Mean ebb direction in degrees"} | - | - | - |
| `depth` | `double` | `True` | {"description": "Depth of measurement"} | - | - | - |
| `bin` | `string` | `True` | {"description": "Bin number"} | - | - | - |

### Schemagroup `Microsoft.OpenData.US.NOAA.avro`
<a id="schemagroup-microsoftopendatausnoaaavro"></a>

#### Schema `Microsoft.OpenData.US.NOAA.WaterLevel`
<a id="schema-microsoftopendatausnoaawaterlevel"></a>

| Field | Value |
| --- | --- |
| Name | WaterLevel |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterLevel |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the water level measurement"} | `-` |
| `value` | `double` | {"description": "Value of the water level"} | `-` |
| `stddev` | `double` | {"description": "Standard deviation of 1-second samples used to compute the water level height"} | `-` |
| `outside_sigma_band` | `boolean` | {"description": "Flag indicating if the water level is outside a 3-sigma band. Possible values: 'false' (not outside), 'true' (outside)."} | `-` |
| `flat_tolerance_limit` | `boolean` | {"description": "Flag indicating if the flat tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} | `-` |
| `rate_of_change_limit` | `boolean` | {"description": "Flag indicating if the rate of change tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} | `-` |
| `max_min_expected_height` | `boolean` | {"description": "Flag indicating if the max/min expected water level height is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."} | `-` |
| `quality` | enum `QualityLevel` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.Predictions`
<a id="schema-microsoftopendatausnoaapredictions"></a>

| Field | Value |
| --- | --- |
| Name | Predictions |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Predictions |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the prediction"} | `-` |
| `value` | `double` | {"description": "Value of the prediction"} | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.AirPressure`
<a id="schema-microsoftopendatausnoaaairpressure"></a>

| Field | Value |
| --- | --- |
| Name | AirPressure |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | AirPressure |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the air pressure measurement"} | `-` |
| `value` | `double` | {"description": "Value of the air pressure"} | `-` |
| `max_pressure_exceeded` | `boolean` | Flag indicating if the maximum expected air pressure was exceeded | `-` |
| `min_pressure_exceeded` | `boolean` | Flag indicating if the minimum expected air pressure was exceeded | `-` |
| `rate_of_change_exceeded` | `boolean` | Flag indicating if the rate of change tolerance limit was exceeded | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.AirTemperature`
<a id="schema-microsoftopendatausnoaaairtemperature"></a>

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | AirTemperature |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the air temperature measurement"} | `-` |
| `value` | `double` | {"description": "Value of the air temperature"} | `-` |
| `max_temp_exceeded` | `boolean` | Flag indicating if the maximum expected air temperature was exceeded | `-` |
| `min_temp_exceeded` | `boolean` | Flag indicating if the minimum expected air temperature was exceeded | `-` |
| `rate_of_change_exceeded` | `boolean` | Flag indicating if the rate of change tolerance limit was exceeded | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.WaterTemperature`
<a id="schema-microsoftopendatausnoaawatertemperature"></a>

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | WaterTemperature |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the water temperature measurement"} | `-` |
| `value` | `double` | {"description": "Value of the water temperature"} | `-` |
| `max_temp_exceeded` | `boolean` | Flag indicating if the maximum expected water temperature was exceeded | `-` |
| `min_temp_exceeded` | `boolean` | Flag indicating if the minimum expected water temperature was exceeded | `-` |
| `rate_of_change_exceeded` | `boolean` | Flag indicating if the rate of change tolerance limit was exceeded | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.Wind`
<a id="schema-microsoftopendatausnoaawind"></a>

| Field | Value |
| --- | --- |
| Name | Wind |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Wind |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the wind measurement"} | `-` |
| `speed` | `double` | {"description": "Wind speed"} | `-` |
| `direction_degrees` | `string` | {"description": "Wind direction"} | `-` |
| `direction_text` | `string` | {"description": "Direction - wind direction in text."} | `-` |
| `gusts` | `double` | {"description": "Wind gust speed"} | `-` |
| `max_wind_speed_exceeded` | `boolean` | Flag indicating if the maximum wind speed was exceeded | `-` |
| `rate_of_change_exceeded` | `boolean` | Flag indicating if the rate of change tolerance limit was exceeded | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.Humidity`
<a id="schema-microsoftopendatausnoaahumidity"></a>

| Field | Value |
| --- | --- |
| Name | Humidity |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Humidity |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the humidity measurement"} | `-` |
| `value` | `double` | {"description": "Value of the humidity"} | `-` |
| `max_humidity_exceeded` | `boolean` | Flag indicating if the maximum expected humidity was exceeded | `-` |
| `min_humidity_exceeded` | `boolean` | Flag indicating if the minimum expected humidity was exceeded | `-` |
| `rate_of_change_exceeded` | `boolean` | Flag indicating if the rate of change tolerance limit was exceeded | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.Conductivity`
<a id="schema-microsoftopendatausnoaaconductivity"></a>

| Field | Value |
| --- | --- |
| Name | Conductivity |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Conductivity |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the conductivity measurement"} | `-` |
| `value` | `double` | {"description": "Value of the conductivity"} | `-` |
| `max_conductivity_exceeded` | `boolean` | Flag indicating if the maximum expected conductivity was exceeded | `-` |
| `min_conductivity_exceeded` | `boolean` | Flag indicating if the minimum expected conductivity was exceeded | `-` |
| `rate_of_change_exceeded` | `boolean` | Flag indicating if the rate of change tolerance limit was exceeded | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.Salinity`
<a id="schema-microsoftopendatausnoaasalinity"></a>

| Field | Value |
| --- | --- |
| Name | Salinity |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Salinity |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the salinity measurement"} | `-` |
| `salinity` | `double` | {"description": "Value of the salinity"} | `-` |
| `grams_per_kg` | `double` | {"description": "Grams of salt per kilogram of water"} | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.Station`
<a id="schema-microsoftopendatausnoaastation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `tidal` | `boolean` | {"description": "Indicates whether the station measures tidal data."} | `-` |
| `greatlakes` | `boolean` | {"description": "Indicates whether the station is located in the Great Lakes region."} | `-` |
| `shefcode` | `string` | {"description": "Standard Hydrologic Exchange Format code for the station."} | `-` |
| `details` | record `details` |  | `-` |
| `sensors` | record `sensors` |  | `-` |
| `floodlevels` | record `floodlevels` |  | `-` |
| `datums` | record `datums` |  | `-` |
| `supersededdatums` | record `supersededdatums` |  | `-` |
| `harmonicConstituents` | record `harmonicConstituents` |  | `-` |
| `benchmarks` | record `benchmarks` |  | `-` |
| `tidePredOffsets` | record `tidePredOffsets` |  | `-` |
| `ofsMapOffsets` | record `ofsMapOffsets` |  | `-` |
| `state` | `string` | {"description": "State where the station is located."} | `-` |
| `timezone` | `string` | {"description": "Timezone of the station."} | `-` |
| `timezonecorr` | `int` | {"description": "Timezone correction in minutes for the station."} | `-` |
| `observedst` | `boolean` | {"description": "Indicates whether the station observes Daylight Saving Time."} | `-` |
| `stormsurge` | `boolean` | {"description": "Indicates whether the station measures storm surge data."} | `-` |
| `nearby` | record `nearby` |  | `-` |
| `forecast` | `boolean` | {"description": "Indicates whether the station provides forecast data."} | `-` |
| `outlook` | `boolean` | {"description": "Indicates whether the station provides outlook data."} | `-` |
| `HTFhistorical` | `boolean` | {"description": "Indicates whether the station has historical High Tide Flooding data."} | `-` |
| `nonNavigational` | `boolean` | {"description": "Indicates whether the station is non-navigational."} | `-` |
| `station_id` | `string` | {"description": "Unique identifier for the station."} | `-` |
| `name` | `string` | {"description": "Name of the station."} | `-` |
| `lat` | `double` | {"description": "Latitude of the station."} | `-` |
| `lng` | `double` | {"description": "Longitude of the station."} | `-` |
| `affiliations` | `string` | {"description": "Affiliations of the station."} | `-` |
| `portscode` | `string` | {"description": "PORTS code for the station."} | `-` |
| `products` | record `products` |  | `-` |
| `disclaimers` | record `disclaimers` |  | `-` |
| `notices` | record `notices` |  | `-` |
| `self` | `string` | {"description": "URL to the station's data."} | `-` |
| `expand` | `string` | {"description": "URL to expanded information about the station."} | `-` |
| `tideType` | `string` | {"description": "Type of tide measured by the station."} | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.Visibility`
<a id="schema-microsoftopendatausnoaavisibility"></a>

| Field | Value |
| --- | --- |
| Name | Visibility |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Visibility |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `timestamp` | `string` | {"description": "Timestamp of the visibility measurement"} | `-` |
| `value` | `double` | {"description": "Value of the visibility"} | `-` |
| `max_visibility_exceeded` | `boolean` | A flag that indicates whether the maximum expected visibility was exceeded | `-` |
| `min_visibility_exceeded` | `boolean` | A flag that indicates whether the minimum expected visibility was exceeded | `-` |
| `rate_of_change_exceeded` | `boolean` | A flag that indicates whether the rate of change tolerance limit was exceeded | `-` |
| `station_id` | `string` |  | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.Currents`
<a id="schema-microsoftopendatausnoaacurrents"></a>

| Field | Value |
| --- | --- |
| Name | Currents |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Currents |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the currents measurement"} | `-` |
| `speed` | `double` | {"description": "Current speed"} | `-` |
| `direction_degrees` | `double` | {"description": "Current direction in degrees"} | `-` |
| `bin` | `string` | {"description": "Bin number"} | `-` |

#### Schema `Microsoft.OpenData.US.NOAA.CurrentPredictions`
<a id="schema-microsoftopendatausnoaacurrentpredictions"></a>

| Field | Value |
| --- | --- |
| Name | CurrentPredictions |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | CurrentPredictions |
| Namespace | Microsoft.OpenData.US.NOAA |
| Type | `record` |
| Doc |  |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | {"description": "7 character station ID, or a currents station ID."} | `-` |
| `timestamp` | `string` | {"description": "Timestamp of the current prediction"} | `-` |
| `velocity_major` | `double` | {"description": "Major axis velocity"} | `-` |
| `mean_flood_dir` | `double` | {"description": "Mean flood direction in degrees"} | `-` |
| `mean_ebb_dir` | `double` | {"description": "Mean ebb direction in degrees"} | `-` |
| `depth` | `double` | {"description": "Depth of measurement"} | `-` |
| `bin` | `string` | {"description": "Bin number"} | `-` |
