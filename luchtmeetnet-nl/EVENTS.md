# Luchtmeetnet Netherlands Air Quality Bridge Events

This source bridges the public Dutch **Luchtmeetnet** API into Apache Kafka compatible brokers as structured JSON CloudEvents. It emits both slowly changing reference data and hourly telemetry so downstream consumers can reconstruct air quality context and measurements over time without making their own side calls.

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

### Endpoint `nl.rivm.luchtmeetnet.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`nl.rivm.luchtmeetnet`](#messagegroup-nlrivmluchtmeetnet) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `luchtmeetnet-nl` |
| Kafka key | `{station_number}` |
| Deployed | False |

### Endpoint `nl.rivm.luchtmeetnet.components.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`nl.rivm.luchtmeetnet.components`](#messagegroup-nlrivmluchtmeetnetcomponents) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `luchtmeetnet-nl` |
| Kafka key | `{formula}` |
| Deployed | False |

## Messagegroups

### Messagegroup `nl.rivm.luchtmeetnet`
<a id="messagegroup-nlrivmluchtmeetnet"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `nl.rivm.luchtmeetnet.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `nl.rivm.luchtmeetnet.Station`
<a id="message-nlrivmluchtmeetnetstation"></a>

Luchtmeetnet station metadata with location, operator, coordinates, and the formulas measured at the station.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/nl.rivm.luchtmeetnet.jstruct/schemas/nl.rivm.luchtmeetnet.Station`](#schema-nlrivmluchtmeetnetstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `nl.rivm.luchtmeetnet.Station` |
| `source` |  | `string` | `False` | `https://api.luchtmeetnet.nl/open_api/stations` |
| `subject` |  | `uritemplate` | `False` | `{station_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `nl.rivm.luchtmeetnet.Kafka` | `KAFKA` | topic `luchtmeetnet-nl`; key `{station_number}` |

#### Message `nl.rivm.luchtmeetnet.Measurement`
<a id="message-nlrivmluchtmeetnetmeasurement"></a>

Hourly Luchtmeetnet measurement for a station and component formula.

| Field | Value |
| --- | --- |
| Name | Measurement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/nl.rivm.luchtmeetnet.jstruct/schemas/nl.rivm.luchtmeetnet.Measurement`](#schema-nlrivmluchtmeetnetmeasurement) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `nl.rivm.luchtmeetnet.Measurement` |
| `source` |  | `string` | `False` | `https://api.luchtmeetnet.nl/open_api/measurements` |
| `subject` |  | `uritemplate` | `False` | `{station_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `nl.rivm.luchtmeetnet.Kafka` | `KAFKA` | topic `luchtmeetnet-nl`; key `{station_number}` |

#### Message `nl.rivm.luchtmeetnet.LKI`
<a id="message-nlrivmluchtmeetnetlki"></a>

Hourly Dutch Luchtkwaliteitsindex value for a station.

| Field | Value |
| --- | --- |
| Name | LKI |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/nl.rivm.luchtmeetnet.jstruct/schemas/nl.rivm.luchtmeetnet.LKI`](#schema-nlrivmluchtmeetnetlki) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `nl.rivm.luchtmeetnet.LKI` |
| `source` |  | `string` | `False` | `https://api.luchtmeetnet.nl/open_api/lki` |
| `subject` |  | `uritemplate` | `False` | `{station_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `nl.rivm.luchtmeetnet.Kafka` | `KAFKA` | topic `luchtmeetnet-nl`; key `{station_number}` |

### Messagegroup `nl.rivm.luchtmeetnet.components`
<a id="messagegroup-nlrivmluchtmeetnetcomponents"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `nl.rivm.luchtmeetnet.components.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `nl.rivm.luchtmeetnet.components.Component`
<a id="message-nlrivmluchtmeetnetcomponentscomponent"></a>

Reference definition for a monitored component formula in the Luchtmeetnet network.

| Field | Value |
| --- | --- |
| Name | Component |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/nl.rivm.luchtmeetnet.jstruct/schemas/nl.rivm.luchtmeetnet.components.Component`](#schema-nlrivmluchtmeetnetcomponentscomponent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `nl.rivm.luchtmeetnet.components.Component` |
| `source` |  | `string` | `False` | `https://api.luchtmeetnet.nl/open_api/components` |
| `subject` |  | `uritemplate` | `False` | `{formula}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `nl.rivm.luchtmeetnet.components.Kafka` | `KAFKA` | topic `luchtmeetnet-nl`; key `{formula}` |

## Schemagroups

### Schemagroup `nl.rivm.luchtmeetnet.jstruct`
<a id="schemagroup-nlrivmluchtmeetnetjstruct"></a>

#### Schema `nl.rivm.luchtmeetnet.Station`
<a id="schema-nlrivmluchtmeetnetstation"></a>

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
| $id | `https://realtime.example.com/schemas/nl/rivm/luchtmeetnet/Station` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/nl/rivm/luchtmeetnet/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Metadata for a Luchtmeetnet measuring station, combining the station list resource with the station detail resource so downstream consumers can interpret later measurements and LKI values in temporal context.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_number` | `string` | `True` | Stable Luchtmeetnet station code, such as NL01491, used in station, measurement, and LKI requests. | - | - | - |
| `location` | `string` | `True` | Human-readable station location label published by Luchtmeetnet. | - | - | - |
| `type` | `string` | `True` | Station classification returned by the detail endpoint, for example Traffic, Industrial, Background, or Regional. | - | - | - |
| `organisation` | `string` | `True` | Organisation operating or publishing the station in the Luchtmeetnet network, such as RIVM or a regional environmental agency. | - | - | - |
| `municipality` | `union` | `True` | Municipality name for the station location when present in the detail response; null when the API does not provide one. | - | - | - |
| `province` | `union` | `True` | Province name for the station location when present in the detail response; null when the API omits it. | - | - | - |
| `longitude` | `double` | `True` | Longitude of the station in WGS84 decimal degrees, taken from geometry.coordinates[0]. | - | - | - |
| `latitude` | `double` | `True` | Latitude of the station in WGS84 decimal degrees, taken from geometry.coordinates[1]. | - | - | - |
| `year_start` | `string` | `True` | Year in which the station became operational according to the detail response. The upstream can return an empty string when the start year is not populated. | - | - | - |
| `components` | array of `string` | `True` | Ordered list of formula codes measured at the station, as returned by the station detail endpoint. | - | - | - |

#### Schema `nl.rivm.luchtmeetnet.Measurement`
<a id="schema-nlrivmluchtmeetnetmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | Measurement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://realtime.example.com/schemas/nl/rivm/luchtmeetnet/Measurement` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/nl/rivm/luchtmeetnet/Measurement` |
| Type | `object` |

###### Object `Measurement`
<a id="schema-node-measurement"></a>

Hourly Luchtmeetnet measurement for a station and a single component formula. The API returns the latest values on page 1 and orders the series by measurement time.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_number` | `string` | `True` | Stable Luchtmeetnet station code identifying where the measurement was taken. | - | - | - |
| `formula` | `string` | `True` | Component formula code identifying what was measured, for example NO2, O3, PM10, or FN. | - | - | - |
| `value` | `double` | `True` | Numeric measurement value published by the API for the station and formula at the given timestamp. Standard gaseous and particulate concentration formulas are expressed in micrograms per cubic meter; some specialised formulas such as particle counts or black-carbon indicators may use different domain-specific units, so consumers should interpret the formula-specific semantics together with the component catalog. | unit=`ugm-3` | - | - |
| `timestamp_measured` | `string` | `True` | Timestamp at which the value was measured, encoded as an ISO 8601 date-time string with timezone offset. | - | - | - |

#### Schema `nl.rivm.luchtmeetnet.LKI`
<a id="schema-nlrivmluchtmeetnetlki"></a>

| Field | Value |
| --- | --- |
| Name | LKI |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://realtime.example.com/schemas/nl/rivm/luchtmeetnet/LKI` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/nl/rivm/luchtmeetnet/LKI` |
| Type | `object` |

###### Object `LKI`
<a id="schema-node-lki"></a>

Hourly Dutch national air quality index value for a station. The LKI scale runs from 1 to 11, where lower values indicate better air quality.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_number` | `string` | `True` | Stable Luchtmeetnet station code identifying the station for which the LKI value was calculated. | - | - | - |
| `value` | `integer` | `True` | Luchtkwaliteitsindex value on the Dutch 1 to 11 scale, where 1 to 3 is good, 4 to 6 is moderate, 7 to 9 is bad, and 10 to 11 is very bad. | unit=`1` | - | - |
| `timestamp_measured` | `string` | `True` | Timestamp for the hourly LKI value, encoded as an ISO 8601 date-time string with timezone offset. | - | - | - |

#### Schema `nl.rivm.luchtmeetnet.components.Component`
<a id="schema-nlrivmluchtmeetnetcomponentscomponent"></a>

| Field | Value |
| --- | --- |
| Name | Component |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://realtime.example.com/schemas/nl/rivm/luchtmeetnet/Component` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/nl/rivm/luchtmeetnet/components/Component` |
| Type | `object` |

###### Object `Component`
<a id="schema-node-component"></a>

Reference definition for a Luchtmeetnet monitored component formula as returned by the component catalog endpoint.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `formula` | `string` | `True` | Stable component formula code used in measurement queries and in station component lists, such as NO2, PM25, O3, or BCWB. | - | - | - |
| `name_nl` | `string` | `True` | Dutch display name for the component from the component catalog. | - | - | - |
| `name_en` | `string` | `True` | English display name for the component from the component catalog. | - | - | - |

### Schemagroup `nl.rivm.luchtmeetnet.avro`
<a id="schemagroup-nlrivmluchtmeetnetavro"></a>

#### Schema `nl.rivm.luchtmeetnet.Station`
<a id="schema-nlrivmluchtmeetnetstation"></a>

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
| Namespace | nl.rivm.luchtmeetnet |
| Type | `record` |
| Doc | Metadata for a Luchtmeetnet measuring station, combining the station list resource with the station detail resource so downstream consumers can interpret later measurements and LKI values in temporal context. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_number` | `string` | Stable Luchtmeetnet station code, such as NL01491, used in station, measurement, and LKI requests. | `-` |
| `location` | `string` | Human-readable station location label published by Luchtmeetnet. | `-` |
| `type` | `string` | Station classification returned by the detail endpoint, for example Traffic, Industrial, Background, or Regional. | `-` |
| `organisation` | `string` | Organisation operating or publishing the station in the Luchtmeetnet network, such as RIVM or a regional environmental agency. | `-` |
| `municipality` | `null` \| `string` | Municipality name for the station location when present in the detail response; null when the API does not provide one. | `-` |
| `province` | `null` \| `string` | Province name for the station location when present in the detail response; null when the API omits it. | `-` |
| `longitude` | `double` | Longitude of the station in WGS84 decimal degrees, taken from geometry.coordinates[0]. | `-` |
| `latitude` | `double` | Latitude of the station in WGS84 decimal degrees, taken from geometry.coordinates[1]. | `-` |
| `year_start` | `string` | Year in which the station became operational according to the detail response. The upstream can return an empty string when the start year is not populated. | `-` |
| `components` | array of `string` | Ordered list of formula codes measured at the station, as returned by the station detail endpoint. | `-` |

#### Schema `nl.rivm.luchtmeetnet.Measurement`
<a id="schema-nlrivmluchtmeetnetmeasurement"></a>

| Field | Value |
| --- | --- |
| Name | Measurement |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Measurement |
| Namespace | nl.rivm.luchtmeetnet |
| Type | `record` |
| Doc | Hourly Luchtmeetnet measurement for a station and a single component formula. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_number` | `string` | Stable Luchtmeetnet station code identifying where the measurement was taken. | `-` |
| `formula` | `string` | Component formula code identifying what was measured, for example NO2, O3, PM10, or FN. | `-` |
| `value` | `double` | Numeric measurement value published by the API for the station and formula at the given timestamp. | `-` |
| `timestamp_measured` | `string` | Timestamp at which the value was measured, encoded as an ISO 8601 date-time string with timezone offset. | `-` |

#### Schema `nl.rivm.luchtmeetnet.LKI`
<a id="schema-nlrivmluchtmeetnetlki"></a>

| Field | Value |
| --- | --- |
| Name | LKI |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | LKI |
| Namespace | nl.rivm.luchtmeetnet |
| Type | `record` |
| Doc | Hourly Dutch national air quality index value for a station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_number` | `string` | Stable Luchtmeetnet station code identifying the station for which the LKI value was calculated. | `-` |
| `value` | `int` | Luchtkwaliteitsindex value on the Dutch 1 to 11 scale. | `-` |
| `timestamp_measured` | `string` | Timestamp for the hourly LKI value, encoded as an ISO 8601 date-time string with timezone offset. | `-` |

#### Schema `nl.rivm.luchtmeetnet.components.Component`
<a id="schema-nlrivmluchtmeetnetcomponentscomponent"></a>

| Field | Value |
| --- | --- |
| Name | Component |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Component |
| Namespace | nl.rivm.luchtmeetnet.components |
| Type | `record` |
| Doc | Reference definition for a Luchtmeetnet monitored component formula as returned by the component catalog endpoint. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `formula` | `string` | Stable component formula code used in measurement queries and in station component lists, such as NO2, PM25, O3, or BCWB. | `-` |
| `name_nl` | `string` | Dutch display name for the component from the component catalog. | `-` |
| `name_en` | `string` | English display name for the component from the component catalog. | `-` |
