# AISstream.io Bridge Usage Guide Events

**AISstream.io Bridge** connects to the AISstream.io WebSocket API for real-time global AIS vessel tracking and forwards decoded messages to a Kafka topic as [CloudEvents](https://cloudevents.io/) in JSON format.

## At a glance

- **Event types:** 26 documented event types.
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 1 reference/catalog event type and 25 telemetry event types.
- **Identity:** `{mmsi}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `aisstream`. The record key is `{mmsi}`. In plain language, `{mmsi}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['aisstream'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `maritime/intl/aisstream/aisstream/+/+/+/+/position-report`, `maritime/intl/aisstream/aisstream/+/+/+/+/static`, `maritime/intl/aisstream/aisstream/+/+/+/+/aid-to-navigation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('maritime/intl/aisstream/aisstream/+/+/+/+/position-report', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Position Report

CloudEvents type: `IO.AISstream.PositionReport`

#### What it tells you

This event carries position report data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Position Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`NavigationalStatus`** (int32, optional): No description provided.
- **`RateOfTurn`** (int32, optional): No description provided.
- **`Sog`** (double, optional): No description provided.
- **`PositionAccuracy`** (boolean, optional): No description provided.
- **`Longitude`** (double, required): No description provided.
- **`Latitude`** (double, required): No description provided.
- **`Cog`** (double, optional): No description provided.
- **`TrueHeading`** (int32, optional): No description provided.
- **`Timestamp`** (int32, optional): No description provided.
- **`SpecialManoeuvreIndicator`** (int32, optional): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`Raim`** (boolean, optional): No description provided.
- **`CommunicationState`** (int32, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "NavigationalStatus": 0,
  "RateOfTurn": 0,
  "Sog": 0,
  "PositionAccuracy": false,
  "Longitude": 0,
  "Latitude": 0,
  "Cog": 0,
  "TrueHeading": 0,
  "Timestamp": 0,
  "SpecialManoeuvreIndicator": 0,
  "Spare": 0,
  "Raim": false,
  "CommunicationState": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Ship Static Data

CloudEvents type: `IO.AISstream.ShipStaticData`

#### What it tells you

This event carries ship static data data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Ship Static Data` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`AisVersion`** (int32, optional): No description provided.
- **`ImoNumber`** (int32, optional): No description provided.
- **`CallSign`** (string, optional): No description provided.
- **`Name`** (string, optional): No description provided.
- **`Type`** (int32, optional): No description provided.
- **`Dimension`** (object, optional): No description provided. See [Dimension](#payload-io-aisstream-shipstaticdata-dimension).
- **`FixType`** (int32, optional): No description provided.
- **`Eta`** (object, optional): No description provided. See [Eta](#payload-io-aisstream-shipstaticdata-eta).
- **`MaximumStaticDraught`** (double, optional): No description provided.
- **`Destination`** (string, optional): No description provided.
- **`Dte`** (boolean, optional): No description provided.
- **`Spare`** (boolean, optional): No description provided.
##### Dimension
<a id="payload-io-aisstream-shipstaticdata-dimension"></a>

Nested record.

- **`A`** (int32, required): No description provided.
- **`B`** (int32, required): No description provided.
- **`C`** (int32, required): No description provided.
- **`D`** (int32, required): No description provided.
##### Eta
<a id="payload-io-aisstream-shipstaticdata-eta"></a>

Nested record.

- **`Month`** (int32, required): No description provided.
- **`Day`** (int32, required): No description provided.
- **`Hour`** (int32, required): No description provided.
- **`Minute`** (int32, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "AisVersion": 0,
  "ImoNumber": 0,
  "CallSign": "string",
  "Name": "string",
  "Type": 0,
  "Dimension": {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0
  },
  "FixType": 0,
  "Eta": {
    "Month": 0,
    "Day": 0,
    "Hour": 0,
    "Minute": 0
  },
  "MaximumStaticDraught": 0,
  "Destination": "string",
  "Dte": false,
  "Spare": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Standard Class Bposition Report

CloudEvents type: `IO.AISstream.StandardClassBPositionReport`

#### What it tells you

This event carries standard class bposition report data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Standard Class Bposition Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`Sog`** (double, optional): No description provided.
- **`PositionAccuracy`** (boolean, optional): No description provided.
- **`Longitude`** (double, required): No description provided.
- **`Latitude`** (double, required): No description provided.
- **`Cog`** (double, optional): No description provided.
- **`TrueHeading`** (int32, optional): No description provided.
- **`Timestamp`** (int32, optional): No description provided.
- **`Spare2`** (int32, optional): No description provided.
- **`ClassBUnit`** (boolean, optional): No description provided.
- **`ClassBDisplay`** (boolean, optional): No description provided.
- **`ClassBDsc`** (boolean, optional): No description provided.
- **`ClassBBand`** (boolean, optional): No description provided.
- **`ClassBMsg22`** (boolean, optional): No description provided.
- **`AssignedMode`** (boolean, optional): No description provided.
- **`Raim`** (boolean, optional): No description provided.
- **`CommunicationStateIsItdma`** (boolean, optional): No description provided.
- **`CommunicationState`** (int32, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare1": 0,
  "Sog": 0,
  "PositionAccuracy": false,
  "Longitude": 0,
  "Latitude": 0,
  "Cog": 0,
  "TrueHeading": 0,
  "Timestamp": 0,
  "Spare2": 0,
  "ClassBUnit": false,
  "ClassBDisplay": false,
  "ClassBDsc": false,
  "ClassBBand": false,
  "ClassBMsg22": false,
  "AssignedMode": false,
  "Raim": false,
  "CommunicationStateIsItdma": false,
  "CommunicationState": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Extended Class Bposition Report

CloudEvents type: `IO.AISstream.ExtendedClassBPositionReport`

#### What it tells you

This event carries extended class bposition report data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Extended Class Bposition Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`Sog`** (double, optional): No description provided.
- **`PositionAccuracy`** (boolean, optional): No description provided.
- **`Longitude`** (double, required): No description provided.
- **`Latitude`** (double, required): No description provided.
- **`Cog`** (double, optional): No description provided.
- **`TrueHeading`** (int32, optional): No description provided.
- **`Timestamp`** (int32, optional): No description provided.
- **`Spare2`** (int32, optional): No description provided.
- **`Name`** (string, optional): No description provided.
- **`Type`** (int32, optional): No description provided.
- **`Dimension`** (object, optional): No description provided. See [Dimension](#payload-io-aisstream-extendedclassbpositionreport-dimension).
- **`FixType`** (int32, optional): No description provided.
- **`Raim`** (boolean, optional): No description provided.
- **`Dte`** (boolean, optional): No description provided.
- **`AssignedMode`** (boolean, optional): No description provided.
- **`Spare3`** (int32, optional): No description provided.
##### Dimension
<a id="payload-io-aisstream-extendedclassbpositionreport-dimension"></a>

Nested record.

- **`A`** (int32, required): No description provided.
- **`B`** (int32, required): No description provided.
- **`C`** (int32, required): No description provided.
- **`D`** (int32, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare1": 0,
  "Sog": 0,
  "PositionAccuracy": false,
  "Longitude": 0,
  "Latitude": 0,
  "Cog": 0,
  "TrueHeading": 0,
  "Timestamp": 0,
  "Spare2": 0,
  "Name": "string",
  "Type": 0,
  "Dimension": {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0
  },
  "FixType": 0,
  "Raim": false,
  "Dte": false,
  "AssignedMode": false,
  "Spare3": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Aids To Navigation Report

CloudEvents type: `IO.AISstream.AidsToNavigationReport`

#### What it tells you

This event carries aids to navigation report data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Aids To Navigation Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Type`** (int32, optional): No description provided.
- **`Name`** (string, optional): No description provided.
- **`PositionAccuracy`** (boolean, optional): No description provided.
- **`Longitude`** (double, required): No description provided.
- **`Latitude`** (double, required): No description provided.
- **`Dimension`** (object, optional): No description provided. See [Dimension](#payload-io-aisstream-aidstonavigationreport-dimension).
- **`Fixtype`** (int32, optional): No description provided.
- **`Timestamp`** (int32, optional): No description provided.
- **`OffPosition`** (boolean, optional): No description provided.
- **`AtoN`** (int32, optional): No description provided.
- **`Raim`** (boolean, optional): No description provided.
- **`VirtualAtoN`** (boolean, optional): No description provided.
- **`AssignedMode`** (boolean, optional): No description provided.
- **`Spare`** (boolean, optional): No description provided.
- **`NameExtension`** (string, optional): No description provided.
##### Dimension
<a id="payload-io-aisstream-aidstonavigationreport-dimension"></a>

Nested record.

- **`A`** (int32, required): No description provided.
- **`B`** (int32, required): No description provided.
- **`C`** (int32, required): No description provided.
- **`D`** (int32, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Type": 0,
  "Name": "string",
  "PositionAccuracy": false,
  "Longitude": 0,
  "Latitude": 0,
  "Dimension": {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0
  },
  "Fixtype": 0,
  "Timestamp": 0,
  "OffPosition": false,
  "AtoN": 0,
  "Raim": false,
  "VirtualAtoN": false,
  "AssignedMode": false,
  "Spare": false,
  "NameExtension": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Static Data Report

CloudEvents type: `IO.AISstream.StaticDataReport`

#### What it tells you

This event carries static data report data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Static Data Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Reserved`** (int32, optional): No description provided.
- **`PartNumber`** (boolean, optional): No description provided.
- **`ReportA`** (object, optional): No description provided. See [ReportA](#payload-io-aisstream-staticdatareport-reporta).
- **`ReportB`** (object, optional): No description provided. See [ReportB](#payload-io-aisstream-staticdatareport-reportb).
##### ReportA
<a id="payload-io-aisstream-staticdatareport-reporta"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`Name`** (string, required): No description provided.
##### ReportB
<a id="payload-io-aisstream-staticdatareport-reportb"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`ShipType`** (int32, optional): No description provided.
- **`VendorIDName`** (string, optional): No description provided.
- **`VenderIDModel`** (int32, optional): No description provided.
- **`VenderIDSerial`** (int32, optional): No description provided.
- **`CallSign`** (string, optional): No description provided.
- **`Dimension`** (object, optional): No description provided. See [Dimension](#payload-io-aisstream-staticdatareport-reportb-dimension).
- **`FixType`** (int32, optional): No description provided.
- **`Spare`** (int32, optional): No description provided.
##### Dimension
<a id="payload-io-aisstream-staticdatareport-dimension"></a>

Nested record.

- **`A`** (int32, required): No description provided.
- **`B`** (int32, required): No description provided.
- **`C`** (int32, required): No description provided.
- **`D`** (int32, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Reserved": 0,
  "PartNumber": false,
  "ReportA": {
    "Valid": false,
    "Name": "string"
  },
  "ReportB": {
    "Valid": false,
    "ShipType": 0,
    "VendorIDName": "string",
    "VenderIDModel": 0,
    "VenderIDSerial": 0,
    "CallSign": "string",
    "Dimension": {
      "A": 0,
      "B": 0,
      "C": 0,
      "D": 0
    },
    "FixType": 0,
    "Spare": 0
  }
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Base Station Report

CloudEvents type: `IO.AISstream.BaseStationReport`

#### What it tells you

This event carries base station report data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Base Station Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`UtcYear`** (int32, optional): No description provided.
- **`UtcMonth`** (int32, optional): No description provided.
- **`UtcDay`** (int32, optional): No description provided.
- **`UtcHour`** (int32, optional): No description provided.
- **`UtcMinute`** (int32, optional): No description provided.
- **`UtcSecond`** (int32, optional): No description provided.
- **`PositionAccuracy`** (boolean, optional): No description provided.
- **`Longitude`** (double, required): No description provided.
- **`Latitude`** (double, required): No description provided.
- **`FixType`** (int32, optional): No description provided.
- **`LongRangeEnable`** (boolean, optional): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`Raim`** (boolean, optional): No description provided.
- **`CommunicationState`** (int32, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "UtcYear": 0,
  "UtcMonth": 0,
  "UtcDay": 0,
  "UtcHour": 0,
  "UtcMinute": 0,
  "UtcSecond": 0,
  "PositionAccuracy": false,
  "Longitude": 0,
  "Latitude": 0,
  "FixType": 0,
  "LongRangeEnable": false,
  "Spare": 0,
  "Raim": false,
  "CommunicationState": 0
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

### Safety Broadcast Message

CloudEvents type: `IO.AISstream.SafetyBroadcastMessage`

#### What it tells you

This event carries safety broadcast message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Safety Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`Text`** (string, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare": 0,
  "Text": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Standard Search And Rescue Aircraft Report

CloudEvents type: `IO.AISstream.StandardSearchAndRescueAircraftReport`

#### What it tells you

This event carries standard search and rescue aircraft report data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Standard Search And Rescue Aircraft Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Altitude`** (int32, optional): No description provided.
- **`Sog`** (double, optional): No description provided.
- **`PositionAccuracy`** (boolean, optional): No description provided.
- **`Longitude`** (double, required): No description provided.
- **`Latitude`** (double, required): No description provided.
- **`Cog`** (double, optional): No description provided.
- **`Timestamp`** (int32, optional): No description provided.
- **`AltFromBaro`** (boolean, optional): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`Dte`** (boolean, optional): No description provided.
- **`Spare2`** (int32, optional): No description provided.
- **`AssignedMode`** (boolean, optional): No description provided.
- **`Raim`** (boolean, optional): No description provided.
- **`CommunicationStateIsItdma`** (boolean, optional): No description provided.
- **`CommunicationState`** (int32, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Altitude": 0,
  "Sog": 0,
  "PositionAccuracy": false,
  "Longitude": 0,
  "Latitude": 0,
  "Cog": 0,
  "Timestamp": 0,
  "AltFromBaro": false,
  "Spare1": 0,
  "Dte": false,
  "Spare2": 0,
  "AssignedMode": false,
  "Raim": false,
  "CommunicationStateIsItdma": false,
  "CommunicationState": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Long Range Ais Broadcast Message

CloudEvents type: `IO.AISstream.LongRangeAisBroadcastMessage`

#### What it tells you

This event carries long range ais broadcast message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Long Range Ais Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`PositionAccuracy`** (boolean, optional): No description provided.
- **`Raim`** (boolean, optional): No description provided.
- **`NavigationalStatus`** (int32, optional): No description provided.
- **`Longitude`** (double, required): No description provided.
- **`Latitude`** (double, required): No description provided.
- **`Sog`** (double, optional): No description provided.
- **`Cog`** (double, optional): No description provided.
- **`PositionLatency`** (boolean, optional): No description provided.
- **`Spare`** (boolean, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "PositionAccuracy": false,
  "Raim": false,
  "NavigationalStatus": 0,
  "Longitude": 0,
  "Latitude": 0,
  "Sog": 0,
  "Cog": 0,
  "PositionLatency": false,
  "Spare": false
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Addressed Safety Message

CloudEvents type: `IO.AISstream.AddressedSafetyMessage`

#### What it tells you

This event carries addressed safety message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Addressed Safety Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Sequenceinteger`** (int32, optional): No description provided.
- **`DestinationID`** (int32, optional): No description provided.
- **`Retransmission`** (boolean, optional): No description provided.
- **`Spare`** (boolean, optional): No description provided.
- **`Text`** (string, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Sequenceinteger": 0,
  "DestinationID": 0,
  "Retransmission": false,
  "Spare": false,
  "Text": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Addressed Binary Message

CloudEvents type: `IO.AISstream.AddressedBinaryMessage`

#### What it tells you

This event carries addressed binary message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Addressed Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Sequenceinteger`** (int32, optional): No description provided.
- **`DestinationID`** (int32, optional): No description provided.
- **`Retransmission`** (boolean, optional): No description provided.
- **`Spare`** (boolean, optional): No description provided.
- **`ApplicationID`** (object, optional): No description provided. See [ApplicationID](#payload-io-aisstream-addressedbinarymessage-applicationid).
- **`BinaryData`** (string, optional): No description provided.
##### ApplicationID
<a id="payload-io-aisstream-addressedbinarymessage-applicationid"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`DesignatedAreaCode`** (int32, required): No description provided.
- **`FunctionIdentifier`** (int32, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Sequenceinteger": 0,
  "DestinationID": 0,
  "Retransmission": false,
  "Spare": false,
  "ApplicationID": {
    "Valid": false,
    "DesignatedAreaCode": 0,
    "FunctionIdentifier": 0
  },
  "BinaryData": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Assigned Mode Command

CloudEvents type: `IO.AISstream.AssignedModeCommand`

#### What it tells you

This event carries assigned mode command data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Assigned Mode Command` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`Commands`** (map, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare": 0,
  "Commands": null
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Binary Acknowledge

CloudEvents type: `IO.AISstream.BinaryAcknowledge`

#### What it tells you

This event carries binary acknowledge data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Binary Acknowledge` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`Destinations`** (map, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare": 0,
  "Destinations": null
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Binary Broadcast Message

CloudEvents type: `IO.AISstream.BinaryBroadcastMessage`

#### What it tells you

This event carries binary broadcast message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Binary Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`ApplicationID`** (object, optional): No description provided. See [ApplicationID](#payload-io-aisstream-binarybroadcastmessage-applicationid).
- **`BinaryData`** (string, optional): No description provided.
##### ApplicationID
<a id="payload-io-aisstream-binarybroadcastmessage-applicationid"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`DesignatedAreaCode`** (int32, required): No description provided.
- **`FunctionIdentifier`** (int32, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare": 0,
  "ApplicationID": {
    "Valid": false,
    "DesignatedAreaCode": 0,
    "FunctionIdentifier": 0
  },
  "BinaryData": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Channel Management

CloudEvents type: `IO.AISstream.ChannelManagement`

#### What it tells you

This event carries channel management data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Channel Management` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`ChannelA`** (int32, optional): No description provided.
- **`ChannelB`** (int32, optional): No description provided.
- **`TxRxMode`** (int32, optional): No description provided.
- **`LowPower`** (boolean, optional): No description provided.
- **`Area`** (object, optional): No description provided. See [Area](#payload-io-aisstream-channelmanagement-area).
- **`Unicast`** (object, optional): No description provided. See [Unicast](#payload-io-aisstream-channelmanagement-unicast).
- **`IsAddressed`** (boolean, optional): No description provided.
- **`BwA`** (boolean, optional): No description provided.
- **`BwB`** (boolean, optional): No description provided.
- **`TransitionalZoneSize`** (int32, optional): No description provided.
- **`Spare4`** (int32, optional): No description provided.
##### Area
<a id="payload-io-aisstream-channelmanagement-area"></a>

Nested record.

- **`Longitude1`** (double, required): No description provided.
- **`Latitude1`** (double, required): No description provided.
- **`Longitude2`** (double, required): No description provided.
- **`Latitude2`** (double, required): No description provided.
##### Unicast
<a id="payload-io-aisstream-channelmanagement-unicast"></a>

Nested record.

- **`AddressStation1`** (int32, required): No description provided.
- **`Spare2`** (int32, optional): No description provided.
- **`AddressStation2`** (int32, required): No description provided.
- **`Spare3`** (int32, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare1": 0,
  "ChannelA": 0,
  "ChannelB": 0,
  "TxRxMode": 0,
  "LowPower": false,
  "Area": {
    "Longitude1": 0,
    "Latitude1": 0,
    "Longitude2": 0,
    "Latitude2": 0
  },
  "Unicast": {
    "AddressStation1": 0,
    "Spare2": 0,
    "AddressStation2": 0,
    "Spare3": 0
  },
  "IsAddressed": false,
  "BwA": false,
  "BwB": false,
  "TransitionalZoneSize": 0,
  "Spare4": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Coordinated Utcinquiry

CloudEvents type: `IO.AISstream.CoordinatedUTCInquiry`

#### What it tells you

This event carries coordinated utcinquiry data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Coordinated Utcinquiry` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`DestinationID`** (int32, optional): No description provided.
- **`Spare2`** (int32, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare1": 0,
  "DestinationID": 0,
  "Spare2": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Data Link Management Message

CloudEvents type: `IO.AISstream.DataLinkManagementMessage`

#### What it tells you

This event carries data link management message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Data Link Management Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`Data`** (map, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare": 0,
  "Data": null
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Gnss Broadcast Binary Message

CloudEvents type: `IO.AISstream.GnssBroadcastBinaryMessage`

#### What it tells you

This event carries gnss broadcast binary message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Gnss Broadcast Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`Longitude`** (double, optional): No description provided.
- **`Latitude`** (double, optional): No description provided.
- **`Spare2`** (int32, optional): No description provided.
- **`Data`** (string, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare1": 0,
  "Longitude": 0,
  "Latitude": 0,
  "Spare2": 0,
  "Data": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Group Assignment Command

CloudEvents type: `IO.AISstream.GroupAssignmentCommand`

#### What it tells you

This event carries group assignment command data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Group Assignment Command` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`Longitude1`** (double, optional): No description provided.
- **`Latitude1`** (double, optional): No description provided.
- **`Longitude2`** (double, optional): No description provided.
- **`Latitude2`** (double, optional): No description provided.
- **`StationType`** (int32, optional): No description provided.
- **`ShipType`** (int32, optional): No description provided.
- **`Spare2`** (int32, optional): No description provided.
- **`TxRxMode`** (int32, optional): No description provided.
- **`ReportingInterval`** (int32, optional): No description provided.
- **`QuietTime`** (int32, optional): No description provided.
- **`Spare3`** (int32, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare1": 0,
  "Longitude1": 0,
  "Latitude1": 0,
  "Longitude2": 0,
  "Latitude2": 0,
  "StationType": 0,
  "ShipType": 0,
  "Spare2": 0,
  "TxRxMode": 0,
  "ReportingInterval": 0,
  "QuietTime": 0,
  "Spare3": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Interrogation

CloudEvents type: `IO.AISstream.Interrogation`

#### What it tells you

This event carries interrogation data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Interrogation` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`Station1Msg1`** (object, optional): No description provided. See [Station1Msg1](#payload-io-aisstream-interrogation-station1msg1).
- **`Station1Msg2`** (object, optional): No description provided. See [Station1Msg2](#payload-io-aisstream-interrogation-station1msg2).
- **`Station2`** (object, optional): No description provided. See [Station2](#payload-io-aisstream-interrogation-station2).
##### Station1Msg1
<a id="payload-io-aisstream-interrogation-station1msg1"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`StationID`** (int32, required): No description provided.
- **`MessageID`** (int32, required): No description provided.
- **`SlotOffset`** (int32, required): No description provided.
##### Station1Msg2
<a id="payload-io-aisstream-interrogation-station1msg2"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`MessageID`** (int32, required): No description provided.
- **`SlotOffset`** (int32, required): No description provided.
##### Station2
<a id="payload-io-aisstream-interrogation-station2"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`StationID`** (int32, required): No description provided.
- **`MessageID`** (int32, required): No description provided.
- **`SlotOffset`** (int32, required): No description provided.
- **`Spare2`** (int32, optional): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "Spare": 0,
  "Station1Msg1": {
    "Valid": false,
    "StationID": 0,
    "MessageID": 0,
    "SlotOffset": 0
  },
  "Station1Msg2": {
    "Valid": false,
    "Spare": 0,
    "MessageID": 0,
    "SlotOffset": 0
  },
  "Station2": {
    "Valid": false,
    "Spare1": 0,
    "StationID": 0,
    "MessageID": 0,
    "SlotOffset": 0,
    "Spare2": 0
  }
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Multi Slot Binary Message

CloudEvents type: `IO.AISstream.MultiSlotBinaryMessage`

#### What it tells you

This event carries multi slot binary message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Multi Slot Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`DestinationIDValid`** (boolean, optional): No description provided.
- **`ApplicationIDValid`** (boolean, optional): No description provided.
- **`DestinationID`** (int32, optional): No description provided.
- **`Spare1`** (int32, optional): No description provided.
- **`ApplicationID`** (object, optional): No description provided. See [ApplicationID](#payload-io-aisstream-multislotbinarymessage-applicationid).
- **`Payload`** (string, optional): No description provided.
- **`Spare2`** (int32, optional): No description provided.
- **`CommunicationStateIsItdma`** (boolean, optional): No description provided.
- **`CommunicationState`** (int32, optional): No description provided.
##### ApplicationID
<a id="payload-io-aisstream-multislotbinarymessage-applicationid"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`DesignatedAreaCode`** (int32, required): No description provided.
- **`FunctionIdentifier`** (int32, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "DestinationIDValid": false,
  "ApplicationIDValid": false,
  "DestinationID": 0,
  "Spare1": 0,
  "ApplicationID": {
    "Valid": false,
    "DesignatedAreaCode": 0,
    "FunctionIdentifier": 0
  },
  "Payload": "string",
  "Spare2": 0,
  "CommunicationStateIsItdma": false,
  "CommunicationState": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Single Slot Binary Message

CloudEvents type: `IO.AISstream.SingleSlotBinaryMessage`

#### What it tells you

This event carries single slot binary message data for this source. The payload fields below are the authoritative reference for the fields currently documented in the xRegistry manifest.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Single Slot Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): No description provided.
- **`RepeatIndicator`** (int32, optional): No description provided.
- **`UserID`** (int32, required): No description provided.
- **`Valid`** (boolean, required): No description provided.
- **`DestinationIDValid`** (boolean, optional): No description provided.
- **`ApplicationIDValid`** (boolean, optional): No description provided.
- **`DestinationID`** (int32, optional): No description provided.
- **`Spare`** (int32, optional): No description provided.
- **`ApplicationID`** (object, optional): No description provided. See [ApplicationID](#payload-io-aisstream-singleslotbinarymessage-applicationid).
- **`Payload`** (string, optional): No description provided.
##### ApplicationID
<a id="payload-io-aisstream-singleslotbinarymessage-applicationid"></a>

Nested record.

- **`Valid`** (boolean, required): No description provided.
- **`DesignatedAreaCode`** (int32, required): No description provided.
- **`FunctionIdentifier`** (int32, required): No description provided.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "MessageID": 0,
  "RepeatIndicator": 0,
  "UserID": 0,
  "Valid": false,
  "DestinationIDValid": false,
  "ApplicationIDValid": false,
  "DestinationID": 0,
  "Spare": 0,
  "ApplicationID": {
    "Valid": false,
    "DesignatedAreaCode": 0,
    "FunctionIdentifier": 0
  },
  "Payload": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Position Report

CloudEvents type: `IO.AISstream.mqtt.PositionReport`

#### What it tells you

Position report (Type 1/2/3/4/9/18/19/27) projected onto the UNS axes.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report`, retain `false`, QoS `0` |

#### Payload

`Position Report` payloads are JSON object. Required fields: `mmsi`, `flag`, `ship_type`, `geohash5`, `msg_type`, `user_id`, `latitude`, `longitude`, `message_id`.

- **`mmsi`** (string, required): Source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. Mirrors UserID from the upstream AIS payload, padded to 9 digits with leading zeros. Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. Constraints: pattern `^[0-9]{9}$`.
- **`flag`** (string, required): ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country (e.g. inland-water identifiers, auxiliary craft, base stations) or for MMSIs shorter than 9 digits. Constraints: pattern `^[a-z]{2}$|^xx$`.
- **`ship_type`** (string, required): Kebab-case ship-type bucket. For static reports this is derived directly from the AIS Type-5/24 ShipType field via the standard ITU-R M.1371 vocabulary (e.g. 'cargo', 'tanker', 'passenger', 'fishing', 'tug', 'pleasure-craft'). For position reports it is looked up from an in-process ship-type cache keyed by MMSI; if no static report has been observed for the MMSI yet, the value is 'unknown'.
- **`geohash5`** (string, required): 5-character geohash of the reported (Latitude, Longitude) using the standard base32 geohash alphabet. Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position (Type 5/24/21 base reports) this is filled from the most recently observed position for the MMSI, falling back to '00000' if no position has been seen. Constraints: pattern `^[0-9b-hjkmnp-z]{5}$`.
- **`msg_type`** (enum, required): Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template.
- **`user_id`** (int32, required): Source AIS UserID (numeric MMSI, 9-digit).
- **`latitude`** (double, required): Reported latitude in WGS-84 decimal degrees.
- **`longitude`** (double, required): Reported longitude in WGS-84 decimal degrees.
- **`sog`** (double, optional): Speed over ground in knots (0..102.2).
- **`cog`** (double, optional): Course over ground in degrees (0..359.9).
- **`true_heading`** (int32, optional): True heading in degrees (0..359, 511 = not available).
- **`navigational_status`** (int32, optional): ITU navigation status code (0..15).
- **`rate_of_turn`** (int32, optional): Rate of turn in AIS-encoded units.
- **`position_accuracy`** (boolean, optional): True if the reported position is high accuracy (DGPS).
- **`timestamp`** (int32, optional): AIS report timestamp seconds-of-minute (0..59, 60..63 = special).
- **`raim`** (boolean, optional): RAIM (Receiver Autonomous Integrity Monitoring) flag.
- **`message_id`** (int32, required): Original ITU-R M.1371 message ID (1, 2, 3, 4, 9, 18, 19, or 27).
##### `msg_type` values

- `position-report`
- `static`
- `aid-to-navigation`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": "string",
  "flag": "string",
  "ship_type": "string",
  "geohash5": "string",
  "msg_type": "position-report",
  "user_id": 0,
  "latitude": 0,
  "longitude": 0,
  "sog": 0,
  "cog": 0,
  "true_heading": 0,
  "navigational_status": 0,
  "rate_of_turn": 0,
  "position_accuracy": false,
  "timestamp": 0,
  "raim": false,
  "message_id": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Ship Static

CloudEvents type: `IO.AISstream.mqtt.ShipStatic`

#### What it tells you

Static and voyage-related data (Type 5 ShipStaticData / Type 24 StaticDataReport).

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/static`, retain `false`, QoS `0` |

#### Payload

`Ship Static` payloads are JSON object. Required fields: `mmsi`, `flag`, `ship_type`, `geohash5`, `msg_type`, `user_id`, `name`, `ship_type_code`, `message_id`.

- **`mmsi`** (string, required): Source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. Mirrors UserID from the upstream AIS payload, padded to 9 digits with leading zeros. Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. Constraints: pattern `^[0-9]{9}$`.
- **`flag`** (string, required): ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country (e.g. inland-water identifiers, auxiliary craft, base stations) or for MMSIs shorter than 9 digits. Constraints: pattern `^[a-z]{2}$|^xx$`.
- **`ship_type`** (string, required): Kebab-case ship-type bucket. For static reports this is derived directly from the AIS Type-5/24 ShipType field via the standard ITU-R M.1371 vocabulary (e.g. 'cargo', 'tanker', 'passenger', 'fishing', 'tug', 'pleasure-craft'). For position reports it is looked up from an in-process ship-type cache keyed by MMSI; if no static report has been observed for the MMSI yet, the value is 'unknown'.
- **`geohash5`** (string, required): 5-character geohash of the reported (Latitude, Longitude) using the standard base32 geohash alphabet. Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position (Type 5/24/21 base reports) this is filled from the most recently observed position for the MMSI, falling back to '00000' if no position has been seen. Constraints: pattern `^[0-9b-hjkmnp-z]{5}$`.
- **`msg_type`** (enum, required): Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template.
- **`user_id`** (int32, required): Source AIS UserID (numeric MMSI, 9-digit).
- **`name`** (string, required): Vessel name as broadcast (max 20 chars, trimmed of AIS '@' padding).
- **`call_sign`** (string, optional): Radio call sign as broadcast (max 7 chars).
- **`imo_number`** (int32, optional): IMO number (7-digit). 0 if not assigned.
- **`ship_type_code`** (int32, required): Raw ITU-R M.1371 ship type code (0..99).
- **`destination`** (string, optional): Voyage destination string (max 20 chars). Empty for Type 24.
- **`eta`** (string, optional): Voyage ETA as ISO-8601 string, derived from AIS month/day/hour/minute. Empty if absent.
- **`draught`** (double, optional): Maximum present static draught in metres. 0.0 if not provided.
- **`dim_to_bow`** (int32, optional): Distance from reference point to bow in metres.
- **`dim_to_stern`** (int32, optional): Distance from reference point to stern in metres.
- **`dim_to_port`** (int32, optional): Distance from reference point to port side in metres.
- **`dim_to_starboard`** (int32, optional): Distance from reference point to starboard side in metres.
- **`message_id`** (int32, required): Original ITU-R M.1371 message ID (5 or 24).
##### `msg_type` values

- `position-report`
- `static`
- `aid-to-navigation`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": "string",
  "flag": "string",
  "ship_type": "string",
  "geohash5": "string",
  "msg_type": "position-report",
  "user_id": 0,
  "name": "string",
  "call_sign": "string",
  "imo_number": 0,
  "ship_type_code": 0,
  "destination": "string",
  "eta": "string",
  "draught": 0,
  "dim_to_bow": 0,
  "dim_to_stern": 0,
  "dim_to_port": 0,
  "dim_to_starboard": 0,
  "message_id": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Aid To Navigation

CloudEvents type: `IO.AISstream.mqtt.AidToNavigation`

#### What it tells you

Aid-to-Navigation report (Type 21).

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/aid-to-navigation`, retain `false`, QoS `0` |

#### Payload

`Aid To Navigation` payloads are JSON object. Required fields: `mmsi`, `flag`, `ship_type`, `geohash5`, `msg_type`, `user_id`, `name`, `type`, `latitude`, `longitude`, `message_id`.

- **`mmsi`** (string, required): Source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. Mirrors UserID from the upstream AIS payload, padded to 9 digits with leading zeros. Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. Constraints: pattern `^[0-9]{9}$`.
- **`flag`** (string, required): ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country (e.g. inland-water identifiers, auxiliary craft, base stations) or for MMSIs shorter than 9 digits. Constraints: pattern `^[a-z]{2}$|^xx$`.
- **`ship_type`** (string, required): Kebab-case ship-type bucket. For static reports this is derived directly from the AIS Type-5/24 ShipType field via the standard ITU-R M.1371 vocabulary (e.g. 'cargo', 'tanker', 'passenger', 'fishing', 'tug', 'pleasure-craft'). For position reports it is looked up from an in-process ship-type cache keyed by MMSI; if no static report has been observed for the MMSI yet, the value is 'unknown'.
- **`geohash5`** (string, required): 5-character geohash of the reported (Latitude, Longitude) using the standard base32 geohash alphabet. Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position (Type 5/24/21 base reports) this is filled from the most recently observed position for the MMSI, falling back to '00000' if no position has been seen. Constraints: pattern `^[0-9b-hjkmnp-z]{5}$`.
- **`msg_type`** (enum, required): Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template.
- **`user_id`** (int32, required): Source AIS UserID for the AtoN station (9-digit MMSI).
- **`name`** (string, required): AtoN name as broadcast.
- **`type`** (int32, required): AtoN type code (0..31) per ITU-R M.1371.
- **`latitude`** (double, required): Reported latitude in WGS-84 decimal degrees.
- **`longitude`** (double, required): Reported longitude in WGS-84 decimal degrees.
- **`off_position`** (boolean, optional): True if the AtoN is reported off its assigned position.
- **`virtual_atoN`** (boolean, optional): True if this is a virtual AtoN broadcast by a base station.
- **`message_id`** (int32, required): Original ITU-R M.1371 message ID (21).
##### `msg_type` values

- `position-report`
- `static`
- `aid-to-navigation`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": "string",
  "flag": "string",
  "ship_type": "string",
  "geohash5": "string",
  "msg_type": "position-report",
  "user_id": 0,
  "name": "string",
  "type": 0,
  "latitude": 0,
  "longitude": 0,
  "off_position": false,
  "virtual_atoN": false,
  "message_id": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

## Conventions

CloudEvents is the envelope around each JSON payload. It supplies metadata such as `specversion` (`1.0`), `type` (what kind of event this is), `source` (who produced it), `id` (the event occurrence identifier), `time`, and `subject` (the resource the event is about). For this source, `subject` is the stable routing identity described in each event above; the unique event occurrence is identified by CloudEvents `id` together with `source`. This repository convention mirrors the same identity to transport-native routing fields where available: Kafka message key (or the `partitionkey` extension when present), MQTT topic identity segments, and AMQP message `subject` or application properties. Those mirrors are application conventions, not generic CloudEvents binding rules. The AMQP link address identifies the stream as a whole, not an individual station or entity.

Transport bindings carry CloudEvents metadata differently:

| Transport | CloudEvents metadata location | Payload location |
| --- | --- | --- |
| Kafka binary mode | Kafka headers named `ce_<attribute>` for CloudEvents attributes except `datacontenttype`; `datacontenttype` maps to Kafka `content-type` | Kafka record value |
| Kafka structured mode | Inside the JSON CloudEvent envelope, with content type `application/cloudevents+json`; batched mode is not used by this generator | Kafka record value |
| MQTT 5 binary mode | MQTT 5 user properties named by the CloudEvents attribute (`id`, `source`, `type`, `subject`, ...), as defined by the CloudEvents MQTT binding; no `ce_` prefix | PUBLISH payload |
| AMQP 1.0 binary mode | Application properties named `cloudEvents:<attribute>` except `datacontenttype`; `datacontenttype` maps to AMQP `content-type` and must not be duplicated as an application property | AMQP message body |

All payloads documented here are JSON. MQTT retained messages are Last Known Value snapshots: the broker stores the most recent retained message per exact topic and delivers it to new subscribers when their subscription matches that topic. Schema evolution is additive where possible; incompatible semantic or structural changes are published as a new CloudEvents type so existing consumers can keep running.

## Operational notes

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/aisstream.xreg.json`](xreg/aisstream.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
