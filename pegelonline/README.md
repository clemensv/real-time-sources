# PegelOnline feeder

This feeder turns the German [WSV PegelOnline](https://www.pegelonline.wsv.de/) REST API into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.

## Why this bridge

The German Federal Waterways and Shipping Administration (Wasserstraßen-
und Schifffahrtsverwaltung des Bundes, **WSV**) publishes
[PegelOnline](https://www.pegelonline.wsv.de/), the canonical real-time
water-level feed for every federally administered inland and coastal
gauge in Germany — over **1,200 stations** on rivers, canals and
estuaries including the Rhine, Elbe, Danube, Weser, Main, Mosel, Oder
and Kiel Canal. The data is free, open, and the authoritative source
that downstream consumers (flood agencies, ports, ship pilots,
hydropower operators, insurers) build on.

This bridge turns that REST API into a first-class real-time event
stream so you can stop polling REST endpoints from inside your
business systems and start subscribing to a topic:

- **Flood early warning and civil protection** — react to rising
  gauges within one polling cycle (default 60 s) across an entire
  river basin, drive alerts and dashboards.
- **Inland shipping operations** — Rhine, Mosel and Elbe cargo
  scheduling depends on minimum-fairway-depth thresholds at named
  gauges (Kaub, Maxau, Emmerich, …); stream the values directly into
  voyage-planning, ETA prediction and demurrage workflows.
- **Hydropower and water-management dispatch** — bid into intraday
  electricity markets with up-to-the-minute headwater and tailwater
  readings; feed real-time inflows into reservoir-control SCADA.
- **Environmental compliance and research** — long-running, dedupe-
  aware ingestion into Microsoft Fabric Eventhouse / Azure Data
  Explorer / a data lake for low-flow analysis, climate-impact studies
  and statutory reporting.
- **Insurance and risk** — drive parametric flood triggers and live
  exposure dashboards from the same feed the public authorities use.

The bridge does the boring work — REST polling with ETag awareness,
state-file dedupe, JSON-Structure–validated CloudEvents, identity
plumbing, retries — so the consumer just subscribes.

## Overview

**PegelOnline** is a bridge that polls the German WSV PegelOnline REST API
and re-emits both the station catalog and the live water-level measurements
as CloudEvents. The source ships in three transport variants from a single
upstream poller:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-pegelonline-kafka` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `{station_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-pegelonline-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree under `hydro/de/wsv/pegelonline/{water}/{station}/...`, JSON body, CloudEvent attributes as MQTT 5 user properties, retained at QoS 1 |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-pegelonline-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | Single AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three variants share:

* The upstream poller (`pegelonline_core`).
* The xRegistry contract (`xreg/pegelonline.xreg.json`).
* The CloudEvents schemas for the `Station` reference event and the
  `CurrentMeasurement` telemetry event.

## Key features
- **Station catalog** emitted at startup as reference CloudEvents and
  refreshed periodically — consumers learn the universe of gauges
  without a separate metadata fetch.
- **Live water-level measurements** with ETag-aware polling and per-
  station dedupe state, so only genuinely new readings are republished.
- **Three transport binaries** with identical configuration knobs
  upstream (polling interval, state file, once-mode) — switch transport
  without changing the data model.
- **Azure Event Hubs / Microsoft Fabric Event Streams** ready via standard
  connection strings (Kafka variant).
- **Unified Namespace** ready out of the box with retained MQTT 5.0
  binary CloudEvents (MQTT variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra
  ID** (no SAS-key rotation) via the AMQP variant's CBS put-token flow,
  plus SAS-token CBS for the Service Bus emulator and SAS-only
  namespaces.

## Repository layout

```text
pegelonline/
  xreg/pegelonline.xreg.json     # shared xRegistry contract
  pegelonline_core/              # transport-agnostic poller
  pegelonline_kafka/             # Kafka feeder application
  pegelonline_mqtt/              # MQTT/UNS feeder application
  pegelonline_amqp/              # AMQP 1.0 feeder application
  pegelonline_producer/          # xRegistry-generated Kafka producer
  pegelonline_mqtt_producer/     # xRegistry-generated MQTT producer
  pegelonline_amqp_producer/     # xRegistry-generated AMQP producer
  Dockerfile.kafka               # builds the Kafka feeder image
  Dockerfile.mqtt                # builds the MQTT feeder image
  Dockerfile.amqp                # builds the AMQP feeder image
  tests/                         # unit + integration tests
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound HTTPS to `pegelonline.wsv.de` (the upstream REST API; no credentials required).
- Network access to your target Kafka broker, MQTT broker, or AMQP 1.0 peer.
- A writable host directory mounted into the container at `/state` to persist the dedupe state file across restarts. Without it, dedupe restarts cold on every container start, and "long-running, dedupe-aware ingestion" only holds for the lifetime of one container.

## Quick start with Docker

> [!IMPORTANT]
> Always mount a volume for `STATE_FILE`. The default path lives inside the container's home directory and is lost on restart, which silently disables cross-restart deduplication. The examples below mount the host directory `./state` into `/state` and point `STATE_FILE` at it.

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/pegelonline.json \
  -e CONNECTION_STRING="<event-hubs-connection-string>" \
  ghcr.io/clemensv/real-time-sources-pegelonline-kafka:latest
```

Replace `<event-hubs-connection-string>` with a connection string from your Azure Event Hubs namespace, Microsoft Fabric Event Stream custom endpoint, or any Kafka 2.x broker that accepts the same SASL-PLAIN-over-TLS shape.

### MQTT (Unified Namespace)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/pegelonline.json \
  -e MQTT_BROKER_URL=mqtts://<broker-host>:8883 \
  -e MQTT_USERNAME=<username> \
  -e MQTT_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-pegelonline-mqtt:latest
```

Topics published (retained, QoS 1):

```text
hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/info          # Station reference
hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/water-level   # CurrentMeasurement telemetry
```

### AMQP 1.0

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/pegelonline.json \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/pegelonline' \
  ghcr.io/clemensv/real-time-sources-pegelonline-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service Bus emulator, or SAS-only namespaces, see [CONTAINER.md](CONTAINER.md#using-the-amqp-image) for the full environment-variable matrix.

## Configuration reference

The complete list of environment variables for every variant (Kafka, MQTT, AMQP), every authentication mode (SASL PLAIN, Microsoft Entra ID via CBS or OAUTH2-JWT, SAS-token CBS), and every Azure deployment shape lives in [CONTAINER.md](CONTAINER.md). The runtime entry point for every image is `python -m pegelonline_{kafka,mqtt,amqp} feed`; the image's default `CMD` invokes it for you.

## Deploying into Microsoft Fabric

PegelOnline targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached Eventhouse / KQL database materializes the contract from [`kql/pegelonline.kql`](kql/pegelonline.kql), and the bundled 8-layer Fabric Map ([`fabric/`](fabric/README.md)) visualizes the live state of every gauge on a basemap with river geometry.

Two hosting models are supported. **Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources/#pegelonline)** to launch either; both deploy buttons walk you through the same Fabric workspace selection and follow-up steps.

### Fabric Notebook feeder (recommended for low-volume polling)

A scheduled Fabric Notebook ([`notebook/pegelonline-feed.ipynb`](notebook/pegelonline-feed.ipynb)) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `pegelonline` package and both generated producer sub-packages. The Event Stream custom endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/pegelonline/`.

Deploy with `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source pegelonline -WorkspaceId <id> -CapacityId <id>` (the portal button wraps this for you). Best fit for the default 60-second polling cadence; the notebook executes on a Fabric schedule (default every 5 minutes) and writes a per-run diagnostic log to OneLake.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#pegelonline/fabric-notebook)

### Fabric ACI feeder (recommended for high-volume / always-on)

A long-running Azure Container Instance hosts one of the three container images and writes into the same Fabric Event Stream custom endpoint. Use this when you want continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit the notebook scheduling model.

Deploy with `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source pegelonline -WorkspaceId <id> -CapacityId <id>` (the portal button wraps this for you). The script creates the Eventhouse, the KQL database with the [`kql/pegelonline.kql`](kql/pegelonline.kql) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#pegelonline/fabric-aci)

### Fabric Map visualization (optional, post-deploy)

After either hosting model has events flowing, run [`fabric/post-deploy.ps1`](fabric/README.md) (or `tools/deploy-fabric/deploy-fabric.ps1 -Source pegelonline`) to ingest the curated river geometry into the `RiverSegments` table and wire the 8 Kusto-backed layers (hydrological state, navigation state, 1h/3h/6h/24h trend, data freshness, station labels) onto a blank Fabric Map item. The map updates live as new measurements arrive.

## Deploying into Azure Container Instances

Five one-click deployment templates are available — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event
Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace
(Standard SKU, 1 throughput unit) and event hub. The connection string
is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker. You
provide the `mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new
[Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview)
with the MQTT broker enabled, a topic space rooted at `hydro/#`, a
user-assigned managed identity, and the **EventGrid TopicSpaces
Publisher** role assignment. The feeder authenticates with MQTT v5
enhanced authentication (`OAUTH2-JWT`).

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new
[Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview)
with a queue named `pegelonline`, a user-assigned managed identity, and
the **Azure Service Bus Data Sender** role assignment. The feeder
authenticates via AMQP CBS put-token with Microsoft Entra ID — no SAS
key rotation required.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-servicebus.json)

## Next steps

- Pick a hosting model: a [Fabric Notebook or Fabric ACI feeder](#deploying-into-microsoft-fabric) if your destination is a Fabric workspace; a [direct Azure deployment](#deploying-into-azure-container-instances) if you target Event Hubs, an MQTT broker, or AMQP without Fabric.
- Review the [event contract and schemas](EVENTS.md) before writing a consumer.
- Look up authentication modes and the full environment-variable matrix in [CONTAINER.md](CONTAINER.md).
- The upstream API surface, terms of use, and station coverage are documented at the [WSV PegelOnline portal](https://www.pegelonline.wsv.de/).
