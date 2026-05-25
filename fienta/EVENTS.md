# Fienta Public Events Bridge Events

**Fienta Public Events Bridge** polls the [Fienta](https://fienta.com) public events API for ticketed events across Europe and sends them to a Kafka topic as CloudEvents. The tool tracks previously observed `sale_status` values to detect changes and emit targeted telemetry events.

## At a glance

- **Event types:** 2 documented event types.
- **Transports:** KAFKA
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{event_id}` identifies the resource each event is about.
- **Operations:** The bridge keeps dedupe state so repeated upstream records are not intentionally republished as new events.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `fienta`. The record key is `{event_id}`. In plain language, `{event_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['fienta'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.

## Event catalog

### Event

CloudEvents type: `Com.Fienta.Event`

#### What it tells you

Reference data for a Fienta public event as exposed by the public events endpoint. Emitted at bridge startup and refreshed periodically so downstream consumers can correlate sale-status change events with the latest published event metadata from https://fienta.com/api/v1/public/events.

#### Identity

Each event identifies the real-world resource with `{event_id}`. `{event_id}` is unique stable identifier for the event as assigned by Fienta. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `fienta`, key `{event_id}` |

#### Payload

`Event` payloads are JSON object. Required fields: `event_id`, `name`, `start`, `event_status`, `sale_status`, `url`.

- **`event_id`** (string, required): Unique stable identifier for the event as assigned by Fienta. Sourced from the 'id' field in the Fienta API response and used as the CloudEvents subject and Kafka key.
- **`name`** (string, required): Display title of the event as shown on the public event page. Sourced from the 'title' field in the Fienta API response.
- **`start`** (string, required): Local event start datetime string in the format 'YYYY-MM-DD HH:MM:SS'. Sourced from the 'starts_at' field in the Fienta API response.
- **`end`** (string or null, optional): Local event end datetime string in the format 'YYYY-MM-DD HH:MM:SS'. Null when the public event payload has no end time. Sourced from the 'ends_at' field in the Fienta API response.
- **`duration_text`** (string or null, optional): Human-readable duration summary rendered by Fienta for the event schedule, for example 'Tue 1. April 2025 at 09:00 - Thu 31. December 2026 at 17:00'. Sourced from the 'duration_string' field in the Fienta API response.
- **`time_notes`** (string or null, optional): Free-form notes about the event timing published by the organizer. Null when the event listing has no timing note. Sourced from the 'notes_about_time' field in the Fienta API response.
- **`event_status`** (string, required): Lifecycle status of the event listing as published by Fienta, for example 'scheduled'. Sourced from the 'event_status' field in the Fienta API response.
- **`sale_status`** (string, required): Current ticket sale status of the event. Observed values in the public feed include 'onSale', 'soldOut', 'notOnSale', and 'saleEnded'. Sourced from the 'sale_status' field in the Fienta API response.
- **`attendance_mode`** (string or null, optional): Attendance mode reported by Fienta for the event, for example 'offline'. Null when the public event listing omits the field. Sourced from the 'attendance_mode' field in the Fienta API response.
- **`venue_name`** (string or null, optional): Venue or place name shown on the public event listing, for example 'Worldwide' or a named physical venue. Null when not supplied. Sourced from the 'venue' field in the Fienta API response.
- **`venue_id`** (string or null, optional): Venue identifier provided by Fienta for the event location. Null when the listing has no venue identifier. Sourced from the 'venue_id' field in the Fienta API response.
- **`address`** (string or null, optional): Postal street address for the venue as shown on the public event listing. Null when the address is not supplied. Sourced from the 'address' field in the Fienta API response.
- **`postal_code`** (string or null, optional): Postal code for the venue address. Null when the event listing has no postal code. Sourced from the 'address_postal_code' field in the Fienta API response.
- **`description`** (string or null, optional): Event description as published by the organizer. The public payload can contain HTML markup or be empty. Sourced from the 'description' field in the Fienta API response.
- **`url`** (string, required): Public Fienta URL for the event details page. Sourced from the 'url' field in the Fienta API response.
- **`buy_tickets_url`** (string or null, optional): Public URL that Fienta exposes for the ticket purchase flow. Null when the listing does not include a dedicated purchase URL. Sourced from the 'buy_tickets_url' field in the Fienta API response.
- **`image_url`** (string or null, optional): URL of the primary promotional image for the event. Null when no image is provided. Sourced from the 'image_url' field in the Fienta API response.
- **`image_small_url`** (string or null, optional): URL of the smaller promotional image variant for the event. Null when the public event listing does not include a smaller image rendition. Sourced from the 'image_small_url' field in the Fienta API response.
- **`series_id`** (string or null, optional): Series identifier or slug used by Fienta to group related event listings. Null when the event is not associated with a series. Sourced from the 'series_id' field in the Fienta API response.
- **`organizer_name`** (string or null, optional): Display name of the event organizer. Null when the organizer name is absent from the public payload. Sourced from the 'organizer_name' field in the Fienta API response.
- **`organizer_phone`** (string or null, optional): Organizer phone number published on the event listing. Null when the organizer did not expose a phone number. Sourced from the 'organizer_phone' field in the Fienta API response.
- **`organizer_email`** (string or null, optional): Organizer email address published on the event listing. Null when the organizer did not expose an email address. Sourced from the 'organizer_email' field in the Fienta API response.
- **`organizer_id`** (integer or null, optional): Numeric identifier of the organizer account in Fienta. Null when the public event payload omits the organizer identifier. Sourced from the 'organizer_id' field in the Fienta API response.
- **`categories`** (array of string, optional): List of category labels assigned to the event listing, such as 'other' or 'family'. The bridge emits an empty array when the public event payload omits the categories array. Sourced from the 'categories' field in the Fienta API response.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": "string",
  "name": "string",
  "start": "string",
  "end": "string",
  "duration_text": "string",
  "time_notes": "string",
  "event_status": "string",
  "sale_status": "string",
  "attendance_mode": "string",
  "venue_name": "string",
  "venue_id": "string",
  "address": "string",
  "postal_code": "string",
  "description": "string",
  "url": "string",
  "buy_tickets_url": "string",
  "image_url": "string",
  "image_small_url": "string",
  "series_id": "string",
  "organizer_name": "string",
  "organizer_phone": "string",
  "organizer_email": "string",
  "organizer_id": 0,
  "categories": [
    "string"
  ]
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Event Sale Status

CloudEvents type: `Com.Fienta.EventSaleStatus`

#### What it tells you

Telemetry event emitted whenever the bridge observes a change in the sale_status value of a Fienta public event between two polls of the public events endpoint.

#### Identity

Each event identifies the real-world resource with `{event_id}`. `{event_id}` is unique stable identifier for the event as assigned by Fienta. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `fienta`, key `{event_id}` |

#### Payload

`Event Sale Status` payloads are JSON object. Required fields: `event_id`, `name`, `sale_status`, `observed_at`.

- **`event_id`** (string, required): Unique stable identifier for the event as assigned by Fienta. Sourced from the 'id' field in the Fienta API response and used as the CloudEvents subject and Kafka key.
- **`name`** (string, required): Display title of the event at the time the bridge observed the sale status change. Sourced from the 'title' field in the Fienta API response.
- **`sale_status`** (string, required): Current ticket sale status observed for the event, such as 'onSale', 'soldOut', 'notOnSale', or 'saleEnded'. Sourced from the 'sale_status' field in the Fienta API response.
- **`event_status`** (string or null, optional): Lifecycle status of the event listing at the time of observation, for example 'scheduled'. Null when the public payload omits the value. Sourced from the 'event_status' field in the Fienta API response.
- **`start`** (string or null, optional): Local event start datetime string in the format 'YYYY-MM-DD HH:MM:SS'. Null when the public event payload omits the start time. Sourced from the 'starts_at' field in the Fienta API response.
- **`end`** (string or null, optional): Local event end datetime string in the format 'YYYY-MM-DD HH:MM:SS'. Null when the public event payload omits the end time. Sourced from the 'ends_at' field in the Fienta API response.
- **`url`** (string or null, optional): Public Fienta URL for the event details page. Null when the public payload omits the event URL. Sourced from the 'url' field in the Fienta API response.
- **`buy_tickets_url`** (string or null, optional): Public URL that Fienta exposes for the ticket purchase flow at the time of the observation. Null when the listing does not include a dedicated purchase URL. Sourced from the 'buy_tickets_url' field in the Fienta API response.
- **`observed_at`** (string, required): RFC 3339 UTC timestamp generated by the bridge when it observed the sale_status change while polling the Fienta public events API.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": "string",
  "name": "string",
  "sale_status": "string",
  "event_status": "string",
  "start": "string",
  "end": "string",
  "url": "string",
  "buy_tickets_url": "string",
  "observed_at": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

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
- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/fienta.xreg.json`](xreg/fienta.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Fienta Terms of Service: <https://fienta.com/terms>
