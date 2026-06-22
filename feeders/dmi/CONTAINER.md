<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/dk.png" alt="Denmark" width="64" height="48"><br>
<sub><b>Denmark</b></sub>
</td>
<td valign="middle">

# DMI

<sub>meteorological observations, sea level, lightning strikes · Kafka · MQTT · AMQP · <a href="https://www.dmi.dk/">upstream</a> · <a href="https://opendataapi.dmi.dk/">API docs</a></sub>

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

This source ships three container images backed by the same upstream poller
and xRegistry contract:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.dmi.dk/>
- API / data documentation: <https://opendataapi.dmi.dk/>

<!-- upstream-links:end -->

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-dmi-kafka` | Apache Kafka 2.x (Azure Event Hubs, Fabric Event Streams, Confluent Cloud, plain Kafka) | Single topic `dmi`, JSON CloudEvents (binary mode); subscribers route by `ce_type` |
| `ghcr.io/clemensv/real-time-sources-dmi-mqtt` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric MQTT) | Unified-Namespace topic tree under `weather/dk/dmi/…` and `ocean/dk/dmi/…`, retained QoS 1, CloudEvent attributes as MQTT 5 user properties |
| `ghcr.io/clemensv/real-time-sources-dmi-amqp` | AMQP 1.0 broker (Azure Service Bus, Azure Event Hubs, ActiveMQ Artemis, RabbitMQ AMQP 1.0) | Binary-mode AMQP 1.0 messages to one address `dmi`; subject = stable upstream identifier |

All three images consume the [DMI Open Data REST API](https://opendataapi.dmi.dk/)
operated by the Danish Meteorological Institute and emit the
**observation triad**: `metObs` (land weather), `oceanObs` (sea-state and
tidewater), and `lightningData` (per-strike events published on Kafka and AMQP).

The on-the-wire schemas live in [EVENTS.md](EVENTS.md). The container images
work with any Apache Kafka–compatible service that supports TLS with
SASL/PLAIN, any MQTT 5.0 broker, and AMQP 1.0 brokers ranging from
generic SASL PLAIN peers to Azure Service Bus / Event Hubs with Entra ID.

## Image contract

All three images share the same operational contract:

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` |
| Default entry point | `python -m dmi_{kafka,mqtt,amqp} feed` |
| Default user | root (no `USER` directive) |
| Exposed ports | none — the feeder is an outbound publisher only |
| Health check | none defined; treat process liveness as health |
| Persistent state | `STATE_FILE`; defaults are `~/.dmi_state.json` (Kafka / shared core), `~/.dmi_mqtt_state.json`, and `~/.dmi_amqp_state.json`. Mount a volume to keep dedupe state across restarts. |
| Image tags | `:latest` tracks the default branch; immutable release tags and `:sha-<git-sha>` tags are published with repository releases. |

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md). The DMI-specific KQL schema is
in [kql/dmi.kql](kql/dmi.kql).

## Installing the Container Images

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-dmi-kafka:latest
$ docker pull ghcr.io/clemensv/real-time-sources-dmi-mqtt:latest
$ docker pull ghcr.io/clemensv/real-time-sources-dmi-amqp:latest
```

## Using the Kafka image

The Kafka image (`…-dmi-kafka`) reads from the three DMI APIs and writes
JSON CloudEvents (binary mode) to a **single** Kafka topic. Subscribers
route by the CloudEvent `type` attribute.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='dmi' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    -e DMI_LIGHTNING_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-kafka:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    -e DMI_LIGHTNING_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-kafka:latest
```

## Using the MQTT image

The MQTT image (`…-dmi-mqtt`) publishes MQTT 5.0 binary-mode CloudEvents
into a Unified-Namespace topic tree at QoS 1 with `retain=true` on each
leaf. **Lightning is excluded** — per-strike events have no LKV fit.

Topics (retained):

```
weather/dk/dmi/met-obs/{station_id}/info
weather/dk/dmi/met-obs/{station_id}/{parameter_id}
ocean/dk/dmi/ocean-obs/{station_id}/info
ocean/dk/dmi/ocean-obs/{station_id}/{parameter_id}
ocean/dk/dmi/tidewater/{station_id}/info
ocean/dk/dmi/tidewater/{station_id}/prediction
```

### With a generic MQTT 5 broker (username/password)

```shell
$ docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

When the host has a managed identity that holds the
**EventGrid TopicSpaces Publisher** role on the target topic space, the
feeder uses MQTT v5 enhanced authentication (`OAUTH2-JWT`) with a token
issued for audience `https://eventgrid.azure.net/`.

```shell
$ docker run --rm \
    -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
    -e MQTT_AUTH_MODE=entra \
    -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e MQTT_CLIENT_ID='<unique-client-id>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-mqtt:latest
```

