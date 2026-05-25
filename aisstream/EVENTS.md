# AISstream.io Bridge Usage Guide Events

**AISstream.io Bridge** connects to the AISstream.io WebSocket API for real-time global AIS vessel tracking and forwards decoded messages to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format.

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

### Endpoint `IO.AISstream.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`IO.AISstream`](#messagegroup-ioaisstream) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `aisstream` |
| Kafka key | `{mmsi}` |
| Deployed | False |

### Endpoint `IO.AISstream.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`IO.AISstream.mqtt`](#messagegroup-ioaisstreammqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |

## Messagegroups

### Messagegroup `IO.AISstream`
<a id="messagegroup-ioaisstream"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `IO.AISstream.Kafka` (KAFKA) |
| Messages | 23 |

#### Message `IO.AISstream.PositionReport`
<a id="message-ioaisstreampositionreport"></a>

| Field | Value |
| --- | --- |
| Name | PositionReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.PositionReport`](#schema-ioaisstreampositionreport) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.PositionReport` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.ShipStaticData`
<a id="message-ioaisstreamshipstaticdata"></a>

| Field | Value |
| --- | --- |
| Name | ShipStaticData |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.ShipStaticData`](#schema-ioaisstreamshipstaticdata) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.ShipStaticData` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.StandardClassBPositionReport`
<a id="message-ioaisstreamstandardclassbpositionreport"></a>

| Field | Value |
| --- | --- |
| Name | StandardClassBPositionReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.StandardClassBPositionReport`](#schema-ioaisstreamstandardclassbpositionreport) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.StandardClassBPositionReport` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.ExtendedClassBPositionReport`
<a id="message-ioaisstreamextendedclassbpositionreport"></a>

| Field | Value |
| --- | --- |
| Name | ExtendedClassBPositionReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.ExtendedClassBPositionReport`](#schema-ioaisstreamextendedclassbpositionreport) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.ExtendedClassBPositionReport` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.AidsToNavigationReport`
<a id="message-ioaisstreamaidstonavigationreport"></a>

| Field | Value |
| --- | --- |
| Name | AidsToNavigationReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.AidsToNavigationReport`](#schema-ioaisstreamaidstonavigationreport) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.AidsToNavigationReport` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.StaticDataReport`
<a id="message-ioaisstreamstaticdatareport"></a>

| Field | Value |
| --- | --- |
| Name | StaticDataReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.StaticDataReport`](#schema-ioaisstreamstaticdatareport) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.StaticDataReport` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.BaseStationReport`
<a id="message-ioaisstreambasestationreport"></a>

| Field | Value |
| --- | --- |
| Name | BaseStationReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.BaseStationReport`](#schema-ioaisstreambasestationreport) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.BaseStationReport` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.SafetyBroadcastMessage`
<a id="message-ioaisstreamsafetybroadcastmessage"></a>

| Field | Value |
| --- | --- |
| Name | SafetyBroadcastMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.SafetyBroadcastMessage`](#schema-ioaisstreamsafetybroadcastmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.SafetyBroadcastMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.StandardSearchAndRescueAircraftReport`
<a id="message-ioaisstreamstandardsearchandrescueaircraftreport"></a>

| Field | Value |
| --- | --- |
| Name | StandardSearchAndRescueAircraftReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.StandardSearchAndRescueAircraftReport`](#schema-ioaisstreamstandardsearchandrescueaircraftreport) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.StandardSearchAndRescueAircraftReport` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.LongRangeAisBroadcastMessage`
<a id="message-ioaisstreamlongrangeaisbroadcastmessage"></a>

| Field | Value |
| --- | --- |
| Name | LongRangeAisBroadcastMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.LongRangeAisBroadcastMessage`](#schema-ioaisstreamlongrangeaisbroadcastmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.LongRangeAisBroadcastMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.AddressedSafetyMessage`
<a id="message-ioaisstreamaddressedsafetymessage"></a>

| Field | Value |
| --- | --- |
| Name | AddressedSafetyMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.AddressedSafetyMessage`](#schema-ioaisstreamaddressedsafetymessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.AddressedSafetyMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.AddressedBinaryMessage`
<a id="message-ioaisstreamaddressedbinarymessage"></a>

| Field | Value |
| --- | --- |
| Name | AddressedBinaryMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.AddressedBinaryMessage`](#schema-ioaisstreamaddressedbinarymessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.AddressedBinaryMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.AssignedModeCommand`
<a id="message-ioaisstreamassignedmodecommand"></a>

| Field | Value |
| --- | --- |
| Name | AssignedModeCommand |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.AssignedModeCommand`](#schema-ioaisstreamassignedmodecommand) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.AssignedModeCommand` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.BinaryAcknowledge`
<a id="message-ioaisstreambinaryacknowledge"></a>

| Field | Value |
| --- | --- |
| Name | BinaryAcknowledge |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.BinaryAcknowledge`](#schema-ioaisstreambinaryacknowledge) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.BinaryAcknowledge` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.BinaryBroadcastMessage`
<a id="message-ioaisstreambinarybroadcastmessage"></a>

| Field | Value |
| --- | --- |
| Name | BinaryBroadcastMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.BinaryBroadcastMessage`](#schema-ioaisstreambinarybroadcastmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.BinaryBroadcastMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.ChannelManagement`
<a id="message-ioaisstreamchannelmanagement"></a>

| Field | Value |
| --- | --- |
| Name | ChannelManagement |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.ChannelManagement`](#schema-ioaisstreamchannelmanagement) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.ChannelManagement` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.CoordinatedUTCInquiry`
<a id="message-ioaisstreamcoordinatedutcinquiry"></a>

| Field | Value |
| --- | --- |
| Name | CoordinatedUTCInquiry |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.CoordinatedUTCInquiry`](#schema-ioaisstreamcoordinatedutcinquiry) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.CoordinatedUTCInquiry` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.DataLinkManagementMessage`
<a id="message-ioaisstreamdatalinkmanagementmessage"></a>

| Field | Value |
| --- | --- |
| Name | DataLinkManagementMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.DataLinkManagementMessage`](#schema-ioaisstreamdatalinkmanagementmessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.DataLinkManagementMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.GnssBroadcastBinaryMessage`
<a id="message-ioaisstreamgnssbroadcastbinarymessage"></a>

| Field | Value |
| --- | --- |
| Name | GnssBroadcastBinaryMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.GnssBroadcastBinaryMessage`](#schema-ioaisstreamgnssbroadcastbinarymessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.GnssBroadcastBinaryMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.GroupAssignmentCommand`
<a id="message-ioaisstreamgroupassignmentcommand"></a>

| Field | Value |
| --- | --- |
| Name | GroupAssignmentCommand |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.GroupAssignmentCommand`](#schema-ioaisstreamgroupassignmentcommand) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.GroupAssignmentCommand` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.Interrogation`
<a id="message-ioaisstreaminterrogation"></a>

| Field | Value |
| --- | --- |
| Name | Interrogation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.Interrogation`](#schema-ioaisstreaminterrogation) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.Interrogation` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.MultiSlotBinaryMessage`
<a id="message-ioaisstreammultislotbinarymessage"></a>

| Field | Value |
| --- | --- |
| Name | MultiSlotBinaryMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.MultiSlotBinaryMessage`](#schema-ioaisstreammultislotbinarymessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.MultiSlotBinaryMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

#### Message `IO.AISstream.SingleSlotBinaryMessage`
<a id="message-ioaisstreamsingleslotbinarymessage"></a>

| Field | Value |
| --- | --- |
| Name | SingleSlotBinaryMessage |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.jstruct/schemas/IO.AISstream.SingleSlotBinaryMessage`](#schema-ioaisstreamsingleslotbinarymessage) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.SingleSlotBinaryMessage` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Kafka` | `KAFKA` | topic `aisstream`; key `{mmsi}` |

### Messagegroup `IO.AISstream.mqtt`
<a id="messagegroup-ioaisstreammqtt"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `IO.AISstream.Mqtt` (MQTT/5.0) |
| Messages | 3 |

#### Message `IO.AISstream.mqtt.PositionReport`
<a id="message-ioaisstreammqttpositionreport"></a>

| Field | Value |
| --- | --- |
| Name | PositionReport |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.mqtt.jstruct/schemas/IO.AISstream.mqtt.PositionReport`](#schema-ioaisstreammqttpositionreport) |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.mqtt.PositionReport` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Mqtt` | `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report` |
| Retain | False |

#### Message `IO.AISstream.mqtt.ShipStatic`
<a id="message-ioaisstreammqttshipstatic"></a>

| Field | Value |
| --- | --- |
| Name | ShipStatic |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.mqtt.jstruct/schemas/IO.AISstream.mqtt.ShipStatic`](#schema-ioaisstreammqttshipstatic) |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.mqtt.ShipStatic` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Mqtt` | `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/static` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/static` |
| Retain | False |

#### Message `IO.AISstream.mqtt.AidToNavigation`
<a id="message-ioaisstreammqttaidtonavigation"></a>

| Field | Value |
| --- | --- |
| Name | AidToNavigation |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/IO.AISstream.mqtt.jstruct/schemas/IO.AISstream.mqtt.AidToNavigation`](#schema-ioaisstreammqttaidtonavigation) |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `IO.AISstream.mqtt.AidToNavigation` |
| `source` |  | `string` | `False` | `wss://stream.aisstream.io/v0/stream` |
| `subject` |  | `uritemplate` | `False` | `{mmsi}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `IO.AISstream.Mqtt` | `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/aid-to-navigation` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/aid-to-navigation` |
| Retain | False |

## Schemagroups

### Schemagroup `IO.AISstream.jstruct`
<a id="schemagroup-ioaisstreamjstruct"></a>

#### Schema `IO.AISstream.PositionReport`
<a id="schema-ioaisstreampositionreport"></a>

| Field | Value |
| --- | --- |
| Name | PositionReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/PositionReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PositionReport`
<a id="schema-node-positionreport"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/PositionReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `NavigationalStatus` | `int32` | `False` |  | - | - | - |
| `RateOfTurn` | `int32` | `False` |  | - | - | - |
| `Sog` | `double` | `False` |  | - | - | - |
| `PositionAccuracy` | `boolean` | `False` |  | - | - | - |
| `Longitude` | `double` | `True` |  | - | - | - |
| `Latitude` | `double` | `True` |  | - | - | - |
| `Cog` | `double` | `False` |  | - | - | - |
| `TrueHeading` | `int32` | `False` |  | - | - | - |
| `Timestamp` | `int32` | `False` |  | - | - | - |
| `SpecialManoeuvreIndicator` | `int32` | `False` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `Raim` | `boolean` | `False` |  | - | - | - |
| `CommunicationState` | `int32` | `False` |  | - | - | - |

#### Schema `IO.AISstream.ShipStaticData`
<a id="schema-ioaisstreamshipstaticdata"></a>

| Field | Value |
| --- | --- |
| Name | ShipStaticData |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/ShipStaticData` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ShipStaticData`
<a id="schema-node-shipstaticdata"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/ShipStaticData` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `AisVersion` | `int32` | `False` |  | - | - | - |
| `ImoNumber` | `int32` | `False` |  | - | - | - |
| `CallSign` | `string` | `False` |  | - | - | - |
| `Name` | `string` | `False` |  | - | - | - |
| `Type` | `int32` | `False` |  | - | - | - |
| `Dimension` | [object `Dimension`](#schema-node-dimension) | `False` |  | - | - | - |
| `FixType` | `int32` | `False` |  | - | - | - |
| `Eta` | [object `Eta`](#schema-node-eta) | `False` |  | - | - | - |
| `MaximumStaticDraught` | `double` | `False` |  | - | - | - |
| `Destination` | `string` | `False` |  | - | - | - |
| `Dte` | `boolean` | `False` |  | - | - | - |
| `Spare` | `boolean` | `False` |  | - | - | - |

###### Object `Dimension`
<a id="schema-node-dimension"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `A` | `int32` | `True` |  | - | - | - |
| `B` | `int32` | `True` |  | - | - | - |
| `C` | `int32` | `True` |  | - | - | - |
| `D` | `int32` | `True` |  | - | - | - |

###### Object `Eta`
<a id="schema-node-eta"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Month` | `int32` | `True` |  | - | - | - |
| `Day` | `int32` | `True` |  | - | - | - |
| `Hour` | `int32` | `True` |  | - | - | - |
| `Minute` | `int32` | `True` |  | - | - | - |

#### Schema `IO.AISstream.StandardClassBPositionReport`
<a id="schema-ioaisstreamstandardclassbpositionreport"></a>

| Field | Value |
| --- | --- |
| Name | StandardClassBPositionReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/StandardClassBPositionReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `StandardClassBPositionReport`
<a id="schema-node-standardclassbpositionreport"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/StandardClassBPositionReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `Sog` | `double` | `False` |  | - | - | - |
| `PositionAccuracy` | `boolean` | `False` |  | - | - | - |
| `Longitude` | `double` | `True` |  | - | - | - |
| `Latitude` | `double` | `True` |  | - | - | - |
| `Cog` | `double` | `False` |  | - | - | - |
| `TrueHeading` | `int32` | `False` |  | - | - | - |
| `Timestamp` | `int32` | `False` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |
| `ClassBUnit` | `boolean` | `False` |  | - | - | - |
| `ClassBDisplay` | `boolean` | `False` |  | - | - | - |
| `ClassBDsc` | `boolean` | `False` |  | - | - | - |
| `ClassBBand` | `boolean` | `False` |  | - | - | - |
| `ClassBMsg22` | `boolean` | `False` |  | - | - | - |
| `AssignedMode` | `boolean` | `False` |  | - | - | - |
| `Raim` | `boolean` | `False` |  | - | - | - |
| `CommunicationStateIsItdma` | `boolean` | `False` |  | - | - | - |
| `CommunicationState` | `int32` | `False` |  | - | - | - |

#### Schema `IO.AISstream.ExtendedClassBPositionReport`
<a id="schema-ioaisstreamextendedclassbpositionreport"></a>

| Field | Value |
| --- | --- |
| Name | ExtendedClassBPositionReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/ExtendedClassBPositionReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ExtendedClassBPositionReport`
<a id="schema-node-extendedclassbpositionreport"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/ExtendedClassBPositionReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `Sog` | `double` | `False` |  | - | - | - |
| `PositionAccuracy` | `boolean` | `False` |  | - | - | - |
| `Longitude` | `double` | `True` |  | - | - | - |
| `Latitude` | `double` | `True` |  | - | - | - |
| `Cog` | `double` | `False` |  | - | - | - |
| `TrueHeading` | `int32` | `False` |  | - | - | - |
| `Timestamp` | `int32` | `False` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |
| `Name` | `string` | `False` |  | - | - | - |
| `Type` | `int32` | `False` |  | - | - | - |
| `Dimension` | [object `Dimension`](#schema-node-dimension) | `False` |  | - | - | - |
| `FixType` | `int32` | `False` |  | - | - | - |
| `Raim` | `boolean` | `False` |  | - | - | - |
| `Dte` | `boolean` | `False` |  | - | - | - |
| `AssignedMode` | `boolean` | `False` |  | - | - | - |
| `Spare3` | `int32` | `False` |  | - | - | - |

###### Object `Dimension`
<a id="schema-node-dimension"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `A` | `int32` | `True` |  | - | - | - |
| `B` | `int32` | `True` |  | - | - | - |
| `C` | `int32` | `True` |  | - | - | - |
| `D` | `int32` | `True` |  | - | - | - |

#### Schema `IO.AISstream.AidsToNavigationReport`
<a id="schema-ioaisstreamaidstonavigationreport"></a>

| Field | Value |
| --- | --- |
| Name | AidsToNavigationReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/AidsToNavigationReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AidsToNavigationReport`
<a id="schema-node-aidstonavigationreport"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/AidsToNavigationReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Type` | `int32` | `False` |  | - | - | - |
| `Name` | `string` | `False` |  | - | - | - |
| `PositionAccuracy` | `boolean` | `False` |  | - | - | - |
| `Longitude` | `double` | `True` |  | - | - | - |
| `Latitude` | `double` | `True` |  | - | - | - |
| `Dimension` | [object `Dimension`](#schema-node-dimension) | `False` |  | - | - | - |
| `Fixtype` | `int32` | `False` |  | - | - | - |
| `Timestamp` | `int32` | `False` |  | - | - | - |
| `OffPosition` | `boolean` | `False` |  | - | - | - |
| `AtoN` | `int32` | `False` |  | - | - | - |
| `Raim` | `boolean` | `False` |  | - | - | - |
| `VirtualAtoN` | `boolean` | `False` |  | - | - | - |
| `AssignedMode` | `boolean` | `False` |  | - | - | - |
| `Spare` | `boolean` | `False` |  | - | - | - |
| `NameExtension` | `string` | `False` |  | - | - | - |

###### Object `Dimension`
<a id="schema-node-dimension"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `A` | `int32` | `True` |  | - | - | - |
| `B` | `int32` | `True` |  | - | - | - |
| `C` | `int32` | `True` |  | - | - | - |
| `D` | `int32` | `True` |  | - | - | - |

#### Schema `IO.AISstream.StaticDataReport`
<a id="schema-ioaisstreamstaticdatareport"></a>

| Field | Value |
| --- | --- |
| Name | StaticDataReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/StaticDataReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `StaticDataReport`
<a id="schema-node-staticdatareport"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/StaticDataReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Reserved` | `int32` | `False` |  | - | - | - |
| `PartNumber` | `boolean` | `False` |  | - | - | - |
| `ReportA` | [object `ReportA`](#schema-node-reporta) | `False` |  | - | - | - |
| `ReportB` | [object `ReportB`](#schema-node-reportb) | `False` |  | - | - | - |

###### Object `ReportA`
<a id="schema-node-reporta"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Name` | `string` | `True` |  | - | - | - |

###### Object `ReportB`
<a id="schema-node-reportb"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `ShipType` | `int32` | `False` |  | - | - | - |
| `VendorIDName` | `string` | `False` |  | - | - | - |
| `VenderIDModel` | `int32` | `False` |  | - | - | - |
| `VenderIDSerial` | `int32` | `False` |  | - | - | - |
| `CallSign` | `string` | `False` |  | - | - | - |
| `Dimension` | [object `Dimension`](#schema-node-dimension) | `False` |  | - | - | - |
| `FixType` | `int32` | `False` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |

###### Object `Dimension`
<a id="schema-node-dimension"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `A` | `int32` | `True` |  | - | - | - |
| `B` | `int32` | `True` |  | - | - | - |
| `C` | `int32` | `True` |  | - | - | - |
| `D` | `int32` | `True` |  | - | - | - |

#### Schema `IO.AISstream.BaseStationReport`
<a id="schema-ioaisstreambasestationreport"></a>

| Field | Value |
| --- | --- |
| Name | BaseStationReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/BaseStationReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BaseStationReport`
<a id="schema-node-basestationreport"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/BaseStationReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `UtcYear` | `int32` | `False` |  | - | - | - |
| `UtcMonth` | `int32` | `False` |  | - | - | - |
| `UtcDay` | `int32` | `False` |  | - | - | - |
| `UtcHour` | `int32` | `False` |  | - | - | - |
| `UtcMinute` | `int32` | `False` |  | - | - | - |
| `UtcSecond` | `int32` | `False` |  | - | - | - |
| `PositionAccuracy` | `boolean` | `False` |  | - | - | - |
| `Longitude` | `double` | `True` |  | - | - | - |
| `Latitude` | `double` | `True` |  | - | - | - |
| `FixType` | `int32` | `False` |  | - | - | - |
| `LongRangeEnable` | `boolean` | `False` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `Raim` | `boolean` | `False` |  | - | - | - |
| `CommunicationState` | `int32` | `False` |  | - | - | - |

#### Schema `IO.AISstream.SafetyBroadcastMessage`
<a id="schema-ioaisstreamsafetybroadcastmessage"></a>

| Field | Value |
| --- | --- |
| Name | SafetyBroadcastMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/SafetyBroadcastMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SafetyBroadcastMessage`
<a id="schema-node-safetybroadcastmessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/SafetyBroadcastMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `Text` | `string` | `False` |  | - | - | - |

#### Schema `IO.AISstream.StandardSearchAndRescueAircraftReport`
<a id="schema-ioaisstreamstandardsearchandrescueaircraftreport"></a>

| Field | Value |
| --- | --- |
| Name | StandardSearchAndRescueAircraftReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/StandardSearchAndRescueAircraftReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `StandardSearchAndRescueAircraftReport`
<a id="schema-node-standardsearchandrescueaircraftreport"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/StandardSearchAndRescueAircraftReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Altitude` | `int32` | `False` |  | - | - | - |
| `Sog` | `double` | `False` |  | - | - | - |
| `PositionAccuracy` | `boolean` | `False` |  | - | - | - |
| `Longitude` | `double` | `True` |  | - | - | - |
| `Latitude` | `double` | `True` |  | - | - | - |
| `Cog` | `double` | `False` |  | - | - | - |
| `Timestamp` | `int32` | `False` |  | - | - | - |
| `AltFromBaro` | `boolean` | `False` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `Dte` | `boolean` | `False` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |
| `AssignedMode` | `boolean` | `False` |  | - | - | - |
| `Raim` | `boolean` | `False` |  | - | - | - |
| `CommunicationStateIsItdma` | `boolean` | `False` |  | - | - | - |
| `CommunicationState` | `int32` | `False` |  | - | - | - |

#### Schema `IO.AISstream.LongRangeAisBroadcastMessage`
<a id="schema-ioaisstreamlongrangeaisbroadcastmessage"></a>

| Field | Value |
| --- | --- |
| Name | LongRangeAisBroadcastMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/LongRangeAisBroadcastMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `LongRangeAisBroadcastMessage`
<a id="schema-node-longrangeaisbroadcastmessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/LongRangeAisBroadcastMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `PositionAccuracy` | `boolean` | `False` |  | - | - | - |
| `Raim` | `boolean` | `False` |  | - | - | - |
| `NavigationalStatus` | `int32` | `False` |  | - | - | - |
| `Longitude` | `double` | `True` |  | - | - | - |
| `Latitude` | `double` | `True` |  | - | - | - |
| `Sog` | `double` | `False` |  | - | - | - |
| `Cog` | `double` | `False` |  | - | - | - |
| `PositionLatency` | `boolean` | `False` |  | - | - | - |
| `Spare` | `boolean` | `False` |  | - | - | - |

#### Schema `IO.AISstream.AddressedSafetyMessage`
<a id="schema-ioaisstreamaddressedsafetymessage"></a>

| Field | Value |
| --- | --- |
| Name | AddressedSafetyMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/AddressedSafetyMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AddressedSafetyMessage`
<a id="schema-node-addressedsafetymessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/AddressedSafetyMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Sequenceinteger` | `int32` | `False` |  | - | - | - |
| `DestinationID` | `int32` | `False` |  | - | - | - |
| `Retransmission` | `boolean` | `False` |  | - | - | - |
| `Spare` | `boolean` | `False` |  | - | - | - |
| `Text` | `string` | `False` |  | - | - | - |

#### Schema `IO.AISstream.AddressedBinaryMessage`
<a id="schema-ioaisstreamaddressedbinarymessage"></a>

| Field | Value |
| --- | --- |
| Name | AddressedBinaryMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/AddressedBinaryMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AddressedBinaryMessage`
<a id="schema-node-addressedbinarymessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/AddressedBinaryMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Sequenceinteger` | `int32` | `False` |  | - | - | - |
| `DestinationID` | `int32` | `False` |  | - | - | - |
| `Retransmission` | `boolean` | `False` |  | - | - | - |
| `Spare` | `boolean` | `False` |  | - | - | - |
| `ApplicationID` | [object `ApplicationID`](#schema-node-applicationid) | `False` |  | - | - | - |
| `BinaryData` | `string` | `False` |  | - | - | - |

###### Object `ApplicationID`
<a id="schema-node-applicationid"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `DesignatedAreaCode` | `int32` | `True` |  | - | - | - |
| `FunctionIdentifier` | `int32` | `True` |  | - | - | - |

#### Schema `IO.AISstream.AssignedModeCommand`
<a id="schema-ioaisstreamassignedmodecommand"></a>

| Field | Value |
| --- | --- |
| Name | AssignedModeCommand |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/AssignedModeCommand` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AssignedModeCommand`
<a id="schema-node-assignedmodecommand"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/AssignedModeCommand` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `Commands` | `map` | `False` |  | values=`{"type": "string"}` | - | - |

#### Schema `IO.AISstream.BinaryAcknowledge`
<a id="schema-ioaisstreambinaryacknowledge"></a>

| Field | Value |
| --- | --- |
| Name | BinaryAcknowledge |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/BinaryAcknowledge` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BinaryAcknowledge`
<a id="schema-node-binaryacknowledge"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/BinaryAcknowledge` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `Destinations` | `map` | `False` |  | values=`{"type": "string"}` | - | - |

#### Schema `IO.AISstream.BinaryBroadcastMessage`
<a id="schema-ioaisstreambinarybroadcastmessage"></a>

| Field | Value |
| --- | --- |
| Name | BinaryBroadcastMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/BinaryBroadcastMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `BinaryBroadcastMessage`
<a id="schema-node-binarybroadcastmessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/BinaryBroadcastMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `ApplicationID` | [object `ApplicationID`](#schema-node-applicationid) | `False` |  | - | - | - |
| `BinaryData` | `string` | `False` |  | - | - | - |

###### Object `ApplicationID`
<a id="schema-node-applicationid"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `DesignatedAreaCode` | `int32` | `True` |  | - | - | - |
| `FunctionIdentifier` | `int32` | `True` |  | - | - | - |

#### Schema `IO.AISstream.ChannelManagement`
<a id="schema-ioaisstreamchannelmanagement"></a>

| Field | Value |
| --- | --- |
| Name | ChannelManagement |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/ChannelManagement` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ChannelManagement`
<a id="schema-node-channelmanagement"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/ChannelManagement` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `ChannelA` | `int32` | `False` |  | - | - | - |
| `ChannelB` | `int32` | `False` |  | - | - | - |
| `TxRxMode` | `int32` | `False` |  | - | - | - |
| `LowPower` | `boolean` | `False` |  | - | - | - |
| `Area` | [object `Area`](#schema-node-area) | `False` |  | - | - | - |
| `Unicast` | [object `Unicast`](#schema-node-unicast) | `False` |  | - | - | - |
| `IsAddressed` | `boolean` | `False` |  | - | - | - |
| `BwA` | `boolean` | `False` |  | - | - | - |
| `BwB` | `boolean` | `False` |  | - | - | - |
| `TransitionalZoneSize` | `int32` | `False` |  | - | - | - |
| `Spare4` | `int32` | `False` |  | - | - | - |

###### Object `Area`
<a id="schema-node-area"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Longitude1` | `double` | `True` |  | - | - | - |
| `Latitude1` | `double` | `True` |  | - | - | - |
| `Longitude2` | `double` | `True` |  | - | - | - |
| `Latitude2` | `double` | `True` |  | - | - | - |

###### Object `Unicast`
<a id="schema-node-unicast"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `AddressStation1` | `int32` | `True` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |
| `AddressStation2` | `int32` | `True` |  | - | - | - |
| `Spare3` | `int32` | `False` |  | - | - | - |

#### Schema `IO.AISstream.CoordinatedUTCInquiry`
<a id="schema-ioaisstreamcoordinatedutcinquiry"></a>

| Field | Value |
| --- | --- |
| Name | CoordinatedUTCInquiry |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/CoordinatedUTCInquiry` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `CoordinatedUTCInquiry`
<a id="schema-node-coordinatedutcinquiry"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/CoordinatedUTCInquiry` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `DestinationID` | `int32` | `False` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |

#### Schema `IO.AISstream.DataLinkManagementMessage`
<a id="schema-ioaisstreamdatalinkmanagementmessage"></a>

| Field | Value |
| --- | --- |
| Name | DataLinkManagementMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/DataLinkManagementMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `DataLinkManagementMessage`
<a id="schema-node-datalinkmanagementmessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/DataLinkManagementMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `Data` | `map` | `False` |  | values=`{"type": "string"}` | - | - |

#### Schema `IO.AISstream.GnssBroadcastBinaryMessage`
<a id="schema-ioaisstreamgnssbroadcastbinarymessage"></a>

| Field | Value |
| --- | --- |
| Name | GnssBroadcastBinaryMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/GnssBroadcastBinaryMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GnssBroadcastBinaryMessage`
<a id="schema-node-gnssbroadcastbinarymessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/GnssBroadcastBinaryMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `Longitude` | `double` | `False` |  | - | - | - |
| `Latitude` | `double` | `False` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |
| `Data` | `string` | `False` |  | - | - | - |

#### Schema `IO.AISstream.GroupAssignmentCommand`
<a id="schema-ioaisstreamgroupassignmentcommand"></a>

| Field | Value |
| --- | --- |
| Name | GroupAssignmentCommand |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/GroupAssignmentCommand` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `GroupAssignmentCommand`
<a id="schema-node-groupassignmentcommand"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/GroupAssignmentCommand` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `Longitude1` | `double` | `False` |  | - | - | - |
| `Latitude1` | `double` | `False` |  | - | - | - |
| `Longitude2` | `double` | `False` |  | - | - | - |
| `Latitude2` | `double` | `False` |  | - | - | - |
| `StationType` | `int32` | `False` |  | - | - | - |
| `ShipType` | `int32` | `False` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |
| `TxRxMode` | `int32` | `False` |  | - | - | - |
| `ReportingInterval` | `int32` | `False` |  | - | - | - |
| `QuietTime` | `int32` | `False` |  | - | - | - |
| `Spare3` | `int32` | `False` |  | - | - | - |

#### Schema `IO.AISstream.Interrogation`
<a id="schema-ioaisstreaminterrogation"></a>

| Field | Value |
| --- | --- |
| Name | Interrogation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/Interrogation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Interrogation`
<a id="schema-node-interrogation"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/Interrogation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `Station1Msg1` | [object `Station1Msg1`](#schema-node-station1msg1) | `False` |  | - | - | - |
| `Station1Msg2` | [object `Station1Msg2`](#schema-node-station1msg2) | `False` |  | - | - | - |
| `Station2` | [object `Station2`](#schema-node-station2) | `False` |  | - | - | - |

###### Object `Station1Msg1`
<a id="schema-node-station1msg1"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `StationID` | `int32` | `True` |  | - | - | - |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `SlotOffset` | `int32` | `True` |  | - | - | - |

###### Object `Station1Msg2`
<a id="schema-node-station1msg2"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `SlotOffset` | `int32` | `True` |  | - | - | - |

###### Object `Station2`
<a id="schema-node-station2"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `StationID` | `int32` | `True` |  | - | - | - |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `SlotOffset` | `int32` | `True` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |

#### Schema `IO.AISstream.MultiSlotBinaryMessage`
<a id="schema-ioaisstreammultislotbinarymessage"></a>

| Field | Value |
| --- | --- |
| Name | MultiSlotBinaryMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/MultiSlotBinaryMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `MultiSlotBinaryMessage`
<a id="schema-node-multislotbinarymessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/MultiSlotBinaryMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `DestinationIDValid` | `boolean` | `False` |  | - | - | - |
| `ApplicationIDValid` | `boolean` | `False` |  | - | - | - |
| `DestinationID` | `int32` | `False` |  | - | - | - |
| `Spare1` | `int32` | `False` |  | - | - | - |
| `ApplicationID` | [object `ApplicationID`](#schema-node-applicationid) | `False` |  | - | - | - |
| `Payload` | `string` | `False` |  | - | - | - |
| `Spare2` | `int32` | `False` |  | - | - | - |
| `CommunicationStateIsItdma` | `boolean` | `False` |  | - | - | - |
| `CommunicationState` | `int32` | `False` |  | - | - | - |

###### Object `ApplicationID`
<a id="schema-node-applicationid"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `DesignatedAreaCode` | `int32` | `True` |  | - | - | - |
| `FunctionIdentifier` | `int32` | `True` |  | - | - | - |

#### Schema `IO.AISstream.SingleSlotBinaryMessage`
<a id="schema-ioaisstreamsingleslotbinarymessage"></a>

| Field | Value |
| --- | --- |
| Name | SingleSlotBinaryMessage |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/SingleSlotBinaryMessage` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `SingleSlotBinaryMessage`
<a id="schema-node-singleslotbinarymessage"></a>

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/IO/AISstream/SingleSlotBinaryMessage` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `MessageID` | `int32` | `True` |  | - | - | - |
| `RepeatIndicator` | `int32` | `False` |  | - | - | - |
| `UserID` | `int32` | `True` |  | - | - | - |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `DestinationIDValid` | `boolean` | `False` |  | - | - | - |
| `ApplicationIDValid` | `boolean` | `False` |  | - | - | - |
| `DestinationID` | `int32` | `False` |  | - | - | - |
| `Spare` | `int32` | `False` |  | - | - | - |
| `ApplicationID` | [object `ApplicationID`](#schema-node-applicationid) | `False` |  | - | - | - |
| `Payload` | `string` | `False` |  | - | - | - |

###### Object `ApplicationID`
<a id="schema-node-applicationid"></a>

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `Valid` | `boolean` | `True` |  | - | - | - |
| `DesignatedAreaCode` | `int32` | `True` |  | - | - | - |
| `FunctionIdentifier` | `int32` | `True` |  | - | - | - |

### Schemagroup `IO.AISstream.mqtt.jstruct`
<a id="schemagroup-ioaisstreammqttjstruct"></a>

#### Schema `IO.AISstream.mqtt.PositionReport`
<a id="schema-ioaisstreammqttpositionreport"></a>

| Field | Value |
| --- | --- |
| Name | PositionReport |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.dev/aisstream/mqtt/PositionReport` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `PositionReport`
<a id="schema-node-positionreport"></a>

Position report (Type 1/2/3/4/9/18/19/27) projected onto the UNS axes.

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.dev/aisstream/mqtt/PositionReport` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `string` | `True` | Source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. Mirrors UserID from the upstream AIS payload, padded to 9 digits with leading zeros. Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. | - | pattern=`^[0-9]{9}$` | - |
| `flag` | `string` | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country (e.g. inland-water identifiers, auxiliary craft, base stations) or for MMSIs shorter than 9 digits. | - | pattern=`^[a-z]{2}$\\|^xx$` | - |
| `ship_type` | `string` | `True` | Kebab-case ship-type bucket. For static reports this is derived directly from the AIS Type-5/24 ShipType field via the standard ITU-R M.1371 vocabulary (e.g. 'cargo', 'tanker', 'passenger', 'fishing', 'tug', 'pleasure-craft'). For position reports it is looked up from an in-process ship-type cache keyed by MMSI; if no static report has been observed for the MMSI yet, the value is 'unknown'. | - | - | - |
| `geohash5` | `string` | `True` | 5-character geohash of the reported (Latitude, Longitude) using the standard base32 geohash alphabet. Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position (Type 5/24/21 base reports) this is filled from the most recently observed position for the MMSI, falling back to '00000' if no position has been seen. | - | pattern=`^[0-9b-hjkmnp-z]{5}$` | - |
| `msg_type` | enum `['position-report', 'static', 'aid-to-navigation']` | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. | - | - | - |
| `user_id` | `int32` | `True` | Source AIS UserID (numeric MMSI, 9-digit). | - | - | - |
| `latitude` | `double` | `True` | Reported latitude in WGS-84 decimal degrees. | - | - | - |
| `longitude` | `double` | `True` | Reported longitude in WGS-84 decimal degrees. | - | - | - |
| `sog` | `double` | `False` | Speed over ground in knots (0..102.2). | - | - | - |
| `cog` | `double` | `False` | Course over ground in degrees (0..359.9). | - | - | - |
| `true_heading` | `int32` | `False` | True heading in degrees (0..359, 511 = not available). | - | - | - |
| `navigational_status` | `int32` | `False` | ITU navigation status code (0..15). | - | - | - |
| `rate_of_turn` | `int32` | `False` | Rate of turn in AIS-encoded units. | - | - | - |
| `position_accuracy` | `boolean` | `False` | True if the reported position is high accuracy (DGPS). | - | - | - |
| `timestamp` | `int32` | `False` | AIS report timestamp seconds-of-minute (0..59, 60..63 = special). | - | - | - |
| `raim` | `boolean` | `False` | RAIM (Receiver Autonomous Integrity Monitoring) flag. | - | - | - |
| `message_id` | `int32` | `True` | Original ITU-R M.1371 message ID (1, 2, 3, 4, 9, 18, 19, or 27). | - | - | - |

#### Schema `IO.AISstream.mqtt.ShipStatic`
<a id="schema-ioaisstreammqttshipstatic"></a>

| Field | Value |
| --- | --- |
| Name | ShipStatic |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.dev/aisstream/mqtt/ShipStatic` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `ShipStatic`
<a id="schema-node-shipstatic"></a>

Static and voyage-related data (Type 5 ShipStaticData / Type 24 StaticDataReport).

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.dev/aisstream/mqtt/ShipStatic` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `string` | `True` | Source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. Mirrors UserID from the upstream AIS payload, padded to 9 digits with leading zeros. Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. | - | pattern=`^[0-9]{9}$` | - |
| `flag` | `string` | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country (e.g. inland-water identifiers, auxiliary craft, base stations) or for MMSIs shorter than 9 digits. | - | pattern=`^[a-z]{2}$\\|^xx$` | - |
| `ship_type` | `string` | `True` | Kebab-case ship-type bucket. For static reports this is derived directly from the AIS Type-5/24 ShipType field via the standard ITU-R M.1371 vocabulary (e.g. 'cargo', 'tanker', 'passenger', 'fishing', 'tug', 'pleasure-craft'). For position reports it is looked up from an in-process ship-type cache keyed by MMSI; if no static report has been observed for the MMSI yet, the value is 'unknown'. | - | - | - |
| `geohash5` | `string` | `True` | 5-character geohash of the reported (Latitude, Longitude) using the standard base32 geohash alphabet. Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position (Type 5/24/21 base reports) this is filled from the most recently observed position for the MMSI, falling back to '00000' if no position has been seen. | - | pattern=`^[0-9b-hjkmnp-z]{5}$` | - |
| `msg_type` | enum `['position-report', 'static', 'aid-to-navigation']` | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. | - | - | - |
| `user_id` | `int32` | `True` | Source AIS UserID (numeric MMSI, 9-digit). | - | - | - |
| `name` | `string` | `True` | Vessel name as broadcast (max 20 chars, trimmed of AIS '@' padding). | - | - | - |
| `call_sign` | `string` | `False` | Radio call sign as broadcast (max 7 chars). | - | - | - |
| `imo_number` | `int32` | `False` | IMO number (7-digit). 0 if not assigned. | - | - | - |
| `ship_type_code` | `int32` | `True` | Raw ITU-R M.1371 ship type code (0..99). | - | - | - |
| `destination` | `string` | `False` | Voyage destination string (max 20 chars). Empty for Type 24. | - | - | - |
| `eta` | `string` | `False` | Voyage ETA as ISO-8601 string, derived from AIS month/day/hour/minute. Empty if absent. | - | - | - |
| `draught` | `double` | `False` | Maximum present static draught in metres. 0.0 if not provided. | - | - | - |
| `dim_to_bow` | `int32` | `False` | Distance from reference point to bow in metres. | - | - | - |
| `dim_to_stern` | `int32` | `False` | Distance from reference point to stern in metres. | - | - | - |
| `dim_to_port` | `int32` | `False` | Distance from reference point to port side in metres. | - | - | - |
| `dim_to_starboard` | `int32` | `False` | Distance from reference point to starboard side in metres. | - | - | - |
| `message_id` | `int32` | `True` | Original ITU-R M.1371 message ID (5 or 24). | - | - | - |

#### Schema `IO.AISstream.mqtt.AidToNavigation`
<a id="schema-ioaisstreammqttaidtonavigation"></a>

| Field | Value |
| --- | --- |
| Name | AidToNavigation |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.dev/aisstream/mqtt/AidToNavigation` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `AidToNavigation`
<a id="schema-node-aidtonavigation"></a>

Aid-to-Navigation report (Type 21).

| Field | Value |
| --- | --- |
| $id | `https://schemas.real-time-sources.dev/aisstream/mqtt/AidToNavigation` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `mmsi` | `string` | `True` | Source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. Mirrors UserID from the upstream AIS payload, padded to 9 digits with leading zeros. Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. | - | pattern=`^[0-9]{9}$` | - |
| `flag` | `string` | `True` | ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country (e.g. inland-water identifiers, auxiliary craft, base stations) or for MMSIs shorter than 9 digits. | - | pattern=`^[a-z]{2}$\\|^xx$` | - |
| `ship_type` | `string` | `True` | Kebab-case ship-type bucket. For static reports this is derived directly from the AIS Type-5/24 ShipType field via the standard ITU-R M.1371 vocabulary (e.g. 'cargo', 'tanker', 'passenger', 'fishing', 'tug', 'pleasure-craft'). For position reports it is looked up from an in-process ship-type cache keyed by MMSI; if no static report has been observed for the MMSI yet, the value is 'unknown'. | - | - | - |
| `geohash5` | `string` | `True` | 5-character geohash of the reported (Latitude, Longitude) using the standard base32 geohash alphabet. Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position (Type 5/24/21 base reports) this is filled from the most recently observed position for the MMSI, falling back to '00000' if no position has been seen. | - | pattern=`^[0-9b-hjkmnp-z]{5}$` | - |
| `msg_type` | enum `['position-report', 'static', 'aid-to-navigation']` | `True` | Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template. | - | - | - |
| `user_id` | `int32` | `True` | Source AIS UserID for the AtoN station (9-digit MMSI). | - | - | - |
| `name` | `string` | `True` | AtoN name as broadcast. | - | - | - |
| `type` | `int32` | `True` | AtoN type code (0..31) per ITU-R M.1371. | - | - | - |
| `latitude` | `double` | `True` | Reported latitude in WGS-84 decimal degrees. | - | - | - |
| `longitude` | `double` | `True` | Reported longitude in WGS-84 decimal degrees. | - | - | - |
| `off_position` | `boolean` | `False` | True if the AtoN is reported off its assigned position. | - | - | - |
| `virtual_atoN` | `boolean` | `False` | True if this is a virtual AtoN broadcast by a base station. | - | - | - |
| `message_id` | `int32` | `True` | Original ITU-R M.1371 message ID (21). | - | - | - |
