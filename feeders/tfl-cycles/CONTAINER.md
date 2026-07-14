<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/gb.png" alt="United Kingdom" width="64" height="48"><br>
<sub><b>United Kingdom</b></sub>
</td>
<td valign="middle">

# TfL Santander Cycles

<sub>London public bikeshare, ~798 docking stations · Kafka · MQTT · AMQP · <a href="https://tfl.gov.uk/modes/cycling/santander-cycles">upstream</a> · <a href="https://api.tfl.gov.uk/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> United Kingdom — London Santander Cycles docking-station catalog and live availability

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#tfl-cycles) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#tfl-cycles/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/tfl-cycles.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://api.tfl.gov.uk/BikePoint)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI container images for the TfL Santander
Cycles feeder, their environment-variable contract, authentication modes, and
one-click Azure deployments. For the project overview see [README.md](README.md);
for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- BikePoint endpoint: <https://api.tfl.gov.uk/BikePoint>
- TfL Unified API: <https://api.tfl.gov.uk/>
- Santander Cycles: <https://tfl.gov.uk/modes/cycling/santander-cycles>
- Open data terms: <https://tfl.gov.uk/info-for/open-data-users/open-data-policy>

<!-- upstream-links:end -->

## Why this container

Transport for London (**TfL**) publishes the authoritative Santander Cycles
BikePoint feed for London docking stations through the TfL Unified API. The
feed is available anonymously, with an optional `TFL_APP_KEY` for higher rate
limits, but it is still a REST endpoint: every consumer ends up writing the
same polling, dedupe, schema-validation, retry and identity glue.

These container images do that work once and re-emit the feed as
**CloudEvents** on the messaging fabric of your choice — so micromobility
operators, city dashboards, journey planners, event operations, Fabric
Eventhouse / ADX users, and digital-twin teams can subscribe to a stream
instead of scraping `GET /BikePoint` from inside their business systems.

TfL Open Data attribution must be preserved by downstream applications:
**"Powered by TfL Open Data"**. TfL also notes that the open data contains
Ordnance Survey data © Crown copyright and database rights.

## What ships in the box

This source ships three container images backed by the same upstream poller and
the same xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-tfl-cycles-kafka` | Apache Kafka 2.x (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic `tfl-cycles`, CloudEvents, key = `{station_id}` |
| `ghcr.io/clemensv/real-time-sources-tfl-cycles-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace topic tree `mobility/tfl-cycles/{station_id}/{info|status}`, binary CloudEvents as MQTT 5 user properties |
| `ghcr.io/clemensv/real-time-sources-tfl-cycles-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | One AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three images consume the TfL Unified API BikePoint resource and re-emit two
CloudEvent types:

* `UK.Gov.TfL.Cycles.StationInformation` — docking-station reference data
  (identity, location, capacity, lifecycle), emitted first each cycle and
  retained on MQTT.
* `UK.Gov.TfL.Cycles.StationStatus` — live bike and dock availability telemetry.

The on-the-wire schemas live in [EVENTS.md](EVENTS.md). `StationInformation`
is emitted into the same topic/address/tree as telemetry so consumers get a
temporally consistent station catalog without making a side call to the TfL API.

## Database schemas and handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Microsoft Fabric Eventhouse and Azure Data
Explorer is described in [DATABASE.md](../DATABASE.md). Apply the generated
[`kql/tfl-cycles.kql`](kql/tfl-cycles.kql) script before wiring consumers to
typed KQL tables and latest-state views.

## Image contract

All three images share the same operational contract:

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` |
| Default entry point | `python -m tfl_cycles feed`, `python -m tfl_cycles_mqtt feed`, or `python -m tfl_cycles_amqp feed` |
| Default user | root (no `USER` directive) |
| Exposed ports | none — the feeder is an outbound publisher only |
| Health check | none defined; treat process liveness as health |
| Signals | terminates cleanly on `SIGTERM`; the polling loop flushes producers before exit |
| Persistent state | `STATE_FILE` (default `~/.tfl_cycles_state.json` inside the container). **Mount a volume** to keep dedupe state across restarts. |
| Image tags | `:latest` tracks the default branch; immutable tags `:v<MAJOR>.<MINOR>.<PATCH>` and `:sha-<git-sha>` are published per release. |

