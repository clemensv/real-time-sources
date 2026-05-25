# iRail Belgian Railway Bridge Events

MQTT/5.0 transport variants for iRail Belgian railway station metadata and live board snapshots. Topics are retained QoS-1 state leaves under transit/be/irail/irail/{station_id}/{event}. The station_id topic axis preserves the existing Kafka/CloudEvents subject. Use transit/be/irail/irail/{station_id}/# for one station, transit/be/irail/irail/+/station-board for all departure boards, and transit/be/irail/irail/+/arrival-board for all arrival boards. Board snapshots use message expiry so stale liveboards age out if polling stops.

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

### Endpoint `be.irail.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`be.irail`](#messagegroup-beirail) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `irail` |
| Kafka key | `{station_id}` |
| Deployed | False |

### Endpoint `be.irail.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`be.irail.mqtt`](#messagegroup-beirailmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `be.irail`
<a id="messagegroup-beirail"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `be.irail.Kafka` (KAFKA) |
| Messages | 3 |

#### Message `be.irail.Station`
<a id="message-beirailstation"></a>

Metadata for a Belgian railway station in the NMBS/SNCB network as provided by the iRail API. The Belgian rail network comprises approximately 600 passenger stations. Each station has a unique UIC-derived numeric identifier assigned by the NMBS, geographic coordinates, and multilingual names.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irail.jstruct/schemas/be.irail.Station`](#schema-beirailstation) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irail.Station` |
| `source` |  | `string` | `False` | `https://api.irail.be/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irail.Kafka` | `KAFKA` | topic `irail`; key `{station_id}` |

#### Message `be.irail.StationBoard`
<a id="message-beirailstationboard"></a>

A real-time departure board snapshot for a Belgian railway station from the iRail liveboard API. Contains all currently scheduled departures from the station with real-time delay information, platform assignments, cancellation status, and crowd-sourced occupancy levels. The board is polled periodically and each event replaces the previous board state for the same station.

| Field | Value |
| --- | --- |
| Name | StationBoard |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irail.jstruct/schemas/be.irail.StationBoard`](#schema-beirailstationboard) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irail.StationBoard` |
| `source` |  | `string` | `False` | `https://api.irail.be/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irail.Kafka` | `KAFKA` | topic `irail`; key `{station_id}` |

#### Message `be.irail.ArrivalBoard`
<a id="message-beirailarrivalboard"></a>

A real-time arrival board snapshot for a Belgian railway station from the iRail liveboard API. Contains all currently scheduled arrivals at the station with real-time delay information, platform assignments, cancellation status, and crowd-sourced occupancy levels. The board is polled periodically and each event replaces the previous arrival-board state for the same station.

| Field | Value |
| --- | --- |
| Name | ArrivalBoard |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irail.jstruct/schemas/be.irail.ArrivalBoard`](#schema-beirailarrivalboard) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irail.ArrivalBoard` |
| `source` |  | `string` | `False` | `https://api.irail.be/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irail.Kafka` | `KAFKA` | topic `irail`; key `{station_id}` |

### Messagegroup `be.irail.mqtt`
<a id="messagegroup-beirailmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for iRail Belgian railway station metadata and live board snapshots. Topics are retained QoS-1 state leaves under transit/be/irail/irail/{station_id}/{event}. The station_id topic axis preserves the existing Kafka/CloudEvents subject. Use transit/be/irail/irail/{station_id}/# for one station, transit/be/irail/irail/+/station-board for all departure boards, and transit/be/irail/irail/+/arrival-board for all arrival boards. Board snapshots use message expiry so stale liveboards age out if polling stops. |
| Transport bindings | `be.irail.Mqtt` (MQTT/5.0) |
| Messages | 3 |

#### Message `be.irail.mqtt.Station`
<a id="message-beirailmqttstation"></a>

Metadata for a Belgian railway station in the NMBS/SNCB network as provided by the iRail API. The Belgian rail network comprises approximately 600 passenger stations. Each station has a unique UIC-derived numeric identifier assigned by the NMBS, geographic coordinates, and multilingual names.

