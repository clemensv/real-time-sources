# Bluesky Firehose Producer Events

MQTT/5.0 non-retained firehose variants of the Bluesky CloudEvents. Each record family gets a dedicated topic with the kebab record name baked as the trailing segment so subscribers can wildcard per family. QoS 0, retain=false — there is no LKV slot for a firehose.

## At a glance

- **Event types:** 6 documented event types (12 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0
- **Reference vs telemetry:** 0 reference/catalog event types and 6 telemetry event types.
- **Identity:** `{did}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `bluesky`. The record key is `{did}`. In plain language, `{did}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['bluesky'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `social/intl/bluesky/bluesky/+/+/+/post`, `social/intl/bluesky/bluesky/+/+/+/like`, `social/intl/bluesky/bluesky/+/+/+/repost`, `social/intl/bluesky/bluesky/+/+/+/follow`, `social/intl/bluesky/bluesky/+/+/+/block`, `social/intl/bluesky/bluesky/+/+/+/profile`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('social/intl/bluesky/bluesky/+/+/+/post', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.

## Event catalog

### Post

CloudEvents type: `Bluesky.Feed.Post`

#### What it tells you

A post in the Bluesky feed A post in the Bluesky feed

#### Identity

Each event identifies the real-world resource with `{did}`. `{did}` is decentralized Identifier of the author. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bluesky`, key `{did}` |
| `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/post`, retain `false`, QoS `0` |

#### Payload

`Post` payloads are JSON object. Required fields: `uri`, `cid`, `did`, `text`, `langs`, `tags`, `created_at`, `indexed_at`, `seq`, `collection`, `lang`.

- **`uri`** (string, required): AT-URI of the post (at://did:plc:xxx/app.bsky.feed.post/xxx)
- **`cid`** (string, required): Content Identifier (CID) of the post
- **`did`** (string, required): Decentralized Identifier of the author
- **`handle`** (string, optional): Handle of the author
- **`text`** (string, required): Text content of the post
- **`langs`** (array of string, required): Language codes for the post
- **`reply_parent`** (string, optional): AT-URI of parent post if this is a reply
- **`reply_root`** (string, optional): AT-URI of root post in thread
- **`embed_type`** (string, optional): Type of embedded content (images, external, record, etc.)
- **`embed_uri`** (string, optional): URI of embedded content
- **`facets`** (string, optional): JSON string of rich text facets (mentions, links, tags)
- **`tags`** (array of string, required): Hashtags in the post
- **`created_at`** (string, required): ISO 8601 timestamp of post creation
- **`indexed_at`** (string, required): ISO 8601 timestamp of when the post was indexed
- **`seq`** (int64, required): Firehose sequence number
- **`collection`** (string, required): AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty.
- **`lang`** (string, required): Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "uri": "string",
  "cid": "string",
  "did": "string",
  "handle": "string",
  "text": "string",
  "langs": [],
  "reply_parent": "string",
  "reply_root": "string",
  "embed_type": "string",
  "embed_uri": "string",
  "facets": "string",
  "tags": [],
  "created_at": "string",
  "indexed_at": "string",
  "seq": 0,
  "collection": "string",
  "lang": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Like

CloudEvents type: `Bluesky.Feed.Like`

#### What it tells you

A like on a post A like on a post

#### Identity

Each event identifies the real-world resource with `{did}`. `{did}` is DID of the user who liked. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bluesky`, key `{did}` |
| `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/like`, retain `false`, QoS `0` |

#### Payload

`Like` payloads are JSON object. Required fields: `uri`, `cid`, `did`, `subject_uri`, `subject_cid`, `created_at`, `indexed_at`, `seq`, `collection`, `lang`.

- **`uri`** (string, required): AT-URI of the like record
- **`cid`** (string, required): Content Identifier of the like
- **`did`** (string, required): DID of the user who liked
- **`handle`** (string, optional): Handle of the user who liked
- **`subject_uri`** (string, required): AT-URI of the liked post
- **`subject_cid`** (string, required): CID of the liked post
- **`created_at`** (string, required): ISO 8601 timestamp of like creation
- **`indexed_at`** (string, required): ISO 8601 timestamp of indexing
- **`seq`** (int64, required): Firehose sequence number
- **`collection`** (string, required): AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty.
- **`lang`** (string, required): Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "uri": "string",
  "cid": "string",
  "did": "string",
  "handle": "string",
  "subject_uri": "string",
  "subject_cid": "string",
  "created_at": "string",
  "indexed_at": "string",
  "seq": 0,
  "collection": "string",
  "lang": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Repost

CloudEvents type: `Bluesky.Feed.Repost`

#### What it tells you

A repost of a post A repost of a post

#### Identity

Each event identifies the real-world resource with `{did}`. `{did}` is DID of the user who reposted. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bluesky`, key `{did}` |
| `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/repost`, retain `false`, QoS `0` |

#### Payload

`Repost` payloads are JSON object. Required fields: `uri`, `cid`, `did`, `subject_uri`, `subject_cid`, `created_at`, `indexed_at`, `seq`, `collection`, `lang`.

- **`uri`** (string, required): AT-URI of the repost record
- **`cid`** (string, required): Content Identifier of the repost
- **`did`** (string, required): DID of the user who reposted
- **`handle`** (string, optional): Handle of the user who reposted
- **`subject_uri`** (string, required): AT-URI of the reposted post
- **`subject_cid`** (string, required): CID of the reposted post
- **`created_at`** (string, required): ISO 8601 timestamp of repost creation
- **`indexed_at`** (string, required): ISO 8601 timestamp of indexing
- **`seq`** (int64, required): Firehose sequence number
- **`collection`** (string, required): AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty.
- **`lang`** (string, required): Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "uri": "string",
  "cid": "string",
  "did": "string",
  "handle": "string",
  "subject_uri": "string",
  "subject_cid": "string",
  "created_at": "string",
  "indexed_at": "string",
  "seq": 0,
  "collection": "string",
  "lang": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Follow

CloudEvents type: `Bluesky.Graph.Follow`

#### What it tells you

A follow relationship between users A follow relationship between users

#### Identity

Each event identifies the real-world resource with `{did}`. `{did}` is DID of the follower. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bluesky`, key `{did}` |
| `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/follow`, retain `false`, QoS `0` |

#### Payload

`Follow` payloads are JSON object. Required fields: `uri`, `cid`, `did`, `subject`, `created_at`, `indexed_at`, `seq`, `collection`, `lang`.

- **`uri`** (string, required): AT-URI of the follow record
- **`cid`** (string, required): Content Identifier of the follow
- **`did`** (string, required): DID of the follower
- **`handle`** (string, optional): Handle of the follower
- **`subject`** (string, required): DID of the followed user
- **`subject_handle`** (string, optional): Handle of the followed user
- **`created_at`** (string, required): ISO 8601 timestamp of follow creation
- **`indexed_at`** (string, required): ISO 8601 timestamp of indexing
- **`seq`** (int64, required): Firehose sequence number
- **`collection`** (string, required): AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty.
- **`lang`** (string, required): Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "uri": "string",
  "cid": "string",
  "did": "string",
  "handle": "string",
  "subject": "string",
  "subject_handle": "string",
  "created_at": "string",
  "indexed_at": "string",
  "seq": 0,
  "collection": "string",
  "lang": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Block

CloudEvents type: `Bluesky.Graph.Block`

#### What it tells you

A block relationship between users A block relationship between users

#### Identity

Each event identifies the real-world resource with `{did}`. `{did}` is DID of the blocker. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bluesky`, key `{did}` |
| `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/block`, retain `false`, QoS `0` |

#### Payload

`Block` payloads are JSON object. Required fields: `uri`, `cid`, `did`, `subject`, `created_at`, `indexed_at`, `seq`, `collection`, `lang`.

- **`uri`** (string, required): AT-URI of the block record
- **`cid`** (string, required): Content Identifier of the block
- **`did`** (string, required): DID of the blocker
- **`handle`** (string, optional): Handle of the blocker
- **`subject`** (string, required): DID of the blocked user
- **`subject_handle`** (string, optional): Handle of the blocked user
- **`created_at`** (string, required): ISO 8601 timestamp of block creation
- **`indexed_at`** (string, required): ISO 8601 timestamp of indexing
- **`seq`** (int64, required): Firehose sequence number
- **`collection`** (string, required): AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty.
- **`lang`** (string, required): Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "uri": "string",
  "cid": "string",
  "did": "string",
  "handle": "string",
  "subject": "string",
  "subject_handle": "string",
  "created_at": "string",
  "indexed_at": "string",
  "seq": 0,
  "collection": "string",
  "lang": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Profile

CloudEvents type: `Bluesky.Actor.Profile`

#### What it tells you

A user profile update A user profile update

#### Identity

Each event identifies the real-world resource with `{did}`. `{did}` is decentralized Identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `bluesky`, key `{did}` |
| `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/profile`, retain `false`, QoS `0` |

#### Payload

`Profile` payloads are JSON object. Required fields: `did`, `handle`, `created_at`, `indexed_at`, `seq`, `collection`, `lang`.

- **`did`** (string, required): Decentralized Identifier
- **`handle`** (string, required): User handle
- **`display_name`** (string, optional): Display name
- **`description`** (string, optional): Bio/description
- **`avatar`** (string, optional): Avatar image URL
- **`banner`** (string, optional): Banner image URL
- **`created_at`** (string, required): ISO 8601 timestamp of profile creation
- **`indexed_at`** (string, required): ISO 8601 timestamp of indexing
- **`seq`** (int64, required): Firehose sequence number
- **`collection`** (string, required): AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty.
- **`lang`** (string, required): Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "did": "string",
  "handle": "string",
  "display_name": "string",
  "description": "string",
  "avatar": "string",
  "banner": "string",
  "created_at": "string",
  "indexed_at": "string",
  "seq": 0,
  "collection": "string",
  "lang": "string"
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

- xRegistry manifest: [`xreg/bluesky.xreg.json`](xreg/bluesky.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
