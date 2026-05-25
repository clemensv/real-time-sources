# USGS Earthquake Hazards Program - Real-time Earthquake Feed Events

MQTT/5.0 transport variant for USGS earthquake events. Non-retained QoS-1 event stream routed by contributor network, magnitude bucket, and event code under seismic/intl/usgs/usgs-earthquakes/... Buckets are m0 for <1 or unknown, m1..m6 for [1,7), and m7plus for >=7.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{net}/{code}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `usgs-earthquakes`. The record key is `{net}/{code}`. In plain language, `{net}/{code}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['usgs-earthquakes'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `seismic/intl/usgs/usgs-earthquakes/+/+/+/quake`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('seismic/intl/usgs/usgs-earthquakes/+/+/+/quake', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `usgs-earthquakes`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/usgs-earthquakes')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Event

CloudEvents type: `USGS.Earthquakes.Event`

#### What it tells you

USGS earthquake event data from the Earthquake Hazards Program.

#### Identity

Each event identifies the real-world resource with `{net}/{code}`. `{net}` is ID of the data contributor network; `{code}` is identifying code assigned by the corresponding source for the event. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `usgs-earthquakes`, key `{net}/{code}` |
| `MQTT/5.0` | topic `seismic/intl/usgs/usgs-earthquakes/{net}/{magnitude_bucket}/{code}/quake`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/usgs-earthquakes`, message subject `{net}/{code}` |

#### Payload

`Event` payloads are JSON object. Required fields: `id`, `event_time`, `updated`, `status`, `tsunami`, `net`, `code`, `latitude`, `longitude`, `magnitude_bucket`.

- **`id`** (string, required): Unique identifier for the earthquake event.
- **`magnitude`** (double or null, optional): Magnitude of the earthquake.
- **`mag_type`** (string or null, optional): Method or algorithm used to calculate the magnitude (e.g. ml, md, mb, mww).
- **`place`** (string or null, optional): Textual description of the named geographic region near the event.
- **`event_time`** (string, required): Time of the earthquake event in ISO-8601 format.
- **`updated`** (string, required): Time when the event was most recently updated in ISO-8601 format.
- **`url`** (string or null, optional): Link to USGS Event Page for this event.
- **`detail_url`** (string or null, optional): Link to GeoJSON detail feed for this event.
- **`felt`** (int32 or null, optional): Number of felt reports submitted to the DYFI system.
- **`cdi`** (double or null, optional): Maximum reported community determined intensity (DYFI).
- **`mmi`** (double or null, optional): Maximum estimated instrumental intensity (ShakeMap).
- **`alert`** (string or null, optional): PAGER alert level (green, yellow, orange, red).
- **`status`** (string, required): Review status of the event (automatic, reviewed, deleted).
- **`tsunami`** (int32, required): Flag indicating whether the event has a tsunami advisory (1=yes, 0=no).
- **`sig`** (int32 or null, optional): Significance of the event, a number describing how significant the event is (0-1000).
- **`net`** (string, required): ID of the data contributor network.
- **`code`** (string, required): Identifying code assigned by the corresponding source for the event.
- **`sources`** (string or null, optional): Comma-separated list of network contributors.
- **`nst`** (int32 or null, optional): Number of seismic stations used to determine earthquake location.
- **`dmin`** (double or null, optional): Horizontal distance from the epicenter to the nearest station (degrees).
- **`rms`** (double or null, optional): Root-mean-square travel time residual (seconds).
- **`gap`** (double or null, optional): Largest azimuthal gap between azimuthally adjacent stations (degrees).
- **`event_type`** (string or null, optional): Type of seismic event (earthquake, quarry blast, etc.).
- **`latitude`** (double, required): Latitude of the earthquake epicenter in decimal degrees.
- **`longitude`** (double, required): Longitude of the earthquake epicenter in decimal degrees.
- **`depth`** (double or null, optional): Depth of the earthquake in kilometers.
- **`magnitude_bucket`** (string, required): Topic-safe magnitude bucket: m0 for magnitude <1 or unknown, m1..m6 for [1,7), and m7plus for magnitude >=7.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "id": "string",
  "magnitude": 0,
  "mag_type": "string",
  "place": "string",
  "event_time": "string",
  "updated": "string",
  "url": "string",
  "detail_url": "string",
  "felt": 0,
  "cdi": 0,
  "mmi": 0,
  "alert": "string",
  "status": "string",
  "tsunami": 0,
  "sig": 0,
  "net": "string",
  "code": "string",
  "sources": "string",
  "nst": 0,
  "dmin": 0,
  "rms": 0,
  "gap": 0,
  "event_type": "string",
  "latitude": 0,
  "longitude": 0,
  "depth": 0,
  "magnitude_bucket": "string"
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

- xRegistry manifest: [`xreg/usgs_earthquakes.xreg.json`](xreg/usgs_earthquakes.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- ![Deploy AMQP to Azure Service Bus: <https://aka.ms/deploytoazurebutton>
