# Bluesky Firehose Producer Events

MQTT/5.0 non-retained firehose variants of the Bluesky CloudEvents. Each record family gets a dedicated topic with the kebab record name baked as the trailing segment so subscribers can wildcard per family. QoS 0, retain=false — there is no LKV slot for a firehose.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 2 |

## Endpoints

### Endpoint `BlueskyFirehose.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`BlueskyFirehose`](#messagegroup-blueskyfirehose) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `bluesky` |
| Kafka key | `{did}` |
| Deployed | False |

### Endpoint `BlueskyFirehose.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`BlueskyFirehose.mqtt`](#messagegroup-blueskyfirehosemqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `BlueskyFirehose`
<a id="messagegroup-blueskyfirehose"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `BlueskyFirehose.Kafka` (KAFKA) |
| Messages | 6 |

#### Message `Bluesky.Feed.Post`
<a id="message-blueskyfeedpost"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Feed.Post`](#schema-blueskyfeedpost) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Post` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Kafka` | `KAFKA` | topic `bluesky`; key `{did}` |

#### Message `Bluesky.Feed.Like`
<a id="message-blueskyfeedlike"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Feed.Like`](#schema-blueskyfeedlike) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Like` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Kafka` | `KAFKA` | topic `bluesky`; key `{did}` |

#### Message `Bluesky.Feed.Repost`
<a id="message-blueskyfeedrepost"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Feed.Repost`](#schema-blueskyfeedrepost) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Repost` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Kafka` | `KAFKA` | topic `bluesky`; key `{did}` |

#### Message `Bluesky.Graph.Follow`
<a id="message-blueskygraphfollow"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Graph.Follow`](#schema-blueskygraphfollow) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Graph.Follow` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Kafka` | `KAFKA` | topic `bluesky`; key `{did}` |

#### Message `Bluesky.Graph.Block`
<a id="message-blueskygraphblock"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Graph.Block`](#schema-blueskygraphblock) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Graph.Block` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Kafka` | `KAFKA` | topic `bluesky`; key `{did}` |

#### Message `Bluesky.Actor.Profile`
<a id="message-blueskyactorprofile"></a>

| Field | Value |
| --- | --- |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Actor.Profile`](#schema-blueskyactorprofile) |
| Transport override | `None` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Actor.Profile` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Kafka` | `KAFKA` | topic `bluesky`; key `{did}` |

### Messagegroup `BlueskyFirehose.mqtt`
<a id="messagegroup-blueskyfirehosemqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 non-retained firehose variants of the Bluesky CloudEvents. Each record family gets a dedicated topic with the kebab record name baked as the trailing segment so subscribers can wildcard per family. QoS 0, retain=false — there is no LKV slot for a firehose. |
| Transport bindings | `BlueskyFirehose.Mqtt` (MQTT/5.0) |
| Messages | 6 |

#### Message `Bluesky.Feed.Post.mqtt`
<a id="message-blueskyfeedpostmqtt"></a>

| Field | Value |
| --- | --- |
| Name | Post |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Feed.Post`](#schema-blueskyfeedpost) |
| Base message chain | `/messagegroups/BlueskyFirehose/messages/Bluesky.Feed.Post` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Post` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Mqtt` | `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/post` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/post` |
| Retain | False |

#### Message `Bluesky.Feed.Like.mqtt`
<a id="message-blueskyfeedlikemqtt"></a>

| Field | Value |
| --- | --- |
| Name | Like |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Feed.Like`](#schema-blueskyfeedlike) |
| Base message chain | `/messagegroups/BlueskyFirehose/messages/Bluesky.Feed.Like` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Like` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Mqtt` | `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/like` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/like` |
| Retain | False |

#### Message `Bluesky.Feed.Repost.mqtt`
<a id="message-blueskyfeedrepostmqtt"></a>

| Field | Value |
| --- | --- |
| Name | Repost |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Feed.Repost`](#schema-blueskyfeedrepost) |
| Base message chain | `/messagegroups/BlueskyFirehose/messages/Bluesky.Feed.Repost` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Feed.Repost` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Mqtt` | `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/repost` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/repost` |
| Retain | False |

#### Message `Bluesky.Graph.Follow.mqtt`
<a id="message-blueskygraphfollowmqtt"></a>

| Field | Value |
| --- | --- |
| Name | Follow |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Graph.Follow`](#schema-blueskygraphfollow) |
| Base message chain | `/messagegroups/BlueskyFirehose/messages/Bluesky.Graph.Follow` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Graph.Follow` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Mqtt` | `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/follow` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/follow` |
| Retain | False |

#### Message `Bluesky.Graph.Block.mqtt`
<a id="message-blueskygraphblockmqtt"></a>

| Field | Value |
| --- | --- |
| Name | Block |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Graph.Block`](#schema-blueskygraphblock) |
| Base message chain | `/messagegroups/BlueskyFirehose/messages/Bluesky.Graph.Block` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Graph.Block` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Mqtt` | `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/block` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/block` |
| Retain | False |

#### Message `Bluesky.Actor.Profile.mqtt`
<a id="message-blueskyactorprofilemqtt"></a>

| Field | Value |
| --- | --- |
| Name | Profile |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/BlueskyFirehose.jstruct/schemas/Bluesky.Actor.Profile`](#schema-blueskyactorprofile) |
| Base message chain | `/messagegroups/BlueskyFirehose/messages/Bluesky.Actor.Profile` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents version | `string` | `True` | `1.0` |
| `type` | Event type | `string` | `True` | `Bluesky.Actor.Profile` |
| `source` | Source Firehose URL | `uritemplate` | `True` | `{firehoseurl}` |
| `subject` | Decentralized Identifier | `uritemplate` | `True` | `{did}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `BlueskyFirehose.Mqtt` | `MQTT/5.0` | topic `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/profile` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `social/intl/bluesky/bluesky/{collection}/{lang}/{did}/profile` |
| Retain | False |

## Schemagroups

### Schemagroup `BlueskyFirehose.jstruct`
<a id="schemagroup-blueskyfirehosejstruct"></a>

#### Schema `Bluesky.Feed.Post`
<a id="schema-blueskyfeedpost"></a>

| Field | Value |
| --- | --- |
| Name | Post |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Bluesky/Feed/Post` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Bluesky/Feed/Post` |
| Type | `object` |

###### Object `Post`
<a id="schema-node-post"></a>

A post in the Bluesky feed

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `uri` | `string` | `True` | AT-URI of the post (at://did:plc:xxx/app.bsky.feed.post/xxx) | - | - | - |
| `cid` | `string` | `True` | Content Identifier (CID) of the post | - | - | - |
| `did` | `string` | `True` | Decentralized Identifier of the author | - | - | - |
| `handle` | `string` | `False` | Handle of the author | - | default=`-` | default=`-` |
| `text` | `string` | `True` | Text content of the post | - | - | - |
| `langs` | array of `string` | `True` | Language codes for the post | - | default=`[]` | default=`[]` |
| `reply_parent` | `string` | `False` | AT-URI of parent post if this is a reply | - | default=`-` | default=`-` |
| `reply_root` | `string` | `False` | AT-URI of root post in thread | - | default=`-` | default=`-` |
| `embed_type` | `string` | `False` | Type of embedded content (images, external, record, etc.) | - | default=`-` | default=`-` |
| `embed_uri` | `string` | `False` | URI of embedded content | - | default=`-` | default=`-` |
| `facets` | `string` | `False` | JSON string of rich text facets (mentions, links, tags) | - | default=`-` | default=`-` |
| `tags` | array of `string` | `True` | Hashtags in the post | - | default=`[]` | default=`[]` |
| `created_at` | `string` | `True` | ISO 8601 timestamp of post creation | - | - | - |
| `indexed_at` | `string` | `True` | ISO 8601 timestamp of when the post was indexed | - | - | - |
| `seq` | `int64` | `True` | Firehose sequence number | - | - | - |
| `collection` | `string` | `True` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | - | - | - |
| `lang` | `string` | `True` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | - | - | - |

#### Schema `Bluesky.Feed.Like`
<a id="schema-blueskyfeedlike"></a>

| Field | Value |
| --- | --- |
| Name | Like |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Bluesky/Feed/Like` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Bluesky/Feed/Like` |
| Type | `object` |

###### Object `Like`
<a id="schema-node-like"></a>

A like on a post

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `uri` | `string` | `True` | AT-URI of the like record | - | - | - |
| `cid` | `string` | `True` | Content Identifier of the like | - | - | - |
| `did` | `string` | `True` | DID of the user who liked | - | - | - |
| `handle` | `string` | `False` | Handle of the user who liked | - | default=`-` | default=`-` |
| `subject_uri` | `string` | `True` | AT-URI of the liked post | - | - | - |
| `subject_cid` | `string` | `True` | CID of the liked post | - | - | - |
| `created_at` | `string` | `True` | ISO 8601 timestamp of like creation | - | - | - |
| `indexed_at` | `string` | `True` | ISO 8601 timestamp of indexing | - | - | - |
| `seq` | `int64` | `True` | Firehose sequence number | - | - | - |
| `collection` | `string` | `True` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | - | - | - |
| `lang` | `string` | `True` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | - | - | - |

#### Schema `Bluesky.Feed.Repost`
<a id="schema-blueskyfeedrepost"></a>

| Field | Value |
| --- | --- |
| Name | Repost |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Bluesky/Feed/Repost` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Bluesky/Feed/Repost` |
| Type | `object` |

###### Object `Repost`
<a id="schema-node-repost"></a>

A repost of a post

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `uri` | `string` | `True` | AT-URI of the repost record | - | - | - |
| `cid` | `string` | `True` | Content Identifier of the repost | - | - | - |
| `did` | `string` | `True` | DID of the user who reposted | - | - | - |
| `handle` | `string` | `False` | Handle of the user who reposted | - | default=`-` | default=`-` |
| `subject_uri` | `string` | `True` | AT-URI of the reposted post | - | - | - |
| `subject_cid` | `string` | `True` | CID of the reposted post | - | - | - |
| `created_at` | `string` | `True` | ISO 8601 timestamp of repost creation | - | - | - |
| `indexed_at` | `string` | `True` | ISO 8601 timestamp of indexing | - | - | - |
| `seq` | `int64` | `True` | Firehose sequence number | - | - | - |
| `collection` | `string` | `True` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | - | - | - |
| `lang` | `string` | `True` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | - | - | - |

#### Schema `Bluesky.Graph.Follow`
<a id="schema-blueskygraphfollow"></a>

| Field | Value |
| --- | --- |
| Name | Follow |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Bluesky/Graph/Follow` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Bluesky/Graph/Follow` |
| Type | `object` |

###### Object `Follow`
<a id="schema-node-follow"></a>

A follow relationship between users

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `uri` | `string` | `True` | AT-URI of the follow record | - | - | - |
| `cid` | `string` | `True` | Content Identifier of the follow | - | - | - |
| `did` | `string` | `True` | DID of the follower | - | - | - |
| `handle` | `string` | `False` | Handle of the follower | - | default=`-` | default=`-` |
| `subject` | `string` | `True` | DID of the followed user | - | - | - |
| `subject_handle` | `string` | `False` | Handle of the followed user | - | default=`-` | default=`-` |
| `created_at` | `string` | `True` | ISO 8601 timestamp of follow creation | - | - | - |
| `indexed_at` | `string` | `True` | ISO 8601 timestamp of indexing | - | - | - |
| `seq` | `int64` | `True` | Firehose sequence number | - | - | - |
| `collection` | `string` | `True` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | - | - | - |
| `lang` | `string` | `True` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | - | - | - |

#### Schema `Bluesky.Graph.Block`
<a id="schema-blueskygraphblock"></a>

| Field | Value |
| --- | --- |
| Name | Block |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Bluesky/Graph/Block` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Bluesky/Graph/Block` |
| Type | `object` |

###### Object `Block`
<a id="schema-node-block"></a>

A block relationship between users

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `uri` | `string` | `True` | AT-URI of the block record | - | - | - |
| `cid` | `string` | `True` | Content Identifier of the block | - | - | - |
| `did` | `string` | `True` | DID of the blocker | - | - | - |
| `handle` | `string` | `False` | Handle of the blocker | - | default=`-` | default=`-` |
| `subject` | `string` | `True` | DID of the blocked user | - | - | - |
| `subject_handle` | `string` | `False` | Handle of the blocked user | - | default=`-` | default=`-` |
| `created_at` | `string` | `True` | ISO 8601 timestamp of block creation | - | - | - |
| `indexed_at` | `string` | `True` | ISO 8601 timestamp of indexing | - | - | - |
| `seq` | `int64` | `True` | Firehose sequence number | - | - | - |
| `collection` | `string` | `True` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | - | - | - |
| `lang` | `string` | `True` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | - | - | - |

#### Schema `Bluesky.Actor.Profile`
<a id="schema-blueskyactorprofile"></a>

| Field | Value |
| --- | --- |
| Name | Profile |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Bluesky/Actor/Profile` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Bluesky/Actor/Profile` |
| Type | `object` |

###### Object `Profile`
<a id="schema-node-profile"></a>

A user profile update

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `did` | `string` | `True` | Decentralized Identifier | - | - | - |
| `handle` | `string` | `True` | User handle | - | - | - |
| `display_name` | `string` | `False` | Display name | - | default=`-` | default=`-` |
| `description` | `string` | `False` | Bio/description | - | default=`-` | default=`-` |
| `avatar` | `string` | `False` | Avatar image URL | - | default=`-` | default=`-` |
| `banner` | `string` | `False` | Banner image URL | - | default=`-` | default=`-` |
| `created_at` | `string` | `True` | ISO 8601 timestamp of profile creation | - | - | - |
| `indexed_at` | `string` | `True` | ISO 8601 timestamp of indexing | - | - | - |
| `seq` | `int64` | `True` | Firehose sequence number | - | - | - |
| `collection` | `string` | `True` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | - | - | - |
| `lang` | `string` | `True` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | - | - | - |

### Schemagroup `BlueskyFirehose.avro`
<a id="schemagroup-blueskyfirehoseavro"></a>

#### Schema `Bluesky.Feed.Post`
<a id="schema-blueskyfeedpost"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Post |
| Namespace | Bluesky.Feed |
| Type | `record` |
| Doc | A post in the Bluesky feed |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `string` | AT-URI of the post (at://did:plc:xxx/app.bsky.feed.post/xxx) | `-` |
| `cid` | `string` | Content Identifier (CID) of the post | `-` |
| `did` | `string` | Decentralized Identifier of the author | `-` |
| `handle` | `null` \| `string` | Handle of the author | `-` |
| `text` | `string` | Text content of the post | `-` |
| `langs` | array of `string` | Language codes for the post | `[]` |
| `reply_parent` | `null` \| `string` | AT-URI of parent post if this is a reply | `-` |
| `reply_root` | `null` \| `string` | AT-URI of root post in thread | `-` |
| `embed_type` | `null` \| `string` | Type of embedded content (images, external, record, etc.) | `-` |
| `embed_uri` | `null` \| `string` | URI of embedded content | `-` |
| `facets` | `null` \| `string` | JSON string of rich text facets (mentions, links, tags) | `-` |
| `tags` | array of `string` | Hashtags in the post | `[]` |
| `created_at` | `string` | ISO 8601 timestamp of post creation | `-` |
| `indexed_at` | `string` | ISO 8601 timestamp of when the post was indexed | `-` |
| `seq` | `long` | Firehose sequence number | `-` |
| `collection` | `string` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | `-` |
| `lang` | `string` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | `und` |

#### Schema `Bluesky.Feed.Like`
<a id="schema-blueskyfeedlike"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Like |
| Namespace | Bluesky.Feed |
| Type | `record` |
| Doc | A like on a post |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `string` | AT-URI of the like record | `-` |
| `cid` | `string` | Content Identifier of the like | `-` |
| `did` | `string` | DID of the user who liked | `-` |
| `handle` | `null` \| `string` | Handle of the user who liked | `-` |
| `subject_uri` | `string` | AT-URI of the liked post | `-` |
| `subject_cid` | `string` | CID of the liked post | `-` |
| `created_at` | `string` | ISO 8601 timestamp of like creation | `-` |
| `indexed_at` | `string` | ISO 8601 timestamp of indexing | `-` |
| `seq` | `long` | Firehose sequence number | `-` |
| `collection` | `string` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | `-` |
| `lang` | `string` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | `und` |

#### Schema `Bluesky.Feed.Repost`
<a id="schema-blueskyfeedrepost"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Repost |
| Namespace | Bluesky.Feed |
| Type | `record` |
| Doc | A repost of a post |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `string` | AT-URI of the repost record | `-` |
| `cid` | `string` | Content Identifier of the repost | `-` |
| `did` | `string` | DID of the user who reposted | `-` |
| `handle` | `null` \| `string` | Handle of the user who reposted | `-` |
| `subject_uri` | `string` | AT-URI of the reposted post | `-` |
| `subject_cid` | `string` | CID of the reposted post | `-` |
| `created_at` | `string` | ISO 8601 timestamp of repost creation | `-` |
| `indexed_at` | `string` | ISO 8601 timestamp of indexing | `-` |
| `seq` | `long` | Firehose sequence number | `-` |
| `collection` | `string` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | `-` |
| `lang` | `string` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | `und` |

#### Schema `Bluesky.Graph.Follow`
<a id="schema-blueskygraphfollow"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Follow |
| Namespace | Bluesky.Graph |
| Type | `record` |
| Doc | A follow relationship between users |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `string` | AT-URI of the follow record | `-` |
| `cid` | `string` | Content Identifier of the follow | `-` |
| `did` | `string` | DID of the follower | `-` |
| `handle` | `null` \| `string` | Handle of the follower | `-` |
| `subject` | `string` | DID of the followed user | `-` |
| `subject_handle` | `null` \| `string` | Handle of the followed user | `-` |
| `created_at` | `string` | ISO 8601 timestamp of follow creation | `-` |
| `indexed_at` | `string` | ISO 8601 timestamp of indexing | `-` |
| `seq` | `long` | Firehose sequence number | `-` |
| `collection` | `string` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | `-` |
| `lang` | `string` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | `und` |

#### Schema `Bluesky.Graph.Block`
<a id="schema-blueskygraphblock"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Block |
| Namespace | Bluesky.Graph |
| Type | `record` |
| Doc | A block relationship between users |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `string` | AT-URI of the block record | `-` |
| `cid` | `string` | Content Identifier of the block | `-` |
| `did` | `string` | DID of the blocker | `-` |
| `handle` | `null` \| `string` | Handle of the blocker | `-` |
| `subject` | `string` | DID of the blocked user | `-` |
| `subject_handle` | `null` \| `string` | Handle of the blocked user | `-` |
| `created_at` | `string` | ISO 8601 timestamp of block creation | `-` |
| `indexed_at` | `string` | ISO 8601 timestamp of indexing | `-` |
| `seq` | `long` | Firehose sequence number | `-` |
| `collection` | `string` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | `-` |
| `lang` | `string` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | `und` |

#### Schema `Bluesky.Actor.Profile`
<a id="schema-blueskyactorprofile"></a>

| Field | Value |
| --- | --- |
| Format | Avro |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro |

###### Avro

| Field | Value |
| --- | --- |
| Name | Profile |
| Namespace | Bluesky.Actor |
| Type | `record` |
| Doc | A user profile update |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `did` | `string` | Decentralized Identifier | `-` |
| `handle` | `string` | User handle | `-` |
| `display_name` | `null` \| `string` | Display name | `-` |
| `description` | `null` \| `string` | Bio/description | `-` |
| `avatar` | `null` \| `string` | Avatar image URL | `-` |
| `banner` | `null` \| `string` | Banner image URL | `-` |
| `created_at` | `string` | ISO 8601 timestamp of profile creation | `-` |
| `indexed_at` | `string` | ISO 8601 timestamp of indexing | `-` |
| `seq` | `long` | Firehose sequence number | `-` |
| `collection` | `string` | AT Protocol record collection NSID (e.g. 'app.bsky.feed.post'). Populated by the bridge from the upstream firehose commit and used as the second MQTT topic segment so subscribers can wildcard on a record family (e.g. all posts via 'app.bsky.feed.post/+/+/post'). Lowercase; never empty. | `-` |
| `lang` | `string` | Primary BCP-47 language tag for the record. For posts this is the first entry of `record.langs[]`; for records without a language field the bridge emits the sentinel 'und' (BCP-47 'undetermined'). Always lowercase, so subscribers can wildcard on `…/ja/+/+`. | `und` |