Pull and inspect available tags at <https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-tfl-cycles-kafka>.

## Installing the container images

Pull the container images from the GitHub Container Registry:

```bash
docker pull ghcr.io/clemensv/real-time-sources-tfl-cycles-kafka:latest
docker pull ghcr.io/clemensv/real-time-sources-tfl-cycles-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-tfl-cycles-amqp:latest
```

## Using the Kafka image

The Kafka image (`…-tfl-cycles-kafka`) reads data from the TfL BikePoint API and
writes CloudEvents to a Kafka topic. It works with Apache Kafka 2.x, Azure
Event Hubs, and Microsoft Fabric Event Streams.

### With a Kafka broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e STATE_FILE=/state/tfl-cycles.json \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='tfl-cycles' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e TFL_APP_KEY='<optional-tfl-app-key>' \
    ghcr.io/clemensv/real-time-sources-tfl-cycles-kafka:latest
```

For local plaintext brokers, add `-e KAFKA_ENABLE_TLS=false`.

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the
connection string from the Azure portal, the Azure CLI, or the "custom endpoint"
of a Fabric Event Stream.

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e STATE_FILE=/state/tfl-cycles.json \
    -e CONNECTION_STRING='<connection-string>' \
    -e TFL_APP_KEY='<optional-tfl-app-key>' \
    ghcr.io/clemensv/real-time-sources-tfl-cycles-kafka:latest
```

## Using the MQTT image

