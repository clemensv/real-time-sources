# Billetto Public Events Bridge

This bridge polls the [Billetto](https://billetto.dk) public events REST API
and forwards event data to Apache Kafka, Azure Event Hubs, or Fabric Event
Streams as [CloudEvents](https://cloudevents.io/).

Billetto is a pan-European ticketing and event-discovery platform operating
in Denmark, the United Kingdom, Germany, Sweden, Norway, Finland, Belgium,
Austria, and Ireland.

## Overview

The bridge periodically calls the Billetto public events endpoint
(`/api/v3/public/events`), detects new and updated events by content hash,
and emits `Billetto.Events.Event` CloudEvents to the configured Kafka topic.
The stable Billetto event ID is used as both the CloudEvents `subject` and
the Kafka partition key.

## Event Families

| Type | Description |
|------|-------------|
| `Billetto.Events.Event` | A public Billetto event with schedule, venue, organizer, price, and availability |

## Data Model

Each event record carries:

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | `int` | Unique Billetto event ID (Kafka key) |
| `title` | `string` | Event title |
| `description` | `string?` | HTML event description |
| `startdate` | `string` | Start date/time (ISO 8601) |
| `enddate` | `string?` | End date/time (ISO 8601) |
| `url` | `string?` | Billetto event page URL |
| `image_link` | `string?` | Cover image URL |
| `status` | `string?` | Lifecycle status (e.g. `published`, `cancelled`) |
| `location_city` | `string?` | City |
| `location_name` | `string?` | Venue name |
| `location_address` | `string?` | Street address |
| `location_zip_code` | `string?` | Postal code |
| `location_country_code` | `string?` | ISO 3166-1 alpha-2 country code |
| `location_latitude` | `double?` | Venue latitude (WGS 84) |
| `location_longitude` | `double?` | Venue longitude (WGS 84) |
| `organiser_id` | `int?` | Organizer ID |
| `organiser_name` | `string?` | Organizer display name |
| `minimum_price_amount_in_cents` | `int?` | Minimum ticket price in smallest currency unit |
| `minimum_price_currency` | `string?` | ISO 4217 currency code |
| `availability` | `string?` | Ticket availability: `available`, `sold_out`, or `unavailable` |

## Source Files

| File | Description |
|------|-------------|
| [xreg/billetto.xreg.json](xreg/billetto.xreg.json) | xRegistry manifest (authoritative contract) |
| [billetto/billetto.py](billetto/billetto.py) | Runtime bridge |
| [billetto_producer/](billetto_producer/) | Generated producer (xrcg 0.10.1) |
| [tests/](tests/) | Unit tests |
| [Dockerfile](Dockerfile) | Container image |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |

## API Access

A free Billetto developer account is required to obtain an API keypair.
Register at <https://go.billetto.com/en-gb/resources/developers>.

The API accepts requests to `https://billetto.dk/api/v3/public/events` with
an `Api-Keypair: <key_id>:<secret>` header.

## Upstream Links

- [Billetto Developer Hub](https://go.billetto.com/en-gb/resources/developers)
- [Billetto API documentation](https://api.billetto.com/docs)
- [Billetto main site](https://billetto.dk)
