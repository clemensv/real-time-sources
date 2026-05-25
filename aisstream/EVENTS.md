# AISstream.io Bridge Usage Guide Events

AISStream publishes vessel position, voyage, safety, and static AIS messages from AISStream public AIS firehose for AIS-equipped vessels received by the AISStream network. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 26 documented event types (29 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
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
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `aisstream`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/aisstream')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Position Report

CloudEvents type: `IO.AISstream.PositionReport`

#### What it tells you

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Position Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`NavigationalStatus`** (int32, optional): Provider field for navigational status in this record.
- **`RateOfTurn`** (int32, optional): Provider field for rate of turn in this record.
- **`Sog`** (double, optional): Provider field for sog in this record.
- **`PositionAccuracy`** (boolean, optional): Provider field for position accuracy in this record.
- **`Longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`Latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`Cog`** (double, optional): Provider field for cog in this record.
- **`TrueHeading`** (int32, optional): Provider field for true heading in this record.
- **`Timestamp`** (int32, optional): Time when the provider recorded or published the update.
- **`SpecialManoeuvreIndicator`** (int32, optional): Provider field for special manoeuvre indicator in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`Raim`** (boolean, optional): Provider field for raim in this record.
- **`CommunicationState`** (int32, optional): Provider field for communication state in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Ship Static Data` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`AisVersion`** (int32, optional): Provider field for ais version in this record.
- **`ImoNumber`** (int32, optional): Provider field for imo number in this record.
- **`CallSign`** (string, optional): Provider field for call sign in this record.
- **`Name`** (string, optional): Human-readable name of the resource.
- **`Type`** (int32, optional): Provider field for type in this record.
- **`Dimension`** (object, optional): Provider field for dimension in this record. See [Dimension](#payload-io-aisstream-shipstaticdata-dimension).
- **`FixType`** (int32, optional): Provider field for fix type in this record.
- **`Eta`** (object, optional): Provider field for eta in this record. See [Eta](#payload-io-aisstream-shipstaticdata-eta).
- **`MaximumStaticDraught`** (double, optional): Provider field for maximum static draught in this record.
- **`Destination`** (string, optional): Provider field for destination in this record.
- **`Dte`** (boolean, optional): Provider field for dte in this record.
- **`Spare`** (boolean, optional): Provider field for spare in this record.
##### Dimension
<a id="payload-io-aisstream-shipstaticdata-dimension"></a>

Provider field for dimension in this record.

- **`A`** (int32, required): Provider field for a in this record.
- **`B`** (int32, required): Provider field for b in this record.
- **`C`** (int32, required): Provider field for c in this record.
- **`D`** (int32, required): Provider field for d in this record.
##### Eta
<a id="payload-io-aisstream-shipstaticdata-eta"></a>

Provider field for eta in this record.

- **`Month`** (int32, required): Provider field for month in this record.
- **`Day`** (int32, required): Provider field for day in this record.
- **`Hour`** (int32, required): Provider field for hour in this record.
- **`Minute`** (int32, required): Provider field for minute in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Standard Class Bposition Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`Sog`** (double, optional): Provider field for sog in this record.
- **`PositionAccuracy`** (boolean, optional): Provider field for position accuracy in this record.
- **`Longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`Latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`Cog`** (double, optional): Provider field for cog in this record.
- **`TrueHeading`** (int32, optional): Provider field for true heading in this record.
- **`Timestamp`** (int32, optional): Time when the provider recorded or published the update.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
- **`ClassBUnit`** (boolean, optional): Provider field for class b unit in this record.
- **`ClassBDisplay`** (boolean, optional): Provider field for class b display in this record.
- **`ClassBDsc`** (boolean, optional): Provider field for class b dsc in this record.
- **`ClassBBand`** (boolean, optional): Provider field for class b band in this record.
- **`ClassBMsg22`** (boolean, optional): Provider field for class b msg22 in this record.
- **`AssignedMode`** (boolean, optional): Provider field for assigned mode in this record.
- **`Raim`** (boolean, optional): Provider field for raim in this record.
- **`CommunicationStateIsItdma`** (boolean, optional): Provider field for communication state is itdma in this record.
- **`CommunicationState`** (int32, optional): Provider field for communication state in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Extended Class Bposition Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`Sog`** (double, optional): Provider field for sog in this record.
- **`PositionAccuracy`** (boolean, optional): Provider field for position accuracy in this record.
- **`Longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`Latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`Cog`** (double, optional): Provider field for cog in this record.
- **`TrueHeading`** (int32, optional): Provider field for true heading in this record.
- **`Timestamp`** (int32, optional): Time when the provider recorded or published the update.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
- **`Name`** (string, optional): Human-readable name of the resource.
- **`Type`** (int32, optional): Provider field for type in this record.
- **`Dimension`** (object, optional): Provider field for dimension in this record. See [Dimension](#payload-io-aisstream-extendedclassbpositionreport-dimension).
- **`FixType`** (int32, optional): Provider field for fix type in this record.
- **`Raim`** (boolean, optional): Provider field for raim in this record.
- **`Dte`** (boolean, optional): Provider field for dte in this record.
- **`AssignedMode`** (boolean, optional): Provider field for assigned mode in this record.
- **`Spare3`** (int32, optional): Provider field for spare3 in this record.
##### Dimension
<a id="payload-io-aisstream-extendedclassbpositionreport-dimension"></a>

Provider field for dimension in this record.

- **`A`** (int32, required): Provider field for a in this record.
- **`B`** (int32, required): Provider field for b in this record.
- **`C`** (int32, required): Provider field for c in this record.
- **`D`** (int32, required): Provider field for d in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Aids To Navigation Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Type`** (int32, optional): Provider field for type in this record.
- **`Name`** (string, optional): Human-readable name of the resource.
- **`PositionAccuracy`** (boolean, optional): Provider field for position accuracy in this record.
- **`Longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`Latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`Dimension`** (object, optional): Provider field for dimension in this record. See [Dimension](#payload-io-aisstream-aidstonavigationreport-dimension).
- **`Fixtype`** (int32, optional): Provider field for fixtype in this record.
- **`Timestamp`** (int32, optional): Time when the provider recorded or published the update.
- **`OffPosition`** (boolean, optional): Provider field for off position in this record.
- **`AtoN`** (int32, optional): Provider field for ato n in this record.
- **`Raim`** (boolean, optional): Provider field for raim in this record.
- **`VirtualAtoN`** (boolean, optional): Provider field for virtual ato n in this record.
- **`AssignedMode`** (boolean, optional): Provider field for assigned mode in this record.
- **`Spare`** (boolean, optional): Provider field for spare in this record.
- **`NameExtension`** (string, optional): Provider field for name extension in this record.
##### Dimension
<a id="payload-io-aisstream-aidstonavigationreport-dimension"></a>

Provider field for dimension in this record.

- **`A`** (int32, required): Provider field for a in this record.
- **`B`** (int32, required): Provider field for b in this record.
- **`C`** (int32, required): Provider field for c in this record.
- **`D`** (int32, required): Provider field for d in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Static Data Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Reserved`** (int32, optional): Provider field for reserved in this record.
- **`PartNumber`** (boolean, optional): Provider field for part number in this record.
- **`ReportA`** (object, optional): Provider field for report a in this record. See [ReportA](#payload-io-aisstream-staticdatareport-reporta).
- **`ReportB`** (object, optional): Provider field for report b in this record. See [ReportB](#payload-io-aisstream-staticdatareport-reportb).
##### ReportA
<a id="payload-io-aisstream-staticdatareport-reporta"></a>

Provider field for report a in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Name`** (string, required): Human-readable name of the resource.
##### ReportB
<a id="payload-io-aisstream-staticdatareport-reportb"></a>

Provider field for report b in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`ShipType`** (int32, optional): Provider field for ship type in this record.
- **`VendorIDName`** (string, optional): Provider field for vendor i d name in this record.
- **`VenderIDModel`** (int32, optional): Provider field for vender i d model in this record.
- **`VenderIDSerial`** (int32, optional): Provider field for vender i d serial in this record.
- **`CallSign`** (string, optional): Provider field for call sign in this record.
- **`Dimension`** (object, optional): Provider field for dimension in this record. See [Dimension](#payload-io-aisstream-staticdatareport-reportb-dimension).
- **`FixType`** (int32, optional): Provider field for fix type in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
##### Dimension
<a id="payload-io-aisstream-staticdatareport-dimension"></a>

Provider field for dimension in this record.

- **`A`** (int32, required): Provider field for a in this record.
- **`B`** (int32, required): Provider field for b in this record.
- **`C`** (int32, required): Provider field for c in this record.
- **`D`** (int32, required): Provider field for d in this record.
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

A reference record from AISStream public AIS firehose for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Base Station Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`UtcYear`** (int32, optional): Provider field for utc year in this record.
- **`UtcMonth`** (int32, optional): Provider field for utc month in this record.
- **`UtcDay`** (int32, optional): Provider field for utc day in this record.
- **`UtcHour`** (int32, optional): Provider field for utc hour in this record.
- **`UtcMinute`** (int32, optional): Provider field for utc minute in this record.
- **`UtcSecond`** (int32, optional): Provider field for utc second in this record.
- **`PositionAccuracy`** (boolean, optional): Provider field for position accuracy in this record.
- **`Longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`Latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`FixType`** (int32, optional): Provider field for fix type in this record.
- **`LongRangeEnable`** (boolean, optional): Provider field for long range enable in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`Raim`** (boolean, optional): Provider field for raim in this record.
- **`CommunicationState`** (int32, optional): Provider field for communication state in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Safety Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`Text`** (string, optional): Provider field for text in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Standard Search And Rescue Aircraft Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Altitude`** (int32, optional): Provider field for altitude in this record.
- **`Sog`** (double, optional): Provider field for sog in this record.
- **`PositionAccuracy`** (boolean, optional): Provider field for position accuracy in this record.
- **`Longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`Latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`Cog`** (double, optional): Provider field for cog in this record.
- **`Timestamp`** (int32, optional): Time when the provider recorded or published the update.
- **`AltFromBaro`** (boolean, optional): Provider field for alt from baro in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`Dte`** (boolean, optional): Provider field for dte in this record.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
- **`AssignedMode`** (boolean, optional): Provider field for assigned mode in this record.
- **`Raim`** (boolean, optional): Provider field for raim in this record.
- **`CommunicationStateIsItdma`** (boolean, optional): Provider field for communication state is itdma in this record.
- **`CommunicationState`** (int32, optional): Provider field for communication state in this record.
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

A vehicle or vessel update from AISStream public AIS firehose. It reports the latest position, movement, identity, or voyage information available from the upstream feed.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Long Range Ais Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`PositionAccuracy`** (boolean, optional): Provider field for position accuracy in this record.
- **`Raim`** (boolean, optional): Provider field for raim in this record.
- **`NavigationalStatus`** (int32, optional): Provider field for navigational status in this record.
- **`Longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`Latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`Sog`** (double, optional): Provider field for sog in this record.
- **`Cog`** (double, optional): Provider field for cog in this record.
- **`PositionLatency`** (boolean, optional): Provider field for position latency in this record.
- **`Spare`** (boolean, optional): Provider field for spare in this record.
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

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Addressed Safety Message

CloudEvents type: `IO.AISstream.AddressedSafetyMessage`

#### What it tells you

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Addressed Safety Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Sequenceinteger`** (int32, optional): Provider field for sequenceinteger in this record.
- **`DestinationID`** (int32, optional): Provider field for destination i d in this record.
- **`Retransmission`** (boolean, optional): Provider field for retransmission in this record.
- **`Spare`** (boolean, optional): Provider field for spare in this record.
- **`Text`** (string, optional): Provider field for text in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Addressed Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Sequenceinteger`** (int32, optional): Provider field for sequenceinteger in this record.
- **`DestinationID`** (int32, optional): Provider field for destination i d in this record.
- **`Retransmission`** (boolean, optional): Provider field for retransmission in this record.
- **`Spare`** (boolean, optional): Provider field for spare in this record.
- **`ApplicationID`** (object, optional): Provider field for application i d in this record. See [ApplicationID](#payload-io-aisstream-addressedbinarymessage-applicationid).
- **`BinaryData`** (string, optional): Provider field for binary data in this record.
##### ApplicationID
<a id="payload-io-aisstream-addressedbinarymessage-applicationid"></a>

Provider field for application i d in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`DesignatedAreaCode`** (int32, required): Provider field for designated area code in this record.
- **`FunctionIdentifier`** (int32, required): Provider field for function identifier in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Assigned Mode Command` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`Commands`** (map, optional): Provider field for commands in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Binary Acknowledge` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`Destinations`** (map, optional): Provider field for destinations in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Binary Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`ApplicationID`** (object, optional): Provider field for application i d in this record. See [ApplicationID](#payload-io-aisstream-binarybroadcastmessage-applicationid).
- **`BinaryData`** (string, optional): Provider field for binary data in this record.
##### ApplicationID
<a id="payload-io-aisstream-binarybroadcastmessage-applicationid"></a>

Provider field for application i d in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`DesignatedAreaCode`** (int32, required): Provider field for designated area code in this record.
- **`FunctionIdentifier`** (int32, required): Provider field for function identifier in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Channel Management` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`ChannelA`** (int32, optional): Provider field for channel a in this record.
- **`ChannelB`** (int32, optional): Provider field for channel b in this record.
- **`TxRxMode`** (int32, optional): Provider field for tx rx mode in this record.
- **`LowPower`** (boolean, optional): Provider field for low power in this record.
- **`Area`** (object, optional): Provider field for area in this record. See [Area](#payload-io-aisstream-channelmanagement-area).
- **`Unicast`** (object, optional): Provider field for unicast in this record. See [Unicast](#payload-io-aisstream-channelmanagement-unicast).
- **`IsAddressed`** (boolean, optional): Provider field for is addressed in this record.
- **`BwA`** (boolean, optional): Provider field for bw a in this record.
- **`BwB`** (boolean, optional): Provider field for bw b in this record.
- **`TransitionalZoneSize`** (int32, optional): Provider field for transitional zone size in this record.
- **`Spare4`** (int32, optional): Provider field for spare4 in this record.
##### Area
<a id="payload-io-aisstream-channelmanagement-area"></a>

Provider field for area in this record.

- **`Longitude1`** (double, required): Provider field for longitude1 in this record.
- **`Latitude1`** (double, required): Provider field for latitude1 in this record.
- **`Longitude2`** (double, required): Provider field for longitude2 in this record.
- **`Latitude2`** (double, required): Provider field for latitude2 in this record.
##### Unicast
<a id="payload-io-aisstream-channelmanagement-unicast"></a>

Provider field for unicast in this record.

- **`AddressStation1`** (int32, required): Provider field for address station1 in this record.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
- **`AddressStation2`** (int32, required): Provider field for address station2 in this record.
- **`Spare3`** (int32, optional): Provider field for spare3 in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Coordinated Utcinquiry` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`DestinationID`** (int32, optional): Provider field for destination i d in this record.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Data Link Management Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`Data`** (map, optional): Provider field for data in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Gnss Broadcast Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`Longitude`** (double, optional): Longitude of the resource in WGS 84 coordinates.
- **`Latitude`** (double, optional): Latitude of the resource in WGS 84 coordinates.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
- **`Data`** (string, optional): Provider field for data in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Group Assignment Command` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`Longitude1`** (double, optional): Provider field for longitude1 in this record.
- **`Latitude1`** (double, optional): Provider field for latitude1 in this record.
- **`Longitude2`** (double, optional): Provider field for longitude2 in this record.
- **`Latitude2`** (double, optional): Provider field for latitude2 in this record.
- **`StationType`** (int32, optional): Provider field for station type in this record.
- **`ShipType`** (int32, optional): Provider field for ship type in this record.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
- **`TxRxMode`** (int32, optional): Provider field for tx rx mode in this record.
- **`ReportingInterval`** (int32, optional): Provider field for reporting interval in this record.
- **`QuietTime`** (int32, optional): Provider field for quiet time in this record.
- **`Spare3`** (int32, optional): Provider field for spare3 in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Interrogation` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`Station1Msg1`** (object, optional): Provider field for station1 msg1 in this record. See [Station1Msg1](#payload-io-aisstream-interrogation-station1msg1).
- **`Station1Msg2`** (object, optional): Provider field for station1 msg2 in this record. See [Station1Msg2](#payload-io-aisstream-interrogation-station1msg2).
- **`Station2`** (object, optional): Provider field for station2 in this record. See [Station2](#payload-io-aisstream-interrogation-station2).
##### Station1Msg1
<a id="payload-io-aisstream-interrogation-station1msg1"></a>

Provider field for station1 msg1 in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`StationID`** (int32, required): Provider field for station i d in this record.
- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`SlotOffset`** (int32, required): Provider field for slot offset in this record.
##### Station1Msg2
<a id="payload-io-aisstream-interrogation-station1msg2"></a>

Provider field for station1 msg2 in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`SlotOffset`** (int32, required): Provider field for slot offset in this record.
##### Station2
<a id="payload-io-aisstream-interrogation-station2"></a>

Provider field for station2 in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`StationID`** (int32, required): Provider field for station i d in this record.
- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`SlotOffset`** (int32, required): Provider field for slot offset in this record.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Multi Slot Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`DestinationIDValid`** (boolean, optional): Provider field for destination i d valid in this record.
- **`ApplicationIDValid`** (boolean, optional): Provider field for application i d valid in this record.
- **`DestinationID`** (int32, optional): Provider field for destination i d in this record.
- **`Spare1`** (int32, optional): Provider field for spare1 in this record.
- **`ApplicationID`** (object, optional): Provider field for application i d in this record. See [ApplicationID](#payload-io-aisstream-multislotbinarymessage-applicationid).
- **`Payload`** (string, optional): Provider field for payload in this record.
- **`Spare2`** (int32, optional): Provider field for spare2 in this record.
- **`CommunicationStateIsItdma`** (boolean, optional): Provider field for communication state is itdma in this record.
- **`CommunicationState`** (int32, optional): Provider field for communication state in this record.
##### ApplicationID
<a id="payload-io-aisstream-multislotbinarymessage-applicationid"></a>

Provider field for application i d in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`DesignatedAreaCode`** (int32, required): Provider field for designated area code in this record.
- **`FunctionIdentifier`** (int32, required): Provider field for function identifier in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{mmsi}` |

#### Payload

`Single Slot Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): Provider field for message i d in this record.
- **`RepeatIndicator`** (int32, optional): Provider field for repeat indicator in this record.
- **`UserID`** (int32, required): Provider field for user i d in this record.
- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`DestinationIDValid`** (boolean, optional): Provider field for destination i d valid in this record.
- **`ApplicationIDValid`** (boolean, optional): Provider field for application i d valid in this record.
- **`DestinationID`** (int32, optional): Provider field for destination i d in this record.
- **`Spare`** (int32, optional): Provider field for spare in this record.
- **`ApplicationID`** (object, optional): Provider field for application i d in this record. See [ApplicationID](#payload-io-aisstream-singleslotbinarymessage-applicationid).
- **`Payload`** (string, optional): Provider field for payload in this record.
##### ApplicationID
<a id="payload-io-aisstream-singleslotbinarymessage-applicationid"></a>

Provider field for application i d in this record.

- **`Valid`** (boolean, required): Provider field for valid in this record.
- **`DesignatedAreaCode`** (int32, required): Provider field for designated area code in this record.
- **`FunctionIdentifier`** (int32, required): Provider field for function identifier in this record.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{mmsi}`; application properties flag `{flag}`, ship_type `{ship_type}`, geohash5 `{geohash5}` |

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

- `position-report`: Provider coded value `position-report` for this field.
- `static`: Provider coded value `static` for this field.
- `aid-to-navigation`: Provider coded value `aid-to-navigation` for this field.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/static`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{mmsi}`; application properties flag `{flag}`, ship_type `{ship_type}`, geohash5 `{geohash5}` |

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

- `position-report`: Provider coded value `position-report` for this field.
- `static`: Provider coded value `static` for this field.
- `aid-to-navigation`: Provider coded value `aid-to-navigation` for this field.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI (Maritime Mobile Service Identity) as a 9-digit ASCII string. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/aid-to-navigation`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{mmsi}`; application properties flag `{flag}`, ship_type `{ship_type}`, geohash5 `{geohash5}` |

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

- `position-report`: Provider coded value `position-report` for this field.
- `static`: Provider coded value `static` for this field.
- `aid-to-navigation`: Provider coded value `aid-to-navigation` for this field.
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
