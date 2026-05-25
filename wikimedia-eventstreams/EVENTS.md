# Wikimedia EventStreams RecentChange Bridge Events

MQTT/5.0 non-retained Wikimedia EventStreams recentchange firehose. Single family (recent-change) baked as the trailing topic segment so subscribers can wildcard per wiki/namespace/event. QoS 0, retain=false.

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
| Schemagroups | 1 |

## Endpoints

### Endpoint `Wikimedia.EventStreams.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Wikimedia.EventStreams`](#messagegroup-wikimediaeventstreams) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `wikimedia-eventstreams` |
| Kafka key | `{event_id}` |
| Deployed | False |

### Endpoint `Wikimedia.EventStreams.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`Wikimedia.EventStreams.mqtt`](#messagegroup-wikimediaeventstreamsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |

## Messagegroups

### Messagegroup `Wikimedia.EventStreams`
<a id="messagegroup-wikimediaeventstreams"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Wikimedia.EventStreams.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Wikimedia.EventStreams.RecentChange`
<a id="message-wikimediaeventstreamsrecentchange"></a>

Public recentchange events from Wikimedia EventStreams. Each event describes one edit, page creation, log action, categorization change, or related MediaWiki recentchanges entry from across Wikimedia projects.

| Field | Value |
| --- | --- |
| Name | RecentChange |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Wikimedia.EventStreams.jstruct/schemas/Wikimedia.EventStreams.RecentChange`](#schema-wikimediaeventstreamsrecentchange) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Wikimedia.EventStreams.RecentChange` |
| `source` |  | `string` | `False` | `https://stream.wikimedia.org/v2/stream/recentchange` |
| `subject` |  | `uritemplate` | `False` | `{event_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Wikimedia.EventStreams.Kafka` | `KAFKA` | topic `wikimedia-eventstreams`; key `{event_id}` |

### Messagegroup `Wikimedia.EventStreams.mqtt`
<a id="messagegroup-wikimediaeventstreamsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 non-retained Wikimedia EventStreams recentchange firehose. Single family (recent-change) baked as the trailing topic segment so subscribers can wildcard per wiki/namespace/event. QoS 0, retain=false. |
| Transport bindings | `Wikimedia.EventStreams.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `Wikimedia.EventStreams.RecentChange.mqtt`
<a id="message-wikimediaeventstreamsrecentchangemqtt"></a>

Public recentchange events from Wikimedia EventStreams. Each event describes one edit, page creation, log action, categorization change, or related MediaWiki recentchanges entry from across Wikimedia projects.

| Field | Value |
| --- | --- |
| Name | RecentChange |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Wikimedia.EventStreams.jstruct/schemas/Wikimedia.EventStreams.RecentChange`](#schema-wikimediaeventstreamsrecentchange) |
| Base message chain | `/messagegroups/Wikimedia.EventStreams/messages/Wikimedia.EventStreams.RecentChange` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Wikimedia.EventStreams.RecentChange` |
| `source` |  | `string` | `False` | `https://stream.wikimedia.org/v2/stream/recentchange` |
| `subject` |  | `uritemplate` | `False` | `{wiki}/{namespace}/{event_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Wikimedia.EventStreams.Mqtt` | `MQTT/5.0` | topic `-` |

## Schemagroups

### Schemagroup `Wikimedia.EventStreams.jstruct`
<a id="schemagroup-wikimediaeventstreamsjstruct"></a>

#### Schema `Wikimedia.EventStreams.RecentChange`
<a id="schema-wikimediaeventstreamsrecentchange"></a>

| Field | Value |
| --- | --- |
| Name | RecentChange |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Wikimedia/EventStreams/RecentChange` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `RecentChange`
<a id="schema-node-recentchange"></a>

Normalized representation of Wikimedia's mediawiki/recentchange event schema. This contract preserves the documented recentchange payload while renaming the upstream $schema field to schema_uri and serializing the variant log_params field into log_params_json for stable generated types.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Wikimedia/EventStreams/RecentChange` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | `string` | `True` | Top-level copy of meta.id so downstream validators and consumers can resolve the CloudEvents subject and Kafka key from the event payload itself. | - | - | - |
| `event_time` | `string` | `True` | Top-level copy of meta.dt in ISO-8601 UTC format so downstream validators and consumers can resolve the CloudEvents time attribute from the payload itself. | - | - | - |
| `schema_uri` | `string` | `True` | URI of the upstream Wikimedia JSON schema from the $schema field on the original event payload. | - | - | - |
| `meta` | [object `RecentChange.meta`](#schema-node-recentchangemeta) | `True` | Wikimedia EventStreams envelope metadata describing the event identity, domain, stream, and Kafka-origin details. | - | - | - |
| `id` | `union` | `False` | MediaWiki recentchanges row identifier (rcid) for the event, stringified because some Wikimedia wikis already exceed signed 32-bit integer range. | - | - | - |
| `type` | `string` | `True` | Recentchange type such as edit, new, log, categorize, or external. | - | - | - |
| `namespace_id` | `integer` | `True` | Numeric MediaWiki namespace identifier for the affected page (0 = main, 1 = talk, 6 = file, 14 = category, -1 for special log events). Renamed from ``namespace`` to free that name for the kebab-case bucket that is also used as the {namespace} MQTT topic axis. | - | - | - |
| `title` | `string` | `True` | Affected page title in MediaWiki prefixed text form. | - | - | - |
| `title_url` | `union` | `False` | Canonical page URL for the affected title when present in the upstream payload. | - | - | - |
| `comment` | `union` | `False` | Edit or log comment as supplied by the upstream recentchange record. | - | - | - |
| `timestamp` | `integer` | `True` | Unix timestamp derived from the MediaWiki rc_timestamp value. | - | - | - |
| `user` | `string` | `True` | User name or IP address associated with the change. | - | - | - |
| `bot` | `union` | `False` | Whether the recentchange entry was flagged as a bot edit. | - | - | - |
| `minor` | `union` | `False` | Whether the recentchange entry was flagged as a minor change. | - | - | - |
| `patrolled` | `union` | `False` | Whether the recentchange entry had been patrolled when the event was emitted. | - | - | - |
| `length` | [object `RecentChange.length`](#schema-node-recentchangelength) | `False` | Page lengths before and after the change, measured in bytes or characters as provided by MediaWiki. | - | - | - |
| `revision` | [object `RecentChange.revision`](#schema-node-recentchangerevision) | `False` | Old and new MediaWiki revision identifiers associated with the change. | - | - | - |
| `server_url` | `union` | `False` | Canonical server URL for the wiki that emitted the event. | - | - | - |
| `server_name` | `union` | `False` | Server host name of the wiki that emitted the event. | - | - | - |
| `server_script_path` | `union` | `False` | MediaWiki script path on the emitting wiki. | - | - | - |
| `wiki` | `string` | `True` | Internal Wikimedia wiki identifier such as enwiki, commonswiki, or wikidatawiki. | - | - | - |
| `namespace` | `string` | `True` | Kebab-case bucket label for the MediaWiki namespace (e.g. ``main`` for 0, ``talk`` for 1, ``file`` for 6, ``category`` for 14, ``ns-<n>`` for unrecognised values). Used as the {namespace} MQTT topic segment; subscribers can wildcard per wiki/namespace without parsing the integer id. | - | - | - |
| `parsedcomment` | `union` | `False` | HTML-parsed form of the recentchange comment when Wikimedia provides it. | - | - | - |
| `notify_url` | `union` | `False` | URL that points to a diff view or other relevant page for the change. | - | - | - |
| `log_type` | `union` | `False` | MediaWiki log type for log events, such as move, delete, or patrol. | - | - | - |
| `log_action` | `union` | `False` | Specific MediaWiki log action name for log events. | - | - | - |
| `log_action_comment` | `union` | `False` | Additional comment field emitted for some MediaWiki log actions. | - | - | - |
| `log_id` | `union` | `False` | MediaWiki log identifier associated with the event when the change is a log entry, stringified for stable cross-language handling. | - | - | - |
| `log_params_json` | `union` | `False` | Serialized form of the upstream log_params field, which may be an object, array, or string in the raw Wikimedia payload. | - | - | - |

###### Object `RecentChange.meta`
<a id="schema-node-recentchangemeta"></a>

Wikimedia EventStreams envelope metadata describing the event identity, domain, stream, and Kafka-origin details.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `uri` | `string` | `False` | URI of the Wikimedia entity or page the event pertains to, when provided by the upstream stream. | - | - | - |
| `request_id` | `string` | `False` | Unique request identifier assigned by Wikimedia for the request that caused the event. | - | - | - |
| `id` | `string` | `True` | Globally unique Wikimedia event UUID for this recentchange record. | - | - | - |
| `domain` | `string` | `True` | Wikimedia domain the event pertains to, such as www.wikipedia.org or www.wikidata.org. | - | - | - |
| `stream` | `string` | `True` | Name of the upstream EventStreams stream that emitted the event, typically mediawiki.recentchange. | - | - | - |
| `topic` | `string` | `False` | Underlying Wikimedia Kafka topic that carried the event before it was exposed through EventStreams. | - | - | - |
| `partition` | `integer` | `False` | Underlying Kafka partition number from Wikimedia's internal stream metadata. | - | - | - |
| `offset` | `union` | `False` | Underlying Kafka offset from Wikimedia's internal stream metadata, stringified to avoid range loss across generated languages and validators. | - | - | - |
| `dt` | `string` | `True` | UTC event timestamp in ISO-8601 format from the upstream metadata block. | - | - | - |

###### Object `RecentChange.length`
<a id="schema-node-recentchangelength"></a>

Page lengths before and after the change, measured in bytes or characters as provided by MediaWiki.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `old` | `union` | `False` | Length of the page before the change. | - | - | - |
| `new` | `union` | `False` | Length of the page after the change. | - | - | - |

###### Object `RecentChange.revision`
<a id="schema-node-recentchangerevision"></a>

Old and new MediaWiki revision identifiers associated with the change.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `old` | `union` | `False` | Previous revision identifier before the change, stringified because recent Wikimedia revision identifiers can exceed signed 32-bit integer range. | - | - | - |
| `new` | `union` | `False` | New revision identifier after the change, stringified because recent Wikimedia revision identifiers can exceed signed 32-bit integer range. | - | - | - |
