# Xceed Nightlife Events feeder Events

Xceed public nightlife and live-entertainment event reference data. Contains scheduled event metadata including venue information. Emitted at bridge startup and refreshed periodically.

## At a glance

- **Event types:** 2 documented event types (6 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 2 telemetry event types.
- **Identity:** `{event_id}`, `{event_id}/{admission_id}` identifies the resource each event is about.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `xceed`. The record key is `{event_id}`, `{event_id}/{admission_id}`. Each key template is explained in the event catalog below. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['xceed'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `civic-events/intl/xceed/xceed/+/+/event`, `civic-events/intl/xceed/xceed/admissions/+/+/admission`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('civic-events/intl/xceed/xceed/+/+/event', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `xceed`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/xceed')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Event

CloudEvents type: `xceed.Event`

#### What it tells you

Metadata for a scheduled nightlife or live-entertainment event as published by the Xceed Open Event API. Includes event identity, schedule, venue, and external sales link. Emitted as reference data at startup and on each refresh cycle.

#### Identity

Each event identifies the real-world resource with `{event_id}`. `{event_id}` is stable UUID assigned by Xceed to uniquely identify this event across all API versions. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `xceed`, key `{event_id}` |
| `MQTT/5.0` | topic `civic-events/intl/xceed/xceed/{city}/{event_id}/event`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/xceed`, message subject `{event_id}` |

#### Payload

`Event` payloads are JSON object. Required fields: `event_id`, `name`, `starting_time`.

- **`event_id`** (string, required): Stable UUID assigned by Xceed to uniquely identify this event across all API versions. Returned as the 'id' field in the /events response. Used as the CloudEvents subject and Kafka key.
- **`legacy_id`** (int32 or null, optional): Legacy numeric integer identifier for the event from an earlier Xceed system version. Returned as 'legacyId' in the /events response. May be null for events that were created natively in the current UUID-based system.
- **`name`** (string, required): Human-readable display name of the event as entered by the event organiser on the Xceed platform. Examples: 'Techno Warehouse Party', 'Club Night with DJ X', 'Summer Festival Opening'. Returned as 'name' in the /events response.
- **`slug`** (string or null, optional): URL-friendly string identifier for the event, derived from the event name and suitable for use in Xceed web URLs. Returned as 'slug' in the /events response. Example: 'techno-warehouse-party-2024'. May be null for draft or unlisted events.
- **`starting_time`** (datetime, required): Scheduled start time of the event expressed as a UTC datetime. Derived from the 'startingTime' UNIX epoch seconds integer in the /events response. Represents when the event doors open or the event officially begins.
- **`ending_time`** (datetime or null, optional): Scheduled end time of the event expressed as a UTC datetime. Derived from the 'endingTime' UNIX epoch seconds integer in the /events response. May be null if the organiser has not specified an end time.
- **`cover_url`** (string or null, optional): HTTPS URL pointing to the event's main banner or cover image hosted on the Xceed CDN. Returned as 'coverUrl' in the /events response. Suitable for display in listings and detail views. May be null if no image has been uploaded.
- **`external_sales_url`** (string or null, optional): HTTPS URL pointing to an external ticket vendor or the event organiser's own sales page, when tickets are not sold directly through the Xceed platform. Returned as 'externalSalesUrl' in the /events response. Null when tickets are sold via Xceed admissions.
- **`venue_id`** (string or null, optional): UUID assigned by Xceed to uniquely identify the venue where this event takes place. Extracted from the nested 'venue.id' field in the /events response. Null if venue information is not available for this event.
- **`venue_name`** (string or null, optional): Display name of the venue as listed on the Xceed platform. Extracted from 'venue.name' in the /events response. Examples: 'Berghain', 'Fabric', 'Pacha Barcelona'. Null if venue information is not attached to this event.
- **`venue_city`** (string or null, optional): City in which the venue is located, as stored in the Xceed venue record. Extracted from 'venue.city' or 'venue.location.city' in the /events response. Null if venue or city information is unavailable.
- **`venue_country_code`** (string or null, optional): ISO 3166-1 alpha-2 country code indicating the country where the venue is located. Extracted from 'venue.countryCode' or the venue location object in the /events response. Examples: 'DE', 'GB', 'ES', 'FR'. Null if country information is unavailable.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": "string",
  "legacy_id": 0,
  "name": "string",
  "slug": "string",
  "starting_time": "2024-01-01T00:00:00Z",
  "ending_time": "2024-01-01T00:00:00Z",
  "cover_url": "string",
  "external_sales_url": "string",
  "venue_id": "string",
  "venue_name": "string",
  "venue_city": "string",
  "venue_country_code": "string"
}
```

#### Reference vs telemetry

This is telemetry/event data. Treat each event as a current observation or state change. If an MQTT binding is retained, the retained copy is only the latest value for that exact topic, not a history.

### Event Admission

CloudEvents type: `xceed.EventAdmission`

#### What it tells you

Ticket-, guest-list-, or bottle-service-offer snapshot for a single Xceed event admission record, retrieved from the public GET https://offer.xceed.me/v1/events/:eventId/admissions endpoint. The bridge flattens the upstream category arrays into one normalized event family while preserving the offer kind in the admission_type field. Normalized offer snapshot for a single admission record of an Xceed event, retrieved from the public GET https://offer.xceed.me/v1/events/:eventId/admissions endpoint.

#### Identity

Each event identifies the real-world resource with `{event_id}/{admission_id}`. `{event_id}` is UUID of the parent Xceed event that this admission tier belongs to; `{admission_id}` is stable UUID assigned by Xceed to uniquely identify this admission or offer record within its parent event. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `xceed`, key `{event_id}/{admission_id}` |
| `MQTT/5.0` | topic `civic-events/intl/xceed/xceed/admissions/{event_id}/{admission_id}/admission`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/xceed`, message subject `{event_id}/{admission_id}` |

#### Payload

`Event Admission` payloads are JSON object. Required fields: `event_id`, `admission_id`, `admission_type`.

- **`event_id`** (string, required): UUID of the parent Xceed event that this admission tier belongs to. Matches the 'event_id' field in the corresponding xceed.Event record and the first segment of the Kafka key.
- **`admission_id`** (string, required): Stable UUID assigned by Xceed to uniquely identify this admission or offer record within its parent event. Returned as the 'id' field of each object inside the bottleService, guestList, or ticket arrays of the GET https://offer.xceed.me/v1/events/:eventId/admissions response. Forms the second segment of the composite Kafka key '{event_id}/{admission_id}'.
- **`admission_type`** (string, required): Normalized Xceed offer kind for this record. Derived from the upstream 'admissionType' field when present, otherwise from the containing array name in the public offer-service response. Typical values include 'ticket', 'guestlist', and 'bottleservice'. This field preserves whether the record represents a standard ticket, a guest-list slot, or a bottle-service/table booking.
- **`name`** (string or null, optional): Human-readable label for this offer as set by the event organiser. Examples: 'Early Bird', 'General Admission', 'VIP Access', 'Guest List', or named table areas. Returned as 'name' in each offer object of the public offer-service response. May be null if the record has no display label.
- **`is_sold_out`** (boolean or null, optional): Boolean flag indicating whether this offer is sold out. Derived from the nested 'salesStatus.isSoldOut' field in the public offer-service response, or from a top-level 'isSoldOut' field if Xceed exposes one in future. True means no more units of this offer can be purchased. Null if the sales-state field is absent.
- **`is_sales_closed`** (boolean or null, optional): Boolean flag indicating whether sales for this offer have been closed, either because the sales window expired, the event started, or the organiser manually closed sales. Derived from the nested 'salesStatus.isSalesClosed' field in the public offer-service response, or from a top-level 'isSalesClosed' field if present. Null if the sales-state field is absent.
- **`price`** (double or null, optional, currency_unit): Normalized price amount for this offer in the currency specified by the 'currency' field. Derived from the nested 'price.amount' field in the public offer-service response. May be null for free events, complimentary guest-list offers, or when pricing information is not exposed through the public API.
- **`currency`** (string or null, optional): ISO 4217 three-letter currency code indicating the currency in which the normalized 'price' field is denominated. Derived from the nested 'price.currency' field in the public offer-service response. Examples include 'EUR' and 'GBP'. Null when price is null or when currency information is not provided by the API.
- **`remaining`** (int32 or null, optional): Remaining quantity for this offer at the time the API was polled. Derived from the upstream 'quantity' field when present, with fallback to a top-level 'remaining' field if Xceed exposes one in future. Null when remaining quantity is not tracked or not exposed through the public API. A value of 0 typically accompanies is_sold_out=true.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": "string",
  "admission_id": "string",
  "admission_type": "string",
  "name": "string",
  "is_sold_out": false,
  "is_sales_closed": false,
  "price": 0,
  "currency": "string",
  "remaining": 0
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

No source-specific polling cadence, rate limit, or stream characteristic is documented in the checked-in README or CONTAINER guide.

## References

- xRegistry manifest: [`xreg/xceed.xreg.json`](xreg/xceed.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
