<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/fi.png" alt="Finland / Baltic Sea" width="64" height="48"><br>
<sub><b>Finland / Baltic Sea</b></sub>
</td>
<td valign="middle">

# Digitraffic Maritime

<sub>AIS via MQTT · Kafka · MQTT · AMQP · <a href="https://www.digitraffic.fi/en/marine-traffic/">upstream</a> · <a href="https://meri.digitraffic.fi/swagger/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Finland / Baltic Sea — AIS via MQTT

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#digitraffic-maritime) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/digitraffic_maritime.kql) &nbsp;·&nbsp;
[🗺️ **Fabric Map**](fabric/README.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.digitraffic.fi/en/marine-traffic/)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI images for the Digitraffic Maritime feeder and their runtime contract. See [README.md](README.md) for source overview and [EVENTS.md](EVENTS.md) for the CloudEvents schema/routing contract.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.digitraffic.fi/en/marine-traffic/>
- API / data documentation: <https://meri.digitraffic.fi/swagger/>

<!-- upstream-links:end -->

## Why this container

These images package the upstream connector, CloudEvents normalization, and transport-specific publisher wiring into ready-to-run artifacts for Kafka deployments.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-digitraffic-maritime` | Kafka | Topic(s): `digitraffic-maritime`, key = `{locode}`, `{mmsi}`, `{port_call_id}`, `{vessel_id}` |

Event families (base groups):

- `fi.digitraffic.marine.ais`
- `fi.digitraffic.marine.portcall`
- `fi.digitraffic.marine.portcall.vesseldetails`
- `fi.digitraffic.marine.portcall.portlocation`

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.12-slim` |
| Default entry point | Kafka: `["python", "-m", "digitraffic_maritime", "stream"]` |
| Exposed ports | none — outbound publisher only |
| Signals | graceful shutdown on `SIGTERM` |
| State | `DIGITRAFFIC_PORTCALL_STATE_FILE` |
| Image tags | `:latest`, `:sha-<git-sha>`, release tags |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

## Using the Kafka image

### With Azure Event Hubs / Fabric Event Streams (connection string)

```bash
docker run --rm \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

### With Kafka broker parameters (SASL/PLAIN)

```bash
docker run --rm \
  -e KAFKA_BOOTSTRAP_SERVERS='<host:port>' \
  -e KAFKA_TOPIC='digitraffic-maritime' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

## Environment variables

### Source configuration

| Variable | Description |
|---|---|
| `DIGITRAFFIC_FILTER_MMSI` | Comma-separated MMSI numbers to include (default: all). |
| `DIGITRAFFIC_FLUSH_INTERVAL` | Flush Kafka producer every N events (default `1000`). |
| `DIGITRAFFIC_MODE` | Acquisition mode — `stream` consumes the live MQTT firehose (default `stream`). |
| `DIGITRAFFIC_PORTCALL_POLL_INTERVAL` | Poll interval in seconds for the port call REST feed (default `300`). |
| `DIGITRAFFIC_SUBSCRIBE` | Comma-separated: location,metadata (default: both) (default `location,metadata`). |

### Common

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string for Kafka-mode publishing. |
| `KAFKA_ENABLE_TLS` | Set `false` for local/plain Kafka; default `true`. |
| `DIGITRAFFIC_PORTCALL_STATE_FILE` | Source-specific state/resume setting. |
| `LOG_LEVEL` | Standard Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default `INFO`. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Kafka image

| Variable | Description |
|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list (`host:port,...`). |
| `KAFKA_TOPIC` | Destination topic (default from contract). |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials for Kafka-compatible brokers. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL, e.g. `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra ID (Azure Event Grid). |
| `MQTT_CLIENT_ID` | MQTT client identifier. |
| `MQTT_CA_FILE` | Path to a CA certificate bundle for verifying the broker's TLS certificate. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_USERNAME` | Username when `MQTT_AUTH_MODE=password` (default). |
| `MQTT_PASSWORD` | Password when `MQTT_AUTH_MODE=password` (default). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL, e.g. `amqp://user:pw@host:5672/address` or `amqps://host:5671/address`. |
| `AMQP_ADDRESS` | AMQP node (queue / topic) name to publish to. |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS (Service Bus / Event Hubs), or `sas` for SAS-token CBS. |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |
| `AMQP_ENTRA_AUDIENCE` | Token audience for `entra` mode (default `https://servicebus.azure.net/.default`). |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `AMQP_HOST` | AMQP broker host (component-level alternative to `AMQP_BROKER_URL`). |
| `AMQP_PORT` | AMQP broker port (default `5672`, or `5671` with TLS). |
| `AMQP_TLS` | Set `true` to use TLS (`amqps`) for the component-level connection. |
| `AMQP_USERNAME` | SASL PLAIN username, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_PASSWORD` | SASL PLAIN password, used when `AMQP_AUTH_MODE=password` (default). |


## Deploying into Azure Container Instances

One deploy button is provided per ARM template file present in this folder:

- **azure-template-with-eventhub.json** (with eventhub)
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdigitraffic-maritime%2Fazure-template-with-eventhub.json)
- **azure-template.json** (default (BYO Event Hubs/Kafka))
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdigitraffic-maritime%2Fazure-template.json)

## Related

- [README.md](README.md) — source overview and quick-start guidance.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schemas.
- [`xreg/digitraffic_maritime.xreg.json`](xreg/digitraffic_maritime.xreg.json) — authoritative xRegistry manifest.
