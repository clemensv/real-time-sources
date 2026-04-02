# AISstream.io Bridge Events

This document describes the events emitted by the AISstream.io bridge.

- [IO.AISstream](#message-group-ioaisstream)
  - [IO.AISstream.PositionReport](#message-ioaisstreampositionreport)
  - [IO.AISstream.ShipStaticData](#message-ioaisstreamshipstaticdata)
  - [IO.AISstream.StandardClassBPositionReport](#message-ioaisstreamstandardclassbpositionreport)
  - [IO.AISstream.ExtendedClassBPositionReport](#message-ioaisstreamextendedclassbpositionreport)
  - [IO.AISstream.AidsToNavigationReport](#message-ioaisstreamaidstonavigationreport)
  - [IO.AISstream.StaticDataReport](#message-ioaisstreamstaticdatareport)
  - [IO.AISstream.BaseStationReport](#message-ioaisstreambasestationreport)
  - [IO.AISstream.SafetyBroadcastMessage](#message-ioaisstreamsafetybroadcastmessage)
  - [IO.AISstream.StandardSearchAndRescueAircraftReport](#message-ioaisstreamstandardsearchandrescueaircraftreport)
  - [IO.AISstream.LongRangeAisBroadcastMessage](#message-ioaisstreamlongrangeaisbroadcastmessage)
  - [IO.AISstream.AddressedSafetyMessage](#message-ioaisstreamaddressedsafetymessage)
  - [IO.AISstream.AddressedBinaryMessage](#message-ioaisstreamaddressedbinarymessage)
  - [IO.AISstream.AssignedModeCommand](#message-ioaisstreamassignedmodecommand)
  - [IO.AISstream.BinaryAcknowledge](#message-ioaisstreambinaryacknowledge)
  - [IO.AISstream.BinaryBroadcastMessage](#message-ioaisstreambinarybroadcastmessage)
  - [IO.AISstream.ChannelManagement](#message-ioaisstreamchannelmanagement)
  - [IO.AISstream.CoordinatedUTCInquiry](#message-ioaisstreamcoordinatedutcinquiry)
  - [IO.AISstream.DataLinkManagementMessage](#message-ioaisstreamdatalinkmanagementmessage)
  - [IO.AISstream.GnssBroadcastBinaryMessage](#message-ioaisstreamgnssbroadcastbinarymessage)
  - [IO.AISstream.GroupAssignmentCommand](#message-ioaisstreamgroupassignmentcommand)
  - [IO.AISstream.Interrogation](#message-ioaisstreaminterrogation)
  - [IO.AISstream.MultiSlotBinaryMessage](#message-ioaisstreammultislotbinarymessage)
  - [IO.AISstream.SingleSlotBinaryMessage](#message-ioaisstreamsingleslotbinarymessage)

---

## Message Group: IO.AISstream

All events share these common CloudEvents attributes:

| **Name** | **Value** |
|----------|-----------|
| `source` | `wss://stream.aisstream.io/v0/stream` |

The `type` attribute is set to the fully qualified message name (e.g.,
`IO.AISstream.PositionReport`).

---

### Message: IO.AISstream.PositionReport

Class A vessel position report (AIS types 1, 2, 3).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.PositionReport` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

#### Key Fields:

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `UserID` | integer | MMSI number |
| `Longitude` | number | Longitude in decimal degrees |
| `Latitude` | number | Latitude in decimal degrees |
| `Sog` | number | Speed over ground (knots) |
| `Cog` | number | Course over ground (degrees) |
| `TrueHeading` | integer | True heading (degrees) |
| `NavigationalStatus` | integer | Navigation status code |

---

### Message: IO.AISstream.ShipStaticData

Ship identity and voyage data (AIS type 5).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.ShipStaticData` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

#### Key Fields:

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `UserID` | integer | MMSI number |
| `ImoNumber` | integer | IMO ship ID |
| `CallSign` | string | Radio callsign |
| `Name` | string | Vessel name |
| `Type` | integer | Ship and cargo type |
| `Dimension` | object | Ship dimensions (A, B, C, D) |
| `Destination` | string | Destination port |
| `Eta` | object | Estimated time of arrival |
| `MaximumStaticDraught` | number | Draught in meters |

---

### Message: IO.AISstream.StandardClassBPositionReport

Class B CS vessel position report (AIS type 18).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.StandardClassBPositionReport` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.ExtendedClassBPositionReport

Extended Class B position report with vessel name (AIS type 19).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.ExtendedClassBPositionReport` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.AidsToNavigationReport

Aids to navigation — buoys, lighthouses, etc. (AIS type 21).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.AidsToNavigationReport` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.StaticDataReport

Class B static data (AIS type 24).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.StaticDataReport` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.BaseStationReport

Base station report with UTC time (AIS type 4).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.BaseStationReport` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.SafetyBroadcastMessage

Safety-related text broadcast (AIS type 14).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.SafetyBroadcastMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.StandardSearchAndRescueAircraftReport

SAR aircraft position report (AIS type 9).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.StandardSearchAndRescueAircraftReport` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.LongRangeAisBroadcastMessage

Long-range AIS broadcast (AIS type 27).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.LongRangeAisBroadcastMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.AddressedSafetyMessage

Addressed safety message (AIS type 12).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.AddressedSafetyMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.AddressedBinaryMessage

Addressed binary message (AIS type 6).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.AddressedBinaryMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.AssignedModeCommand

Assigned mode command (AIS type 16).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.AssignedModeCommand` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.BinaryAcknowledge

Binary acknowledgement (AIS type 7/13).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.BinaryAcknowledge` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.BinaryBroadcastMessage

Binary broadcast message (AIS type 8).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.BinaryBroadcastMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.ChannelManagement

Channel management (AIS type 22).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.ChannelManagement` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.CoordinatedUTCInquiry

Coordinated UTC inquiry (AIS type 10).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.CoordinatedUTCInquiry` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.DataLinkManagementMessage

Data link management (AIS type 20).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.DataLinkManagementMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.GnssBroadcastBinaryMessage

GNSS corrections broadcast (AIS type 17).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.GnssBroadcastBinaryMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.GroupAssignmentCommand

Group assignment command (AIS type 23).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.GroupAssignmentCommand` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.Interrogation

Interrogation (AIS type 15).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.Interrogation` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.MultiSlotBinaryMessage

Multi-slot binary message (AIS type 26).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.MultiSlotBinaryMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |

---

### Message: IO.AISstream.SingleSlotBinaryMessage

Single-slot binary message (AIS type 25).

#### CloudEvents Attributes:

| **Name** | **Value** |
|----------|-----------|
| `type` | `IO.AISstream.SingleSlotBinaryMessage` |
| `source` | `wss://stream.aisstream.io/v0/stream` |
