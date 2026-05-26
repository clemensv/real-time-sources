# Wikimedia EventStreams RecentChange feeder Events

MQTT/5.0 non-retained Wikimedia EventStreams recentchange firehose. Single family (recent-change) baked as the trailing topic segment so subscribers can wildcard per wiki/namespace/event. QoS 0, retain=false.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{event_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `wikimedia-eventstreams`. The record key is `{event_id}`. In plain language, `{event_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['wikimedia-eventstreams'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to the topic filters documented per event below. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('#', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `wikimedia-eventstreams`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/wikimedia-eventstreams')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Recent Change

CloudEvents type: `Wikimedia.EventStreams.RecentChange`

#### What it tells you

Public recentchange events from Wikimedia EventStreams. Each event describes one edit, page creation, log action, categorization change, or related MediaWiki recentchanges entry from across Wikimedia projects. Normalized representation of Wikimedia's mediawiki/recentchange event schema.

#### Identity

Each event identifies the real-world resource with `{event_id}`. `{event_id}` is top-level copy of meta.id so downstream validators and consumers can resolve the CloudEvents subject and Kafka key from the event payload itself. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `wikimedia-eventstreams`, key `{event_id}` |
| `MQTT/5.0` | topic `not declared`, retain `not declared`, QoS `not declared` |
| `AMQP/1.0` | source address `amqps://localhost:5671/wikimedia-eventstreams`, message subject `{event_id}` |

#### Payload

`Recent Change` payloads are JSON object. Required fields: `event_id`, `event_time`, `schema_uri`, `meta`, `type`, `namespace_id`, `title`, `timestamp`, `user`, `wiki`, `namespace`.

- **`event_id`** (string, required): Top-level copy of meta.id so downstream validators and consumers can resolve the CloudEvents subject and Kafka key from the event payload itself.
- **`event_time`** (string, required): Top-level copy of meta.dt in ISO-8601 UTC format so downstream validators and consumers can resolve the CloudEvents time attribute from the payload itself.
- **`schema_uri`** (string, required): URI of the upstream Wikimedia JSON schema from the $schema field on the original event payload.
- **`meta`** (object, required): Wikimedia EventStreams envelope metadata describing the event identity, domain, stream, and Kafka-origin details. See [meta](#payload-wikimedia-eventstreams-recentchange-meta).
- **`id`** (null or string, optional): MediaWiki recentchanges row identifier (rcid) for the event, stringified because some Wikimedia wikis already exceed signed 32-bit integer range.
- **`type`** (string, required): Recentchange type such as edit, new, log, categorize, or external.
- **`namespace_id`** (integer, required): Numeric MediaWiki namespace identifier for the affected page (0 = main, 1 = talk, 6 = file, 14 = category, -1 for special log events). Renamed from ``namespace`` to free that name for the kebab-case bucket that is also used as the {namespace} MQTT topic axis.
- **`title`** (string, required): Affected page title in MediaWiki prefixed text form.
- **`title_url`** (null or string, optional): Canonical page URL for the affected title when present in the upstream payload.
- **`comment`** (null or string, optional): Edit or log comment as supplied by the upstream recentchange record.
- **`timestamp`** (integer, required): Unix timestamp derived from the MediaWiki rc_timestamp value.
- **`user`** (string, required): User name or IP address associated with the change.
- **`bot`** (null or boolean, optional): Whether the recentchange entry was flagged as a bot edit.
- **`minor`** (null or boolean, optional): Whether the recentchange entry was flagged as a minor change.
- **`patrolled`** (null or boolean, optional): Whether the recentchange entry had been patrolled when the event was emitted.
- **`length`** (object, optional): Page lengths before and after the change, measured in bytes or characters as provided by MediaWiki. See [length](#payload-wikimedia-eventstreams-recentchange-length).
- **`revision`** (object, optional): Old and new MediaWiki revision identifiers associated with the change. See [revision](#payload-wikimedia-eventstreams-recentchange-revision).
- **`server_url`** (null or string, optional): Canonical server URL for the wiki that emitted the event.
- **`server_name`** (null or string, optional): Server host name of the wiki that emitted the event.
- **`server_script_path`** (null or string, optional): MediaWiki script path on the emitting wiki.
- **`wiki`** (string, required): Internal Wikimedia wiki identifier such as enwiki, commonswiki, or wikidatawiki.
- **`namespace`** (string, required): Kebab-case bucket label for the MediaWiki namespace (e.g. ``main`` for 0, ``talk`` for 1, ``file`` for 6, ``category`` for 14, ``ns-<n>`` for unrecognised values). Used as the {namespace} MQTT topic segment; subscribers can wildcard per wiki/namespace without parsing the integer id.
- **`parsedcomment`** (null or string, optional): HTML-parsed form of the recentchange comment when Wikimedia provides it.
- **`notify_url`** (null or string, optional): URL that points to a diff view or other relevant page for the change.
- **`log_type`** (null or string, optional): MediaWiki log type for log events, such as move, delete, or patrol.
- **`log_action`** (null or string, optional): Specific MediaWiki log action name for log events.
- **`log_action_comment`** (null or string, optional): Additional comment field emitted for some MediaWiki log actions.
- **`log_id`** (null or string, optional): MediaWiki log identifier associated with the event when the change is a log entry, stringified for stable cross-language handling.
- **`log_params_json`** (null or string, optional): Serialized form of the upstream log_params field, which may be an object, array, or string in the raw Wikimedia payload.
##### meta
<a id="payload-wikimedia-eventstreams-recentchange-meta"></a>

Wikimedia EventStreams envelope metadata describing the event identity, domain, stream, and Kafka-origin details.

- **`uri`** (string, optional): URI of the Wikimedia entity or page the event pertains to, when provided by the upstream stream.
- **`request_id`** (string, optional): Unique request identifier assigned by Wikimedia for the request that caused the event.
- **`id`** (string, required): Globally unique Wikimedia event UUID for this recentchange record.
- **`domain`** (string, required): Wikimedia domain the event pertains to, such as www.wikipedia.org or www.wikidata.org.
- **`stream`** (string, required): Name of the upstream EventStreams stream that emitted the event, typically mediawiki.recentchange.
- **`topic`** (string, optional): Underlying Wikimedia Kafka topic that carried the event before it was exposed through EventStreams.
- **`partition`** (integer, optional): Underlying Kafka partition number from Wikimedia's internal stream metadata.
- **`offset`** (null or string, optional): Underlying Kafka offset from Wikimedia's internal stream metadata, stringified to avoid range loss across generated languages and validators.
- **`dt`** (string, required): UTC event timestamp in ISO-8601 format from the upstream metadata block.
##### length
<a id="payload-wikimedia-eventstreams-recentchange-length"></a>

Page lengths before and after the change, measured in bytes or characters as provided by MediaWiki.

- **`old`** (null or integer, optional): Length of the page before the change.
- **`new`** (null or integer, optional): Length of the page after the change.
##### revision
<a id="payload-wikimedia-eventstreams-recentchange-revision"></a>

Old and new MediaWiki revision identifiers associated with the change.

- **`old`** (null or string, optional): Previous revision identifier before the change, stringified because recent Wikimedia revision identifiers can exceed signed 32-bit integer range.
- **`new`** (null or string, optional): New revision identifier after the change, stringified because recent Wikimedia revision identifiers can exceed signed 32-bit integer range.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": "string",
  "event_time": "string",
  "schema_uri": "string",
  "meta": {
    "uri": "string",
    "request_id": "string",
    "id": "string",
    "domain": "string",
    "stream": "string",
    "topic": "string",
    "partition": 0,
    "offset": "string",
    "dt": "string"
  },
  "id": "string",
  "type": "string",
  "namespace_id": 0,
  "title": "string",
  "title_url": "string",
  "comment": "string",
  "timestamp": 0,
  "user": "string",
  "bot": false,
  "minor": false,
  "patrolled": false,
  "length": {
    "old": 0,
    "new": 0
  },
  "revision": {
    "old": "string",
    "new": "string"
  },
  "server_url": "string",
  "server_name": "string",
  "server_script_path": "string",
  "wiki": "string",
  "namespace": "string",
  "parsedcomment": "string",
  "notify_url": "string",
  "log_type": "string",
  "log_action": "string",
  "log_action_comment": "string",
  "log_id": "string",
  "log_params_json": "string"
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

## References

- xRegistry manifest: [`xreg/wikimedia_eventstreams.xreg.json`](xreg/wikimedia_eventstreams.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
