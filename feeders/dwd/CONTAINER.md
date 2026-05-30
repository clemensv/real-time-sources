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

This document covers the published OCI container images for the DWD Open Data feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.dwd.de/>
- API / data documentation: <https://opendata.dwd.de/>

<!-- upstream-links:end -->

## Why this container

[Deutscher Wetterdienst (DWD)](https://opendata.dwd.de/) publishes weather-station observations, CAP alerts, radar product listings, and ICON-D2 forecast file metadata from a large open-data estate spanning station directories, ZIP bundles, alert archives, and rolling product trees. The data is free to use under GeoNutzV, but every production consumer otherwise ends up rebuilding the same state tracking, ZIP/file parsing, directory-diffing, dedupe, and schema-validation logic.

These container images do that work once and re-emit the DWD feed as **CloudEvents** on the messaging fabric of your choice — so national weather dashboards, infrastructure operators, hydrology and agriculture analytics stacks, radar/forecast processing pipelines, and public-sector data platforms can subscribe to a topic instead of polling DWD directly.

## What ships in the box

This source ships three container images backed by the same modular poller and the same xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-dwd` | Apache Kafka 2.x (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud, plain Kafka) | Four message-family topics (CDC, Weather, Radar, Forecast), JSON CloudEvents (binary mode), keys = `{station_id}`, `{identifier}`, `{file_url}` depending on family |
| `ghcr.io/clemensv/real-time-sources-dwd-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace topic branches for stations, alerts, radar products, and forecast catalogs/files; QoS 1 with retain enabled for reference / observation branches and disabled for alert / file-notification branches |
| `ghcr.io/clemensv/real-time-sources-dwd-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | One AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three images consume the same DWD modules and re-emit the same 13 CloudEvents types across four families. The on-the-wire schemas live in [EVENTS.md](EVENTS.md).

## Database schemas and handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Microsoft Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md). The KQL assets for DWD live in [`kql/dwd.kql`](kql/dwd.kql) and [`kql/icond2.kql`](kql/icond2.kql).

## Image contract

All three images share the same operational contract:

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` |
| Default entry point | `python -m dwd feed`, `python -m dwd_mqtt feed`, `python -m dwd_amqp feed` |
| Default user | root (no `USER` directive) |
| Exposed ports | none — the feeder is an outbound publisher only |
| Health check | none defined; treat process liveness as health |
| Signals | terminates cleanly on `SIGTERM`; the active poll cycle and downstream producer flush before exit |
| Persistent state | `STATE_FILE` stores last-seen station timestamps, seen alert identifiers, and watched directory metadata. If you do not persist it outside the container, restarts may replay recent observations, alerts, or file notifications. |
| Image tags | `:latest` tracks the default branch; immutable tags `:v<MAJOR>.<MINOR>.<PATCH>` and `:sha-<git-sha>` are published per release. |

Pull and inspect available tags at <https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-dwd>.

## Installing the container images

Pull the container images from the GitHub Container Registry:

```bash
docker pull ghcr.io/clemensv/real-time-sources-dwd:latest
docker pull ghcr.io/clemensv/real-time-sources-dwd-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-dwd-amqp:latest
```

## Using the Kafka image

The Kafka image (`…-dwd`) polls DWD and writes JSON CloudEvents (binary mode) to Kafka. It works with Apache Kafka 2.x, Azure Event Hubs, and Microsoft Fabric Event Streams.

### With a Kafka broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container with the following command:

```bash
docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-dwd:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, the Azure CLI, or the custom endpoint of a Fabric Event Stream.

```bash
docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-dwd:latest
```

### Selecting modules

Enable only the DWD modules you need:

```bash
docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e DWD_MODULES='station_metadata,station_obs_10min,weather_alerts' \
    ghcr.io/clemensv/real-time-sources-dwd:latest
```

## Using the MQTT image

The MQTT image (`…-dwd-mqtt`) publishes MQTT 5.0 CloudEvents into a Unified-Namespace tree at QoS 1. Retain behavior is family-specific: station, observation, and catalog topics are retained because they represent the latest known state; alert and file-notification topics are live-only because they represent change events.

It works against any MQTT 5 broker (Mosquitto, EMQX, HiveMQ, …) and against the [Azure Event Grid namespace MQTT broker](https://learn.microsoft.com/azure/event-grid/mqtt-overview), including the integrated [Microsoft Fabric Real-Time Hub MQTT source](https://learn.microsoft.com/fabric/real-time-hub/add-source-event-grid).

### Topic templates

```text
weather/de/dwd/dwd/{state}/{station_id}/info
weather/de/dwd/dwd/{state}/{station_id}/air-temperature-10min
alerts/de/dwd/dwd/{state}/{severity}/{identifier}/alert
weather/de/dwd/dwd/products/radar/{product_type}/{file_id}/file
weather/de/dwd/dwd/catalogs/{kind}/catalog
weather/de/dwd/dwd/products/icon-d2/{variable}/{file_id}/file
```

| Branch | Meaning |
|------|---------|
| `weather/de/dwd/dwd/{state}/{station_id}/...` | Station metadata and CDC observation families keyed by German state and station id. |
| `alerts/de/dwd/dwd/{state}/{severity}/{identifier}/alert` | CAP weather alerts keyed by alert identity and severity. |
| `weather/de/dwd/dwd/catalogs/{kind}/catalog` | Catalog/reference branches for radar and forecast model families. |
| `weather/de/dwd/dwd/products/radar/{product_type}/{file_id}/file` | Radar file notifications for newly discovered or updated DWD radar files. |
| `weather/de/dwd/dwd/products/icon-d2/{variable}/{file_id}/file` | ICON-D2 forecast file notifications keyed by variable and file id. |

`ContentType` is `application/json`; CloudEvents attributes ride as MQTT 5 user properties.

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-dwd-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

When the host is an Azure VM, Container Instance, App Service, etc. with a managed identity that holds the **EventGrid TopicSpaces Publisher** role on the target topic space, the feeder uses MQTT v5 enhanced authentication (`OAUTH2-JWT`) to authenticate with a token issued for audience `https://eventgrid.azure.net/`.

> [!IMPORTANT]
> `MQTT_CLIENT_ID` must be globally unique across all clients connected to the same broker. Azure Event Grid disconnects an existing session when a second client connects with the same identifier ("subscription steal"). Use a deterministic but unique value per deployed feeder instance.

```bash
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    ghcr.io/clemensv/real-time-sources-dwd-mqtt:latest
```

## Using the AMQP image

The AMQP image (`…-dwd-amqp`) publishes CloudEvents over AMQP 1.0 to a single AMQP node (queue, topic, or address). It targets two deployment shapes:

### Generic AMQP 1.0 brokers (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch)

Use SASL PLAIN with a connection URL:

```bash
docker run --rm \
    -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/dwd' \
    ghcr.io/clemensv/real-time-sources-dwd-amqp:latest
```

For TLS-enabled brokers use `amqps://<broker-host>:5671/<address>`.

### Azure Service Bus / Event Hubs (Microsoft Entra ID, no SAS keys)

> [!IMPORTANT]
> For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`. Port 5672 is only valid against the local Service Bus emulator.

Run the image with `AMQP_AUTH_MODE=entra` against a user-assigned managed identity. The identity must hold the **Azure Service Bus Data Sender** role (or **Azure Event Hubs Data Sender** for Event Hubs) on the target queue or hub:

```bash
docker run --rm \
    -e AMQP_HOST='<namespace>.servicebus.windows.net' \
    -e AMQP_PORT=5671 -e AMQP_TLS=true \
    -e AMQP_ADDRESS='dwd' \
    -e AMQP_AUTH_MODE=entra \
    -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
    -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    ghcr.io/clemensv/real-time-sources-dwd-amqp:latest
```

The bridge mints an Entra ID access token via `DefaultAzureCredential` and hands it to the broker through the AMQP CBS (Claims-Based Security) put-token control link — no SAS-key rotation required.

### Azure Service Bus emulator / SAS-only namespaces (SAS-token CBS)

For local development against the [Azure Service Bus emulator](https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator) or for Service Bus / Event Hubs namespaces still configured for SAS authentication (no Entra ID), use `AMQP_AUTH_MODE=sas`:

```bash
docker run --rm \
    -e AMQP_HOST='servicebus-emulator' \
    -e AMQP_PORT=5672 \
    -e AMQP_ADDRESS='dwd' \
    -e AMQP_AUTH_MODE=sas \
    -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
    -e AMQP_SAS_KEY='<sas-key>' \
    ghcr.io/clemensv/real-time-sources-dwd-amqp:latest
```

For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`.

## Environment variables

### Common (all images)

| Variable | Description |
|---|---|
| `STATE_FILE` | Path to the checkpoint file for DWD polling state. Default `~/.dwd_state.json`. |
| `POLLING_INTERVAL` | Optional global polling interval override in seconds. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream–style connection string. Supersedes `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, `SASL_PASSWORD`. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of TLS-enabled Kafka brokers. |
| `KAFKA_TOPIC` | Target Kafka topic or topic root used by the Kafka deployment shape. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |
| `DWD_MODULES` | Comma-separated module names to enable. |
| `DWD_MODULES_DISABLED` | Comma-separated module names to disable. |
| `DWD_10MIN_PARAMS` | Comma-separated 10-minute categories such as `air_temperature,precipitation,wind,solar`. |
| `DWD_STATIONS` | Comma-separated list of station ids to include. Default: all stations. |
| `DWD_BASE_URL` | Override URL for the upstream DWD opendata endpoint. Default `https://opendata.dwd.de`. |
| `DWD_MOCK` | `true` emits mock events for Docker E2E and smoke testing. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional credentials when `MQTT_AUTH_MODE=password` (default). |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra JWT. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id; otherwise `DefaultAzureCredential` selection applies. |
| `MQTT_CLIENT_ID` | MQTT client identifier (must be globally unique per broker). |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `DWD_MODULES` | Comma-separated module names to enable for the MQTT transport. |
| `DWD_MOCK` | `true` emits mock events for smoke testing. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, e.g. `amqp://user:pw@host:5672/address` or `amqps://host:5671/address`. Path overrides `AMQP_ADDRESS`. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL` (default port 5672, or 5671 with `AMQP_TLS=true`). |
| `AMQP_ADDRESS` | AMQP node (queue / topic) name (default `dwd`). |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS (Service Bus / Event Hubs), or `sas` for SAS-token CBS (Service Bus emulator, or SAS-only namespaces). |
| `AMQP_ENTRA_AUDIENCE` | Token audience (default `https://servicebus.azure.net/.default`). Use `https://eventhubs.azure.net/.default` for Event Hubs. Used only when `AMQP_AUTH_MODE=entra`. |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id; otherwise `DefaultAzureCredential` selection applies. Used only when `AMQP_AUTH_MODE=entra`. |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name (e.g. `RootManageSharedAccessKey`). **Required when `AMQP_AUTH_MODE=sas`.** |
| `AMQP_SAS_KEY` | SAS key value (base64-encoded shared secret). **Required when `AMQP_AUTH_MODE=sas`.** |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `DWD_MODULES` | Comma-separated module names to enable for the AMQP transport. |
| `DWD_MOCK` | `true` emits mock events for smoke testing. |

## Deploying into Azure Container Instances

Six one-click deployment templates are available — covering every Azure deployment shape checked into this source.

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdwd%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdwd%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

Deploy the MQTT container with your own MQTT broker.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdwd%2Fazure-template-mqtt.json)

### MQTT — provision Azure Event Grid namespace MQTT

Deploy the MQTT container together with an Azure Event Grid namespace for MQTT publishing.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdwd%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP 1.0 — bring your own broker

Deploy the AMQP container with your own AMQP 1.0 broker.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdwd%2Fazure-template-amqp.json)

### AMQP 1.0 — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with an address named `dwd`, a user-assigned managed identity, and a role assignment granting the identity the **Azure Service Bus Data Sender** role. The feeder authenticates to the broker using AMQP 1.0 claims-based security (CBS) with tokens minted by the managed identity for audience `https://servicebus.azure.net/`.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdwd%2Fazure-template-with-servicebus.json)

## Related

- [README.md](README.md) — project overview, audience, and one-paragraph operational summary.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, per-transport routing, and example payloads.
- [`xreg/dwd.xreg.json`](xreg/dwd.xreg.json) — the xRegistry manifest the producers and EVENTS.md are derived from.
