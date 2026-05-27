<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# NOAA SWPC L1

<sub>L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time · Kafka · MQTT · AMQP · <a href="https://www.swpc.noaa.gov/">upstream</a> · <a href="https://services.swpc.noaa.gov/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — L1 propagated solar wind (DSCOVR/ACE), 1-min cadence, 30–60 min Earth-impact lead time

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#noaa-swpc-l1) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#noaa-swpc-l1/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/noaa_swpc_l1.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.swpc.noaa.gov/)

</td></tr></table>
<!-- source-hero:end -->

## Why this container

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.swpc.noaa.gov/>
- API / data documentation: <https://services.swpc.noaa.gov/>

<!-- upstream-links:end -->

The NOAA Space Weather Prediction Center (**SWPC**) publishes the
[propagated solar wind](https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json)
product: the L1 solar-wind time series forward-projected to predicted
Earth arrival. L1 is the Sun-Earth Lagrange point about 1.5 million km
sunward of Earth. NOAA DSCOVR is the operational primary L1 spacecraft;
NASA ACE is the backup.

The product is free and open, but it is a rolling JSON document: an
array-of-arrays with a header row at index 0, about seven days of rows,
and roughly one new observation per minute. These containers do the
polling, timestamp normalization, cold-start backfill, dedupe, schema
mapping and transport-specific identity work once, then re-emit the feed
as **CloudEvents** on the messaging fabric of your choice.

This feed matters operationally because sustained southward **Bz** is a
primary trigger for geomagnetic-storm warnings. Power-grid operators,
aviation and maritime HF-radio users, satellite operators and space-
weather forecasters use the propagated arrival time to get roughly
30–60 minutes of lead time before the solar-wind parcel reaches Earth.

## What ships in the box

This source ships three container images backed by the same upstream
poller and the same xRegistry contract:

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-kafka:latest` | Apache Kafka 2.x compatible (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud, plain Kafka) | One topic, JSON CloudEvents (binary mode), key = `{spacecraft}` |
| `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-mqtt:latest` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace topic `space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind`, retained QoS 1, CloudEvent attributes as MQTT 5 user properties |
| `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs, Azure Service Bus emulator) | One AMQP node `noaa-swpc-l1`, binary CloudEvents, AMQP subject = `{spacecraft}`, `x-opt-partition-key` = `{spacecraft}` |

All three images consume the NOAA SWPC propagated-solar-wind endpoint and
emit one CloudEvent type:

* `gov.noaa.swpc.l1.PropagatedSolarWind` — one minute-resolution L1 row
  that fuses plasma, magnetic-field and velocity-vector values. The
  CloudEvent `time` mirrors `time_tag`; the predicted Earth-arrival time
  is in `data.propagated_time_tag`.

The on-the-wire schema lives in [EVENTS.md](EVENTS.md). The generated KQL
schema for Fabric Eventhouse / Azure Data Explorer is in
[`kql/noaa_swpc_l1.kql`](kql/noaa_swpc_l1.kql).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer
is described in [DATABASE.md](../DATABASE.md). This source ships a typed
`PropagatedSolarWind` table and `PropagatedSolarWindLatest` materialized
view script under `kql/`.

## Installing the Container Images

Pull the container images from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-kafka:latest
$ docker pull ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-mqtt:latest
$ docker pull ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest
```

## Using the Kafka image

The Kafka image (`…-noaa-swpc-l1-kafka`) reads data from the NOAA SWPC
API and writes JSON CloudEvents (binary mode) to a Kafka topic. It works
with Apache Kafka 2.x, Azure Event Hubs, Microsoft Fabric Event Streams
and Confluent Cloud.

### With a Kafka broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='noaa-swpc-l1' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-kafka:latest
```

For a plaintext local broker, add `-e KAFKA_ENABLE_TLS=false`.

### With Azure Event Hubs or Fabric Event Streams

