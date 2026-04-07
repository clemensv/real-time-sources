# Wikimedia EventStreams RecentChange Events

This document describes the event emitted by the Wikimedia EventStreams
recentchange bridge.

- [Wikimedia.EventStreams](#message-group-wikimediaeventstreams)
  - [Wikimedia.EventStreams.RecentChange](#message-wikimediaeventstreamsrecentchange)

---

## Message Group: Wikimedia.EventStreams

---

### Message: Wikimedia.EventStreams.RecentChange

Public Wikimedia recentchange event data from
`https://stream.wikimedia.org/v2/stream/recentchange`.

#### CloudEvents Attributes

| **Name** | **Value** |
|----------|-----------|
| `type` | `Wikimedia.EventStreams.RecentChange` |
| `source` | `https://stream.wikimedia.org/v2/stream/recentchange` |
| `subject` | `{event_id}` |
| `time` | `{event_time}` |

#### Selected Fields

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `event_id` | string | Top-level copy of `meta.id`, used for Kafka key and CloudEvents subject |
| `event_time` | string | Top-level copy of `meta.dt`, used for CloudEvents time |
| `schema_uri` | string | Upstream Wikimedia schema URI from `$schema` |
| `meta.id` | string | Globally unique Wikimedia event UUID |
| `meta.dt` | string | Event timestamp in ISO-8601 UTC |
| `meta.domain` | string | Wikimedia domain the event pertains to |
| `meta.stream` | string | Upstream stream name, typically `mediawiki.recentchange` |
| `id` | string? | Wikimedia recentchange row identifier (`rcid`), stringified for range safety |
| `type` | string | Recentchange type such as `edit`, `new`, `log`, or `categorize` |
| `namespace` | integer | MediaWiki namespace ID |
| `title` | string | Page title in prefixed MediaWiki form |
| `title_url` | string? | Canonical page URL |
| `comment` | string? | Edit or log comment |
| `timestamp` | integer | Unix timestamp derived from `rc_timestamp` |
| `user` | string | Editing user name or anonymous IP |
| `bot` | boolean? | Whether the change was marked as a bot edit |
| `minor` | boolean? | Whether the change was marked minor |
| `patrolled` | boolean? | Whether the change was patrolled |
| `length.old` | integer? | Page length before the change |
| `length.new` | integer? | Page length after the change |
| `revision.old` | string? | Previous revision ID, stringified |
| `revision.new` | string? | New revision ID, stringified |
| `wiki` | string | Internal Wikimedia wiki identifier such as `enwiki` or `wikidatawiki` |
| `parsedcomment` | string? | Parsed HTML rendering of the comment |
| `notify_url` | string? | URL to a diff or log view for the change |
| `log_type` | string? | Log type for log events |
| `log_action` | string? | Log action for log events |
| `log_id` | string? | Log row identifier, stringified |
| `log_params_json` | string? | Serialized upstream `log_params` value |

#### Example

```json
{
  "specversion": "1.0",
  "type": "Wikimedia.EventStreams.RecentChange",
  "source": "https://stream.wikimedia.org/v2/stream/recentchange",
  "subject": "ded39d54-8ad6-43bd-baf5-8b06c2607a56",
  "time": "2026-04-07T10:57:48.160Z",
  "data": {
    "event_id": "ded39d54-8ad6-43bd-baf5-8b06c2607a56",
    "event_time": "2026-04-07T10:57:48.160Z",
    "schema_uri": "/mediawiki/recentchange/1.0.0",
    "meta": {
      "uri": "https://www.wikidata.org/wiki/Lexeme:L236207",
      "request_id": "12c47e2c-f5b8-4b72-9747-34ef82dcc475",
      "id": "ded39d54-8ad6-43bd-baf5-8b06c2607a56",
      "domain": "www.wikidata.org",
      "stream": "mediawiki.recentchange",
      "topic": "eqiad.mediawiki.recentchange",
      "partition": 0,
      "offset": 6002030074,
      "dt": "2026-04-07T10:57:48.160Z"
    },
    "id": 2555986212,
    "type": "edit",
    "namespace": 146,
    "title": "Lexeme:L236207",
    "title_url": "https://www.wikidata.org/wiki/Lexeme:L236207",
    "comment": "/* wbsetqualifier-add:1| */ [[Property:P304]]: 238, [[:toollabs:quickstatements/#/batch/256383|batch #256383]]",
    "timestamp": 1775559467,
    "user": "Vesihiisi",
    "bot": false,
    "minor": false,
    "patrolled": true,
    "length": {
      "old": 4191,
      "new": 4467
    },
    "revision": {
      "old": 2479093568,
      "new": 2479093572
    },
    "server_url": "https://www.wikidata.org",
    "server_name": "www.wikidata.org",
    "server_script_path": "/w",
    "wiki": "wikidatawiki"
  }
}
```
