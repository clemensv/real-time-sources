<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# Blitzortung

<sub>community lightning strokes, seconds latency · Kafka · MQTT · AMQP · <a href="https://www.blitzortung.org/">upstream</a> · <a href="https://www.lightningmaps.org/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — community lightning strokes, seconds latency

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#blitzortung) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/blitzortung.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.blitzortung.org/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI container images for the Blitzortung lightning feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.blitzortung.org/>
- API / data documentation: <https://www.lightningmaps.org/>

<!-- upstream-links:end -->

> [!IMPORTANT]
> **Blitzortung / LightningMaps is a community-run, non-commercial service.** The upstream project explicitly frames its data as **not** an official safety information service: do not use it for life-safety alerting, aviation operations, or as a substitute for a certified lightning-detection feed. Honour the upstream non-commercial terms when redistributing.

## Why this container

[Blitzortung.org](https://www.blitzortung.org/) and its public viewer [LightningMaps.org](https://www.lightningmaps.org/) operate a worldwide volunteer network of VLF lightning detectors. The combined system geolocates cloud-to-ground and cloud-to-cloud strokes within seconds of occurrence with continent-scale coverage no other free feed approaches. The data is published over a live websocket, but every consumer ends up writing the same reconnect, dedupe, geohash-enrichment and CloudEvents-validation glue.

These container images do that work once and re-emit the firehose as **CloudEvents** on the messaging fabric of your choice — so weather situational-awareness dashboards, parametric insurers, grid operators, outdoor-venue safety teams, and climate researchers can subscribe to a topic instead of holding their own websocket.

## What ships in the box

This source ships three container images backed by the same upstream websocket client and the same xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-blitzortung` | Apache Kafka 2.x (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic, JSON CloudEvents (binary mode), key = `{source_id}/{stroke_id}` |
| `ghcr.io/clemensv/real-time-sources-blitzortung-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace topic tree `weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke`, QoS 0 non-retained, CloudEvent attributes as MQTT 5 user properties |
| `ghcr.io/clemensv/real-time-sources-blitzortung-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | One AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three images consume the LightningMaps / Blitzortung live websocket feed and re-emit one CloudEvent type:

* `Blitzortung.Lightning.LightningStroke` — one located lightning stroke from the public live feed.

The on-the-wire schema lives in [EVENTS.md](EVENTS.md). This source emits **telemetry only**; the upstream does not publish a station-metadata endpoint that would support a separate reference-data event family.

## Database schemas and handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Microsoft Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md). The KQL schema for Blitzortung lives in [`kql/`](kql/).

## Image contract

All three images share the same operational contract:

| Aspect | Value |
| --- | --- |
| Base image | `python:3.12-slim` (multi-arch: `linux/amd64`, `linux/arm64`) |
| Default entry point | `python -m blitzortung{,_mqtt,_amqp} feed` |
| Default user | root (no `USER` directive) |
| Exposed ports | none — the feeder is an outbound publisher only |
| Health check | none defined; treat process liveness as health |
| Signals | terminates cleanly on `SIGTERM`; the websocket and downstream producer flush before exit |
| Persistent state | **none required.** Cross-reconnect stroke-id dedupe is an in-memory ring that rebuilds from the live stream after every restart. |
| Image tags | `:latest` tracks the default branch; immutable tags `:v<MAJOR>.<MINOR>.<PATCH>` and `:sha-<git-sha>` are published per release. |

Pull and inspect available tags at <https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-blitzortung>.

## Installing the container images

Pull the container images from the GitHub Container Registry:

```bash
docker pull ghcr.io/clemensv/real-time-sources-blitzortung:latest
docker pull ghcr.io/clemensv/real-time-sources-blitzortung-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-blitzortung-amqp:latest
```

## Using the Kafka image

The Kafka image (`…-blitzortung`) connects to the LightningMaps / Blitzortung websocket and writes JSON CloudEvents (binary mode) to a Kafka topic. It works with Apache Kafka 2.x, Azure Event Hubs, and Microsoft Fabric Event Streams.

### With a Kafka broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container with the following command:

```bash
docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-blitzortung:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, the Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```bash
docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-blitzortung:latest
```

## Using the MQTT image

The MQTT image (`…-blitzortung-mqtt`) publishes MQTT 5.0 binary-mode CloudEvents into a Unified-Namespace topic tree at QoS 0 with `retain=false` on each leaf — a firehose has no Last-Known-Value slot. It works against any MQTT 5 broker (Mosquitto, EMQX, HiveMQ, …) and against the [Azure Event Grid namespace MQTT broker](https://learn.microsoft.com/azure/event-grid/mqtt-overview), including the integrated [Microsoft Fabric Real-Time Hub MQTT source](https://learn.microsoft.com/fabric/real-time-hub/add-source-event-grid).

### Topic template

```text
weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke
```

| Axis | Meaning |
|------|---------|
| `{geohash5}` | 5-character geohash of the located stroke (~5 km cell at the equator), derived in the bridge from latitude and longitude. Used for coarse geographic wildcards. |
| `{geohash7}` | 7-character geohash of the located stroke (~150 m cell), derived from latitude and longitude. Used for fine-grained geographic wildcards. |
| `{stroke_id}` | Source-scoped stroke identifier from the upstream `id` field. |

`ContentType` is `application/json`; CloudEvents attributes ride as MQTT 5 user properties; `subject` equals `{source_id}/{stroke_id}` (the same compound identity used as the Kafka key).

Subscribe with `weather/intl/blitzortung/blitzortung/u281/#` to receive every stroke within the corresponding ~5 km cell, or with `weather/intl/blitzortung/blitzortung/+/+/+/stroke` to receive the global firehose.

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-blitzortung-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

When the host is an Azure VM, Container Instance, App Service, etc. with a managed identity that holds the **EventGrid TopicSpaces Publisher** role on the target topic space, the feeder uses MQTT v5 enhanced authentication (`OAUTH2-JWT`) to authenticate with a token issued for audience `https://eventgrid.azure.net/`.

> [!IMPORTANT]
> `MQTT_CLIENT_ID` must be globally unique across all clients connected to the same broker. Azure Event Grid disconnects an existing session when a second client connects with the same identifier ("subscription steal"). Use a deterministic but unique value (for example a hostname-plus-suffix) per deployed feeder instance.

```bash
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    ghcr.io/clemensv/real-time-sources-blitzortung-mqtt:latest
```

## Using the AMQP image

The AMQP image (`…-blitzortung-amqp`) publishes CloudEvents over AMQP 1.0 to a single AMQP node (queue, topic, or address). It targets two deployment shapes:

### Generic AMQP 1.0 brokers (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch)

Use SASL PLAIN with a connection URL:

```bash
docker run --rm \
    -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/blitzortung' \
    ghcr.io/clemensv/real-time-sources-blitzortung-amqp:latest
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
    -e AMQP_ADDRESS='blitzortung' \
    -e AMQP_AUTH_MODE=entra \
    -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
    -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    ghcr.io/clemensv/real-time-sources-blitzortung-amqp:latest
```

The bridge mints an Entra ID access token via `DefaultAzureCredential` and hands it to the broker through the AMQP CBS (Claims-Based Security) put-token control link — no SAS-key rotation required.

### Azure Service Bus emulator / SAS-only namespaces (SAS-token CBS)

For local development against the [Azure Service Bus emulator](https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator) or for Service Bus / Event Hubs namespaces still configured for SAS authentication (no Entra ID), use `AMQP_AUTH_MODE=sas`:

```bash
docker run --rm \
    -e AMQP_HOST='servicebus-emulator' \
    -e AMQP_PORT=5672 \
    -e AMQP_ADDRESS='blitzortung' \
    -e AMQP_AUTH_MODE=sas \
    -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
    -e AMQP_SAS_KEY='<sas-key>' \
    ghcr.io/clemensv/real-time-sources-blitzortung-amqp:latest
```

For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`.

## Environment variables

### Common (all images)

| Variable | Description |
|---|---|
| `BLITZORTUNG_WEBSOCKET_URL` | Upstream websocket URL. Default `wss://live.lightningmaps.org:443/`; failover to `wss://live2.lightningmaps.org:443/` is automatic. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream–style connection string. Supersedes `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, `SASL_PASSWORD`. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of TLS-enabled Kafka brokers. |
| `KAFKA_TOPIC` | Target Kafka topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |

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

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, e.g. `amqp://user:pw@host:5672/address` or `amqps://host:5671/address`. Path overrides `AMQP_ADDRESS`. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL` (default port 5672, or 5671 with `AMQP_TLS=true`). |
| `AMQP_ADDRESS` | AMQP node (queue / topic) name (default `blitzortung`). |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS (Service Bus / Event Hubs), or `sas` for SAS-token CBS (Service Bus emulator, or SAS-only namespaces). |
| `AMQP_ENTRA_AUDIENCE` | Token audience (default `https://servicebus.azure.net/.default`). Use `https://eventhubs.azure.net/.default` for Event Hubs. Used only when `AMQP_AUTH_MODE=entra`. |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id; otherwise `DefaultAzureCredential` selection applies. Used only when `AMQP_AUTH_MODE=entra`. |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name (e.g. `RootManageSharedAccessKey`). **Required when `AMQP_AUTH_MODE=sas`.** |
| `AMQP_SAS_KEY` | SAS key value (base64-encoded shared secret). **Required when `AMQP_AUTH_MODE=sas`.** |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |

## Deploying into Azure Container Instances

Three one-click deployment templates are available — one for each realistic Azure target.

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-with-eventhub.json)

### AMQP 1.0 — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue named `blitzortung`, a user-assigned managed identity, and a role assignment granting the identity the **Azure Service Bus Data Sender** role on the queue. The feeder authenticates to the broker using AMQP 1.0 claims-based security (CBS) with tokens minted by the managed identity for audience `https://servicebus.azure.net/`. Works the same way against an Event Hubs namespace by changing the audience and endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fblitzortung%2Fazure-template-amqp.json)

## Related

- [README.md](README.md) — project overview, audience, and one-paragraph operational summary.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, per-transport routing, and example payloads.
- [`xreg/blitzortung.xreg.json`](xreg/blitzortung.xreg.json) — the xRegistry manifest the producers and EVENTS.md are derived from.
