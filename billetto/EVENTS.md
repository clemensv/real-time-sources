# Billetto Public Events Bridge Events

This bridge polls the [Billetto](https://billetto.dk) public events REST API and forwards event data to Apache Kafka, Azure Event Hubs, or Fabric Event Streams as [CloudEvents](https://cloudevents.io/).

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

### Endpoint `Billetto.Events.Kafka`

| Field | Value |
| --- | --- |
| Usage | producer |
| Protocol | `KAFKA` |
| Envelope | CloudEvents/1.0 |
| Envelope options | `{"format": "application/cloudevents+json", "mode": "structured"}` |
| Messagegroups | [`Billetto.Events`](#messagegroup-billettoevents) |

#### Transport options

| Option | Value |
| --- | --- |
| Kafka topic | `billetto-events` |
| Kafka key | `{event_id}` |
| Deployed | False |

## Messagegroups

### Messagegroup `Billetto.Events`
<a id="messagegroup-billettoevents"></a>

| Field | Value |
| --- | --- |
| Transport bindings | `Billetto.Events.Kafka` (KAFKA) |
| Messages | 1 |

#### Message `Billetto.Events.Event`
<a id="message-billettoeventsevent"></a>

A public ticketed event from the Billetto platform, including title, schedule, venue, organizer, pricing, and ticket availability status.

| Field | Value |
| --- | --- |
| Name | Event |
| Envelope | CloudEvents/1.0 |
| Schema format | JsonStructure/draft-02 |
| Data schema | [`#/schemagroups/Billetto.Events.jstruct/schemas/Billetto.Events.Event`](#schema-billettoeventsevent) |
| Event role | Reference/status data |

##### CloudEvents metadata

| Attribute | Description | Type | Required | Value/template |
| --- | --- | --- | --- | --- |
| `type` |  | `string` | `False` | `Billetto.Events.Event` |
| `source` |  | `string` | `False` | `https://billetto.dk/api/v3/public/events` |
| `subject` |  | `uritemplate` | `False` | `{event_id}` |
| `time` |  | `uritemplate` | `False` | `{startdate}` |

##### Bound transports

| Endpoint | Protocol | Binding |
| --- | --- | --- |
| `Billetto.Events.Kafka` | `KAFKA` | topic `billetto-events`; key `{event_id}` |

## Schemagroups

### Schemagroup `Billetto.Events.jstruct`
<a id="schemagroup-billettoeventsjstruct"></a>

#### Schema `Billetto.Events.Event`
<a id="schema-billettoeventsevent"></a>

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
| $id | `https://example.com/schemas/Billetto/Events/Event` |
| $schema | `https://json-structure.org/meta/extended/v0/#` |
| Type | `object` |

###### Object `Event`
<a id="schema-node-event"></a>

A public ticketed event from the Billetto platform. Each record represents a single upcoming or ongoing public event with schedule, venue, organizer, pricing, and availability information.

| Field | Value |
| --- | --- |
| $id | `https://example.com/schemas/Billetto/Events/Event` |

| Field | Type | Required | Description | Extensions | Validation | Default/const |
| --- | --- | --- | --- | --- | --- | --- |
| `event_id` | `int32` | `True` | Unique numeric identifier for the event on the Billetto platform, assigned at event creation. Used as the Kafka key and CloudEvents subject for stable event identity across polls. | altnames=`{"upstream": "id"}` | - | - |
| `title` | `string` | `True` | Event title as set by the organizer. | - | - | - |
| `description` | `union` | `False` | Full event description in HTML format as provided by the organizer. May be null if not set. | - | - | - |
| `startdate` | `string` | `True` | Event start date and time in ISO 8601 format (e.g. '2026-06-15T19:00:00'). Used as the CloudEvents time attribute. | altnames=`{"upstream": "startdate"}` | - | - |
| `enddate` | `union` | `False` | Event end date and time in ISO 8601 format. Null when no end time is specified by the organizer. | - | - | - |
| `url` | `union` | `False` | Canonical URL of the event page on the Billetto platform. | - | - | - |
| `image_link` | `union` | `False` | URL of the cover image for the event as uploaded by the organizer. | - | - | - |
| `status` | `union` | `False` | Event lifecycle status as reported by the Billetto platform. Common values include 'published', 'cancelled', and 'postponed'. | - | - | - |
| `location_city` | `union` | `False` | City where the event is held, from the event location object. | altnames=`{"upstream": "location.city"}` | - | - |
| `location_name` | `union` | `False` | Venue name where the event is held, from the event location object. | altnames=`{"upstream": "location.location_name"}` | - | - |
| `location_address` | `union` | `False` | Street address of the event venue, from the event location object. | altnames=`{"upstream": "location.address"}` | - | - |
| `location_zip_code` | `union` | `False` | Postal code of the event venue, from the event location object. | altnames=`{"upstream": "location.zip_code"}` | - | - |
| `location_country_code` | `union` | `False` | ISO 3166-1 alpha-2 country code of the event venue (e.g. 'DK' for Denmark, 'GB' for Great Britain, 'DE' for Germany). From the event location object. | altnames=`{"upstream": "location.country_code"}` | - | - |
| `location_latitude` | `union` | `False` | WGS 84 latitude of the event venue in decimal degrees. From the event location object. | unit=`degree` symbol=`°`<br>altnames=`{"upstream": "location.latitude"}` | - | - |
| `location_longitude` | `union` | `False` | WGS 84 longitude of the event venue in decimal degrees. From the event location object. | unit=`degree` symbol=`°`<br>altnames=`{"upstream": "location.longitude"}` | - | - |
| `organiser_id` | `union` | `False` | Unique numeric identifier for the event organizer on the Billetto platform. From the event organiser object. | altnames=`{"upstream": "organiser.id"}` | - | - |
| `organiser_name` | `union` | `False` | Display name of the event organizer as registered on the Billetto platform. From the event organiser object. | altnames=`{"upstream": "organiser.name"}` | - | - |
| `minimum_price_amount_in_cents` | `union` | `False` | Minimum ticket price across all available ticket types, expressed in the smallest currency unit (e.g. pence for GBP, øre for DKK, cent for EUR). Zero indicates a free event. From the event minimum_price object. | altnames=`{"upstream": "minimum_price.amount_in_cents"}` | - | - |
| `minimum_price_currency` | `union` | `False` | ISO 4217 currency code for the minimum ticket price (e.g. 'GBP', 'DKK', 'EUR', 'NOK', 'SEK'). From the event minimum_price object. | altnames=`{"upstream": "minimum_price.currency"}` | - | - |
| `availability` | `union` | `False` | Ticket availability status for the event. 'available' means tickets are currently on sale. 'sold_out' means all tickets have been sold. 'unavailable' means ticket sales are not yet open or have closed. Null when not determinable from the API response. | - | - | - |
