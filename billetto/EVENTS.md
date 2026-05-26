# Billetto Public Events Bridge Events

MQTT 5.0 binary-mode CloudEvents variant of Billetto.Events.

## At a glance

- **Event types:** 1 documented event type (3 transport bindings in the manifest).
- **Transports:** KAFKA, MQTT/5.0, AMQP/1.0
- **Reference vs telemetry:** 0 reference/catalog event types and 1 telemetry event type.
- **Identity:** `{event_id}` identifies the resource each event is about.
- **Operations:** Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.
- **Read next:** [Quick start](#quick-start--how-to-consume), [Event catalog](#event-catalog), [Conventions](#conventions), [Operational notes](#operational-notes), [References](#references).

## Quick start — how to consume

These examples show the smallest useful consumer for each transport declared by this source. Replace host names, credentials, topics, and addresses with your deployment values.

### Kafka

Subscribe to `billetto-events`. The record key is `{event_id}`. In plain language, `{event_id}` is the stable identity of the resource described by the event. Kafka uses the key for partition routing: events with the same key go to the same partition and keep per-key order, but consumers still receive an interleaved stream.

```python
from confluent_kafka import Consumer
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'events-demo','auto.offset.reset':'earliest'})
c.subscribe(['billetto-events'])
while True:
    m=c.poll(1.0)
    if m and not m.error(): print(m.key(), dict(m.headers() or []), m.value())
```

Use different `group.id` values when every consumer should see every event; use the same group id to share partitions. Disable auto-commit and commit after processing for at-least-once application handling.
### MQTT 5

Connect to `mqtt://localhost:1883` and subscribe to `civic-events/intl/billetto/billetto/+/+/+/+/event`. In MQTT filters, `+` matches exactly one topic level and `#` matches the remaining levels only when it is the final segment. Messages published with the RETAIN flag are delivered once per matching topic at subscribe time as Last Known Value; non-retained messages are live stream updates only.

```python
import paho.mqtt.client as mqtt
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
c.on_message=lambda c,u,m: print(m.topic, getattr(m.properties,'UserProperty',None), m.payload)
c.connect('localhost',1883)
c.subscribe(('civic-events/intl/billetto/billetto/+/+/+/+/event', 1))
c.loop_forever()
```

Subscribe at QoS 1 with a stable client id, `CleanStart=false`, and a finite non-zero session expiry when you need at-least-once delivery across reconnects. Retained messages are delivered subject to MQTT 5 Retain Handling, and publishing an empty retained payload clears the retained value. MQTT 5 user properties carry CloudEvents metadata; MQTT 3.1.1 clients need structured CloudEvents because they do not have user properties.
### AMQP 1.0

Attach a link with `role=receiver` whose **source** is `billetto`. The source terminus is the broker-side node you consume from; source filters such as selectors, Event Hubs offsets, or subscription filters further select which messages flow. The target is your client-side terminus. Generic brokers use their advertised SASL mechanisms (often PLAIN over TLS, EXTERNAL with mTLS, or ANONYMOUS on trusted links). Azure Service Bus and Event Hubs can use SASL PLAIN for SAS credentials on short-lived connections; CBS `put-token` on `$cbs` installs and refreshes Entra ID JWTs or SAS tokens for long-lived AMQP connections.

```python
from proton.handlers import MessagingHandler
from proton.reactor import Container
class H(MessagingHandler):
    def on_start(self,e): e.container.create_receiver('amqps://user:pass@localhost:5671/billetto')
    def on_message(self,e): print(e.message.subject, e.message.properties, e.message.body)
Container(H()).run()
```

The examples use AMQP binary content mode: the JSON payload is the message body, `datacontenttype` maps to the AMQP `content-type`, and CloudEvents attributes map to application properties named `cloudEvents:<attribute>`.

## Event catalog

### Event

CloudEvents type: `Billetto.Events.Event`

#### What it tells you

A public ticketed event from the Billetto platform, including title, schedule, venue, organizer, pricing, and ticket availability status. A public ticketed event from the Billetto platform. Each record represents a single upcoming or ongoing public event with schedule, venue, organizer, pricing, and availability information.

#### Identity

Each event identifies the real-world resource with `{event_id}`. `{event_id}` is unique numeric identifier for the event on the Billetto platform, assigned at event creation. That value is the CloudEvents `subject` and is mirrored into transport routing fields where the protocol has them.

#### Where to find it

| Transport | Location |
| --- | --- |
| `KAFKA` | topic `billetto-events`, key `{event_id}` |
| `MQTT/5.0` | topic `civic-events/intl/billetto/billetto/{country}/{city}/{category}/{event_id}/event`, retain `true`, QoS `1` |
| `AMQP/1.0` | source address `amqps://localhost:5671/billetto`, message subject `{event_id}` |

#### Payload

`Event` payloads are JSON object. Required fields: `event_id`, `title`, `startdate`.

- **`event_id`** (int32, required): Unique numeric identifier for the event on the Billetto platform, assigned at event creation. Used as the Kafka key and CloudEvents subject for stable event identity across polls.
- **`title`** (string, required): Event title as set by the organizer.
- **`description`** (string or null, optional): Full event description in HTML format as provided by the organizer. May be null if not set.
- **`startdate`** (string, required): Event start date and time in ISO 8601 format (e.g. '2026-06-15T19:00:00'). Used as the CloudEvents time attribute.
- **`enddate`** (string or null, optional): Event end date and time in ISO 8601 format. Null when no end time is specified by the organizer.
- **`url`** (string or null, optional): Canonical URL of the event page on the Billetto platform.
- **`image_link`** (string or null, optional): URL of the cover image for the event as uploaded by the organizer.
- **`status`** (string or null, optional): Event lifecycle status as reported by the Billetto platform. Common values include 'published', 'cancelled', and 'postponed'.
- **`location_city`** (string or null, optional): City where the event is held, from the event location object.
- **`location_name`** (string or null, optional): Venue name where the event is held, from the event location object.
- **`location_address`** (string or null, optional): Street address of the event venue, from the event location object.
- **`location_zip_code`** (string or null, optional): Postal code of the event venue, from the event location object.
- **`location_country_code`** (string or null, optional): ISO 3166-1 alpha-2 country code of the event venue (e.g. 'DK' for Denmark, 'GB' for Great Britain, 'DE' for Germany). From the event location object.
- **`location_latitude`** (double or null, optional, degree (°)): WGS 84 latitude of the event venue in decimal degrees. From the event location object.
- **`location_longitude`** (double or null, optional, degree (°)): WGS 84 longitude of the event venue in decimal degrees. From the event location object.
- **`organiser_id`** (int32 or null, optional): Unique numeric identifier for the event organizer on the Billetto platform. From the event organiser object.
- **`organiser_name`** (string or null, optional): Display name of the event organizer as registered on the Billetto platform. From the event organiser object.
- **`minimum_price_amount_in_cents`** (int32 or null, optional): Minimum ticket price across all available ticket types, expressed in the smallest currency unit (e.g. pence for GBP, øre for DKK, cent for EUR). Zero indicates a free event. From the event minimum_price object.
- **`minimum_price_currency`** (string or null, optional): ISO 4217 currency code for the minimum ticket price (e.g. 'GBP', 'DKK', 'EUR', 'NOK', 'SEK'). From the event minimum_price object.
- **`availability`** (string or null, optional): Ticket availability status for the event. 'available' means tickets are currently on sale. 'sold_out' means all tickets have been sold. 'unavailable' means ticket sales are not yet open or have closed. Null when not determinable from the API response.
#### Example payload

Synthetic example values are generated deterministically from the schema: constants, defaults, or examples win; otherwise strings use `"string"`, numbers use `0`, booleans use `false`, enums use their first value, arrays contain one item, nullable fields use a non-null example when possible, and timestamps use `2024-01-01T00:00:00Z`.

```json
{
  "event_id": 0,
  "title": "string",
  "description": "string",
  "startdate": "string",
  "enddate": "string",
  "url": "string",
  "image_link": "string",
  "status": "string",
  "location_city": "string",
  "location_name": "string",
  "location_address": "string",
  "location_zip_code": "string",
  "location_country_code": "string",
  "location_latitude": 0,
  "location_longitude": 0,
  "organiser_id": 0,
  "organiser_name": "string",
  "minimum_price_amount_in_cents": 0,
  "minimum_price_currency": "string",
  "availability": "string"
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

- Reference/catalog events are documented as startup emissions, with periodic refresh when the source supports it.

## References

- xRegistry manifest: [`xreg/billetto.xreg.json`](xreg/billetto.xreg.json)
- Source README: [`README.md`](README.md)
- Container deployment guide: [`CONTAINER.md`](CONTAINER.md)
- Obtaining an API key: <https://api.billetto.com/docs/obtaining-an-api-key>
