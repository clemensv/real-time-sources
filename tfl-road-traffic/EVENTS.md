# TfL Road Traffic Events

MQTT/5.0 binary CloudEvents for the TfL Road Traffic Unified Namespace. Roads are retained last-known-value topics; disruption severities are literal topic partitions.

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
| Schemagroups | 1 |

## Endpoints

### Endpoint `uk.gov.tfl.road.corridors.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`uk.gov.tfl.road.corridors`](#messagegroup-ukgovtflroadcorridors) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `tfl-road-traffic` |
| Kafka key | `roads/{road_id}` |
| Deployed | False |

### Endpoint `uk.gov.tfl.road.disruptions.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`uk.gov.tfl.road.disruptions`](#messagegroup-ukgovtflroaddisruptions) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `tfl-road-traffic` |
| Kafka key | `disruptions/{road_id}/{severity}/{disruption_id}` |
| Deployed | False |

### Endpoint `uk.gov.tfl.road.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`uk.gov.tfl.road.mqtt`](#messagegroup-ukgovtflroadmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `uk.gov.tfl.road.corridors`
<a id="messagegroup-ukgovtflroadcorridors"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `uk.gov.tfl.road.corridors.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `uk.gov.tfl.road.RoadCorridor`
<a id="message-ukgovtflroadroadcorridor"></a>

Reference record for a TfL managed road corridor fetched from GET /Road.

| Field | Value |
| --- | --- |
| Name | RoadCorridor |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadCorridor`](#schema-ukgovtflroadroadcorridor) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadCorridor` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road` |
| `subject` |  | `uritemplate` | `False` | `roads/{road_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.corridors.Kafka` | `KAFKA` | topic `tfl-road-traffic`; key `roads/{road_id}` |

#### Message `uk.gov.tfl.road.RoadStatus`
<a id="message-ukgovtflroadroadstatus"></a>

Real-time status snapshot for a TfL managed road corridor fetched from GET /Road/all/Status.

| Field | Value |
| --- | --- |
| Name | RoadStatus |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadStatus`](#schema-ukgovtflroadroadstatus) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadStatus` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Status` |
| `subject` |  | `uritemplate` | `False` | `roads/{road_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.corridors.Kafka` | `KAFKA` | topic `tfl-road-traffic`; key `roads/{road_id}` |

### Messagegroup `uk.gov.tfl.road.disruptions`
<a id="messagegroup-ukgovtflroaddisruptions"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `uk.gov.tfl.road.disruptions.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `uk.gov.tfl.road.RoadDisruption`
<a id="message-ukgovtflroadroaddisruption"></a>

Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.

| Field | Value |
| --- | --- |
| Name | RoadDisruption |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadDisruption`](#schema-ukgovtflroadroaddisruption) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.disruptions.Kafka` | `KAFKA` | topic `tfl-road-traffic`; key `disruptions/{road_id}/{severity}/{disruption_id}` |

### Messagegroup `uk.gov.tfl.road.mqtt`
<a id="messagegroup-ukgovtflroadmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 binary CloudEvents for the TfL Road Traffic Unified Namespace. Roads are retained last-known-value topics; disruption severities are literal topic partitions. |
| Transport bindings | `uk.gov.tfl.road.Mqtt` (MQTT/5.0) |
| Messages | 8 |

#### Message `uk.gov.tfl.road.mqtt.RoadCorridor`
<a id="message-ukgovtflroadmqttroadcorridor"></a>

Reference record for a TfL managed road corridor fetched from GET /Road.

| Field | Value |
| --- | --- |
| Name | RoadCorridor |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadCorridor`](#schema-ukgovtflroadroadcorridor) |
| Base message chain | `/messagegroups/uk.gov.tfl.road.corridors/messages/uk.gov.tfl.road.RoadCorridor` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadCorridor` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road` |
| `subject` |  | `uritemplate` | `False` | `roads/{road_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.Mqtt` | `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/corridor` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/corridor` |
| QoS | 1 |
| Retain | True |

#### Message `uk.gov.tfl.road.mqtt.RoadStatus`
<a id="message-ukgovtflroadmqttroadstatus"></a>

Real-time status snapshot for a TfL managed road corridor fetched from GET /Road/all/Status.

| Field | Value |
| --- | --- |
| Name | RoadStatus |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadStatus`](#schema-ukgovtflroadroadstatus) |
| Base message chain | `/messagegroups/uk.gov.tfl.road.corridors/messages/uk.gov.tfl.road.RoadStatus` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadStatus` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Status` |
| `subject` |  | `uritemplate` | `False` | `roads/{road_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.Mqtt` | `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/status` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/gb/tfl/tfl-road-traffic/roads/{road_id}/status` |
| QoS | 1 |
| Retain | True |

#### Message `uk.gov.tfl.road.mqtt.RoadDisruptionSerious`
<a id="message-ukgovtflroadmqttroaddisruptionserious"></a>

Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.

| Field | Value |
| --- | --- |
| Name | RoadDisruptionSerious |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadDisruption`](#schema-ukgovtflroadroaddisruption) |
| Base message chain | `/messagegroups/uk.gov.tfl.road.disruptions/messages/uk.gov.tfl.road.RoadDisruption` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.Mqtt` | `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/serious/{disruption_id}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/serious/{disruption_id}` |
| QoS | 1 |
| Retain | False |

#### Message `uk.gov.tfl.road.mqtt.RoadDisruptionSevere`
<a id="message-ukgovtflroadmqttroaddisruptionsevere"></a>

Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.

| Field | Value |
| --- | --- |
| Name | RoadDisruptionSevere |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadDisruption`](#schema-ukgovtflroadroaddisruption) |
| Base message chain | `/messagegroups/uk.gov.tfl.road.disruptions/messages/uk.gov.tfl.road.RoadDisruption` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.Mqtt` | `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/severe/{disruption_id}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/severe/{disruption_id}` |
| QoS | 1 |
| Retain | False |

#### Message `uk.gov.tfl.road.mqtt.RoadDisruptionModerate`
<a id="message-ukgovtflroadmqttroaddisruptionmoderate"></a>

Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.

| Field | Value |
| --- | --- |
| Name | RoadDisruptionModerate |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadDisruption`](#schema-ukgovtflroadroaddisruption) |
| Base message chain | `/messagegroups/uk.gov.tfl.road.disruptions/messages/uk.gov.tfl.road.RoadDisruption` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.Mqtt` | `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/moderate/{disruption_id}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/moderate/{disruption_id}` |
| QoS | 1 |
| Retain | False |

#### Message `uk.gov.tfl.road.mqtt.RoadDisruptionMinor`
<a id="message-ukgovtflroadmqttroaddisruptionminor"></a>

Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.

| Field | Value |
| --- | --- |
| Name | RoadDisruptionMinor |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadDisruption`](#schema-ukgovtflroadroaddisruption) |
| Base message chain | `/messagegroups/uk.gov.tfl.road.disruptions/messages/uk.gov.tfl.road.RoadDisruption` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.Mqtt` | `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/minor/{disruption_id}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/minor/{disruption_id}` |
| QoS | 1 |
| Retain | False |

#### Message `uk.gov.tfl.road.mqtt.RoadDisruptionInformation`
<a id="message-ukgovtflroadmqttroaddisruptioninformation"></a>

Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.

| Field | Value |
| --- | --- |
| Name | RoadDisruptionInformation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadDisruption`](#schema-ukgovtflroadroaddisruption) |
| Base message chain | `/messagegroups/uk.gov.tfl.road.disruptions/messages/uk.gov.tfl.road.RoadDisruption` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.Mqtt` | `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/information/{disruption_id}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/information/{disruption_id}` |
| QoS | 1 |
| Retain | False |

#### Message `uk.gov.tfl.road.mqtt.RoadDisruptionClosure`
<a id="message-ukgovtflroadmqttroaddisruptionclosure"></a>

Real-time road disruption event on the TfL road network fetched from GET /Road/all/Disruption.

| Field | Value |
| --- | --- |
| Name | RoadDisruptionClosure |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/uk.gov.tfl.road.jstruct/schemas/uk.gov.tfl.road.RoadDisruption`](#schema-ukgovtflroadroaddisruption) |
| Base message chain | `/messagegroups/uk.gov.tfl.road.disruptions/messages/uk.gov.tfl.road.RoadDisruption` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `uk.gov.tfl.road.RoadDisruption` |
| `source` |  | `string` | `False` | `https://api.tfl.gov.uk/Road/all/Disruption` |
| `subject` |  | `uritemplate` | `False` | `disruptions/{road_id}/{severity}/{disruption_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `uk.gov.tfl.road.Mqtt` | `MQTT/5.0` | topic `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/closure/{disruption_id}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/gb/tfl/tfl-road-traffic/disruptions/{road_id}/closure/{disruption_id}` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `uk.gov.tfl.road.jstruct`
<a id="schemagroup-ukgovtflroadjstruct"></a>

#### Schema `uk.gov.tfl.road.RoadCorridor`
<a id="schema-ukgovtflroadroadcorridor"></a>

| Field | Value |
| --- | --- |
| Name | RoadCorridor |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.tfl.gov.uk/schemas/uk/gov/tfl/road/RoadCorridor` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `RoadCorridor`
<a id="schema-node-roadcorridor"></a>

Reference record for a Transport for London (TfL) managed road corridor. Fetched from the GET /Road endpoint at bridge startup and refreshed periodically. Each corridor is a named road segment under TfL operational control, such as the A2, A12, or M25, with its current aggregate traffic status.

| Field | Value |
| --- | --- |
| $id | `https://api.tfl.gov.uk/schemas/uk/gov/tfl/road/RoadCorridor` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `road_id` | `string` | `True` | Unique identifier for the road corridor as used by the TfL Unified API. Corresponds to 'id' in the upstream response. Examples: 'a2', 'a12', 'm25'. Used as the stable domain key. | altnames=`{"upstream": "id"}` | - | - |
| `display_name` | `string` | `True` | Human-readable display name for the road corridor as reported by TfL. Corresponds to 'displayName' in the upstream response. Examples: 'A2', 'A12', 'M25'. | altnames=`{"upstream": "displayName"}` | - | - |
| `status_severity` | `union` | `False` | Current aggregate status severity for this corridor as assessed by TfL. Corresponds to 'statusSeverity' in the upstream response. Common values: 'Good', 'Moderate', 'Serious', 'Severe', 'NoDisruptions'. | altnames=`{"upstream": "statusSeverity"}` | - | - |
| `status_severity_description` | `union` | `False` | Human-readable description of the current status severity. Corresponds to 'statusSeverityDescription' in the upstream response. Example: 'Serious Delays'. | altnames=`{"upstream": "statusSeverityDescription"}` | - | - |
| `bounds` | `union` | `False` | Bounding box for the road corridor as a JSON array string. Corresponds to 'bounds' in the upstream response. Format: '[[lon_sw,lat_sw],[lon_ne,lat_ne]]' in WGS84 decimal degrees. | - | - | - |
| `envelope` | `union` | `False` | GeoJSON envelope polygon for the road corridor geometry. Corresponds to 'envelope' in the upstream response. | - | - | - |
| `url` | `union` | `False` | URL to the TfL Unified API detail page for this corridor. Corresponds to 'url' in the upstream response. | - | - | - |
| `status_aggregation_start_date` | `union` | `False` | Start date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationStartDate' in the upstream response. | altnames=`{"upstream": "statusAggregationStartDate"}` | - | - |
| `status_aggregation_end_date` | `union` | `False` | End date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationEndDate' in the upstream response. | altnames=`{"upstream": "statusAggregationEndDate"}` | - | - |

#### Schema `uk.gov.tfl.road.RoadStatus`
<a id="schema-ukgovtflroadroadstatus"></a>

| Field | Value |
| --- | --- |
| Name | RoadStatus |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.tfl.gov.uk/schemas/uk/gov/tfl/road/RoadStatus` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `RoadStatus`
<a id="schema-node-roadstatus"></a>

Real-time status snapshot for a Transport for London (TfL) managed road corridor. Fetched from the GET /Road/all/Status endpoint on each polling cycle. Each event represents the current aggregate traffic status for one corridor as computed by TfL from active disruptions.

| Field | Value |
| --- | --- |
| $id | `https://api.tfl.gov.uk/schemas/uk/gov/tfl/road/RoadStatus` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `road_id` | `string` | `True` | Unique identifier for the road corridor as used by the TfL Unified API. Corresponds to 'id' in the upstream response. Examples: 'a2', 'a12', 'm25'. Used as the stable domain key. | altnames=`{"upstream": "id"}` | - | - |
| `display_name` | `string` | `True` | Human-readable display name for the road corridor as reported by TfL. Corresponds to 'displayName' in the upstream response. Examples: 'A2', 'A12', 'M25'. | altnames=`{"upstream": "displayName"}` | - | - |
| `status_severity` | `union` | `False` | Current aggregate status severity for this corridor as assessed by TfL. Corresponds to 'statusSeverity' in the upstream response. Common values: 'Good', 'Moderate', 'Serious', 'Severe', 'NoDisruptions'. | altnames=`{"upstream": "statusSeverity"}` | - | - |
| `status_severity_description` | `union` | `False` | Human-readable description of the current status severity. Corresponds to 'statusSeverityDescription' in the upstream response. Example: 'Serious Delays'. | altnames=`{"upstream": "statusSeverityDescription"}` | - | - |
| `bounds` | `union` | `False` | Bounding box for the road corridor as a JSON array string. Corresponds to 'bounds' in the upstream response. Format: '[[lon_sw,lat_sw],[lon_ne,lat_ne]]' in WGS84 decimal degrees. | - | - | - |
| `envelope` | `union` | `False` | GeoJSON envelope polygon for the road corridor geometry. Corresponds to 'envelope' in the upstream response. | - | - | - |
| `url` | `union` | `False` | URL to the TfL Unified API detail page for this corridor. Corresponds to 'url' in the upstream response. | - | - | - |
| `status_aggregation_start_date` | `union` | `False` | Start date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationStartDate' in the upstream response. | altnames=`{"upstream": "statusAggregationStartDate"}` | - | - |
| `status_aggregation_end_date` | `union` | `False` | End date of the current status aggregation period reported by TfL. Corresponds to 'statusAggregationEndDate' in the upstream response. | altnames=`{"upstream": "statusAggregationEndDate"}` | - | - |

#### Schema `uk.gov.tfl.road.RoadDisruption`
<a id="schema-ukgovtflroadroaddisruption"></a>

| Field | Value |
| --- | --- |
| Name | RoadDisruption |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://api.tfl.gov.uk/schemas/uk/gov/tfl/road/RoadDisruption` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `RoadDisruption`
<a id="schema-node-roaddisruption"></a>

Real-time road disruption event on the Transport for London (TfL) road network. Fetched from the GET /Road/all/Disruption endpoint. Each disruption represents an active incident, planned works, or road closure affecting one or more roads in London. Disruption records are deduped by ID and lastModifiedTime so only changed records are re-emitted.

| Field | Value |
| --- | --- |
| $id | `https://api.tfl.gov.uk/schemas/uk/gov/tfl/road/RoadDisruption` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `road_id` | `string` | `True` | Primary affected TfL road corridor identifier used by MQTT/UNS topics. Derived from the first upstream corridorIds entry when present, otherwise 'unknown'. | - | - | - |
| `disruption_id` | `string` | `True` | Unique identifier for the disruption assigned by the TfL Traffic Information Management System (TIMS). Corresponds to 'id' in the upstream response. Format: 'TIMS-NNNNN' or similar TIMS prefix. | altnames=`{"upstream": "id"}` | - | - |
| `category` | `union` | `False` | Top-level category of the disruption. Corresponds to 'category' in the upstream response. Common values: 'RealTime' for live incidents, 'PlannedWork' for scheduled roadworks. | - | - | - |
| `sub_category` | `union` | `False` | More detailed sub-category of the disruption. Corresponds to 'subCategory' in the upstream response. Examples: 'TfL planned works', 'Utility works', 'Incident', 'Traffic signal failure'. | altnames=`{"upstream": "subCategory"}` | - | - |
| `severity` | `string` | `True` | Normalized TfL-native severity for MQTT partitioning. Values: serious, severe, moderate, minor, information, closure. Upstream values are normalized to lowercase-kebab. | - | - | - |
| `ordinal` | `union` | `False` | Ordinal rank of this disruption used for ordering within a severity level. Corresponds to 'ordinal' in the upstream response. | - | - | - |
| `url` | `union` | `False` | URL to the TfL Unified API detail page for this disruption. Corresponds to 'url' in the upstream response. | - | - | - |
| `point` | `union` | `False` | Representative point location of the disruption as a WKT or coordinate string. Corresponds to 'point' in the upstream response. | - | - | - |
| `comments` | `union` | `False` | Free-text comments describing the disruption context. Corresponds to 'comments' in the upstream response. May include street names, junction descriptions, or operational notes. | - | - | - |
| `current_update` | `union` | `False` | Latest operational update text for this disruption. Corresponds to 'currentUpdate' in the upstream response. Updated by TfL operators as the situation evolves. | altnames=`{"upstream": "currentUpdate"}` | - | - |
| `current_update_datetime` | `union` | `False` | Timestamp when the current update text was last modified. Corresponds to 'currentUpdateDateTime' in the upstream response. | altnames=`{"upstream": "currentUpdateDateTime"}` | - | - |
| `corridor_ids` | `union` | `False` | Array of road corridor identifiers affected by this disruption. Corresponds to 'corridorIds' in the upstream response. Examples: ['a2', 'a12']. May be empty or null for disruptions not associated with a specific named corridor. | altnames=`{"upstream": "corridorIds"}` | - | - |
| `start_datetime` | `union` | `False` | Scheduled or actual start date and time of the disruption. Corresponds to 'startDateTime' in the upstream response. | altnames=`{"upstream": "startDateTime"}` | - | - |
| `end_datetime` | `union` | `False` | Scheduled or actual end date and time of the disruption. Corresponds to 'endDateTime' in the upstream response. May be null for open-ended incidents. | altnames=`{"upstream": "endDateTime"}` | - | - |
| `last_modified_time` | `union` | `False` | Timestamp when this disruption record was last modified in the TfL system. Corresponds to 'lastModifiedTime' in the upstream response. Used for deduplication: disruptions are re-emitted only when this value changes. | altnames=`{"upstream": "lastModifiedTime"}` | - | - |
| `level_of_interest` | `union` | `False` | TfL classification of the level of public interest for this disruption. Corresponds to 'levelOfInterest' in the upstream response. Examples: 'Low', 'Medium', 'High'. | altnames=`{"upstream": "levelOfInterest"}` | - | - |
| `location` | `union` | `False` | Free-text textual description of the disruption location. Corresponds to 'location' in the upstream response. | - | - | - |
| `is_provisional` | `union` | `False` | Whether the disruption timing or details are provisional and subject to change. Corresponds to 'isProvisional' in the upstream response. | altnames=`{"upstream": "isProvisional"}` | - | - |
| `has_closures` | `union` | `False` | Whether this disruption includes full or partial road closures. Corresponds to 'hasClosures' in the upstream response. | altnames=`{"upstream": "hasClosures"}` | - | - |
| `streets` | `union` | `False` | Array of street segments affected by this disruption. Corresponds to 'streets' in the upstream response. Each entry describes an individual street with its closure type, affected directions, and geometry. | - | - | - |
| `geography` | `union` | `False` | GeoJSON geometry of the disruption area as a JSON string. Corresponds to 'geography' in the upstream response. May be a Point, LineString, or Polygon representing the spatial extent of the disruption. | - | - | - |
| `geometry` | `union` | `False` | Secondary geometry field from the TfL database as a JSON string. Corresponds to 'geometry' in the upstream response. May contain database geometry in an alternate representation. | - | - | - |
| `status` | `union` | `False` | Current lifecycle status of the disruption. Corresponds to 'status' in the upstream response. | - | - | - |
| `is_active` | `union` | `False` | Whether this disruption is currently active. Corresponds to 'isActive' in the upstream response. | altnames=`{"upstream": "isActive"}` | - | - |
