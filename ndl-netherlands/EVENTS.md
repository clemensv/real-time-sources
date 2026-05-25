# NDW Netherlands Road Traffic Bridge Events

NDL Netherlands publishes road traffic measurements and situation updates from Dutch road-traffic open data feeds for Dutch road network sites and traffic situations. These events help consumers monitor mobility operations, passenger information, and traffic conditions without polling the upstream source directly.

## At a glance

- **Event types:** 3 documented event types (9 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 3 telemetry event types.
- **Identity:** `{site_id}`, `{situation_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `ndl-traffic`, `ndl-traffic-situations`. The record key is `{site_id}`, `{situation_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['ndl-traffic', 'ndl-traffic-situations'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `traffic/nl/ndl/ndl-netherlands/+/+/speed`, `traffic/nl/ndl/ndl-netherlands/+/+/travel-time`, `traffic/nl/ndl/ndl-netherlands/situations/+/+/event`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('traffic/nl/ndl/ndl-netherlands/+/+/speed', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `broker-configured address`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/events')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Traffic Speed

CloudEvents type: `NL.NDW.Traffic.TrafficSpeed`

#### What it tells you

Aggregated traffic speed and flow measurement per road segment from the Dutch NDW DATEX II trafficspeed feed. Each record represents one measurement site with speed averaged and flow summed across all reporting lanes.

#### Identity

Each event identifies the real-world resource with `{site_id}`. `{site_id}` is unique identifier of the NDW measurement site, taken from the DATEX II measurementSiteReference id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndl-traffic`, key `{site_id}` |
| `MQTT/5.0` | topic `traffic/nl/ndl/ndl-netherlands/{road}/{site_id}/speed`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{site_id}` |

#### Payload

`Traffic Speed` payloads are JSON object. Required fields: `site_id`, `measurement_time`, `number_of_lanes_with_data`.

- **`site_id`** (string, required): Unique identifier of the NDW measurement site, taken from the DATEX II measurementSiteReference id attribute. Example: PZH01_MST_0029-00.
- **`measurement_time`** (string, required): Timestamp of the measurement in ISO 8601 format (UTC), from the DATEX II measurementTimeDefault element.
- **`average_speed`** (double or null, optional, km/h): Average vehicle speed in km/h across all lanes with valid data at this site. Null when no lane reported a valid speed (all lanes had speed <= 0).
- **`vehicle_flow_rate`** (int32 or null, optional, vehicles/h): Total vehicle flow rate in vehicles per hour, summed across all lanes at this measurement site. Null when no valid flow data was reported.
- **`number_of_lanes_with_data`** (int32, required): Number of lanes that reported valid measurement data (speed > 0 or flow >= 0) at this measurement site.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_id": "string",
  "measurement_time": "string",
  "average_speed": 0,
  "vehicle_flow_rate": 0,
  "number_of_lanes_with_data": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Travel Time

CloudEvents type: `NL.NDW.Traffic.TravelTime`

#### What it tells you

Travel time measurement for a road segment from the Dutch NDW DATEX II traveltime feed. Each record contains the actual measured travel time and the static free-flow reference time for a measurement site.

#### Identity

Each event identifies the real-world resource with `{site_id}`. `{site_id}` is unique identifier of the NDW measurement site, taken from the DATEX II measurementSiteReference id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndl-traffic`, key `{site_id}` |
| `MQTT/5.0` | topic `traffic/nl/ndl/ndl-netherlands/{road}/{site_id}/travel-time`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{site_id}` |

#### Payload

`Travel Time` payloads are JSON object. Required fields: `site_id`, `measurement_time`.

- **`site_id`** (string, required): Unique identifier of the NDW measurement site, taken from the DATEX II measurementSiteReference id attribute.
- **`measurement_time`** (string, required): Timestamp of the measurement in ISO 8601 format (UTC), from the DATEX II measurementTimeDefault element.
- **`duration`** (double or null, optional, s): Actual measured travel time in seconds for this road segment. Null when the measurement has a data error (duration is -1 in the upstream).
- **`reference_duration`** (double or null, optional, s): Static reference (free-flow) travel time in seconds for this road segment. Null when unavailable or when the measurement has a data error.
- **`accuracy`** (double or null, optional): Accuracy of the travel time measurement as a percentage (0-100), indicating the quality of the sensor coverage.
- **`data_quality`** (double or null, optional): Supplier-calculated data quality score as a percentage (0-100). Higher values indicate more reliable measurements.
- **`number_of_input_values`** (int32 or null, optional): Number of individual vehicle travel times used to compute this aggregate travel time measurement.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "site_id": "string",
  "measurement_time": "string",
  "duration": 0,
  "reference_duration": 0,
  "accuracy": 0,
  "data_quality": 0,
  "number_of_input_values": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Traffic Situation

CloudEvents type: `NL.NDW.Traffic.TrafficSituation`

#### What it tells you

Current traffic situation record from the Dutch NDW DATEX II actueel_beeld (current situation overview) feed. Includes road works, closures, lane management, and other traffic-affecting events on the Dutch road network.

#### Identity

Each event identifies the real-world resource with `{situation_id}`. `{situation_id}` is unique identifier of the traffic situation from the DATEX II situation id attribute. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ndl-traffic-situations`, key `{situation_id}` |
| `MQTT/5.0` | topic `traffic/nl/ndl/ndl-netherlands/situations/{road}/{situation_id}/event`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `broker-configured node`, message subject `{situation_id}` |

#### Payload

`Traffic Situation` payloads are JSON object. Required fields: `situation_id`, `version_time`, `information_status`.

- **`situation_id`** (string, required): Unique identifier of the traffic situation from the DATEX II situation id attribute. Example: RWS01_SM1117672_D2_WWA.
- **`version_time`** (string, required): Timestamp of the latest version of this situation in ISO 8601 format (UTC), from the DATEX II situationVersionTime element.
- **`severity`** (string or null, optional): Overall severity of the situation. Values include: low, medium, high, highest, unknown. Null if not specified.
- **`record_type`** (string or null, optional): DATEX II situation record type indicating the nature of the event. Common values: RoadOrCarriagewayOrLaneManagement, MaintenanceWorks, ConstructionWorks, ReroutingManagement. Null when not available.
- **`cause_type`** (string or null, optional): Cause of the traffic situation. Common values: roadMaintenance, accident, congestion, roadClosed. Null when no cause is specified.
- **`start_time`** (string or null, optional): Start time of the situation validity period in ISO 8601 format (UTC). Null when no validity time specification is provided.
- **`end_time`** (string or null, optional): End time of the situation validity period in ISO 8601 format (UTC). Null when the end time is open-ended or not specified.
- **`information_status`** (string, required): Status of the information: real (confirmed traffic data), test (test data), or exercise (drill/exercise data).
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "situation_id": "string",
  "version_time": "string",
  "severity": "string",
  "record_type": "string",
  "cause_type": "string",
  "start_time": "string",
  "end_time": "string",
  "information_status": "string"
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

## References

- xRegistry manifest: [`xreg/ndl_netherlands.xreg.json`](xreg/ndl_netherlands.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
