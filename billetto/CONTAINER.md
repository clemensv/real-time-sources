# Billetto Public Events bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container bridges the [Billetto](https://billetto.dk) public events REST
API to Apache Kafka, Azure Event Hubs, and Fabric Event Streams.

## Billetto

[Billetto](https://billetto.dk) is a pan-European ticketing and
event-discovery platform operating in Denmark, the United Kingdom, Germany,
Sweden, Norway, Finland, Belgium, Austria, and Ireland. The public REST API
provides a paginated list of upcoming publicly advertised events.

## Functionality

The bridge polls the Billetto events endpoint at a configurable interval,
detects new and updated events by content hash, and emits
`Billetto.Events.Event` CloudEvents to the configured Kafka topic in
structured JSON format, documented in [EVENTS.md](EVENTS.md).

## API Access

A free Billetto developer account is required.  Register at
<https://go.billetto.com/en-gb/resources/developers> to obtain an API keypair
(`key_id:secret` format).

## Installing the Container Image

```shell
docker pull ghcr.io/clemensv/real-time-sources-billetto:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CONNECTION_STRING` | Yes | — | Kafka connection string. Plain format: `BootstrapServer=host:port;EntityPath=topic`. Azure Event Hubs / Fabric format: full AMQP connection string with `EntityPath`. |
| `BILLETTO_API_KEYPAIR` | Yes | — | Billetto API keypair in `key_id:secret` format. Obtain from the Billetto developer hub. |
| `BILLETTO_BASE_URL` | No | `https://billetto.dk` | Billetto API base URL. Override to target country-specific endpoints (e.g. `https://billetto.co.uk`). |
| `KAFKA_TOPIC` | No | `billetto-events` | Kafka topic name used when no explicit `--topic` is provided and `CONNECTION_STRING` does not already include `EntityPath`. |
| `POLLING_INTERVAL` | No | `300` | Seconds between polls. |
| `KAFKA_ENABLE_TLS` | No | `true` | Set to `false` to disable TLS for plain Kafka brokers. |
| `LOG_LEVEL` | No | `INFO` | Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `BILLETTO_POSTAL_CODE` | No | — | Optional upstream `postal_code` filter. |
| `BILLETTO_MACROREGION` | No | — | Optional upstream `macroregion` filter. |
| `BILLETTO_REGION` | No | — | Optional upstream `region` filter. |
| `BILLETTO_SUBREGION` | No | — | Optional upstream `subregion` filter. |
| `BILLETTO_ORGANIZER_ID` | No | — | Optional upstream `organizer_id` filter. |
| `BILLETTO_EVENT_TYPE` | No | — | Optional upstream `type` filter. |
| `BILLETTO_CATEGORY` | No | — | Optional upstream `category` filter. |
| `BILLETTO_SUBCATEGORY` | No | — | Optional upstream `subcategory` filter. |

## Using the Container Image

### With a Kafka Broker

```shell
docker run --rm \
    -e CONNECTION_STRING='BootstrapServer=<broker>:9092;EntityPath=billetto-events' \
    -e BILLETTO_API_KEYPAIR='<key_id>:<secret>' \
    -e BILLETTO_REGION='Midtjylland' \
    -e BILLETTO_CATEGORY='music' \
    -e KAFKA_ENABLE_TLS='false' \
    ghcr.io/clemensv/real-time-sources-billetto:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
docker run --rm \
    -e CONNECTION_STRING='Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<key>;EntityPath=billetto-events' \
    -e BILLETTO_API_KEYPAIR='<key_id>:<secret>' \
    ghcr.io/clemensv/real-time-sources-billetto:latest
```

### With Azure Container Instances

An ARM template is included as [azure-template.json](azure-template.json). It
exposes the Billetto filter parameters as optional template parameters with
descriptions that explain when to leave them blank and when to use observed
values such as `region`, `category`, or `eventType`.

```shell
az deployment group create \
    --resource-group <resource-group> \
    --template-file azure-template.json \
    --parameters \
        connectionString='<event-hubs-or-kafka-connection-string>' \
        billettoApiKeypair='<key_id>:<secret>' \
        region='Midtjylland' \
        category='music'
```

### List Events (Diagnostic)

```shell
docker run --rm \
    -e BILLETTO_API_KEYPAIR='<key_id>:<secret>' \
    ghcr.io/clemensv/real-time-sources-billetto:latest \
    python -m billetto list --limit 20 --region Midtjylland --category music
```

## Observed Filter Vocabularies

Billetto documents the filter parameters on `GET /api/v3/public/events`, but it
does not publish separate public discovery endpoints for the allowed values. The
lists below were inferred from a broad crawl of the `billetto.dk` public feed on
**2026-04-15** covering **1,126** current public events. Treat them as
**observed values**, not a fixed enum.

| Filter | Observed values |
|---|---|
| `macroregion` | `Danmark`, `RUP FR — Régions Ultrapériphériques Françaises`, `Södra Sverige`, `Ortadoğu Anadolu`, `Ile-de-France`, `London`, `Ísland`, `Makroregion województwo mazowieckie`, `Continente`, `Kuzeydoğu Anadolu`, `Κύπρος`, `Ireland` |
| `region` | `Hovedstaden`, `Syddanmark`, `Midtjylland`, `Sjælland`, `Nordjylland`, `Guadeloupe`, `Västsverige`, `Van, Muş, Bitlis, Hakkari`, `Ile-de-France`, `Inner London — West`, `Ísland`, `Guyane`, `Warszawski stołeczny`, `Área Metropolitana de Lisboa`, `Ağrı, Kars, Iğdır, Ardahan`, `Κύπρος`, `Eastern and Midland` |
| `subregion` | `Byen København`, `Østjylland`, `Vest- og Sydsjælland`, `Fyn`, `Nordsjælland`, `Sydjylland`, `Østsjælland`, `Københavns omegn`, `Vestjylland`, `Nordjylland`, `Guadeloupe`, `Bornholm`, `Hakkari`, `Paris`, `Hallands län`, `Westminster`, `Landsbyggð`, `Guyane`, `Miasto Warszawa`, `Västra Götalands län`, `Área Metropolitana de Lisboa`, `Iğdır`, `Κύπρος`, `Dublin` |
| `category` | `music`, `performing_arts`, `community`, `food_drink`, `health_wellness`, `lifestyle`, `other`, `travel`, `sports`, `religion`, `family`, `hobbies`, `auto_boat`, `business`, `fashion`, `science`, `film_media`, `seasonal`, `government`, `charity`, `school` |
| `type` | `concert`, `class_training`, `party`, `seminar`, `tour`, `other`, `dinner`, `festival`, `appearance`, `attraction`, `conference`, `camp_trip`, `game`, `meeting`, `screening`, `tradeshow`, `race`, `rally`, `tournament` |
| `subcategory` | `other`, `comedy`, `pop`, `classical`, `dating`, `wine`, `historic`, `show`, `blues_jazz`, `theatre`, `rock`, `mental_health`, `food`, `auto`, `diy`, `city_town`, `alternative`, `baby`, `beer`, `new_age`, `circus`, `live`, `personal_health`, `hiking`, `dance`, `science`, `folk`, `mindfulness`, `fashion_beauty`, `yoga`, `latin`, `meditation`, `metal`, `zoo`, `education`, `beauty`, `kayaking`, `sales_marketing`, `basketball`, `spirits`, `drawing_painting`, `career`, `medieval`, `fine_art`, `photography`, `film`, `disco`, `indie`, `hiphop_rap`, `home_garden`, `parenting`, `edm_electronic`, `literary_arts`, `mysticism_occult`, `medical`, `alumni`, `football`, `cultural`, `heritage`, `exercise`, `chanukkah`, `cycling`, `trance`, `running`, `travel`, `national_government`, `fall_events`, `walking`, `religious_spiritual`, `adult`, `children_youth`, `blues`, `electro`, `christmas`, `americanfootball`, `opera`, `diet`, `poverty`, `anime`, `boat`, `painting`, `animal_welfare`, `randb`, `musical`, `design`, `wrestling`, `startups`, `easter`, `fighting_martial`, `reggae`, `house`, `nonprofit`, `hunting_fishing`, `christianity`, `skiing`, `international_aid`, `leadership`, `international_affairs`, `books`, `spa`, `biotech`, `after_school_care`, `gaming`, `dinner`, `golf`, `hockey`, `pets_animals`, `futsal`, `language` |

`postal_code` and `organizer_id` are supported filters too, but they are
high-cardinality and dynamic. The same crawl observed **241** distinct postal
codes, and organizer IDs vary with the currently active event publishers.

## Kafka Message Format

Messages are emitted as CloudEvents in structured JSON format
(`application/cloudevents+json`).  The Kafka partition key is the Billetto
event ID (integer, rendered as string).

### Example

```json
{
  "specversion": "1.0",
  "type": "Billetto.Events.Event",
  "source": "https://billetto.dk/api/v3/public/events",
  "subject": "12345",
  "time": "2026-07-15T19:00:00",
  "datacontenttype": "application/json",
  "data": {
    "event_id": 12345,
    "title": "Summer Jazz Festival",
    "description": "<p>A wonderful evening of jazz</p>",
    "startdate": "2026-07-15T19:00:00",
    "enddate": "2026-07-15T23:00:00",
    "url": "https://billetto.dk/e/summer-jazz-festival",
    "image_link": "https://billetto.dk/images/event/12345.jpg",
    "status": "published",
    "location_city": "Copenhagen",
    "location_name": "The Jazz Club",
    "location_address": "Nørregade 1",
    "location_zip_code": "1165",
    "location_country_code": "DK",
    "location_latitude": 55.6761,
    "location_longitude": 12.5683,
    "organiser_id": 999,
    "organiser_name": "Jazz Events DK",
    "minimum_price_amount_in_cents": 15000,
    "minimum_price_currency": "DKK",
    "availability": "available"
  }
}
```
