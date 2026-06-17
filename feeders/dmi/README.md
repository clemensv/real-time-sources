<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/dk.png" alt="Denmark" width="64" height="48"><br>
<sub><b>Denmark</b></sub>
</td>
<td valign="middle">

# DMI

<sub>meteorological observations, sea level, lightning strikes · Kafka · MQTT · AMQP · <a href="https://www.dmi.dk/">upstream</a> · <a href="https://opendatadocs.dmi.govcloud.dk/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Denmark — meteorological observations, sea level, lightning strikes

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#dmi) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#dmi/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/dmi.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.dmi.dk/)

</td></tr></table>
<!-- source-hero:end -->

## Overview

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.dmi.dk/>
- API / data documentation: <https://opendatadocs.dmi.govcloud.dk/>

<!-- upstream-links:end -->

**DMI** is a bridge that polls the [Danish Meteorological Institute Open Data
API](https://opendatadocs.dmi.govcloud.dk/) and re-emits the **observation
triad** (`metObs` + `oceanObs` + `lightningData`) as CloudEvents. A single
upstream poller feeds three transport variants:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-dmi-kafka` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | Single topic `dmi`, JSON CloudEvents (binary mode), keys = stable upstream identifiers |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-dmi-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree under `weather/dk/dmi/…` and `ocean/dk/dmi/…`, JSON body, CloudEvent attributes as MQTT 5 user properties, retained at QoS 1 |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-dmi-amqp` | AMQP 1.0 broker (incl. Azure Service Bus, Azure Event Hubs, ActiveMQ Artemis, RabbitMQ AMQP 1.0) | Binary-mode AMQP 1.0 messages to one address `dmi`; subject = stable upstream identifier |

> **Lightning is excluded from MQTT only.** Per-strike events have no natural last-known-value
> shape, so the MQTT image publishes only `metObs` and `oceanObs`. Kafka and
> AMQP both carry the full observation triad, including `lightningData`.

## CloudEvent types

| Type | Source | Key / subject template | Retained on MQTT |
|---|---|---|---|
| `dk.dmi.metObs.Station` | metObs | `{station_id}` | yes |
| `dk.dmi.metObs.Observation` | metObs | `{station_id}/{parameter_id}` | yes |
| `dk.dmi.oceanObs.OceanStation` | oceanObs | `{station_id}` | yes |
| `dk.dmi.oceanObs.OceanObservation` | oceanObs | `{station_id}/{parameter_id}` | yes |
| `dk.dmi.oceanObs.TidewaterStation` | oceanObs | `{station_id}` | yes |
| `dk.dmi.oceanObs.TidewaterPrediction` | oceanObs | `{station_id}` | yes |
| `dk.dmi.lightning.Sensor` | lightningData | `{sensor_id}` | — (not on MQTT) |
| `dk.dmi.lightning.Strike` | lightningData | `{strike_id}` | — (not on MQTT) |

All three messagegroups multiplex onto the **single** Kafka topic `dmi` and the **single** AMQP address `dmi`. Subscribers route by CloudEvent `type`. Full schemas are in
[EVENTS.md](EVENTS.md); KQL ingestion in [kql/dmi.kql](kql/dmi.kql).

## Repository Layout

```
dmi/
  xreg/dmi.xreg.json            # shared xRegistry contract
  dmi_core/                     # transport-agnostic acquisition + config
  dmi_kafka/                    # Kafka feeder (metObs + oceanObs + lightning)
  dmi_mqtt/                     # MQTT/UNS feeder  (metObs + oceanObs)
  dmi_amqp/                     # AMQP 1.0 feeder (metObs + oceanObs + lightning)
  dmi_producer/                 # xrcg-generated Kafka producer
  dmi_mqtt_producer/            # xrcg-generated MQTT producer
  dmi_amqp_producer/            # xrcg-generated AMQP producer
  Dockerfile.kafka              # Kafka image
  Dockerfile.mqtt               # MQTT image
  Dockerfile.amqp               # AMQP image
  kql/dmi.kql                   # KQL schema for Fabric Eventhouse / ADX
  notebook/dmi-feed.ipynb       # Fabric notebook feeder (Kafka path)
  azure-template*.json          # five one-click ACI deploy templates
  tests/                        # unit + integration tests
```

## API keys

DMI Open Data is served auth-free from `https://opendataapi.dmi.dk` — **no
API key is required** for any of the three products. The feeders poll all
configured products out of the box with no credentials.

Keys remain optional and are only used if you point a feed back at the
legacy authenticated host (`https://dmigw.govcloud.dk`) via the
`DMI_METOBS_FEED_ROOT` / `DMI_OCEANOBS_FEED_ROOT` / `DMI_LIGHTNING_FEED_ROOT`
env vars. In that case supply the matching key:

* `DMI_METOBS_API_KEY` / `DMI_OCEANOBS_API_KEY` / `DMI_LIGHTNING_API_KEY` —
  per-API keys, sent in the `X-Gravitee-Api-Key` header when present.
* `DMI_API_KEY` — fallback used for any API without a dedicated key.

The MQTT image only publishes MetObs and OceanObs events; Kafka and AMQP
additionally publish lightning events.

Rate limits: **500 req / 5 s** per key apply to the legacy authenticated
host (DMI public quota).

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="$EVENT_HUBS_CONNECTION_STRING" \
  -e DMI_METOBS_API_KEY="$DMI_METOBS_API_KEY" \
  -e DMI_OCEANOBS_API_KEY="$DMI_OCEANOBS_API_KEY" \
  -e DMI_LIGHTNING_API_KEY="$DMI_LIGHTNING_API_KEY" \
  ghcr.io/clemensv/real-time-sources-dmi-kafka:latest
```

### MQTT / UNS

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtts://broker.example.com:8883 \
  -e MQTT_USERNAME=alice \
  -e MQTT_PASSWORD=secret \
  -e DMI_METOBS_API_KEY="$DMI_METOBS_API_KEY" \
  -e DMI_OCEANOBS_API_KEY="$DMI_OCEANOBS_API_KEY" \
  ghcr.io/clemensv/real-time-sources-dmi-mqtt:latest
```

Topics published (retained, QoS 1):

```
weather/dk/dmi/met-obs/{station_id}/info
weather/dk/dmi/met-obs/{station_id}/{parameter_id}
ocean/dk/dmi/ocean-obs/{station_id}/info
ocean/dk/dmi/ocean-obs/{station_id}/{parameter_id}
ocean/dk/dmi/tidewater/{station_id}/info
ocean/dk/dmi/tidewater/{station_id}/prediction
```

### AMQP 1.0

```bash
docker run --rm \
  -e AMQP_BROKER_URL=amqps://broker.example.com:5671/dmi \
  -e DMI_METOBS_API_KEY="$DMI_METOBS_API_KEY" \
  -e DMI_OCEANOBS_API_KEY="$DMI_OCEANOBS_API_KEY" \
  -e DMI_LIGHTNING_API_KEY="$DMI_LIGHTNING_API_KEY" \
  ghcr.io/clemensv/real-time-sources-dmi-amqp:latest
```

For Azure Service Bus / Event Hubs with Microsoft Entra ID, set `AMQP_AUTH_MODE=entra`, `AMQP_HOST=<namespace>.servicebus.windows.net`, `AMQP_TLS=true`, and `AMQP_ADDRESS=dmi` (or your queue / event hub name).

## Configuration knobs

All three images share these upstream-side knobs:

* `POLLING_INTERVAL` — seconds between polling cycles (default `300`).
* `STATE_FILE` — path to the dedupe state file.
* `ONCE_MODE=true` — single cycle and exit.
* `DMI_OBSERVATION_PERIOD` — DMI period filter (default `latest-hour`).
* `DMI_REFERENCE_REFRESH_HOURS` — re-emit reference data every N hours
  (default `6`).

Transport-specific knobs are listed in [CONTAINER.md](CONTAINER.md).

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

DMI targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#dmi) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `dmi` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/dmi/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source dmi `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#dmi/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source dmi `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#dmi/fabric-aci)


### Deploying into Azure Container Instances

5 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, Azure Service Bus, or MQTT brokers. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template-with-eventhub.json)

#### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid namespace MQTT, etc.). You provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template-mqtt.json)

#### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space for this source, a user-assigned managed identity, and the **EventGrid TopicSpaces Publisher** role assignment. The feeder authenticates with MQTT v5 enhanced authentication (`OAUTH2-JWT`) — no shared keys to rotate.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template-with-eventgrid-mqtt.json)

#### AMQP — provision a new Azure Service Bus queue

Deploy the AMQP container together with a new Azure Service Bus namespace, queue, user-assigned managed identity, and the **Azure Service Bus Data Sender** role assignment. The feeder authenticates with Microsoft Entra ID over the AMQP CBS `$cbs` link — no SAS keys to mint in the runtime.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template-with-servicebus.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Upstream

* DMI Open Data Portal: <https://opendatadocs.dmi.govcloud.dk/>
* MetObs Bulk: <https://opendatadocs.dmi.govcloud.dk/APIs/MetObsAPI>
* OceanObs Bulk: <https://opendatadocs.dmi.govcloud.dk/APIs/OceanObsAPI>
* Lightning: <https://opendatadocs.dmi.govcloud.dk/APIs/LightningDataAPI>
* Data licence: [Creative Commons Attribution (CC BY 4.0)](https://www.dmi.dk/vejrarkiv/about-dmi/about-dmis-data/).
