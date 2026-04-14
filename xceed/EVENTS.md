# Xceed Events

- [xceed](#message-group-xceed)
  - [xceed.Event](#message-xceedevent)
- [xceed.admissions](#message-group-xceedadmissions)
  - [xceed.EventAdmission](#message-xceedeventadmission)

---

## Message Group: xceed
---
### Message: xceed.Event
*Metadata for a scheduled nightlife or live-entertainment event as published by the Xceed Open Event API. Includes event identity, schedule, venue, and external sales link. Emitted as reference data at startup and on each refresh cycle.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents specification version | `string` | `True` | `1.0` |
| `type` | CloudEvents type identifier for an Xceed event record | `string` | `True` | `xceed.Event` |
| `source` | Base URL of the Xceed Open Event API feed | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Unique UUID identifier of the Xceed event, matching the Kafka key | `uritemplate` | `True` | `{event_id}` |

#### Schema:
##### Object: Event
*Scheduled nightlife or live-entertainment event record as published by the Xceed Open Event API v1 /events endpoint. Xceed is a European nightlife and ticketing platform covering clubs, bars, parties, and festivals. Each event has a stable UUID assigned by Xceed, a human-readable slug, schedule timestamps, a cover image, an optional external ticket sales link, and an embedded venue object describing the physical location.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `event_id` | *string* | - | `True` | Stable UUID assigned by Xceed to uniquely identify this event across all API versions. Returned as the 'id' field in the /events response. Used as the CloudEvents subject and Kafka key. |
| `legacy_id` | *int32* (optional) | - | `False` | Legacy numeric integer identifier for the event from an earlier Xceed system version. Returned as 'legacyId' in the /events response. May be null for events that were created natively in the current UUID-based system. |
| `name` | *string* | - | `True` | Human-readable display name of the event as entered by the event organiser on the Xceed platform. Examples: 'Techno Warehouse Party', 'Club Night with DJ X', 'Summer Festival Opening'. Returned as 'name' in the /events response. |
| `slug` | *string* (optional) | - | `False` | URL-friendly string identifier for the event, derived from the event name and suitable for use in Xceed web URLs. Returned as 'slug' in the /events response. Example: 'techno-warehouse-party-2024'. May be null for draft or unlisted events. |
| `starting_time` | *datetime* | - | `True` | Scheduled start time of the event expressed as a UTC datetime. Derived from the 'startingTime' UNIX epoch seconds integer in the /events response. Represents when the event doors open or the event officially begins. |
| `ending_time` | *datetime* (optional) | - | `False` | Scheduled end time of the event expressed as a UTC datetime. Derived from the 'endingTime' UNIX epoch seconds integer in the /events response. May be null if the organiser has not specified an end time. |
| `cover_url` | *string* (optional) | - | `False` | HTTPS URL pointing to the event's main banner or cover image hosted on the Xceed CDN. Returned as 'coverUrl' in the /events response. Suitable for display in listings and detail views. May be null if no image has been uploaded. |
| `external_sales_url` | *string* (optional) | - | `False` | HTTPS URL pointing to an external ticket vendor or the event organiser's own sales page, when tickets are not sold directly through the Xceed platform. Returned as 'externalSalesUrl' in the /events response. Null when tickets are sold via Xceed admissions. |
| `venue_id` | *string* (optional) | - | `False` | UUID assigned by Xceed to uniquely identify the venue where this event takes place. Extracted from the nested 'venue.id' field in the /events response. Null if venue information is not available for this event. |
| `venue_name` | *string* (optional) | - | `False` | Display name of the venue as listed on the Xceed platform. Extracted from 'venue.name' in the /events response. Examples: 'Berghain', 'Fabric', 'Pacha Barcelona'. Null if venue information is not attached to this event. |
| `venue_city` | *string* (optional) | - | `False` | City in which the venue is located, as stored in the Xceed venue record. Extracted from 'venue.city' or 'venue.location.city' in the /events response. Null if venue or city information is unavailable. |
| `venue_country_code` | *string* (optional) | - | `False` | ISO 3166-1 alpha-2 country code indicating the country where the venue is located. Extracted from 'venue.countryCode' or the venue location object in the /events response. Examples: 'DE', 'GB', 'ES', 'FR'. Null if country information is unavailable. |
## Message Group: xceed.admissions
---
### Message: xceed.EventAdmission
*Ticket-, guest-list-, or bottle-service-offer snapshot for a single Xceed event admission record, retrieved from the public GET https://offer.xceed.me/v1/events/:eventId/admissions endpoint. The bridge flattens the upstream category arrays into one normalized event family while preserving the offer kind in the admission_type field.*
#### CloudEvents Attributes:
| **Name**    | **Description** | **Type**     | **Required** | **Value** |
|-------------|-----------------|--------------|--------------|-----------|
| `specversion` | CloudEvents specification version | `string` | `True` | `1.0` |
| `type` | CloudEvents type identifier for an Xceed admission record | `string` | `True` | `xceed.EventAdmission` |
| `source` | Base URL of the Xceed public offer API feed | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Composite identifier consisting of the parent event UUID and the admission tier UUID, separated by a slash, matching the Kafka key | `uritemplate` | `True` | `{event_id}/{admission_id}` |

#### Schema:
##### Object: EventAdmission
*Normalized offer snapshot for a single admission record of an Xceed event, retrieved from the public GET https://offer.xceed.me/v1/events/:eventId/admissions endpoint. The upstream payload groups offers into bottleService, guestList, and ticket arrays. The bridge flattens those arrays into one event stream and preserves the original offer kind in admission_type while carrying key sales-state signals, normalized price, and remaining quantity.*
| **Field Name** | **Type** | **Unit** | **Required** | **Description** |
|----------------|----------|----------|--------------|-----------------|
| `event_id` | *string* | - | `True` | UUID of the parent Xceed event that this admission tier belongs to. Matches the 'event_id' field in the corresponding xceed.Event record and the first segment of the Kafka key. |
| `admission_id` | *string* | - | `True` | Stable UUID assigned by Xceed to uniquely identify this admission or offer record within its parent event. Returned as the 'id' field of each object inside the bottleService, guestList, or ticket arrays of the GET https://offer.xceed.me/v1/events/:eventId/admissions response. Forms the second segment of the composite Kafka key '{event_id}/{admission_id}'. |
| `admission_type` | *string* | - | `True` | Normalized Xceed offer kind for this record. Derived from the upstream 'admissionType' field when present, otherwise from the containing array name in the public offer-service response. Typical values include 'ticket', 'guestlist', and 'bottleservice'. This field preserves whether the record represents a standard ticket, a guest-list slot, or a bottle-service/table booking. |
| `name` | *string* (optional) | - | `False` | Human-readable label for this offer as set by the event organiser. Examples: 'Early Bird', 'General Admission', 'VIP Access', 'Guest List', or named table areas. Returned as 'name' in each offer object of the public offer-service response. May be null if the record has no display label. |
| `is_sold_out` | *boolean* (optional) | - | `False` | Boolean flag indicating whether this offer is sold out. Derived from the nested 'salesStatus.isSoldOut' field in the public offer-service response, or from a top-level 'isSoldOut' field if Xceed exposes one in future. True means no more units of this offer can be purchased. Null if the sales-state field is absent. |
| `is_sales_closed` | *boolean* (optional) | - | `False` | Boolean flag indicating whether sales for this offer have been closed, either because the sales window expired, the event started, or the organiser manually closed sales. Derived from the nested 'salesStatus.isSalesClosed' field in the public offer-service response, or from a top-level 'isSalesClosed' field if present. Null if the sales-state field is absent. |
| `price` | *double* (optional) | currency_unit | `False` | Normalized price amount for this offer in the currency specified by the 'currency' field. Derived from the nested 'price.amount' field in the public offer-service response. May be null for free events, complimentary guest-list offers, or when pricing information is not exposed through the public API. |
| `currency` | *string* (optional) | - | `False` | ISO 4217 three-letter currency code indicating the currency in which the normalized 'price' field is denominated. Derived from the nested 'price.currency' field in the public offer-service response. Examples include 'EUR' and 'GBP'. Null when price is null or when currency information is not provided by the API. |
| `remaining` | *int32* (optional) | - | `False` | Remaining quantity for this offer at the time the API was polled. Derived from the upstream 'quantity' field when present, with fallback to a top-level 'remaining' field if Xceed exposes one in future. Null when remaining quantity is not tracked or not exposed through the public API. A value of 0 typically accompanies is_sold_out=true. |
