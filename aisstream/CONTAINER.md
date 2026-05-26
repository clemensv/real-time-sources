# AISstream.io container images

This document covers the published OCI container images for the AISstream.io feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://aisstream.io/>
- API / data documentation: <https://aisstream.io/documentation>

<!-- upstream-links:end -->

> [!WARNING]
> **AISstream.io is a free, community-run service with no SLA.** During testing on 2026-04-02 the WebSocket accepted connections and API keys without error but delivered **zero messages** over sustained periods. Silent outages lasting hours to days have been [reported by multiple users](https://github.com/aisstream/issues/issues/134). These containers reconnect with exponential backoff, but data gaps are expected.

## Why this container

[AISstream.io](https://aisstream.io/) aggregates **terrestrial AIS** traffic (Automatic Identification System, ITU-R M.1371-5) from community ground stations worldwide — approximately 200 km of coverage from every coast where a station is in range — and delivers pre-decoded JSON for all 23 standard message families over a single free WebSocket. The feed is open, but it is a long-lived socket: every consumer ends up writing the same reconnect-with-backoff, filter, schema-validation and identity glue.

These container images do that work once and re-emit the firehose as **CloudEvents** on the messaging fabric of your choice — so port operators, naval / coast-guard situational-awareness systems, logistics ETA pipelines, emissions-modelling platforms (Microsoft Fabric Eventhouse / Azure Data Explorer / data lakes), and maritime researchers can subscribe to a topic instead of holding their own WebSocket.

## What ships in the box

This source ships three container images backed by the same upstream WebSocket client and the same xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-aisstream` | Apache Kafka 2.x (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic, JSON CloudEvents (binary mode), key = `{mmsi}`, all 23 AIS message families |
| `ghcr.io/clemensv/real-time-sources-aisstream-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace topic tree `maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}`, QoS 0 non-retained, CloudEvent attributes as MQTT 5 user properties, routing-friendly subset (`PositionReport`, `ShipStatic`, `AidToNavigation`) |
| `ghcr.io/clemensv/real-time-sources-aisstream-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | One AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers, Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs, or SAS-token CBS for the emulator and SAS-only namespaces |

All three images consume the AISstream.io WebSocket firehose and re-emit CloudEvents. The on-the-wire schemas live in [EVENTS.md](EVENTS.md).

## Database schemas and handling

If you want to build a full data pipeline with all events ingested into a database, the integration with Microsoft Fabric Eventhouse and Azure Data Explorer is described in [DATABASE.md](../DATABASE.md). The KQL schema for AISstream lives in [`kql/aisstream.kql`](kql/aisstream.kql).

## Image contract

All three images share the same operational contract:

| Aspect | Value |
| --- | --- |
| Base image | `python:3.12-slim` (multi-arch: `linux/amd64`, `linux/arm64`) |
| Default entry point | `python -m aisstream{,_mqtt,_amqp} stream` |
| Default user | root (no `USER` directive) |
| Exposed ports | none — the feeder is an outbound publisher only |
| Health check | none defined; treat process liveness as health |
| Signals | terminates cleanly on `SIGTERM`; the WebSocket and downstream producer flush before exit |
| Persistent state | **none required.** The bridge is a pure WebSocket forwarder; the MQTT image holds an in-memory ship-type / position cache that rebuilds from the live stream after every restart. |
| Image tags | `:latest` tracks the default branch; immutable tags `:v<MAJOR>.<MINOR>.<PATCH>` and `:sha-<git-sha>` are published per release. |

Pull and inspect available tags at <https://github.com/clemensv/real-time-sources/pkgs/container/real-time-sources-aisstream>.

## Installing the container images

Pull the container images from the GitHub Container Registry:

```bash
docker pull ghcr.io/clemensv/real-time-sources-aisstream:latest
docker pull ghcr.io/clemensv/real-time-sources-aisstream-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-aisstream-amqp:latest
```

## Using the Kafka image

The Kafka image (`…-aisstream`) connects to the AISstream.io WebSocket firehose and writes JSON CloudEvents (binary mode) to a Kafka topic. It works with Apache Kafka 2.x, Azure Event Hubs, and Microsoft Fabric Event Streams.

### With a Kafka broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN authentication. Run the container with the following command:

```bash
docker run --rm \
    -e AISSTREAM_API_KEY='<aisstream-api-key>' \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-aisstream:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string to establish a connection to the service. Obtain the connection string from the Azure portal, the Azure CLI, or the "custom endpoint" of a Fabric Event Stream.

```bash
docker run --rm \
    -e AISSTREAM_API_KEY='<aisstream-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-aisstream:latest
```

### Filtering by region

Restrict the feed to one or more geographic bounding boxes; multiple boxes are separated by `;`.

```bash
docker run --rm \
    -e AISSTREAM_API_KEY='<aisstream-api-key>' \
    -e CONNECTION_STRING='<connection-string>' \
    -e AISSTREAM_BOUNDING_BOXES='35,-15,72,45' \
    ghcr.io/clemensv/real-time-sources-aisstream:latest
```

## Using the MQTT image

The MQTT image (`…-aisstream-mqtt`) publishes MQTT 5.0 binary-mode CloudEvents into a Unified-Namespace topic tree at QoS 0 with `retain=false` on each leaf. It works against any MQTT 5 broker (Mosquitto, EMQX, HiveMQ, …) and against the [Azure Event Grid namespace MQTT broker](https://learn.microsoft.com/azure/event-grid/mqtt-overview), including the integrated [Microsoft Fabric Real-Time Hub MQTT source](https://learn.microsoft.com/fabric/real-time-hub/add-source-event-grid).

The MQTT contract is intentionally narrower than the Kafka contract: only three event families are published (`PositionReport`, `ShipStatic`, `AidToNavigation`), each carrying five routing axes baked into the topic tree.

### Topic template

```text
maritime/intl/aisstream/aisstream/{flag}/{ship_type}/{geohash5}/{mmsi}/{msg_type}
```

| Axis | Meaning |
|------|---------|
| `{flag}` | ISO-3166-1 alpha-2 (lower-case) derived from the MMSI MID; `xx` for special MMSIs (AtoN, SAR, …) or unknown MIDs. |
| `{ship_type}` | Kebab bucket: `cargo`, `tanker`, `passenger`, `fishing`, `tug`, `pleasure-craft`, `high-speed`, `pilot`, `sar`, `aton`, `other`, `unknown`. |
| `{geohash5}` | 5-character geohash of the last known position (`00000` if unknown for a static report). |
| `{mmsi}` | 9-digit MMSI. |
| `{msg_type}` | Literal tail per family: `position-report`, `static`, `aid-to-navigation`. |

`ContentType` is `application/json`; CloudEvents attributes ride as MQTT 5 user properties; `subject` equals the MMSI.

#### Ship-type and position caches

`ShipStatic` (AIS Type 5 / 24) messages populate an in-memory MMSI → ship-type cache; subsequent `PositionReport` messages from the same MMSI inherit that bucket. Likewise the most recent position is cached so that later static reports get a real `geohash5` instead of `00000`. Caches are process-local and rebuild from the live stream after every restart.

#### MID → ISO mapping

The MID-to-ISO table (`aisstream_mqtt/mid_iso.csv`) is a curated subset of the public **ITU-R M.585** Maritime Identification Digits registry (vintage `2024-01`). The ITU-R recommendation is openly published and the digit→state mapping it contains is factual reference data not subject to copyright. Refresh the CSV when ITU publishes a new revision and bump `MID_ISO_VERSION` in `enrichment.py`.

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
    -e AISSTREAM_API_KEY='<aisstream-api-key>' \
    -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-aisstream-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

When the host is an Azure VM, Container Instance, App Service, etc. with a managed identity that holds the **EventGrid TopicSpaces Publisher** role on the target topic space, the feeder uses MQTT v5 enhanced authentication (`OAUTH2-JWT`) to authenticate with a token issued for audience `https://eventgrid.azure.net/`.

> [!IMPORTANT]
> `MQTT_CLIENT_ID` must be globally unique across all clients connected to the same broker. Azure Event Grid disconnects an existing session when a second client connects with the same identifier ("subscription steal"). Use a deterministic but unique value (for example a hostname-plus-suffix) per deployed feeder instance.

```bash
docker run --rm \
    -e AISSTREAM_API_KEY='<aisstream-api-key>' \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    ghcr.io/clemensv/real-time-sources-aisstream-mqtt:latest
```

## Using the AMQP image

The AMQP image (`…-aisstream-amqp`) publishes CloudEvents over AMQP 1.0 to a single AMQP node (queue, topic, or address). It targets two deployment shapes:

### Generic AMQP 1.0 brokers (RabbitMQ AMQP 1.0, Artemis, Qpid Dispatch)

Use SASL PLAIN with a connection URL:

```bash
docker run --rm \
    -e AISSTREAM_API_KEY='<aisstream-api-key>' \
    -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/aisstream' \
    ghcr.io/clemensv/real-time-sources-aisstream-amqp:latest
```

For TLS-enabled brokers use `amqps://<broker-host>:5671/<address>`.

### Azure Service Bus / Event Hubs (Microsoft Entra ID, no SAS keys)

> [!IMPORTANT]
> For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`. Port 5672 is only valid against the local Service Bus emulator.

Run the image with `AMQP_AUTH_MODE=entra` against a user-assigned managed identity. The identity must hold the **Azure Service Bus Data Sender** role (or **Azure Event Hubs Data Sender** for Event Hubs) on the target queue or hub:

```bash
docker run --rm \
    -e AISSTREAM_API_KEY='<aisstream-api-key>' \
    -e AMQP_HOST='<namespace>.servicebus.windows.net' \
    -e AMQP_PORT=5671 -e AMQP_TLS=true \
    -e AMQP_ADDRESS='aisstream' \
    -e AMQP_AUTH_MODE=entra \
    -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
    -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    ghcr.io/clemensv/real-time-sources-aisstream-amqp:latest
```

The bridge mints an Entra ID access token via `DefaultAzureCredential` and hands it to the broker through the AMQP CBS (Claims-Based Security) put-token control link — no SAS-key rotation required.

### Azure Service Bus emulator / SAS-only namespaces (SAS-token CBS)

For local development against the [Azure Service Bus emulator](https://learn.microsoft.com/azure/service-bus-messaging/test-locally-with-service-bus-emulator) or for Service Bus / Event Hubs namespaces still configured for SAS authentication (no Entra ID), use `AMQP_AUTH_MODE=sas`. The bridge mints a `SharedAccessSignature` token from the key and key-name and presents it via AMQP CBS (`type=servicebus.windows.net:sastoken`):

```bash
docker run --rm \
    -e AISSTREAM_API_KEY='<aisstream-api-key>' \
    -e AMQP_HOST='servicebus-emulator' \
    -e AMQP_PORT=5672 \
    -e AMQP_ADDRESS='aisstream' \
    -e AMQP_AUTH_MODE=sas \
    -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
    -e AMQP_SAS_KEY='<sas-key>' \
    ghcr.io/clemensv/real-time-sources-aisstream-amqp:latest
```

For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`.

## Environment variables

### Common (all images)

| Variable | Description |
|---|---|
| `AISSTREAM_API_KEY` | **Required.** AISstream.io API key. Obtain one by registering at [aisstream.io](https://aisstream.io/) via GitHub OAuth (free). |
| `AISSTREAM_BOUNDING_BOXES` | Server-side geographic filter as semicolon-separated bounding boxes: `lat1,lon1,lat2,lon2;...`. Default `-90,-180,90,180` (global). |
| `AISSTREAM_MESSAGE_TYPES` | Comma-separated list of AIS message-type names to subscribe to. Default: all 23 types. |
| `AISSTREAM_FILTER_MMSI` | Comma-separated list of MMSI numbers to include (client-side filter applied after the server-side AISstream.io filter). Default: all vessels. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream–style connection string. Supersedes `KAFKA_BOOTSTRAP_SERVERS`, `SASL_USERNAME`, `SASL_PASSWORD`. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of TLS-enabled Kafka brokers. |
| `KAFKA_TOPIC` | Target Kafka topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |
| `AISSTREAM_FLUSH_INTERVAL` | Number of events to buffer before flushing the Kafka producer. Default `1000`. |

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
| `AISSTREAM_MOCK` | `true` emits one canned message per family (used by Docker E2E). |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, e.g. `amqp://user:pw@host:5672/address` or `amqps://host:5671/address`. Path overrides `AMQP_ADDRESS`. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL` (default port 5672, or 5671 with `AMQP_TLS=true`). |
| `AMQP_ADDRESS` | AMQP node (queue / topic) name (default `aisstream`). |
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

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace (Standard SKU, 1 throughput unit) and event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-eventhub.json)

### AMQP 1.0 — provision a new Azure Service Bus namespace

Deploy the AMQP container together with a new [Azure Service Bus Standard namespace](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview) with a queue named `aisstream`, a user-assigned managed identity, and a role assignment granting the identity the **Azure Service Bus Data Sender** role on the queue. The feeder authenticates to the broker using AMQP 1.0 claims-based security (CBS) with tokens minted by the managed identity for audience `https://servicebus.azure.net/`. Works the same way against an Event Hubs namespace by changing the audience and endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faisstream%2Fazure-template-with-servicebus.json)

## Related

- [README.md](README.md) — project overview, audience, and one-paragraph operational summary.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, per-transport routing, and example payloads.
- [`xreg/aisstream.xreg.json`](xreg/aisstream.xreg.json) — the xRegistry manifest the producers and EVENTS.md are derived from.
