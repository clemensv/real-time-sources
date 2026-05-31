# PTWC Tsunami feeder Events

PTWC Tsunami publishes tsunami bulletins from the Pacific Tsunami Warning Center for ocean basins and tsunami bulletin areas. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{bulletin_id}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `ptwc-tsunami`. The record key is `{bulletin_id}`. In plain language, `{bulletin_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['ptwc-tsunami'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `alerts/intl/ptwc/ptwc-tsunami/+/+/+/bulletin`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('alerts/intl/ptwc/ptwc-tsunami/+/+/+/bulletin', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `ptwc-tsunami`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/ptwc-tsunami')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Tsunami Bulletin

CloudEvents type: `PTWC.TsunamiBulletin`

#### What it tells you

A tsunami bulletin from the US National Tsunami Warning Center (NTWC) or the Pacific Tsunami Warning Center (PTWC). Bulletins indicate seismic events and their tsunami threat assessment, parsed from the NOAA Atom feeds at tsunami.gov.

#### Identity

Each event identifies the real-world resource with `{bulletin_id}`. `{bulletin_id}` is the unique bulletin identifier as a URN UUID from the Atom entry (e.g., 'urn:uuid:7a6b0584-8201-4ef6-aac6-e512d77cbfb9'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ptwc-tsunami`, key `{bulletin_id}` |
| `MQTT/5.0` | topic `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqp://localhost:5672/ptwc-tsunami`, message subject `{bulletin_id}`; application properties basin `{basin}`, ptwc_level `{ptwc_level}` |

#### Payload

`Tsunami Bulletin` payloads are JSON object. Required fields: `bulletin_id`, `feed`, `title`, `updated`, `basin`, `ptwc_level`.

- **`bulletin_id`** (string, required): The unique bulletin identifier as a URN UUID from the Atom entry (e.g., 'urn:uuid:7a6b0584-8201-4ef6-aac6-e512d77cbfb9').
- **`feed`** (enum, required): The feed this bulletin was obtained from.
- **`center`** (string, optional): The issuing tsunami warning center name (e.g., 'NWS National Tsunami Warning Center Palmer AK', 'NWS PACIFIC TSUNAMI WARNING CENTER HONOLULU HI').
- **`title`** (string, required): The title of the bulletin, typically the location of the seismic event (e.g., '60 miles SW of Buldir I., Alaska').
- **`updated`** (datetime, required): The date and time when the bulletin was last updated, in ISO-8601 format.
- **`latitude`** (double, optional): The latitude of the seismic event epicenter in decimal degrees.
- **`longitude`** (double, optional): The longitude of the seismic event epicenter in decimal degrees.
- **`category`** (enum, optional): Native tsunami bulletin category from the feed summary (Warning, Advisory, Watch, or Information). ptwc_level carries the lowercase topic-routing form.
- **`magnitude`** (string, optional): The preliminary earthquake magnitude and type (e.g., '5.2(mb)', '7.1(Mw)').
- **`affected_region`** (string, optional): The affected region description from the bulletin summary.
- **`note`** (string, optional): Additional notes from the bulletin (e.g., 'There is NO tsunami danger from this earthquake.').
- **`bulletin_url`** (string, optional): URL to the full text bulletin on tsunami.gov.
- **`cap_url`** (string, optional): URL to the CAP XML document for this bulletin.
- **`basin`** (enum, required): Basin or warning-area slug derived from the NOAA tsunami.gov feed (pacific for PHEB, alaska for PAAQ, or unknown). Matches the {basin} MQTT topic axis.
- **`ptwc_level`** (enum, required): Native tsunami bulletin category normalized to lowercase for MQTT routing. Matches the {ptwc_level} MQTT topic axis.
##### `feed` values

- `PAAQ`: Provider value `PAAQ` for this coded alert field.
- `PHEB`: Provider value `PHEB` for this coded alert field.
##### `category` values

- `Warning`: Provider value `Warning` for this coded alert field.
- `Advisory`: Provider value `Advisory` for this coded alert field.
- `Watch`: Provider value `Watch` for this coded alert field.
- `Information`: Provider value `Information` for this coded alert field.
##### `basin` values

- `pacific`: Provider value `pacific` for this coded alert field.
- `alaska`: Provider value `alaska` for this coded alert field.
- `unknown`: Provider value `unknown` for this coded alert field.
##### `ptwc_level` values

- `warning`: Provider value `warning` for this coded alert field.
- `advisory`: Provider value `advisory` for this coded alert field.
- `watch`: Provider value `watch` for this coded alert field.
- `information`: Provider value `information` for this coded alert field.
- `unknown`: Provider value `unknown` for this coded alert field.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "bulletin_id": "string",
  "feed": "PAAQ",
  "center": "string",
  "title": "string",
  "updated": "2024-01-01T00:00:00Z",
  "latitude": 0,
  "longitude": 0,
  "category": "Warning",
  "magnitude": "string",
  "affected_region": "string",
  "note": "string",
  "bulletin_url": "string",
  "cap_url": "string",
  "basin": "pacific",
  "ptwc_level": "warning"
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

- xRegistry manifest: [`xreg/ptwc-tsunami.xreg.json`](xreg/ptwc-tsunami.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
