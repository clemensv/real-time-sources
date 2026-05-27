# GraceDB feeder Events

GraceDB publishes superevent alerts and classifications from the LIGO/Virgo/KAGRA GraceDB service for gravitational-wave candidate events. These events help consumers monitor hazards, route notifications, and correlate public-warning updates without polling the upstream source directly.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{superevent_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `gracedb`. The record key is `{superevent_id}`. In plain language, `{superevent_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['gracedb'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `seismic/intl/ligo/gracedb/+/+/+/superevent`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('seismic/intl/ligo/gracedb/+/+/+/superevent', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `gracedb`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/gracedb')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Superevent

CloudEvents type: `org.ligo.gracedb.Superevent`

#### What it tells you

A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. A superevent aggregates one or more pipeline detections into a single candidate and carries significance, classification, and alert-lifecycle metadata.

#### Identity

Each event identifies the real-world resource with `{superevent_id}`. `{superevent_id}` is unique identifier for the superevent assigned by GraceDB, e.g. 'S240414a' for production events or 'MS260408x' for MDC (mock data challenge) events. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `gracedb`, key `{superevent_id}` |
| `MQTT/5.0` | topic `seismic/intl/ligo/gracedb/{category}/{group}/{superevent_id}/superevent`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/gracedb`, message subject `{superevent_id}` |

#### Payload

`Superevent` payloads are JSON object. Required fields: `superevent_id`, `category`, `created`, `t_start`, `t_0`, `t_end`, `far`, `labels_json`, `group`, `submitter`, `self_uri`.

- **`superevent_id`** (string, required): Unique identifier for the superevent assigned by GraceDB, e.g. 'S240414a' for production events or 'MS260408x' for MDC (mock data challenge) events.
- **`category`** (string, required): Category of the superevent. 'Production' for real observing-run candidates, 'MDC' for mock data challenge injections, 'Test' for engineering/test events.
- **`created`** (string, required): ISO-8601 UTC timestamp when the superevent was first created in GraceDB, e.g. '2026-04-08 23:59:34 UTC'.
- **`t_start`** (double, required): GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the start of the superevent time window.
- **`t_0`** (double, required): GPS time (seconds since 1980-01-06T00:00:00 UTC) of the central trigger time for this superevent.
- **`t_end`** (double, required): GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the end of the superevent time window.
- **`far`** (double, required): False alarm rate in Hz. Lower values indicate a more significant event. For example, 1e-14 Hz corresponds to roughly one false alarm per 3 million years.
- **`time_coinc_far`** (double or null, optional): Time-coincidence false alarm rate in Hz from the RAVEN pipeline, representing the probability of a temporal coincidence with an external trigger. Null if no external coincidence was evaluated.
- **`space_coinc_far`** (double or null, optional): Space-and-time-coincidence false alarm rate in Hz from the RAVEN pipeline, incorporating both temporal and spatial overlap with an external trigger. Null if no external coincidence was evaluated.
- **`labels_json`** (string, required): JSON-encoded array of label strings attached to this superevent, e.g. '["EM_READY","GCN_PRELIM_SENT","SKYMAP_READY"]'. Labels track alert lifecycle: EM_READY (electromagnetic follow-up viable), GCN_PRELIM_SENT (GCN preliminary notice sent), SKYMAP_READY (sky localization map available), EMBRIGHT_READY (source classification available), PASTRO_READY (probability of astrophysical origin available), ADVOK/ADVNO (advocate approval/rejection), SIGNIF_LOCKED (significance frozen), DQR_REQUEST (data quality review requested), HIGH_PROFILE (high-profile candidate), RAVEN_ALERT (external trigger coincidence found).
- **`preferred_event_id`** (string or null, optional): GraceDB event ID of the preferred pipeline event (the best detection) associated with this superevent, e.g. 'M632680'. Null if no preferred event has been selected.
- **`pipeline`** (string or null, optional): Name of the detection pipeline that produced the preferred event, e.g. 'gstlal', 'MBTAOnline', 'SPIIR', 'PyCBC'. Null if no preferred event has been set.
- **`group`** (string, required): Physics group of the preferred event: 'CBC' (compact binary coalescence), 'Burst' (unmodeled transient), 'Test', or 'unknown' when GraceDB has not supplied preferred-event group data.
- **`instruments`** (string or null, optional): Comma-separated list of detector instruments that contributed to the preferred event, e.g. 'H1,L1,V1' for LIGO Hanford, LIGO Livingston, and Virgo. Null if no preferred event has been set.
- **`gw_id`** (string or null, optional): Official gravitational wave event name assigned after confirmation, e.g. 'GW200115'. Null if the event has not been confirmed or named.
- **`submitter`** (string, required): Username or service account that submitted the superevent to GraceDB, e.g. 'read-cvmfs-emfollow'.
- **`em_type`** (string or null, optional): Identifier of the associated electromagnetic event from an external trigger (e.g. a Fermi GBM or Swift trigger ID). Null if no external EM association exists.
- **`search`** (string or null, optional): Search type of the preferred event: 'AllSky' (standard all-sky search), 'MDC' (mock data challenge), 'BBH' (binary black hole targeted), 'EarlyWarning' (pre-merger alert). Null if no preferred event has been set.
- **`far_is_upper_limit`** (boolean or null, optional): Whether the reported FAR value is an upper limit rather than an exact estimate. True indicates the actual false alarm rate may be lower. Null if no preferred event has been set.
- **`nevents`** (int32 or null, optional): Number of pipeline events aggregated into this superevent. Null if the preferred event data is not available.
- **`self_uri`** (string, required): HATEOAS self link for the superevent resource in the GraceDB REST API, e.g. 'https://gracedb.ligo.org/api/superevents/MS260408x/'.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "superevent_id": "string",
  "category": "string",
  "created": "string",
  "t_start": 0,
  "t_0": 0,
  "t_end": 0,
  "far": 0,
  "time_coinc_far": 0,
  "space_coinc_far": 0,
  "labels_json": "string",
  "preferred_event_id": "string",
  "pipeline": "string",
  "group": "string",
  "instruments": "string",
  "gw_id": "string",
  "submitter": "string",
  "em_type": "string",
  "search": "string",
  "far_is_upper_limit": false,
  "nevents": 0,
  "self_uri": "string"
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

- xRegistry manifest: [`xreg/gracedb.xreg.json`](xreg/gracedb.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- GraceDB superevents API: <https://gracedb.ligo.org/api/superevents/?format=json>
