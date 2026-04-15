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
| [azure-template.json](azure-template.json) | Azure Container Instance deployment template |
| [CONTAINER.md](CONTAINER.md) | Deployment contract |
| [EVENTS.md](EVENTS.md) | Event catalog |

## API Access

A Billetto account is required to obtain an API keypair. Per Billetto's
[Obtaining an API key](https://api.billetto.com/docs/obtaining-an-api-key)
guide, the flow is:

1. Create or sign in to your Billetto account.
2. Switch the account into the organiser experience using **Switch to Organiser**.
3. Open **Menu** -> **Integrate**.
4. Open the **Developers** section.
5. Generate an API keypair and copy both the key ID and the secret.

Billetto only shows the secret on first read. If you do not store it when the
keypair is created, you must generate a new one.

The API accepts requests to `https://billetto.dk/api/v3/public/events` with
an `Api-Keypair: <key_id>:<secret>` header.

For this bridge, set:

```powershell
$env:BILLETTO_API_KEYPAIR = "<key_id>:<secret>"
```

## Supported API Filters

The bridge now exposes the Billetto public-events filters supported by
`GET /api/v3/public/events`. You can provide them as CLI arguments or
environment variables.

| API query param | CLI argument | Environment variable |
|---|---|---|
| `postal_code` | `--postal-code` | `BILLETTO_POSTAL_CODE` |
| `macroregion` | `--macroregion` | `BILLETTO_MACROREGION` |
| `region` | `--region` | `BILLETTO_REGION` |
| `subregion` | `--subregion` | `BILLETTO_SUBREGION` |
| `organizer_id` | `--organizer-id` | `BILLETTO_ORGANIZER_ID` |
| `type` | `--event-type` | `BILLETTO_EVENT_TYPE` |
| `category` | `--category` | `BILLETTO_CATEGORY` |
| `subcategory` | `--subcategory` | `BILLETTO_SUBCATEGORY` |

Example:

```powershell
$env:BILLETTO_REGION = "Midtjylland"
$env:BILLETTO_CATEGORY = "music"
python -m billetto feed --connection-string "BootstrapServer=localhost:9092;EntityPath=billetto-events"
```

### Observed Filter Values

Billetto does not publish separate discovery endpoints for these vocabularies in
the public docs. The lists below were therefore inferred from a broad
`billetto.dk` feed crawl on **2026-04-15** covering **1,126** public events.
They are **observed values**, not a contractual enum, and they can change as
Billetto listings change or when you target a different Billetto domain.

**Observed macroregions**

```text
Danmark
RUP FR — Régions Ultrapériphériques Françaises
Södra Sverige
Ortadoğu Anadolu
Ile-de-France
London
Ísland
Makroregion województwo mazowieckie
Continente
Kuzeydoğu Anadolu
Κύπρος
Ireland
```

**Observed regions**

```text
Hovedstaden
Syddanmark
Midtjylland
Sjælland
Nordjylland
Guadeloupe
Västsverige
Van, Muş, Bitlis, Hakkari
Ile-de-France
Inner London — West
Ísland
Guyane
Warszawski stołeczny
Área Metropolitana de Lisboa
Ağrı, Kars, Iğdır, Ardahan
Κύπρος
Eastern and Midland
```

**Observed subregions**

```text
Byen København
Østjylland
Vest- og Sydsjælland
Fyn
Nordsjælland
Sydjylland
Østsjælland
Københavns omegn
Vestjylland
Nordjylland
Guadeloupe
Bornholm
Hakkari
Paris
Hallands län
Westminster
Landsbyggð
Guyane
Miasto Warszawa
Västra Götalands län
Área Metropolitana de Lisboa
Iğdır
Κύπρος
Dublin
```

**Observed categories**

```text
music
performing_arts
community
food_drink
health_wellness
lifestyle
other
travel
sports
religion
family
hobbies
auto_boat
business
fashion
science
film_media
seasonal
government
charity
school
```

**Observed event types**

```text
concert
class_training
party
seminar
tour
other
dinner
festival
appearance
attraction
conference
camp_trip
game
meeting
screening
tradeshow
race
rally
tournament
```

**Observed subcategories**

```text
other
comedy
pop
classical
dating
wine
historic
show
blues_jazz
theatre
rock
mental_health
food
auto
diy
city_town
alternative
baby
beer
new_age
circus
live
personal_health
hiking
dance
science
folk
mindfulness
fashion_beauty
yoga
latin
meditation
metal
zoo
education
beauty
kayaking
sales_marketing
basketball
spirits
drawing_painting
career
medieval
fine_art
photography
film
disco
indie
hiphop_rap
home_garden
parenting
edm_electronic
literary_arts
mysticism_occult
medical
alumni
football
cultural
heritage
exercise
chanukkah
cycling
trance
running
travel
national_government
fall_events
walking
religious_spiritual
adult
children_youth
blues
electro
christmas
americanfootball
opera
diet
poverty
anime
boat
painting
animal_welfare
randb
musical
design
wrestling
startups
easter
fighting_martial
reggae
house
nonprofit
hunting_fishing
christianity
skiing
international_aid
leadership
international_affairs
books
spa
biotech
after_school_care
gaming
dinner
golf
hockey
pets_animals
futsal
language
```

`postal_code` and `organizer_id` are intentionally not listed here because they
are high-cardinality, data-driven filters. The same crawl observed **241**
distinct postal codes, and organizer IDs vary with the active publisher set.

## Upstream Links

- [Billetto Developer Hub](https://go.billetto.com/en-gb/resources/developers)
- [Obtaining an API key](https://api.billetto.com/docs/obtaining-an-api-key)
- [List all public events](https://api.billetto.com/reference/list-public-events)
- [Billetto API documentation](https://api.billetto.com/docs)
- [Billetto main site](https://billetto.dk)
