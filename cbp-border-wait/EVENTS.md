# US CBP Border Wait Times Events

MQTT/5.0 transport variants for US CBP border wait-time state. Topics are retained QoS-1 leaves under traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/{event}. The border_slug axis is lowercase kebab-case from the CBP border field (canadian-border or mexican-border); port_number preserves the Kafka key and CloudEvents subject. Wait-time snapshots use message expiry so stale retained state ages out if polling stops.

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

### Endpoint `gov.cbp.borderwait.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`gov.cbp.borderwait`](#messagegroup-govcbpborderwait) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `cbp-border-wait` |
| Kafka key | `{port_number}` |
| Deployed | False |

### Endpoint `gov.cbp.borderwait.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`gov.cbp.borderwait.mqtt`](#messagegroup-govcbpborderwaitmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `gov.cbp.borderwait`
<a id="messagegroup-govcbpborderwait"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `gov.cbp.borderwait.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `gov.cbp.borderwait.Port`
<a id="message-govcbpborderwaitport"></a>

Reference data for a US Customs and Border Protection land border port of entry. The CBP Border Wait Time system covers approximately 81 ports along the US-Canada and US-Mexico borders. Each port record identifies the crossing name, operating hours, border (Canadian or Mexican), and current operational status. Emitted at bridge startup and periodically refreshed.

| Field | Value |
| --- | --- |
| Name | Port |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.cbp.borderwait.jstruct/schemas/gov.cbp.borderwait.Port`](#schema-govcbpborderwaitport) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.cbp.borderwait.Port` |
| `source` |  | `string` | `False` | `https://bwt.cbp.gov` |
| `subject` |  | `uritemplate` | `False` | `{port_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.cbp.borderwait.Kafka` | `KAFKA` | topic `cbp-border-wait`; key `{port_number}` |

#### Message `gov.cbp.borderwait.WaitTime`
<a id="message-govcbpborderwaitwaittime"></a>

Current wait times at a US land border port of entry, flattened from the CBP nested lane structure. Reports delay in minutes and number of open lanes for each combination of traveler category (passenger vehicle, pedestrian, commercial vehicle) and lane type (standard, SENTRI/NEXUS, Ready Lane, FAST). Wait times are updated approximately every hour by CBP officers at each port.

| Field | Value |
| --- | --- |
| Name | WaitTime |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.cbp.borderwait.jstruct/schemas/gov.cbp.borderwait.WaitTime`](#schema-govcbpborderwaitwaittime) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.cbp.borderwait.WaitTime` |
| `source` |  | `string` | `False` | `https://bwt.cbp.gov` |
| `subject` |  | `uritemplate` | `False` | `{port_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.cbp.borderwait.Kafka` | `KAFKA` | topic `cbp-border-wait`; key `{port_number}` |

### Messagegroup `gov.cbp.borderwait.mqtt`
<a id="messagegroup-govcbpborderwaitmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variants for US CBP border wait-time state. Topics are retained QoS-1 leaves under traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/{event}. The border_slug axis is lowercase kebab-case from the CBP border field (canadian-border or mexican-border); port_number preserves the Kafka key and CloudEvents subject. Wait-time snapshots use message expiry so stale retained state ages out if polling stops. |
| Transport bindings | `gov.cbp.borderwait.Mqtt` (MQTT/5.0) |
| Messages | 2 |

#### Message `gov.cbp.borderwait.mqtt.Port`
<a id="message-govcbpborderwaitmqttport"></a>

Reference data for a US Customs and Border Protection land border port of entry. The CBP Border Wait Time system covers approximately 81 ports along the US-Canada and US-Mexico borders. Each port record identifies the crossing name, operating hours, border (Canadian or Mexican), and current operational status. Emitted at bridge startup and periodically refreshed.

| Field | Value |
| --- | --- |
| Name | Port |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.cbp.borderwait.jstruct/schemas/gov.cbp.borderwait.Port`](#schema-govcbpborderwaitport) |
| Base message chain | `/messagegroups/gov.cbp.borderwait/messages/gov.cbp.borderwait.Port` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.cbp.borderwait.Port` |
| `source` |  | `string` | `False` | `https://bwt.cbp.gov` |
| `subject` |  | `uritemplate` | `False` | `{port_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.cbp.borderwait.Mqtt` | `MQTT/5.0` | topic `traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/info` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/info` |
| QoS | 1 |
| Retain | True |

#### Message `gov.cbp.borderwait.mqtt.WaitTime`
<a id="message-govcbpborderwaitmqttwaittime"></a>

Current wait times at a US land border port of entry, flattened from the CBP nested lane structure. Reports delay in minutes and number of open lanes for each combination of traveler category (passenger vehicle, pedestrian, commercial vehicle) and lane type (standard, SENTRI/NEXUS, Ready Lane, FAST). Wait times are updated approximately every hour by CBP officers at each port.

| Field | Value |
| --- | --- |
| Name | WaitTime |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/gov.cbp.borderwait.jstruct/schemas/gov.cbp.borderwait.WaitTime`](#schema-govcbpborderwaitwaittime) |
| Base message chain | `/messagegroups/gov.cbp.borderwait/messages/gov.cbp.borderwait.WaitTime` |
| Transport override | `MQTT/5.0` |
| Event role | Reference data (retained transport message) |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `gov.cbp.borderwait.WaitTime` |
| `source` |  | `string` | `False` | `https://bwt.cbp.gov` |
| `subject` |  | `uritemplate` | `False` | `{port_number}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `gov.cbp.borderwait.Mqtt` | `MQTT/5.0` | topic `traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/wait-time` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/wait-time` |
| QoS | 1 |
| Retain | True |
| Additional protocol metadata | `{"message_expiry_interval": 7200}` |

## Schemagroups

### Schemagroup `gov.cbp.borderwait.jstruct`
<a id="schemagroup-govcbpborderwaitjstruct"></a>

#### Schema `gov.cbp.borderwait.Port`
<a id="schema-govcbpborderwaitport"></a>

| Field | Value |
| --- | --- |
| Name | Port |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/gov/cbp/borderwait/Port` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/gov/cbp/borderwait/Port` |
| Type | `object` |

###### Object `Port`
<a id="schema-node-port"></a>

Reference data for a US CBP land border port of entry. Describes the port identity, geographic border, crossing name, and operating hours. The port_number is a six-digit code assigned by CBP that uniquely identifies each crossing point. A single city (port_name) may have multiple crossings, each with its own port_number.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `port_number` | `string` | `True` | Six-digit CBP port number that uniquely identifies this crossing. Composed of a district code and a port sequence. Example: '250401' for San Ysidro. This is the stable key used for all wait time lookups. | - | pattern=`^[0-9]{6}$` | - |
| `port_name` | `string` | `True` | Name of the city or locality where the port is located. Example: 'Blaine', 'San Ysidro'. Multiple crossings may share the same port_name. | - | - | - |
| `border` | `string` | `True` | Which international border this port serves. One of 'Canadian Border' or 'Mexican Border'. | - | - | - |
| `crossing_name` | `string` | `True` | Name of the specific border crossing facility. Example: 'Peace Arch', 'Thousand Islands Bridge', 'San Ysidro'. Distinguishes multiple crossings within the same port_name city. | - | - | - |
| `hours` | `string` | `True` | Operating hours of the port as a human-readable string. Examples: '24 hrs/day', '6:00 am - 10:00 pm'. Empty string if not reported. | - | - | - |
| `passenger_vehicle_max_lanes` | `union` | `True` | Maximum number of passenger vehicle inspection lanes available at this crossing. Null if passenger vehicle processing is not available at this port. | - | - | - |
| `commercial_vehicle_max_lanes` | `union` | `True` | Maximum number of commercial vehicle inspection lanes available at this crossing. Null if commercial vehicle processing is not available at this port. | - | - | - |
| `pedestrian_max_lanes` | `union` | `True` | Maximum number of pedestrian inspection lanes available at this crossing. Null if pedestrian processing is not available at this port. | - | - | - |
| `border_slug` | enum `['canadian-border', 'mexican-border']` | `True` | Lowercase kebab-case MQTT/UNS routing segment derived from the CBP border field. Expected values are canadian-border or mexican-border. | - | pattern=`^[a-z0-9]+(-[a-z0-9]+)*$` | - |

#### Schema `gov.cbp.borderwait.WaitTime`
<a id="schema-govcbpborderwaitwaittime"></a>

| Field | Value |
| --- | --- |
| Name | WaitTime |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://real-time-sources.2030.io/schemas/gov/cbp/borderwait/WaitTime` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| $root | `#/definitions/gov/cbp/borderwait/WaitTime` |
| Type | `object` |

###### Object `WaitTime`
<a id="schema-node-waittime"></a>

Flattened wait time snapshot for a single US land border port of entry. Derived from the CBP Border Wait Time API nested lane structure. Each record captures delay in minutes and number of open lanes for every combination of traveler category (passenger vehicle, pedestrian, commercial vehicle) and lane type (standard, SENTRI/NEXUS, Ready Lane, FAST). Operational status values from CBP include 'no delay', 'delay', 'N/A', 'Lanes Closed', and 'Update Pending'.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `port_number` | `string` | `True` | Six-digit CBP port number identifying this crossing. Matches the port_number in the Port schema. | - | pattern=`^[0-9]{6}$` | - |
| `port_name` | `string` | `True` | Name of the city or locality where the port is located. | - | - | - |
| `border` | `string` | `True` | Which international border this port serves. One of 'Canadian Border' or 'Mexican Border'. | - | - | - |
| `crossing_name` | `string` | `True` | Name of the specific border crossing facility. | - | - | - |
| `port_status` | `string` | `True` | Overall operational status of the port. Typically 'Open' when the port is accepting traffic. | - | - | - |
| `date` | `string` | `True` | Date of the wait time report in US format (M/D/YYYY) as provided by CBP. Example: '4/8/2026'. | - | - | - |
| `time` | `string` | `True` | Time of the wait time report in HH:MM:SS format as provided by CBP, in the port's local time zone. Example: '16:16:47'. | - | - | - |
| `passenger_vehicle_standard_delay` | `union` | `True` | Delay in minutes for standard (non-trusted-traveler) passenger vehicle lanes. Null when the lane type is not available at this port (operational_status 'N/A'). | unit=`min` symbol=`min` | - | - |
| `passenger_vehicle_standard_lanes_open` | `union` | `True` | Number of standard passenger vehicle lanes currently open. Null when not available. | - | - | - |
| `passenger_vehicle_standard_operational_status` | `union` | `True` | Operational status of standard passenger vehicle lanes. Values: 'no delay', 'delay', 'N/A', 'Lanes Closed', 'Update Pending'. Null when not reported. | - | - | - |
| `passenger_vehicle_nexus_sentri_delay` | `union` | `True` | Delay in minutes for NEXUS (Canadian border) or SENTRI (Mexican border) trusted-traveler passenger vehicle lanes. Null when not available. | unit=`min` symbol=`min` | - | - |
| `passenger_vehicle_nexus_sentri_lanes_open` | `union` | `True` | Number of NEXUS/SENTRI trusted-traveler passenger vehicle lanes currently open. Null when not available. | - | - | - |
| `passenger_vehicle_nexus_sentri_operational_status` | `union` | `True` | Operational status of NEXUS/SENTRI passenger vehicle lanes. Null when not reported. | - | - | - |
| `passenger_vehicle_ready_delay` | `union` | `True` | Delay in minutes for Ready Lane passenger vehicle lanes. Ready Lanes accept RFID-enabled documents for expedited processing. Null when not available. | unit=`min` symbol=`min` | - | - |
| `passenger_vehicle_ready_lanes_open` | `union` | `True` | Number of Ready Lane passenger vehicle lanes currently open. Null when not available. | - | - | - |
| `passenger_vehicle_ready_operational_status` | `union` | `True` | Operational status of Ready Lane passenger vehicle lanes. Null when not reported. | - | - | - |
| `pedestrian_standard_delay` | `union` | `True` | Delay in minutes for standard pedestrian lanes. Null when pedestrian processing is not available at this port. | unit=`min` symbol=`min` | - | - |
| `pedestrian_standard_lanes_open` | `union` | `True` | Number of standard pedestrian lanes currently open. Null when not available. | - | - | - |
| `pedestrian_standard_operational_status` | `union` | `True` | Operational status of standard pedestrian lanes. Null when not reported. | - | - | - |
| `pedestrian_ready_delay` | `union` | `True` | Delay in minutes for Ready Lane pedestrian lanes. Null when not available. | unit=`min` symbol=`min` | - | - |
| `pedestrian_ready_lanes_open` | `union` | `True` | Number of Ready Lane pedestrian lanes currently open. Null when not available. | - | - | - |
| `pedestrian_ready_operational_status` | `union` | `True` | Operational status of Ready Lane pedestrian lanes. Null when not reported. | - | - | - |
| `commercial_vehicle_standard_delay` | `union` | `True` | Delay in minutes for standard commercial vehicle lanes. Null when commercial processing is not available at this port. | unit=`min` symbol=`min` | - | - |
| `commercial_vehicle_standard_lanes_open` | `union` | `True` | Number of standard commercial vehicle lanes currently open. Null when not available. | - | - | - |
| `commercial_vehicle_standard_operational_status` | `union` | `True` | Operational status of standard commercial vehicle lanes. Null when not reported. | - | - | - |
| `commercial_vehicle_fast_delay` | `union` | `True` | Delay in minutes for FAST (Free and Secure Trade) trusted-traveler commercial vehicle lanes. Null when not available. | unit=`min` symbol=`min` | - | - |
| `commercial_vehicle_fast_lanes_open` | `union` | `True` | Number of FAST commercial vehicle lanes currently open. Null when not available. | - | - | - |
| `commercial_vehicle_fast_operational_status` | `union` | `True` | Operational status of FAST commercial vehicle lanes. Null when not reported. | - | - | - |
| `construction_notice` | `union` | `True` | Free-text construction or closure notice for the port. Empty string or null when no notice is active. | - | - | - |
| `border_slug` | enum `['canadian-border', 'mexican-border']` | `True` | Lowercase kebab-case MQTT/UNS routing segment derived from the CBP border field. Expected values are canadian-border or mexican-border. | - | pattern=`^[a-z0-9]+(-[a-z0-9]+)*$` | - |

### Schemagroup `gov.cbp.borderwait.avro`
<a id="schemagroup-govcbpborderwaitavro"></a>

#### Schema `gov.cbp.borderwait.Port`
<a id="schema-govcbpborderwaitport"></a>

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
| Name | Port |
| Namespace | gov.cbp.borderwait |
| Type | `record` |
| Doc | Reference data for a US CBP land border port of entry. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `port_number` | `string` | Six-digit CBP port number. | `-` |
| `border_slug` | `string` | Lowercase kebab-case MQTT/UNS routing segment derived from the CBP border field. Expected values: canadian-border, mexican-border. | `-` |
| `port_name` | `string` | City or locality name. | `-` |
| `border` | `string` | International border: Canadian Border or Mexican Border. | `-` |
| `crossing_name` | `string` | Name of the crossing facility. | `-` |
| `hours` | `string` | Operating hours as a human-readable string. | `-` |
| `passenger_vehicle_max_lanes` | `null` \| `int` | Max passenger vehicle lanes. Null if not available. | `-` |
| `commercial_vehicle_max_lanes` | `null` \| `int` | Max commercial vehicle lanes. Null if not available. | `-` |
| `pedestrian_max_lanes` | `null` \| `int` | Max pedestrian lanes. Null if not available. | `-` |

#### Schema `gov.cbp.borderwait.WaitTime`
<a id="schema-govcbpborderwaitwaittime"></a>

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
| Name | WaitTime |
| Namespace | gov.cbp.borderwait |
| Type | `record` |
| Doc | Flattened wait time snapshot for a US land border port of entry. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `port_number` | `string` | Six-digit CBP port number. | `-` |
| `border_slug` | `string` | Lowercase kebab-case MQTT/UNS routing segment derived from the CBP border field. Expected values: canadian-border, mexican-border. | `-` |
| `port_name` | `string` | City or locality name. | `-` |
| `border` | `string` | International border. | `-` |
| `crossing_name` | `string` | Crossing facility name. | `-` |
| `port_status` | `string` | Overall port operational status. | `-` |
| `date` | `string` | Report date in US format (M/D/YYYY). | `-` |
| `time` | `string` | Report time in HH:MM:SS local time. | `-` |
| `passenger_vehicle_standard_delay` | `null` \| `int` | Standard passenger vehicle delay in minutes. | `-` |
| `passenger_vehicle_standard_lanes_open` | `null` \| `int` | Standard passenger vehicle lanes open. | `-` |
| `passenger_vehicle_standard_operational_status` | `null` \| `string` | Standard passenger vehicle operational status. | `-` |
| `passenger_vehicle_nexus_sentri_delay` | `null` \| `int` | NEXUS/SENTRI passenger vehicle delay in minutes. | `-` |
| `passenger_vehicle_nexus_sentri_lanes_open` | `null` \| `int` | NEXUS/SENTRI passenger vehicle lanes open. | `-` |
| `passenger_vehicle_nexus_sentri_operational_status` | `null` \| `string` | NEXUS/SENTRI passenger vehicle operational status. | `-` |
| `passenger_vehicle_ready_delay` | `null` \| `int` | Ready Lane passenger vehicle delay in minutes. | `-` |
| `passenger_vehicle_ready_lanes_open` | `null` \| `int` | Ready Lane passenger vehicle lanes open. | `-` |
| `passenger_vehicle_ready_operational_status` | `null` \| `string` | Ready Lane passenger vehicle operational status. | `-` |
| `pedestrian_standard_delay` | `null` \| `int` | Standard pedestrian delay in minutes. | `-` |
| `pedestrian_standard_lanes_open` | `null` \| `int` | Standard pedestrian lanes open. | `-` |
| `pedestrian_standard_operational_status` | `null` \| `string` | Standard pedestrian operational status. | `-` |
| `pedestrian_ready_delay` | `null` \| `int` | Ready Lane pedestrian delay in minutes. | `-` |
| `pedestrian_ready_lanes_open` | `null` \| `int` | Ready Lane pedestrian lanes open. | `-` |
| `pedestrian_ready_operational_status` | `null` \| `string` | Ready Lane pedestrian operational status. | `-` |
| `commercial_vehicle_standard_delay` | `null` \| `int` | Standard commercial vehicle delay in minutes. | `-` |
| `commercial_vehicle_standard_lanes_open` | `null` \| `int` | Standard commercial vehicle lanes open. | `-` |
| `commercial_vehicle_standard_operational_status` | `null` \| `string` | Standard commercial vehicle operational status. | `-` |
| `commercial_vehicle_fast_delay` | `null` \| `int` | FAST commercial vehicle delay in minutes. | `-` |
| `commercial_vehicle_fast_lanes_open` | `null` \| `int` | FAST commercial vehicle lanes open. | `-` |
| `commercial_vehicle_fast_operational_status` | `null` \| `string` | FAST commercial vehicle operational status. | `-` |
| `construction_notice` | `null` \| `string` | Construction or closure notice text. | `-` |