| Field | Value |
| --- | --- |
| Name | Station |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irail.jstruct/schemas/be.irail.Station`](#schema-beirailstation) |
| Base message chain | `/messagegroups/be.irail/messages/be.irail.Station` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irail.Station` |
| `source` |  | `string` | `False` | `https://api.irail.be/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irail.Mqtt` | `MQTT/5.0` | topic `transit/be/irail/irail/{station_id}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `transit/be/irail/irail/{station_id}/info` |
| QoS | 1 |
| Retain | True |

#### Message `be.irail.mqtt.StationBoard`
<a id="message-beirailmqttstationboard"></a>

A real-time departure board snapshot for a Belgian railway station from the iRail liveboard API. Contains all currently scheduled departures from the station with real-time delay information, platform assignments, cancellation status, and crowd-sourced occupancy levels. The board is polled periodically and each event replaces the previous board state for the same station.

| Field | Value |
| --- | --- |
| Name | StationBoard |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irail.jstruct/schemas/be.irail.StationBoard`](#schema-beirailstationboard) |
| Base message chain | `/messagegroups/be.irail/messages/be.irail.StationBoard` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irail.StationBoard` |
| `source` |  | `string` | `False` | `https://api.irail.be/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irail.Mqtt` | `MQTT/5.0` | topic `transit/be/irail/irail/{station_id}/station-board` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `transit/be/irail/irail/{station_id}/station-board` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 900}` |

#### Message `be.irail.mqtt.ArrivalBoard`
<a id="message-beirailmqttarrivalboard"></a>

A real-time arrival board snapshot for a Belgian railway station from the iRail liveboard API. Contains all currently scheduled arrivals at the station with real-time delay information, platform assignments, cancellation status, and crowd-sourced occupancy levels. The board is polled periodically and each event replaces the previous arrival-board state for the same station.

| Field | Value |
| --- | --- |
| Name | ArrivalBoard |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/be.irail.jstruct/schemas/be.irail.ArrivalBoard`](#schema-beirailarrivalboard) |
| Base message chain | `/messagegroups/be.irail/messages/be.irail.ArrivalBoard` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `be.irail.ArrivalBoard` |
| `source` |  | `string` | `False` | `https://api.irail.be/` |
| `subject` |  | `uritemplate` | `False` | `{station_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `be.irail.Mqtt` | `MQTT/5.0` | topic `transit/be/irail/irail/{station_id}/arrival-board` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `transit/be/irail/irail/{station_id}/arrival-board` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 900}` |

## Schemagroups

### Schemagroup `be.irail.jstruct`
<a id="schemagroup-beirailjstruct"></a>

#### Schema `be.irail.Station`
<a id="schema-beirailstation"></a>

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
| $id | `https://real-time-sources.2030.io/schemas/be/irail/Station` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/be/irail/Station` |
| Type | `object` |

###### Object `Station`
<a id="schema-node-station"></a>

Metadata for a Belgian railway station in the NMBS/SNCB (Nationale Maatschappij der Belgische Spoorwegen / Société Nationale des Chemins de fer Belges) network. Station identifiers follow the UIC (Union Internationale des Chemins de fer) numbering scheme with a Belgian country prefix of 0088. The iRail API provides these as nine-digit codes prefixed with 'BE.NMBS.'.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Nine-digit UIC-derived numeric station identifier assigned by NMBS. Extracted from the iRail id field by stripping the 'BE.NMBS.' prefix. Example: '008814001' for Brussels-South (Bruxelles-Midi / Brussel-Zuid). | altnames=`{"json": "id"}` | - | - |
| `name` | `string` | `True` | Default display name of the station in the requested language. Example: 'Brussels-South'. | - | - | - |
| `standard_name` | `string` | `True` | Consistent official station name that does not vary by language, typically using the primary local name. Example: 'Bruxelles-Midi / Brussel-Zuid'. | altnames=`{"json": "standardname"}` | - | - |
| `longitude` | `double` | `True` | Longitude of the station in WGS84 decimal degrees. Sourced from the iRail locationX field. | unit=`deg` symbol=`°`<br>altnames=`{"json": "locationX"}` | - | - |
| `latitude` | `double` | `True` | Latitude of the station in WGS84 decimal degrees. Sourced from the iRail locationY field. | unit=`deg` symbol=`°`<br>altnames=`{"json": "locationY"}` | - | - |
| `uri` | `string` | `True` | Stable linked-data URI identifying this station in the iRail namespace. Example: 'http://irail.be/stations/NMBS/008814001'. | altnames=`{"json": "@id"}` | - | - |

#### Schema `be.irail.StationBoard`
<a id="schema-beirailstationboard"></a>

| Field | Value |
| --- | --- |
| Name | StationBoard |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/be/irail/StationBoard` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/be/irail/StationBoard` |
| Type | `object` |

###### Object `StationBoard`
<a id="schema-node-stationboard"></a>

Real-time departure board for a Belgian railway station. Contains all currently visible departures from the station as returned by the iRail liveboard API. The board reflects the current state of the departure display at the station, including delays, cancellations, and platform assignments. Typically shows the next 30-50 departures within a rolling time window.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Nine-digit UIC-derived numeric identifier of the station this board belongs to. Matches the station_id in the Station schema. | - | - | - |
| `station_name` | `string` | `True` | Display name of the station this board belongs to. | - | - | - |
| `retrieved_at` | `string` | `True` | ISO 8601 UTC timestamp when this board was retrieved from the iRail API. Converted from the iRail response timestamp field. | - | - | - |
| `departure_count` | `int32` | `True` | Number of departures in this board snapshot. Matches the length of the departures array. | - | - | - |
| `departures` | array of `schema` | `True` | Array of departure entries currently shown on the station's departure board. Each entry represents a train service scheduled to depart from this station, enriched with real-time delay and cancellation information. | - | - | - |

#### Schema `be.irail.ArrivalBoard`
<a id="schema-beirailarrivalboard"></a>

| Field | Value |
| --- | --- |
| Name | ArrivalBoard |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/be/irail/ArrivalBoard` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/be/irail/ArrivalBoard` |
| Type | `object` |

###### Object `ArrivalBoard`
<a id="schema-node-arrivalboard"></a>

Real-time arrival board for a Belgian railway station. Contains all currently visible arrivals at the station as returned by the iRail liveboard API with arrdep=arrival. The board reflects the current state of the arrival display at the station, including delays, cancellations, and platform assignments.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `station_id` | `string` | `True` | Nine-digit UIC-derived numeric identifier of the station this board belongs to. Matches the station_id in the Station schema. | - | - | - |
| `station_name` | `string` | `True` | Display name of the station this board belongs to. | - | - | - |
| `retrieved_at` | `string` | `True` | ISO 8601 UTC timestamp when this board was retrieved from the iRail API. Converted from the iRail response timestamp field. | - | - | - |
| `arrival_count` | `int32` | `True` | Number of arrivals in this board snapshot. Matches the length of the arrivals array. | - | - | - |
| `arrivals` | array of `schema` | `True` | Array of arrival entries currently shown on the station's arrival board. Each entry represents a train service scheduled to arrive at this station, enriched with real-time delay and cancellation information. | - | - | - |

### Schemagroup `be.irail.avro`
<a id="schemagroup-beirailavro"></a>

#### Schema `be.irail.Station`
<a id="schema-beirailstation"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | Station |
| Namespace | be.irail |
| Type | `record` |
| Doc | Metadata for a Belgian railway station in the NMBS/SNCB network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Nine-digit UIC-derived numeric station identifier assigned by NMBS. | `-` |
| `name` | `string` | Default display name of the station. | `-` |
| `standard_name` | `string` | Consistent official station name. | `-` |
| `longitude` | `double` | Longitude in WGS84 decimal degrees. | `-` |
| `latitude` | `double` | Latitude in WGS84 decimal degrees. | `-` |
| `uri` | `string` | Stable linked-data URI identifying this station. | `-` |

#### Schema `be.irail.StationBoard`
<a id="schema-beirailstationboard"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | StationBoard |
| Namespace | be.irail |
| Type | `record` |
| Doc | Real-time departure board for a Belgian railway station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Nine-digit UIC-derived numeric identifier of the station. | `-` |
| `station_name` | `string` | Display name of the station. | `-` |
| `retrieved_at` | `string` | ISO 8601 UTC timestamp when this board was retrieved. | `-` |
| `departure_count` | `int` | Number of departures in this board snapshot. | `-` |
| `departures` | array of record `Departure` | Array of departure entries on the station board. | `-` |

#### Schema `be.irail.ArrivalBoard`
<a id="schema-beirailarrivalboard"></a>

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | ArrivalBoard |
| Namespace | be.irail |
| Type | `record` |
| Doc | Real-time arrival board for a Belgian railway station. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `station_id` | `string` | Nine-digit UIC-derived numeric identifier of the station. | `-` |
| `station_name` | `string` | Display name of the station. | `-` |
| `retrieved_at` | `string` | ISO 8601 UTC timestamp when this board was retrieved. | `-` |
| `arrival_count` | `int` | Number of arrivals in this board snapshot. | `-` |
| `arrivals` | array of record `Arrival` | Array of arrival entries on the station board. | `-` |
