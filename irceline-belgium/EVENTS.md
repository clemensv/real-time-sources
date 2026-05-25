# IRCELINE Belgium Events

This source bridges the IRCELINE Belgium 52°North SOS Timeseries API into Kafka as CloudEvents. It covers Belgium's interregional air-quality monitoring network and emits both reference data and hourly telemetry into a single topic.

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

### Endpoint `be.irceline.Stations.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`be.irceline.Stations`](#messagegroup-beircelinestations) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `irceline-belgium` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `be.irceline.Timeseries.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`be.irceline.Timeseries`](#messagegroup-beircelinetimeseries) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `irceline-belgium` |
| Kafka key | `{timeseries_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `be.irceline.Stations`
<a id="messagegroup-beircelinestations"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `be.irceline.Stations.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `be.irceline.Station`
<a id="message-beircelinestation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irceline.jstruct/schemas/be.irceline.Station`](#schema-beircelinestation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irceline.Station` |
| `source` |  | `string` | `False` | `https://geo.irceline.be/sos/api/v1/stations` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irceline.Stations.Kafka` | `KAFKA` | topic `irceline-belgium`; key `{station_id}` |

### Messagegroup `be.irceline.Timeseries`
<a id="messagegroup-beircelinetimeseries"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `be.irceline.Timeseries.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `be.irceline.Timeseries`
<a id="message-beircelinetimeseries"></a>

| Field | Value |
| --- | --- |
| Name | Timeseries |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irceline.jstruct/schemas/be.irceline.Timeseries`](#schema-beircelinetimeseries) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irceline.Timeseries` |
| `source` |  | `string` | `False` | `https://geo.irceline.be/sos/api/v1/timeseries` |
| `subject` |  | `uritemplate` | `False` | `{timeseries_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irceline.Timeseries.Kafka` | `KAFKA` | topic `irceline-belgium`; key `{timeseries_id}` |

#### Message `be.irceline.Observation`
<a id="message-beircelineobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irceline.jstruct/schemas/be.irceline.Observation`](#schema-beircelineobservation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irceline.Observation` |
| `source` |  | `string` | `False` | `https://geo.irceline.be/sos/api/v1/timeseries` |
| `subject` |  | `uritemplate` | `False` | `{timeseries_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irceline.Timeseries.Kafka` | `KAFKA` | topic `irceline-belgium`; key `{timeseries_id}` |

## Schemagroups

### Schemagroup `be.irceline.jstruct`
<a id="schemagroup-beircelinejstruct"></a>

#### Schema `be.irceline.Station`
<a id="schema-beircelinestation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Reference event for an IRCELINE Belgium air-quality monitoring station from GET /stations. Each record represents one GeoJSON feature with a stable numeric station identifier, human-readable label, and WGS 84 point coordinates. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://geo.irceline.be/schemas/be/irceline/Station` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `Station`
<a id="schema-node-station"></a>

Reference data describing one IRCELINE monitoring station from the GET /stations collection. The bridge maps the upstream GeoJSON feature to stable English field names and ignores the third coordinate element, which is the literal string 'NaN' in the live payloads.

| Field | Value |
| --- | --- |
| $id | `https://geo.irceline.be/schemas/be/irceline/Station` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Stable numeric station identifier from station.properties.id in the IRCELINE stations GeoJSON feed. The bridge converts the upstream integer identifier to a string because this value is also used as the CloudEvents subject and Kafka key. | altnames=`{"irceline": "properties.id"}` | pattern=`^[0-9]+$` | - |
| `label` | `string` | `True` | Human-readable station label from station.properties.label, typically formatted as '{station code} - {municipality}' such as '40AL02 - Beveren'. This is the display name published by IRCELINE for the monitoring site. | altnames=`{"irceline": "properties.label"}` | - | - |
| `latitude` | `double` | `True` | Station latitude in decimal degrees north, derived from the second element of station.geometry.coordinates in the upstream GeoJSON Point geometry. The upstream array follows GeoJSON order [longitude, latitude, elevation]. | unit=`deg` symbol=`°`<br>altnames=`{"irceline": "geometry.coordinates[1]"}` | - | - |
| `longitude` | `double` | `True` | Station longitude in decimal degrees east, derived from the first element of station.geometry.coordinates in the upstream GeoJSON Point geometry. The third element is the literal string 'NaN' in live payloads and is ignored. | unit=`deg` symbol=`°`<br>altnames=`{"irceline": "geometry.coordinates[0]"}` | - | - |

#### Schema `be.irceline.Timeseries`
<a id="schema-beircelinetimeseries"></a>

