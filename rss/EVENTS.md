# RSS Bridge Usage Guide Events

MQTT/5.0 transport variant for RSS/Atom feed items. Non-retained QoS-1 item events are routed by feed_slug and topic-safe item token; source category remains in the payload and is intentionally not a topic axis.

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

### Endpoint `Microsoft.OpenData.RssFeeds.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Microsoft.OpenData.RssFeeds`](#messagegroup-microsoftopendatarssfeeds) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `rss-feeds` |
| Kafka key | `{item_id}` |
| Deployed | False |

### Endpoint `Microsoft.OpenData.RssFeeds.Mqtt`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `MQTT/5.0` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"mode": "binary"}` |
| Messagegroups | [`Microsoft.OpenData.RssFeeds.mqtt`](#messagegroup-microsoftopendatarssfeedsmqtt) |

#### Transport options

| Option | Value |
| --- | --- |
| Deployed | False |
| Broker endpoints | `[{"uri": "mqtt://localhost:1883"}]` |

## Messagegroups

### Messagegroup `Microsoft.OpenData.RssFeeds`
<a id="messagegroup-microsoftopendatarssfeeds"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Microsoft.OpenData.RssFeeds.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Microsoft.OpenData.RssFeeds.FeedItem`
<a id="message-microsoftopendatarssfeedsfeeditem"></a>

A new item has been added to the RSS feed.

| Field | Value |
| --- | --- |
| Name | FeedItem |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.RssFeeds.jstruct/schemas/Microsoft.OpenData.RssFeeds.FeedItem`](#schema-microsoftopendatarssfeedsfeeditem) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.RssFeeds.FeedItem` |
| `source` |  | `uritemplate` | `False` | `{sourceurl}` |
| `subject` |  | `uritemplate` | `False` | `{item_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.RssFeeds.Kafka` | `KAFKA` | topic `rss-feeds`; key `{item_id}` |

### Messagegroup `Microsoft.OpenData.RssFeeds.mqtt`
<a id="messagegroup-microsoftopendatarssfeedsmqtt"></a>

| Field | Value |
| --- | --- |
| Description | MQTT/5.0 transport variant for RSS/Atom feed items. Non-retained QoS-1 item events are routed by feed_slug and topic-safe item token; source category remains in the payload and is intentionally not a topic axis. |
| Transport bindings | `Microsoft.OpenData.RssFeeds.Mqtt` (MQTT/5.0) |
| Messages | 1 |

#### Message `Microsoft.OpenData.RssFeeds.mqtt.FeedItem`
<a id="message-microsoftopendatarssfeedsmqttfeeditem"></a>

A new item has been added to the RSS feed.

| Field | Value |
| --- | --- |
| Name | FeedItem |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Microsoft.OpenData.RssFeeds.jstruct/schemas/Microsoft.OpenData.RssFeeds.FeedItem`](#schema-microsoftopendatarssfeedsfeeditem) |
| Base message chain | `/messagegroups/Microsoft.OpenData.RssFeeds/messages/Microsoft.OpenData.RssFeeds.FeedItem` |
| Transport override | `MQTT/5.0` |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Microsoft.OpenData.RssFeeds.FeedItem` |
| `source` |  | `uritemplate` | `False` | `{sourceurl}` |
| `subject` |  | `uritemplate` | `False` | `{item_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Microsoft.OpenData.RssFeeds.Mqtt` | `MQTT/5.0` | topic `news/intl/rss/rss/{feed_slug}/{item}` |

##### Transport options

| Option | Value |
| --- | --- |
| MQTT topic | `news/intl/rss/rss/{feed_slug}/{item}` |
| QoS | 1 |
| Retain | False |

## Schemagroups

### Schemagroup `Microsoft.OpenData.RssFeeds.jstruct`
<a id="schemagroup-microsoftopendatarssfeedsjstruct"></a>

#### Schema `Microsoft.OpenData.RssFeeds.FeedItem`
<a id="schema-microsoftopendatarssfeedsfeeditem"></a>

| Field | Value |
| --- | --- |
| Name | FeedItem |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Microsoft/OpenData/RssFeeds/FeedItem` |
| $schema | `https://json-structure.org/meta/core/v0/#` |
| $root | `#/definitions/Microsoft/OpenData/RssFeeds/FeedItem` |
| Type | `object` |

###### Object `FeedItem`
<a id="schema-node-feeditem"></a>

Represents an item in an RSS feed, containing metadata such as the author, title, and content.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `feed_slug` | `string` | `True` | Topic-safe stable slug derived from the configured feed URL. | - | minLength=`1`<br>pattern=`^[A-Za-z0-9._-]+$` | - |
| `item` | `string` | `True` | Topic-safe stable item token derived from the feed entry id/link/title and used for MQTT routing. | - | minLength=`1`<br>pattern=`^[A-Za-z0-9._-]+$` | - |
| `author` | `schema` | `False` | Information about the feed item's author. | - | default=`-` | default=`-` |
| `publisher` | `schema` | `False` | Information about the feed item's publisher. | - | default=`-` | default=`-` |
| `summary` | `schema` | `False` | A short summary of the feed item. | - | default=`-` | default=`-` |
| `title` | `schema` | `False` | The feed item's title. | - | default=`-` | default=`-` |
| `source` | `schema` | `False` | Information about the source feed of the item. | - | default=`-` | default=`-` |
| `content` | array of [`FeedItemContent`](#schema-node-feeditemcontent) | `False` | The content of the feed item, potentially including multiple formats. | - | default=`-` | default=`-` |
| `enclosures` | array of [`FeedItemEnclosure`](#schema-node-feeditemenclosure) | `False` | Media attachments associated with the feed item. | - | default=`-` | default=`-` |
| `published` | `int64` | `False` | The publication date and time of the feed item. | - | default=`-` | default=`-` |
| `updated` | `int64` | `False` | The last updated date and time of the feed item. | - | default=`-` | default=`-` |
| `created` | `int64` | `False` | The creation date and time of the feed item. | - | default=`-` | default=`-` |
| `expired` | `int64` | `False` | The expiration date and time of the feed item. | - | default=`-` | default=`-` |
| `id` | `string` | `False` | A unique identifier for the feed item. | - | default=`-` | default=`-` |
| `license` | `string` | `False` | License information for the feed item. | - | default=`-` | default=`-` |
| `comments` | `string` | `False` | A link to comments or feedback related to the feed item. | - | default=`-` | default=`-` |
| `contributors` | array of [`FeedItemAuthor`](#schema-node-feeditemauthor) | `False` | A list of individuals who contributed to the feed item. | - | default=`-` | default=`-` |
| `links` | array of [`Link`](#schema-node-link) | `False` | A collection of links related to the feed item. | - | default=`-` | default=`-` |

###### Object `FeedItemContent`
<a id="schema-node-feeditemcontent"></a>

Represents the main content of the feed item.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `value` | `string` | `False` | The actual content of the feed item. | - | default=`-` | default=`-` |
| `type` | `string` | `False` | The content type, such as 'text/html' or 'text/plain'. | - | default=`-` | default=`-` |
| `language` | `string` | `False` | The language of the content. | - | default=`-` | default=`-` |
| `base` | `string` | `False` | The base URI for resolving relative URIs within the content. | - | default=`-` | default=`-` |

###### Object `FeedItemEnclosure`
<a id="schema-node-feeditemenclosure"></a>

Represents media content attached to the feed item, such as audio or video files.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `href` | `string` | `False` | The URL of the enclosure. | - | default=`-` | default=`-` |
| `length` | `int64` | `False` | The size of the enclosure in bytes. | - | default=`-` | default=`-` |
| `type` | `string` | `False` | The MIME type of the enclosure content. | - | default=`-` | default=`-` |

###### Object `FeedItemAuthor`
<a id="schema-node-feeditemauthor"></a>

Contains information about the author of the feed item.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `name` | `string` | `False` | The full name of the author. | - | default=`-` | default=`-` |
| `href` | `string` | `False` | A URL associated with the author, such as a personal website or profile. | - | default=`-` | default=`-` |
| `email` | `string` | `False` | The author's email address. | - | default=`-` | default=`-` |

###### Object `Link`
<a id="schema-node-link"></a>

Represents a hyperlink associated with the feed or feed item.

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `rel` | `string` | `False` | The relationship type of the link, such as 'alternate' or 'self'. | - | default=`-` | default=`-` |
| `href` | `string` | `False` | The URL of the link. | - | default=`-` | default=`-` |
| `type` | `string` | `False` | The MIME type of the linked resource. | - | default=`-` | default=`-` |
| `title` | `string` | `False` | The title or description of the link. | - | default=`-` | default=`-` |

### Schemagroup `Microsoft.OpenData.RssFeeds.avro`
<a id="schemagroup-microsoftopendatarssfeedsavro"></a>

#### Schema `Microsoft.OpenData.RssFeeds.FeedItem`
<a id="schema-microsoftopendatarssfeedsfeeditem"></a>

| Field | Value |
| --- | --- |
| Name | FeedItem |
| Format | Avro/1.11.3 |
| Default version | 1 |
| Description | Schema for the FeedItem event in the RssFeeds message group. |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | Avro/1.11.3 |

###### Avro

| Field | Value |
| --- | --- |
| Name | FeedItem |
| Namespace | Microsoft.OpenData.RssFeeds |
| Type | `record` |
| Doc | Represents an item in an RSS feed, containing metadata such as the author, title, and content. |

| Field | Type | Description | Default |
| --- | --- | --- | --- |
| `feed_slug` | `string` | Topic-safe stable slug derived from the configured feed URL. | `-` |
| `item` | `string` | Topic-safe stable item token derived from the feed entry id/link/title and used for MQTT routing. | `-` |
| `author` | `null` \| record `FeedItemAuthor` | Information about the feed item's author. | `-` |
| `publisher` | `null` \| record `FeedItemPublisher` | Information about the feed item's publisher. | `-` |
| `summary` | `null` \| record `FeedItemSummary` | A short summary of the feed item. | `-` |
| `title` | `null` \| record `FeedItemTitle` | The feed item's title. | `-` |
| `source` | `null` \| record `FeedItemSource` | Information about the source feed of the item. | `-` |
| `content` | `null` \| array of record `FeedItemContent` | The content of the feed item, potentially including multiple formats. | `-` |
| `enclosures` | `null` \| array of record `FeedItemEnclosure` | Media attachments associated with the feed item. | `-` |
| `published` | `null` \| `long` | The publication date and time of the feed item. | `-` |
| `updated` | `null` \| `long` | The last updated date and time of the feed item. | `-` |
| `created` | `null` \| `long` | The creation date and time of the feed item. | `-` |
| `expired` | `null` \| `long` | The expiration date and time of the feed item. | `-` |
| `id` | `null` \| `string` | A unique identifier for the feed item. | `-` |
| `license` | `null` \| `string` | License information for the feed item. | `-` |
| `comments` | `null` \| `string` | A link to comments or feedback related to the feed item. | `-` |
| `contributors` | `null` \| array of `Microsoft.OpenData.RssFeeds.FeedItemAuthor` | A list of individuals who contributed to the feed item. | `-` |
| `links` | `null` \| array of `Microsoft.OpenData.RssFeeds.Link` | A collection of links related to the feed item. | `-` |
