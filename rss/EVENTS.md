# RSS Bridge Usage Guide Events

MQTT/5.0 transport variant for RSS/Atom feed items. Non-retained QoS-1 item events are routed by feed_slug and topic-safe item token; source category remains in the payload and is intentionally not a topic axis.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{item_id}` identifies the resource each event is about.
- **Operations:** The bridge documentation mentions ETag-aware polling, so consumers should expect unchanged upstream responses to be skipped.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `rss-feeds`. The record key is `{item_id}`. In plain language, `{item_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['rss-feeds'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `news/intl/rss/rss/+/+`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('news/intl/rss/rss/+/+', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `rss`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/rss')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Feed Item

CloudEvents type: `Microsoft.OpenData.RssFeeds.FeedItem`

#### What it tells you

A new item has been added to the RSS feed. Represents an item in an RSS feed, containing metadata such as the author, title, and content.

#### Identity

Each event identifies the real-world resource with `{item_id}`. `{item_id}` is a payload field with the same name. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `rss-feeds`, key `{item_id}` |
| `MQTT/5.0` | topic `news/intl/rss/rss/{feed_slug}/{item}`, retain `false`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/rss`, message subject `{item_id}` |

#### Payload

`Feed Item` payloads are JSON object. Required fields: `feed_slug`, `item`.

- **`feed_slug`** (string, required): Topic-safe stable slug derived from the configured feed URL. Constraints: minLength `1`, pattern `^[A-Za-z0-9._-]+$`.
- **`item`** (string, required): Topic-safe stable item token derived from the feed entry id/link/title and used for MQTT routing. Constraints: minLength `1`, pattern `^[A-Za-z0-9._-]+$`.
- **`author`** (object, optional): Information about the feed item's author. See [FeedItemAuthor](#payload-microsoft-opendata-rssfeeds-feeditem-feeditemauthor).
- **`publisher`** (object, optional): Information about the feed item's publisher. See [FeedItemPublisher](#payload-microsoft-opendata-rssfeeds-feeditem-feeditempublisher).
- **`summary`** (object, optional): A short summary of the feed item. See [FeedItemSummary](#payload-microsoft-opendata-rssfeeds-feeditem-feeditemsummary).
- **`title`** (object, optional): The feed item's title. See [FeedItemTitle](#payload-microsoft-opendata-rssfeeds-feeditem-feeditemtitle).
- **`source`** (object, optional): Information about the source feed of the item. See [FeedItemSource](#payload-microsoft-opendata-rssfeeds-feeditem-feeditemsource).
- **`content`** (array of object, optional): The content of the feed item, potentially including multiple formats.
- **`enclosures`** (array of object, optional): Media attachments associated with the feed item.
- **`published`** (int64, optional): The publication date and time of the feed item.
- **`updated`** (int64, optional): The last updated date and time of the feed item.
- **`created`** (int64, optional): The creation date and time of the feed item.
- **`expired`** (int64, optional): The expiration date and time of the feed item.
- **`id`** (string, optional): A unique identifier for the feed item.
- **`license`** (string, optional): License information for the feed item.
- **`comments`** (string, optional): A link to comments or feedback related to the feed item.
- **`contributors`** (array of object, optional): A list of individuals who contributed to the feed item.
- **`links`** (array of object, optional): A collection of links related to the feed item.
##### FeedItemAuthor
<a id="payload-microsoft-opendata-rssfeeds-feeditem-feeditemauthor"></a>

Contains information about the author of the feed item.

- **`name`** (string, optional): The full name of the author.
- **`href`** (string, optional): A URL associated with the author, such as a personal website or profile.
- **`email`** (string, optional): The author's email address.
##### FeedItemPublisher
<a id="payload-microsoft-opendata-rssfeeds-feeditem-feeditempublisher"></a>

Contains information about the publisher of the feed item.

- **`name`** (string, optional): The name of the publisher.
- **`href`** (string, optional): A URL associated with the publisher.
- **`email`** (string, optional): The publisher's email address.
##### FeedItemSummary
<a id="payload-microsoft-opendata-rssfeeds-feeditem-feeditemsummary"></a>

A brief summary or abstract of the feed item.

- **`value`** (string, optional): The text content of the summary.
- **`type`** (string, optional): The content type of the summary, such as 'text/plain' or 'text/html'.
- **`language`** (string, optional): The language of the summary content.
- **`base`** (string, optional): The base URI for resolving relative URIs within the summary.
##### FeedItemTitle
<a id="payload-microsoft-opendata-rssfeeds-feeditem-feeditemtitle"></a>

The title of the feed item.

- **`value`** (string, optional): The text content of the title.
- **`type`** (string, optional): The content type of the title.
- **`language`** (string, optional): The language of the title.
- **`base`** (string, optional): The base URI for resolving relative URIs within the title.
##### FeedItemSource
<a id="payload-microsoft-opendata-rssfeeds-feeditem-feeditemsource"></a>

Metadata about the original source feed, useful if the item was republished from another feed.

- **`author`** (string, optional): The name of the original author.
- **`author_detail`** (object, optional): Detailed information about the original author. See [FeedItemAuthor](#payload-microsoft-opendata-rssfeeds-feeditem-feeditemsource-feeditemauthor).
- **`contributors`** (array of object, optional): A list of contributors to the source feed.
- **`icon`** (string, optional): An icon image associated with the source feed.
- **`id`** (string, optional): A unique identifier for the source feed.
- **`link`** (string, optional): A link to the source feed.
- **`links`** (array of object, optional): A collection of links related to the source feed.
- **`logo`** (string, optional): A logo image associated with the source feed.
- **`rights`** (string, optional): Rights information for the source feed, such as copyright notices.
- **`subtitle`** (string, optional): A secondary title or tagline for the source feed.
- **`title`** (string, optional): The title of the source feed.
- **`updated`** (int64, optional): The last updated timestamp of the source feed.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "feed_slug": "string",
  "item": "string",
  "author": {
    "name": "string",
    "href": "string",
    "email": "string"
  },
  "publisher": {
    "name": "string",
    "href": "string",
    "email": "string"
  },
  "summary": {
    "value": "string",
    "type": "string",
    "language": "string",
    "base": "string"
  },
  "title": {
    "value": "string",
    "type": "string",
    "language": "string",
    "base": "string"
  },
  "source": {
    "author": "string",
    "author_detail": {},
    "contributors": [
      {}
    ],
    "icon": "string",
    "id": "string",
    "link": "string",
    "links": [
      {
        "rel": "string",
        "href": "string",
        "type": "string",
        "title": "string"
      }
    ],
    "logo": "string",
    "rights": "string",
    "subtitle": "string",
    "title": "string",
    "updated": 0
  },
  "content": [
    {
      "value": "string",
      "type": "string",
      "language": "string",
      "base": "string"
    }
  ],
  "enclosures": [
    {
      "href": "string",
      "length": 0,
      "type": "string"
    }
  ],
  "published": 0,
  "updated": 0,
  "created": 0,
  "expired": 0,
  "id": "string",
  "license": "string",
  "comments": "string",
  "contributors": [
    {}
  ],
  "links": [
    {}
  ]
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

- The bridge documentation mentions ETag-aware polling, so consumers should expect unchanged upstream responses to be skipped.
- The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- The MQTT variant publishes with QoS 1 and retained-message Last-Known-Value semantics where declared in the event catalog.

## References

- xRegistry manifest: [`xreg/feeds.xreg.json`](xreg/feeds.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
