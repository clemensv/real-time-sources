# Fienta Public Events Bridge Events

This document describes the events emitted by the Fienta Public Events Bridge.

- [Com.Fienta](#message-group-comfienta)
  - [Com.Fienta.Event](#message-comfientaevent)
  - [Com.Fienta.EventSaleStatus](#message-comfientaeventsalestatus)

---

## Message Group: Com.Fienta

---

### Message: Com.Fienta.Event

*Reference data — sent once at startup and refreshed hourly before the telemetry polling continues.*

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `type` | CloudEvent type | `string` | `True` | `Com.Fienta.Event` |
| `source` | CloudEvent source | `string` | `True` | `https://fienta.com/api/v1/public/events` |
| `subject` | Event identifier | `uritemplate` | `True` | `{event_id}` |

#### Schema: Event

| **Field Name** | **Type** | **Description** |
|---|---|---|
| `event_id` | *string* | Unique stable identifier for the event assigned by Fienta |
| `name` | *string* | Display name of the event |
| `slug` | *string (nullable)* | URL-friendly slug for the event |
| `description` | *string (nullable)* | Full event description as set by the organizer |
| `start` | *string* | ISO 8601 start datetime including timezone offset |
| `end` | *string (nullable)* | ISO 8601 end datetime; null if not specified |
| `timezone` | *string (nullable)* | IANA timezone identifier (e.g., `Europe/Tallinn`) |
| `url` | *string* | Public web URL of the event page on Fienta |
| `language` | *string (nullable)* | ISO 639-1 language code of the event content |
| `currency` | *string (nullable)* | ISO 4217 currency code for ticket pricing |
| `status` | *string* | Publication status (e.g., `published`, `cancelled`) |
| `sale_status` | *string* | Ticket sale status (`onSale`, `soldOut`, `notOnSale`, `saleEnded`) |
| `is_online` | *boolean (nullable)* | True if the event is online |
| `is_free` | *boolean (nullable)* | True if the event has no ticket price |
| `location` | *string (nullable)* | Venue name and/or address |
| `country` | *string (nullable)* | ISO 3166-1 alpha-2 country code |
| `region` | *string (nullable)* | Sub-national region or city |
| `image_url` | *string (nullable)* | URL of the main promotional image |
| `organizer_name` | *string (nullable)* | Display name of the organizer |
| `organizer_url` | *string (nullable)* | URL of the organizer's Fienta profile |
| `categories` | *array of string (nullable)* | List of category labels |
| `created_at` | *string (nullable)* | ISO 8601 creation datetime |
| `updated_at` | *string (nullable)* | ISO 8601 last modification datetime |

#### Example CloudEvent:

```json
{
  "specversion": "1.0",
  "type": "Com.Fienta.Event",
  "source": "https://fienta.com/api/v1/public/events",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "subject": "evt-001",
  "datacontenttype": "application/json",
  "data": {
    "event_id": "evt-001",
    "name": "Jazz Night at Kultuurikatel",
    "slug": "jazz-night-at-kultuurikatel",
    "description": "An evening of live jazz music at the historic Kultuurikatel in Tallinn.",
    "start": "2024-07-15T19:00:00+03:00",
    "end": "2024-07-15T22:00:00+03:00",
    "timezone": "Europe/Tallinn",
    "url": "https://fienta.com/jazz-night-at-kultuurikatel",
    "language": "et",
    "currency": "EUR",
    "status": "published",
    "sale_status": "onSale",
    "is_online": false,
    "is_free": false,
    "location": "Kultuurikatel, Tallinn",
    "country": "EE",
    "region": "Tallinn",
    "image_url": "https://fienta.com/images/evt-001.jpg",
    "organizer_name": "Kultuurikatel",
    "organizer_url": "https://fienta.com/organizer/kultuurikatel",
    "categories": ["music", "jazz", "concert"],
    "created_at": "2024-06-01T12:00:00+03:00",
    "updated_at": "2024-07-01T10:00:00+03:00"
  }
}
```

---

### Message: Com.Fienta.EventSaleStatus

*Telemetry data — emitted whenever the `sale_status` of a public event changes.*

#### CloudEvents Attributes:

| **Name** | **Description** | **Type** | **Required** | **Value** |
|---|---|---|---|---|
| `type` | CloudEvent type | `string` | `True` | `Com.Fienta.EventSaleStatus` |
| `source` | CloudEvent source | `string` | `True` | `https://fienta.com/api/v1/public/events` |
| `subject` | Event identifier | `uritemplate` | `True` | `{event_id}` |

#### Schema: EventSaleStatus

| **Field Name** | **Type** | **Description** |
|---|---|---|
| `event_id` | *string* | Unique stable identifier for the event |
| `name` | *string* | Display name of the event at the time of the status change |
| `sale_status` | *string* | Current sale status (`onSale`, `soldOut`, `notOnSale`, `saleEnded`) |
| `status` | *string (nullable)* | Publication status (e.g., `published`, `cancelled`) |
| `start` | *string (nullable)* | ISO 8601 start datetime of the event |
| `url` | *string (nullable)* | Public URL of the event on Fienta |
| `updated_at` | *string* | ISO 8601 datetime when the event record was last modified |

#### Sale Status Values

| **Value** | **Description** |
|---|---|
| `onSale` | Tickets are available for purchase |
| `soldOut` | All tickets have been sold |
| `notOnSale` | Ticket sales have not yet opened |
| `saleEnded` | Ticket sales have closed |

#### Example CloudEvent:

```json
{
  "specversion": "1.0",
  "type": "Com.Fienta.EventSaleStatus",
  "source": "https://fienta.com/api/v1/public/events",
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "subject": "evt-001",
  "datacontenttype": "application/json",
  "data": {
    "event_id": "evt-001",
    "name": "Jazz Night at Kultuurikatel",
    "sale_status": "soldOut",
    "status": "published",
    "start": "2024-07-15T19:00:00+03:00",
    "url": "https://fienta.com/jazz-night-at-kultuurikatel",
    "updated_at": "2024-07-15T21:58:00+03:00"
  }
}
```
