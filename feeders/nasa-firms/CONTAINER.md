<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<div style="font-size:48px">🌍</div>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# NASA FIRMS

<sub>global active-fire detections · Kafka · MQTT · AMQP · <a href="https://firms.modaps.eosdis.nasa.gov/">upstream</a> · <a href="https://firms.modaps.eosdis.nasa.gov/api/area/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-ACI_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_Map_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — active fires for OSINT and situational awareness

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#nasa-firms) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#nasa-firms/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/nasa-firms.kql) &nbsp;·&nbsp;
[🗺️ **Fabric Map**](fabric/README.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://firms.modaps.eosdis.nasa.gov/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI container images for the NASA FIRMS feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://firms.modaps.eosdis.nasa.gov/>
- API / data documentation: <https://firms.modaps.eosdis.nasa.gov/api/area/>
- Free map key: <https://firms.modaps.eosdis.nasa.gov/api/map_key/>

<!-- upstream-links:end -->

## Why this container

[NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) (Fire Information for Resource Management System) publishes global near-real-time active-fire detections from NASA LANCE / Earth Science Data Systems. The feed is a core OSINT and situational-awareness signal: analysts use sudden hotspots to track shelling, arson, burning infrastructure, and wildfire expansion; emergency responders, environmental teams, air-quality analysts, insurers, risk teams, and journalists use the same detections for live maps and incident timelines.

These container images handle the polling, free `MAP_KEY` authentication, source coverage reference events, dedupe state, and identity glue once, then re-emit the feed as **CloudEvents** on the messaging fabric of your choice. Consumers subscribe to a stable topic or UNS tree instead of polling the FIRMS area API from every downstream system.

## What ships in the box

This source ships three container images backed by the same upstream acquisition core and the same xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-nasa-firms-kafka` | Apache Kafka 2.x (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic `nasa-firms`, JSON CloudEvents (binary mode), key = `{source}/{record_id}` |
| `ghcr.io/clemensv/real-time-sources-nasa-firms-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace trees `geo/fire/firms/{source}/{confidence_level}/{tile}/detection` and `geo/fire/firms/{source}/availability`, CloudEvent attributes as MQTT 5 user properties |
| `ghcr.io/clemensv/real-time-sources-nasa-firms-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | One AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three images consume the FIRMS area API and re-emit two CloudEvent types in message group `NASA.FIRMS`:

* `NASA.FIRMS.DataAvailability` — per-source coverage-window reference event, emitted first each cycle.
* `NASA.FIRMS.FireDetection` — one VIIRS or MODIS active-fire detection per active-fire pixel.

The on-the-wire schemas live in [EVENTS.md](EVENTS.md). The container images work with any Apache Kafka–compatible server or service that supports TLS with SASL/PLAIN, any MQTT 5.0 broker, and any AMQP 1.0 peer matching the auth modes below.

## Database schemas and handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Microsoft Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md). NASA FIRMS also ships a [Fabric Map](fabric/README.md) that uses `kql/nasa-firms.kql` to render global hotspots and detections over a dark basemap.

## Image contract

All three images share the same operational contract:

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` |
| Default entry point | Kafka: `python -m nasa_firms feed`; MQTT: `python -m nasa_firms_mqtt`; AMQP: `python -m nasa_firms_amqp` |
| Default user | root (no `USER` directive) |
| Exposed ports | none — the feeder is an outbound publisher only |
| Health check | none defined; treat process liveness as health |
| Signals | terminates cleanly on `SIGTERM`; the polling loop flushes producers before exit |
| Persistent state | `FIRMS_LAST_POLLED_FILE` (default `/state/nasa-firms.json`). **Mount a volume** to keep dedupe state across restarts. |
| Image tags | `:latest` tracks the default branch; immutable tags `:v<MAJOR>.<MINOR>.<PATCH>` and `:sha-<git-sha>` are published per release. |

Pull and inspect available tags at <https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-nasa-firms>.

## Installing the container images

Pull the container images from the GitHub Container Registry:

```bash
docker pull ghcr.io/clemensv/real-time-sources-nasa-firms-kafka:latest
docker pull ghcr.io/clemensv/real-time-sources-nasa-firms-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-nasa-firms-amqp:latest
```

## Using the Kafka image

The Kafka image (`…-nasa-firms-kafka`) reads data from the NASA FIRMS area API and writes JSON CloudEvents (binary mode) to the `nasa-firms` Kafka topic. It works with Apache Kafka 2.x, Azure Event Hubs, and Microsoft Fabric Event Streams.

### With a Kafka broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication, or set `KAFKA_ENABLE_TLS=false` for a plaintext broker. Run the container with the following command:

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e FIRMS_MAP_KEY='<free-earthdata-map-key>' \
    -e FIRMS_LAST_POLLED_FILE=/state/nasa-firms.json \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='nasa-firms' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-nasa-firms-kafka:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, the Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e FIRMS_MAP_KEY='<free-earthdata-map-key>' \
    -e FIRMS_LAST_POLLED_FILE=/state/nasa-firms.json \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-nasa-firms-kafka:latest
```

For local Kafka or Docker E2E style runs, the connection-string form is also accepted:

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e FIRMS_MAP_KEY='<free-earthdata-map-key>' \
    -e FIRMS_LAST_POLLED_FILE=/state/nasa-firms.json \
    -e CONNECTION_STRING='BootstrapServer=host.docker.internal:9092;EntityPath=nasa-firms' \
    -e KAFKA_ENABLE_TLS=false \
    ghcr.io/clemensv/real-time-sources-nasa-firms-kafka:latest
```

## Using the MQTT image

The MQTT image (`…-nasa-firms-mqtt`) publishes MQTT 5.0 binary-mode CloudEvents into Unified-Namespace topic trees:

- `geo/fire/firms/{source}/{confidence_level}/{tile}/detection`
- `geo/fire/firms/{source}/availability`

It works against any MQTT 5 broker (Mosquitto, EMQX, HiveMQ, …) and against the [Azure Event Grid namespace MQTT broker](https://learn.microsoft.com/azure/event-grid/mqtt-overview), including the integrated Microsoft Fabric MQTT source.

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e FIRMS_MAP_KEY='<free-earthdata-map-key>' \
    -e FIRMS_LAST_POLLED_FILE=/state/nasa-firms.json \
    -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-nasa-firms-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

When the host is an Azure VM, Container Instance, App Service, etc. with a managed identity that holds the **EventGrid TopicSpaces Publisher** role on the target topic space, the feeder uses MQTT v5 enhanced authentication (`OAUTH2-JWT`) to authenticate with a token issued for audience `https://eventgrid.azure.net/`.

> [!IMPORTANT]
> `MQTT_CLIENT_ID` must be globally unique across all clients connected to the same broker. Azure Event Grid disconnects an existing session when a second client connects with the same identifier ("subscription steal"). Use a deterministic but unique value (for example a hostname-plus-suffix) per deployed feeder instance.

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e FIRMS_MAP_KEY='<free-earthdata-map-key>' \
    -e FIRMS_LAST_POLLED_FILE=/state/nasa-firms.json \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    ghcr.io/clemensv/real-time-sources-nasa-firms-mqtt:latest
```

## Using the AMQP image

The AMQP image (`…-nasa-firms-amqp`) publishes CloudEvents over AMQP 1.0 to a single AMQP node (queue, topic, or address). It targets three deployment shapes:

### Generic AMQP 1.0 brokers (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch)

Use SASL PLAIN with a connection URL:

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e FIRMS_MAP_KEY='<free-earthdata-map-key>' \
    -e FIRMS_LAST_POLLED_FILE=/state/nasa-firms.json \
    -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/nasa-firms' \
    ghcr.io/clemensv/real-time-sources-nasa-firms-amqp:latest
```

For TLS-enabled brokers use `amqps://<broker-host>:5671/<address>`.

### Azure Service Bus / Event Hubs (Microsoft Entra ID, no SAS keys)

> [!IMPORTANT]
> For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`. Port 5672 is only valid against the local Service Bus emulator.

Run the image with `AMQP_AUTH_MODE=entra` against a user-assigned managed identity. The identity must hold the **Azure Service Bus Data Sender** role (or **Azure Event Hubs Data Sender** for Event Hubs) on the target queue or hub:

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e FIRMS_MAP_KEY='<free-earthdata-map-key>' \
    -e FIRMS_LAST_POLLED_FILE=/state/nasa-firms.json \
    -e AMQP_HOST='<namespace>.servicebus.windows.net' \
    -e AMQP_PORT=5671 -e AMQP_TLS=true \
    -e AMQP_ADDRESS='nasa-firms' \
    -e AMQP_AUTH_MODE=entra \
    -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
    -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    ghcr.io/clemensv/real-time-sources-nasa-firms-amqp:latest
```

The bridge mints an Entra ID access token via `DefaultAzureCredential` and hands it to the broker through the AMQP CBS (Claims-Based Security) put-token control link — no SAS-key rotation required.

### Azure Service Bus emulator / SAS-only namespaces (SAS-token CBS)

For local development against the [Azure Service Bus emulator](https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator) or for Service Bus / Event Hubs namespaces still configured for SAS authentication (no Entra ID), use `AMQP_AUTH_MODE=sas`. The bridge mints a `SharedAccessSignature` token from the key and key-name and presents it via AMQP CBS (`type=servicebus.windows.net:sastoken`):

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e FIRMS_MAP_KEY='<free-earthdata-map-key>' \
    -e FIRMS_LAST_POLLED_FILE=/state/nasa-firms.json \
    -e AMQP_HOST='servicebus-emulator' \
    -e AMQP_PORT=5672 \
    -e AMQP_ADDRESS='nasa-firms' \
    -e AMQP_AUTH_MODE=sas \
    -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
    -e AMQP_SAS_KEY='<sas-key>' \
    ghcr.io/clemensv/real-time-sources-nasa-firms-amqp:latest
```

For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`.

## Environment variables

### Common source runtime variables

| Variable | Description |
|---|---|
| `FIRMS_MAP_KEY` | **Required.** Free NASA Earthdata FIRMS map key from <https://firms.modaps.eosdis.nasa.gov/api/map_key/>. |
| `FIRMS_SOURCES` | Comma-separated FIRMS source ids. Default: `VIIRS_SNPP_NRT,VIIRS_NOAA20_NRT,VIIRS_NOAA21_NRT,MODIS_NRT`. |
| `FIRMS_DAY_RANGE` | FIRMS day range to request, from `1` to `10`. Default: `1`. |
| `POLLING_INTERVAL` | Seconds between polling cycles. Default: `900` (15 minutes). |
| `FIRMS_LAST_POLLED_FILE` | Path to persisted dedupe/checkpoint state. Default: `/state/nasa-firms.json`. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. The runtime also supports `--once`. |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, or `ERROR`. Default: `INFO`. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream–style connection string, or `BootstrapServer=host:port;EntityPath=topic` for plain Kafka. Supersedes individual Kafka settings. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of Kafka brokers. |
| `KAFKA_TOPIC` | Target Kafka topic. Default topic is `nasa-firms`. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS; default is `true`. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional credentials when `MQTT_AUTH_MODE=password` (default). |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra JWT. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id; otherwise `DefaultAzureCredential` selection applies. |
| `MQTT_CLIENT_ID` | MQTT client identifier. Must be unique per broker. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, e.g. `amqp://user:pw@host:5672/address` or `amqps://host:5671/address`. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL` (default port 5672, or 5671 with `AMQP_TLS=true`). |
| `AMQP_ADDRESS` | AMQP node (queue / topic) name. Default: `nasa-firms`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS (Service Bus / Event Hubs), or `sas` for SAS-token CBS (Service Bus emulator, or SAS-only namespaces). |
| `AMQP_ENTRA_AUDIENCE` | Token audience (default `https://servicebus.azure.net/.default`). Use `https://eventhubs.azure.net/.default` for Event Hubs. Used only when `AMQP_AUTH_MODE=entra`. |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id; otherwise `DefaultAzureCredential` selection applies. Used only when `AMQP_AUTH_MODE=entra`. |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name (e.g. `RootManageSharedAccessKey`). **Required when `AMQP_AUTH_MODE=sas`.** |
| `AMQP_SAS_KEY` | SAS key value (base64-encoded shared secret). **Required when `AMQP_AUTH_MODE=sas`.** |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |

## Deploying into Microsoft Fabric

NASA FIRMS ships both a poll-based Fabric Notebook feeder and a Fabric **Map**. Events land in a Fabric Event Stream custom endpoint, the generated [`kql/nasa-firms.kql`](kql/nasa-firms.kql) script materializes typed Eventhouse tables and materialized views, and [`fabric/`](fabric/README.md) adds the OSINT global fire map.

### Fabric Notebook feeder

Use `tools/deploy-fabric/deploy-feeder-notebook.ps1` to deploy the notebook in `notebook/`, bind Event Stream/Lakehouse/KQL assets, build the per-source Fabric Environment, and schedule poll runs. The notebook looks up the Event Stream connection string at runtime via the public Fabric Topology API and writes diagnostic state to OneLake.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source nasa-firms `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#nasa-firms/fabric-notebook)

### Fabric ACI feeder

Use `tools/deploy-fabric/deploy-fabric-aci.ps1` for always-on container hosting that publishes to Fabric Event Streams. This is the preferred Fabric route for the MQTT and AMQP variants, and for continuous container operation.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source nasa-firms `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#nasa-firms/fabric-aci)

### Fabric Map visualization

After either hosting model has events flowing, run [`fabric/post-deploy.ps1`](fabric/README.md) or the generic Fabric deployer to provision the **NASA FIRMS Global Fire Map**. The map uses a dark global basemap, a fire-hotspot bubble layer, an individual fire-detection bubble layer, and an FRP heat ramp.

## Deploying into Azure Container Instances

Azure Container Instance templates are available for the Kafka, MQTT, and AMQP transport families. The templates host the container directly in Azure and create a storage account and file share for persistent dedupe state.

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string. The template creates a storage account and file share for persistent state and prompts for `FIRMS_MAP_KEY`.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnasa-firms%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace and event hub. The connection string is wired automatically; provide `FIRMS_MAP_KEY` at deployment time.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnasa-firms%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker. You provide the `mqtts://` URL, optional credentials, and `FIRMS_MAP_KEY`.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnasa-firms%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview) with the MQTT broker enabled, a topic space rooted for the FIRMS UNS tree, a user-assigned managed identity, and a role assignment granting the identity the **EventGrid TopicSpaces Publisher** role. The feeder authenticates to the broker using MQTT v5 enhanced authentication (`OAUTH2-JWT`) with tokens minted by the managed identity for audience `https://eventgrid.azure.net/`.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnasa-firms%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP 1.0 — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue named `nasa-firms`, a user-assigned managed identity, and a role assignment granting the identity the **Azure Service Bus Data Sender** role on the queue. The feeder authenticates to the broker using AMQP 1.0 claims-based security (CBS) with tokens minted by the managed identity for audience `https://servicebus.azure.net/`. Works the same way against an Event Hubs namespace by changing the audience and endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnasa-firms%2Fazure-template-with-servicebus.json)

### AMQP 1.0 — bring your own peer

Deploy the AMQP container against an existing AMQP 1.0 peer. You provide the broker URL, optional credentials, and `FIRMS_MAP_KEY`.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnasa-firms%2Fazure-template-amqp.json)

## Related

- [README.md](README.md) — project overview, audience, and one-paragraph operational summary.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, per-transport routing, and example payloads.
- [`xreg/nasa-firms.xreg.json`](xreg/nasa-firms.xreg.json) — the xRegistry manifest the producers and EVENTS.md are derived from.
- [`kql/nasa-firms.kql`](kql/nasa-firms.kql) — Fabric Eventhouse / ADX table, mapping, update-policy, and materialized-view script.
- [`fabric/README.md`](fabric/README.md) — Fabric Map design and post-deploy hook.
