# RSS API Bridge Events

This document describes the events that are emitted by the RSS API Bridge.

- [Microsoft.OpenData.RssFeeds](#message-group-microsoftopendatarssfeeds)
  - [Microsoft.OpenData.RssFeeds.FeedItem](#message-microsoftopendatarssfeedsfeeditem)

---

## Message Group: Microsoft.OpenData.RssFeeds

### Message: Microsoft.OpenData.RssFeeds.FeedItem

**ID**: Microsoft.OpenData.RssFeeds.FeedItem
**Format**: CloudEvents/1.0
**Binding**: None
**Schema Format**: Avro/1.11.3
**Created At**: None
**Modified At**: None

#### Metadata:

- **type**: None
  - Type: *None*
  - Required: *False*
  - Value: `Microsoft.OpenData.RssFeeds.FeedItem`

- **source**: None
  - Type: *uritemplate*
  - Required: *False*
  - Value: `{sourceurl}`

- **subject**: None
  - Type: *uritemplate*
  - Required: *False*
  - Value: `{item_id}`

#### Schema:

##### Record: FeedItem

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `author` | [Record FeedItemAuthor](#record-feeditemauthor) (optional) |  |
| `publisher` | [Record FeedItemPublisher](#record-feeditempublisher) (optional) |  |
| `summary` | [Record FeedItemSummary](#record-feeditemsummary) (optional) |  |
| `title` | [Record FeedItemTitle](#record-feeditemtitle) (optional) |  |
| `source` | [Record FeedItemSource](#record-feeditemsource) (optional) |  |
| `content` | *array* (optional) |  |
| `enclosures` | *array* (optional) |  |
| `published` | *long* (optional) |  |
| `updated` | *long* (optional) |  |
| `created` | *long* (optional) |  |
| `expired` | *long* (optional) |  |
| `id` | *string* (optional) |  |
| `license` | *string* (optional) |  |
| `comments` | *string* (optional) |  |
| `contributors` | *array* (optional) |  |
| `links` | *array* (optional) |  |

---

##### Record: FeedItemAuthor

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `name` | *string* (optional) |  |
| `href` | *string* (optional) |  |
| `email` | *string* (optional) |  |

---

##### Record: FeedItemPublisher

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `name` | *string* (optional) |  |
| `href` | *string* (optional) |  |
| `email` | *string* (optional) |  |

---

##### Record: FeedItemSummary

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `value` | *string* (optional) |  |
| `type` | *string* (optional) |  |
| `language` | *string* (optional) |  |
| `base` | *string* (optional) |  |

---

##### Record: FeedItemTitle

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `value` | *string* (optional) |  |
| `type` | *string* (optional) |  |
| `language` | *string* (optional) |  |
| `base` | *string* (optional) |  |

---

##### Record: FeedItemSource

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `author` | *string* (optional) |  |
| `author_detail` | *Microsoft.OpenData.RssFeeds.FeedItemAuthor* (optional) |  |
| `contributors` | *array* (optional) |  |
| `icon` | *string* (optional) |  |
| `id` | *string* (optional) |  |
| `link` | *string* (optional) |  |
| `links` | *array* (optional) |  |
| `logo` | *string* (optional) |  |
| `rights` | *string* (optional) |  |
| `subtitle` | *string* (optional) |  |
| `title` | *string* (optional) |  |
| `updated` | *long* (optional) |  |
