# Kystverket AIS Bridge Usage Guide Events

Kystverket AIS publishes vessel position and voyage updates from the Norwegian Coastal Administration for AIS-equipped vessels in Norwegian waters. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 7 documented event types (13 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 7 telemetry event types.
- **Identity:** `{mmsi}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `ais`. The record key is `{mmsi}`. In plain language, `{mmsi}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['ais'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `maritime/no/kystverket/kystverket-ais/+/+/+/+/position-report`, `maritime/no/kystverket/kystverket-ais/+/+/+/+/static`, `maritime/no/kystverket/kystverket-ais/+/+/+/+/aid-to-navigation`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('maritime/no/kystverket/kystverket-ais/+/+/+/+/position-report', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `kystverket-ais`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/kystverket-ais')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Position Report Class A

CloudEvents type: `NO.Kystverket.AIS.PositionReportClassA`

#### What it tells you

A transport update from the Norwegian Coastal Administration. It carries vessel position and voyage updates for AIS-equipped vessels in Norwegian waters.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is provider field for mmsi in this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ais`, key `{mmsi}` |

#### Payload

`Position Report Class A` payloads are JSON object. Required fields: `mmsi`, `longitude`, `latitude`, `timestamp`.

- **`mmsi`** (int32, required): Provider field for mmsi in this record.
- **`navigation_status`** (int32, optional): Provider field for navigation status in this record.
- **`rate_of_turn`** (double, optional): Provider field for rate of turn in this record.
- **`speed_over_ground`** (double, optional): Provider field for speed over ground in this record.
- **`position_accuracy`** (int32, optional): Provider field for position accuracy in this record.
- **`longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`course_over_ground`** (double, optional): Provider field for course over ground in this record.
- **`true_heading`** (int32, optional): Provider field for true heading in this record.
- **`timestamp`** (string, required): Time when the provider recorded or published the update.
- **`station_id`** (string, optional): Stable identifier assigned by the upstream provider for the station or stop.
- **`msg_type`** (int32, optional): Provider field for msg type in this record.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": 0,
  "navigation_status": 0,
  "rate_of_turn": 0,
  "speed_over_ground": 0,
  "position_accuracy": 0,
  "longitude": 0,
  "latitude": 0,
  "course_over_ground": 0,
  "true_heading": 0,
  "timestamp": "string",
  "station_id": "string",
  "msg_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Static Voyage Data

CloudEvents type: `NO.Kystverket.AIS.StaticVoyageData`

#### What it tells you

A transport update from the Norwegian Coastal Administration. It carries vessel position and voyage updates for AIS-equipped vessels in Norwegian waters.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is provider field for mmsi in this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ais`, key `{mmsi}` |

#### Payload

`Static Voyage Data` payloads are JSON object. Required fields: `mmsi`, `timestamp`.

- **`mmsi`** (int32, required): Provider field for mmsi in this record.
- **`imo_number`** (int32, optional): Provider field for imo number in this record.
- **`callsign`** (string, optional): Provider field for callsign in this record.
- **`ship_name`** (string, optional): Human-readable name of the ship.
- **`ship_type`** (int32, optional): Provider field for ship type in this record.
- **`dimension_to_bow`** (int32, optional): Provider field for dimension to bow in this record.
- **`dimension_to_stern`** (int32, optional): Provider field for dimension to stern in this record.
- **`dimension_to_port`** (int32, optional): Provider field for dimension to port in this record.
- **`dimension_to_starboard`** (int32, optional): Provider field for dimension to starboard in this record.
- **`draught`** (double, optional): Provider field for draught in this record.
- **`destination`** (string, optional): Provider field for destination in this record.
- **`eta_month`** (int32, optional): Provider field for eta month in this record.
- **`eta_day`** (int32, optional): Provider field for eta day in this record.
- **`eta_hour`** (int32, optional): Provider field for eta hour in this record.
- **`eta_minute`** (int32, optional): Provider field for eta minute in this record.
- **`timestamp`** (string, required): Time when the provider recorded or published the update.
- **`station_id`** (string, optional): Stable identifier assigned by the upstream provider for the station or stop.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": 0,
  "imo_number": 0,
  "callsign": "string",
  "ship_name": "string",
  "ship_type": 0,
  "dimension_to_bow": 0,
  "dimension_to_stern": 0,
  "dimension_to_port": 0,
  "dimension_to_starboard": 0,
  "draught": 0,
  "destination": "string",
  "eta_month": 0,
  "eta_day": 0,
  "eta_hour": 0,
  "eta_minute": 0,
  "timestamp": "string",
  "station_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Position Report Class B

CloudEvents type: `NO.Kystverket.AIS.PositionReportClassB`

#### What it tells you

A transport update from the Norwegian Coastal Administration. It carries vessel position and voyage updates for AIS-equipped vessels in Norwegian waters.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is provider field for mmsi in this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ais`, key `{mmsi}` |

#### Payload

`Position Report Class B` payloads are JSON object. Required fields: `mmsi`, `longitude`, `latitude`, `timestamp`.

- **`mmsi`** (int32, required): Provider field for mmsi in this record.
- **`speed_over_ground`** (double, optional): Provider field for speed over ground in this record.
- **`position_accuracy`** (int32, optional): Provider field for position accuracy in this record.
- **`longitude`** (double, required): Longitude of the resource in WGS 84 coordinates.
- **`latitude`** (double, required): Latitude of the resource in WGS 84 coordinates.
- **`course_over_ground`** (double, optional): Provider field for course over ground in this record.
- **`true_heading`** (int32, optional): Provider field for true heading in this record.
- **`timestamp`** (string, required): Time when the provider recorded or published the update.
- **`station_id`** (string, optional): Stable identifier assigned by the upstream provider for the station or stop.
- **`msg_type`** (int32, optional): Provider field for msg type in this record.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": 0,
  "speed_over_ground": 0,
  "position_accuracy": 0,
  "longitude": 0,
  "latitude": 0,
  "course_over_ground": 0,
  "true_heading": 0,
  "timestamp": "string",
  "station_id": "string",
  "msg_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Static Data Class B

CloudEvents type: `NO.Kystverket.AIS.StaticDataClassB`

#### What it tells you

A transport update from the Norwegian Coastal Administration. It carries vessel position and voyage updates for AIS-equipped vessels in Norwegian waters.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is provider field for mmsi in this record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ais`, key `{mmsi}` |

#### Payload

`Static Data Class B` payloads are JSON object. Required fields: `mmsi`, `timestamp`.

- **`mmsi`** (int32, required): Provider field for mmsi in this record.
- **`part_number`** (int32, optional): Provider field for part number in this record.
- **`ship_name`** (string, optional): Human-readable name of the ship.
- **`ship_type`** (int32, optional): Provider field for ship type in this record.
- **`callsign`** (string, optional): Provider field for callsign in this record.
- **`dimension_to_bow`** (int32, optional): Provider field for dimension to bow in this record.
- **`dimension_to_stern`** (int32, optional): Provider field for dimension to stern in this record.
- **`dimension_to_port`** (int32, optional): Provider field for dimension to port in this record.
- **`dimension_to_starboard`** (int32, optional): Provider field for dimension to starboard in this record.
- **`timestamp`** (string, required): Time when the provider recorded or published the update.
- **`station_id`** (string, optional): Stable identifier assigned by the upstream provider for the station or stop.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "mmsi": 0,
  "part_number": 0,
  "ship_name": "string",
  "ship_type": 0,
  "callsign": "string",
  "dimension_to_bow": 0,
  "dimension_to_stern": 0,
  "dimension_to_port": 0,
  "dimension_to_starboard": 0,
  "timestamp": "string",
  "station_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Aid To Navigation

CloudEvents type: `NO.Kystverket.AIS.AidToNavigation`

#### What it tells you

A transport update from the Norwegian Coastal Administration. It carries vessel position and voyage updates for AIS-equipped vessels in Norwegian waters.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI as a 9-digit ASCII string (padded with leading zeros). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ais`, key `{mmsi}` |
| `MQTT/5.0` | topic `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/aid-to-navigation`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/kystverket-ais`, message subject `{mmsi}`; application properties flag `{flag}`, ship_type `{ship_type}`, geohash5 `{geohash5}` |

#### Payload

`Aid To Navigation` payloads are JSON object. Required fields: `mmsi`, `flag`, `ship_type`, `geohash5`, `msg_type`, `aid_type`, `latitude`, `longitude`, `ais_msg_type`.

- **`mmsi`** (string, required): Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. Constraints: pattern `^[0-9]{9}$`.
- **`flag`** (string, required): ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. Constraints: pattern `^[a-z]{2}$|^xx$`.
- **`ship_type`** (string, required): Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet.
- **`geohash5`** (string, required): 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. Constraints: pattern `^[0-9b-hjkmnp-z]{5}$`.
- **`msg_type`** (enum, required): Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template.
- **`name`** (string, optional): Aid-to-Navigation name as broadcast.
- **`aid_type`** (int32, required): AtoN type code (0..31) per ITU-R M.1371.
- **`latitude`** (double, required): Reported latitude in WGS-84 decimal degrees.
- **`longitude`** (double, required): Reported longitude in WGS-84 decimal degrees.
- **`position_accuracy`** (int32, optional): 1 if high-accuracy (DGPS), else 0.
- **`timestamp`** (string, optional): ISO-8601 receive time as supplied by the upstream NMEA tag.
- **`station_id`** (string, optional): Kystverket base-station identifier.
- **`ais_msg_type`** (int32, required): Original ITU-R M.1371 message ID (21).
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
  "name": "string",
  "aid_type": 0,
  "latitude": 0,
  "longitude": 0,
  "position_accuracy": 0,
  "timestamp": "string",
  "station_id": "string",
  "ais_msg_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Position Report

CloudEvents type: `NO.Kystverket.AIS.PositionReport`

#### What it tells you

A transport update from the Norwegian Coastal Administration. It carries vessel position and voyage updates for AIS-equipped vessels in Norwegian waters.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI as a 9-digit ASCII string (padded with leading zeros). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ais`, key `{mmsi}` |
| `MQTT/5.0` | topic `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/position-report`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/kystverket-ais`, message subject `{mmsi}`; application properties flag `{flag}`, ship_type `{ship_type}`, geohash5 `{geohash5}` |

#### Payload

`Position Report` payloads are JSON object. Required fields: `mmsi`, `flag`, `ship_type`, `geohash5`, `msg_type`, `latitude`, `longitude`, `ais_msg_type`.

- **`mmsi`** (string, required): Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. Constraints: pattern `^[0-9]{9}$`.
- **`flag`** (string, required): ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. Constraints: pattern `^[a-z]{2}$|^xx$`.
- **`ship_type`** (string, required): Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet.
- **`geohash5`** (string, required): 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. Constraints: pattern `^[0-9b-hjkmnp-z]{5}$`.
- **`msg_type`** (enum, required): Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template.
- **`latitude`** (double, required): Reported latitude in WGS-84 decimal degrees.
- **`longitude`** (double, required): Reported longitude in WGS-84 decimal degrees.
- **`speed_over_ground`** (double, optional): Speed over ground in knots.
- **`course_over_ground`** (double, optional): Course over ground in degrees (0..359.9).
- **`true_heading`** (int32, optional): True heading in degrees (0..359, 511 = not available).
- **`navigation_status`** (int32, optional): ITU navigation status code (0..15). 0 for Class-B.
- **`rate_of_turn`** (double, optional): Rate of turn in AIS-encoded units. 0 for Class-B.
- **`position_accuracy`** (int32, optional): 1 if high-accuracy (DGPS), else 0.
- **`timestamp`** (string, optional): ISO-8601 receive time as supplied by the upstream NMEA tag.
- **`station_id`** (string, optional): Kystverket base-station identifier from the NMEA tag block.
- **`ais_msg_type`** (int32, required): Original ITU-R M.1371 message ID (1, 2, 3, 18, or 19).
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
  "latitude": 0,
  "longitude": 0,
  "speed_over_ground": 0,
  "course_over_ground": 0,
  "true_heading": 0,
  "navigation_status": 0,
  "rate_of_turn": 0,
  "position_accuracy": 0,
  "timestamp": "string",
  "station_id": "string",
  "ais_msg_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Ship Static

CloudEvents type: `NO.Kystverket.AIS.ShipStatic`

#### What it tells you

A transport update from the Norwegian Coastal Administration. It carries vessel position and voyage updates for AIS-equipped vessels in Norwegian waters.

#### Identity

Each event identifies the real-world resource with `{mmsi}`. `{mmsi}` is source MMSI as a 9-digit ASCII string (padded with leading zeros). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ais`, key `{mmsi}` |
| `MQTT/5.0` | topic `maritime/no/kystverket/kystverket-ais/{flag}/{ship_type}/{geohash5}/{mmsi}/static`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/kystverket-ais`, message subject `{mmsi}`; application properties flag `{flag}`, ship_type `{ship_type}`, geohash5 `{geohash5}` |

#### Payload

`Ship Static` payloads are JSON object. Required fields: `mmsi`, `flag`, `ship_type`, `geohash5`, `msg_type`, `ship_type_code`, `ais_msg_type`.

- **`mmsi`** (string, required): Source MMSI as a 9-digit ASCII string (padded with leading zeros). Used as the UNS topic '{mmsi}' placeholder and as the CloudEvents subject. Constraints: pattern `^[0-9]{9}$`.
- **`flag`** (string, required): ISO-3166-1 alpha-2 country code (lower-case) derived from the first three digits of the MMSI via the ITU MID (Maritime Identification Digit) registry. 'xx' is used for MIDs that do not map to a country. Constraints: pattern `^[a-z]{2}$|^xx$`.
- **`ship_type`** (string, required): Kebab-case ship-type bucket derived from the ITU-R M.1371 ShipType code. For static reports it is derived from the broadcast Type-5/24 ShipType field; for position reports it is looked up from an in-process ship-type cache keyed by MMSI. 'unknown' if no static report has been observed yet.
- **`geohash5`** (string, required): 5-character geohash of the reported (latitude, longitude). Approx. 4.9 km x 4.9 km cells at the equator. For messages without a position, filled from the most recently observed position for the MMSI, falling back to '00000'. Constraints: pattern `^[0-9b-hjkmnp-z]{5}$`.
- **`msg_type`** (enum, required): Kebab-case event family used as the trailing UNS topic segment. Always equals the segment baked into the message's MQTT topic template.
- **`ship_name`** (string, optional): Vessel name as broadcast (max 20 chars, trimmed).
- **`callsign`** (string, optional): Radio call sign as broadcast (max 7 chars).
- **`imo_number`** (int32, optional): IMO number (7-digit). 0 if not assigned or for Class-B.
- **`ship_type_code`** (int32, required): Raw ITU-R M.1371 ship type code (0..99).
- **`destination`** (string, optional): Voyage destination string (max 20 chars). Empty for Type 24.
- **`eta`** (string, optional): Voyage ETA as ISO-8601 string. Empty if absent (Type 24).
- **`draught`** (double, optional): Maximum present static draught in metres. 0.0 if absent.
- **`dim_to_bow`** (int32, optional): Distance from reference point to bow in metres.
- **`dim_to_stern`** (int32, optional): Distance from reference point to stern in metres.
- **`dim_to_port`** (int32, optional): Distance from reference point to port side in metres.
- **`dim_to_starboard`** (int32, optional): Distance from reference point to starboard side in metres.
- **`timestamp`** (string, optional): ISO-8601 receive time as supplied by the upstream NMEA tag.
- **`station_id`** (string, optional): Kystverket base-station identifier.
- **`ais_msg_type`** (int32, required): Original ITU-R M.1371 message ID (5 or 24).
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
  "ship_name": "string",
  "callsign": "string",
  "imo_number": 0,
  "ship_type_code": 0,
  "destination": "string",
  "eta": "string",
  "draught": 0,
  "dim_to_bow": 0,
  "dim_to_stern": 0,
  "dim_to_port": 0,
  "dim_to_starboard": 0,
  "timestamp": "string",
  "station_id": "string",
  "ais_msg_type": 0
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

- xRegistry manifest: [`xreg/ais.xreg.json`](xreg/ais.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