| Field | Value |
| --- | --- |
| Name | Timeseries |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Reference event for one IRCELINE station-timeseries combination from GET /timeseries?expanded=true. The record identifies the monitored phenomenon, unit of measurement, linked station metadata, and optional BelAQI-style status interval bands published by IRCELINE. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://geo.irceline.be/schemas/be/irceline/Timeseries` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `Timeseries`
<a id="schema-node-timeseries"></a>

Reference data for a single IRCELINE timeseries from GET /timeseries or GET /timeseries/{id}?expanded=true. Each timeseries combines a stable numeric timeseries identifier with a station, a phenomenon/category pair, the published unit of measurement, and optional statusIntervals that describe threshold bands used by IRCELINE for display and air-quality interpretation.

| Field | Value |
| --- | --- |
| $id | `https://geo.irceline.be/schemas/be/irceline/Timeseries` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `timeseries_id` | `string` | `True` | Stable numeric identifier of the IRCELINE timeseries from the root id property on GET /timeseries results. The bridge converts the upstream value to a string because this identifier is the Kafka key and CloudEvents subject for both reference and observation events. | altnames=`{"irceline": "id"}` | pattern=`^[0-9]+$` | - |
| `label` | `string` | `True` | Descriptive timeseries label from the upstream label property, combining phenomenon name, timeseries identifier, procedure label, and station label. Example: 'Particulate Matter < 10 µm 6152 - DAILY CORRECTION TEOM - procedure, 40AL01 - Linkeroever'. | altnames=`{"irceline": "label"}` | - | - |
| `uom` | `string` | `True` | Published unit of measurement from the upstream uom property, such as 'µg/m³'. IRCELINE returns this literal display unit on both collection and expanded timeseries responses. | altnames=`{"irceline": "uom"}` | - | - |
| `station_id` | `string` | `True` | Numeric station identifier linked to the timeseries, mapped from station.properties.id on the embedded station feature. This is the stable identifier of the monitoring site that hosts the timeseries. | altnames=`{"irceline": "station.properties.id"}` | pattern=`^[0-9]+$` | - |
| `station_label` | `string` | `True` | Human-readable station label linked to the timeseries, mapped from station.properties.label on the embedded station feature. | altnames=`{"irceline": "station.properties.label"}` | - | - |
| `latitude` | `union` | `False` | Station latitude in decimal degrees north, derived from station.geometry.coordinates[1] when the embedded station feature includes a GeoJSON Point geometry. | unit=`deg` symbol=`°`<br>altnames=`{"irceline": "station.geometry.coordinates[1]"}` | - | - |
| `longitude` | `union` | `False` | Station longitude in decimal degrees east, derived from station.geometry.coordinates[0] when the embedded station feature includes a GeoJSON Point geometry. | unit=`deg` symbol=`°`<br>altnames=`{"irceline": "station.geometry.coordinates[0]"}` | - | - |
| `phenomenon_id` | `union` | `False` | Identifier of the measured phenomenon from parameters.phenomenon.id on expanded timeseries metadata, for example '5' for particulate matter under 10 micrometers. | altnames=`{"irceline": "parameters.phenomenon.id"}` | - | - |
| `phenomenon_label` | `union` | `False` | Human-readable phenomenon label from parameters.phenomenon.label on expanded timeseries metadata, for example 'Nitrogen dioxide' or 'Ozone'. | altnames=`{"irceline": "parameters.phenomenon.label"}` | - | - |
| `category_id` | `union` | `False` | Identifier of the IRCELINE category linked to the timeseries from parameters.category.id. In the live API this currently mirrors the phenomenon identifier for air-quality pollutants. | altnames=`{"irceline": "parameters.category.id"}` | - | - |
| `category_label` | `union` | `False` | Human-readable IRCELINE category label from parameters.category.label. In the live API this currently mirrors the phenomenon label for air-quality pollutants. | altnames=`{"irceline": "parameters.category.label"}` | - | - |
| `status_intervals` | `union` | `False` | Optional ordered array of status interval bands from the upstream statusIntervals expansion. Each entry describes a lower and upper threshold, a display label, and a color used by IRCELINE for BelAQI-style interpretation of the timeseries values. | altnames=`{"irceline": "statusIntervals"}` | - | - |

#### Schema `be.irceline.Observation`
<a id="schema-beircelineobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |
| Description | Telemetry event for one measurement value from GET /timeseries/{id}/getData. The bridge polls the last two hours of data per timeseries and emits only observations with timestamps newer than the persisted per-timeseries dedup state. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://geo.irceline.be/schemas/be/irceline/Observation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |
| Additional properties | `False` |

