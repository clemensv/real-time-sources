# AISstream.io feeder Events

AISStream publishes vessel position, voyage, safety, and static AIS messages from AISStream public AIS firehose for AIS-equipped vessels received by the AISStream network. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 23 documented event types (69 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 22 telemetry event types.
- **Identity:** `{UserID}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `aisstream`. The record key is `{UserID}`. In plain language, `{UserID}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

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

Connect to `mqtt://localhost:1883` and subscribe to `maritime/intl/aisstream/aisstream/+/+/+/+/position-report`, `maritime/intl/aisstream/aisstream/+/+/+/+/ship-static-data`, `maritime/intl/aisstream/aisstream/+/+/+/+/standard-class-b-position-report`, `maritime/intl/aisstream/aisstream/+/+/+/+/extended-class-b-position-report`, `maritime/intl/aisstream/aisstream/+/+/+/+/aids-to-navigation-report`, `maritime/intl/aisstream/aisstream/+/+/+/+/static-data-report`, `maritime/intl/aisstream/aisstream/+/+/+/+/base-station-report`, `maritime/intl/aisstream/aisstream/+/+/+/+/safety-broadcast-message`, `maritime/intl/aisstream/aisstream/+/+/+/+/standard-search-and-rescue-aircraft-report`, `maritime/intl/aisstream/aisstream/+/+/+/+/long-range-ais-broadcast-message`, `maritime/intl/aisstream/aisstream/+/+/+/+/addressed-safety-message`, `maritime/intl/aisstream/aisstream/+/+/+/+/addressed-binary-message`, `maritime/intl/aisstream/aisstream/+/+/+/+/assigned-mode-command`, `maritime/intl/aisstream/aisstream/+/+/+/+/binary-acknowledge`, `maritime/intl/aisstream/aisstream/+/+/+/+/binary-broadcast-message`, `maritime/intl/aisstream/aisstream/+/+/+/+/channel-management`, `maritime/intl/aisstream/aisstream/+/+/+/+/coordinated-utc-inquiry`, `maritime/intl/aisstream/aisstream/+/+/+/+/data-link-management-message`, `maritime/intl/aisstream/aisstream/+/+/+/+/gnss-broadcast-binary-message`, `maritime/intl/aisstream/aisstream/+/+/+/+/group-assignment-command`, `maritime/intl/aisstream/aisstream/+/+/+/+/interrogation`, `maritime/intl/aisstream/aisstream/+/+/+/+/multi-slot-binary-message`, `maritime/intl/aisstream/aisstream/+/+/+/+/single-slot-binary-message`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Class A Automatic Identification System (AIS) position report (ITU-R M.1371 messages 1, 2 and 3) as decoded and relayed by the aisstream.io firehose.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Position Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this Class A position report it is 1 for a scheduled report, 2 for an assigned-schedule report or 3 for a special / interrogation-response report (the three variants share an identical field layout).
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`NavigationalStatus`** (int32, optional): Navigational status code (ITU-R M.1371): 0 = under way using engine, 1 = at anchor, 2 = not under command, 3 = restricted manoeuvrability, 4 = constrained by her draught, 5 = moored, 6 = aground, 7 = engaged in fishing, 8 = under way sailing, 9-13 = reserved/special categories, 14 = AIS-SART/MOB/EPIRB active, 15 = undefined (default).
- **`RateOfTurn`** (int32, optional): Rate of turn as the AIS-encoded value in the range -128..127. 0 = not turning; positive = turning to starboard (right), negative = turning to port (left); +127/-127 = turning faster than 5 degrees per 30 s; -128 = no turn information available. Decoded degrees per minute = (value/4.733) squared, carrying the sign of the value.
- **`Sog`** (double, optional, [kn_i] (kt)): Speed over ground in knots (aisstream.io reports the decoded value; AIS native resolution is 0.1 kn, 102.3 = not available).
- **`PositionAccuracy`** (boolean, optional): Position accuracy flag: true = high accuracy (better than 10 m, e.g. DGNSS-corrected), false = low accuracy (greater than 10 m, autonomous GNSS).
- **`Longitude`** (double, required, deg (°)): Longitude of the reported position in WGS-84 decimal degrees, east positive (range -180 to 180; 181 = position not available).
- **`Latitude`** (double, required, deg (°)): Latitude of the reported position in WGS-84 decimal degrees, north positive (range -90 to 90; 91 = position not available).
- **`Cog`** (double, optional, deg (°)): Course over ground in degrees true (0-359.9; the encoded value 3600, i.e. 360 degrees, means not available).
- **`TrueHeading`** (int32, optional, deg (°)): Heading in degrees true from the vessel's compass or gyro (0-359); 511 = heading not available.
- **`Timestamp`** (int32, optional): UTC second of the minute (0-59) at which the report was generated by the originating station's electronic position-fixing system; 60 = time stamp not available (default), 61 = positioning system in manual input mode, 62 = positioning system in dead-reckoning mode, 63 = positioning system inoperative.
- **`SpecialManoeuvreIndicator`** (int32, optional): Special manoeuvre indicator: 0 = not available (default), 1 = not engaged in special manoeuvre, 2 = engaged in special manoeuvre (e.g. a regional passing arrangement).
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Raim`** (boolean, optional): Receiver Autonomous Integrity Monitoring (RAIM) flag of the position-fixing device: true = RAIM in use, false = RAIM not in use.
- **`CommunicationState`** (int32, optional): SOTDMA/ITDMA communication state value carrying the synchronisation state and slot time-out / slot-allocation information used by the AIS TDMA link layer.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Class A static and voyage-related data report (ITU-R M.1371 message 5) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/ship-static-data`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Ship Static Data` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this static and voyage-related data report it is 5.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`AisVersion`** (int32, optional): AIS protocol version the station complies with: 0 = ITU-R M.1371-1; values 1, 2 and 3 indicate later editions of the standard.
- **`ImoNumber`** (int32, optional): IMO ship identification number (a seven-digit number that stays with the hull for its lifetime); 0 = not available or not applicable.
- **`CallSign`** (string, optional): International radio call sign of the vessel as up to 7 six-bit ASCII characters (right-padded with '@'); an all-'@' value means not available.
- **`Name`** (string, optional): Name of the vessel as up to 20 six-bit ASCII characters (right-padded with '@'); an all-'@' value means not available.
- **`Type`** (int32, optional): Ship and cargo type code (0-99): the tens digit gives the category (3x = special craft, 6x = passenger, 7x = cargo, 8x = tanker, 9x = other) and the units digit the subtype or hazard class. 0 = not available.
- **`Dimension`** (object, optional): Reference point for the reported position and overall vessel dimensions, given as distances in metres from the position-fixing antenna to the bow (A), stern (B), port side (C) and starboard side (D); overall length = A + B and beam = C + D. See [Dimension](#payload-io-aisstream-shipstaticdata-dimension).
- **`FixType`** (int32, optional): Type of electronic position-fixing device: 0 = undefined, 1 = GPS, 2 = GLONASS, 3 = combined GPS/GLONASS, 4 = Loran-C, 5 = Chayka, 6 = integrated navigation system, 7 = surveyed, 8 = Galileo, 15 = internal GNSS.
- **`Eta`** (object, optional): Estimated time of arrival (ETA) at destination, in UTC, encoded as separate month, day, hour and minute fields. See [Eta](#payload-io-aisstream-shipstaticdata-eta).
- **`MaximumStaticDraught`** (double, optional, m): Maximum present static draught of the vessel in metres (AIS resolution 0.1 m); 0 = not available, 25.5 = 25.5 m or greater.
- **`Destination`** (string, optional): Free-text destination of the current voyage as up to 20 six-bit ASCII characters (right-padded with '@'), typically a UN/LOCODE or port name; an all-'@' value means not available.
- **`Dte`** (boolean, optional): Data terminal equipment (DTE) readiness flag: false = DTE ready/available, true = DTE not available.
- **`Spare`** (boolean, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
##### Dimension
<a id="payload-io-aisstream-shipstaticdata-dimension"></a>

Reference point for the reported position and overall vessel dimensions, given as distances in metres from the position-fixing antenna to the bow (A), stern (B), port side (C) and starboard side (D); overall length = A + B and beam = C + D.

- **`A`** (int32, required, m): Distance from the position-fixing antenna to the bow of the vessel, in metres (overall length = A + B). 0 = not available.
- **`B`** (int32, required, m): Distance from the position-fixing antenna to the stern of the vessel, in metres. 0 = not available.
- **`C`** (int32, required, m): Distance from the position-fixing antenna to the port side of the vessel, in metres (beam = C + D). 0 = not available.
- **`D`** (int32, required, m): Distance from the position-fixing antenna to the starboard side of the vessel, in metres. 0 = not available.
##### Eta
<a id="payload-io-aisstream-shipstaticdata-eta"></a>

Estimated time of arrival (ETA) at destination, in UTC, encoded as separate month, day, hour and minute fields.

- **`Month`** (int32, required): Estimated time of arrival - month (UTC), 1-12; 0 = not available.
- **`Day`** (int32, required): Estimated time of arrival - day of month (UTC), 1-31; 0 = not available.
- **`Hour`** (int32, required): Estimated time of arrival - hour (UTC), 0-23; 24 = not available.
- **`Minute`** (int32, required): Estimated time of arrival - minute (UTC), 0-59; 60 = not available.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Standard Class B equipment position report (ITU-R M.1371 message 18) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/standard-class-b-position-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Standard Class Bposition Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this standard Class B position report it is 18.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Sog`** (double, optional, [kn_i] (kt)): Speed over ground in knots (aisstream.io reports the decoded value; AIS native resolution is 0.1 kn, 102.3 = not available).
- **`PositionAccuracy`** (boolean, optional): Position accuracy flag: true = high accuracy (better than 10 m, e.g. DGNSS-corrected), false = low accuracy (greater than 10 m, autonomous GNSS).
- **`Longitude`** (double, required, deg (°)): Longitude of the reported position in WGS-84 decimal degrees, east positive (range -180 to 180; 181 = position not available).
- **`Latitude`** (double, required, deg (°)): Latitude of the reported position in WGS-84 decimal degrees, north positive (range -90 to 90; 91 = position not available).
- **`Cog`** (double, optional, deg (°)): Course over ground in degrees true (0-359.9; the encoded value 3600, i.e. 360 degrees, means not available).
- **`TrueHeading`** (int32, optional, deg (°)): Heading in degrees true from the vessel's compass or gyro (0-359); 511 = heading not available.
- **`Timestamp`** (int32, optional): UTC second of the minute (0-59) at which the report was generated by the originating station's electronic position-fixing system; 60 = time stamp not available (default), 61 = positioning system in manual input mode, 62 = positioning system in dead-reckoning mode, 63 = positioning system inoperative.
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`ClassBUnit`** (boolean, optional): Class B unit type flag: true = 'CS' (carrier-sense) unit, false = 'SO' (self-organising) unit.
- **`ClassBDisplay`** (boolean, optional): Class B capability flag: true = the unit is equipped with a display showing received AIS messages.
- **`ClassBDsc`** (boolean, optional): Class B capability flag: true = the unit is equipped with a DSC (digital selective calling) function.
- **`ClassBBand`** (boolean, optional): Class B capability flag: true = the unit can operate over the whole marine band (both AIS channels), false = limited band.
- **`ClassBMsg22`** (boolean, optional): Class B capability flag: true = the unit can accept channel-management commands via Message 22, false = not capable.
- **`AssignedMode`** (boolean, optional): Assigned-mode flag: true = the station's reporting behaviour is controlled by a base station (assigned mode, via message 16/23), false = autonomous mode.
- **`Raim`** (boolean, optional): Receiver Autonomous Integrity Monitoring (RAIM) flag of the position-fixing device: true = RAIM in use, false = RAIM not in use.
- **`CommunicationStateIsItdma`** (boolean, optional): Indicates how to interpret CommunicationState: true = the station is using ITDMA (incremental) access, false = SOTDMA (self-organising) access.
- **`CommunicationState`** (int32, optional): SOTDMA/ITDMA communication state value carrying the synchronisation state and slot time-out / slot-allocation information used by the AIS TDMA link layer.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Extended Class B equipment position report (ITU-R M.1371 message 19) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/extended-class-b-position-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Extended Class Bposition Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this extended Class B position report it is 19.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Sog`** (double, optional, [kn_i] (kt)): Speed over ground in knots (aisstream.io reports the decoded value; AIS native resolution is 0.1 kn, 102.3 = not available).
- **`PositionAccuracy`** (boolean, optional): Position accuracy flag: true = high accuracy (better than 10 m, e.g. DGNSS-corrected), false = low accuracy (greater than 10 m, autonomous GNSS).
- **`Longitude`** (double, required, deg (°)): Longitude of the reported position in WGS-84 decimal degrees, east positive (range -180 to 180; 181 = position not available).
- **`Latitude`** (double, required, deg (°)): Latitude of the reported position in WGS-84 decimal degrees, north positive (range -90 to 90; 91 = position not available).
- **`Cog`** (double, optional, deg (°)): Course over ground in degrees true (0-359.9; the encoded value 3600, i.e. 360 degrees, means not available).
- **`TrueHeading`** (int32, optional, deg (°)): Heading in degrees true from the vessel's compass or gyro (0-359); 511 = heading not available.
- **`Timestamp`** (int32, optional): UTC second of the minute (0-59) at which the report was generated by the originating station's electronic position-fixing system; 60 = time stamp not available (default), 61 = positioning system in manual input mode, 62 = positioning system in dead-reckoning mode, 63 = positioning system inoperative.
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Name`** (string, optional): Name of the vessel as up to 20 six-bit ASCII characters (right-padded with '@'); an all-'@' value means not available.
- **`Type`** (int32, optional): Ship and cargo type code (0-99): the tens digit gives the category (3x = special craft, 6x = passenger, 7x = cargo, 8x = tanker, 9x = other) and the units digit the subtype or hazard class. 0 = not available.
- **`Dimension`** (object, optional): Reference point for the reported position and overall vessel dimensions, given as distances in metres from the position-fixing antenna to the bow (A), stern (B), port side (C) and starboard side (D); overall length = A + B and beam = C + D. See [Dimension](#payload-io-aisstream-extendedclassbpositionreport-dimension).
- **`FixType`** (int32, optional): Type of electronic position-fixing device: 0 = undefined, 1 = GPS, 2 = GLONASS, 3 = combined GPS/GLONASS, 4 = Loran-C, 5 = Chayka, 6 = integrated navigation system, 7 = surveyed, 8 = Galileo, 15 = internal GNSS.
- **`Raim`** (boolean, optional): Receiver Autonomous Integrity Monitoring (RAIM) flag of the position-fixing device: true = RAIM in use, false = RAIM not in use.
- **`Dte`** (boolean, optional): Data terminal equipment (DTE) readiness flag: false = DTE ready/available, true = DTE not available.
- **`AssignedMode`** (boolean, optional): Assigned-mode flag: true = the station's reporting behaviour is controlled by a base station (assigned mode, via message 16/23), false = autonomous mode.
- **`Spare3`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
##### Dimension
<a id="payload-io-aisstream-extendedclassbpositionreport-dimension"></a>

Reference point for the reported position and overall vessel dimensions, given as distances in metres from the position-fixing antenna to the bow (A), stern (B), port side (C) and starboard side (D); overall length = A + B and beam = C + D.

- **`A`** (int32, required, m): Distance from the position-fixing antenna to the bow of the vessel, in metres (overall length = A + B). 0 = not available.
- **`B`** (int32, required, m): Distance from the position-fixing antenna to the stern of the vessel, in metres. 0 = not available.
- **`C`** (int32, required, m): Distance from the position-fixing antenna to the port side of the vessel, in metres (beam = C + D). 0 = not available.
- **`D`** (int32, required, m): Distance from the position-fixing antenna to the starboard side of the vessel, in metres. 0 = not available.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Aids-to-Navigation (AtoN) report (ITU-R M.1371 message 21) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/aids-to-navigation-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Aids To Navigation Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this aids-to-navigation report it is 21.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Type`** (int32, optional): Aid-to-Navigation type code (0-31) per ITU-R M.1371 (e.g. 1 = reference point, 5 = light without sectors, 9 = beacon, 20-31 = cardinal, lateral, special and safe-water marks); 0 = default/type not specified.
- **`Name`** (string, optional): Name of the aid to navigation as up to 20 six-bit ASCII characters (right-padded with '@'); continued in NameExtension when longer than 20 characters.
- **`PositionAccuracy`** (boolean, optional): Position accuracy flag: true = high accuracy (better than 10 m, e.g. DGNSS-corrected), false = low accuracy (greater than 10 m, autonomous GNSS).
- **`Longitude`** (double, required, deg (°)): Longitude of the reported position in WGS-84 decimal degrees, east positive (range -180 to 180; 181 = position not available).
- **`Latitude`** (double, required, deg (°)): Latitude of the reported position in WGS-84 decimal degrees, north positive (range -90 to 90; 91 = position not available).
- **`Dimension`** (object, optional): Reference point for the reported position and overall vessel dimensions, given as distances in metres from the position-fixing antenna to the bow (A), stern (B), port side (C) and starboard side (D); overall length = A + B and beam = C + D. See [Dimension](#payload-io-aisstream-aidstonavigationreport-dimension).
- **`Fixtype`** (int32, optional): Type of electronic position-fixing device: 0 = undefined, 1 = GPS, 2 = GLONASS, 3 = combined GPS/GLONASS, 4 = Loran-C, 5 = Chayka, 6 = integrated navigation system, 7 = surveyed, 8 = Galileo, 15 = internal GNSS.
- **`Timestamp`** (int32, optional): UTC second of the minute (0-59) at which the report was generated by the originating station's electronic position-fixing system; 60 = time stamp not available (default), 61 = positioning system in manual input mode, 62 = positioning system in dead-reckoning mode, 63 = positioning system inoperative.
- **`OffPosition`** (boolean, optional): Off-position flag for the aid to navigation: true = the AtoN is not at its charted position (only meaningful when the time stamp is 0-59).
- **`AtoN`** (int32, optional): Aid-to-Navigation status: eight status/condition bits reserved for regional or competent-authority use; 0 = default.
- **`Raim`** (boolean, optional): Receiver Autonomous Integrity Monitoring (RAIM) flag of the position-fixing device: true = RAIM in use, false = RAIM not in use.
- **`VirtualAtoN`** (boolean, optional): Virtual aid-to-navigation flag: true = a virtual AtoN with no physical structure (synthesised by a base station), false = a real, physical AtoN.
- **`AssignedMode`** (boolean, optional): Assigned-mode flag: true = the station's reporting behaviour is controlled by a base station (assigned mode, via message 16/23), false = autonomous mode.
- **`Spare`** (boolean, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`NameExtension`** (string, optional): Continuation of the aid-to-navigation name beyond the first 20 characters (0-14 additional six-bit ASCII characters); empty when the name fits within the Name field.
##### Dimension
<a id="payload-io-aisstream-aidstonavigationreport-dimension"></a>

Reference point for the reported position and overall vessel dimensions, given as distances in metres from the position-fixing antenna to the bow (A), stern (B), port side (C) and starboard side (D); overall length = A + B and beam = C + D.

- **`A`** (int32, required, m): Distance from the position-fixing antenna to the bow of the vessel, in metres (overall length = A + B). 0 = not available.
- **`B`** (int32, required, m): Distance from the position-fixing antenna to the stern of the vessel, in metres. 0 = not available.
- **`C`** (int32, required, m): Distance from the position-fixing antenna to the port side of the vessel, in metres (beam = C + D). 0 = not available.
- **`D`** (int32, required, m): Distance from the position-fixing antenna to the starboard side of the vessel, in metres. 0 = not available.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Class B static data report (ITU-R M.1371 message 24) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/static-data-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Static Data Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this Class B static data report it is 24.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Reserved`** (int32, optional): Reserved field defined by ITU-R M.1371 for regional or future use; not semantically meaningful.
- **`PartNumber`** (boolean, optional): Selects which part of the Class B static data report this message carries: false (0) = Part A (vessel name), true (1) = Part B (ship type, vendor ID, call sign, dimensions and fix type).
- **`ReportA`** (object, optional): Part A of the Class B static data report, carrying the vessel name (present when PartNumber = 0). See [ReportA](#payload-io-aisstream-staticdatareport-reporta).
- **`ReportB`** (object, optional): Part B of the Class B static data report, carrying ship type, vendor identification, call sign, dimensions and fix type (present when PartNumber = 1). See [ReportB](#payload-io-aisstream-staticdatareport-reportb).
##### ReportA
<a id="payload-io-aisstream-staticdatareport-reporta"></a>

Part A of the Class B static data report, carrying the vessel name (present when PartNumber = 0).

- **`Valid`** (boolean, required): Flag indicating Part A of the static data report was present and successfully decoded.
- **`Name`** (string, required): Name of the vessel from Part A of the static data report, as up to 20 six-bit ASCII characters (right-padded with '@').
##### ReportB
<a id="payload-io-aisstream-staticdatareport-reportb"></a>

Part B of the Class B static data report, carrying ship type, vendor identification, call sign, dimensions and fix type (present when PartNumber = 1).

- **`Valid`** (boolean, required): Flag indicating Part B of the static data report was present and successfully decoded.
- **`ShipType`** (int32, optional): Ship and cargo type code (0-99) reported in Part B of the static data report; 0 = not available.
- **`VendorIDName`** (string, optional): Manufacturer/vendor identifier of the Class B unit (three six-bit ASCII characters of the vendor ID).
- **`VenderIDModel`** (int32, optional): Vendor model code of the Class B unit (manufacturer-assigned equipment model identifier).
- **`VenderIDSerial`** (int32, optional): Vendor serial number of the Class B unit (manufacturer-assigned unit serial number).
- **`CallSign`** (string, optional): International radio call sign of the vessel as up to 7 six-bit ASCII characters (right-padded with '@'); an all-'@' value means not available.
- **`Dimension`** (object, optional): Reference point for the reported position and overall vessel dimensions, given as distances in metres from the position-fixing antenna to the bow (A), stern (B), port side (C) and starboard side (D); overall length = A + B and beam = C + D. See [Dimension](#payload-io-aisstream-staticdatareport-reportb-dimension).
- **`FixType`** (int32, optional): Type of electronic position-fixing device: 0 = undefined, 1 = GPS, 2 = GLONASS, 3 = combined GPS/GLONASS, 4 = Loran-C, 5 = Chayka, 6 = integrated navigation system, 7 = surveyed, 8 = Galileo, 15 = internal GNSS.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
##### Dimension
<a id="payload-io-aisstream-staticdatareport-dimension"></a>

Reference point for the reported position and overall vessel dimensions, given as distances in metres from the position-fixing antenna to the bow (A), stern (B), port side (C) and starboard side (D); overall length = A + B and beam = C + D.

- **`A`** (int32, required, m): Distance from the position-fixing antenna to the bow of the vessel, in metres (overall length = A + B). 0 = not available.
- **`B`** (int32, required, m): Distance from the position-fixing antenna to the stern of the vessel, in metres. 0 = not available.
- **`C`** (int32, required, m): Distance from the position-fixing antenna to the port side of the vessel, in metres (beam = C + D). 0 = not available.
- **`D`** (int32, required, m): Distance from the position-fixing antenna to the starboard side of the vessel, in metres. 0 = not available.
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

A reference record from AISStream public AIS firehose for a station, stop, route, site, or other transport resource. It gives consumers stable identifiers and labels needed to interpret realtime updates. AIS base station report (ITU-R M.1371 message 4) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/base-station-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Base Station Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this base station report it is 4.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`UtcYear`** (int32, optional): UTC year of the base station's time reference (e.g. 2026); 0 = not available.
- **`UtcMonth`** (int32, optional): UTC month of the base station's time reference (1-12); 0 = not available.
- **`UtcDay`** (int32, optional): UTC day of month of the base station's time reference (1-31); 0 = not available.
- **`UtcHour`** (int32, optional): UTC hour of the base station's time reference (0-23); 24 = not available.
- **`UtcMinute`** (int32, optional): UTC minute of the base station's time reference (0-59); 60 = not available.
- **`UtcSecond`** (int32, optional): UTC second of the base station's time reference (0-59); 60 = not available.
- **`PositionAccuracy`** (boolean, optional): Position accuracy flag: true = high accuracy (better than 10 m, e.g. DGNSS-corrected), false = low accuracy (greater than 10 m, autonomous GNSS).
- **`Longitude`** (double, required, deg (°)): Longitude of the reported position in WGS-84 decimal degrees, east positive (range -180 to 180; 181 = position not available).
- **`Latitude`** (double, required, deg (°)): Latitude of the reported position in WGS-84 decimal degrees, north positive (range -90 to 90; 91 = position not available).
- **`FixType`** (int32, optional): Type of electronic position-fixing device: 0 = undefined, 1 = GPS, 2 = GLONASS, 3 = combined GPS/GLONASS, 4 = Loran-C, 5 = Chayka, 6 = integrated navigation system, 7 = surveyed, 8 = Galileo, 15 = internal GNSS.
- **`LongRangeEnable`** (boolean, optional): Flag indicating the base station is able to handle long-range AIS messages: true = capable.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Raim`** (boolean, optional): Receiver Autonomous Integrity Monitoring (RAIM) flag of the position-fixing device: true = RAIM in use, false = RAIM not in use.
- **`CommunicationState`** (int32, optional): SOTDMA/ITDMA communication state value carrying the synchronisation state and slot time-out / slot-allocation information used by the AIS TDMA link layer.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Safety-related broadcast message (ITU-R M.1371 message 14) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/safety-broadcast-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Safety Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this safety-related broadcast message it is 14.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Text`** (string, optional): Free-text safety-related message content, encoded as six-bit ASCII characters.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Standard search-and-rescue (SAR) aircraft position report (ITU-R M.1371 message 9) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/standard-search-and-rescue-aircraft-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Standard Search And Rescue Aircraft Report` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this standard SAR aircraft position report it is 9.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Altitude`** (int32, optional, m): Altitude of the SAR aircraft above sea level in metres (0-4094); 4095 = not available. Derived from GNSS unless AltFromBaro indicates a barometric source.
- **`Sog`** (double, optional, [kn_i] (kt)): Speed over ground in knots (aisstream.io reports the decoded value; AIS native resolution is 0.1 kn, 102.3 = not available).
- **`PositionAccuracy`** (boolean, optional): Position accuracy flag: true = high accuracy (better than 10 m, e.g. DGNSS-corrected), false = low accuracy (greater than 10 m, autonomous GNSS).
- **`Longitude`** (double, required, deg (°)): Longitude of the reported position in WGS-84 decimal degrees, east positive (range -180 to 180; 181 = position not available).
- **`Latitude`** (double, required, deg (°)): Latitude of the reported position in WGS-84 decimal degrees, north positive (range -90 to 90; 91 = position not available).
- **`Cog`** (double, optional, deg (°)): Course over ground in degrees true (0-359.9; the encoded value 3600, i.e. 360 degrees, means not available).
- **`Timestamp`** (int32, optional): UTC second of the minute (0-59) at which the report was generated by the originating station's electronic position-fixing system; 60 = time stamp not available (default), 61 = positioning system in manual input mode, 62 = positioning system in dead-reckoning mode, 63 = positioning system inoperative.
- **`AltFromBaro`** (boolean, optional): Altitude source flag: true = altitude derived from a barometric (QNH) sensor, false = altitude derived from the GNSS receiver.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Dte`** (boolean, optional): Data terminal equipment (DTE) readiness flag: false = DTE ready/available, true = DTE not available.
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`AssignedMode`** (boolean, optional): Assigned-mode flag: true = the station's reporting behaviour is controlled by a base station (assigned mode, via message 16/23), false = autonomous mode.
- **`Raim`** (boolean, optional): Receiver Autonomous Integrity Monitoring (RAIM) flag of the position-fixing device: true = RAIM in use, false = RAIM not in use.
- **`CommunicationStateIsItdma`** (boolean, optional): Indicates how to interpret CommunicationState: true = the station is using ITDMA (incremental) access, false = SOTDMA (self-organising) access.
- **`CommunicationState`** (int32, optional): SOTDMA/ITDMA communication state value carrying the synchronisation state and slot time-out / slot-allocation information used by the AIS TDMA link layer.
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

A vehicle or vessel update from AISStream public AIS firehose. It reports the latest position, movement, identity, or voyage information available from the upstream feed. Long-range AIS broadcast / position report for long-range applications (ITU-R M.1371 message 27) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/long-range-ais-broadcast-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Long Range Ais Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`, `Longitude`, `Latitude`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this long-range AIS broadcast it is 27.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`PositionAccuracy`** (boolean, optional): Position accuracy flag: true = high accuracy (better than 10 m, e.g. DGNSS-corrected), false = low accuracy (greater than 10 m, autonomous GNSS).
- **`Raim`** (boolean, optional): Receiver Autonomous Integrity Monitoring (RAIM) flag of the position-fixing device: true = RAIM in use, false = RAIM not in use.
- **`NavigationalStatus`** (int32, optional): Navigational status code (ITU-R M.1371): 0 = under way using engine, 1 = at anchor, 2 = not under command, 3 = restricted manoeuvrability, 4 = constrained by her draught, 5 = moored, 6 = aground, 7 = engaged in fishing, 8 = under way sailing, 9-13 = reserved/special categories, 14 = AIS-SART/MOB/EPIRB active, 15 = undefined (default).
- **`Longitude`** (double, required, deg (°)): Longitude of the reported position in WGS-84 decimal degrees, east positive, at the reduced 1/10-minute resolution used by long-range reports; 181 = position not available.
- **`Latitude`** (double, required, deg (°)): Latitude of the reported position in WGS-84 decimal degrees, north positive, at the reduced 1/10-minute resolution used by long-range reports; 91 = position not available.
- **`Sog`** (double, optional, [kn_i] (kt)): Speed over ground in knots at the reduced resolution used by long-range reports (0-62); 63 = not available.
- **`Cog`** (double, optional, deg (°)): Course over ground in degrees true at the reduced resolution used by long-range reports (0-359); 511 = not available.
- **`PositionLatency`** (boolean, optional): Position latency flag: false = the reported position is the current GNSS position (latency less than 5 s), true = the reported position may be older than 5 s.
- **`Spare`** (boolean, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Addressed safety-related message (ITU-R M.1371 message 12) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/addressed-safety-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Addressed Safety Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this addressed safety-related message it is 12.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Sequenceinteger`** (int32, optional): Sequence number (0-3) used to pair this addressed message with its acknowledgement (message 7 or 13).
- **`DestinationID`** (int32, optional): Maritime Mobile Service Identity (MMSI) of the addressed destination station this message is sent to.
- **`Retransmission`** (boolean, optional): Retransmission flag: true = this message is a retransmission of a previously sent message, false = first transmission.
- **`Spare`** (boolean, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Text`** (string, optional): Free-text safety-related message content, encoded as six-bit ASCII characters.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Addressed binary message (ITU-R M.1371 message 6) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/addressed-binary-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Addressed Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this addressed binary message it is 6.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Sequenceinteger`** (int32, optional): Sequence number (0-3) used to pair this addressed message with its acknowledgement (message 7 or 13).
- **`DestinationID`** (int32, optional): Maritime Mobile Service Identity (MMSI) of the addressed destination station this message is sent to.
- **`Retransmission`** (boolean, optional): Retransmission flag: true = this message is a retransmission of a previously sent message, false = first transmission.
- **`Spare`** (boolean, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`ApplicationID`** (object, optional): Binary application identifier (ITU-R M.1371 IAI) selecting the application that defines the binary payload; it comprises a Designated Area Code and a Function Identifier. See [ApplicationID](#payload-io-aisstream-addressedbinarymessage-applicationid).
- **`BinaryData`** (string, optional): Application-specific binary payload defined by the application identifier, conveyed as a string of binary data.
##### ApplicationID
<a id="payload-io-aisstream-addressedbinarymessage-applicationid"></a>

Binary application identifier (ITU-R M.1371 IAI) selecting the application that defines the binary payload; it comprises a Designated Area Code and a Function Identifier.

- **`Valid`** (boolean, required): Flag indicating the application identifier (DAC/FI) was present and successfully decoded.
- **`DesignatedAreaCode`** (int32, required): Designated Area Code (DAC) of the application identifier - the maritime jurisdiction or region authority that defines the binary application (e.g. 1 = international).
- **`FunctionIdentifier`** (int32, required): Function Identifier (FI) of the application identifier - selects the specific application message within the Designated Area Code.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Assigned mode command (ITU-R M.1371 message 16) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/assigned-mode-command`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Assigned Mode Command` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this assigned mode command it is 16.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Commands`** (map, optional): Map of the assignment commands carried by this message (keyed by command index, normally two entries), each assigning a destination station MMSI together with a slot offset and increment; the aisstream.io feed encodes each command as a string value.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Binary acknowledgement (ITU-R M.1371 message 7) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/binary-acknowledge`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Binary Acknowledge` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this binary acknowledgement it is 7.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Destinations`** (map, optional): Map of the acknowledged destinations (keyed by index, up to four entries), each identifying an addressed station and the sequence number of the binary message being acknowledged; the aisstream.io feed encodes each entry as a string value.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Binary broadcast message (ITU-R M.1371 message 8) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/binary-broadcast-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Binary Broadcast Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this binary broadcast message it is 8.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`ApplicationID`** (object, optional): Binary application identifier (ITU-R M.1371 IAI) selecting the application that defines the binary payload; it comprises a Designated Area Code and a Function Identifier. See [ApplicationID](#payload-io-aisstream-binarybroadcastmessage-applicationid).
- **`BinaryData`** (string, optional): Application-specific binary payload defined by the application identifier, conveyed as a string of binary data.
##### ApplicationID
<a id="payload-io-aisstream-binarybroadcastmessage-applicationid"></a>

Binary application identifier (ITU-R M.1371 IAI) selecting the application that defines the binary payload; it comprises a Designated Area Code and a Function Identifier.

- **`Valid`** (boolean, required): Flag indicating the application identifier (DAC/FI) was present and successfully decoded.
- **`DesignatedAreaCode`** (int32, required): Designated Area Code (DAC) of the application identifier - the maritime jurisdiction or region authority that defines the binary application (e.g. 1 = international).
- **`FunctionIdentifier`** (int32, required): Function Identifier (FI) of the application identifier - selects the specific application message within the Designated Area Code.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Channel management command (ITU-R M.1371 message 22) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/channel-management`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Channel Management` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this channel management command it is 22.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`ChannelA`** (int32, optional): Primary AIS frequency channel number the command designates as channel A for the region or addressed stations.
- **`ChannelB`** (int32, optional): Secondary AIS frequency channel number the command designates as channel B for the region or addressed stations.
- **`TxRxMode`** (int32, optional): Transmit/receive mode the command sets: 0 = Tx A and Tx B, Rx A and Rx B (default); 1 = Tx A only, Rx A and Rx B; 2 = Tx B only, Rx A and Rx B; 3 = reserved.
- **`LowPower`** (boolean, optional): Transmitter power-level flag for the designated channels: true = low power (1 W), false = high power.
- **`Area`** (object, optional): Rectangular geographic region the channel-management command applies to, defined by two opposite corners (north-east and south-west) in WGS-84 decimal degrees. See [Area](#payload-io-aisstream-channelmanagement-area).
- **`Unicast`** (object, optional): Addressed (unicast) form of the channel-management command, carrying the MMSIs of the one or two stations the command is addressed to (used when IsAddressed is true). See [Unicast](#payload-io-aisstream-channelmanagement-unicast).
- **`IsAddressed`** (boolean, optional): Addressing mode flag: true = the command is addressed to the specific stations in Unicast, false = it applies to the geographic region in Area (broadcast).
- **`BwA`** (boolean, optional): Bandwidth flag for channel A: false = default 25 kHz channel, true = 12.5 kHz channel.
- **`BwB`** (boolean, optional): Bandwidth flag for channel B: false = default 25 kHz channel, true = 12.5 kHz channel.
- **`TransitionalZoneSize`** (int32, optional): Size of the transitional zone around the region, in nautical miles (transmitted value + 1 nm), within which stations may use either the old or the new channel assignment.
- **`Spare4`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
##### Area
<a id="payload-io-aisstream-channelmanagement-area"></a>

Rectangular geographic region the channel-management command applies to, defined by two opposite corners (north-east and south-west) in WGS-84 decimal degrees.

- **`Longitude1`** (double, required, deg (°)): Longitude of the first (north-east) corner of the region the command applies to, in WGS-84 decimal degrees, east positive.
- **`Latitude1`** (double, required, deg (°)): Latitude of the first (north-east) corner of the region the command applies to, in WGS-84 decimal degrees, north positive.
- **`Longitude2`** (double, required, deg (°)): Longitude of the second (south-west) corner of the region the command applies to, in WGS-84 decimal degrees, east positive.
- **`Latitude2`** (double, required, deg (°)): Latitude of the second (south-west) corner of the region the command applies to, in WGS-84 decimal degrees, north positive.
##### Unicast
<a id="payload-io-aisstream-channelmanagement-unicast"></a>

Addressed (unicast) form of the channel-management command, carrying the MMSIs of the one or two stations the command is addressed to (used when IsAddressed is true).

- **`AddressStation1`** (int32, required): MMSI of the first station addressed by the channel-management command.
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`AddressStation2`** (int32, required): MMSI of the second station addressed by the channel-management command.
- **`Spare3`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. UTC and date inquiry (ITU-R M.1371 message 10) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/coordinated-utc-inquiry`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Coordinated Utcinquiry` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this UTC and date inquiry it is 10.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`DestinationID`** (int32, optional): Maritime Mobile Service Identity (MMSI) of the addressed destination station this message is sent to.
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Data link management message (ITU-R M.1371 message 20) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/data-link-management-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Data Link Management Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this data link management message it is 20.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Data`** (map, optional): Map of the TDMA slot reservations carried by this message (keyed by index, up to four entries), each describing a reserved block by slot offset, number of slots, time-out and increment; the aisstream.io feed encodes each reservation as a string value.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. GNSS/DGNSS broadcast binary message (ITU-R M.1371 message 17) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/gnss-broadcast-binary-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Gnss Broadcast Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this GNSS/DGNSS broadcast binary message it is 17.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Longitude`** (double, optional, deg (°)): Longitude of the reported position in WGS-84 decimal degrees, east positive (range -180 to 180; 181 = position not available).
- **`Latitude`** (double, optional, deg (°)): Latitude of the reported position in WGS-84 decimal degrees, north positive (range -90 to 90; 91 = position not available).
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Data`** (string, optional): Differential GNSS (DGNSS) correction payload broadcast by the reference station, conveyed as a string of binary data.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Group assignment command (ITU-R M.1371 message 23) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/group-assignment-command`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Group Assignment Command` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this group assignment command it is 23.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Longitude1`** (double, optional, deg (°)): Longitude of the first (north-east) corner of the region the command applies to, in WGS-84 decimal degrees, east positive.
- **`Latitude1`** (double, optional, deg (°)): Latitude of the first (north-east) corner of the region the command applies to, in WGS-84 decimal degrees, north positive.
- **`Longitude2`** (double, optional, deg (°)): Longitude of the second (south-west) corner of the region the command applies to, in WGS-84 decimal degrees, east positive.
- **`Latitude2`** (double, optional, deg (°)): Latitude of the second (south-west) corner of the region the command applies to, in WGS-84 decimal degrees, north positive.
- **`StationType`** (int32, optional): Station type the assignment applies to: 0 = all stations, 1 = Class A, 2 = all Class B, 3 = SAR airborne, 4 = Class B 'SO', 5 = Class B 'CS', 6 = inland waterways, 10 = base station coverage region (ITU-R M.1371).
- **`ShipType`** (int32, optional): Ship and cargo type code (0-99) selecting which vessels the command applies to; 0 = all types.
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`TxRxMode`** (int32, optional): Transmit/receive mode the command sets: 0 = Tx A and Tx B, Rx A and Rx B (default); 1 = Tx A only, Rx A and Rx B; 2 = Tx B only, Rx A and Rx B; 3 = reserved.
- **`ReportingInterval`** (int32, optional): Assigned reporting interval code (ITU-R M.1371): selects the autonomous reporting rate the addressed stations must use (0 = as autonomously determined, 1 = 10 min, 2 = 6 min, 3 = 3 min, 4 = 1 min, 5 = 30 s, up to 9 = 2 s).
- **`QuietTime`** (int32, optional): Assigned quiet time in minutes (0 = no quiet time; 1-15 = number of minutes during which the addressed stations must not transmit).
- **`Spare3`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Interrogation (ITU-R M.1371 message 15) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/interrogation`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Interrogation` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this interrogation message it is 15.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`Station1Msg1`** (object, optional): First message requested from interrogated station 1: the AIS message type requested and the TDMA slot offset at which the reply should be sent. See [Station1Msg1](#payload-io-aisstream-interrogation-station1msg1).
- **`Station1Msg2`** (object, optional): Second message requested from interrogated station 1 (the same station): an additional AIS message type requested and its reply slot offset. See [Station1Msg2](#payload-io-aisstream-interrogation-station1msg2).
- **`Station2`** (object, optional): Message requested from a second interrogated station: that station's MMSI, the AIS message type requested and the reply slot offset. See [Station2](#payload-io-aisstream-interrogation-station2).
##### Station1Msg1
<a id="payload-io-aisstream-interrogation-station1msg1"></a>

First message requested from interrogated station 1: the AIS message type requested and the TDMA slot offset at which the reply should be sent.

- **`Valid`** (boolean, required): Flag indicating this interrogation request slot was present and successfully decoded.
- **`StationID`** (int32, required): MMSI of the first interrogated station.
- **`MessageID`** (int32, required): AIS message type number requested from the interrogated station.
- **`SlotOffset`** (int32, required): Requested TDMA slot offset at which the interrogated station should transmit its reply (0 = no specific slot requested).
##### Station1Msg2
<a id="payload-io-aisstream-interrogation-station1msg2"></a>

Second message requested from interrogated station 1 (the same station): an additional AIS message type requested and its reply slot offset.

- **`Valid`** (boolean, required): Flag indicating this second interrogation request for station 1 was present and successfully decoded.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`MessageID`** (int32, required): AIS message type number requested from the interrogated station (the second requested message).
- **`SlotOffset`** (int32, required): Requested TDMA slot offset for the reply to the second requested message (0 = no specific slot requested).
##### Station2
<a id="payload-io-aisstream-interrogation-station2"></a>

Message requested from a second interrogated station: that station's MMSI, the AIS message type requested and the reply slot offset.

- **`Valid`** (boolean, required): Flag indicating the second interrogated station's request was present and successfully decoded.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`StationID`** (int32, required): MMSI of the second interrogated station.
- **`MessageID`** (int32, required): AIS message type number requested from the second interrogated station.
- **`SlotOffset`** (int32, required): Requested TDMA slot offset at which the second interrogated station should transmit its reply (0 = no specific slot requested).
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Multiple-slot binary message with communication state (ITU-R M.1371 message 26) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/multi-slot-binary-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Multi Slot Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this multiple-slot binary message with communication state it is 26.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`DestinationIDValid`** (boolean, optional): Flag indicating the message is addressed and the DestinationID field is valid (true) rather than a broadcast (false).
- **`ApplicationIDValid`** (boolean, optional): Flag indicating the application identifier (DAC/FI) is present and the ApplicationID field is valid.
- **`DestinationID`** (int32, optional): Maritime Mobile Service Identity (MMSI) of the addressed destination station this message is sent to.
- **`Spare1`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`ApplicationID`** (object, optional): Binary application identifier (ITU-R M.1371 IAI) selecting the application that defines the binary payload; it comprises a Designated Area Code and a Function Identifier. See [ApplicationID](#payload-io-aisstream-multislotbinarymessage-applicationid).
- **`Payload`** (string, optional): Application-specific binary payload, conveyed as a string of binary data.
- **`Spare2`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`CommunicationStateIsItdma`** (boolean, optional): Indicates how to interpret CommunicationState: true = the station is using ITDMA (incremental) access, false = SOTDMA (self-organising) access.
- **`CommunicationState`** (int32, optional): SOTDMA/ITDMA communication state value carrying the synchronisation state and slot time-out / slot-allocation information used by the AIS TDMA link layer.
##### ApplicationID
<a id="payload-io-aisstream-multislotbinarymessage-applicationid"></a>

Binary application identifier (ITU-R M.1371 IAI) selecting the application that defines the binary payload; it comprises a Designated Area Code and a Function Identifier.

- **`Valid`** (boolean, required): Flag indicating the application identifier (DAC/FI) was present and successfully decoded.
- **`DesignatedAreaCode`** (int32, required): Designated Area Code (DAC) of the application identifier - the maritime jurisdiction or region authority that defines the binary application (e.g. 1 = international).
- **`FunctionIdentifier`** (int32, required): Function Identifier (FI) of the application identifier - selects the specific application message within the Designated Area Code.
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

A transport update from AISStream public AIS firehose. It carries vessel position, voyage, safety, and static AIS messages for AIS-equipped vessels received by the AISStream network. Single-slot binary message (ITU-R M.1371 message 25) relayed by aisstream.io.

#### Identity

Each event identifies the real-world resource with `{UserID}`. `{UserID}` is maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `aisstream`, key `{UserID}` |
| `MQTT/5.0` | topic `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/single-slot-binary-message`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/aisstream`, message subject `{UserID}` |

#### Payload

`Single Slot Binary Message` payloads are JSON object. Required fields: `MessageID`, `UserID`, `Valid`.

- **`MessageID`** (int32, required): AIS message type number per ITU-R M.1371, carried in the first six bits of every AIS message; for this single-slot binary message it is 25.
- **`RepeatIndicator`** (int32, optional): Repeat indicator set by AIS repeater stations to count how many times the message has been repeated: 0 = original transmission, 3 = do not repeat any more.
- **`UserID`** (int32, required): Maritime Mobile Service Identity (MMSI) of the transmitting station - the nine-digit identity of the vessel or station and the partition/event key for this stream.
- **`Valid`** (boolean, required): aisstream.io decoder flag: true = the AIS sentence was decoded successfully and the fields in this message are reliable; false = the message could not be fully decoded.
- **`DestinationIDValid`** (boolean, optional): Flag indicating the message is addressed and the DestinationID field is valid (true) rather than a broadcast (false).
- **`ApplicationIDValid`** (boolean, optional): Flag indicating the application identifier (DAC/FI) is present and the ApplicationID field is valid.
- **`DestinationID`** (int32, optional): Maritime Mobile Service Identity (MMSI) of the addressed destination station this message is sent to.
- **`Spare`** (int32, optional): Spare bits reserved by ITU-R M.1371 for future use; transmitted as zero and carry no semantic meaning.
- **`ApplicationID`** (object, optional): Binary application identifier (ITU-R M.1371 IAI) selecting the application that defines the binary payload; it comprises a Designated Area Code and a Function Identifier. See [ApplicationID](#payload-io-aisstream-singleslotbinarymessage-applicationid).
- **`Payload`** (string, optional): Application-specific binary payload, conveyed as a string of binary data.
##### ApplicationID
<a id="payload-io-aisstream-singleslotbinarymessage-applicationid"></a>

Binary application identifier (ITU-R M.1371 IAI) selecting the application that defines the binary payload; it comprises a Designated Area Code and a Function Identifier.

- **`Valid`** (boolean, required): Flag indicating the application identifier (DAC/FI) was present and successfully decoded.
- **`DesignatedAreaCode`** (int32, required): Designated Area Code (DAC) of the application identifier - the maritime jurisdiction or region authority that defines the binary application (e.g. 1 = international).
- **`FunctionIdentifier`** (int32, required): Function Identifier (FI) of the application identifier - selects the specific application message within the Designated Area Code.
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

- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.

## References

- xRegistry manifest: [`xreg/aisstream.xreg.json`](xreg/aisstream.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
- Azure Service Bus emulator: <https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator>
