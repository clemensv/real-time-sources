# RSS API Bridge Events

This document describes the events that are emitted by the RSS API Bridge.

- [Microsoft.OpenData.RssFeeds](#message-group-microsoftopendatarssfeeds)
  - [Microsoft.OpenData.RssFeeds.FeedItem](#message-microsoftopendatarssfeedsfeeditem)

---

## Message Group: Microsoft.OpenData.RssFeeds

### Message: Microsoft.OpenData.RssFeeds.FeedItem

#### EventProperties:

| **Property**    | **Value**                        |
|-----------------|----------------------------------|
| **ID**          | `Microsoft.OpenData.RssFeeds.FeedItem`                |
| **Format**      | `CloudEvents/1.0`            |
| **Binding**     | `None`           |
| **Schema Format** | `Avro/1.11.3`    |
| **Created At**  | `None`         |
| **Modified At** | `None`        |

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` |  | `` | `False` | `Microsoft.OpenData.RssFeeds.FeedItem` |
| `source` |  | `uritemplate` | `False` | `{sourceurl}` |
| `subject` |  | `uritemplate` | `False` | `{item_id}` |

#### Schema:

##### Record: FeedItem

*Represents an item in an RSS feed, containing metadata such as the author, title, and content.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `author` | [Record FeedItemAuthor](#record-feeditemauthor) (optional) | Information about the feed item's author. |
| `publisher` | [Record FeedItemPublisher](#record-feeditempublisher) (optional) | Information about the feed item's publisher. |
| `summary` | [Record FeedItemSummary](#record-feeditemsummary) (optional) | A short summary of the feed item. |
| `title` | [Record FeedItemTitle](#record-feeditemtitle) (optional) | The feed item's title. |
| `source` | [Record FeedItemSource](#record-feeditemsource) (optional) | Information about the source feed of the item. |
| `content` | *array* (optional) | The content of the feed item, potentially including multiple formats. |
| `enclosures` | *array* (optional) | Media attachments associated with the feed item. |
| `published` | *long* (optional) | The publication date and time of the feed item. |
| `updated` | *long* (optional) | The last updated date and time of the feed item. |
| `created` | *long* (optional) | The creation date and time of the feed item. |
| `expired` | *long* (optional) | The expiration date and time of the feed item. |
| `id` | *string* (optional) | A unique identifier for the feed item. |
| `license` | *string* (optional) | License information for the feed item. |
| `comments` | *string* (optional) | A link to comments or feedback related to the feed item. |
| `contributors` | *array* (optional) | A list of individuals who contributed to the feed item. |
| `links` | *array* (optional) | A collection of links related to the feed item. |

---

##### Record: FeedItemAuthor

*Contains information about the author of the feed item.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `name` | *string* (optional) | The full name of the author. |
| `href` | *string* (optional) | A URL associated with the author, such as a personal website or profile. |
| `email` | *string* (optional) | The author's email address. |

---

##### Record: FeedItemPublisher

*Contains information about the publisher of the feed item.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `name` | *string* (optional) | The name of the publisher. |
| `href` | *string* (optional) | A URL associated with the publisher. |
| `email` | *string* (optional) | The publisher's email address. |

---

##### Record: FeedItemSummary

*A brief summary or abstract of the feed item.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `value` | *string* (optional) | The text content of the summary. |
| `type` | *string* (optional) | The content type of the summary, such as 'text/plain' or 'text/html'. |
| `language` | *string* (optional) | The language of the summary content. |
| `base` | *string* (optional) | The base URI for resolving relative URIs within the summary. |

---

##### Record: FeedItemTitle

*The title of the feed item.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `value` | *string* (optional) | The text content of the title. |
| `type` | *string* (optional) | The content type of the title. |
| `language` | *string* (optional) | The language of the title. |
| `base` | *string* (optional) | The base URI for resolving relative URIs within the title. |

---

##### Record: FeedItemSource

*Metadata about the original source feed, useful if the item was republished from another feed.*

| **Field Name** | **Type** | **Description** |
|----------------|----------|-----------------|
| `author` | *string* (optional) | The name of the original author. |
| `author_detail` | *Microsoft.OpenData.RssFeeds.FeedItemAuthor* (optional) | Detailed information about the original author. |
| `contributors` | *array* (optional) | A list of contributors to the source feed. |
| `icon` | *string* (optional) | An icon image associated with the source feed. |
| `id` | *string* (optional) | A unique identifier for the source feed. |
| `link` | *string* (optional) | A link to the source feed. |
| `links` | *array* (optional) | A collection of links related to the source feed. |
| `logo` | *string* (optional) | A logo image associated with the source feed. |
| `rights` | *string* (optional) | Rights information for the source feed, such as copyright notices. |
| `subtitle` | *string* (optional) | A secondary title or tagline for the source feed. |
| `title` | *string* (optional) | The title of the source feed. |
| `updated` | *long* (optional) | The last updated timestamp of the source feed. |
