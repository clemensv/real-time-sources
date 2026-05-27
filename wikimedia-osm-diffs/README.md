<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# OpenStreetMap Diffs

<sub>OSM minutely replication diffs · Kafka · MQTT · AMQP · <a href="https://www.openstreetmap.org/">upstream</a> · <a href="https://wiki.openstreetmap.org/wiki/Planet.osm/diffs">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-2_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — OSM minutely replication diffs

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#wikimedia-osm-diffs) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#wikimedia-osm-diffs/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/wikimedia_osm_diffs.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.openstreetmap.org/)

</td></tr></table>
<!-- source-hero:end -->

This feeder turns the OpenStreetMap minutely replication feed into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), and AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.openstreetmap.org/>
- API / data documentation: <https://wiki.openstreetmap.org/wiki/Planet.osm/diffs>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published images, environment variables, and deployment options.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and routing details.

## Why this bridge

OSM minutely diffs are a high-volume global map-change stream used in geospatial monitoring and ETL pipelines. This feeder parses the feed and emits CloudEvents for downstream consumers.

Concrete consumer scenarios:

- **Operations dashboards** ingest the stream for near-real-time visibility without polling logic in every app.
- **Data engineering pipelines** land events in Eventhouse/Data Lake/Kafka topics with stable keys and schemas.
- **Alerting and automation** subscribe to the relevant event families and trigger downstream workflows.
- **Research and analytics teams** replay the same contract across historical and live windows.
- **Cross-domain correlation** joins these events with weather, traffic, or incident streams from sibling feeders.

## Overview

Tracks replication state, downloads minute diff files, parses OsmChange XML, and emits map-change and replication-state events.

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs` | Apache Kafka compatible (incl. Azure Event Hubs/Fabric Event Streams) | CloudEvents on one topic |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-mqtt` | MQTT 5.0 broker | CloudEvents with xRegistry topic mapping |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-amqp` | AMQP 1.0 broker / Service Bus | CloudEvents on one AMQP address |

All variants share:

- The same upstream acquisition logic and poll cadence.
- The same xRegistry contract and schema set.
- The same event identities and key/subject model across transports.

## Key features

- Shared contract and event schemas across Kafka, MQTT, and AMQP images.
- Container-first deployment model for Azure ACI and Fabric hosting.
- Dedupe/resume behavior for long-running ingestion.
- Source-specific event families are documented in [EVENTS.md](EVENTS.md).

## Repository layout

```text
wikimedia-osm-diffs/
  xreg/wikimedia_osm_diffs.xreg.json     # shared xRegistry contract
  wikimedia_osm_diffs/ # feeder runtime
  wikimedia_osm_diffs_amqp/ # AMQP feeder application
  wikimedia_osm_diffs_mqtt/ # MQTT feeder application
  wikimedia_osm_diffs_amqp_producer/ # generated producer package
  wikimedia_osm_diffs_mqtt_producer/ # generated producer package
  wikimedia_osm_diffs_producer/ # generated producer package
  kql/ # KQL schema scripts
  notebook/ # Fabric notebook feeder
  tests/ # unit + integration tests
  infra/ # feeder runtime
  Dockerfile                # builds the Kafka feeder image
  Dockerfile.mqtt                # builds the MQTT feeder image
  Dockerfile.amqp                # builds the AMQP feeder image
```

## Prerequisites

- Docker 20.10+.
- Outbound HTTPS access to the upstream source.
- Network access to your Kafka, MQTT, or AMQP destination.
- A writable `/state` mount for stateful polling deployments.

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs.json \
  -e CONNECTION_STRING="<event-hubs-or-kafka-connection-string>" \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs:latest
```

### MQTT

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs-mqtt.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-mqtt:latest
```

### AMQP

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e OSM_DIFFS_STATE_FILE=/state/wikimedia-osm-diffs-amqp.json \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/wikimedia-osm-diffs" \
  ghcr.io/clemensv/real-time-sources-wikimedia-osm-diffs-amqp:latest
```

## Configuration reference

Full per-transport environment-variable matrices live in [CONTAINER.md](CONTAINER.md).

State-file behavior: Kafka uses `OSM_DIFFS_STATE_FILE`; MQTT uses `OSM_DIFFS_STATE_FILE`; AMQP uses `OSM_DIFFS_STATE_FILE`.

## Data model

- `Org.OpenStreetMap.Diffs.MapChange` — element create/modify/delete
- `Org.OpenStreetMap.Diffs.ReplicationState` — replication-sequence checkpoints

<!-- source-deploy:begin -->
## Deploy

The portal buttons wrap the underlying scripts and ARM templates documented below; pick the path that matches your destination and operational preference. Every route lands in the same Eventhouse / KQL schema if you want one — they only differ in where the feeder container or notebook runs.

### Deploying into Microsoft Fabric

OpenStreetMap Diffs targets Microsoft Fabric end-to-end: events land in a Fabric **Event Stream** (custom endpoint), an attached **Eventhouse / KQL database** materializes the contract from [`kql/`](kql/).

Two hosting models are supported. Use the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources#wikimedia-osm-diffs) to launch either — both walk you through the same Fabric workspace selection and follow-up steps.

#### Fabric Notebook feeder &nbsp;<sub><i>(recommended for low-volume polling)</i></sub>

A scheduled Fabric Notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace itself, against a per-source Fabric **Environment** that bundles the `wikimedia_osm_diffs` package and the generated producer sub-packages. The Event Stream custom-endpoint connection string is looked up at runtime via the public Fabric Topology API using the workspace identity — no secrets in the notebook, no separate container host to manage. Dedupe state lives in OneLake under `/lakehouse/default/Files/feeder-state/wikimedia-osm-diffs/`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source wikimedia-osm-diffs `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

Best fit for poll-based sources whose update cadence aligns with scheduled execution; the notebook writes a per-run diagnostic log to OneLake on every run.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#wikimedia-osm-diffs/fabric-notebook)

#### Fabric ACI feeder &nbsp;<sub><i>(recommended for high-volume / always-on, and for MQTT or AMQP)</i></sub>

A long-running Azure Container Instance hosts the container image and writes into a Fabric Event Stream custom endpoint. Use this for continuous polling, real-time MQTT/UNS publishing, or the AMQP transport — anything that does not fit a scheduled-notebook model.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source wikimedia-osm-diffs `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

The script creates the Eventhouse, the KQL database with the [`kql/`](kql/) schema and update policies, the Event Stream with a custom endpoint, the ACI with the connection string wired in, and a storage account / file share mounted at `/state` for dedupe persistence.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#wikimedia-osm-diffs/fabric-aci)


### Deploying into Azure Container Instances

2 one-click deployment templates — one per realistic Azure target. These templates host the container directly in Azure (without a Fabric workspace) and target an Azure Event Hubs namespace, an MQTT broker, or an AMQP 1.0 peer. All templates create a storage account and file share for persistent dedupe state.

#### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. You pass the connection string at deploy time; the template provisions only the container and a storage account for persistent dedupe state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template.json)

#### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-osm-diffs%2Fazure-template-with-eventhub.json)


### Self-hosted

Pull and run any of the 3 container images directly — laptop, Kubernetes, Azure Container Apps, Cloud Run, ECS, bare metal. The full per-transport / per-auth-mode environment-variable matrix and sample `docker run` commands for every target broker live in [CONTAINER.md](CONTAINER.md).
<!-- source-deploy:end -->
## Next steps
- Review [EVENTS.md](EVENTS.md) before writing consumers.
- Use [CONTAINER.md](CONTAINER.md) for complete environment-variable and auth-mode details.
- Mount persistent state storage in production.
