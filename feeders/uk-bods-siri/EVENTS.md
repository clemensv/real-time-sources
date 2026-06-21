# UK BODS SIRI event reference

UK BODS SIRI now runs as a configuration-only wrapper over the generalized siri feeder. It emits the org.siri CloudEvents contract for BODS VehicleMonitoring payloads.

## At a glance

- **Event types:** 2 documented event types (8 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 1 reference/catalog event type (`org.siri.Operator`) and 1 telemetry event type (`org.siri.VehiclePosition`).
- **Identity:** `{operator_ref}/{vehicle_ref}`, `{operator_ref}` identifies the resource each event is about.
- **Operations:** The checked-in guide documents a default polling interval of 30 seconds.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `siri`. The record key is `{operator_ref}/{vehicle_ref}`. In plain language, `{operator_ref}/{vehicle_ref}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['siri'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `transit/siri/+/+/position`, `transit/siri/+/info`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('transit/siri/+/+/position', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `siri`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/siri')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Vehicle Position

CloudEvents type: `org.siri.VehiclePosition`

#### What it tells you

One current SIRI VehicleActivity observation from a configured provider feed. Each event represents the latest monitored vehicle journey state for one physical vehicle at one poll cycle. Normalized payload for one SIRI 2.0 VehicleActivity element emitted by a configured provider feed.

#### Identity

Each event identifies the real-world resource with `{operator_ref}/{vehicle_ref}`. `{operator_ref}` is operator identifier from `MonitoredVehicleJourney/OperatorRef`; `{vehicle_ref}` is operator-scoped vehicle identifier from `MonitoredVehicleJourney/VehicleRef`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `siri`, key `{operator_ref}/{vehicle_ref}` |
| `MQTT/5.0` | topic `transit/siri/{operator_ref}/{vehicle_ref}/position`, retain `false`, QoS `0` |
| `AMQP/1.0` | source address `amqps://localhost:5671/siri`, message subject `{operator_ref}/{vehicle_ref}` |

#### Payload

`Vehicle Position` payloads are JSON object. Required fields: `operator_ref`, `vehicle_ref`, `line_ref`, `direction_ref`, `published_line_name`, `origin_ref`, `origin_name`, `destination_ref`, `destination_name`, `longitude`, `latitude`, `bearing`, `recorded_at_time`, `valid_until_time`, `block_ref`, `vehicle_journey_ref`, `origin_aimed_departure_time`, `data_frame_ref`, `dated_vehicle_journey_ref`, `item_identifier`.

- **`operator_ref`** (string, required): Operator identifier from `MonitoredVehicleJourney/OperatorRef`. The exact coding scheme depends on the configured provider, but the value remains the stable operator identity used for reference records, CloudEvents subjects, Kafka keys, MQTT topic segments, and AMQP routing properties.
- **`vehicle_ref`** (string, required): Operator-scoped vehicle identifier from `MonitoredVehicleJourney/VehicleRef`. Usually the fleet number or run identifier configured in the operator AVL system. Combined with `operator_ref` it forms the stable vehicle identity for CloudEvents subjects and transport routing.
- **`line_ref`** (string or null, required): Service or route identifier from `MonitoredVehicleJourney/LineRef`. Providers use this value to align the monitored vehicle journey with published line or trip definitions. Null when the source omits a line identifier for the monitored journey.
- **`direction_ref`** (string or null, required): Direction label from `MonitoredVehicleJourney/DirectionRef`, such as `inbound` or `outbound`. Providers use this together with line and dated journey references to align live positions with the scheduled journey pattern.
- **`published_line_name`** (string or null, required): Public-facing route label from `MonitoredVehicleJourney/PublishedLineName`, for example `T12`. This is the human-readable service number or line name shown to passengers.
- **`origin_ref`** (string or null, required): Stop reference from `MonitoredVehicleJourney/OriginRef` naming the first advertised stop of the monitored journey. Null when the provider omits the origin stop code.
- **`origin_name`** (string or null, required): Human-readable stop name from `MonitoredVehicleJourney/OriginName` for the first advertised stop of the monitored journey.
- **`destination_ref`** (string or null, required): Stop reference from `MonitoredVehicleJourney/DestinationRef` naming the last advertised stop of the monitored journey.
- **`destination_name`** (string or null, required): Human-readable stop name from `MonitoredVehicleJourney/DestinationName` for the final advertised destination of the monitored journey.
- **`longitude`** (double or null, required): WGS84 longitude from `MonitoredVehicleJourney/VehicleLocation/Longitude` expressed in decimal degrees. Positive values are east of Greenwich. Null when the AVL feed does not provide a usable vehicle location. Constraints: minimum `-180`, maximum `180`.
- **`latitude`** (double or null, required): WGS84 latitude from `MonitoredVehicleJourney/VehicleLocation/Latitude` expressed in decimal degrees. Positive values are north of the equator. Null when the AVL feed does not provide a usable vehicle location. Constraints: minimum `-90`, maximum `90`.
- **`bearing`** (integer or null, required): Vehicle heading from `MonitoredVehicleJourney/Bearing` in whole degrees clockwise from true north. Null when the AVL producer omits heading information. Constraints: minimum `0`, maximum `360`.
- **`recorded_at_time`** (datetime, required): Timestamp from `VehicleActivity/RecordedAtTime` stating when the AVL system recorded this vehicle activity snapshot. Encoded as an ISO 8601 / RFC 3339 date-time string with an explicit UTC offset.
- **`valid_until_time`** (datetime or null, required): Expiry timestamp from `VehicleActivity/ValidUntilTime` after which consumers should treat the vehicle activity as stale if it has not been refreshed by a newer message.
- **`block_ref`** (string or null, required): Block or duty identifier from `MonitoredVehicleJourney/BlockRef` describing the operational vehicle block used by the operator scheduling system.
- **`vehicle_journey_ref`** (string or null, required): Vehicle journey identifier from `MonitoredVehicleJourney/VehicleJourneyRef` used within the operator AVL system to refer to the monitored trip instance.
- **`origin_aimed_departure_time`** (datetime or null, required): Scheduled departure time from `MonitoredVehicleJourney/OriginAimedDepartureTime` for the origin stop of the monitored journey, encoded as an ISO 8601 / RFC 3339 date-time string.
- **`data_frame_ref`** (string or null, required): Service day identifier from `MonitoredVehicleJourney/FramedVehicleJourneyRef/DataFrameRef`. Providers typically use this value to pair the live journey with the scheduled service-day context.
- **`dated_vehicle_journey_ref`** (string or null, required): Dated journey identifier from `MonitoredVehicleJourney/FramedVehicleJourneyRef/DatedVehicleJourneyRef`. This value disambiguates the scheduled journey instance within the service day defined by `data_frame_ref`.
- **`item_identifier`** (string, required): Unique `VehicleActivity/ItemIdentifier` value assigned by the upstream SIRI payload. The bridge uses this field for deduplication so repeated snapshots of the same unchanged vehicle activity are not re-emitted.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "operator_ref": "string",
  "vehicle_ref": "string",
  "line_ref": "string",
  "direction_ref": "string",
  "published_line_name": "string",
  "origin_ref": "string",
  "origin_name": "string",
  "destination_ref": "string",
  "destination_name": "string",
  "longitude": 0,
  "latitude": 0,
  "bearing": 0,
  "recorded_at_time": "2024-01-01T00:00:00Z",
  "valid_until_time": "2024-01-01T00:00:00Z",
  "block_ref": "string",
  "vehicle_journey_ref": "string",
  "origin_aimed_departure_time": "2024-01-01T00:00:00Z",
  "data_frame_ref": "string",
  "dated_vehicle_journey_ref": "string",
  "item_identifier": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Operator

CloudEvents type: `org.siri.Operator`

#### What it tells you

Reference record for one operator code observed in the configured SIRI feed. The bridge extracts distinct operators from the same upstream payloads that supply telemetry so consumers can build operator context without a separate metadata call. Reference payload for a distinct operator code observed in a configured SIRI feed.

#### Identity

Each event identifies the real-world resource with `{operator_ref}`. `{operator_ref}` is operator identifier from `MonitoredVehicleJourney/OperatorRef`. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `siri`, key `{operator_ref}` |
| `MQTT/5.0` | topic `transit/siri/{operator_ref}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/siri`, message subject `{operator_ref}` |

#### Payload

`Operator` payloads are JSON object. Required fields: `operator_ref`.

- **`operator_ref`** (string, required): Operator identifier from `MonitoredVehicleJourney/OperatorRef`. This is the stable identity of the operator reference event and the prefix of every vehicle subject emitted by the source.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "operator_ref": "string"
}
```

#### Reference vs telemetry

This is reference/catalog data. It is emitted when the feeder observes the operator set for the current payload so consumers can maintain operator context without polling an out-of-band metadata source.

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

- The checked-in guide documents a default polling interval of 30 seconds.
- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.

## References

- xRegistry manifest: [`../siri/xreg/siri.xreg.json`](../siri/xreg/siri.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
