# VATSIM feeder Events

MQTT/5.0 transport variant for VATSIM live network data. Non-retained QoS-1 streams split pilots, controllers, and network facility status into distinct UNS topic branches under aviation-network/intl/vatsim/vatsim/...

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type and 2 telemetry event types.
- **Identity:** `{callsign}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `vatsim`. The record key is `{callsign}`. In plain language, `{callsign}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['vatsim'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `aviation-network/intl/vatsim/vatsim/pilots/+/pilot-position`, `aviation-network/intl/vatsim/vatsim/controllers/+/controller-position`, `aviation-network/intl/vatsim/vatsim/facilities/+/facility-status`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('aviation-network/intl/vatsim/vatsim/pilots/+/pilot-position', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `vatsim`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/vatsim')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Pilot Position

CloudEvents type: `net.vatsim.PilotPosition`

#### What it tells you

Current position, flight plan summary, and state of a pilot connected to the VATSIM virtual aviation network. Updated every 15 seconds at the source.

#### Identity

Each event identifies the real-world resource with `{callsign}`. `{callsign}` is ATC-style callsign chosen by the pilot for this session (e.g. 'BAW123', 'N12345'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `vatsim`, key `{callsign}` |
| `MQTT/5.0` | topic `aviation-network/intl/vatsim/vatsim/pilots/{callsign}/pilot-position`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/vatsim`, message subject `{callsign}` |

#### Payload

`Pilot Position` payloads are JSON object. Required fields: `cid`, `callsign`, `latitude`, `longitude`, `altitude`, `groundspeed`, `heading`, `transponder`, `qnh_mb`, `pilot_rating`, `last_updated`.

- **`cid`** (int32, required): VATSIM Certificate Identifier (CID) — unique numeric member ID.
- **`callsign`** (string, required): ATC-style callsign chosen by the pilot for this session (e.g. 'BAW123', 'N12345').
- **`latitude`** (double, required, degree (°)): Aircraft latitude in decimal degrees (WGS-84). Positive is north.
- **`longitude`** (double, required, degree (°)): Aircraft longitude in decimal degrees (WGS-84). Positive is east.
- **`altitude`** (int32, required, foot (ft)): Indicated altitude of the aircraft in feet above mean sea level.
- **`groundspeed`** (int32, required, knot (kn)): Ground speed of the aircraft in knots.
- **`heading`** (int32, required, degree (°)): Magnetic heading of the aircraft in degrees (0-359).
- **`transponder`** (string, required): Four-digit transponder (squawk) code currently set by the pilot.
- **`qnh_mb`** (int32, required, millibar (mb)): Altimeter setting (QNH) in millibars / hectopascals as reported by the pilot client.
- **`flight_rules`** (string or null, optional): Flight rules filed in the flight plan: 'I' for Instrument Flight Rules, 'V' for Visual Flight Rules. Null if no flight plan is filed.
- **`aircraft_short`** (string or null, optional): ICAO aircraft type designator from the filed flight plan (e.g. 'B738', 'A320'). Null if no flight plan is filed.
- **`departure`** (string or null, optional): ICAO code of the departure airport from the filed flight plan. Null if no flight plan is filed.
- **`arrival`** (string or null, optional): ICAO code of the arrival airport from the filed flight plan. Null if no flight plan is filed.
- **`route`** (string or null, optional): Route string from the filed flight plan. Null if no flight plan is filed.
- **`cruise_altitude`** (string or null, optional): Planned cruise altitude or flight level from the filed flight plan (e.g. '36000' or 'FL350'). Null if no flight plan is filed.
- **`pilot_rating`** (int32, required): VATSIM pilot rating bitmask. 0 = New Member (P0), 1 = PPL, 3 = IR, 7 = CMEL, 15 = ATPL.
- **`last_updated`** (string, required): UTC timestamp of the last position update received by the VATSIM data servers (RFC3339 string).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "cid": 0,
  "callsign": "string",
  "latitude": 0,
  "longitude": 0,
  "altitude": 0,
  "groundspeed": 0,
  "heading": 0,
  "transponder": "string",
  "qnh_mb": 0,
  "flight_rules": "string",
  "aircraft_short": "string",
  "departure": "string",
  "arrival": "string",
  "route": "string",
  "cruise_altitude": "string",
  "pilot_rating": 0,
  "last_updated": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Controller Position

CloudEvents type: `net.vatsim.ControllerPosition`

#### What it tells you

Current state and frequency of an air traffic controller connected to the VATSIM virtual aviation network. Current state and frequency of an air traffic controller or observer connected to the VATSIM virtual aviation network.

#### Identity

Each event identifies the real-world resource with `{callsign}`. `{callsign}` is controller position callsign (e.g. 'EGLL_TWR', 'KJFK_APP'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `vatsim`, key `{callsign}` |
| `MQTT/5.0` | topic `aviation-network/intl/vatsim/vatsim/controllers/{callsign}/controller-position`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/vatsim`, message subject `{callsign}` |

#### Payload

`Controller Position` payloads are JSON object. Required fields: `cid`, `callsign`, `frequency`, `facility`, `rating`, `last_updated`.

- **`cid`** (int32, required): VATSIM Certificate Identifier (CID) — unique numeric member ID.
- **`callsign`** (string, required): Controller position callsign (e.g. 'EGLL_TWR', 'KJFK_APP').
- **`frequency`** (string, required): Radio frequency the controller is operating on, in MHz with three decimal places (e.g. '118.500').
- **`facility`** (int32, required): VATSIM facility type code. 0 = Observer, 1 = Flight Service Station, 2 = Delivery, 3 = Ground, 4 = Tower, 5 = Approach/Departure, 6 = Center/Enroute.
- **`rating`** (int32, required): VATSIM ATC rating. 1 = OBS, 2 = S1, 3 = S2, 4 = S3, 5 = C1, 6 = C2, 7 = C3, 8 = I1, 9 = I2, 10 = I3, 11 = SUP, 12 = ADM.
- **`text_atis`** (string or null, optional): Controller information or ATIS text, with individual lines joined by newline characters. Null when the controller has not set any ATIS text.
- **`last_updated`** (string, required): UTC timestamp of the last update received by the VATSIM data servers (RFC3339 string).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "cid": 0,
  "callsign": "string",
  "frequency": "string",
  "facility": 0,
  "rating": 0,
  "text_atis": "string",
  "last_updated": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Network Status

CloudEvents type: `net.vatsim.NetworkStatus`

#### What it tells you

Aggregate network status snapshot from the VATSIM data feed, emitted once per poll cycle. Aggregate VATSIM network status snapshot emitted once per poll cycle, summarising connected client counts.

#### Identity

Each event identifies the real-world resource with `{callsign}`. `{callsign}` is constant key value 'status' used to identify this network status record. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `vatsim`, key `{callsign}` |
| `MQTT/5.0` | topic `aviation-network/intl/vatsim/vatsim/facilities/{facility}/facility-status`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/vatsim`, message subject `{callsign}`; application properties facility `{facility}` |

#### Payload

`Network Status` payloads are JSON object. Required fields: `callsign`, `update_timestamp`, `connected_clients`, `unique_users`, `pilot_count`, `controller_count`, `facility`.

- **`callsign`** (string, required): Constant key value 'status' used to identify this network status record.
- **`update_timestamp`** (string, required): UTC timestamp of the VATSIM data snapshot as reported by the data feed (RFC3339 string).
- **`connected_clients`** (int32, required): Total number of clients (pilots, controllers, observers) currently connected to the network.
- **`unique_users`** (int32, required): Number of unique VATSIM user IDs currently connected.
- **`pilot_count`** (int32, required): Number of pilots currently connected and flying.
- **`controller_count`** (int32, required): Number of controllers (including observers) currently connected and providing ATC services.
- **`facility`** (string, required): UNS facility identifier for this aggregate VATSIM network status snapshot. The bridge emits 'network'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "callsign": "string",
  "update_timestamp": "string",
  "connected_clients": 0,
  "unique_users": 0,
  "pilot_count": 0,
  "controller_count": 0,
  "facility": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. Consumers should cache it and use it to interpret telemetry events that share the same identity.

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

- xRegistry manifest: [`xreg/vatsim.xreg.json`](xreg/vatsim.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
