# Table of Contents

- [Wikimedia.EventStreams](#message-group-wikimediaeventstreams)
  - [Wikimedia.EventStreams.RecentChange](#message-wikimediaeventstreamsrecentchange)
- [Wikimedia.EventStreams.mqtt](#message-group-wikimediaeventstreamsmqtt)
  - [Wikimedia.EventStreams.RecentChange.mqtt](#message-wikimediaeventstreamsrecentchangemqtt)

---

## Message Group: Wikimedia.EventStreams
---
### Message: Wikimedia.EventStreams.RecentChange
*Public recentchange events from Wikimedia EventStreams. Each event describes one edit, page creation, log action, categorization change, or related MediaWiki recentchanges entry from across Wikimedia projects.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Wikimedia.EventStreams.RecentChange` |
| `source` |  | `` | `False` | `https://stream.wikimedia.org/v2/stream/recentchange` |
| `subject` |  | `uritemplate` | `False` | `{event_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RecentChange
*Normalized representation of Wikimedia's mediawiki/recentchange event schema. This contract preserves the documented recentchange payload while renaming the upstream $schema field to schema_uri and serializing the variant log_params field into log_params_json for stable generated types.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `event_id` | *string* | - | `True` | Top-level copy of meta.id so downstream validators and consumers can resolve the CloudEvents subject and Kafka key from the event payload itself. |
| `event_time` | *string* | - | `True` | Top-level copy of meta.dt in ISO-8601 UTC format so downstream validators and consumers can resolve the CloudEvents time attribute from the payload itself. |
| `schema_uri` | *string* | - | `True` | URI of the upstream Wikimedia JSON schema from the $schema field on the original event payload. |
| `meta` | [Object RecentChange.meta](#object-recentchangemeta) | - | `True` | Wikimedia EventStreams envelope metadata describing the event identity, domain, stream, and Kafka-origin details. |
| `id` | *string* (optional) | - | `False` | MediaWiki recentchanges row identifier (rcid) for the event, stringified because some Wikimedia wikis already exceed signed 32-bit integer range. |
| `type` | *string* | - | `True` | Recentchange type such as edit, new, log, categorize, or external. |
| `namespace` | *integer* | - | `True` | Numeric MediaWiki namespace identifier for the affected page, or -1 for special log events. |
| `title` | *string* | - | `True` | Affected page title in MediaWiki prefixed text form. |
| `title_url` | *string* (optional) | - | `False` | Canonical page URL for the affected title when present in the upstream payload. |
| `comment` | *string* (optional) | - | `False` | Edit or log comment as supplied by the upstream recentchange record. |
| `timestamp` | *integer* | - | `True` | Unix timestamp derived from the MediaWiki rc_timestamp value. |
| `user` | *string* | - | `True` | User name or IP address associated with the change. |
| `bot` | *boolean* (optional) | - | `False` | Whether the recentchange entry was flagged as a bot edit. |
| `minor` | *boolean* (optional) | - | `False` | Whether the recentchange entry was flagged as a minor change. |
| `patrolled` | *boolean* (optional) | - | `False` | Whether the recentchange entry had been patrolled when the event was emitted. |
| `length` | [Object RecentChange.length](#object-recentchangelength) | - | `False` | Page lengths before and after the change, measured in bytes or characters as provided by MediaWiki. |
| `revision` | [Object RecentChange.revision](#object-recentchangerevision) | - | `False` | Old and new MediaWiki revision identifiers associated with the change. |
| `server_url` | *string* (optional) | - | `False` | Canonical server URL for the wiki that emitted the event. |
| `server_name` | *string* (optional) | - | `False` | Server host name of the wiki that emitted the event. |
| `server_script_path` | *string* (optional) | - | `False` | MediaWiki script path on the emitting wiki. |
| `wiki` | *string* | - | `True` | Internal Wikimedia wiki identifier such as enwiki, commonswiki, or wikidatawiki. |
| `namespace_bucket` | *string* | - | `True` | Kebab-case bucket label for the MediaWiki namespace number (e.g. main for 0, talk for 1, file for 6, category for 14, ns-<n> for unrecognised values). Replicates the MQTT topic axis so subscribers can validate the topic segment against the payload. |
| `parsedcomment` | *string* (optional) | - | `False` | HTML-parsed form of the recentchange comment when Wikimedia provides it. |
| `notify_url` | *string* (optional) | - | `False` | URL that points to a diff view or other relevant page for the change. |
| `log_type` | *string* (optional) | - | `False` | MediaWiki log type for log events, such as move, delete, or patrol. |
| `log_action` | *string* (optional) | - | `False` | Specific MediaWiki log action name for log events. |
| `log_action_comment` | *string* (optional) | - | `False` | Additional comment field emitted for some MediaWiki log actions. |
| `log_id` | *string* (optional) | - | `False` | MediaWiki log identifier associated with the event when the change is a log entry, stringified for stable cross-language handling. |
| `log_params_json` | *string* (optional) | - | `False` | Serialized form of the upstream log_params field, which may be an object, array, or string in the raw Wikimedia payload. |

---
##### Object: RecentChange.meta
*Wikimedia EventStreams envelope metadata describing the event identity, domain, stream, and Kafka-origin details.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `uri` | *string* | - | `False` | URI of the Wikimedia entity or page the event pertains to, when provided by the upstream stream. |
| `request_id` | *string* | - | `False` | Unique request identifier assigned by Wikimedia for the request that caused the event. |
| `id` | *string* | - | `True` | Globally unique Wikimedia event UUID for this recentchange record. |
| `domain` | *string* | - | `True` | Wikimedia domain the event pertains to, such as www.wikipedia.org or www.wikidata.org. |
| `stream` | *string* | - | `True` | Name of the upstream EventStreams stream that emitted the event, typically mediawiki.recentchange. |
| `topic` | *string* | - | `False` | Underlying Wikimedia Kafka topic that carried the event before it was exposed through EventStreams. |
| `partition` | *integer* | - | `False` | Underlying Kafka partition number from Wikimedia's internal stream metadata. |
| `offset` | *string* (optional) | - | `False` | Underlying Kafka offset from Wikimedia's internal stream metadata, stringified to avoid range loss across generated languages and validators. |
| `dt` | *string* | - | `True` | UTC event timestamp in ISO-8601 format from the upstream metadata block. |

---
##### Object: RecentChange.length
*Page lengths before and after the change, measured in bytes or characters as provided by MediaWiki.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `old` | *integer* (optional) | - | `False` | Length of the page before the change. |
| `new` | *integer* (optional) | - | `False` | Length of the page after the change. |

---
##### Object: RecentChange.revision
*Old and new MediaWiki revision identifiers associated with the change.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `old` | *string* (optional) | - | `False` | Previous revision identifier before the change, stringified because recent Wikimedia revision identifiers can exceed signed 32-bit integer range. |
| `new` | *string* (optional) | - | `False` | New revision identifier after the change, stringified because recent Wikimedia revision identifiers can exceed signed 32-bit integer range. |
## Message Group: Wikimedia.EventStreams.mqtt
---
### Message: Wikimedia.EventStreams.RecentChange.mqtt
*Public recentchange events from Wikimedia EventStreams. Each event describes one edit, page creation, log action, categorization change, or related MediaWiki recentchanges entry from across Wikimedia projects.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Wikimedia.EventStreams.RecentChange` |
| `source` |  | `` | `False` | `https://stream.wikimedia.org/v2/stream/recentchange` |
| `subject` |  | `uritemplate` | `True` | `{wiki}/{namespace_bucket}/{event_id}` |
| `time` |  | `uritemplate` | `False` | `{event_time}` |

#### Schema:
##### Object: RecentChange
*Normalized representation of Wikimedia's mediawiki/recentchange event schema. This contract preserves the documented recentchange payload while renaming the upstream $schema field to schema_uri and serializing the variant log_params field into log_params_json for stable generated types.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `event_id` | *string* | - | `True` | Top-level copy of meta.id so downstream validators and consumers can resolve the CloudEvents subject and Kafka key from the event payload itself. |
| `event_time` | *string* | - | `True` | Top-level copy of meta.dt in ISO-8601 UTC format so downstream validators and consumers can resolve the CloudEvents time attribute from the payload itself. |
| `schema_uri` | *string* | - | `True` | URI of the upstream Wikimedia JSON schema from the $schema field on the original event payload. |
| `meta` | [Object RecentChange.meta](#object-recentchangemeta) | - | `True` | Wikimedia EventStreams envelope metadata describing the event identity, domain, stream, and Kafka-origin details. |
| `id` | *string* (optional) | - | `False` | MediaWiki recentchanges row identifier (rcid) for the event, stringified because some Wikimedia wikis already exceed signed 32-bit integer range. |
| `type` | *string* | - | `True` | Recentchange type such as edit, new, log, categorize, or external. |
| `namespace` | *integer* | - | `True` | Numeric MediaWiki namespace identifier for the affected page, or -1 for special log events. |
| `title` | *string* | - | `True` | Affected page title in MediaWiki prefixed text form. |
| `title_url` | *string* (optional) | - | `False` | Canonical page URL for the affected title when present in the upstream payload. |
| `comment` | *string* (optional) | - | `False` | Edit or log comment as supplied by the upstream recentchange record. |
| `timestamp` | *integer* | - | `True` | Unix timestamp derived from the MediaWiki rc_timestamp value. |
| `user` | *string* | - | `True` | User name or IP address associated with the change. |
| `bot` | *boolean* (optional) | - | `False` | Whether the recentchange entry was flagged as a bot edit. |
| `minor` | *boolean* (optional) | - | `False` | Whether the recentchange entry was flagged as a minor change. |
| `patrolled` | *boolean* (optional) | - | `False` | Whether the recentchange entry had been patrolled when the event was emitted. |
| `length` | [Object RecentChange.length](#object-recentchangelength) | - | `False` | Page lengths before and after the change, measured in bytes or characters as provided by MediaWiki. |
| `revision` | [Object RecentChange.revision](#object-recentchangerevision) | - | `False` | Old and new MediaWiki revision identifiers associated with the change. |
| `server_url` | *string* (optional) | - | `False` | Canonical server URL for the wiki that emitted the event. |
| `server_name` | *string* (optional) | - | `False` | Server host name of the wiki that emitted the event. |
| `server_script_path` | *string* (optional) | - | `False` | MediaWiki script path on the emitting wiki. |
| `wiki` | *string* | - | `True` | Internal Wikimedia wiki identifier such as enwiki, commonswiki, or wikidatawiki. |
| `namespace_bucket` | *string* | - | `True` | Kebab-case bucket label for the MediaWiki namespace number (e.g. main for 0, talk for 1, file for 6, category for 14, ns-<n> for unrecognised values). Replicates the MQTT topic axis so subscribers can validate the topic segment against the payload. |
| `parsedcomment` | *string* (optional) | - | `False` | HTML-parsed form of the recentchange comment when Wikimedia provides it. |
| `notify_url` | *string* (optional) | - | `False` | URL that points to a diff view or other relevant page for the change. |
| `log_type` | *string* (optional) | - | `False` | MediaWiki log type for log events, such as move, delete, or patrol. |
| `log_action` | *string* (optional) | - | `False` | Specific MediaWiki log action name for log events. |
| `log_action_comment` | *string* (optional) | - | `False` | Additional comment field emitted for some MediaWiki log actions. |
| `log_id` | *string* (optional) | - | `False` | MediaWiki log identifier associated with the event when the change is a log entry, stringified for stable cross-language handling. |
| `log_params_json` | *string* (optional) | - | `False` | Serialized form of the upstream log_params field, which may be an object, array, or string in the raw Wikimedia payload. |

---
##### Object: RecentChange.meta
*Wikimedia EventStreams envelope metadata describing the event identity, domain, stream, and Kafka-origin details.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `uri` | *string* | - | `False` | URI of the Wikimedia entity or page the event pertains to, when provided by the upstream stream. |
| `request_id` | *string* | - | `False` | Unique request identifier assigned by Wikimedia for the request that caused the event. |
| `id` | *string* | - | `True` | Globally unique Wikimedia event UUID for this recentchange record. |
| `domain` | *string* | - | `True` | Wikimedia domain the event pertains to, such as www.wikipedia.org or www.wikidata.org. |
| `stream` | *string* | - | `True` | Name of the upstream EventStreams stream that emitted the event, typically mediawiki.recentchange. |
| `topic` | *string* | - | `False` | Underlying Wikimedia Kafka topic that carried the event before it was exposed through EventStreams. |
| `partition` | *integer* | - | `False` | Underlying Kafka partition number from Wikimedia's internal stream metadata. |
| `offset` | *string* (optional) | - | `False` | Underlying Kafka offset from Wikimedia's internal stream metadata, stringified to avoid range loss across generated languages and validators. |
| `dt` | *string* | - | `True` | UTC event timestamp in ISO-8601 format from the upstream metadata block. |

---
##### Object: RecentChange.length
*Page lengths before and after the change, measured in bytes or characters as provided by MediaWiki.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `old` | *integer* (optional) | - | `False` | Length of the page before the change. |
| `new` | *integer* (optional) | - | `False` | Length of the page after the change. |

---
##### Object: RecentChange.revision
*Old and new MediaWiki revision identifiers associated with the change.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `old` | *string* (optional) | - | `False` | Previous revision identifier before the change, stringified because recent Wikimedia revision identifiers can exceed signed 32-bit integer range. |
| `new` | *string* (optional) | - | `False` | New revision identifier after the change, stringified because recent Wikimedia revision identifiers can exceed signed 32-bit integer range. |
