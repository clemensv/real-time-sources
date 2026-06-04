<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/gb.png" alt="England" width="64" height="48"><br>
<sub><b>England</b></sub>
</td>
<td valign="middle">

# UK BODS SIRI

<sub>28,000+ buses · Kafka · MQTT · AMQP · <a href="https://data.bus-data.dft.gov.uk/">upstream</a> · <a href="https://www.gov.uk/government/publications/technical-guidance-publishing-location-data-using-the-bus-open-data-service-siri-vm">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> England — Department for Transport Bus Open Data Service AVL archive (requires free API key)

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#uk-bods-siri) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#uk-bods-siri/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/uk-bods-siri.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://data.bus-data.dft.gov.uk/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the UK Department for Transport **Bus Open Data Service** (**BODS**) AVL bulk archive into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 / Unified Namespace, and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://data.bus-data.dft.gov.uk/>
- API / data documentation: <https://www.gov.uk/government/publications/technical-guidance-publishing-location-data-using-the-bus-open-data-service-siri-vm>
- Archive reference: <https://data.datalibrary.uk/transport/BODS-ARCHIVE/sirivm/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

BODS publishes bus Automatic Vehicle Location data as SIRI-VM XML snapshots. That makes the source excellent public infrastructure, but awkward operational input: every consumer otherwise has to register for an API key, download the bulk archive, unzip it, stream-parse XML, deduplicate repeated `ItemIdentifier` values, and then fan the result out to its own brokers and schemas.

This bridge does that work once and re-emits the feed as typed CloudEvents so downstream systems can subscribe instead of scrape:

- **Transit operations** — live fleet movement and route-progress dashboards.
- **City intelligence** — join bus movement with roads, incidents, weather, and events.
- **Analytics and archival** — standardized ingestion into Fabric Eventhouse, ADX, or lakehouses.
- **Automation** — route/vehicle-based rules over stable subjects and topic trees.
- **Digital twins** — operator and vehicle identities carried consistently across transports.

## Overview

**UK BODS SIRI** is a poll-based bridge. It emits two event families from the AVL bulk archive:

- `uk.gov.dft.bods.Operator` — distinct operator codes observed in the archive (reference data).
- `uk.gov.dft.bods.VehiclePosition` — one current vehicle activity per bus per poll cycle (telemetry).

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-uk-bods-siri-kafka` | Apache Kafka 2.x compatible (incl. Azure Event Hubs and Microsoft Fabric Event Streams) | Topic `uk-bods-siri`, key `{operator_ref}/{vehicle_ref}` for telemetry and `{operator_ref}` for operator references |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt` | MQTT 5.0 broker (incl. Event Grid MQTT and Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree `transit/uk/dft/bods/{operator_ref}/{vehicle_ref}/position` and `transit/uk/dft/bods/{operator_ref}/info` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp` | AMQP 1.0 (incl. Service Bus and Event Hubs via CBS auth) | Binary CloudEvents on AMQP node `uk-bods-siri` |

All variants share the same xRegistry contract (`xreg/uk-bods-siri.xreg.json`), generated producer packages, XML parser, dedupe model, and operator filter.

## Transports

Kafka, MQTT, and AMQP all carry the same payload schemas and CloudEvents types, but target different consumption styles:

- **Kafka** — best for ordered stream processing, Event Hubs, and Fabric Event Streams.
- **MQTT** — best for low-latency pub/sub and UNS-style routing by operator and vehicle.
- **AMQP** — best for queue/topic brokers such as Azure Service Bus and Artemis where broker-side filters or enterprise messaging semantics matter.

Deployment templates shipped with this source:

1. Kafka container against your own Kafka/Event Hubs connection string.
2. Kafka container plus a new Event Hubs namespace.
3. MQTT container against your own MQTT broker.
4. MQTT container plus a new Azure Event Grid namespace broker.
5. AMQP container plus a new Azure Service Bus namespace.
6. Fabric ACI deployment via the project portal.
7. Fabric Notebook deployment for the poller via `tools/deploy-fabric/deploy-feeder-notebook.ps1`.

## Repository layout

```text
uk-bods-siri/
  xreg/uk-bods-siri.xreg.json
  uk_bods_siri_core/
  uk_bods_siri_kafka/
  uk_bods_siri_mqtt/
  uk_bods_siri_amqp/
  uk_bods_siri_producer/
  uk_bods_siri_mqtt_producer/
  uk_bods_siri_amqp_producer/
  kql/
  notebook/
  tests/
  Dockerfile.kafka
  Dockerfile.mqtt
  Dockerfile.amqp
```

## Quick start with Docker

> [!IMPORTANT]
> BODS requires a free API key passed as `BODS_API_KEY`.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e CONNECTION_STRING="<event-hubs-or-fabric-connection-string>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-kafka:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt:latest
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/uk-bods-siri" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp:latest
```

## Configuration reference

The complete environment-variable matrix for each image is documented in [CONTAINER.md](CONTAINER.md). The bridge accepts:

- `BODS_API_KEY` — required unless `BODS_SAMPLE_MODE=true` is used for tests.
- `OPERATORS` — optional comma-separated NOC filter.
- `POLLING_INTERVAL` — poll cadence in seconds (default 30).
- `STATE_FILE` — restart-safe dedupe state path.
- `ONCE_MODE` / `--once` — single-cycle execution for Docker E2E and Fabric notebooks.

## Fabric notebook hosting

Because this source is a poller, it also ships a Fabric notebook feeder in [`notebook/uk-bods-siri-feed.ipynb`](notebook/uk-bods-siri-feed.ipynb), deployable with `tools/deploy-fabric/deploy-feeder-notebook.ps1`.

## Data model

The feeder emits the following event families:

- **uk.gov.dft.bods** — `Operator`, `VehiclePosition`.

See [EVENTS.md](EVENTS.md) for the full field-level schema contract and per-transport routing details.
