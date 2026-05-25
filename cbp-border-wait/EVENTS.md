# US CBP Border Wait Times Events

MQTT/5.0 transport variants for US CBP border wait-time state. Topics are retained QoS-1 leaves under traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/{event}. The border_slug axis is lowercase kebab-case from the CBP border field (canadian-border or mexican-border); port_number preserves the Kafka key and CloudEvents subject. Wait-time snapshots use message expiry so stale retained state ages out if polling stops.

## At a glance

- **Event types:** 2 documented event types (4 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{port_number}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `cbp-border-wait`. The record key is `{port_number}`. In plain language, `{port_number}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['cbp-border-wait'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/us/cbp/cbp-border-wait/+/+/info`, `traffic/us/cbp/cbp-border-wait/+/+/wait-time`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/us/cbp/cbp-border-wait/+/+/info', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Port

CloudEvents type: `gov.cbp.borderwait.Port`

#### What it tells you

Reference data for a US Customs and Border Protection land border port of entry. The CBP Border Wait Time system covers approximately 81 ports along the US-Canada and US-Mexico borders. Each port record identifies the crossing name, operating hours, border (Canadian or Mexican), and current operational status.

#### Identity

Each event identifies the real-world resource with `{port_number}`. `{port_number}` is six-digit CBP port number that uniquely identifies this crossing. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `cbp-border-wait`, key `{port_number}` |
| `MQTT/5.0` | topic `traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/info`, retain `true`, QoS `1` |

#### Payload

`Port` payloads are JSON object. Required fields: `port_number`, `port_name`, `border`, `crossing_name`, `hours`, `passenger_vehicle_max_lanes`, `commercial_vehicle_max_lanes`, `pedestrian_max_lanes`, `border_slug`.

- **`port_number`** (string, required): Six-digit CBP port number that uniquely identifies this crossing. Composed of a district code and a port sequence. Example: '250401' for San Ysidro. This is the stable key used for all wait time lookups. Constraints: pattern `^[0-9]{6}$`.
- **`port_name`** (string, required): Name of the city or locality where the port is located. Example: 'Blaine', 'San Ysidro'. Multiple crossings may share the same port_name.
- **`border`** (string, required): Which international border this port serves. One of 'Canadian Border' or 'Mexican Border'.
- **`crossing_name`** (string, required): Name of the specific border crossing facility. Example: 'Peace Arch', 'Thousand Islands Bridge', 'San Ysidro'. Distinguishes multiple crossings within the same port_name city.
- **`hours`** (string, required): Operating hours of the port as a human-readable string. Examples: '24 hrs/day', '6:00 am - 10:00 pm'. Empty string if not reported.
- **`passenger_vehicle_max_lanes`** (integer or null, required): Maximum number of passenger vehicle inspection lanes available at this crossing. Null if passenger vehicle processing is not available at this port.
- **`commercial_vehicle_max_lanes`** (integer or null, required): Maximum number of commercial vehicle inspection lanes available at this crossing. Null if commercial vehicle processing is not available at this port.
- **`pedestrian_max_lanes`** (integer or null, required): Maximum number of pedestrian inspection lanes available at this crossing. Null if pedestrian processing is not available at this port.
- **`border_slug`** (enum, required): Lowercase kebab-case MQTT/UNS routing segment derived from the CBP border field. Expected values are canadian-border or mexican-border. Constraints: pattern `^[a-z0-9]+(-[a-z0-9]+)*$`.
##### `border_slug` values

- `canadian-border`
- `mexican-border`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "port_number": "string",
  "port_name": "string",
  "border": "string",
  "crossing_name": "string",
  "hours": "string",
  "passenger_vehicle_max_lanes": 0,
  "commercial_vehicle_max_lanes": 0,
  "pedestrian_max_lanes": 0,
  "border_slug": "canadian-border"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Wait Time

CloudEvents type: `gov.cbp.borderwait.WaitTime`

#### What it tells you

Current wait times at a US land border port of entry, flattened from the CBP nested lane structure. Reports delay in minutes and number of open lanes for each combination of traveler category (passenger vehicle, pedestrian, commercial vehicle) and lane type (standard, SENTRI/NEXUS, Ready Lane, FAST). Wait times are updated approximately every hour by CBP officers at each port.

#### Identity

Each event identifies the real-world resource with `{port_number}`. `{port_number}` is six-digit CBP port number identifying this crossing. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `cbp-border-wait`, key `{port_number}` |
| `MQTT/5.0` | topic `traffic/us/cbp/cbp-border-wait/{border_slug}/{port_number}/wait-time`, retain `true`, QoS `1` |

#### Payload

`Wait Time` payloads are JSON object. Required fields: `port_number`, `port_name`, `border`, `crossing_name`, `port_status`, `date`, `time`, `passenger_vehicle_standard_delay`, `passenger_vehicle_standard_lanes_open`, `passenger_vehicle_standard_operational_status`, `passenger_vehicle_nexus_sentri_delay`, `passenger_vehicle_nexus_sentri_lanes_open`, `passenger_vehicle_nexus_sentri_operational_status`, `passenger_vehicle_ready_delay`, `passenger_vehicle_ready_lanes_open`, `passenger_vehicle_ready_operational_status`, `pedestrian_standard_delay`, `pedestrian_standard_lanes_open`, `pedestrian_standard_operational_status`, `pedestrian_ready_delay`, `pedestrian_ready_lanes_open`, `pedestrian_ready_operational_status`, `commercial_vehicle_standard_delay`, `commercial_vehicle_standard_lanes_open`, `commercial_vehicle_standard_operational_status`, `commercial_vehicle_fast_delay`, `commercial_vehicle_fast_lanes_open`, `commercial_vehicle_fast_operational_status`, `construction_notice`, `border_slug`.

- **`port_number`** (string, required): Six-digit CBP port number identifying this crossing. Matches the port_number in the Port schema. Constraints: pattern `^[0-9]{6}$`.
- **`port_name`** (string, required): Name of the city or locality where the port is located.
- **`border`** (string, required): Which international border this port serves. One of 'Canadian Border' or 'Mexican Border'.
- **`crossing_name`** (string, required): Name of the specific border crossing facility.
- **`port_status`** (string, required): Overall operational status of the port. Typically 'Open' when the port is accepting traffic.
- **`date`** (string, required): Date of the wait time report in US format (M/D/YYYY) as provided by CBP. Example: '4/8/2026'.
- **`time`** (string, required): Time of the wait time report in HH:MM:SS format as provided by CBP, in the port's local time zone. Example: '16:16:47'.
- **`passenger_vehicle_standard_delay`** (integer or null, required, min): Delay in minutes for standard (non-trusted-traveler) passenger vehicle lanes. Null when the lane type is not available at this port (operational_status 'N/A').
- **`passenger_vehicle_standard_lanes_open`** (integer or null, required): Number of standard passenger vehicle lanes currently open. Null when not available.
- **`passenger_vehicle_standard_operational_status`** (string or null, required): Operational status of standard passenger vehicle lanes. Values: 'no delay', 'delay', 'N/A', 'Lanes Closed', 'Update Pending'. Null when not reported.
- **`passenger_vehicle_nexus_sentri_delay`** (integer or null, required, min): Delay in minutes for NEXUS (Canadian border) or SENTRI (Mexican border) trusted-traveler passenger vehicle lanes. Null when not available.
- **`passenger_vehicle_nexus_sentri_lanes_open`** (integer or null, required): Number of NEXUS/SENTRI trusted-traveler passenger vehicle lanes currently open. Null when not available.
- **`passenger_vehicle_nexus_sentri_operational_status`** (string or null, required): Operational status of NEXUS/SENTRI passenger vehicle lanes. Null when not reported.
- **`passenger_vehicle_ready_delay`** (integer or null, required, min): Delay in minutes for Ready Lane passenger vehicle lanes. Ready Lanes accept RFID-enabled documents for expedited processing. Null when not available.
- **`passenger_vehicle_ready_lanes_open`** (integer or null, required): Number of Ready Lane passenger vehicle lanes currently open. Null when not available.
- **`passenger_vehicle_ready_operational_status`** (string or null, required): Operational status of Ready Lane passenger vehicle lanes. Null when not reported.
- **`pedestrian_standard_delay`** (integer or null, required, min): Delay in minutes for standard pedestrian lanes. Null when pedestrian processing is not available at this port.
- **`pedestrian_standard_lanes_open`** (integer or null, required): Number of standard pedestrian lanes currently open. Null when not available.
- **`pedestrian_standard_operational_status`** (string or null, required): Operational status of standard pedestrian lanes. Null when not reported.
- **`pedestrian_ready_delay`** (integer or null, required, min): Delay in minutes for Ready Lane pedestrian lanes. Null when not available.
- **`pedestrian_ready_lanes_open`** (integer or null, required): Number of Ready Lane pedestrian lanes currently open. Null when not available.
- **`pedestrian_ready_operational_status`** (string or null, required): Operational status of Ready Lane pedestrian lanes. Null when not reported.
- **`commercial_vehicle_standard_delay`** (integer or null, required, min): Delay in minutes for standard commercial vehicle lanes. Null when commercial processing is not available at this port.
- **`commercial_vehicle_standard_lanes_open`** (integer or null, required): Number of standard commercial vehicle lanes currently open. Null when not available.
- **`commercial_vehicle_standard_operational_status`** (string or null, required): Operational status of standard commercial vehicle lanes. Null when not reported.
- **`commercial_vehicle_fast_delay`** (integer or null, required, min): Delay in minutes for FAST (Free and Secure Trade) trusted-traveler commercial vehicle lanes. Null when not available.
- **`commercial_vehicle_fast_lanes_open`** (integer or null, required): Number of FAST commercial vehicle lanes currently open. Null when not available.
- **`commercial_vehicle_fast_operational_status`** (string or null, required): Operational status of FAST commercial vehicle lanes. Null when not reported.
- **`construction_notice`** (string or null, required): Free-text construction or closure notice for the port. Empty string or null when no notice is active.
- **`border_slug`** (enum, required): Lowercase kebab-case MQTT/UNS routing segment derived from the CBP border field. Expected values are canadian-border or mexican-border. Constraints: pattern `^[a-z0-9]+(-[a-z0-9]+)*$`.
##### `border_slug` values

- `canadian-border`
- `mexican-border`
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "port_number": "string",
  "port_name": "string",
  "border": "string",
  "crossing_name": "string",
  "port_status": "string",
  "date": "string",
  "time": "string",
  "passenger_vehicle_standard_delay": 0,
  "passenger_vehicle_standard_lanes_open": 0,
  "passenger_vehicle_standard_operational_status": "string",
  "passenger_vehicle_nexus_sentri_delay": 0,
  "passenger_vehicle_nexus_sentri_lanes_open": 0,
  "passenger_vehicle_nexus_sentri_operational_status": "string",
  "passenger_vehicle_ready_delay": 0,
  "passenger_vehicle_ready_lanes_open": 0,
  "passenger_vehicle_ready_operational_status": "string",
  "pedestrian_standard_delay": 0,
  "pedestrian_standard_lanes_open": 0,
  "pedestrian_standard_operational_status": "string",
  "pedestrian_ready_delay": 0,
  "pedestrian_ready_lanes_open": 0,
  "pedestrian_ready_operational_status": "string",
  "commercial_vehicle_standard_delay": 0,
  "commercial_vehicle_standard_lanes_open": 0,
  "commercial_vehicle_standard_operational_status": "string",
  "commercial_vehicle_fast_delay": 0,
  "commercial_vehicle_fast_lanes_open": 0,
  "commercial_vehicle_fast_operational_status": "string",
  "construction_notice": "string",
  "border_slug": "canadian-border"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/cbp_border_wait.xreg.json`](xreg/cbp_border_wait.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
