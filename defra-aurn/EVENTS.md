# Defra AURN Bridge Usage Guide Events

This bridge polls the UK Defra Automatic Urban and Rural Network (AURN) SOS Timeseries API and republishes station metadata, timeseries metadata, and fresh hourly observations to Kafka as CloudEvents in structured JSON mode.

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

### Endpoint `uk.gov.defra.aurn.Stations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`uk.gov.defra.aurn.Stations`](#messagegroup-ukgovdefraaurnstations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `defra-aurn` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `uk.gov.defra.aurn.Timeseries.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`uk.gov.defra.aurn.Timeseries`](#messagegroup-ukgovdefraaurntimeseries) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `defra-aurn` |
| Kafka key | `{timeseries_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `uk.gov.defra.aurn.Stations`
<a id="messagegroup-ukgovdefraaurnstations"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `uk.gov.defra.aurn.Stations.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `uk.gov.defra.aurn.Station`
<a id="message-ukgovdefraaurnstation"></a>

Reference metadata for a Defra AURN monitoring station entry as published by the 52°North SOS Timeseries API stations collection.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.defra.aurn.jstruct/schemas/uk.gov.defra.aurn.Station`](#schema-ukgovdefraaurnstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.defra.aurn.Station` |
| `source` |  | `string` | `False` | `https://uk-air.defra.gov.uk/sos-ukair/api/v1/stations` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.defra.aurn.Stations.Kafka` | `KAFKA` | topic `defra-aurn`; key `{station_id}` |

### Messagegroup `uk.gov.defra.aurn.Timeseries`
<a id="messagegroup-ukgovdefraaurntimeseries"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `uk.gov.defra.aurn.Timeseries.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `uk.gov.defra.aurn.Timeseries`
<a id="message-ukgovdefraaurntimeseries"></a>

Reference metadata for a Defra AURN station and pollutant timeseries combination, including linked station coordinates and pollutant taxonomy identifiers.

| Field | Value |
| --- | --- |
| Name | Timeseries |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.defra.aurn.jstruct/schemas/uk.gov.defra.aurn.Timeseries`](#schema-ukgovdefraaurntimeseries) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.defra.aurn.Timeseries` |
| `source` |  | `string` | `False` | `https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries` |
| `subject` |  | `uritemplate` | `False` | `{timeseries_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.defra.aurn.Timeseries.Kafka` | `KAFKA` | topic `defra-aurn`; key `{timeseries_id}` |

#### Message `uk.gov.defra.aurn.Observation`
<a id="message-ukgovdefraaurnobservation"></a>

Hourly or near-hourly Defra AURN observation value for a single timeseries, emitted from the getData endpoint for the most recent two-hour polling window.

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.defra.aurn.jstruct/schemas/uk.gov.defra.aurn.Observation`](#schema-ukgovdefraaurnobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.defra.aurn.Observation` |
| `source` |  | `string` | `False` | `https://uk-air.defra.gov.uk/sos-ukair/api/v1/timeseries` |
| `subject` |  | `uritemplate` | `False` | `{timeseries_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.defra.aurn.Timeseries.Kafka` | `KAFKA` | topic `defra-aurn`; key `{timeseries_id}` |

## Schemagroups

### Schemagroup `uk.gov.defra.aurn.jstruct`
<a id="schemagroup-ukgovdefraaurnjstruct"></a>

