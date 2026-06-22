<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# Bluesky Firehose

<sub>posts, likes, reposts, follows · Kafka · MQTT · AMQP · <a href="https://bsky.app/">upstream</a> · <a href="https://docs.bsky.app/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — posts, likes, reposts, follows

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#bluesky) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/bluesky.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://bsky.app/)

</td></tr></table>
<!-- source-hero:end -->

Related docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://bsky.app/>
- API / data documentation: <https://docs.bsky.app/>

<!-- upstream-links:end -->

- [README.md](README.md) — source context, quick-start flow, and deployment guidance.
- [EVENTS.md](EVENTS.md) — event families, CloudEvents types, and payload schemas.

## Why this container

These images package the Bluesky Firehose bridge runtime so teams can run a production feeder with consistent event contracts across Kafka, MQTT, and AMQP transports.

## What ships in the box

| Image | Dockerfile | Purpose |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-bluesky:latest` | `Dockerfile` | Kafka-compatible publishing path |
| `ghcr.io/clemensv/real-time-sources-bluesky-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 publishing path |
| `ghcr.io/clemensv/real-time-sources-bluesky-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 publishing path |

## Image contract

| Aspect | Kafka | MQTT | AMQP |
|---|---|---|---|
| Base image | `python:3.10-slim` | `python:3.10-slim` | `python:3.10-slim` |
| Default command | `CMD ["python", "-m", "bluesky", "stream"]` | `CMD ["python", "-m", "bluesky_mqtt", "feed"]` | `CMD ["python", "-m", "bluesky_amqp", "feed"]` |
| Delivery format | CloudEvents to Kafka topic | CloudEvents to MQTT topic tree | CloudEvents to AMQP address |
| Shared contract | \- | Uses same xRegistry event model | Uses same xRegistry event model |

## Kafka image quick start

```bash
docker run --rm   -e CONNECTION_STRING="<connection-string>"   ghcr.io/clemensv/real-time-sources-bluesky:latest
```

## MQTT image quick start

```bash
docker run --rm   -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-bluesky-mqtt:latest
```

## AMQP image quick start

```bash
docker run --rm   -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/bluesky"   ghcr.io/clemensv/real-time-sources-bluesky-amqp:latest
```

## Environment variable matrix

### Common (all images)

| Variable | Description |
|---|---|
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Source configuration

| Variable | Description |
|---|---|
| `BLUESKY_MAX_EVENTS` | Optional cap on the number of events emitted before the feeder exits; `0` means run indefinitely (mainly for testing) (default `0`). |
| `BOTFINDER_KUSTO_DATABASE` | Kusto database name for the optional offline bot-finder analysis tool (also `--kusto-database`); not used by the live feeder. |
| `BOTFINDER_KUSTO_URI` | Kusto cluster URI for the optional offline bot-finder analysis tool (also `--kusto-uri`); not used by the live feeder. |
| `CLOUDEVENTS_MODE` | CloudEvents encoding mode — `structured` or `binary` (default `structured`). |
| `CONTENT_TYPE` | Event payload content type — `application/json` or `application/vnd.apache.avro+avro` (default `application/json`). |
| `USE_COMPRESSION` | Set to a truthy value to gzip-compress the emitted CloudEvent payloads. |

### Kafka image (`ghcr.io/clemensv/real-time-sources-bluesky:latest`)

| Variable | Purpose |
|---|---|
| `CONNECTION_STRING` | Event Hubs / Fabric custom-endpoint connection string; a shortcut supplying bootstrap server, credentials, and topic in one value. |
| `BLUESKY_FIREHOSE_URL` | Bluesky firehose WebSocket endpoint URL. |
| `BLUESKY_COLLECTIONS` | Comma-separated AT Protocol collection NSIDs to emit (for example `app.bsky.feed.post`). |
| `BLUESKY_SAMPLE_RATE` | Fraction (0–1) of firehose events to sample and emit. |
| `BLUESKY_CURSOR_FILE` | Path to the firehose cursor file used to resume the stream after restarts. |
| `KAFKA_ENABLE_TLS` | Set `false` to disable TLS for local/plaintext brokers (default `true`). |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated `host:port` list of TLS-enabled Kafka brokers. |
| `KAFKA_TOPIC` | Target Kafka topic. |
| `SASL_PASSWORD` | SASL PLAIN password. For Event Hubs use the full connection string. |
| `SASL_USERNAME` | SASL PLAIN username. For Event Hubs use `$ConnectionString`. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-bluesky-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `MQTT_BROKER_URL` | MQTT broker URL (`mqtt://` or `mqtts://host:port`). |
| `MQTT_USERNAME` | Username for MQTT `password` auth mode. |
| `MQTT_PASSWORD` | Password for MQTT `password` auth mode. |
| `MQTT_CLIENT_ID` | Stable MQTT client identifier; set a unique value per running instance. |
| `BLUESKY_COLLECTIONS` | Comma-separated AT Protocol collection NSIDs to emit (for example `app.bsky.feed.post`). |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra ID (Azure Event Grid). |
| `MQTT_ENABLE_TLS` | Set `true` to use TLS (`mqtts`) for the MQTT connection. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-bluesky-amqp:latest`)

| Variable | Purpose |
|---|---|
| `AMQP_BROKER_URL` | AMQP 1.0 connection URL shortcut (host, port, TLS, credentials). |
| `AMQP_ADDRESS` | AMQP destination address (queue/topic/entity) to publish to. |
| `AMQP_AUTH_MODE` | AMQP authentication mode — `password` (SASL PLAIN), `entra` (Service Bus + Microsoft Entra CBS), or `sas` (SAS-token CBS). |
| `AMQP_CONTENT_MODE` | CloudEvents content mode for AMQP — `binary` or `structured`. |
| `BLUESKY_COLLECTIONS` | Comma-separated AT Protocol collection NSIDs to emit (for example `app.bsky.feed.post`). |
| `AMQP_ENTRA_AUDIENCE` | Token audience for `entra` mode (default `https://servicebus.azure.net/.default`). |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |
| `AMQP_HOST` | AMQP broker host (component-level alternative to `AMQP_BROKER_URL`). |
| `AMQP_PASSWORD` | SASL PLAIN password, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_PORT` | AMQP broker port (default `5672`, or `5671` with TLS). |
| `AMQP_SAS_KEY` | SAS key value (base64-encoded shared secret). Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name (e.g. `RootManageSharedAccessKey`). Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_TLS` | Set `true` to use TLS (`amqps`) for the component-level connection. |
| `AMQP_USERNAME` | SASL PLAIN username, used when `AMQP_AUTH_MODE=password` (default). |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbluesky%2Fazure-template-with-eventhub.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbluesky%2Fazure-template.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbluesky%2Fazure-template-with-servicebus.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid MQTT provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbluesky%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbluesky%2Fazure-template-mqtt.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
