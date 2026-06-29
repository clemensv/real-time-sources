# HSL HFP Events

HSL High-Frequency Positioning (HFP) — Helsinki Region Transport real-time vehicle telemetry. Each upstream HFP message is wrapped verbatim as a CloudEvent and re-emitted over Kafka, MQTT, and AMQP, alongside GTFS reference data (operators, routes, stops).

## At a glance

- **Event types:** 39 documented event types (81 transport bindings in the manifest).
- **Transports:** MQTT/5.0, KAFKA, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 39 telemetry event types.
- **Identity:** `{operator_id}/{vehicle_number}`, `operator/{operator_id}`, `route/{route_id}`, `stop/{stop_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `hsl-hfp`. The record key is `{operator_id}/{vehicle_number}`, `operator/{operator_id}`, `route/{route_id}`, `stop/{stop_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['hsl-hfp'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtts://mqtt.hsl.fi:8883`, `mqtt://localhost:1883` and subscribe to `hfp/v2/journey/+/vp/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/due/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/arr/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/dep/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/ars/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/pde/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/pas/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/wait/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/doo/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/doc/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/vja/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/vjout/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/tlr/+/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/tla/+/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/da/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/dout/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/ba/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/journey/+/bout/+/+/+/+/+/+/+/+/+/+`, `hfp/v2/reference/operator/+`, `hfp/v2/reference/route/+`, `hfp/v2/reference/stop/+`, `/hfp/v2/journey/+/vp/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/due/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/arr/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/dep/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/ars/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/pde/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/pas/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/wait/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/doo/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/doc/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/vja/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/vjout/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/tlr/+/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/tla/+/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/da/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/dout/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/ba/+/+/+/+/+/+/+/+/+/+`, `/hfp/v2/journey/+/bout/+/+/+/+/+/+/+/+/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('hfp/v2/journey/+/vp/+/+/+/+/+/+/+/+/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `hsl-hfp`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/hsl-hfp')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Vp

CloudEvents type: `fi.hsl.hfp.vp`

#### What it tells you

Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an ongoing public journey. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/vp/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Vp` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Due

CloudEvents type: `fi.hsl.hfp.due`

#### What it tells you

The vehicle will soon arrive at a stop. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/due/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Due` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Arr

CloudEvents type: `fi.hsl.hfp.arr`

#### What it tells you

The vehicle has arrived inside a stop's radius. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/arr/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Arr` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Dep

CloudEvents type: `fi.hsl.hfp.dep`

#### What it tells you

The vehicle has departed and left a stop's radius. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/dep/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Dep` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Ars

CloudEvents type: `fi.hsl.hfp.ars`

#### What it tells you

The vehicle has arrived at a stop (stop-position event). Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/ars/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Ars` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Pde

CloudEvents type: `fi.hsl.hfp.pde`

#### What it tells you

The vehicle is ready to depart from a stop. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/pde/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Pde` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Pas

CloudEvents type: `fi.hsl.hfp.pas`

#### What it tells you

The vehicle passes through a stop without stopping. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/pas/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Pas` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Wait

CloudEvents type: `fi.hsl.hfp.wait`

#### What it tells you

The vehicle is waiting at a stop. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/wait/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Wait` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Doo

CloudEvents type: `fi.hsl.hfp.doo`

#### What it tells you

The doors of the vehicle have been opened. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/doo/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Doo` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Doc

CloudEvents type: `fi.hsl.hfp.doc`

#### What it tells you

The doors of the vehicle have been closed. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/doc/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Doc` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Vja

CloudEvents type: `fi.hsl.hfp.vja`

#### What it tells you

The vehicle signs in to a service journey (trip). Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/vja/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Vja` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Vjout

CloudEvents type: `fi.hsl.hfp.vjout`

#### What it tells you

The vehicle signs off from a service journey after the final stop. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`). Mirrors the single HFP v2 payload field table verbatim (the upstream defines one payload object whose populated fields depend on the event type, identified by the CloudEvents `type`).

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/vjout/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Vjout` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Tlr

CloudEvents type: `fi.hsl.hfp.tlr`

#### What it tells you

The vehicle requests traffic-light priority at a junction. Telemetry payload for the traffic-light priority events: the request (`tlr`) and the response (`tla`). Carries the vehicle identity, time and position context plus the `tlp-*`, `sid` and `signal-groupid` priority fields.

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/tlr/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}/{sid}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Tlr` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`tlp_requestid`** (null or int32, optional): Traffic-light priority request ID on the interval [0, 255]. Populated on `tlr` (the request) and echoed on `tla` (the response). Sourced from the HFP payload `tlp-requestid` field. Constraints: minimum `0`, maximum `255`.
- **`tlp_requesttype`** (enum, optional): Type of the traffic-light priority request. One of `NORMAL`, `DOOR_CLOSE`, `DOOR_OPEN` or `ADVANCE`. Populated on `tlr`. Sourced from the HFP payload `tlp-requesttype` field.
- **`tlp_prioritylevel`** (enum, optional): Priority level of the traffic-light priority request. One of `normal`, `high` or `norequest`. Populated on `tlr`. Sourced from the HFP payload `tlp-prioritylevel` field.
- **`tlp_reason`** (enum, optional): Reason for *not* sending a traffic-light priority request. One of `GLOBAL`, `AHEAD`, `LINE` or `PRIOEXEP`. Populated on `tlr`. Sourced from the HFP payload `tlp-reason` field.
- **`tlp_att_seq`** (null or int32, optional): Traffic-light priority request attempt sequence number. Populated on `tlr`. Sourced from the HFP payload `tlp-att-seq` field. Constraints: minimum `0`.
- **`tlp_decision`** (enum, optional): Response decision for the traffic-light priority request. One of `ACK` or `NAK`. Populated on `tla` (the response). Sourced from the HFP payload `tlp-decision` field.
- **`sid`** (null or int32, optional): Junction ID where priority is requested, matching the `sid` topic level. Populated on `tlr` and `tla`. Sourced from the HFP payload `sid` field.
- **`signal_groupid`** (null or int32, optional): Signal-group ID (a group of traffic lights at a junction). Populated on `tlr`. Sourced from the HFP payload `signal-groupid` field.
- **`tlp_signalgroupnbr`** (null or int32, optional): ID of the specific traffic light within the signal group; may be negative. Populated on `tlr`. Sourced from the HFP payload `tlp-signalgroupnbr` field.
- **`tlp_line_configid`** (null or int32, optional): ID of the line configuration in DOI. Populated on `tlr`. Sourced from the HFP payload `tlp-line-configid` field.
- **`tlp_point_configid`** (null or int32, optional): Point configuration ID. Populated on `tlr`. Sourced from the HFP payload `tlp-point-configid` field.
- **`tlp_frequency`** (null or int32, optional): Frequency used for the traffic-light priority request. Populated on `tlr`. Sourced from the HFP payload `tlp-frequency` field.
- **`tlp_protocol`** (null or string, optional): Protocol used for the traffic-light priority request. One of `MQTT` or `KAR-MQTT`. Populated on `tlr`. Sourced from the HFP payload `tlp-protocol` field.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
##### `tlp_requesttype` values

- `NORMAL`
- `DOOR_CLOSE`
- `DOOR_OPEN`
- `ADVANCE`
##### `tlp_prioritylevel` values

- `normal`
- `high`
- `norequest`
##### `tlp_reason` values

- `GLOBAL`
- `AHEAD`
- `LINE`
- `PRIOEXEP`
##### `tlp_decision` values

- `ACK`
- `NAK`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "tlp_requestid": 0,
  "tlp_requesttype": "NORMAL",
  "tlp_prioritylevel": "normal",
  "tlp_reason": "GLOBAL",
  "tlp_att_seq": 0,
  "tlp_decision": "ACK",
  "sid": 0,
  "signal_groupid": 0,
  "tlp_signalgroupnbr": 0,
  "tlp_line_configid": 0,
  "tlp_point_configid": 0,
  "tlp_frequency": 0,
  "tlp_protocol": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Tla

CloudEvents type: `fi.hsl.hfp.tla`

#### What it tells you

The vehicle receives a response to a traffic-light priority request. Telemetry payload for the traffic-light priority events: the request (`tlr`) and the response (`tla`). Carries the vehicle identity, time and position context plus the `tlp-*`, `sid` and `signal-groupid` priority fields.

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/tla/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}/{sid}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Tla` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`tlp_requestid`** (null or int32, optional): Traffic-light priority request ID on the interval [0, 255]. Populated on `tlr` (the request) and echoed on `tla` (the response). Sourced from the HFP payload `tlp-requestid` field. Constraints: minimum `0`, maximum `255`.
- **`tlp_requesttype`** (enum, optional): Type of the traffic-light priority request. One of `NORMAL`, `DOOR_CLOSE`, `DOOR_OPEN` or `ADVANCE`. Populated on `tlr`. Sourced from the HFP payload `tlp-requesttype` field.
- **`tlp_prioritylevel`** (enum, optional): Priority level of the traffic-light priority request. One of `normal`, `high` or `norequest`. Populated on `tlr`. Sourced from the HFP payload `tlp-prioritylevel` field.
- **`tlp_reason`** (enum, optional): Reason for *not* sending a traffic-light priority request. One of `GLOBAL`, `AHEAD`, `LINE` or `PRIOEXEP`. Populated on `tlr`. Sourced from the HFP payload `tlp-reason` field.
- **`tlp_att_seq`** (null or int32, optional): Traffic-light priority request attempt sequence number. Populated on `tlr`. Sourced from the HFP payload `tlp-att-seq` field. Constraints: minimum `0`.
- **`tlp_decision`** (enum, optional): Response decision for the traffic-light priority request. One of `ACK` or `NAK`. Populated on `tla` (the response). Sourced from the HFP payload `tlp-decision` field.
- **`sid`** (null or int32, optional): Junction ID where priority is requested, matching the `sid` topic level. Populated on `tlr` and `tla`. Sourced from the HFP payload `sid` field.
- **`signal_groupid`** (null or int32, optional): Signal-group ID (a group of traffic lights at a junction). Populated on `tlr`. Sourced from the HFP payload `signal-groupid` field.
- **`tlp_signalgroupnbr`** (null or int32, optional): ID of the specific traffic light within the signal group; may be negative. Populated on `tlr`. Sourced from the HFP payload `tlp-signalgroupnbr` field.
- **`tlp_line_configid`** (null or int32, optional): ID of the line configuration in DOI. Populated on `tlr`. Sourced from the HFP payload `tlp-line-configid` field.
- **`tlp_point_configid`** (null or int32, optional): Point configuration ID. Populated on `tlr`. Sourced from the HFP payload `tlp-point-configid` field.
- **`tlp_frequency`** (null or int32, optional): Frequency used for the traffic-light priority request. Populated on `tlr`. Sourced from the HFP payload `tlp-frequency` field.
- **`tlp_protocol`** (null or string, optional): Protocol used for the traffic-light priority request. One of `MQTT` or `KAR-MQTT`. Populated on `tlr`. Sourced from the HFP payload `tlp-protocol` field.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
##### `tlp_requesttype` values

- `NORMAL`
- `DOOR_CLOSE`
- `DOOR_OPEN`
- `ADVANCE`
##### `tlp_prioritylevel` values

- `normal`
- `high`
- `norequest`
##### `tlp_reason` values

- `GLOBAL`
- `AHEAD`
- `LINE`
- `PRIOEXEP`
##### `tlp_decision` values

- `ACK`
- `NAK`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "tlp_requestid": 0,
  "tlp_requesttype": "NORMAL",
  "tlp_prioritylevel": "normal",
  "tlp_reason": "GLOBAL",
  "tlp_att_seq": 0,
  "tlp_decision": "ACK",
  "sid": 0,
  "signal_groupid": 0,
  "tlp_signalgroupnbr": 0,
  "tlp_line_configid": 0,
  "tlp_point_configid": 0,
  "tlp_frequency": 0,
  "tlp_protocol": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Da

CloudEvents type: `fi.hsl.hfp.da`

#### What it tells you

A driver signs in to the vehicle. Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`). These carry a reduced field set — vehicle identity, time, position and driver type — because route, schedule and stop context are not available when the vehicle is not signed on to a public journey.

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/da/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Da` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. Populated on the block events `ba`/`bout`; not populated on the driver sign events `da`/`dout`. Sourced from the HFP payload `oday` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "oday": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Dout

CloudEvents type: `fi.hsl.hfp.dout`

#### What it tells you

A driver signs out of the vehicle. Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`). These carry a reduced field set — vehicle identity, time, position and driver type — because route, schedule and stop context are not available when the vehicle is not signed on to a public journey.

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/dout/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Dout` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. Populated on the block events `ba`/`bout`; not populated on the driver sign events `da`/`dout`. Sourced from the HFP payload `oday` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "oday": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Ba

CloudEvents type: `fi.hsl.hfp.ba`

#### What it tells you

A driver selects the block the vehicle will run. Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`). These carry a reduced field set — vehicle identity, time, position and driver type — because route, schedule and stop context are not available when the vehicle is not signed on to a public journey.

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/ba/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Ba` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. Populated on the block events `ba`/`bout`; not populated on the driver sign events `da`/`dout`. Sourced from the HFP payload `oday` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "oday": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Bout

CloudEvents type: `fi.hsl.hfp.bout`

#### What it tells you

A driver signs out from the selected block (usually at a depot). Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`). These carry a reduced field set — vehicle identity, time, position and driver type — because route, schedule and stop context are not available when the vehicle is not signed on to a public journey.