#### Schema `uk.gov.defra.aurn.Station`
<a id="schema-ukgovdefraaurnstation"></a>

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
| $id | `https://clemensv.github.io/real-time-sources/schemas/uk/gov/defra/aurn/station.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/uk/gov/defra/aurn/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Metadata for a Defra AURN monitoring station as returned by GET /stations. The bridge flattens the GeoJSON feature into a payload with the station identifier, the upstream display label, and WGS84 latitude and longitude values taken from geometry.coordinates[0] and geometry.coordinates[1], because this API returns coordinates in latitude, longitude order.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable numeric monitoring station identifier from the GeoJSON feature properties.id field returned by GET /stations. The bridge converts the numeric API value to a string so it can be used consistently as the Kafka key and CloudEvents subject. | - | pattern=`^[0-9]+$` | - |
| `label` | `string` | `True` | Upstream station label from properties.label in GET /stations. In this API the label includes both the site name and the monitored pollutant description, for example 'Camden Kerbside-Particulate matter less than 10 micro m (aerosol)'. | - | - | - |
| `latitude` | `double` | `True` | WGS84 latitude in decimal degrees taken from geometry.coordinates[0] in the Defra SOS GeoJSON feature. The upstream API uses latitude-first coordinate ordering rather than GeoJSON's usual longitude-first convention. | unit=`degree` symbol=`°` | maximum=`90`<br>minimum=`-90` | - |
| `longitude` | `double` | `True` | WGS84 longitude in decimal degrees taken from geometry.coordinates[1] in the Defra SOS GeoJSON feature. The bridge ignores the third coordinate array member because the upstream API returns a string 'NaN' elevation value there. | unit=`degree` symbol=`°` | maximum=`180`<br>minimum=`-180` | - |

#### Schema `uk.gov.defra.aurn.Timeseries`
<a id="schema-ukgovdefraaurntimeseries"></a>

| Field | Value |
| --- | --- |
| Name | Timeseries |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://clemensv.github.io/real-time-sources/schemas/uk/gov/defra/aurn/timeseries.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/uk/gov/defra/aurn/Timeseries` |
| Type | `object` |

###### Object `Timeseries`
<a id="schema-node-timeseries"></a>

Reference metadata for a Defra AURN station and pollutant timeseries combination, assembled from GET /timeseries/{id}?expanded=true. The payload preserves the stable timeseries identifier, linked station metadata, unit of measurement, and pollutant taxonomy references published in parameters.phenomenon and parameters.category.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `timeseries_id` | `string` | `True` | Stable numeric timeseries identifier from the id field returned by GET /timeseries and GET /timeseries/{id}?expanded=true. Each timeseries represents one station and one pollutant combination. | - | pattern=`^[0-9]+$` | - |
| `label` | `string` | `True` | Descriptive label from the timeseries label field. In the live API this string combines the EIONet pollutant URI, the station identifier, and the station display label. | - | - | - |
| `uom` | `string` | `True` | Unit of measurement string from the timeseries uom field, for example 'ug.m-3'. The bridge republishes the upstream unit token unchanged so consumers can interpret observation values correctly. | - | - | - |
| `station_id` | `string` | `True` | Stable station identifier from station.properties.id inside the expanded timeseries response. This is the identifier of the monitoring site associated with the timeseries. | - | pattern=`^[0-9]+$` | - |
| `station_label` | `string` | `True` | Station display label from station.properties.label inside the expanded timeseries response. In this API the label already includes the pollutant name, so it is unique per station and pollutant combination. | - | - | - |
| `latitude` | `union` | `False` | WGS84 latitude in decimal degrees derived from station.geometry.coordinates[0] in the expanded timeseries response. The field is nullable because the bridge will emit null if the upstream omits coordinates. | unit=`degree` symbol=`°` | maximum=`90`<br>minimum=`-90` | - |
| `longitude` | `union` | `False` | WGS84 longitude in decimal degrees derived from station.geometry.coordinates[1] in the expanded timeseries response. The field is nullable because the bridge will emit null if the upstream omits coordinates. | unit=`degree` symbol=`°` | maximum=`180`<br>minimum=`-180` | - |
| `phenomenon_id` | `union` | `False` | Pollutant phenomenon identifier from parameters.phenomenon.id in the expanded timeseries response. The API models pollutants through EIONet vocabulary identifiers and numeric ids. | - | pattern=`^[0-9]+$` | - |
| `phenomenon_label` | `union` | `False` | Pollutant label from parameters.phenomenon.label in the expanded timeseries response. In the live API this is typically an EIONet pollutant URI such as 'http://dd.eionet.europa.eu/vocabulary/aq/pollutant/5'. | - | - | - |
| `category_id` | `union` | `False` | Category identifier from parameters.category.id in the expanded timeseries response. In this API the category collection currently mirrors the phenomenon collection, but it is still carried through explicitly because it is part of the published timeseries metadata. | - | pattern=`^[0-9]+$` | - |
| `category_label` | `union` | `False` | Category label from parameters.category.label in the expanded timeseries response. In the live API this is the same EIONet URI string as the phenomenon label for the same pollutant. | - | - | - |