Use the Event Hubs or Fabric custom endpoint connection string. The
`EntityPath` value becomes the Kafka topic unless `KAFKA_TOPIC` overrides
it.

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-kafka:latest
```

Kafka is the right fit when consumers need ordered replay, seven-day
backfill into Eventhouse / ADX, or a partitioned log keyed by spacecraft
(`dscovr` today, `ace` for backup failover).

## Using the MQTT image

The MQTT image (`…-noaa-swpc-l1-mqtt`) publishes MQTT 5.0 binary-mode
CloudEvents into a Unified-Namespace topic tree at QoS 1 with
`retain=true`:

```text
space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind
```

The default spacecraft is `dscovr`, so today's retained last-known-value
slot is:

```text
space-weather/us/noaa-swpc/l1/dscovr/propagated-solar-wind
```

MQTT is the right fit for LKV dashboards, edge gateways, UNS integration
and operational systems that need the latest propagated Bz/speed/density
without replaying a log.

### With a generic MQTT 5 broker

```shell
$ docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-mqtt:latest
```

For anonymous brokers, omit `MQTT_USERNAME` and `MQTT_PASSWORD`. You can
also use `MQTT_HOST`, `MQTT_PORT` and `MQTT_TLS` instead of
`MQTT_BROKER_URL`.

### With Azure Event Grid namespace MQTT broker

When the host is an Azure Container Instance, VM, App Service, etc. with a
managed identity that holds the **EventGrid TopicSpaces Publisher** role
on the target topic space, the feeder uses MQTT v5 enhanced
authentication (`OAUTH2-JWT`) with a token for audience
`https://eventgrid.azure.net/`.

```shell
$ docker run --rm \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-mqtt:latest
```

## Using the AMQP image

The AMQP image (`…-noaa-swpc-l1-amqp`) publishes CloudEvents over AMQP
1.0 to a single AMQP node, default address `noaa-swpc-l1`. It sets the
AMQP message subject to `{spacecraft}` and stamps the
`x-opt-partition-key` message annotation with the same value. Azure
Service Bus uses that annotation as `PartitionKey`; Event Hubs hashes it
to pick the partition.

AMQP is the right fit for Azure Service Bus or AMQP consumers that need
queue semantics, sessions, scheduled delivery, dead-lettering, or native
Service Bus / Event Hubs clients while keeping CloudEvents on the wire.

### Generic AMQP 1.0 brokers

Use SASL PLAIN with a connection URL:

```shell
$ docker run --rm \
    -e AMQP_BROKER_URL='amqp://user:pw@broker.example.com:5672/noaa-swpc-l1' \
    ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest
```

For TLS-enabled brokers use `amqps://...:5671/...`.

### Azure Service Bus / Event Hubs with Microsoft Entra ID

Run the image with `AMQP_AUTH_MODE=entra` against a user-assigned managed
identity. The identity must hold the **Azure Service Bus Data Sender**
role on the target queue, or **Azure Event Hubs Data Sender** for Event
Hubs.

```shell
$ docker run --rm \
    -e AMQP_HOST='myns.servicebus.windows.net' \
    -e AMQP_PORT=5671 \
    -e AMQP_TLS=true \
    -e AMQP_ADDRESS='noaa-swpc-l1' \
    -e AMQP_AUTH_MODE=entra \
    -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
    -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest
```

Use `https://eventhubs.azure.net/.default` for Event Hubs.

### Azure Service Bus emulator / SAS-only namespaces

For local development against the Azure Service Bus emulator, or for
namespaces still configured for SAS authentication, use
`AMQP_AUTH_MODE=sas`.

```shell
$ docker run --rm \
    -e AMQP_HOST='servicebus-emulator' \
    -e AMQP_PORT=5672 \
    -e AMQP_ADDRESS='noaa-swpc-l1' \
    -e AMQP_AUTH_MODE=sas \
    -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
    -e AMQP_SAS_KEY='SAS_KEY_VALUE' \
    ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest
```

For live Azure namespaces, set `AMQP_TLS=true` and `AMQP_PORT=5671`.

