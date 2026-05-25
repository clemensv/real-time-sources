# EPA UV Bridge Events

MQTT/5.0 transport variants for EPA UV Index forecasts. Topics are retained QoS-1 UV forecast leaves under uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/..., where {state} is lowercase US state, {city_slug} is lowercase kebab-case city, and {location_id} preserves the existing Kafka/CloudEvents entity id intentionally for subject/key compatibility even though it is derivable from state+city. Hourly slots use topic-safe {forecast_hour}=YYYYMMDDTHH; daily slots use {forecast_date}=YYYY-MM-DD. Message expiry bounds retained forecast slots so stale forecasts age out.

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
| Schemagroups | 1 |

## Endpoints

### Endpoint `US.EPA.UVIndex.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`US.EPA.UVIndex`](#messagegroup-usepauvindex) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `epa-uv` |
| Kafka key | `{location_id}` |
| Deployed | False |

### Endpoint `US.EPA.UVIndex.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`US.EPA.UVIndex.mqtt`](#messagegroup-usepauvindexmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `US.EPA.UVIndex`
<a id="messagegroup-usepauvindex"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `US.EPA.UVIndex.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `US.EPA.UVIndex.HourlyForecast`
<a id="message-usepauvindexhourlyforecast"></a>

| Field | Value |
| --- | --- |
| Name | HourlyForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.EPA.UVIndex.jstruct/schemas/US.EPA.UVIndex.HourlyForecast`](#schema-usepauvindexhourlyforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.EPA.UVIndex.HourlyForecast` |
| `source` |  | `string` | `False` | `https://www.epa.gov/enviro/web-services` |
| `subject` |  | `uritemplate` | `False` | `{location_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.EPA.UVIndex.Kafka` | `KAFKA` | topic `epa-uv`; key `{location_id}` |

#### Message `US.EPA.UVIndex.DailyForecast`
<a id="message-usepauvindexdailyforecast"></a>

| Field | Value |
| --- | --- |
| Name | DailyForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.EPA.UVIndex.jstruct/schemas/US.EPA.UVIndex.DailyForecast`](#schema-usepauvindexdailyforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.EPA.UVIndex.DailyForecast` |
| `source` |  | `string` | `False` | `https://www.epa.gov/enviro/web-services` |
| `subject` |  | `uritemplate` | `False` | `{location_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.EPA.UVIndex.Kafka` | `KAFKA` | topic `epa-uv`; key `{location_id}` |

### Messagegroup `US.EPA.UVIndex.mqtt`
<a id="messagegroup-usepauvindexmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for EPA UV Index forecasts. Topics are retained QoS-1 UV forecast leaves under uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/..., where {state} is lowercase US state, {city_slug} is lowercase kebab-case city, and {location_id} preserves the existing Kafka/CloudEvents entity id intentionally for subject/key compatibility even though it is derivable from state+city. Hourly slots use topic-safe {forecast_hour}=YYYYMMDDTHH; daily slots use {forecast_date}=YYYY-MM-DD. Message expiry bounds retained forecast slots so stale forecasts age out. |
| Transport bindings | `US.EPA.UVIndex.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `US.EPA.UVIndex.mqtt.HourlyForecast`
<a id="message-usepauvindexmqtthourlyforecast"></a>

| Field | Value |
| --- | --- |
| Name | HourlyForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.EPA.UVIndex.jstruct/schemas/US.EPA.UVIndex.HourlyForecast`](#schema-usepauvindexhourlyforecast) |
| Base message chain | `/messagegroups/US.EPA.UVIndex/messages/US.EPA.UVIndex.HourlyForecast` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.EPA.UVIndex.HourlyForecast` |
| `source` |  | `string` | `False` | `https://www.epa.gov/enviro/web-services` |
| `subject` |  | `uritemplate` | `False` | `{location_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.EPA.UVIndex.Mqtt` | `MQTT/5.0` | topic `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/hourly/{forecast_hour}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/hourly/{forecast_hour}` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 172800}` |

#### Message `US.EPA.UVIndex.mqtt.DailyForecast`
<a id="message-usepauvindexmqttdailyforecast"></a>

| Field | Value |
| --- | --- |
| Name | DailyForecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/US.EPA.UVIndex.jstruct/schemas/US.EPA.UVIndex.DailyForecast`](#schema-usepauvindexdailyforecast) |
| Base message chain | `/messagegroups/US.EPA.UVIndex/messages/US.EPA.UVIndex.DailyForecast` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `US.EPA.UVIndex.DailyForecast` |
| `source` |  | `string` | `False` | `https://www.epa.gov/enviro/web-services` |
| `subject` |  | `uritemplate` | `False` | `{location_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `US.EPA.UVIndex.Mqtt` | `MQTT/5.0` | topic `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/daily/{forecast_date}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `uv/us/epa/epa-uv/{state}/{city_slug}/{location_id}/daily/{forecast_date}` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 1209600}` |

## Schemagroups

### Schemagroup `US.EPA.UVIndex.jstruct`
<a id="schemagroup-usepauvindexjstruct"></a>

#### Schema `US.EPA.UVIndex.HourlyForecast`
<a id="schema-usepauvindexhourlyforecast"></a>

| Field | Value |
| --- | --- |
| Name | HourlyForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/epa-uv/schemas/US.EPA.UVIndex.HourlyForecast.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `HourlyForecast`
<a id="schema-node-hourlyforecast"></a>

Hourly UV Index forecast for a configured city and state from the EPA Envirofacts UV hourly service.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/epa-uv/schemas/US.EPA.UVIndex.HourlyForecast.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `location_id` | `string` | `True` | Stable slug derived from the configured city and state. | - | - | - |
| `city` | `string` | `True` | City for which the hourly UV forecast was requested. | - | - | - |
| `state` | `string` | `True` | Lowercase two-letter US state segment used for MQTT/UNS routing; display/input state is normalized by the bridge. | - | - | - |
| `forecast_datetime` | `string` | `True` | Forecast timestamp normalized to ISO local datetime form without an explicit UTC offset. Used as the retained MQTT hourly slot with message expiry. | - | - | - |
| `uv_index` | `integer` | `True` | Hourly UV Index forecast value. | - | - | - |
| `city_slug` | `string` | `True` | Lowercase kebab-case city segment used for MQTT/UNS routing; derived from city without the state suffix. | - | - | - |
| `forecast_hour` | `string` | `True` | Topic-safe retained forecast slot in YYYYMMDDTHH form, derived from forecast_datetime with zero padding and no offset, colon, slash, plus, or hash characters. | - | - | - |

#### Schema `US.EPA.UVIndex.DailyForecast`
<a id="schema-usepauvindexdailyforecast"></a>

| Field | Value |
| --- | --- |
| Name | DailyForecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/epa-uv/schemas/US.EPA.UVIndex.DailyForecast.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `DailyForecast`
<a id="schema-node-dailyforecast"></a>

Daily UV Index forecast and alert flag for a configured city and state from the EPA Envirofacts UV daily service.

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/epa-uv/schemas/US.EPA.UVIndex.DailyForecast.json` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `location_id` | `string` | `True` | Stable slug derived from the configured city and state. | - | - | - |
| `city` | `string` | `True` | City for which the daily UV forecast was requested. | - | - | - |
| `state` | `string` | `True` | Lowercase two-letter US state segment used for MQTT/UNS routing; display/input state is normalized by the bridge. | - | - | - |
| `forecast_date` | `string` | `True` | Topic-safe forecast date normalized to YYYY-MM-DD. Used as the retained MQTT daily slot with message expiry. | - | - | - |
| `uv_index` | `integer` | `True` | Daily UV Index forecast value. | - | - | - |
| `uv_alert` | `string` | `True` | Character flag indicating whether a UV alert is issued for the forecast day. | - | - | - |
| `city_slug` | `string` | `True` | Lowercase kebab-case city segment used for MQTT/UNS routing; derived from city without the state suffix. | - | - | - |