###### Object `Observation`
<a id="schema-node-observation"></a>

Telemetry measurement for a single IRCELINE timeseries from GET /timeseries/{id}/getData. The upstream payload returns Unix timestamps in milliseconds and numeric values that may be null; the bridge converts the timestamp to an ISO 8601 UTC string and carries the unit from the timeseries metadata.

| Field | Value |
| --- | --- |
| $id | `https://geo.irceline.be/schemas/be/irceline/Observation` |
| Additional properties | `False` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `timeseries_id` | `string` | `True` | Stable numeric timeseries identifier of the measurement source. This is copied from the parent timeseries metadata and matches the CloudEvents subject and Kafka key. | altnames=`{"irceline": "id"}` | pattern=`^[0-9]+$` | - |
| `timestamp` | `string` | `True` | Observation timestamp in ISO 8601 UTC form produced by converting the upstream Unix millisecond timestamp from values[].timestamp, for example '2025-04-08T09:00:00Z'. | altnames=`{"irceline": "values.timestamp"}` | pattern=`^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{3})?Z$` | - |
| `value` | `union` | `False` | Measured numeric value from values[].value. IRCELINE can publish null when a data point exists without a numeric value, so the schema explicitly allows null. | altnames=`{"irceline": "values.value"}` | - | - |
| `uom` | `string` | `True` | Unit of measurement carried over from the parent timeseries uom field, such as 'µg/m³'. This keeps each observation self-describing without requiring a separate metadata lookup. | altnames=`{"irceline": "uom"}` | - | - |

### Schemagroup `be.irceline.avro`
<a id="schemagroup-beircelineavro"></a>

#### Schema `be.irceline.Station`
<a id="schema-beircelinestation"></a>

| Field | Value |
| --- | --- |
| Name | Station |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Reference event for one IRCELINE monitoring station. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | be.irceline |
| Type | `record` |
| Doc | Reference event for one IRCELINE monitoring station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Stable numeric station identifier from properties.id. | `-` |
| `label` | `string` | Human-readable station label from properties.label. | `-` |
| `latitude` | `double` | Latitude in decimal degrees north from GeoJSON coordinates[1]. | `-` |
| `longitude` | `double` | Longitude in decimal degrees east from GeoJSON coordinates[0]. | `-` |

#### Schema `be.irceline.Timeseries`
<a id="schema-beircelinetimeseries"></a>

| Field | Value |
| --- | --- |
| Name | Timeseries |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Reference event for one IRCELINE station-timeseries combination. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Timeseries |
| Namespace | be.irceline |
| Type | `record` |
| Doc | Reference event for one IRCELINE station-timeseries combination. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `timeseries_id` | `string` | Stable numeric timeseries identifier from id. | `-` |
| `label` | `string` | Descriptive upstream timeseries label. | `-` |
| `uom` | `string` | Published unit of measurement. | `-` |
| `station_id` | `string` | Linked numeric station identifier from station.properties.id. | `-` |
| `station_label` | `string` | Linked station label from station.properties.label. | `-` |
| `latitude` | `null` \| `double` | Linked station latitude from station.geometry.coordinates[1]. | `-` |
| `longitude` | `null` \| `double` | Linked station longitude from station.geometry.coordinates[0]. | `-` |
| `phenomenon_id` | `null` \| `string` | Measured phenomenon identifier from parameters.phenomenon.id. | `-` |
| `phenomenon_label` | `null` \| `string` | Measured phenomenon label from parameters.phenomenon.label. | `-` |
| `category_id` | `null` \| `string` | Category identifier from parameters.category.id. | `-` |
| `category_label` | `null` \| `string` | Category label from parameters.category.label. | `-` |
| `status_intervals` | `null` \| array of record `StatusInterval` | Optional ordered array of status interval bands from the expanded timeseries metadata. | `-` |

#### Schema `be.irceline.Observation`
<a id="schema-beircelineobservation"></a>

| Field | Value |
| --- | --- |
| Name | Observation |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Telemetry event for one IRCELINE measurement value. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Observation |
| Namespace | be.irceline |
| Type | `record` |
| Doc | Telemetry event for one IRCELINE measurement value. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `timeseries_id` | `string` | Stable numeric timeseries identifier. | `-` |
| `timestamp` | `string` | Observation timestamp in ISO 8601 UTC form. | `-` |
| `value` | `null` \| `double` | Measured value from the IRCELINE getData response. | `-` |
| `uom` | `string` | Published unit of measurement copied from the parent timeseries. | `-` |