The MQTT image (`…-tfl-cycles-mqtt`) publishes MQTT 5.0 binary-mode CloudEvents
into a Unified-Namespace topic tree
(`mobility/tfl-cycles/{station_id}/{info|status}`). It works against any MQTT 5
broker (Mosquitto, EMQX, HiveMQ, …) and against the [Azure Event Grid namespace
MQTT broker](https://learn.microsoft.com/azure/event-grid/mqtt-overview),
including the integrated Microsoft Fabric Real-Time Hub MQTT source.

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e STATE_FILE=/state/tfl-cycles.json \
    -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
    -e MQTT_AUTH_MODE=password \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    -e TFL_APP_KEY='<optional-tfl-app-key>' \
    ghcr.io/clemensv/real-time-sources-tfl-cycles-mqtt:latest
```

Use `mqtt://<broker-host>:1883` for a plaintext broker, or set
`MQTT_HOST`, `MQTT_PORT`, and `MQTT_TLS` separately.

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

When the host is an Azure VM, Container Instance, App Service, etc. with a
managed identity that holds the **EventGrid TopicSpaces Publisher** role on the
target topic space, the feeder uses MQTT v5 enhanced authentication
(`OAUTH2-JWT`) to authenticate with a token issued for audience
`https://eventgrid.azure.net/`.

> [!IMPORTANT]
> `MQTT_CLIENT_ID` must be globally unique across all clients connected to the
> same broker. Azure Event Grid disconnects an existing session when a second
> client connects with the same identifier ("subscription steal"). Use a
> deterministic but unique value per deployed feeder instance.

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e STATE_FILE=/state/tfl-cycles.json \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    -e TFL_APP_KEY='<optional-tfl-app-key>' \
    ghcr.io/clemensv/real-time-sources-tfl-cycles-mqtt:latest
```

## Using the AMQP image

The AMQP image (`…-tfl-cycles-amqp`) publishes CloudEvents over AMQP 1.0 to a
single AMQP node (queue, topic, or address). It targets three deployment
shapes:

### Generic AMQP 1.0 brokers (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch)

Use SASL PLAIN with a connection URL:

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e STATE_FILE=/state/tfl-cycles.json \
    -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/tfl-cycles' \
    -e TFL_APP_KEY='<optional-tfl-app-key>' \
    ghcr.io/clemensv/real-time-sources-tfl-cycles-amqp:latest
```

For TLS-enabled brokers use `amqps://<broker-host>:5671/<address>`.

### Azure Service Bus / Event Hubs (Microsoft Entra ID, no SAS keys)

> [!IMPORTANT]
> For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`. Port
> 5672 is only valid against the local Service Bus emulator.

Run the image with `AMQP_AUTH_MODE=entra` against a user-assigned managed
identity. The identity must hold the **Azure Service Bus Data Sender** role (or
**Azure Event Hubs Data Sender** for Event Hubs) on the target queue or hub:

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e STATE_FILE=/state/tfl-cycles.json \
    -e AMQP_HOST='<namespace>.servicebus.windows.net' \
    -e AMQP_PORT=5671 -e AMQP_TLS=true \
    -e AMQP_ADDRESS='tfl-cycles' \
    -e AMQP_AUTH_MODE=entra \
    -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
    -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e TFL_APP_KEY='<optional-tfl-app-key>' \
    ghcr.io/clemensv/real-time-sources-tfl-cycles-amqp:latest
```

The bridge mints an Entra ID access token via `DefaultAzureCredential` and hands
it to the broker through the AMQP CBS (Claims-Based Security) put-token control
link — no SAS-key rotation required. Use
`AMQP_ENTRA_AUDIENCE=https://eventhubs.azure.net/.default` for Event Hubs.

### Azure Service Bus emulator / SAS-only namespaces (SAS-token CBS)

For local development against the [Azure Service Bus emulator](https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator)
or for Service Bus / Event Hubs namespaces still configured for SAS
authentication (no Entra ID), use `AMQP_AUTH_MODE=sas`. The bridge mints a
`SharedAccessSignature` token from the key and key-name and presents it via
AMQP CBS (`type=servicebus.windows.net:sastoken`):

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e STATE_FILE=/state/tfl-cycles.json \
    -e AMQP_HOST='servicebus-emulator' \
    -e AMQP_PORT=5672 \
    -e AMQP_ADDRESS='tfl-cycles' \
    -e AMQP_AUTH_MODE=sas \
    -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
    -e AMQP_SAS_KEY='<sas-key>' \
    -e TFL_APP_KEY='<optional-tfl-app-key>' \
    ghcr.io/clemensv/real-time-sources-tfl-cycles-amqp:latest
```

For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`.

## Environment variables

### Common (all images)

| Variable | Description |
|---|---|
| `TFL_APP_KEY` | Optional TfL Unified API application key. Anonymous access works, but an app key raises rate limits. |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `60`). |
| `REFERENCE_REFRESH_INTERVAL` | Seconds between full re-emissions of station reference data (default `3600`). |
| `STATE_FILE` | Path to the dedupe state file (default `~/.tfl_cycles_state.json`). Mount a persistent volume here. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. |
| `USER_AGENT` | HTTP `User-Agent` header sent to TfL. Operators can override the entire string. |
| `USER_AGENT_CONTACT` | Contact token embedded in the default `User-Agent`. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream–style connection string, or `BootstrapServer=...;EntityPath=...`. Supersedes `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, `SASL_PASSWORD` when present. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of Kafka brokers. Required when `CONNECTION_STRING` is not set. |
| `KAFKA_TOPIC` | Target Kafka topic. Required when no `EntityPath` is present in `CONNECTION_STRING`. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `60`). |
| `REFERENCE_REFRESH_INTERVAL` | Seconds between full reference-data re-emissions (default `3600`). |
| `STATE_FILE` | Path to the dedupe state file. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`; default port is 1883, or 8883 with TLS. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional credentials when `MQTT_AUTH_MODE=password` (default). |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra JWT. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id; otherwise `DefaultAzureCredential` selection applies. |
| `MQTT_CLIENT_ID` | MQTT client identifier. Use a unique value for each deployed instance. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `60`). |
| `REFERENCE_REFRESH_INTERVAL` | Seconds between full reference-data re-emissions (default `3600`). |
| `STATE_FILE` | Path to the dedupe state file. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, e.g. `amqp://user:pw@host:5672/address` or `amqps://host:5671/address`. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL` (default port 5672, or 5671 with `AMQP_TLS=true`). |
| `AMQP_ADDRESS` | AMQP node (queue / topic) name (default `tfl-cycles`). |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS (Service Bus / Event Hubs), or `sas` for SAS-token CBS (Service Bus emulator, or SAS-only namespaces). |
| `AMQP_ENTRA_AUDIENCE` | Token audience (default `https://servicebus.azure.net/.default`). Use `https://eventhubs.azure.net/.default` for Event Hubs. Used only when `AMQP_AUTH_MODE=entra`. |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id; otherwise `DefaultAzureCredential` selection applies. Used only when `AMQP_AUTH_MODE=entra`. |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name (e.g. `RootManageSharedAccessKey`). **Required when `AMQP_AUTH_MODE=sas`.** |
| `AMQP_SAS_KEY` | SAS key value (base64-encoded shared secret). **Required when `AMQP_AUTH_MODE=sas`.** |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `60`). |
| `REFERENCE_REFRESH_INTERVAL` | Seconds between full reference-data re-emissions (default `3600`). |
| `STATE_FILE` | Path to the dedupe state file. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. |

