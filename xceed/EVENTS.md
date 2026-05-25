# Xceed Nightlife Events Bridge Events

Xceed public nightlife and live-entertainment event reference data. Contains scheduled event metadata including venue information. Emitted at bridge startup and refreshed periodically.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 2 |
| Messagegroups | 2 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `xceed.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`xceed`](#messagegroup-xceed) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `xceed` |
| Kafka key | `{event_id}` |
| Deployed | False |

### Endpoint `xceed.admissions.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`xceed.admissions`](#messagegroup-xceedadmissions) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `xceed` |
| Kafka key | `{event_id}/{admission_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `xceed`
<a id="messagegroup-xceed"></a>

| Field | Value |
| --- | --- |
| Description | Xceed public nightlife and live-entertainment event reference data. Contains scheduled event metadata including venue information. Emitted at bridge startup and refreshed periodically. |
| Transport bindings | `xceed.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `xceed.Event`
<a id="message-xceedevent"></a>

Metadata for a scheduled nightlife or live-entertainment event as published by the Xceed Open Event API. Includes event identity, schedule, venue, and external sales link. Emitted as reference data at startup and on each refresh cycle.

| Field | Value |
| --- | --- |
| Name | Event |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/xceed.jstruct/schemas/xceed.Event`](#schema-xceedevent) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents specification version | `string` | `True` | `1.0` |
| `type` | CloudEvents type identifier for an Xceed event record | `string` | `True` | `xceed.Event` |
| `source` | Base URL of the Xceed Open Event API feed | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Unique UUID identifier of the Xceed event, matching the Kafka key | `uritemplate` | `True` | `{event_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `xceed.Kafka` | `KAFKA` | topic `xceed`; key `{event_id}` |

### Messagegroup `xceed.admissions`
<a id="messagegroup-xceedadmissions"></a>

| Field | Value |
| --- | --- |
| Description | Xceed public offer telemetry. Contains ticket, guest-list, and bottle-service offer snapshots for each event, including sales-state signals and normalized pricing fields. Emitted each polling cycle. |
| Transport bindings | `xceed.admissions.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `xceed.EventAdmission`
<a id="message-xceedeventadmission"></a>

Ticket-, guest-list-, or bottle-service-offer snapshot for a single Xceed event admission record, retrieved from the public GET https://offer.xceed.me/v1/events/:eventId/admissions endpoint. The bridge flattens the upstream category arrays into one normalized event family while preserving the offer kind in the admission_type field.

| Field | Value |
| --- | --- |
| Name | EventAdmission |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/xceed.jstruct/schemas/xceed.EventAdmission`](#schema-xceedeventadmission) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `specversion` | CloudEvents specification version | `string` | `True` | `1.0` |
| `type` | CloudEvents type identifier for an Xceed admission record | `string` | `True` | `xceed.EventAdmission` |
| `source` | Base URL of the Xceed public offer API feed | `uritemplate` | `True` | `{feedurl}` |
| `subject` | Composite identifier consisting of the parent event UUID and the admission tier UUID, separated by a slash, matching the Kafka key | `uritemplate` | `True` | `{event_id}/{admission_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `xceed.admissions.Kafka` | `KAFKA` | topic `xceed`; key `{event_id}/{admission_id}` |

## Schemagroups

### Schemagroup `xceed.jstruct`
<a id="schemagroup-xceedjstruct"></a>

#### Schema `xceed.Event`
<a id="schema-xceedevent"></a>

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://xceed.me/schemas/xceed/Event` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Event`
<a id="schema-node-event"></a>

Scheduled nightlife or live-entertainment event record as published by the Xceed Open Event API v1 /events endpoint. Xceed is a European nightlife and ticketing platform covering clubs, bars, parties, and festivals. Each event has a stable UUID assigned by Xceed, a human-readable slug, schedule timestamps, a cover image, an optional external ticket sales link, and an embedded venue object describing the physical location.

| Field | Value |
| --- | --- |
| $id | `https://xceed.me/schemas/xceed/Event` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | `string` | `True` | Stable UUID assigned by Xceed to uniquely identify this event across all API versions. Returned as the 'id' field in the /events response. Used as the CloudEvents subject and Kafka key. | altnames=`{"json": "id"}` | - | - |
| `legacy_id` | `union` | `False` | Legacy numeric integer identifier for the event from an earlier Xceed system version. Returned as 'legacyId' in the /events response. May be null for events that were created natively in the current UUID-based system. | altnames=`{"json": "legacyId"}` | - | - |
| `name` | `string` | `True` | Human-readable display name of the event as entered by the event organiser on the Xceed platform. Examples: 'Techno Warehouse Party', 'Club Night with DJ X', 'Summer Festival Opening'. Returned as 'name' in the /events response. | - | - | - |
| `slug` | `union` | `False` | URL-friendly string identifier for the event, derived from the event name and suitable for use in Xceed web URLs. Returned as 'slug' in the /events response. Example: 'techno-warehouse-party-2024'. May be null for draft or unlisted events. | - | - | - |
| `starting_time` | `datetime` | `True` | Scheduled start time of the event expressed as a UTC datetime. Derived from the 'startingTime' UNIX epoch seconds integer in the /events response. Represents when the event doors open or the event officially begins. | altnames=`{"json": "startingTime"}` | - | - |
| `ending_time` | `union` | `False` | Scheduled end time of the event expressed as a UTC datetime. Derived from the 'endingTime' UNIX epoch seconds integer in the /events response. May be null if the organiser has not specified an end time. | altnames=`{"json": "endingTime"}` | - | - |
| `cover_url` | `union` | `False` | HTTPS URL pointing to the event's main banner or cover image hosted on the Xceed CDN. Returned as 'coverUrl' in the /events response. Suitable for display in listings and detail views. May be null if no image has been uploaded. | altnames=`{"json": "coverUrl"}` | - | - |
| `external_sales_url` | `union` | `False` | HTTPS URL pointing to an external ticket vendor or the event organiser's own sales page, when tickets are not sold directly through the Xceed platform. Returned as 'externalSalesUrl' in the /events response. Null when tickets are sold via Xceed admissions. | altnames=`{"json": "externalSalesUrl"}` | - | - |
| `venue_id` | `union` | `False` | UUID assigned by Xceed to uniquely identify the venue where this event takes place. Extracted from the nested 'venue.id' field in the /events response. Null if venue information is not available for this event. | - | - | - |
| `venue_name` | `union` | `False` | Display name of the venue as listed on the Xceed platform. Extracted from 'venue.name' in the /events response. Examples: 'Berghain', 'Fabric', 'Pacha Barcelona'. Null if venue information is not attached to this event. | - | - | - |
| `venue_city` | `union` | `False` | City in which the venue is located, as stored in the Xceed venue record. Extracted from 'venue.city' or 'venue.location.city' in the /events response. Null if venue or city information is unavailable. | - | - | - |
| `venue_country_code` | `union` | `False` | ISO 3166-1 alpha-2 country code indicating the country where the venue is located. Extracted from 'venue.countryCode' or the venue location object in the /events response. Examples: 'DE', 'GB', 'ES', 'FR'. Null if country information is unavailable. | - | - | - |

#### Schema `xceed.EventAdmission`
<a id="schema-xceedeventadmission"></a>

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://xceed.me/schemas/xceed/EventAdmission` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `EventAdmission`
<a id="schema-node-eventadmission"></a>

Normalized offer snapshot for a single admission record of an Xceed event, retrieved from the public GET https://offer.xceed.me/v1/events/:eventId/admissions endpoint. The upstream payload groups offers into bottleService, guestList, and ticket arrays. The bridge flattens those arrays into one event stream and preserves the original offer kind in admission_type while carrying key sales-state signals, normalized price, and remaining quantity.

| Field | Value |
| --- | --- |
| $id | `https://xceed.me/schemas/xceed/EventAdmission` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | `string` | `True` | UUID of the parent Xceed event that this admission tier belongs to. Matches the 'event_id' field in the corresponding xceed.Event record and the first segment of the Kafka key. | - | - | - |
| `admission_id` | `string` | `True` | Stable UUID assigned by Xceed to uniquely identify this admission or offer record within its parent event. Returned as the 'id' field of each object inside the bottleService, guestList, or ticket arrays of the GET https://offer.xceed.me/v1/events/:eventId/admissions response. Forms the second segment of the composite Kafka key '{event_id}/{admission_id}'. | altnames=`{"json": "id"}` | - | - |
| `admission_type` | `string` | `True` | Normalized Xceed offer kind for this record. Derived from the upstream 'admissionType' field when present, otherwise from the containing array name in the public offer-service response. Typical values include 'ticket', 'guestlist', and 'bottleservice'. This field preserves whether the record represents a standard ticket, a guest-list slot, or a bottle-service/table booking. | altnames=`{"json": "admissionType"}` | - | - |
| `name` | `union` | `False` | Human-readable label for this offer as set by the event organiser. Examples: 'Early Bird', 'General Admission', 'VIP Access', 'Guest List', or named table areas. Returned as 'name' in each offer object of the public offer-service response. May be null if the record has no display label. | - | - | - |
| `is_sold_out` | `union` | `False` | Boolean flag indicating whether this offer is sold out. Derived from the nested 'salesStatus.isSoldOut' field in the public offer-service response, or from a top-level 'isSoldOut' field if Xceed exposes one in future. True means no more units of this offer can be purchased. Null if the sales-state field is absent. | altnames=`{"json": "isSoldOut"}` | - | - |
| `is_sales_closed` | `union` | `False` | Boolean flag indicating whether sales for this offer have been closed, either because the sales window expired, the event started, or the organiser manually closed sales. Derived from the nested 'salesStatus.isSalesClosed' field in the public offer-service response, or from a top-level 'isSalesClosed' field if present. Null if the sales-state field is absent. | altnames=`{"json": "isSalesClosed"}` | - | - |
| `price` | `union` | `False` | Normalized price amount for this offer in the currency specified by the 'currency' field. Derived from the nested 'price.amount' field in the public offer-service response. May be null for free events, complimentary guest-list offers, or when pricing information is not exposed through the public API. | unit=`currency_unit` | - | - |
| `currency` | `union` | `False` | ISO 4217 three-letter currency code indicating the currency in which the normalized 'price' field is denominated. Derived from the nested 'price.currency' field in the public offer-service response. Examples include 'EUR' and 'GBP'. Null when price is null or when currency information is not provided by the API. | - | - | - |
| `remaining` | `union` | `False` | Remaining quantity for this offer at the time the API was polled. Derived from the upstream 'quantity' field when present, with fallback to a top-level 'remaining' field if Xceed exposes one in future. Null when remaining quantity is not tracked or not exposed through the public API. A value of 0 typically accompanies is_sold_out=true. | - | - | - |
