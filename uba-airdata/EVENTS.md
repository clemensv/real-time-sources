# UBA Germany Air Quality Bridge Events

This source bridges the Umweltbundesamt (UBA) `air_data/v3` API into Apache Kafka compatible brokers as structured JSON CloudEvents.

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

### Endpoint `de.uba.airdata.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`de.uba.airdata`](#messagegroup-deubaairdata) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `uba-airdata` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `de.uba.airdata.components.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`de.uba.airdata.components`](#messagegroup-deubaairdatacomponents) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `uba-airdata` |
| Kafka key | `{component_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `de.uba.airdata`
<a id="messagegroup-deubaairdata"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `de.uba.airdata.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `de.uba.airdata.Station`
<a id="message-deubaairdatastation"></a>

Reference data for a UBA air quality monitoring station, including geographic position, station environment, and the denormalized monitoring network metadata published by the UBA air_data/v3 station catalog.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.uba.airdata.jstruct/schemas/de.uba.airdata.Station`](#schema-deubaairdatastation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.uba.airdata.Station` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.uba.airdata.Kafka` | `KAFKA` | topic `uba-airdata`; key `{station_id}` |

#### Message `de.uba.airdata.Measure`
<a id="message-deubaairdatameasure"></a>

Hourly one-hour-average air quality measurement for a UBA monitoring station and pollutant component as returned by the air_data/v3 measures endpoint.

| Field | Value |
| --- | --- |
| Name | Measure |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.uba.airdata.jstruct/schemas/de.uba.airdata.Measure`](#schema-deubaairdatameasure) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.uba.airdata.Measure` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.uba.airdata.Kafka` | `KAFKA` | topic `uba-airdata`; key `{station_id}` |

### Messagegroup `de.uba.airdata.components`
<a id="messagegroup-deubaairdatacomponents"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `de.uba.airdata.components.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `de.uba.airdata.components.Component`
<a id="message-deubaairdatacomponentscomponent"></a>

Reference data for an air pollutant component published by the UBA air_data/v3 components catalog, including the stable numeric component identifier, code, symbol, unit, and English display name.

| Field | Value |
| --- | --- |
| Name | Component |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/de.uba.airdata.jstruct/schemas/de.uba.airdata.components.Component`](#schema-deubaairdatacomponentscomponent) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `de.uba.airdata.components.Component` |
| `source` |  | `uritemplate` | `False` | `{feedurl}` |
| `subject` |  | `uritemplate` | `False` | `{component_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `de.uba.airdata.components.Kafka` | `KAFKA` | topic `uba-airdata`; key `{component_id}` |

## Schemagroups

### Schemagroup `de.uba.airdata.jstruct`
<a id="schemagroup-deubaairdatajstruct"></a>

#### Schema `de.uba.airdata.Station`
<a id="schema-deubaairdatastation"></a>

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
| $id | `https://github.com/clemensv/real-time-sources/schemas/de/uba/airdata/Station` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/de/uba/airdata/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data for a station in the Umweltbundesamt air_data/v3 station catalog. The station payload describes the UBA station identifier, official station code, station naming, active period, WGS84 coordinates, the denormalized federal state monitoring network, and the station environment classification.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `int32` | `True` | Stable numeric UBA station identifier from the 'station id' column. This is the station key used for CloudEvents subject and Kafka key. | - | - | - |
| `station_code` | `string` | `True` | Official station code from the 'station code' column, typically the European Environment Agency style identifier such as 'DEBE021' or 'DEBB003'. | - | - | - |
| `station_name` | `string` | `True` | Human-readable station name from the 'station name' column as published by UBA. | - | - | - |
| `station_city` | `string` | `True` | City or locality from the 'station city' column where the monitoring station is located. | - | - | - |
| `station_synonym` | `union` | `True` | Legacy or alternate station short code from the 'station synonym' column. UBA may publish an empty value when no synonym exists. | - | - | - |
| `active_from` | `string` | `True` | Station activation date from the 'station active from' column in ISO date form 'YYYY-MM-DD'. | - | - | - |
| `active_to` | `union` | `True` | Station deactivation date from the 'station active to' column in ISO date form 'YYYY-MM-DD'. Null means the station is still active. | - | - | - |
| `longitude` | `double` | `True` | Station longitude from the 'station longitude' column in WGS84 decimal degrees. | - | - | - |
| `latitude` | `double` | `True` | Station latitude from the 'station latitude' column in WGS84 decimal degrees. | - | - | - |
| `network_id` | `int32` | `True` | Stable numeric monitoring network identifier from the 'network id' column. This maps to the federal state or the UBA-operated network. | - | - | - |
| `network_code` | `string` | `True` | Short network code from the 'network code' column, usually a two-letter German state code such as 'BE' or 'BB', or 'UB' for UBA. | - | - | - |
| `network_name` | `string` | `True` | Monitoring network name from the 'network name' column, typically the English federal state name such as 'Berlin' or 'Brandenburg'. | - | - | - |
| `setting_name` | `string` | `True` | Station environment description from the 'station setting name' column, for example 'urban area'. | - | - | - |
| `setting_short` | `string` | `True` | Short station environment code from the 'station setting short name' column, for example 'urban'. | - | - | - |
| `type_name` | `string` | `True` | Station type classification from the 'station type name' column, for example 'traffic', 'background', or 'industrial'. | - | - | - |
| `street` | `union` | `True` | Street name from the 'station street' column. Null is used when UBA does not publish a street value. | - | - | - |
| `street_nr` | `union` | `True` | Street number from the 'station street nr' column. Null is used when the source publishes an empty value. | - | - | - |
| `zip_code` | `union` | `True` | Postal code from the 'station zip code' column. Null is used when the source publishes an empty value. | - | - | - |

#### Schema `de.uba.airdata.Measure`
<a id="schema-deubaairdatameasure"></a>

| Field | Value |
| --- | --- |
| Name | Measure |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://github.com/clemensv/real-time-sources/schemas/de/uba/airdata/Measure` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/de/uba/airdata/Measure` |
| Type | `object` |

###### Object `Measure`
<a id="schema-node-measure"></a>

Hourly air quality measurement record from the UBA air_data/v3 measures endpoint. The upstream API returns measurements grouped by station and measurement start time for a requested component and averaging scope.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `int32` | `True` | Stable numeric UBA station identifier for the station that reported the measurement. | - | - | - |
| `component_id` | `int32` | `True` | Stable numeric UBA pollutant component identifier from the first element of the measure value array, for example 5 for NO₂. | - | - | - |
| `scope_id` | `int32` | `True` | Stable numeric UBA averaging scope identifier from the second element of the measure value array. Scope 2 represents the one-hour average used by this bridge. | - | - | - |
| `date_start` | `string` | `True` | Measurement period start timestamp from the nested measures object key, using the UBA local datetime format 'YYYY-MM-DD HH:MM:SS'. | - | - | - |
| `date_end` | `string` | `True` | Measurement period end timestamp from the fourth element of the measure value array, using the UBA local datetime format 'YYYY-MM-DD HH:MM:SS'. | - | - | - |
| `value` | `union` | `True` | Measured pollutant value from the third element of the measure value array, expressed in the unit defined by the referenced component. Null means the source returned no numeric measurement value. | - | - | - |
| `quality_index` | `string` | `True` | UBA quality or confidence flag from the fifth element of the measure value array. The published documentation commonly references 0 valid, 1 provisional, and 2 estimated; live payloads have also been observed with the code 3. | - | - | - |

#### Schema `de.uba.airdata.components.Component`
<a id="schema-deubaairdatacomponentscomponent"></a>

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
| $id | `https://github.com/clemensv/real-time-sources/schemas/de/uba/airdata/components/Component` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/de/uba/airdata/components/Component` |
| Type | `object` |

###### Object `Component`
<a id="schema-node-component"></a>

Reference data for a pollutant component from the UBA air_data/v3 components catalog. Each component defines the stable numeric component identifier, short code, published symbol, published unit string, and English display name.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `component_id` | `int32` | `True` | Stable numeric UBA component identifier from the 'component id' column. This is the CloudEvents subject and Kafka key for component events. | - | - | - |
| `component_code` | `string` | `True` | Short UBA component code from the 'component code' column, such as 'PM10', 'NO2', 'O3', or 'PM2'. | - | - | - |
| `symbol` | `string` | `True` | Published component symbol from the 'component symbol' column. This may include Unicode subscripts, for example 'PM₁₀' or 'NO₂'. | - | - | - |
| `unit` | `string` | `True` | Published measurement unit string from the 'component unit' column, such as 'µg/m³', 'mg/m³', or 'ng/m³'. | - | - | - |
| `name` | `string` | `True` | English component display name from the 'component name' column, such as 'Particulate matter' or 'Nitrogen dioxide'. | - | - | - |
