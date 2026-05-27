# Ticketmaster Discovery API feeder Events

MQTT 5.0 binary-mode CloudEvents variant of Ticketmaster.Events.

## At a glance

- **Event types:** 5 documented event types (15 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 5 telemetry event types.
- **Identity:** `{event_id}`, `{entity_id}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `ticketmaster`. The record key is `{event_id}`, `{entity_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['ticketmaster'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `civic-events/intl/ticketmaster/ticketmaster/+/+/+/+/event`, `civic-events/intl/ticketmaster/ticketmaster/+/+/+/venue`, `civic-events/intl/ticketmaster/ticketmaster/+/+/+/+/attraction`, `civic-events/intl/ticketmaster/ticketmaster/+/+/+/+/classification`, `civic-events/intl/ticketmaster/ticketmaster/+/+/+/+/info`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('civic-events/intl/ticketmaster/ticketmaster/+/+/+/+/event', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `ticketmaster`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/ticketmaster')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Event

CloudEvents type: `Ticketmaster.Events.Event`

#### What it tells you

A Ticketmaster event representing a concert, sports match, theater performance, or other live public event. Emitted when a new event is discovered or when an existing event's status or schedule changes. Sourced from the Discovery API v2 /events endpoint.

#### Identity

Each event identifies the real-world resource with `{event_id}`. `{event_id}` is stable Ticketmaster event identifier. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ticketmaster`, key `{event_id}` |
| `MQTT/5.0` | topic `civic-events/intl/ticketmaster/ticketmaster/{country}/{city}/{venue_id}/{event_id}/event`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/ticketmaster`, message subject `{event_id}` |

#### Payload

`Event` payloads are JSON object. Required fields: `event_id`, `name`.

- **`event_id`** (string, required): Stable Ticketmaster event identifier. Globally unique across all event types (e.g. 'G5v0Z9iQkPl_2'). Used as the Kafka message key.
- **`name`** (string, required): Human-readable event name as provided by Ticketmaster (e.g. 'Taylor Swift | The Eras Tour').
- **`type`** (string or null, optional): Ticketmaster resource type discriminator. Usually 'event'.
- **`url`** (string or null, optional): URL to the event page on Ticketmaster.com where tickets can be purchased.
- **`locale`** (string or null, optional): BCP-47 locale string for the event page (e.g. 'en-us', 'en-gb', 'de-de').
- **`start_date`** (string or null, optional): Local calendar date on which the event starts, in ISO 8601 YYYY-MM-DD format. May be absent for events without a confirmed date (time-to-be-announced).
- **`start_time`** (string or null, optional): Local clock time at which the event starts, in HH:MM:SS format. May be absent when the time is to be announced.
- **`start_datetime_local`** (string or null, optional): Combined local start date and time as an ISO 8601 datetime string (e.g. '2024-07-20T19:30:00'). Not adjusted to UTC.
- **`start_datetime_utc`** (string or null, optional): Start date and time expressed in UTC as an ISO 8601 datetime string (e.g. '2024-07-20T23:30:00Z'). Used as the CloudEvents time attribute.
- **`status`** (string or null, optional): Current on-sale status of the event. Known values: 'onsale' (tickets available), 'offsale' (tickets not available), 'cancelled' (event cancelled), 'postponed' (date changed, new date not yet set), 'rescheduled' (new date confirmed).
- **`segment_id`** (string or null, optional): Stable Ticketmaster classification segment identifier for this event (e.g. 'KZFzniwnSyZfZ7v7nJ' for Music). Corresponds to the top-level category.
- **`segment_name`** (string or null, optional): Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre', 'Film', 'Miscellaneous').
- **`genre_id`** (string or null, optional): Stable Ticketmaster genre identifier within the segment. Second level of the classification hierarchy.
- **`genre_name`** (string or null, optional): Human-readable genre name (e.g. 'Rock', 'Pop', 'Hip-Hop/Rap', 'Basketball', 'Theatre').
- **`subgenre_id`** (string or null, optional): Stable Ticketmaster subgenre identifier. Third level of the classification hierarchy, below genre.
- **`subgenre_name`** (string or null, optional): Human-readable subgenre name (e.g. 'Alternative Rock', 'Dance Pop', 'NBA').
- **`venue_id`** (string or null, optional): Stable Ticketmaster venue identifier for the primary venue where this event takes place. Matches entity_id in a Ticketmaster.Reference.Venue event.
- **`venue_name`** (string or null, optional): Human-readable name of the primary venue (e.g. 'Madison Square Garden').
- **`venue_city`** (string or null, optional): City where the venue is located.
- **`venue_state_code`** (string or null, optional): ISO 3166-2 state or province code for the venue location (e.g. 'NY', 'CA'). May be absent for non-US/CA venues.
- **`venue_country_code`** (string or null, optional): ISO 3166-1 alpha-2 country code for the venue location (e.g. 'US', 'GB', 'DE').
- **`venue_latitude`** (double or null, optional): WGS-84 latitude of the venue in decimal degrees. North is positive.
- **`venue_longitude`** (double or null, optional): WGS-84 longitude of the venue in decimal degrees. East is positive.
- **`price_min`** (double or null, optional): Minimum face-value ticket price in the currency indicated by the currency field. Provided by the price_ranges element in the Discovery API response when available.
- **`price_max`** (double or null, optional): Maximum face-value ticket price in the currency indicated by the currency field. Provided by the price_ranges element in the Discovery API response when available.
- **`currency`** (string or null, optional): ISO 4217 currency code for price_min and price_max (e.g. 'USD', 'GBP', 'EUR').
- **`attraction_ids`** (string or null, optional): JSON-encoded array of Ticketmaster attraction identifiers associated with this event (e.g. '["K8vZ91718H7","K8vZ9179Ki7"]'). Each ID corresponds to an entity_id in a Ticketmaster.Reference.Attraction reference event.
- **`attraction_names`** (string or null, optional): JSON-encoded array of attraction names corresponding to the attraction_ids array (e.g. '["Taylor Swift","Sabrina Carpenter"]').
- **`onsale_start_datetime`** (string or null, optional): ISO 8601 UTC datetime when public ticket sales open for this event.
- **`onsale_end_datetime`** (string or null, optional): ISO 8601 UTC datetime when public ticket sales close for this event.
- **`info`** (string or null, optional): General informational text about the event as provided by the promoter or Ticketmaster. May include age restrictions, bag policies, or other event notes.
- **`please_note`** (string or null, optional): Important notes for ticket purchasers, such as bag-check policies, camera restrictions, or health and safety requirements. Displayed prominently on the event page.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": "string",
  "name": "string",
  "type": "string",
  "url": "string",
  "locale": "string",
  "start_date": "string",
  "start_time": "string",
  "start_datetime_local": "string",
  "start_datetime_utc": "string",
  "status": "string",
  "segment_id": "string",
  "segment_name": "string",
  "genre_id": "string",
  "genre_name": "string",
  "subgenre_id": "string",
  "subgenre_name": "string",
  "venue_id": "string",
  "venue_name": "string",
  "venue_city": "string",
  "venue_state_code": "string",
  "venue_country_code": "string",
  "venue_latitude": 0,
  "venue_longitude": 0,
  "price_min": 0,
  "price_max": 0,
  "currency": "string",
  "attraction_ids": "string",
  "attraction_names": "string",
  "onsale_start_datetime": "string",
  "onsale_end_datetime": "string",
  "info": "string",
  "please_note": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Venue

CloudEvents type: `Ticketmaster.Reference.Venue`

#### What it tells you

Reference data for a Ticketmaster venue. Emitted at bridge startup and refreshed periodically. Carries the stable venue identifier, location, address, timezone, and capacity information.

#### Identity

Each event identifies the real-world resource with `{entity_id}`. `{entity_id}` is stable Ticketmaster venue identifier (e.g. 'KovZpaFVAeA'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ticketmaster`, key `{entity_id}` |
| `MQTT/5.0` | topic `civic-events/intl/ticketmaster/ticketmaster/{country}/{city}/{venue_id}/venue`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/ticketmaster`, message subject `{entity_id}` |

#### Payload

`Venue` payloads are JSON object. Required fields: `entity_id`, `name`.

- **`entity_id`** (string, required): Stable Ticketmaster venue identifier (e.g. 'KovZpaFVAeA'). Used as both the Kafka message key and the CloudEvents subject. Matches the venue_id field in Event records.
- **`name`** (string, required): Human-readable name of the venue as listed on Ticketmaster (e.g. 'Madison Square Garden', 'The O2 Arena').
- **`url`** (string or null, optional): URL to the venue page on Ticketmaster.com.
- **`locale`** (string or null, optional): BCP-47 locale string for the venue page (e.g. 'en-us').
- **`timezone`** (string or null, optional): IANA timezone database name for the venue's local time (e.g. 'America/New_York', 'Europe/London'). Used to interpret local start times in Event records.
- **`city`** (string or null, optional): City name where the venue is located.
- **`state_code`** (string or null, optional): ISO 3166-2 state or province code (e.g. 'NY', 'CA'). Populated for US and Canadian venues; absent for most international venues.
- **`country_code`** (string or null, optional): ISO 3166-1 alpha-2 country code (e.g. 'US', 'GB', 'DE', 'AU').
- **`address`** (string or null, optional): Street address line 1 for the venue (e.g. '4 Pennsylvania Plaza').
- **`postal_code`** (string or null, optional): Postal or ZIP code for the venue address.
- **`latitude`** (double or null, optional): WGS-84 latitude of the venue in decimal degrees. North is positive.
- **`longitude`** (double or null, optional): WGS-84 longitude of the venue in decimal degrees. East is positive.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "entity_id": "string",
  "name": "string",
  "url": "string",
  "locale": "string",
  "timezone": "string",
  "city": "string",
  "state_code": "string",
  "country_code": "string",
  "address": "string",
  "postal_code": "string",
  "latitude": 0,
  "longitude": 0
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Attraction

CloudEvents type: `Ticketmaster.Reference.Attraction`

#### What it tells you

Reference data for a Ticketmaster attraction (performer, artist, sports team, or production). Emitted at bridge startup and refreshed periodically. Carries stable attraction identifier, name, and classification.

#### Identity

Each event identifies the real-world resource with `{entity_id}`. `{entity_id}` is stable Ticketmaster attraction identifier (e.g. 'K8vZ91718H7'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ticketmaster`, key `{entity_id}` |
| `MQTT/5.0` | topic `civic-events/intl/ticketmaster/ticketmaster/{country}/{city}/{segment}/{entity_id}/attraction`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/ticketmaster`, message subject `{entity_id}` |

#### Payload

`Attraction` payloads are JSON object. Required fields: `entity_id`, `name`.

- **`entity_id`** (string, required): Stable Ticketmaster attraction identifier (e.g. 'K8vZ91718H7'). Used as both the Kafka message key and the CloudEvents subject. Matches values in the attraction_ids array of Event records.
- **`name`** (string, required): Human-readable name of the attraction as listed on Ticketmaster (e.g. 'Taylor Swift', 'Los Angeles Lakers').
- **`url`** (string or null, optional): URL to the attraction page on Ticketmaster.com.
- **`locale`** (string or null, optional): BCP-47 locale string for the attraction page (e.g. 'en-us').
- **`segment_id`** (string or null, optional): Stable Ticketmaster classification segment identifier for this attraction (e.g. 'KZFzniwnSyZfZ7v7nJ' for Music). Matches entity_id in Classification reference events.
- **`segment_name`** (string or null, optional): Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre').
- **`genre_id`** (string or null, optional): Stable Ticketmaster genre identifier for this attraction within its segment.
- **`genre_name`** (string or null, optional): Human-readable genre name (e.g. 'Rock', 'Pop', 'Basketball').
- **`subgenre_id`** (string or null, optional): Stable Ticketmaster subgenre identifier for this attraction.
- **`subgenre_name`** (string or null, optional): Human-readable subgenre name (e.g. 'Alternative Rock', 'Dance Pop').
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "entity_id": "string",
  "name": "string",
  "url": "string",
  "locale": "string",
  "segment_id": "string",
  "segment_name": "string",
  "genre_id": "string",
  "genre_name": "string",
  "subgenre_id": "string",
  "subgenre_name": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Classification

CloudEvents type: `Ticketmaster.Reference.Classification`

#### What it tells you

Reference data for a Ticketmaster classification segment (e.g. Music, Sports, Arts & Theatre). Emitted at bridge startup and refreshed daily.

#### Identity

Each event identifies the real-world resource with `{entity_id}`. `{entity_id}` is stable Ticketmaster segment identifier (e.g. 'KZFzniwnSyZfZ7v7nJ'). That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ticketmaster`, key `{entity_id}` |
| `MQTT/5.0` | topic `civic-events/intl/ticketmaster/ticketmaster/{country}/{city}/{segment}/{entity_id}/classification`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/ticketmaster`, message subject `{entity_id}` |

#### Payload

`Classification` payloads are JSON object. Required fields: `entity_id`, `name`.

- **`entity_id`** (string, required): Stable Ticketmaster segment identifier (e.g. 'KZFzniwnSyZfZ7v7nJ'). Used as both the Kafka message key and the CloudEvents subject. Matches segment_id in Event and Attraction records.
- **`name`** (string, required): Human-readable name of the classification segment (e.g. 'Music', 'Sports', 'Arts & Theatre', 'Film', 'Miscellaneous').
- **`type`** (string or null, optional): Ticketmaster resource type discriminator for this classification entry. Usually 'segment'.
- **`primary_genre_id`** (string or null, optional): Stable identifier for the primary or most prominent genre within this segment. Provided when the API returns a primary_genre sub-object.
- **`primary_genre_name`** (string or null, optional): Human-readable name of the primary genre (e.g. 'Rock', 'Pop', 'Basketball').
- **`primary_subgenre_id`** (string or null, optional): Stable identifier for the primary subgenre under the primary genre.
- **`primary_subgenre_name`** (string or null, optional): Human-readable name of the primary subgenre.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "entity_id": "string",
  "name": "string",
  "type": "string",
  "primary_genre_id": "string",
  "primary_genre_name": "string",
  "primary_subgenre_id": "string",
  "primary_subgenre_name": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change rather than a complete catalog.

### Info

CloudEvents type: `Ticketmaster.Reference.Info`

#### What it tells you

Retained reference information for MQTT/AMQP topic discovery. Reference information for the source, area, or event collection used by MQTT retained topics and AMQP consumers to discover the logical feed scope.

#### Identity

Each event identifies the real-world resource with `{entity_id}`. `{entity_id}` is stable upstream entity identifier for reference topics, when applicable. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `ticketmaster`, key `{entity_id}` |
| `MQTT/5.0` | topic `civic-events/intl/ticketmaster/ticketmaster/{country}/{city}/{segment}/{entity_id}/info`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/ticketmaster`, message subject `{entity_id}` |

#### Payload

`Info` payloads are JSON object. Required fields: `info_id`, `name`.

- **`info_id`** (string, required): Stable identifier for the reference information record; used as the CloudEvents subject when no more specific upstream entity exists.
- **`name`** (string, required): Human-readable name for the source, area, or event collection represented by this reference information record.
- **`country`** (string or null, optional): Lower-case ISO 3166-1 alpha-2 country code or intl when the feed spans countries.
- **`city`** (string or null, optional): City segment used in civic-events topic routing, or null when not applicable.
- **`category`** (string or null, optional): Event category segment used in topic routing, or null when not applicable.
- **`price_area`** (string or null, optional): Energy market price area or bidding zone represented by this reference record, when applicable.
- **`settlement_date`** (string or null, optional): GB settlement date for Elexon retained information topics when applicable.
- **`settlement_period`** (int32 or null, optional): GB settlement period for Elexon retained information topics when applicable.
- **`area_code`** (string or null, optional): Electricity control area or utility service area code represented by this record when applicable.
- **`segment`** (string or null, optional): Ticketmaster classification segment used for wildcard topic routing, when applicable.
- **`entity_id`** (string or null, optional): Stable upstream entity identifier for reference topics, when applicable.
- **`event_id`** (string or null, optional): Stable upstream event identifier for event-scoped reference topics, when applicable.
- **`venue_id`** (string or null, optional): Stable venue identifier for venue-scoped civic event topics, when applicable.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "info_id": "string",
  "name": "string",
  "country": "string",
  "city": "string",
  "category": "string",
  "price_area": "string",
  "settlement_date": "string",
  "settlement_period": 0,
  "area_code": "string",
  "segment": "string",
  "entity_id": "string",
  "event_id": "string",
  "venue_id": "string"
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

- xRegistry manifest: [`xreg/ticketmaster.xreg.json`](xreg/ticketmaster.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