## Using the AMQP image

### With a generic AMQP 1.0 broker (username/password)

```shell
$ docker run --rm \
    -e AMQP_BROKER_URL='amqps://broker.example.com:5671/dmi' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    -e DMI_LIGHTNING_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-amqp:latest
```

### With Azure Service Bus / Event Hubs (Microsoft Entra ID over CBS)

```shell
$ docker run --rm \
    -e AMQP_HOST='<namespace>.servicebus.windows.net' \
    -e AMQP_PORT=5671 \
    -e AMQP_TLS=true \
    -e AMQP_ADDRESS='dmi' \
    -e AMQP_AUTH_MODE=entra \
    -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
    -e DMI_METOBS_API_KEY='<key>' \
    -e DMI_OCEANOBS_API_KEY='<key>' \
    -e DMI_LIGHTNING_API_KEY='<key>' \
    ghcr.io/clemensv/real-time-sources-dmi-amqp:latest
```

## Environment Variables

### Common (all images)

| Variable | Description |
|---|---|
| `DMI_API_KEY` | *Optional.* Fallback DMI Gravitee key, only used against the legacy authenticated host. |
| `DMI_METOBS_API_KEY` | *Optional.* Per-API key for the MetObs API (legacy host only). |
| `DMI_OCEANOBS_API_KEY` | *Optional.* Per-API key for the OceanObs API (legacy host only). |
| `DMI_LIGHTNING_API_KEY` | *Optional.* Per-API key for the Lightning API (Kafka and AMQP images; legacy host only). |
| `DMI_METOBS_FEED_ROOT` | *Optional.* Override the MetObs base URL (default `https://opendataapi.dmi.dk/v2/metObs`, auth-free). |
| `DMI_OCEANOBS_FEED_ROOT` | *Optional.* Override the OceanObs base URL (default `https://opendataapi.dmi.dk/v2/oceanObs`, auth-free). |
| `DMI_LIGHTNING_FEED_ROOT` | *Optional.* Override the Lightning base URL (default `https://opendataapi.dmi.dk/v2/lightningdata`, auth-free). |
| `DMI_OBSERVATION_PERIOD` | DMI period filter (default `latest-hour`). |
| `DMI_REFERENCE_REFRESH_HOURS` | Hours between re-emit of reference data (default `6`). |
| `POLLING_INTERVAL` | Seconds between polling cycles (default `300`). |
| `STATE_FILE` | Path to the dedupe state file. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Azure Event Hubs / Fabric Event Stream connection string. Supersedes `KAFKA_*` and `SASL_*`. |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of TLS-enabled Kafka brokers. |
| `KAFKA_TOPIC` | Target Kafka topic (default `dmi`). |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_HOST` / `MQTT_PORT` / `MQTT_TLS` | Component-level alternative to `MQTT_BROKER_URL`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional credentials when `MQTT_AUTH_MODE=password`. |
| `MQTT_AUTH_MODE` | `password` (default), `anonymous`, `tls-cert`, or `entra`. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id. |
| `MQTT_CLIENT_ID` | MQTT client identifier. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `MQTT_CA_FILE` | Path to broker CA chain. |
| `MQTT_CLIENT_CERT` / `MQTT_CLIENT_KEY` | PEM paths for `tls-cert` auth. |
| `MQTT_ENABLE_TLS` | Set `true` to use TLS (`mqtts`) for the MQTT connection. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, e.g. `amqp://host:5672/dmi` or `amqps://host:5671/dmi`. |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component-level alternative to `AMQP_BROKER_URL`. |
| `AMQP_ADDRESS` | Queue, topic, or event hub name (default `dmi`). |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | Optional SASL PLAIN credentials when `AMQP_AUTH_MODE=password`. |
| `AMQP_AUTH_MODE` | `password` (default) or `entra`. |
| `AMQP_ENTRA_AUDIENCE` | Entra audience (default `https://servicebus.azure.net/.default`; use `https://eventhubs.azure.net/.default` for Event Hubs). |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client id. |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured`. |

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Azure Event Hubs or Fabric Event
Stream connection string. The template creates a storage account and file
share for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

Deploys the MQTT container together with an Azure Event Grid namespace,
topic space rooted at `weather/#` and `ocean/#`, a user-assigned managed
identity, and an `EventGrid TopicSpaces Publisher` role assignment scoped
to the topic space.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus queue

Deploys the AMQP container together with an Azure Service Bus namespace,
queue `dmi`, a user-assigned managed identity, and an `Azure Service Bus
Data Sender` role assignment scoped to the queue.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdmi%2Fazure-template-with-servicebus.json)