#### Identity

Each event identifies the real-world resource with `{operator_id}/{vehicle_number}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`); `{vehicle_number}` is zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `{operator_id}/{vehicle_number}` |
| `MQTT/5.0` | topic `hfp/v2/journey/{temporal_type}/bout/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `{operator_id}/{vehicle_number}` |

#### Payload

`Bout` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. Populated on the block events `ba`/`bout`; not populated on the driver sign events `da`/`dout`. Sourced from the HFP payload `oday` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "oday": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Operator

CloudEvents type: `fi.hsl.gtfs.Operator`

#### What it tells you

Reference record describing one HSL transit operator. Reference record for one HSL transit operator, derived from the HFP operator catalogue. Emitted at bridge start-up and refreshed periodically so consumers can resolve the `operator_id` topic level and the payload `oper` field to a named operator without an out-of-band lookup.

#### Identity

Each event identifies the real-world resource with `operator/{operator_id}`. `{operator_id}` is zero-padded 4-digit ID of the *owning* operator, matching the `operator_id` MQTT-topic level (e.g. `0012`, `0060`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `operator/{operator_id}` |
| `MQTT/5.0` | topic `hfp/v2/reference/operator/{operator_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `operator/{operator_id}` |

#### Payload

`Operator` payloads are JSON object. Required fields: `operator_id`, `name`.

- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, matching the `operator_id` MQTT-topic level (e.g. `0012`, `0060`). Stable identifier; used as the CloudEvents subject and Kafka key (prefixed `operator/`) for this reference record. Derived from the HSL HFP operator catalogue. Constraints: pattern `^[0-9]{4}$`.
- **`operator_number`** (null or int32, optional): Numeric operator ID without leading zeroes, matching the HFP payload `oper` field form (e.g. `12`, `60`). Note operator `6` appears only in the payload `oper` field and denotes the same owner as `18`. Derived from the HSL HFP operator catalogue.
- **`name`** (string, required): Operator (transit company) name as published in the HSL HFP operator catalogue, e.g. `Koiviston Auto Oy`, `Suomenlinnan Liikenne Oy`.
- **`note`** (null or string, optional): Free-form note from the operator catalogue, e.g. that multiple smaller operators run under a shared operator ID. `null` when there is no note.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "operator_id": "string",
  "operator_number": 0,
  "name": "string",
  "note": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Route

CloudEvents type: `fi.hsl.gtfs.Route`

#### What it tells you

Reference record describing one HSL route. Reference record for one HSL route, sourced from the HSL GTFS static `routes.txt`. Emitted at bridge start-up and refreshed periodically so consumers can resolve the HFP `route` field / `route_id` topic level to a named route and transit mode.

#### Identity

Each event identifies the real-world resource with `route/{route_id}`. `{route_id}` is GTFS route identifier without the `HSL:` prefix, matching the HFP payload `route` field and the `route_id` topic level (e.g. `2550`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `route/{route_id}` |
| `MQTT/5.0` | topic `hfp/v2/reference/route/{route_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `route/{route_id}` |

#### Payload

`Route` payloads are JSON object. Required fields: `route_id`, `route_type`.

- **`route_id`** (string, required): GTFS route identifier without the `HSL:` prefix, matching the HFP payload `route` field and the `route_id` topic level (e.g. `2550`). Stable identifier; used as the CloudEvents subject and Kafka key (prefixed `route/`). Sourced from `route_id` in the HSL GTFS `routes.txt`.
- **`agency_id`** (null or string, optional): Identifier of the agency that operates the route, a foreign key into the GTFS `agency.txt`. Sourced from the `agency_id` field of `routes.txt`.
- **`route_short_name`** (null or string, optional): Short, public-facing route name shown to riders (e.g. `550`, `H72`); frequently equals the HFP `desi` field. Sourced from the `route_short_name` field of `routes.txt`.
- **`route_long_name`** (null or string, optional): Full, descriptive route name, e.g. `Itäkeskus(M) - Westendinasema`. Sourced from the `route_long_name` field of `routes.txt`.
- **`route_desc`** (null or string, optional): Optional human-readable description providing useful information about the route. Sourced from the `route_desc` field of `routes.txt`.
- **`route_type`** (int32, required): GTFS route type / extended Hierarchical Vehicle Type (HVT) describing the transit mode used on the route. HSL emits both the basic GTFS values — `0` = tram / light rail, `1` = subway / metro, `4` = ferry — and the extended HVT codes — `109` = suburban railway, `700`/`701` = bus, `702` = express bus, `704` = local bus, `900` = funicular. Modeled as an open integer (not a closed enum) because HSL may introduce further HVT codes. Sourced from the `route_type` field of `routes.txt`.
- **`route_url`** (null or string, optional): URL of a web page about the route. Sourced from the `route_url` field of `routes.txt`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "route_id": "string",
  "agency_id": "string",
  "route_short_name": "string",
  "route_long_name": "string",
  "route_desc": "string",
  "route_type": 0,
  "route_url": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Stop

CloudEvents type: `fi.hsl.gtfs.Stop`

#### What it tells you

Reference record describing one HSL stop or station. Reference record for one HSL stop, station or station entrance, sourced from the HSL GTFS static `stops.txt`. Emitted at bridge start-up and refreshed periodically so consumers can resolve the HFP `stop` field / `next_stop` topic level to a named, geolocated stop.

#### Identity

Each event identifies the real-world resource with `stop/{stop_id}`. `{stop_id}` is GTFS stop identifier without the `HSL:` prefix, matching the HFP payload `stop` field and the `next_stop` topic level (e.g. `1130106`). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `hsl-hfp`, key `stop/{stop_id}` |
| `MQTT/5.0` | topic `hfp/v2/reference/stop/{stop_id}`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/hsl-hfp`, message subject `stop/{stop_id}` |

#### Payload

`Stop` payloads are JSON object. Required fields: `stop_id`.

- **`stop_id`** (string, required): GTFS stop identifier without the `HSL:` prefix, matching the HFP payload `stop` field and the `next_stop` topic level (e.g. `1130106`). Stable identifier; used as the CloudEvents subject and Kafka key (prefixed `stop/`). Sourced from `stop_id` in the HSL GTFS `stops.txt`.
- **`stop_code`** (null or string, optional): Short text or number that uniquely identifies the stop for riders (shown on signage and in journey planners), e.g. `H1234`. Sourced from the `stop_code` field of `stops.txt`.
- **`stop_name`** (null or string, optional): Name of the stop, station, or station entrance as shown to riders, e.g. `Rautatientori`. Sourced from the `stop_name` field of `stops.txt`.
- **`stop_desc`** (null or string, optional): Description providing useful, quality information about the stop. Sourced from the `stop_desc` field of `stops.txt`.
- **`stop_lat`** (null or double, optional): WGS84 latitude of the stop in decimal degrees (°), on [-90, 90]. Sourced from the `stop_lat` field of `stops.txt`. Constraints: minimum `-90`, maximum `90`.
- **`stop_lon`** (null or double, optional): WGS84 longitude of the stop in decimal degrees (°), on [-180, 180]. Sourced from the `stop_lon` field of `stops.txt`. Constraints: minimum `-180`, maximum `180`.
- **`zone_id`** (null or string, optional): HSL fare zone the stop belongs to, e.g. `A`, `B`, `C`, `D`. Sourced from the `zone_id` field of `stops.txt`.
- **`stop_url`** (null or string, optional): URL of a web page about the stop. Sourced from the `stop_url` field of `stops.txt`.
- **`location_type`** (null or int32, optional): Type of the location. `0` (or empty) = stop / platform, `1` = station, `2` = station entrance / exit, `3` = generic node, `4` = boarding area. Sourced from the `location_type` field of `stops.txt`. Constraints: minimum `0`, maximum `4`.
- **`parent_station`** (null or string, optional): `stop_id` of the parent station for a platform, entrance or boarding area. Sourced from the `parent_station` field of `stops.txt`.
- **`platform_code`** (null or string, optional): Platform identifier for a platform stop (the part that differs between platforms of a station), e.g. `1`, `B`. Sourced from the `platform_code` field of `stops.txt`.
- **`wheelchair_boarding`** (null or int32, optional): Wheelchair accessibility of boarding at the stop. `0` (or empty) = no information, `1` = some accessible boarding, `2` = no accessible boarding. Sourced from the `wheelchair_boarding` field of `stops.txt`. Constraints: minimum `0`, maximum `2`.
- **`vehicle_type`** (null or int32, optional): HSL extension: the Hierarchical Vehicle Type (extended GTFS route type) of the vehicles that serve this stop, e.g. `0` = tram, `1` = subway, `109` = suburban rail, `700`/`704` = bus, `4` = ferry. Empty when not assigned. Sourced from the non-standard `vehicle_type` field of the HSL `stops.txt`.
- **`digistop_id`** (null or string, optional): HSL extension: internal DigiStop identifier for the stop. Sourced from the non-standard `digistop_id` field of the HSL `stops.txt`. `null` when not present.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "stop_id": "string",
  "stop_code": "string",
  "stop_name": "string",
  "stop_desc": "string",
  "stop_lat": 0,
  "stop_lon": 0,
  "zone_id": "string",
  "stop_url": "string",
  "location_type": 0,
  "parent_station": "string",
  "platform_code": "string",
  "wheelchair_boarding": 0,
  "vehicle_type": 0,
  "digistop_id": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Vp

CloudEvents type: `fi.hsl.hfp.upstream.vp`

#### What it tells you

Upstream HFP `vp` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `VP` key. Vehicle position — the ~1 Hz GPS heartbeat of a vehicle on an ongoing public journey. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/vp/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Vp` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Due

CloudEvents type: `fi.hsl.hfp.upstream.due`

#### What it tells you

Upstream HFP `due` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `DUE` key. The vehicle will soon arrive at a stop. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/due/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Due` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Arr

CloudEvents type: `fi.hsl.hfp.upstream.arr`

#### What it tells you

Upstream HFP `arr` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `ARR` key. The vehicle has arrived inside a stop's radius. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/arr/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Arr` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Dep

CloudEvents type: `fi.hsl.hfp.upstream.dep`

#### What it tells you

Upstream HFP `dep` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `DEP` key. The vehicle has departed and left a stop's radius. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/dep/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Dep` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Ars

CloudEvents type: `fi.hsl.hfp.upstream.ars`

#### What it tells you

Upstream HFP `ars` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `ARS` key. The vehicle has arrived at a stop (stop-position event). Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/ars/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Ars` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Pde

CloudEvents type: `fi.hsl.hfp.upstream.pde`

#### What it tells you

Upstream HFP `pde` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `PDE` key. The vehicle is ready to depart from a stop. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/pde/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Pde` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Pas

CloudEvents type: `fi.hsl.hfp.upstream.pas`

#### What it tells you

Upstream HFP `pas` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `PAS` key. The vehicle passes through a stop without stopping. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/pas/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Pas` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Wait

CloudEvents type: `fi.hsl.hfp.upstream.wait`

#### What it tells you

Upstream HFP `wait` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `WAIT` key. The vehicle is waiting at a stop. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/wait/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Wait` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Doo

CloudEvents type: `fi.hsl.hfp.upstream.doo`

#### What it tells you

Upstream HFP `doo` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `DOO` key. The doors of the vehicle have been opened. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/doo/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Doo` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Doc

CloudEvents type: `fi.hsl.hfp.upstream.doc`

#### What it tells you

Upstream HFP `doc` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `DOC` key. The doors of the vehicle have been closed. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/doc/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Doc` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Vja

CloudEvents type: `fi.hsl.hfp.upstream.vja`

#### What it tells you

Upstream HFP `vja` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `VJA` key. The vehicle signs in to a service journey (trip). Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/vja/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Vja` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Vjout

CloudEvents type: `fi.hsl.hfp.upstream.vjout`

#### What it tells you

Upstream HFP `vjout` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `VJOUT` key. The vehicle signs off from a service journey after the final stop. Telemetry payload shared by the HFP vehicle-position event (`vp`), the stop progress events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`), the door events (`doo`,`doc`) and the service-journey sign events (`vja`,`vjout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/vjout/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Vjout` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`seq`** (null or int32, optional): Sequence number of the unit within a multi-unit consist (e.g. coupled metro or train units), starting at 1. Currently only populated for metros. Sourced from the HFP payload `seq` field. Constraints: minimum `1`.
- **`label`** (null or string, optional): Human-visible label that helps identify the vehicle. Currently only Suomenlinna ferries populate this, with the vessel name. Sourced from the HFP payload `label` field.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`ttarr`** (null or string, optional): UTC timestamp of the scheduled arrival time to the stop related to a stop event, ISO 8601. Populated on the stop and door events (`due`,`arr`,`dep`,`ars`,`pde`,`pas`,`wait`,`doo`,`doc`); absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttarr` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`ttdep`** (null or string, optional): UTC timestamp of the scheduled departure time from the stop related to a stop event, ISO 8601. Populated on the stop and door events; absent on `vp` and on the service-journey sign events. Sourced from the HFP payload `ttdep` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Populated on the service-journey sign events (`vja`,`vjout`). Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "seq": 0,
  "label": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "ttarr": "string",
  "ttdep": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Tlr

CloudEvents type: `fi.hsl.hfp.upstream.tlr`

#### What it tells you

Upstream HFP `tlr` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `TLR` key. The vehicle requests traffic-light priority at a junction. Telemetry payload for the traffic-light priority events: the request (`tlr`) and the response (`tla`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/tlr/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}/{sid}`, retain `not declared`, QoS `0` |

#### Payload

`Tlr` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`tlp_requestid`** (null or int32, optional): Traffic-light priority request ID on the interval [0, 255]. Populated on `tlr` (the request) and echoed on `tla` (the response). Sourced from the HFP payload `tlp-requestid` field. Constraints: minimum `0`, maximum `255`.
- **`tlp_requesttype`** (enum, optional): Type of the traffic-light priority request. One of `NORMAL`, `DOOR_CLOSE`, `DOOR_OPEN` or `ADVANCE`. Populated on `tlr`. Sourced from the HFP payload `tlp-requesttype` field.
- **`tlp_prioritylevel`** (enum, optional): Priority level of the traffic-light priority request. One of `normal`, `high` or `norequest`. Populated on `tlr`. Sourced from the HFP payload `tlp-prioritylevel` field.
- **`tlp_reason`** (enum, optional): Reason for *not* sending a traffic-light priority request. One of `GLOBAL`, `AHEAD`, `LINE` or `PRIOEXEP`. Populated on `tlr`. Sourced from the HFP payload `tlp-reason` field.
- **`tlp_att_seq`** (null or int32, optional): Traffic-light priority request attempt sequence number. Populated on `tlr`. Sourced from the HFP payload `tlp-att-seq` field. Constraints: minimum `0`.
- **`tlp_decision`** (enum, optional): Response decision for the traffic-light priority request. One of `ACK` or `NAK`. Populated on `tla` (the response). Sourced from the HFP payload `tlp-decision` field.
- **`sid`** (null or int32, optional): Junction ID where priority is requested, matching the `sid` topic level. Populated on `tlr` and `tla`. Sourced from the HFP payload `sid` field.
- **`signal_groupid`** (null or int32, optional): Signal-group ID (a group of traffic lights at a junction). Populated on `tlr`. Sourced from the HFP payload `signal-groupid` field.
- **`tlp_signalgroupnbr`** (null or int32, optional): ID of the specific traffic light within the signal group; may be negative. Populated on `tlr`. Sourced from the HFP payload `tlp-signalgroupnbr` field.
- **`tlp_line_configid`** (null or int32, optional): ID of the line configuration in DOI. Populated on `tlr`. Sourced from the HFP payload `tlp-line-configid` field.
- **`tlp_point_configid`** (null or int32, optional): Point configuration ID. Populated on `tlr`. Sourced from the HFP payload `tlp-point-configid` field.
- **`tlp_frequency`** (null or int32, optional): Frequency used for the traffic-light priority request. Populated on `tlr`. Sourced from the HFP payload `tlp-frequency` field.
- **`tlp_protocol`** (null or string, optional): Protocol used for the traffic-light priority request. One of `MQTT` or `KAR-MQTT`. Populated on `tlr`. Sourced from the HFP payload `tlp-protocol` field.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
##### `tlp_requesttype` values

- `NORMAL`
- `DOOR_CLOSE`
- `DOOR_OPEN`
- `ADVANCE`
##### `tlp_prioritylevel` values

- `normal`
- `high`
- `norequest`
##### `tlp_reason` values

- `GLOBAL`
- `AHEAD`
- `LINE`
- `PRIOEXEP`
##### `tlp_decision` values

- `ACK`
- `NAK`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "tlp_requestid": 0,
  "tlp_requesttype": "NORMAL",
  "tlp_prioritylevel": "normal",
  "tlp_reason": "GLOBAL",
  "tlp_att_seq": 0,
  "tlp_decision": "ACK",
  "sid": 0,
  "signal_groupid": 0,
  "tlp_signalgroupnbr": 0,
  "tlp_line_configid": 0,
  "tlp_point_configid": 0,
  "tlp_frequency": 0,
  "tlp_protocol": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Tla

CloudEvents type: `fi.hsl.hfp.upstream.tla`

#### What it tells you

Upstream HFP `tla` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `TLA` key. The vehicle receives a response to a traffic-light priority request. Telemetry payload for the traffic-light priority events: the request (`tlr`) and the response (`tla`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/tla/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}/{sid}`, retain `not declared`, QoS `0` |

#### Payload

`Tla` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`desi`** (null or string, optional): Route number visible to passengers — the public-facing line label shown on the head sign, e.g. `551`, `H72`. Sourced from the HFP payload `desi` field. Not populated on driver/block sign events (`da`,`dout`,`ba`,`bout`).
- **`dir`** (null or string, optional): Route direction of the trip as a string, either `"1"` or `"2"`. After type conversion this matches the `direction_id` topic level; relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`). Sourced from the HFP payload `dir` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`dl`** (null or int32, optional, s): Offset from the scheduled timetable in seconds (s). Negative values indicate the vehicle is lagging behind schedule, positive values indicate running ahead. Sourced from the HFP payload `dl` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. The operating day typically ends around 04:30 local time on the following calendar day, so the final moments of day `2018-04-05` fall at 2018-04-06T04:30 local. Sourced from the HFP payload `oday` field. Not populated on `da`,`dout`. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`jrn`** (null or int32, optional): Internal journey descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `jrn` field.
- **`line`** (null or int32, optional): Internal line descriptor used by HSL. Not meant to be useful for external consumers. Sourced from the HFP payload `line` field.
- **`start`** (null or string, optional): Scheduled start time of the trip — the scheduled departure from the first stop — in `HH:mm` 24-hour local time (not the 30-hour GTFS operating-day clock). Matches the `start_time` topic level. Sourced from the HFP payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`stop`** (null or int32, optional): Numeric GTFS stop ID of the stop related to this event (for example the stop the vehicle departed from for a `dep` event, or the stop it currently sits at for a `vp` event). `null` when the event is not related to any stop. Equals `stop_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Stop`. Sourced from the HFP payload `stop` field, which is a JSON number on the wire (the upstream field table mislabels it as a String; live traffic confirms an integer or null).
- **`route`** (null or string, optional): GTFS route ID the vehicle is currently running on. Matches the `route_id` topic level and `route_id` in GTFS without the `HSL:` prefix; resolve against `fi.hsl.gtfs.Route`. Sourced from the HFP payload `route` field. Not populated on `da`,`dout`,`ba`,`bout`.
- **`occu`** (null or int32, optional): Passenger occupancy level on the interval [0, 100]. Currently only Suomenlinna ferries report a measured value; other vehicles emit `0` (space available, accepting passengers) or `100` (full, may not accept passengers). Sourced from the HFP payload `occu` field. Constraints: minimum `0`, maximum `100`.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`tlp_requestid`** (null or int32, optional): Traffic-light priority request ID on the interval [0, 255]. Populated on `tlr` (the request) and echoed on `tla` (the response). Sourced from the HFP payload `tlp-requestid` field. Constraints: minimum `0`, maximum `255`.
- **`tlp_requesttype`** (enum, optional): Type of the traffic-light priority request. One of `NORMAL`, `DOOR_CLOSE`, `DOOR_OPEN` or `ADVANCE`. Populated on `tlr`. Sourced from the HFP payload `tlp-requesttype` field.
- **`tlp_prioritylevel`** (enum, optional): Priority level of the traffic-light priority request. One of `normal`, `high` or `norequest`. Populated on `tlr`. Sourced from the HFP payload `tlp-prioritylevel` field.
- **`tlp_reason`** (enum, optional): Reason for *not* sending a traffic-light priority request. One of `GLOBAL`, `AHEAD`, `LINE` or `PRIOEXEP`. Populated on `tlr`. Sourced from the HFP payload `tlp-reason` field.
- **`tlp_att_seq`** (null or int32, optional): Traffic-light priority request attempt sequence number. Populated on `tlr`. Sourced from the HFP payload `tlp-att-seq` field. Constraints: minimum `0`.
- **`tlp_decision`** (enum, optional): Response decision for the traffic-light priority request. One of `ACK` or `NAK`. Populated on `tla` (the response). Sourced from the HFP payload `tlp-decision` field.
- **`sid`** (null or int32, optional): Junction ID where priority is requested, matching the `sid` topic level. Populated on `tlr` and `tla`. Sourced from the HFP payload `sid` field.
- **`signal_groupid`** (null or int32, optional): Signal-group ID (a group of traffic lights at a junction). Populated on `tlr`. Sourced from the HFP payload `signal-groupid` field.
- **`tlp_signalgroupnbr`** (null or int32, optional): ID of the specific traffic light within the signal group; may be negative. Populated on `tlr`. Sourced from the HFP payload `tlp-signalgroupnbr` field.
- **`tlp_line_configid`** (null or int32, optional): ID of the line configuration in DOI. Populated on `tlr`. Sourced from the HFP payload `tlp-line-configid` field.
- **`tlp_point_configid`** (null or int32, optional): Point configuration ID. Populated on `tlr`. Sourced from the HFP payload `tlp-point-configid` field.
- **`tlp_frequency`** (null or int32, optional): Frequency used for the traffic-light priority request. Populated on `tlr`. Sourced from the HFP payload `tlp-frequency` field.
- **`tlp_protocol`** (null or string, optional): Protocol used for the traffic-light priority request. One of `MQTT` or `KAR-MQTT`. Populated on `tlr`. Sourced from the HFP payload `tlp-protocol` field.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
##### `tlp_requesttype` values

- `NORMAL`
- `DOOR_CLOSE`
- `DOOR_OPEN`
- `ADVANCE`
##### `tlp_prioritylevel` values

- `normal`
- `high`
- `norequest`
##### `tlp_reason` values

- `GLOBAL`
- `AHEAD`
- `LINE`
- `PRIOEXEP`
##### `tlp_decision` values

- `ACK`
- `NAK`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "desi": "string",
  "dir": "string",
  "dl": 0,
  "oday": "string",
  "jrn": 0,
  "line": 0,
  "start": "string",
  "stop": 0,
  "route": "string",
  "occu": 0,
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "tlp_requestid": 0,
  "tlp_requesttype": "NORMAL",
  "tlp_prioritylevel": "normal",
  "tlp_reason": "GLOBAL",
  "tlp_att_seq": 0,
  "tlp_decision": "ACK",
  "sid": 0,
  "signal_groupid": 0,
  "tlp_signalgroupnbr": 0,
  "tlp_line_configid": 0,
  "tlp_point_configid": 0,
  "tlp_frequency": 0,
  "tlp_protocol": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Da

CloudEvents type: `fi.hsl.hfp.upstream.da`

#### What it tells you

Upstream HFP `da` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `DA` key. A driver signs in to the vehicle. Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/da/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Da` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. Populated on the block events `ba`/`bout`; not populated on the driver sign events `da`/`dout`. Sourced from the HFP payload `oday` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "oday": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Dout

CloudEvents type: `fi.hsl.hfp.upstream.dout`

#### What it tells you

Upstream HFP `dout` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `DOUT` key. A driver signs out of the vehicle. Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/dout/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Dout` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. Populated on the block events `ba`/`bout`; not populated on the driver sign events `da`/`dout`. Sourced from the HFP payload `oday` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "oday": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Ba

CloudEvents type: `fi.hsl.hfp.upstream.ba`

#### What it tells you

Upstream HFP `ba` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `BA` key. A driver selects the block the vehicle will run. Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/ba/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Ba` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. Populated on the block events `ba`/`bout`; not populated on the driver sign events `da`/`dout`. Sourced from the HFP payload `oday` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "oday": "string",
  "dr_type": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Bout

CloudEvents type: `fi.hsl.hfp.upstream.bout`

#### What it tells you

Upstream HFP `bout` message as published by HSL on `mqtt.hsl.fi` — plain JSON (no CloudEvents envelope), with the event object under the single `BOUT` key. A driver signs out from the selected block (usually at a depot). Telemetry payload for the low-frequency driver and block sign events: driver sign-in (`da`), driver sign-out (`dout`), block selection (`ba`) and block sign-out (`bout`).

#### Identity

No CloudEvents `subject` template is declared. Use the transport location and payload identifiers documented below.

#### Where to find it

| Transport | Location |
| --- | --- |
| `MQTT/5.0` | topic `/hfp/v2/journey/{temporal_type}/bout/{transport_mode}/{operator_id}/{vehicle_number}/{route_id}/{direction_id}/{headsign}/{start_time}/{next_stop}/{geohash_level}/{geohash}`, retain `not declared`, QoS `0` |

#### Payload

`Bout` payloads are JSON object. Required fields: `oper`, `veh`, `tst`, `tsi`, `operator_id`, `vehicle_number`.

- **`oper`** (int32, required): Unique numeric ID of the operator *running* the trip. This MAY differ from the `operator_id` MQTT-topic level (the *owning* operator) when a service is subcontracted to another operator. Carries no leading zeroes. Sourced from the HFP payload `oper` field. Resolve against the operator catalogue (`fi.hsl.gtfs.Operator`).
- **`veh`** (int32, required): Vehicle number painted on the side of the vehicle (often next to the front door). Unique only in combination with the operator; different operators may reuse vehicle numbers. Matches the `vehicle_number` topic level without its leading zeroes. Sourced from the HFP payload `veh` field.
- **`tst`** (string, required): UTC timestamp with millisecond precision generated by the vehicle, in ISO 8601 `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`. Sourced from the HFP payload `tst` field. Also surfaced as the CloudEvents `time` attribute. Constraints: pattern `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,9})?(Z|[+-]\d{2}:\d{2})$`.
- **`tsi`** (int32, required): POSIX/Unix time in whole seconds from the vehicle, equal to `tst` truncated to seconds. Sourced from the HFP payload `tsi` field. Modeled as a 32-bit integer so it round-trips as a JSON number (verbatim with the upstream) rather than the stringified form avrotize emits for 64-bit integers; the value stays within int32 range until 2038-01-19.
- **`operator_id`** (string, required): Zero-padded 4-digit ID of the *owning* operator, taken from the `operator_id` MQTT-topic level (e.g. `0055`, `0012`). The stable vehicle-owner identifier (unlike the mutable payload `oper`, which is the *running* operator under subcontracting). Forms the first segment of the CloudEvents subject and Kafka key; resolve against `fi.hsl.gtfs.Operator`. Constraints: pattern `^[0-9]{4}$`.
- **`vehicle_number`** (string, required): Zero-padded vehicle number (4-5 digits) taken from the `vehicle_number` MQTT-topic level (e.g. `01216`). Unique only together with `operator_id`; matches the payload `veh` field without its leading zeroes. Forms the second segment of the CloudEvents subject and Kafka key. Constraints: pattern `^[0-9]{4,5}$`.
- **`temporal_type`** (enum, optional): Journey temporal type from the MQTT-topic level: `ongoing` (journey in progress) or `upcoming` (journey about to start). The bridge subscribes to both; the `deadrun`/`signoff` trees are not consumed.
- **`transport_mode`** (enum, optional): Vehicle transport mode from the MQTT-topic level (`bus`, `tram`, `train`, `ferry`, `metro`, `ubus`, `robot`).
- **`route_id`** (null or string, optional): GTFS route ID from the `route_id` MQTT-topic level (without the `HSL:` prefix), e.g. `2550`. The topic twin of the payload `route` field; `null` when the topic level is empty. Resolve against `fi.hsl.gtfs.Route`.
- **`direction_id`** (null or string, optional): Route direction from the `direction_id` MQTT-topic level, `1` or `2` — the topic twin of the payload `dir` field.
- **`headsign`** (null or string, optional): Vehicle headsign from the MQTT-topic level — the destination shown on the vehicle, e.g. `Eira`. May be empty on the topic. Free-form text.
- **`start_time`** (null or string, optional): Scheduled start time of the trip from the `start_time` MQTT-topic level, in `HH:mm` 24-hour local time — the topic twin of the payload `start` field. Constraints: pattern `^([01]\d|2[0-3]):[0-5]\d$`.
- **`next_stop`** (null or string, optional): Next stop ID from the `next_stop` MQTT-topic level, e.g. `1130106`. The topic carries the literal `EOL` at the end of the line and may be empty, so this is a free-form string (not a numeric stop ID). Resolve numeric values against `fi.hsl.gtfs.Stop`.
- **`geohash_level`** (null or string, optional): Geohash precision level (0-5) from the MQTT-topic level, indicating how many leading digits of the vehicle position have changed since the previous message. Carried as a string to mirror the topic verbatim.
- **`geohash`** (null or string, optional): Slash-delimited geohash of the vehicle position assembled from the trailing MQTT-topic levels (e.g. `60;24/18/71/93`), used by HSL for geographic topic filtering. Carried as a string to mirror the topic verbatim.
- **`spd`** (null or double, optional, m/s): Instantaneous ground speed of the vehicle in metres per second (m/s). Sourced from the HFP payload `spd` field.
- **`hdg`** (null or int32, optional, °): Heading of the vehicle in degrees (°) clockwise from geographic north, on the closed interval [0, 360]. Sourced from the HFP payload `hdg` field. Constraints: minimum `0`, maximum `360`.
- **`lat`** (null or double, optional, °): WGS84 latitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `lat` field. Constraints: minimum `-90`, maximum `90`.
- **`long`** (null or double, optional, °): WGS84 longitude of the vehicle in decimal degrees (°). `null` when the vehicle location is unavailable. Sourced from the HFP payload `long` field (the upstream key is literally `long`). Constraints: minimum `-180`, maximum `180`.
- **`acc`** (null or double, optional, m/s²): Acceleration in metres per second squared (m/s^2), derived from the speed delta between this and the previous message. Negative values indicate the vehicle is decelerating. Sourced from the HFP payload `acc` field.
- **`odo`** (null or int32, optional, m): Odometer reading in metres (m) since the start of the trip. The upstream notes the value is currently not very reliable. Sourced from the HFP payload `odo` field.
- **`drst`** (null or int32, optional): Door status. `0` = all doors closed, `1` = at least one door open. `null` when unknown. Sourced from the HFP payload `drst` field. Constraints: minimum `0`, maximum `1`.
- **`loc`** (null or string, optional): Source of the reported location. One of `GPS` (satellite fix), `ODO` (computed from the odometer), `MAN` (manually set), `DR` (dead reckoning, used in tunnels and other GPS-denied locations) or `N/A` (location unavailable). Sourced from the HFP payload `loc` field.
- **`oday`** (null or string, optional): Operating day of the trip in `YYYY-MM-DD`. Populated on the block events `ba`/`bout`; not populated on the driver sign events `da`/`dout`. Sourced from the HFP payload `oday` field. Constraints: pattern `^\d{4}-\d{2}-\d{2}$`.
- **`dr_type`** (null or int32, optional): Type of the driver. `0` = service technician, `1` = normal driver. Sourced from the HFP payload `dr-type` field. Constraints: minimum `0`, maximum `1`.
##### `temporal_type` values

- `ongoing`
- `upcoming`
##### `transport_mode` values

- `bus`
- `tram`
- `train`
- `ferry`
- `metro`
- `ubus`
- `robot`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "oper": 0,
  "veh": 0,
  "tst": "string",
  "tsi": 0,
  "operator_id": "string",
  "vehicle_number": "string",
  "temporal_type": "ongoing",
  "transport_mode": "bus",
  "route_id": "string",
  "direction_id": "string",
  "headsign": "string",
  "start_time": "string",
  "next_stop": "string",
  "geohash_level": "string",
  "geohash": "string",
  "spd": 0,
  "hdg": 0,
  "lat": 0,
  "long": 0,
  "acc": 0,
  "odo": 0,
  "drst": 0,
  "loc": "string",
  "oday": "string",
  "dr_type": 0
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
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/hsl-hfp.xreg.json`](xreg/hsl-hfp.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Upstream/documentation: <https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/>
- Azure Service Bus Standard namespace: <https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview>
