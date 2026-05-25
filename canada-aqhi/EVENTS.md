# Canada AQHI Bridge Events

This source bridges the Canadian Air Quality Health Index (AQHI) program from Environment and Climate Change Canada into Kafka as structured JSON [CloudEvents](https://cloudevents.io/).

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

### Endpoint `ca.gc.weather.aqhi.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`ca.gc.weather.aqhi`](#messagegroup-cagcweatheraqhi) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `canada-aqhi` |
| Kafka key | `{province}/{community_name}` |
| Deployed | False |

## Messagegroups

### Messagegroup `ca.gc.weather.aqhi`
<a id="messagegroup-cagcweatheraqhi"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `ca.gc.weather.aqhi.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `ca.gc.weather.aqhi.Community`
<a id="message-cagcweatheraqhicommunity"></a>

Reference data for a Canadian Air Quality Health Index reporting community, including its stable CGNDB identifier and current upstream feed URLs.

| Field | Value |
| --- | --- |
| Name | Community |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/ca.gc.weather.aqhi.jstruct/schemas/ca.gc.weather.aqhi.Community`](#schema-cagcweatheraqhicommunity) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `ca.gc.weather.aqhi.Community` |
| `source` |  | `uritemplate` | `False` | `https://dd.weather.gc.ca/today/air_quality/aqhi/` |
| `subject` |  | `uritemplate` | `False` | `{province}/{community_name}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `ca.gc.weather.aqhi.Kafka` | `KAFKA` | topic `canada-aqhi`; key `{province}/{community_name}` |

#### Message `ca.gc.weather.aqhi.Observation`
<a id="message-cagcweatheraqhiobservation"></a>

Latest AQHI observation for a reporting community. Observations are published hourly and may include decimal AQHI values.

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/ca.gc.weather.aqhi.jstruct/schemas/ca.gc.weather.aqhi.Observation`](#schema-cagcweatheraqhiobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `ca.gc.weather.aqhi.Observation` |
| `source` |  | `uritemplate` | `False` | `https://dd.weather.gc.ca/today/air_quality/aqhi/` |
| `subject` |  | `uritemplate` | `False` | `{province}/{community_name}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `ca.gc.weather.aqhi.Kafka` | `KAFKA` | topic `canada-aqhi`; key `{province}/{community_name}` |

#### Message `ca.gc.weather.aqhi.Forecast`
<a id="message-cagcweatheraqhiforecast"></a>

Public AQHI forecast for one of the four standard Canadian forecast periods published for an AQHI community.

| Field | Value |
| --- | --- |
| Name | Forecast |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/ca.gc.weather.aqhi.jstruct/schemas/ca.gc.weather.aqhi.Forecast`](#schema-cagcweatheraqhiforecast) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `ca.gc.weather.aqhi.Forecast` |
| `source` |  | `uritemplate` | `False` | `https://dd.weather.gc.ca/today/air_quality/aqhi/` |
| `subject` |  | `uritemplate` | `False` | `{province}/{community_name}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `ca.gc.weather.aqhi.Kafka` | `KAFKA` | topic `canada-aqhi`; key `{province}/{community_name}` |

## Schemagroups

### Schemagroup `ca.gc.weather.aqhi.jstruct`
<a id="schemagroup-cagcweatheraqhijstruct"></a>

#### Schema `ca.gc.weather.aqhi.Community`
<a id="schema-cagcweatheraqhicommunity"></a>

| Field | Value |
| --- | --- |
| Name | Community |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/canada-aqhi/schemas/ca.gc.weather.aqhi.Community` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/ca/gc/weather/aqhi/Community` |
| Type | `object` |

###### Object `Community`
<a id="schema-node-community"></a>

Reference record for an AQHI community from the official ECCC AQHI city lists. It links the public community name and province code to the CGNDB key and current XML feeds used by the bridge.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `province` | `string` | `True` | Two-letter Canadian province or territory abbreviation resolved for the AQHI community. | - | pattern=`^[A-Z]{2}$` | - |
| `community_name` | `string` | `True` | English AQHI community name as published by Environment and Climate Change Canada. | - | - | - |
| `cgndb_code` | `string` | `True` | Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. | - | pattern=`^[A-Z0-9]{5}$` | - |
| `latitude` | `double` | `True` | Latitude of the AQHI community reference point in WGS84 decimal degrees. | - | maximum=`90`<br>minimum=`-90` | - |
| `longitude` | `double` | `True` | Longitude of the AQHI community reference point in WGS84 decimal degrees. | - | maximum=`180`<br>minimum=`-180` | - |
| `observation_url` | `union` | `False` | Current XML observation feed URL for the AQHI community, or null when observations are not distributed for that community. | - | - | - |
| `forecast_url` | `union` | `False` | Current XML forecast feed URL for the AQHI community, or null when a public forecast feed is not available. | - | - | - |

#### Schema `ca.gc.weather.aqhi.Observation`
<a id="schema-cagcweatheraqhiobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/canada-aqhi/schemas/ca.gc.weather.aqhi.Observation` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/ca/gc/weather/aqhi/Observation` |
| Type | `object` |

###### Object `Observation`
<a id="schema-node-observation"></a>

Latest AQHI observation for a reporting community. The value reflects short-term health risk from air pollution and may be null when the upstream feed has not published a value yet.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `province` | `string` | `True` | Two-letter Canadian province or territory abbreviation resolved for the AQHI community. | - | pattern=`^[A-Z]{2}$` | - |
| `community_name` | `string` | `True` | English AQHI community name as published by Environment and Climate Change Canada. | - | - | - |
| `cgndb_code` | `string` | `True` | Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. | - | pattern=`^[A-Z0-9]{5}$` | - |
| `observation_datetime` | `string` | `True` | UTC timestamp of the AQHI observation in ISO 8601 format. | - | - | - |
| `aqhi` | `union` | `False` | Observed AQHI value for the community. Observation feeds publish AQHI with decimal precision. | - | - | - |
| `aqhi_category` | enum `['Low', 'Moderate', 'High', 'Very High', 'Unknown']` | `True` | Public AQHI health-risk category derived from the AQHI value. | - | - | - |

#### Schema `ca.gc.weather.aqhi.Forecast`
<a id="schema-cagcweatheraqhiforecast"></a>

| Field | Value |
| --- | --- |
| Name | Forecast |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/canada-aqhi/schemas/ca.gc.weather.aqhi.Forecast` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/ca/gc/weather/aqhi/Forecast` |
| Type | `object` |

###### Object `Forecast`
<a id="schema-node-forecast"></a>

Public AQHI forecast for a community and one of the four standard forecast periods published by ECCC.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `province` | `string` | `True` | Two-letter Canadian province or territory abbreviation resolved for the AQHI community. | - | pattern=`^[A-Z]{2}$` | - |
| `community_name` | `string` | `True` | English AQHI community name as published by Environment and Climate Change Canada. | - | - | - |
| `cgndb_code` | `string` | `True` | Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. | - | pattern=`^[A-Z0-9]{5}$` | - |
| `publication_datetime` | `string` | `True` | UTC timestamp at which the public AQHI forecast bulletin was issued. | - | - | - |
| `forecast_date` | `string` | `True` | Forecast target date expressed as YYYYMMDD. Periods 1 and 2 use the bulletin issue date; periods 3 and 4 use the following day. | - | pattern=`^[0-9]{8}$` | - |
| `forecast_period` | enum `[1, 2, 3, 4]` | `True` | AQHI public forecast period number: 1 Today, 2 Tonight, 3 Tomorrow, 4 Tomorrow Night. | - | - | - |
| `forecast_period_label` | enum `['Today', 'Tonight', 'Tomorrow', 'Tomorrow Night']` | `True` | English public label for the AQHI forecast period. | - | - | - |
| `aqhi` | `union` | `False` | Forecast AQHI value for the forecast period. Public forecasts are published as whole numbers. | - | - | - |
| `aqhi_category` | enum `['Low', 'Moderate', 'High', 'Very High', 'Unknown']` | `True` | Public AQHI health-risk category derived from the forecast AQHI value. | - | - | - |

### Schemagroup `ca.gc.weather.aqhi.avro`
<a id="schemagroup-cagcweatheraqhiavro"></a>

#### Schema `ca.gc.weather.aqhi.Community`
<a id="schema-cagcweatheraqhicommunity"></a>

| Field | Value |
| --- | --- |
| Name | Community |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Community |
| Namespace | ca.gc.weather.aqhi |
| Type | `record` |
| Doc | Reference record for an AQHI community from the official ECCC AQHI city lists. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `province` | `string` | Two-letter Canadian province or territory abbreviation resolved for the AQHI community. | `-` |
| `community_name` | `string` | English AQHI community name as published by Environment and Climate Change Canada. | `-` |
| `cgndb_code` | `string` | Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. | `-` |
| `latitude` | `double` | Latitude of the AQHI community reference point in WGS84 decimal degrees. | `-` |
| `longitude` | `double` | Longitude of the AQHI community reference point in WGS84 decimal degrees. | `-` |
| `observation_url` | `null` \| `string` | Current XML observation feed URL for the AQHI community, or null when observations are not distributed for that community. | `-` |
| `forecast_url` | `null` \| `string` | Current XML forecast feed URL for the AQHI community, or null when a public forecast feed is not available. | `-` |

#### Schema `ca.gc.weather.aqhi.Observation`
<a id="schema-cagcweatheraqhiobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Observation |
| Namespace | ca.gc.weather.aqhi |
| Type | `record` |
| Doc | Latest AQHI observation for a reporting community. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `province` | `string` | Two-letter Canadian province or territory abbreviation resolved for the AQHI community. | `-` |
| `community_name` | `string` | English AQHI community name as published by Environment and Climate Change Canada. | `-` |
| `cgndb_code` | `string` | Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. | `-` |
| `observation_datetime` | `string` | UTC timestamp of the AQHI observation in ISO 8601 format. | `-` |
| `aqhi` | `null` \| `double` | Observed AQHI value for the community. Observation feeds publish AQHI with decimal precision. | `-` |
| `aqhi_category` | `string` | Public AQHI health-risk category derived from the AQHI value. | `-` |

#### Schema `ca.gc.weather.aqhi.Forecast`
<a id="schema-cagcweatheraqhiforecast"></a>

| Field | Value |
| --- | --- |
| Name | Forecast |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Forecast |
| Namespace | ca.gc.weather.aqhi |
| Type | `record` |
| Doc | Public AQHI forecast for a community and one of the four standard forecast periods published by ECCC. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `province` | `string` | Two-letter Canadian province or territory abbreviation resolved for the AQHI community. | `-` |
| `community_name` | `string` | English AQHI community name as published by Environment and Climate Change Canada. | `-` |
| `cgndb_code` | `string` | Five-character CGNDB community identifier published by Natural Resources Canada and referenced by ECCC AQHI feeds. | `-` |
| `publication_datetime` | `string` | UTC timestamp at which the public AQHI forecast bulletin was issued. | `-` |
| `forecast_date` | `string` | Forecast target date expressed as YYYYMMDD. | `-` |
| `forecast_period` | `int` | AQHI public forecast period number: 1 Today, 2 Tonight, 3 Tomorrow, 4 Tomorrow Night. | `-` |
| `forecast_period_label` | `string` | English public label for the AQHI forecast period. | `-` |
| `aqhi` | `null` \| `int` | Forecast AQHI value for the forecast period. Public forecasts are published as whole numbers. | `-` |
| `aqhi_category` | `string` | Public AQHI health-risk category derived from the forecast AQHI value. | `-` |
