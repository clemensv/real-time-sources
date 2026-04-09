# LAQN London Air Quality Network

## Overview

The LAQN London Air Quality Network bridge polls the public LAQN API operated by
King's College London and emits structured JSON CloudEvents to Kafka. It keeps
the upstream split intact: site metadata, species metadata, hourly site
measurements, and Daily Air Quality Index bulletin records.

The bridge uses the HTTP-only upstream at `http://api.erg.ic.ac.uk/AirQuality/`.
That is not a typo. The upstream does not offer HTTPS.

## Event Families

- `uk.kcl.laqn.Site` — monitoring site reference data keyed by `site_code`
- `uk.kcl.laqn.Species` — pollutant catalog reference data keyed by
  `species_code`
- `uk.kcl.laqn.Measurement` — hourly pollutant measurements keyed by
  `site_code`
- `uk.kcl.laqn.DailyIndex` — Daily AQI bulletin records keyed by `site_code`

Reference data is emitted at startup and refreshed every 24 polls. Telemetry is
polled every hour by default.

Some LAQN site records leave the decimal latitude or longitude blank. The bridge
preserves those as `null` in site reference events instead of failing the
reference-data pass.

## Upstream Channels Reviewed

| Family | Endpoint | Identity | Cadence | Decision |
|---|---|---|---|---|
| Site metadata | `GET /Information/MonitoringSites/GroupName=All/Json` | `site_code` | Daily / startup | Keep |
| Species catalog | `GET /Information/Species/Json` | `species_code` | Rarely changes | Keep |
| Daily AQI index | `GET /Daily/MonitoringIndex/Latest/GroupName=London/Json` | `site_code` | Hourly | Keep |
| Hourly site measurements | `GET /Data/Site/SiteCode={code}/StartDate={YYYY-MM-DD}/EndDate={YYYY-MM-DD}/Json` | `site_code` | Hourly | Keep |
| Hourly AQI by site | `GET /Hourly/MonitoringIndex/SiteCode={code}/Json` | `site_code` | Hourly | Drop — overlaps the Daily AQI bulletin |
| Site-species data | `GET /Data/SiteSpecies/...` | `site_code` | Hourly | Drop — covered by the site measurement endpoint |

## Installation

```bash
git clone https://github.com/clemensv/real-time-sources.git
cd real-time-sources/laqn-london
pip install laqn_london_producer/laqn_london_producer_data
pip install laqn_london_producer/laqn_london_producer_kafka_producer
pip install -e .
```

## Usage

The package installs the `laqn_london` command.

### List sites

```bash
laqn_london sites
```

### List species

```bash
laqn_london species
```

### Fetch the latest Daily AQI bulletin

```bash
laqn_london daily-index
```

### Run the Kafka bridge

```bash
laqn_london feed \
  --kafka-bootstrap-servers "<broker:9093>" \
  --kafka-topic "laqn-london" \
  --sasl-username "<username>" \
  --sasl-password "<password>" \
  --polling-interval 3600
```

Or, with an Event Hubs or Fabric connection string:

```bash
laqn_london feed --connection-string "<connection-string>" --polling-interval 3600
```

## Environment Variables

- `CONNECTION_STRING` — Event Hubs / Fabric connection string
- `KAFKA_BOOTSTRAP_SERVERS` — Kafka bootstrap servers
- `KAFKA_TOPIC` — Kafka topic
- `SASL_USERNAME` — SASL username
- `SASL_PASSWORD` — SASL password
- `KAFKA_ENABLE_TLS` — set to `false` for plain local Kafka
- `POLLING_INTERVAL` — polling interval in seconds, default `3600`
- `STATE_FILE` — path to the persisted dedupe state file

## State and Deduplication

The bridge tracks measurement events by
`site_code:species_code:measurement_date_gmt` and Daily AQI events by
`site_code:species_code:bulletin_date`. Empty measurement values are skipped,
sites with `@DateClosed` are excluded from telemetry polling, and Daily AQI
entries with whitespace-only `Species` payloads are ignored.

## Related Documentation

- [CONTAINER.md](CONTAINER.md) — container usage
- [EVENTS.md](EVENTS.md) — generated event contract documentation
- [DATABASE.md](../DATABASE.md) — downstream analytics notes

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Flaqn-london%2Fazure-template-with-eventhub.json)