## Deploying into Microsoft Fabric

### Fabric Notebook feeder

Poll-based sources in this repo ship a notebook-hosting option. A scheduled
Fabric Notebook in [`notebook/tfl-cycles-feed.ipynb`](notebook/tfl-cycles-feed.ipynb)
runs one polling cycle in the Fabric workspace, resolves the Event Stream
custom-endpoint connection string at runtime via the public Topology API, and
writes diagnostics to `/lakehouse/default/Files/feeder-state/tfl-cycles/last-run.log`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source tfl-cycles `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#tfl-cycles/fabric-notebook)

### Fabric ACI feeder

Use the always-on container path for continuous polling, or for MQTT and AMQP
targets that do not fit a scheduled notebook.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source tfl-cycles `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#tfl-cycles/fabric-aci)

## Deploying into Azure Container Instances

Five one-click deployment templates are available — one per realistic Azure
target. All templates create a storage account and file share for persistent
dedupe state.

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream
connection string. The template creates a storage account and file share for
persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftfl-cycles%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard
SKU, 1 throughput unit) and event hub. The connection string is wired
automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftfl-cycles%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker. You provide the
`mqtts://` URL and optional credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftfl-cycles%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with a new [Azure Event Grid namespace](https://learn.microsoft.com/azure/event-grid/mqtt-overview)
with the MQTT broker enabled, a topic space rooted at `mobility/tfl-cycles/#`,
a user-assigned managed identity, and a role assignment granting the identity
the **EventGrid TopicSpaces Publisher** role on the topic space. The feeder
authenticates to the broker using MQTT v5 enhanced authentication
(`OAUTH2-JWT`) with tokens minted by the managed identity for audience
`https://eventgrid.azure.net/`.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftfl-cycles%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP 1.0 — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview)
with a queue named `tfl-cycles`, a user-assigned managed identity, and a role
assignment granting the identity the **Azure Service Bus Data Sender** role on
the queue. The feeder authenticates to the broker using AMQP 1.0 claims-based
security (CBS) with tokens minted by the managed identity for audience
`https://servicebus.azure.net/`. Works the same way against an Event Hubs
namespace by changing the audience and endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftfl-cycles%2Fazure-template-with-servicebus.json)

## Related

- [README.md](README.md) — project overview, audience, and one-paragraph operational summary.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, per-transport routing, and example payloads.
- [`xreg/tfl-cycles.xreg.json`](xreg/tfl-cycles.xreg.json) — the xRegistry manifest the producers and EVENTS.md are derived from.