#### Schema `uk.gov.defra.aurn.Observation`
<a id="schema-ukgovdefraaurnobservation"></a>

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
| $id | `https://clemensv.github.io/real-time-sources/schemas/uk/gov/defra/aurn/observation.json` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/uk/gov/defra/aurn/Observation` |
| Type | `object` |

###### Object `Observation`
<a id="schema-node-observation"></a>

Observation value from GET /timeseries/{id}/getData. The bridge converts the upstream Unix millisecond timestamp to an ISO 8601 UTC timestamp string and republishes the measurement value together with the timeseries identifier and unit of measurement from the reference metadata.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `timeseries_id` | `string` | `True` | Stable numeric timeseries identifier for the series that produced this observation. This field is the Kafka key and CloudEvents subject for both the reference timeseries event and the observation event. | - | pattern=`^[0-9]+$` | - |
| `timestamp` | `datetime` | `True` | Observation timestamp encoded as an ISO 8601 UTC string. The bridge converts the upstream GET /timeseries/{id}/getData values[].timestamp Unix millisecond value with datetime.fromtimestamp(timestamp/1000, tz=timezone.utc).isoformat(). | - | - | - |
| `value` | `union` | `True` | Measured pollutant concentration or other reported numeric reading from values[].value in GET /timeseries/{id}/getData. The field is nullable because the API can represent missing or flagged values with null. | - | - | - |
| `uom` | `string` | `True` | Unit of measurement for the observation, copied from the parent timeseries uom field so each telemetry event remains self-describing. | - | - | - |

### Schemagroup `uk.gov.defra.aurn.avro`
<a id="schemagroup-ukgovdefraaurnavro"></a>

#### Schema `uk.gov.defra.aurn.Station`
<a id="schema-ukgovdefraaurnstation"></a>

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
| Namespace | uk.gov.defra.aurn |
| Type | `record` |
| Doc | Metadata for a Defra AURN monitoring station as returned by GET /stations. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Stable numeric monitoring station identifier from properties.id. | `-` |
| `label` | `string` | Upstream station label from properties.label. | `-` |
| `latitude` | `double` | WGS84 latitude in decimal degrees from geometry.coordinates[0]. | `-` |
| `longitude` | `double` | WGS84 longitude in decimal degrees from geometry.coordinates[1]. | `-` |

#### Schema `uk.gov.defra.aurn.Timeseries`
<a id="schema-ukgovdefraaurntimeseries"></a>

| Field | Value |
| --- | --- |
| Name | Timeseries |
| Format | Avro/1.11.3 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Timeseries |
| Namespace | uk.gov.defra.aurn |
| Type | `record` |
| Doc | Reference metadata for a Defra AURN station and pollutant timeseries combination. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `timeseries_id` | `string` | Stable numeric timeseries identifier from id. | `-` |
| `label` | `string` | Descriptive label from the timeseries label field. | `-` |
| `uom` | `string` | Unit of measurement string from the timeseries uom field. | `-` |
| `station_id` | `string` | Stable station identifier from station.properties.id. | `-` |
| `station_label` | `string` | Station display label from station.properties.label. | `-` |
| `latitude` | `null` \| `double` | Nullable WGS84 latitude in decimal degrees from station.geometry.coordinates[0]. | `-` |
| `longitude` | `null` \| `double` | Nullable WGS84 longitude in decimal degrees from station.geometry.coordinates[1]. | `-` |
| `phenomenon_id` | `null` \| `string` | Nullable pollutant phenomenon identifier from parameters.phenomenon.id. | `-` |
| `phenomenon_label` | `null` \| `string` | Nullable pollutant label from parameters.phenomenon.label. | `-` |
| `category_id` | `null` \| `string` | Nullable category identifier from parameters.category.id. | `-` |
| `category_label` | `null` \| `string` | Nullable category label from parameters.category.label. | `-` |

#### Schema `uk.gov.defra.aurn.Observation`
<a id="schema-ukgovdefraaurnobservation"></a>

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
| Namespace | uk.gov.defra.aurn |
| Type | `record` |
| Doc | Observation value from GET /timeseries/{id}/getData. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `timeseries_id` | `string` | Stable numeric timeseries identifier for the series that produced this observation. | `-` |
| `timestamp` | `string` | Observation timestamp encoded as an ISO 8601 UTC string. | `-` |
| `value` | `null` \| `double` | Measured pollutant concentration or other reported numeric reading. | `-` |
| `uom` | `string` | Unit of measurement for the observation. | `-` |
