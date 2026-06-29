# FDSN Seismology Events

Federated FDSN event-service bridge over eight pre-configured earthquake nodes (EMSC, GFZ, INGV, ETHZ/SED, RESIF, IPGP, NIEP, USGS). Upstream surface reviewed from the FDSN Event WADL plus live node probes: query (kept, telemetry), catalogs (dropped as duplicate index metadata), contributors (dropped as duplicate contributor listings), version (dropped as operational metadata), and application.wadl (dropped as static service description). The feeder emits node reference records and earthquake telemetry on a single topic family.

## At a glance

- **Event types:** 2 documented event types (8 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{contributor}/{event_id}`, `{node_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `fdsn-seismology`. The record key is `{contributor}/{event_id}`. In plain language, `{contributor}/{event_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['fdsn-seismology'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `seismology/fdsn/+/+`, `seismology/fdsn/+/info`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('seismology/fdsn/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `fdsn-seismology`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/fdsn-seismology')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Earthquake

CloudEvents type: `org.fdsn.event.Earthquake`

#### What it tells you

Telemetry event representing one earthquake detection record returned by an FDSN Event web-service node in the standard pipe-delimited text format. Preferred-origin earthquake event record returned by an FDSN Event web-service node in text format. The record carries origin time, hypocenter, magnitude, provenance, and human-readable region metadata for one seismic event.

#### Identity

Each event identifies the real-world resource with `{contributor}/{event_id}`. `{contributor}` is short code of the institution that contributed this event record to the FDSN node, e.g. 'CSN', 'GFZ', 'EMSC'; `{event_id}` is unique identifier assigned by the contributing institution, e.g. '20260604_0000095' or 'gfz2026kvsq'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `fdsn-seismology`, key `{contributor}/{event_id}` |
| `MQTT/5.0` | topic `seismology/fdsn/{contributor}/{event_id}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/fdsn-seismology`, message subject `{contributor}/{event_id}` |

#### Payload

`Earthquake` payloads are JSON object. Required fields: `event_id`, `time`, `latitude`, `longitude`, `contributor`, `node_url`.

- **`event_id`** (string, required): Unique identifier assigned by the contributing institution, e.g. '20260604_0000095' or 'gfz2026kvsq'. Constraints: minLength `1`.
- **`time`** (datetime, required): Origin time of the seismic event in ISO 8601 UTC format as reported by the authoritative source.
- **`latitude`** (double, required, degree (°)): Epicenter latitude in decimal degrees, WGS84 datum, range -90 to 90. Constraints: minimum `-90`, maximum `90`.
- **`longitude`** (double, required, degree (°)): Epicenter longitude in decimal degrees, WGS84 datum, range -180 to 180. Constraints: minimum `-180`, maximum `180`.
- **`depth_km`** (double or null, optional, kilometer (km)): Hypocentral depth in kilometers below the Earth's surface; null if unconstrained.
- **`author`** (string or null, optional): Agency or analyst who computed the preferred origin solution, e.g. 'EMSC', 'GFZ', 'SURVEY-INGV'.
- **`catalog`** (string or null, optional): Name of the event catalog this earthquake belongs to, e.g. 'EMSC-RTS', 'SED'.
- **`contributor`** (string, required): Short code of the institution that contributed this event record to the FDSN node, e.g. 'CSN', 'GFZ', 'EMSC'. Constraints: minLength `1`.
- **`contributor_id`** (string or null, optional): Contributor's internal identifier for this event, may differ from event_id.
- **`magnitude_type`** (string or null, optional): Scale used for the preferred magnitude: 'ML' (local), 'mb' (body-wave), 'Mw' (moment), 'Ms' (surface), 'm' (unspecified).
- **`magnitude`** (double or null, optional): Preferred magnitude value on the scale indicated by magnitude_type; null if no magnitude computed.
- **`magnitude_author`** (string or null, optional): Agency that computed the preferred magnitude, may differ from the origin author.
- **`event_location_name`** (string or null, optional): Human-readable geographic description of the epicenter region, typically a Flinn-Engdahl region name.
- **`event_type`** (string or null, optional): Seismological event classification: 'earthquake', 'quarry blast', 'explosion', 'induced or triggered event', etc.
- **`node_url`** (uri, required): Base URL of the FDSN node that served this event record, identifying the data source.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": "string",
  "time": "2024-01-01T00:00:00Z",
  "latitude": 0,
  "longitude": 0,
  "depth_km": 0,
  "author": "string",
  "catalog": "string",
  "contributor": "string",
  "contributor_id": "string",
  "magnitude_type": "string",
  "magnitude": 0,
  "magnitude_author": "string",
  "event_location_name": "string",
  "event_type": "string",
  "node_url": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Node

CloudEvents type: `org.fdsn.event.Node`

#### What it tells you

Reference-data event for one pre-configured FDSN event-service node that this feeder can poll. Reference-data record describing one pre-configured FDSN Event web-service node that the feeder polls for earthquake detections.

#### Identity

Each event identifies the real-world resource with `{node_id}`. `{node_id}` is short identifier for the FDSN node, e.g. 'emsc', 'gfz', 'ingv', 'ethz', 'resif'. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `fdsn-seismology`, key `{contributor}/{event_id}` |
| `MQTT/5.0` | topic `seismology/fdsn/{node_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/fdsn-seismology`, message subject `{node_id}` |

#### Payload

`Node` payloads are JSON object. Required fields: `node_id`, `name`, `base_url`, `coverage`.

- **`node_id`** (string, required): Short identifier for the FDSN node, e.g. 'emsc', 'gfz', 'ingv', 'ethz', 'resif'. Constraints: minLength `1`.
- **`name`** (string, required): Full institution name operating the FDSN event service. Constraints: minLength `1`.
- **`base_url`** (uri, required): Base URL for the FDSN event web service endpoint, e.g. 'https://seismicportal.eu/fdsnws/event/1/'.
- **`coverage`** (string, required): Geographic or magnitude coverage description, e.g. 'Global aggregator', 'Italy + Mediterranean'. Constraints: minLength `1`.
- **`country`** (string or null, optional): ISO 3166-1 alpha-2 country code of the operating institution. Constraints: pattern `^[A-Z]{2}$`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "node_id": "string",
  "name": "string",
  "base_url": "string",
  "coverage": "string",
  "country": "string"
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
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/fdsn-seismology.xreg.json`](xreg/fdsn-seismology.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
