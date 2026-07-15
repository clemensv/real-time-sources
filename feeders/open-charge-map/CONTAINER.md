<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# Open Charge Map

<sub>EV charging locations and reference data (requires free API key) · Kafka · MQTT · AMQP · <a href="https://openchargemap.org/">upstream</a> · <a href="https://openchargemap.org/site/develop/api">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — EV charging locations and reference data (requires free API key)

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#open-charge-map) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#open-charge-map/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/open-charge-map.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://openchargemap.org/)

</td></tr></table>
<!-- source-hero:end -->

# Open Charge Map container images

[README](README.md) - [Container contract](CONTAINER.md) - [Event schemas](EVENTS.md) - [Upstream](https://openchargemap.org/) - [API docs](https://openchargemap.org/site/develop/api)

This document covers the published OCI container images for the Open Charge Map feeder, their environment-variable contract, authentication modes, data-license obligations, and Azure / Fabric deployment paths. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://openchargemap.org/>
- API / developer documentation: <https://openchargemap.org/site/develop/api>
- API root: <https://api.openchargemap.io/v3/>
- Free API-key registration: <https://openchargemap.org/site/loginprovider/beginlogin>

<!-- upstream-links:end -->

## Why this container

Open Charge Map (OCM) is the largest global open registry of electric-vehicle charging locations, with 300,000+ points of interest maintained by the community, charging-network operators, national databases, and data providers. The v3 API is REST-shaped: every consumer otherwise needs to write the same API-key handling, `modifiedsince` watermarking, POI normalization, reference-table refresh, retries, and transport plumbing.

These container images do that work once and re-emit the registry as **CloudEvents** on the messaging fabric of your choice - so EV charging apps, fleet operations, city dashboards, energy-system digital twins, Fabric Eventhouse / ADX users, and open-data portals can subscribe to a stream instead of polling Open Charge Map directly from inside each business system.

> [!IMPORTANT]
> Open Charge Map requires attribution and share-alike handling for downstream reuse of its open data. The data is Open Charge Map open data / CC-BY-SA 4.0; the container image and feeder code are MIT-licensed under this repository. `OCM_OPENDATA=true` is the default and requests only openly licensed POIs.

## What ships in the box

This source ships three container images backed by the same upstream poller and the same xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-open-charge-map-kafka` | Apache Kafka 2.x (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic `open-charge-map`, CloudEvents, key = `{poi_id}` for locations or `{reference_type}/{reference_id}` for lookups |
| `ghcr.io/clemensv/real-time-sources-open-charge-map-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace topic tree `ev-charging/open-charge-map/location/{poi_id}` and `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`, binary CloudEvents as MQTT 5 user properties |
| `ghcr.io/clemensv/real-time-sources-open-charge-map-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | One AMQP node `open-charge-map`, binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three images consume two Open Charge Map v3 endpoints:

* `/v3/referencedata/` - nine global lookup tables, emitted reference-first at startup and refreshed daily by default.
* `/v3/poi/` - charging-location POIs, delta-polled with `modifiedsince` from the persisted `DateLastStatusUpdate` watermark.

The on-the-wire schemas live in [EVENTS.md](EVENTS.md). Reference events are emitted into the same topic/address/tree as telemetry so consumers get a temporally consistent operator, connector, country, status, and usage catalog without making a side call to `/v3/referencedata/`.

## Database schemas and handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Microsoft Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md). Apply the generated KQL script for this source when it is present in the worktree before wiring consumers to typed KQL tables and latest-state views.

## Image contract

All three images share the same operational contract:

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` |
| Default entry point | `python -m open_charge_map feed`, `python -m open_charge_map_mqtt feed`, or `python -m open_charge_map_amqp feed` |
| Default user | root (no `USER` directive) |
| Exposed ports | none - the feeder is an outbound publisher only |
| Health check | none defined; treat process liveness as health |
| Signals | terminates cleanly on `SIGTERM`; the polling loop flushes producers before exit |
| Persistent state | `STATE_FILE` (default `~/.open_charge_map_state.json` inside the container). **Mount a volume** to keep the watermark and dedupe state across restarts. |
| Image tags | `:latest` tracks the default branch; immutable tags `:v<MAJOR>.<MINOR>.<PATCH>` and `:sha-<git-sha>` are published per release. |

Pull and inspect available tags at <https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-open-charge-map-kafka>.

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-open-charge-map-kafka:latest
docker pull ghcr.io/clemensv/real-time-sources-open-charge-map-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-open-charge-map-amqp:latest
```

## Using the Kafka image

The Kafka image (`...-open-charge-map-kafka`) reads reference data and changed POIs from the Open Charge Map v3 API and writes CloudEvents to a Kafka topic. It works with Apache Kafka 2.x, Azure Event Hubs, and Microsoft Fabric Event Streams.

### With a Kafka broker

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e OPENCHARGEMAP_API_KEY='<ocm-api-key>' \
    -e STATE_FILE=/state/open-charge-map.json \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='open-charge-map' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-open-charge-map-kafka:latest
```

For local plaintext brokers, add `-e KAFKA_ENABLE_TLS=false`.

### With Azure Event Hubs or Fabric Event Streams

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e OPENCHARGEMAP_API_KEY='<ocm-api-key>' \
    -e STATE_FILE=/state/open-charge-map.json \
    -e CONNECTION_STRING='<connection-string-with-EntityPath-open-charge-map>' \
    ghcr.io/clemensv/real-time-sources-open-charge-map-kafka:latest
```

The Docker E2E harness also supports `CONNECTION_STRING=BootstrapServer=host:port;EntityPath=open-charge-map` with `KAFKA_ENABLE_TLS=false`.

## Using the MQTT image

The MQTT image (`...-open-charge-map-mqtt`) publishes MQTT 5.0 binary-mode CloudEvents into `ev-charging/open-charge-map/location/{poi_id}` and `ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`. It works against any MQTT 5 broker and against Azure Event Grid namespace MQTT.

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e OPENCHARGEMAP_API_KEY='<ocm-api-key>' \
    -e STATE_FILE=/state/open-charge-map.json \
    -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
    -e MQTT_AUTH_MODE=password \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-open-charge-map-mqtt:latest
```

Use `mqtt://<broker-host>:1883` for a plaintext broker, or set `MQTT_HOST`, `MQTT_PORT`, and `MQTT_TLS` separately.

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

> [!IMPORTANT]
> `MQTT_CLIENT_ID` must be globally unique across all clients connected to the same broker. Azure Event Grid disconnects an existing session when a second client connects with the same identifier ("subscription steal").

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e OPENCHARGEMAP_API_KEY='<ocm-api-key>' \
    -e STATE_FILE=/state/open-charge-map.json \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    ghcr.io/clemensv/real-time-sources-open-charge-map-mqtt:latest
```

## Using the AMQP image

The AMQP image (`...-open-charge-map-amqp`) publishes CloudEvents over AMQP 1.0 to a single AMQP node (queue, topic, or address).

### Generic AMQP 1.0 brokers (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch)

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e OPENCHARGEMAP_API_KEY='<ocm-api-key>' \
    -e STATE_FILE=/state/open-charge-map.json \
    -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/open-charge-map' \
    ghcr.io/clemensv/real-time-sources-open-charge-map-amqp:latest
```

For TLS-enabled brokers use `amqps://<broker-host>:5671/<address>`.

### Azure Service Bus / Event Hubs (Microsoft Entra ID, no SAS keys)

> [!IMPORTANT]
> For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`. Port 5672 is only valid against the local Service Bus emulator.

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e OPENCHARGEMAP_API_KEY='<ocm-api-key>' \
    -e STATE_FILE=/state/open-charge-map.json \
    -e AMQP_HOST='<namespace>.servicebus.windows.net' \
    -e AMQP_PORT=5671 -e AMQP_TLS=true \
    -e AMQP_ADDRESS='open-charge-map' \
    -e AMQP_AUTH_MODE=entra \
    -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
    -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    ghcr.io/clemensv/real-time-sources-open-charge-map-amqp:latest
```

Use `AMQP_ENTRA_AUDIENCE=https://eventhubs.azure.net/.default` for Event Hubs.

### Azure Service Bus emulator / SAS-only namespaces (SAS-token CBS)

```bash
docker run --rm \
    -v "$PWD/state:/state" \
    -e OPENCHARGEMAP_API_KEY='<ocm-api-key>' \
    -e STATE_FILE=/state/open-charge-map.json \
    -e AMQP_HOST='servicebus-emulator' \
    -e AMQP_PORT=5672 \
    -e AMQP_ADDRESS='open-charge-map' \
    -e AMQP_AUTH_MODE=sas \
    -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
    -e AMQP_SAS_KEY='<sas-key>' \
    ghcr.io/clemensv/real-time-sources-open-charge-map-amqp:latest
```

## Environment variables

### Common upstream and poller settings (all images)

| Variable | Required | Default | Description |
|---|---:|---|---|
| `OPENCHARGEMAP_API_KEY` | yes | none | Open Charge Map API key sent as the `X-API-Key` header. |
| `OCM_COUNTRYCODE` | no | unset (global) | Optional ISO country code such as `IE`, `DE`, or `US` passed as `/v3/poi/?countrycode=...`. Reference data is global. |
| `OCM_MODIFIED_SINCE_DAYS` | no | `1` | Cold-start look-back window in days when no persisted watermark exists. |
| `OCM_MAX_RESULTS` | no | `5000` | Maximum POI records requested per `/v3/poi/` poll (`maxresults`). |
| `OCM_OPENDATA` | no | `true` | Requests only openly licensed POIs. Set to `false`, `0`, or `no` to omit `opendata=true`. |
| `OCM_BASE_URL` | no | `https://api.openchargemap.io/v3/` | Override the Open Charge Map API root for tests or mirrors. |
| `POLLING_INTERVAL` | no | `600` | Seconds between POI delta-poll cycles. |
| `REFERENCE_REFRESH_INTERVAL` | no | `86400` | Seconds between full re-emissions of `/v3/referencedata/` lookup tables. |
| `STATE_FILE` | no | `~/.open_charge_map_state.json` | Path to the persisted watermark and POI change signatures. Mount a persistent volume here. |
| `ONCE_MODE` | no | `false` | `true`, `1`, or `yes` runs one reference + POI poll cycle and exits. |
| `USER_AGENT` | no | `real-time-sources-open-charge-map/0.1.0 (+https://github.com/clemensv/real-time-sources; <contact>)` | Full HTTP `User-Agent` header sent to Open Charge Map. |
| `USER_AGENT_CONTACT` | no | `clemensv@microsoft.com` | Contact token embedded in the default `USER_AGENT` when `USER_AGENT` is not set. |

### Kafka image

| Variable | Required | Default | Description |
|---|---:|---|---|
| `CONNECTION_STRING` | no | empty | Azure Event Hubs / Fabric Event Stream connection string, or local harness form `BootstrapServer=host:port;EntityPath=open-charge-map`. Supersedes explicit bootstrap / SASL settings when present. |
| `KAFKA_BOOTSTRAP_SERVERS` | required without `CONNECTION_STRING` | none | Comma-separated Kafka bootstrap servers. |
| `KAFKA_TOPIC` | required unless `CONNECTION_STRING` has `EntityPath` | none | Target Kafka topic; use `open-charge-map` for the checked-in contract. |
| `SASL_USERNAME` | no | none | SASL PLAIN username for explicit Kafka settings. |
| `SASL_PASSWORD` | no | none | SASL PLAIN password for explicit Kafka settings. |
| `KAFKA_ENABLE_TLS` | no | `true` | Set to `false`, `0`, or `no` for plaintext local brokers. |

### MQTT image

| Variable | Required | Default | Description |
|---|---:|---|---|
| `MQTT_BROKER_URL` | no | none | Broker URL, for example `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` | no | `localhost` when no URL is set | Broker hostname alternative to `MQTT_BROKER_URL`. |
| `MQTT_PORT` | no | `1883`, or `8883` with TLS | Broker port alternative to `MQTT_BROKER_URL`. |
| `MQTT_TLS` | no | `false` | `true`, `1`, or `yes` enables TLS. `MQTT_AUTH_MODE=entra` also uses TLS. |
| `MQTT_USERNAME` | no | URL username or none | Username for password authentication. |
| `MQTT_PASSWORD` | no | URL password or empty | Password for password authentication. |
| `MQTT_CLIENT_ID` | no | empty (broker assigns) | MQTT client identifier. Use a unique value for each deployed instance. |
| `MQTT_CONTENT_MODE` | no | `binary` | CloudEvents content mode: `binary` or `structured`. |
| `MQTT_AUTH_MODE` | no | `password` | `password` for username/password or anonymous brokers; `entra` for MQTT v5 enhanced auth with Microsoft Entra JWT. |
| `MQTT_ENTRA_AUDIENCE` | no | `https://eventgrid.azure.net/` | JWT audience used when `MQTT_AUTH_MODE=entra`. |
| `MQTT_ENTRA_CLIENT_ID` | no | none | Optional user-assigned managed identity client id; otherwise `DefaultAzureCredential` applies. |

### AMQP image

| Variable | Required | Default | Description |
|---|---:|---|---|
| `AMQP_BROKER_URL` | no | none | Broker URL, for example `amqp://user:pw@host:5672/address` or `amqps://host:5671/address`. |
| `AMQP_HOST` | no | `localhost` when no URL is set | Broker hostname alternative to `AMQP_BROKER_URL`. |
| `AMQP_PORT` | no | `5672`, or `5671` with TLS / Entra | Broker port alternative to `AMQP_BROKER_URL`. |
| `AMQP_TLS` | no | `false` | `true`, `1`, or `yes` enables TLS. `AMQP_AUTH_MODE=entra` also implies TLS when no broker URL is used. |
| `AMQP_ADDRESS` | no | `open-charge-map` | AMQP node (queue / topic / address) to publish to. |
| `AMQP_USERNAME` | no | URL username or none | SASL PLAIN username when `AMQP_AUTH_MODE=password`. |
| `AMQP_PASSWORD` | no | URL password or none | SASL PLAIN password when `AMQP_AUTH_MODE=password`. |
| `AMQP_CONTENT_MODE` | no | `binary` | CloudEvents content mode: `binary` or `structured`. |
| `AMQP_AUTH_MODE` | no | `password` | `password` for SASL PLAIN, `entra` for Microsoft Entra ID via AMQP CBS, or `sas` for SAS-token CBS. |
| `AMQP_ENTRA_AUDIENCE` | no | `https://servicebus.azure.net/.default` | Token audience when `AMQP_AUTH_MODE=entra`; use `https://eventhubs.azure.net/.default` for Event Hubs. |
| `AMQP_ENTRA_CLIENT_ID` | no | none | Optional user-assigned managed identity client id; otherwise `DefaultAzureCredential` applies. |
| `AMQP_SAS_KEY_NAME` | required with `AMQP_AUTH_MODE=sas` | none | SAS policy / key name, for example `RootManageSharedAccessKey`. |
| `AMQP_SAS_KEY` | required with `AMQP_AUTH_MODE=sas` | none | Base64-encoded SAS key used to mint CBS tokens. |

## Deploying into Microsoft Fabric

### Fabric Notebook feeder

Poll-based sources in this repo ship a notebook-hosting option. For Open Charge Map the deployment path expects [`notebook/open-charge-map-feed.ipynb`](notebook/open-charge-map-feed.ipynb): a scheduled Fabric Notebook that runs one polling cycle in the Fabric workspace, resolves the Event Stream custom-endpoint connection string at runtime via the public Topology API, and writes diagnostics to `/lakehouse/default/Files/feeder-state/open-charge-map/last-run.log`.

```powershell
tools/deploy-fabric/deploy-feeder-notebook.ps1 `
  -Source open-charge-map `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg-for-bootstrap> `
  -Location <azure-region>
```

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#open-charge-map/fabric-notebook)

### Fabric ACI feeder

Use the always-on container path for continuous polling, or for MQTT and AMQP targets that do not fit a scheduled notebook.

```powershell
tools/deploy-fabric/deploy-fabric-aci.ps1 `
  -Source open-charge-map `
  -Workspace <fabric-workspace-id-or-name> `
  -ResourceGroup <azure-rg> `
  -Location <azure-region>
```

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources#open-charge-map/fabric-aci)

## Deploying into Azure Container Instances

The Azure portal path uses five deployment shapes. Each deployment must include `OPENCHARGEMAP_API_KEY`, persistent `STATE_FILE` storage, and the transport settings from the environment-variable tables above.

### Kafka - bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://clemensv.github.io/real-time-sources#open-charge-map/azure-kafka)

### Kafka - provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://clemensv.github.io/real-time-sources#open-charge-map/azure-eventhub)

### MQTT - bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://clemensv.github.io/real-time-sources#open-charge-map/azure-mqtt)

### MQTT - provision a new Event Grid namespace MQTT broker

Deploy with a topic space rooted at `ev-charging/#`, a user-assigned managed identity, and **EventGrid TopicSpaces Publisher** permission.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://clemensv.github.io/real-time-sources#open-charge-map/azure-eventgrid-mqtt)

### AMQP 1.0 - provision a new Azure Service Bus namespace

Deploy with a queue named `open-charge-map`, a user-assigned managed identity, and **Azure Service Bus Data Sender** permission. Use `https://eventhubs.azure.net/.default` when targeting Event Hubs through AMQP.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://clemensv.github.io/real-time-sources#open-charge-map/azure-servicebus)

## Data license and attribution

Open Charge Map data is open data made available under Creative Commons attribution / share-alike terms (CC-BY-SA 4.0). Downstream consumers must attribute Open Charge Map and preserve share-alike obligations for republished or derived data. The `OCM_OPENDATA=true` default requests only records flagged as open-data licensed by the API.

This repository's feeder code and the published container images are licensed under the repository MIT license. Do not confuse the MIT code license with the Open Charge Map data license.

## Related

- [README.md](README.md) - project overview, audience, and one-paragraph operational summary.
- [EVENTS.md](EVENTS.md) - CloudEvents contract, schemas, per-transport routing, and example payloads.
- [`xreg/open-charge-map.xreg.json`](xreg/open-charge-map.xreg.json) - the xRegistry manifest the producers and EVENTS.md are derived from.
