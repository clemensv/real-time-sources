# Billetto Public Events Events

This document describes the events emitted by the Billetto Public Events bridge.

- [Billetto.Events](#message-group-billettoevents)
  - [Billetto.Events.Event](#message-billettoeventsevent)

---

## Message Group: Billetto.Events

---

### Message: Billetto.Events.Event

*A public ticketed event from the Billetto platform, including title, schedule, venue, organizer, pricing, and ticket availability status.*

#### CloudEvents Attributes:

| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `type` | CloudEvent type | `string` | `True` | `Billetto.Events.Event` |
| `source` | Billetto public events API endpoint | `string` | `True` | `https://billetto.dk/api/v3/public/events` |
| `subject` | Billetto event ID | `uritemplate` | `True` | `{event_id}` |
| `time` | Event start date/time | `uritemplate` | `True` | `{startdate}` |

#### Schema: Billetto.Events.Event (JsonStructure)

| **Field** | **Type** | **Description** |
|-----------|----------|-----------------|
| `event_id` | `int32` | Unique numeric identifier for the event on the Billetto platform, assigned at event creation. Used as the Kafka key and CloudEvents subject for stable event identity across polls. |
| `title` | `string` | Event title as set by the organizer. |
| `description` | `string?` | Full event description in HTML format as provided by the organizer. May be null if not set. |
| `startdate` | `string` | Event start date and time in ISO 8601 format (e.g. '2026-06-15T19:00:00'). Used as the CloudEvents time attribute. |
| `enddate` | `string?` | Event end date and time in ISO 8601 format. Null when no end time is specified by the organizer. |
| `url` | `string?` | Canonical URL of the event page on the Billetto platform. |
| `image_link` | `string?` | URL of the cover image for the event as uploaded by the organizer. |
| `status` | `string?` | Event lifecycle status as reported by the Billetto platform. Common values include 'published', 'cancelled', and 'postponed'. |
| `location_city` | `string?` | City where the event is held, from the event location object. |
| `location_name` | `string?` | Venue name where the event is held, from the event location object. |
| `location_address` | `string?` | Street address of the event venue, from the event location object. |
| `location_zip_code` | `string?` | Postal code of the event venue, from the event location object. |
| `location_country_code` | `string?` | ISO 3166-1 alpha-2 country code of the event venue (e.g. 'DK' for Denmark, 'GB' for Great Britain, 'DE' for Germany). From the event location object. |
| `location_latitude` | `double?` (°) | WGS 84 latitude of the event venue in decimal degrees. From the event location object. |
| `location_longitude` | `double?` (°) | WGS 84 longitude of the event venue in decimal degrees. From the event location object. |
| `organiser_id` | `int32?` | Unique numeric identifier for the event organizer on the Billetto platform. From the event organiser object. |
| `organiser_name` | `string?` | Display name of the event organizer as registered on the Billetto platform. From the event organiser object. |
| `minimum_price_amount_in_cents` | `int32?` | Minimum ticket price across all available ticket types, expressed in the smallest currency unit (e.g. pence for GBP, øre for DKK, cent for EUR). Zero indicates a free event. From the event minimum_price object. |
| `minimum_price_currency` | `string?` | ISO 4217 currency code for the minimum ticket price (e.g. 'GBP', 'DKK', 'EUR', 'NOK', 'SEK'). From the event minimum_price object. |
| `availability` | `string?` | Ticket availability status for the event. 'available' means tickets are currently on sale. 'sold_out' means all tickets have been sold. 'unavailable' means ticket sales are not yet open or have closed. Null when not determinable from the API response. |
