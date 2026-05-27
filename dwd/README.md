<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/de.png" alt="Germany" width="64" height="48"><br>
<sub><b>Germany</b></sub>
</td>
<td valign="middle">

# DWD

<sub>~1,450 stations, observations and CAP alerts · Kafka · MQTT · AMQP · <a href="https://www.dwd.de/">upstream</a> · <a href="https://opendata.dwd.de/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Germany — ~1,450 stations, observations and CAP alerts

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#dwd) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/dwd.kql) &nbsp;·&nbsp;
[🗺️ **Fabric Map**](fabric/README.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.dwd.de/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the public [Deutscher Wetterdienst (DWD) open-data file server](https://opendata.dwd.de/) into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.dwd.de/>
- API / data documentation: <https://opendata.dwd.de/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

[DWD Open Data](https://opendata.dwd.de/) publishes near-real-time weather observations, station metadata, CAP alerts, radar product listings, and ICON-D2 forecast file metadata from roughly 1,450 stations and multiple national product feeds across Germany. The source is richly structured but operationally awkward: consumers otherwise have to watch directory listings, unpack ZIP bundles, parse CAP feeds, track state per station and per file tree, and correlate reference metadata with telemetry.

This bridge turns that file-server estate into a first-class real-time event stream so consumers can stop polling DWD directly and start subscribing to a topic:

- **National weather operations** — drive station dashboards, state-level weather views, and warning consoles from one normalized stream.
- **Critical infrastructure and utilities** — combine observations, alerts, and radar file updates for grid, rail, airport, and road-weather operations.
- **Hydrology and agriculture analytics** — ingest temperature, precipitation, wind, and solar observations alongside weather alerts for downstream models.
- **Radar and forecast processing pipelines** — use file-metadata events to trigger fetch-and-decode jobs for HDF5, BUFR, and GRIB2 assets only when new files arrive.
- **Research and public-sector data platforms** — land DWD observations and alerts into Microsoft Fabric Eventhouse / Azure Data Explorer without rebuilding polling and dedupe logic.

The bridge does the boring work — module selection, checkpoint state, per-station watermarks, CAP dedupe, directory listing diffs, reference-data emission, JSON-Structure–validated CloudEvents, and identity plumbing — so the consumer just subscribes.

## Overview

**DWD Open Data** is a poll-based bridge that combines several upstream channel families into one operational source. The source ships in three transport variants from the same modular poller contract:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-dwd` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | Four message-family topics (CDC, Weather, Radar, Forecast), JSON CloudEvents (binary mode), key = `{station_id}`, `{identifier}`, or `{file_url}` depending on family |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-dwd-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic branches under `weather/de/dwd/dwd/...` and `alerts/de/dwd/dwd/...`, JSON body, CloudEvent attributes as MQTT 5 user properties, QoS 1 with retain behavior depending on family |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-dwd-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | Single AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three variants share:

* The modular DWD poller (`station_metadata`, `station_obs_10min`, `station_obs_10min_extremes`, `station_obs_hourly`, `weather_alerts`, `radar_products`, `icon_d2_forecast`).
* The xRegistry contract (`xreg/dwd.xreg.json`).
* Four message families with 13 total event types: CDC observations, Weather alerts, Radar catalogs/files, and Forecast catalogs/files.

## Key features

- **13 DWD event types** grouped into four message families with stable identity models.
- **Mixed source coverage** — station metadata, 10-minute and hourly observations, CAP alerts, radar product metadata, and ICON-D2 forecast file metadata.
- **Configurable modules** — enable only the families you need with `DWD_MODULES` / `DWD_MODULES_DISABLED`.
- **Checkpointed polling state** via `STATE_FILE` for station timestamps, seen alerts, and watched directory listings.
- **Reference data first** — station metadata, radar catalogs, and forecast model catalogs are emitted as first-class event types.
- **Three transport binaries** sharing the same upstream scope and event contracts — switch transport without redesigning consumers.
- **Retained MQTT branches where Last Known Value makes sense** (station and observation/catalog topics) and live-only branches where it does not (alerts and file notifications).
- **Azure Event Hubs / Microsoft Fabric Event Streams** ready via standard connection strings (Kafka variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra ID** (no SAS-key rotation) via CBS put-token, plus SAS-token CBS for emulator / SAS-only namespaces.

## Repository layout

```text
dwd/
  xreg/dwd.xreg.json              # shared xRegistry contract
  dwd/                            # modular poller + Kafka feeder application
  dwd_mqtt/                       # MQTT/UNS feeder application
  dwd_amqp/                       # AMQP 1.0 feeder application
  dwd_producer/                   # xRegistry-generated Kafka producer
  dwd_mqtt_producer/              # xRegistry-generated MQTT producer
  dwd_amqp_producer/              # xRegistry-generated AMQP producer
  Dockerfile                      # builds the Kafka feeder image
  Dockerfile.mqtt                 # builds the MQTT feeder image
  Dockerfile.amqp                 # builds the AMQP feeder image
  kql/dwd.kql                     # Eventhouse / KQL schema and update policies
  kql/icond2.kql                  # optional KQL helpers for forecast-file workloads
  tests/                          # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS access to `opendata.dwd.de`.
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.

This feeder is a poller, not a websocket source. It can run stateless for evaluation, but if you want restart continuity you should persist `STATE_FILE` outside the container in your real deployment.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="<event-hubs-connection-string>" \
  ghcr.io/clemensv/real-time-sources-dwd:latest
```

Replace `<event-hubs-connection-string>` with a connection string from your Azure Event Hubs namespace, Microsoft Fabric Event Stream custom endpoint, or any Kafka 2.x broker that accepts the same SASL-PLAIN-over-TLS shape.

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-dwd-mqtt:latest
```

Topics published include retained station / observation branches and live-only alert / file-notification branches, for example:

```text
weather/de/dwd/dwd/{state}/{station_id}/info
alerts/de/dwd/dwd/{state}/{severity}/{identifier}/alert
weather/de/dwd/dwd/products/radar/{product_type}/{file_id}/file
weather/de/dwd/dwd/catalogs/{kind}/catalog
```

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/dwd' \
  ghcr.io/clemensv/real-time-sources-dwd-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service Bus emulator, or SAS-only namespaces, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image) for the full environment-variable matrix.

## Configuration reference

The complete list of environment variables for every variant (Kafka, MQTT, AMQP), every authentication mode (SASL PLAIN, Microsoft Entra ID via CBS, SAS-token CBS), and every Azure deployment shape lives in [CONTAINER.md](CONTAINER.md). The runtime entry point for the images is `python -m dwd feed`, `python -m dwd_mqtt feed`, or `python -m dwd_amqp feed`; the image default `CMD` invokes it for you.

## Data model

DWD is a multi-family source. It emits four message groups with distinct key models and routing shapes.

### `DE.DWD.CDC` — station observations and metadata

Key model: `{station_id}`

| Event type | Description |
|---|---|
| `DE.DWD.CDC.StationMetadata` | Reference metadata for each weather station: identity, coordinates, elevation, state, and validity dates. |
| `DE.DWD.CDC.AirTemperature10Min` | 10-minute air-temperature observations. |
| `DE.DWD.CDC.Precipitation10Min` | 10-minute precipitation observations. |
| `DE.DWD.CDC.Wind10Min` | 10-minute wind observations. |
| `DE.DWD.CDC.Solar10Min` | 10-minute solar-radiation observations. |
| `DE.DWD.CDC.HourlyObservation` | Hourly observation bundle for lower-frequency recent datasets. |
| `DE.DWD.CDC.ExtremeWind10Min` | 10-minute extreme wind observations. |
| `DE.DWD.CDC.ExtremeTemperature10Min` | 10-minute extreme temperature observations. |

This family is the operational weather-station core of the source. Station metadata is reference data; the other event types are telemetry updated on the cadence of the underlying DWD datasets.

### `DE.DWD.Weather` — CAP weather alerts

Key model: `{identifier}`

| Event type | Description |
|---|---|
| `DE.DWD.Weather.Alert` | One DWD CAP alert, including severity, urgency, event classification, affected areas, and validity windows. |

Alerts are live notifications rather than Last Known Value measurements, so the MQTT alert branch is intentionally non-retained.

### `DE.DWD.Radar` — radar product catalogs and file notifications

Key model: `{file_url}` for file events

| Event type | Description |
|---|---|
| `DE.DWD.Radar.RadarProductCatalog` | Reference metadata for a radar product family / directory. |
| `DE.DWD.Radar.RadarFileProduct` | Metadata for a newly discovered or updated radar file, including a fetchable HTTPS URL. |

The bridge emits **file metadata, not the binary radar payload itself**. Consumers fetch the referenced DWD file on demand — typically HDF5, BUFR, or RADOLAN-style binary products depending on the radar branch.

### `DE.DWD.Forecast` — forecast model catalogs and ICON-D2 file notifications

Key model: `{file_url}` for file events

| Event type | Description |
|---|---|
| `DE.DWD.Forecast.ForecastModelCatalog` | Reference metadata for the forecast model family (for example `icon-d2`). |
| `DE.DWD.Forecast.IconD2ForecastFile` | Metadata for a newly discovered or updated ICON-D2 forecast file, including a fetchable HTTPS URL and parsed run/lead information when available. |

As with radar, the bridge emits **metadata about forecast files** rather than embedding GRIB2 content in the event payload. The file event is the trigger to fetch and decode the referenced DWD asset downstream.

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

DWD targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/), and the bundled [Fabric Map](fabric/README.md) visualizes the live state on a basemap.

Use the deploy button on the [project portal](https://clemensv.github.io/real-time-sources#dwd) to launch the Fabric ACI hosting model — it walks you through Fabric workspace selection and follow-up steps.

#### Fabric ACI feeder &nbsp;<sub><i>(continuous container hosting against a Fabric Event Stream)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source dwd `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#dwd/fabric-aci)

#### Fabric Map visualization &nbsp;<sub><i>(optional, post-deploy)</i></sub>

After either hosting model has events flowing, run [`fabric/post-deploy.ps1`](fabric/README.md) (or `tools/deploy-fabric/deploy-fabric.ps1 -Source dwd -Workspace <ws>`) to provision the bundled Fabric Map item and wire its Kusto-backed layers onto a basemap. The map updates live as new events arrive.


### Deploying into Azure Container Instances

6 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue, a user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-with-servicebus.json)

#### AMQP — bring your own AMQP 1.0 peer

Deploy the AMQP container against an existing AMQP 1.0 peer (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs). You pass the broker URL and credentials; the template provisions only the container.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdwd%2Fazure-template-amqp.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps

- Pick a hosting model: a [Fabric ACI feeder](#deploying-into-microsoft-fabric) if your destination is a Fabric workspace; a [direct Azure deployment](#deploying-into-azure-container-instances) if you target Event Hubs, MQTT, or Service Bus without Fabric.
- Review the [event contract and schemas](EVENTS.md) before writing a consumer.
- Look up authentication modes and the full environment-variable matrix in [CONTAINER.md](CONTAINER.md).
- Browse the upstream DWD open-data server at [opendata.dwd.de](https://opendata.dwd.de/) for product-family specifics and downstream file-decoding requirements.
