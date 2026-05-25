# Fienta Public Events Bridge Events

**Fienta Public Events Bridge** polls the [Fienta](https://fienta.com) public events API for ticketed events across Europe and sends them to a Kafka topic as CloudEvents. The tool tracks previously observed `sale_status` values to detect changes and emit targeted telemetry events.

## Table of Contents

- [Registry](#registry)
- [Endpoints](#endpoints)
- [Messagegroups](#messagegroups)
- [Schemagroups](#schemagroups)

---

## Registry

| Field | Value |
| --- | --- |
| Endpoints | 1 |
| Messagegroups | 1 |
| Schemagroups | 1 |

## Endpoints

### Endpoint `Com.Fienta.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Com.Fienta`](#messagegroup-comfienta) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `fienta` |
| Kafka key | `{event_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Com.Fienta`
<a id="messagegroup-comfienta"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Com.Fienta.Kafka` (KAFKA) |
| Messages | 2 |

#### Message `Com.Fienta.Event`
<a id="message-comfientaevent"></a>

| Field | Value |
| --- | --- |
| Name | Event |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Com.Fienta.jstruct/schemas/Com.Fienta.Event`](#schema-comfientaevent) |
| Event role | Telemetry/event data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Com.Fienta.Event` |
| `source` |  | `string` | `False` | `https://fienta.com/api/v1/public/events` |
| `subject` |  | `uritemplate` | `False` | `{event_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Com.Fienta.Kafka` | `KAFKA` | topic `fienta`; key `{event_id}` |

#### Message `Com.Fienta.EventSaleStatus`
<a id="message-comfientaeventsalestatus"></a>

| Field | Value |
| --- | --- |
| Name | EventSaleStatus |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Com.Fienta.jstruct/schemas/Com.Fienta.EventSaleStatus`](#schema-comfientaeventsalestatus) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Com.Fienta.EventSaleStatus` |
| `source` |  | `string` | `False` | `https://fienta.com/api/v1/public/events` |
| `subject` |  | `uritemplate` | `False` | `{event_id}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Com.Fienta.Kafka` | `KAFKA` | topic `fienta`; key `{event_id}` |

## Schemagroups

### Schemagroup `Com.Fienta.jstruct`
<a id="schemagroup-comfientajstruct"></a>

#### Schema `Com.Fienta.Event`
<a id="schema-comfientaevent"></a>

| Field | Value |
| --- | --- |
| Name | Event |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fienta.com/schemas/Com/Fienta/Event` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Event`
<a id="schema-node-event"></a>

Reference data for a Fienta public event as exposed by the public events endpoint. Emitted at bridge startup and refreshed periodically so downstream consumers can correlate sale-status change events with the latest published event metadata from https://fienta.com/api/v1/public/events.

| Field | Value |
| --- | --- |
| $id | `https://fienta.com/schemas/Com/Fienta/Event` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | `string` | `True` | Unique stable identifier for the event as assigned by Fienta. Sourced from the 'id' field in the Fienta API response and used as the CloudEvents subject and Kafka key. | - | - | - |
| `name` | `string` | `True` | Display title of the event as shown on the public event page. Sourced from the 'title' field in the Fienta API response. | - | - | - |
| `start` | `string` | `True` | Local event start datetime string in the format 'YYYY-MM-DD HH:MM:SS'. Sourced from the 'starts_at' field in the Fienta API response. | - | - | - |
| `end` | `union` | `False` | Local event end datetime string in the format 'YYYY-MM-DD HH:MM:SS'. Null when the public event payload has no end time. Sourced from the 'ends_at' field in the Fienta API response. | - | - | - |
| `duration_text` | `union` | `False` | Human-readable duration summary rendered by Fienta for the event schedule, for example 'Tue 1. April 2025 at 09:00 - Thu 31. December 2026 at 17:00'. Sourced from the 'duration_string' field in the Fienta API response. | - | - | - |
| `time_notes` | `union` | `False` | Free-form notes about the event timing published by the organizer. Null when the event listing has no timing note. Sourced from the 'notes_about_time' field in the Fienta API response. | - | - | - |
| `event_status` | `string` | `True` | Lifecycle status of the event listing as published by Fienta, for example 'scheduled'. Sourced from the 'event_status' field in the Fienta API response. | - | - | - |
| `sale_status` | `string` | `True` | Current ticket sale status of the event. Observed values in the public feed include 'onSale', 'soldOut', 'notOnSale', and 'saleEnded'. Sourced from the 'sale_status' field in the Fienta API response. | - | - | - |
| `attendance_mode` | `union` | `False` | Attendance mode reported by Fienta for the event, for example 'offline'. Null when the public event listing omits the field. Sourced from the 'attendance_mode' field in the Fienta API response. | - | - | - |
| `venue_name` | `union` | `False` | Venue or place name shown on the public event listing, for example 'Worldwide' or a named physical venue. Null when not supplied. Sourced from the 'venue' field in the Fienta API response. | - | - | - |
| `venue_id` | `union` | `False` | Venue identifier provided by Fienta for the event location. Null when the listing has no venue identifier. Sourced from the 'venue_id' field in the Fienta API response. | - | - | - |
| `address` | `union` | `False` | Postal street address for the venue as shown on the public event listing. Null when the address is not supplied. Sourced from the 'address' field in the Fienta API response. | - | - | - |
| `postal_code` | `union` | `False` | Postal code for the venue address. Null when the event listing has no postal code. Sourced from the 'address_postal_code' field in the Fienta API response. | - | - | - |
| `description` | `union` | `False` | Event description as published by the organizer. The public payload can contain HTML markup or be empty. Sourced from the 'description' field in the Fienta API response. | - | - | - |
| `url` | `string` | `True` | Public Fienta URL for the event details page. Sourced from the 'url' field in the Fienta API response. | - | - | - |
| `buy_tickets_url` | `union` | `False` | Public URL that Fienta exposes for the ticket purchase flow. Null when the listing does not include a dedicated purchase URL. Sourced from the 'buy_tickets_url' field in the Fienta API response. | - | - | - |
| `image_url` | `union` | `False` | URL of the primary promotional image for the event. Null when no image is provided. Sourced from the 'image_url' field in the Fienta API response. | - | - | - |
| `image_small_url` | `union` | `False` | URL of the smaller promotional image variant for the event. Null when the public event listing does not include a smaller image rendition. Sourced from the 'image_small_url' field in the Fienta API response. | - | - | - |
| `series_id` | `union` | `False` | Series identifier or slug used by Fienta to group related event listings. Null when the event is not associated with a series. Sourced from the 'series_id' field in the Fienta API response. | - | - | - |
| `organizer_name` | `union` | `False` | Display name of the event organizer. Null when the organizer name is absent from the public payload. Sourced from the 'organizer_name' field in the Fienta API response. | - | - | - |
| `organizer_phone` | `union` | `False` | Organizer phone number published on the event listing. Null when the organizer did not expose a phone number. Sourced from the 'organizer_phone' field in the Fienta API response. | - | - | - |
| `organizer_email` | `union` | `False` | Organizer email address published on the event listing. Null when the organizer did not expose an email address. Sourced from the 'organizer_email' field in the Fienta API response. | - | - | - |
| `organizer_id` | `union` | `False` | Numeric identifier of the organizer account in Fienta. Null when the public event payload omits the organizer identifier. Sourced from the 'organizer_id' field in the Fienta API response. | - | - | - |
| `categories` | array of `string` | `False` | List of category labels assigned to the event listing, such as 'other' or 'family'. The bridge emits an empty array when the public event payload omits the categories array. Sourced from the 'categories' field in the Fienta API response. | - | - | - |

#### Schema `Com.Fienta.EventSaleStatus`
<a id="schema-comfientaeventsalestatus"></a>

| Field | Value |
| --- | --- |
| Name | EventSaleStatus |
| Format | JsonStructure/draft-02 |
| Default version | 1 |

##### Version `1`

| Field | Value |
| --- | --- |
| Format | JsonStructure/draft-02 |

###### JsonStructure

| Field | Value |
| --- | --- |
| $id | `https://fienta.com/schemas/Com/Fienta/EventSaleStatus` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `EventSaleStatus`
<a id="schema-node-eventsalestatus"></a>

Telemetry event emitted whenever the bridge observes a change in the sale_status value of a Fienta public event between two polls of the public events endpoint.

| Field | Value |
| --- | --- |
| $id | `https://fienta.com/schemas/Com/Fienta/EventSaleStatus` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | `string` | `True` | Unique stable identifier for the event as assigned by Fienta. Sourced from the 'id' field in the Fienta API response and used as the CloudEvents subject and Kafka key. | - | - | - |
| `name` | `string` | `True` | Display title of the event at the time the bridge observed the sale status change. Sourced from the 'title' field in the Fienta API response. | - | - | - |
| `sale_status` | `string` | `True` | Current ticket sale status observed for the event, such as 'onSale', 'soldOut', 'notOnSale', or 'saleEnded'. Sourced from the 'sale_status' field in the Fienta API response. | - | - | - |
| `event_status` | `union` | `False` | Lifecycle status of the event listing at the time of observation, for example 'scheduled'. Null when the public payload omits the value. Sourced from the 'event_status' field in the Fienta API response. | - | - | - |
| `start` | `union` | `False` | Local event start datetime string in the format 'YYYY-MM-DD HH:MM:SS'. Null when the public event payload omits the start time. Sourced from the 'starts_at' field in the Fienta API response. | - | - | - |
| `end` | `union` | `False` | Local event end datetime string in the format 'YYYY-MM-DD HH:MM:SS'. Null when the public event payload omits the end time. Sourced from the 'ends_at' field in the Fienta API response. | - | - | - |
| `url` | `union` | `False` | Public Fienta URL for the event details page. Null when the public payload omits the event URL. Sourced from the 'url' field in the Fienta API response. | - | - | - |
| `buy_tickets_url` | `union` | `False` | Public URL that Fienta exposes for the ticket purchase flow at the time of the observation. Null when the listing does not include a dedicated purchase URL. Sourced from the 'buy_tickets_url' field in the Fienta API response. | - | - | - |
| `observed_at` | `string` | `True` | RFC 3339 UTC timestamp generated by the bridge when it observed the sale_status change while polling the Fienta public events API. | - | - | - |
