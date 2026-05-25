# VATSIM Live Data Feed Bridge Events

MQTT/5.0 transport variant for VATSIM live network data. Non-retained QoS-1 streams split pilots, controllers, and network facility status into distinct UNS topic branches under aviation-network/intl/vatsim/vatsim/...

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
| Schemagroups | 2 |

## Endpoints

### Endpoint `net.vatsim.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`net.vatsim.pilots`](#messagegroup-netvatsimpilots) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `vatsim` |
| Kafka key | `{callsign}` |
| Deployed | False |

### Endpoint `net.vatsim.controllers.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`net.vatsim.controllers`](#messagegroup-netvatsimcontrollers) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `vatsim` |
| Kafka key | `{callsign}` |
| Deployed | False |

### Endpoint `net.vatsim.status.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`net.vatsim.status`](#messagegroup-netvatsimstatus) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `vatsim` |
| Kafka key | `{callsign}` |
| Deployed | False |

### Endpoint `net.vatsim.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`net.vatsim.mqtt`](#messagegroup-netvatsimmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `net.vatsim.pilots`
<a id="messagegroup-netvatsimpilots"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `net.vatsim.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `net.vatsim.PilotPosition`
<a id="message-netvatsimpilotposition"></a>

Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network.

| Field | Value |
| --- | --- |
| Name | PilotPosition |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/net.vatsim.jstruct/schemas/net.vatsim.PilotPosition`](#schema-netvatsimpilotposition) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `net.vatsim.PilotPosition` |
| `source` |  | `string` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `net.vatsim.Kafka` | `KAFKA` | topic `vatsim`; key `{callsign}` |

### Messagegroup `net.vatsim.controllers`
<a id="messagegroup-netvatsimcontrollers"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `net.vatsim.controllers.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `net.vatsim.ControllerPosition`
<a id="message-netvatsimcontrollerposition"></a>

Current state and frequency of an air traffic controller connected to the VATSIM virtual aviation network.

| Field | Value |
| --- | --- |
| Name | ControllerPosition |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/net.vatsim.jstruct/schemas/net.vatsim.ControllerPosition`](#schema-netvatsimcontrollerposition) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `net.vatsim.ControllerPosition` |
| `source` |  | `string` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `net.vatsim.controllers.Kafka` | `KAFKA` | topic `vatsim`; key `{callsign}` |

### Messagegroup `net.vatsim.status`
<a id="messagegroup-netvatsimstatus"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `net.vatsim.status.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `net.vatsim.NetworkStatus`
<a id="message-netvatsimnetworkstatus"></a>

Aggregate network status snapshot from the VATSIM data feed, emitted once per poll cycle.

| Field | Value |
| --- | --- |
| Name | NetworkStatus |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/net.vatsim.jstruct/schemas/net.vatsim.NetworkStatus`](#schema-netvatsimnetworkstatus) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `net.vatsim.NetworkStatus` |
| `source` |  | `string` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `net.vatsim.status.Kafka` | `KAFKA` | topic `vatsim`; key `{callsign}` |

### Messagegroup `net.vatsim.mqtt`
<a id="messagegroup-netvatsimmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for VATSIM live network data. Non-retained QoS-1 streams split pilots, controllers, and network facility status into distinct UNS topic branches under aviation-network/intl/vatsim/vatsim/... |
| Transport bindings | `net.vatsim.Mqtt` (MQTT/5.0) |
| Messages | 3 |

#### Message `net.vatsim.mqtt.PilotPosition`
<a id="message-netvatsimmqttpilotposition"></a>

Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network.

| Field | Value |
| --- | --- |
| Name | PilotPosition |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/net.vatsim.jstruct/schemas/net.vatsim.PilotPosition`](#schema-netvatsimpilotposition) |
| Base message chain | `/messagegroups/net.vatsim.pilots/messages/net.vatsim.PilotPosition` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `net.vatsim.PilotPosition` |
| `source` |  | `string` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `net.vatsim.Mqtt` | `MQTT/5.0` | topic `aviation-network/intl/vatsim/vatsim/pilots/{callsign}/pilot-position` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `aviation-network/intl/vatsim/vatsim/pilots/{callsign}/pilot-position` |
| QoS | 1 |
| Retain | False |

#### Message `net.vatsim.mqtt.ControllerPosition`
<a id="message-netvatsimmqttcontrollerposition"></a>

Current state and frequency of an air traffic controller connected to the VATSIM virtual aviation network.

| Field | Value |
| --- | --- |
| Name | ControllerPosition |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/net.vatsim.jstruct/schemas/net.vatsim.ControllerPosition`](#schema-netvatsimcontrollerposition) |
| Base message chain | `/messagegroups/net.vatsim.controllers/messages/net.vatsim.ControllerPosition` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `net.vatsim.ControllerPosition` |
| `source` |  | `string` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `net.vatsim.Mqtt` | `MQTT/5.0` | topic `aviation-network/intl/vatsim/vatsim/controllers/{callsign}/controller-position` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `aviation-network/intl/vatsim/vatsim/controllers/{callsign}/controller-position` |
| QoS | 1 |
| Retain | False |

#### Message `net.vatsim.mqtt.FacilityStatus`
<a id="message-netvatsimmqttfacilitystatus"></a>

Aggregate network status snapshot from the VATSIM data feed, emitted once per poll cycle.

| Field | Value |
| --- | --- |
| Name | FacilityStatus |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/net.vatsim.jstruct/schemas/net.vatsim.NetworkStatus`](#schema-netvatsimnetworkstatus) |
| Base message chain | `/messagegroups/net.vatsim.status/messages/net.vatsim.NetworkStatus` |
| Transport override | `MQTT/5.0` |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `net.vatsim.NetworkStatus` |
| `source` |  | `string` | `False` | `https://data.vatsim.net/v3/vatsim-data.json` |
| `subject` |  | `uritemplate` | `False` | `{callsign}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `net.vatsim.Mqtt` | `MQTT/5.0` | topic `aviation-network/intl/vatsim/vatsim/facilities/{facility}/facility-status` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `aviation-network/intl/vatsim/vatsim/facilities/{facility}/facility-status` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `net.vatsim.jstruct`
<a id="schemagroup-netvatsimjstruct"></a>

#### Schema `net.vatsim.PilotPosition`
<a id="schema-netvatsimpilotposition"></a>

| Field | Value |
| --- | --- |
| Name | PilotPosition |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/net/vatsim/PilotPosition` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/net/vatsim/PilotPosition` |
| Type | `object` |

###### Object `PilotPosition`
<a id="schema-node-pilotposition"></a>

Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network. Updated every 15 seconds at the source.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `cid` | `int32` | `True` | VATSIM Certificate Identifier (CID) — unique numeric member ID. | - | - | - |
| `callsign` | `string` | `True` | ATC-style callsign chosen by the pilot for this session (e.g. 'BAW123', 'N12345'). | - | - | - |
| `latitude` | `double` | `True` | Aircraft latitude in decimal degrees (WGS-84). Positive is north. | unit=`degree` symbol=`°` | - | - |
| `longitude` | `double` | `True` | Aircraft longitude in decimal degrees (WGS-84). Positive is east. | unit=`degree` symbol=`°` | - | - |
| `altitude` | `int32` | `True` | Indicated altitude of the aircraft in feet above mean sea level. | unit=`foot` symbol=`ft` | - | - |
| `groundspeed` | `int32` | `True` | Ground speed of the aircraft in knots. | unit=`knot` symbol=`kn` | - | - |
| `heading` | `int32` | `True` | Magnetic heading of the aircraft in degrees (0-359). | unit=`degree` symbol=`°` | - | - |
| `transponder` | `string` | `True` | Four-digit transponder (squawk) code currently set by the pilot. | - | - | - |
| `qnh_mb` | `int32` | `True` | Altimeter setting (QNH) in millibars / hectopascals as reported by the pilot client. | unit=`millibar` symbol=`mb` | - | - |
| `flight_rules` | `union` | `False` | Flight rules filed in the flight plan: 'I' for Instrument Flight Rules, 'V' for Visual Flight Rules. Null if no flight plan is filed. | - | - | - |
| `aircraft_short` | `union` | `False` | ICAO aircraft type designator from the filed flight plan (e.g. 'B738', 'A320'). Null if no flight plan is filed. | - | - | - |
| `departure` | `union` | `False` | ICAO code of the departure airport from the filed flight plan. Null if no flight plan is filed. | - | - | - |
| `arrival` | `union` | `False` | ICAO code of the arrival airport from the filed flight plan. Null if no flight plan is filed. | - | - | - |
| `route` | `union` | `False` | Route string from the filed flight plan. Null if no flight plan is filed. | - | - | - |
| `cruise_altitude` | `union` | `False` | Planned cruise altitude or flight level from the filed flight plan (e.g. '36000' or 'FL350'). Null if no flight plan is filed. | - | - | - |
| `pilot_rating` | `int32` | `True` | VATSIM pilot rating bitmask. 0 = New Member (P0), 1 = PPL, 3 = IR, 7 = CMEL, 15 = ATPL. | - | - | - |
| `last_updated` | `string` | `True` | UTC timestamp of the last position update received by the VATSIM data servers (RFC3339 string). | - | - | - |

#### Schema `net.vatsim.ControllerPosition`
<a id="schema-netvatsimcontrollerposition"></a>

| Field | Value |
| --- | --- |
| Name | ControllerPosition |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/net/vatsim/ControllerPosition` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/net/vatsim/ControllerPosition` |
| Type | `object` |

###### Object `ControllerPosition`
<a id="schema-node-controllerposition"></a>

Current state and frequency of an air traffic controller or observer connected to the VATSIM virtual aviation network.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `cid` | `int32` | `True` | VATSIM Certificate Identifier (CID) — unique numeric member ID. | - | - | - |
| `callsign` | `string` | `True` | Controller position callsign (e.g. 'EGLL_TWR', 'KJFK_APP'). | - | - | - |
| `frequency` | `string` | `True` | Radio frequency the controller is operating on, in MHz with three decimal places (e.g. '118.500'). | - | - | - |
| `facility` | `int32` | `True` | VATSIM facility type code. 0 = Observer, 1 = Flight Service Station, 2 = Delivery, 3 = Ground, 4 = Tower, 5 = Approach/Departure, 6 = Center/Enroute. | - | - | - |
| `rating` | `int32` | `True` | VATSIM ATC rating. 1 = OBS, 2 = S1, 3 = S2, 4 = S3, 5 = C1, 6 = C2, 7 = C3, 8 = I1, 9 = I2, 10 = I3, 11 = SUP, 12 = ADM. | - | - | - |
| `text_atis` | `union` | `False` | Controller information or ATIS text, with individual lines joined by newline characters. Null when the controller has not set any ATIS text. | - | - | - |
| `last_updated` | `string` | `True` | UTC timestamp of the last update received by the VATSIM data servers (RFC3339 string). | - | - | - |

#### Schema `net.vatsim.NetworkStatus`
<a id="schema-netvatsimnetworkstatus"></a>

| Field | Value |
| --- | --- |
| Name | NetworkStatus |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/net/vatsim/NetworkStatus` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/net/vatsim/NetworkStatus` |
| Type | `object` |

###### Object `NetworkStatus`
<a id="schema-node-networkstatus"></a>

Aggregate VATSIM network status snapshot emitted once per poll cycle, summarising connected client counts.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `callsign` | `string` | `True` | Constant key value 'status' used to identify this network status record. | - | - | - |
| `update_timestamp` | `string` | `True` | UTC timestamp of the VATSIM data snapshot as reported by the data feed (RFC3339 string). | - | - | - |
| `connected_clients` | `int32` | `True` | Total number of clients (pilots, controllers, observers) currently connected to the network. | - | - | - |
| `unique_users` | `int32` | `True` | Number of unique VATSIM user IDs currently connected. | - | - | - |
| `pilot_count` | `int32` | `True` | Number of pilots currently connected and flying. | - | - | - |
| `controller_count` | `int32` | `True` | Number of controllers (including observers) currently connected and providing ATC services. | - | - | - |
| `facility` | `string` | `True` | UNS facility identifier for this aggregate VATSIM network status snapshot. The bridge emits 'network'. | - | - | - |

### Schemagroup `net.vatsim.avro`
<a id="schemagroup-netvatsimavro"></a>

#### Schema `net.vatsim.PilotPosition`
<a id="schema-netvatsimpilotposition"></a>

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
| Name | PilotPosition |
| Namespace | net.vatsim |
| Type | `record` |
| Doc | Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `cid` | `int` | VATSIM Certificate Identifier (CID) — unique numeric member ID. | `-` |
| `callsign` | `string` | ATC-style callsign chosen by the pilot for this session. | `-` |
| `latitude` | `double` | Aircraft latitude in decimal degrees (WGS-84). | `-` |
| `longitude` | `double` | Aircraft longitude in decimal degrees (WGS-84). | `-` |
| `altitude` | `int` | Indicated altitude in feet above mean sea level. | `-` |
| `groundspeed` | `int` | Ground speed in knots. | `-` |
| `heading` | `int` | Magnetic heading in degrees (0-359). | `-` |
| `transponder` | `string` | Four-digit transponder (squawk) code. | `-` |
| `qnh_mb` | `int` | Altimeter setting (QNH) in millibars. | `-` |
| `flight_rules` | `null` \| `string` | Flight rules: I or V. Null if no flight plan. | `-` |
| `aircraft_short` | `null` \| `string` | ICAO aircraft type designator. Null if no flight plan. | `-` |
| `departure` | `null` \| `string` | ICAO departure airport code. Null if no flight plan. | `-` |
| `arrival` | `null` \| `string` | ICAO arrival airport code. Null if no flight plan. | `-` |
| `route` | `null` \| `string` | Route string from flight plan. Null if no flight plan. | `-` |
| `cruise_altitude` | `null` \| `string` | Planned cruise altitude. Null if no flight plan. | `-` |
| `pilot_rating` | `int` | VATSIM pilot rating bitmask. | `-` |
| `last_updated` | `string` | UTC timestamp of last position update. | `-` |

#### Schema `net.vatsim.ControllerPosition`
<a id="schema-netvatsimcontrollerposition"></a>

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
| Name | ControllerPosition |
| Namespace | net.vatsim |
| Type | `record` |
| Doc | Current state and frequency of an air traffic controller connected to the VATSIM virtual aviation network. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `cid` | `int` | VATSIM Certificate Identifier (CID). | `-` |
| `callsign` | `string` | Controller position callsign. | `-` |
| `frequency` | `string` | Radio frequency in MHz. | `-` |
| `facility` | `int` | VATSIM facility type code. | `-` |
| `rating` | `int` | VATSIM ATC rating. | `-` |
| `text_atis` | `null` \| `string` | Controller ATIS text, lines joined by newline. Null when not set. | `-` |
| `last_updated` | `string` | UTC timestamp of last update. | `-` |

#### Schema `net.vatsim.NetworkStatus`
<a id="schema-netvatsimnetworkstatus"></a>

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
| Name | NetworkStatus |
| Namespace | net.vatsim |
| Type | `record` |
| Doc | Aggregate VATSIM network status snapshot emitted once per poll cycle. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `callsign` | `string` | Constant key value 'status'. | `-` |
| `facility` | `string` | UNS facility identifier for this aggregate VATSIM network status snapshot. The bridge emits 'network'. | `-` |
| `update_timestamp` | `string` | UTC timestamp of the VATSIM data snapshot. | `-` |
| `connected_clients` | `int` | Total connected clients. | `-` |
| `unique_users` | `int` | Unique connected user IDs. | `-` |
| `pilot_count` | `int` | Number of pilots currently flying. | `-` |
| `controller_count` | `int` | Number of controllers connected. | `-` |