## Environment Variables

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream-style connection string. Supersedes separate bootstrap and SASL settings. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of Kafka brokers. Required when `CONNECTION_STRING` is not set. |
| `KAFKA_TOPIC` | Target Kafka topic (default `noaa-swpc-l1`). |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials for Kafka-compatible brokers. |
| `KAFKA_ENABLE_TLS` | `false`, `0` or `no` disables TLS (default `true`). |
| `SPACECRAFT` | Source spacecraft id stamped onto every event: `dscovr` (default) or `ace`. |
| `BACKFILL_MINUTES` | Cold-start backfill window when no state file exists (default `5`). |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `60`). |
| `STATE_FILE` | Dedupe state path (default `~/.noaa_swpc_l1_state.json`). |
| `ONCE_MODE` | `1`, `true` or `yes` runs one polling cycle and exits. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional username/password credentials. Omit for anonymous brokers. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication with Microsoft Entra JWT. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id. |
| `MQTT_CLIENT_ID` | MQTT client identifier. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `SPACECRAFT` | Source spacecraft id: `dscovr` (default) or `ace`. |
| `BACKFILL_MINUTES` | Cold-start backfill window when no state file exists (default `5`). |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `60`). |
| `STATE_FILE` | Dedupe state path (default `~/.noaa_swpc_l1_state.json`). |
| `ONCE_MODE` | `1`, `true` or `yes` runs one polling cycle and exits. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, e.g. `amqp://user:pw@host:5672/noaa-swpc-l1` or `amqps://host:5671/noaa-swpc-l1`. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL` (default port 5672, or 5671 with TLS). |
| `AMQP_ADDRESS` | AMQP node (queue / topic / address) name (default `noaa-swpc-l1`). |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS, or `sas` for SAS-token CBS. |
| `AMQP_ENTRA_AUDIENCE` | Token audience (default `https://servicebus.azure.net/.default`; use `https://eventhubs.azure.net/.default` for Event Hubs). |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id. |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name. Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_SAS_KEY` | SAS key value. Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `SPACECRAFT` | Source spacecraft id: `dscovr` (default) or `ace`. |
| `BACKFILL_MINUTES` | Cold-start backfill window when no state file exists (default `5`). |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `60`). |
| `STATE_FILE` | Dedupe state path (default `~/.noaa_swpc_l1_state.json`). |
| `ONCE_MODE` | `1`, `true` or `yes` runs one polling cycle and exits. |

## Deploying into Azure Container Instances

Five one-click deployment templates are available. Each template creates
an Azure Container Instance for the selected transport; the provisioned
variants also create the target broker/service and managed identity or
connection wiring required by that service.

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs, Fabric Event
Stream, Confluent or Kafka-compatible connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa-swpc-l1%2Fazure-template.json)

### Kafka — provision a new Event Hub

Deploy the Kafka container together with a new Event Hubs namespace and
event hub. The connection string is wired automatically.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa-swpc-l1%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

Deploy the MQTT container against an existing MQTT 5 broker. You provide
the broker URL and optional username/password credentials.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa-swpc-l1%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

Deploy the MQTT container together with an Azure Event Grid namespace with
the MQTT broker enabled, a topic space rooted at
`space-weather/us/noaa-swpc/l1/#`, a user-assigned managed identity and a
role assignment granting **EventGrid TopicSpaces Publisher**.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa-swpc-l1%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP 1.0 — provision a new Azure Service Bus namespace

Deploy the AMQP container together with an Azure Service Bus Standard
namespace, a queue named `noaa-swpc-l1`, a user-assigned managed identity
and a role assignment granting **Azure Service Bus Data Sender**. The
feeder authenticates via AMQP CBS with Microsoft Entra ID.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnoaa-swpc-l1%2Fazure-template-with-servicebus.json)

## State and dedupe behavior

All three transports share the same acquisition logic. The feeder polls
`https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json`
every `POLLING_INTERVAL` seconds (default 60). On startup it reads
`STATE_FILE` (default `~/.noaa_swpc_l1_state.json`) and emits only rows
whose `time_tag` is strictly newer than the stored `last_time_tag`.

When no state file exists, the bridge starts from now minus
`BACKFILL_MINUTES` (default 5) instead of replaying the full seven-day
rolling window. Rows with partial null numeric values are still emitted;
only rows without parseable `time_tag` or `propagated_time_tag` are
skipped. After a successful cycle, the state file is updated with:

```json
{ "last_time_tag": "2025-01-15T12:34:00+00:00" }
```
