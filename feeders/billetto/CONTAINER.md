<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/eu.png" alt="Europe" width="64" height="48"><br>
<sub><b>Europe</b></sub>
</td>
<td valign="middle">

# Billetto

<sub>pan-European ticketed public events · Kafka · MQTT · AMQP · <a href="https://billetto.com/">upstream</a> · <a href="https://developer.billetto.com/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Europe — pan-European ticketed public events

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#billetto) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#billetto/fabric-notebook) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/billetto.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://billetto.com/)

</td></tr></table>
<!-- source-hero:end -->

Related docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://billetto.com/>
- API / data documentation: <https://developer.billetto.com/>

<!-- upstream-links:end -->

- [README.md](README.md) — source context, quick-start flow, and deployment guidance.
- [EVENTS.md](EVENTS.md) — event families, CloudEvents types, and payload schemas.

## Why this container

These images package the Billetto Public Events bridge runtime so teams can run a production feeder with consistent event contracts across Kafka, MQTT, and AMQP transports.

## What ships in the box

| Image | Dockerfile | Purpose |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-billetto:latest` | `Dockerfile` | Kafka-compatible publishing path |
| `ghcr.io/clemensv/real-time-sources-billetto-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 publishing path |
| `ghcr.io/clemensv/real-time-sources-billetto-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 publishing path |

## Image contract

| Aspect | Kafka | MQTT | AMQP |
|---|---|---|---|
| Base image | `python:3.10-slim` | `python:3.10-slim` | `python:3.10-slim` |
| Default command | `CMD ["python", "-m", "billetto", "feed"]` | `CMD ["python", "-m", "billetto_mqtt", "feed"]` | `CMD ["python", "-m", "billetto_amqp", "feed"]` |
| Delivery format | CloudEvents to Kafka topic | CloudEvents to MQTT topic tree | CloudEvents to AMQP address |
| Shared contract | \- | Uses same xRegistry event model | Uses same xRegistry event model |

## Kafka image quick start

```bash
docker run --rm   -e CONNECTION_STRING="<connection-string>"   ghcr.io/clemensv/real-time-sources-billetto:latest
```

## MQTT image quick start

```bash
docker run --rm   -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-billetto-mqtt:latest
```

## AMQP image quick start

```bash
docker run --rm   -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/billetto"   ghcr.io/clemensv/real-time-sources-billetto-amqp:latest
```

## Environment variable matrix

### Common (all images)

| Variable | Description |
|---|---|
| `LOG_LEVEL` | Standard Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default `INFO`. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |
| `STATE_FILE` | Path to the JSON dedupe / resume state file. Mount persistent storage here for long-running deployments. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Source configuration

| Variable | Description |
|---|---|
| `SOURCE_MANIFEST` | Advanced: path to the xRegistry manifest the bridge loads at startup; defaults to the packaged copy under `/app/xreg/`. Normally only overridden in custom builds. |

### Kafka image (`ghcr.io/clemensv/real-time-sources-billetto:latest`)

| Variable | Purpose |
|---|---|
| `CONNECTION_STRING` | Event Hubs / Fabric custom-endpoint connection string; a shortcut supplying bootstrap server, credentials, and topic in one value. |
| `KAFKA_ENABLE_TLS` | Set `false` to disable TLS for local/plaintext brokers (default `true`). |
| `KAFKA_TOPIC` | Kafka topic the feeder publishes to. |
| `POLLING_INTERVAL` | Seconds between poll cycles. |
| `BILLETTO_API_KEYPAIR` | **Required.** Billetto API key pair used to authenticate upstream public-events API requests; obtain it from the Billetto developer portal before deployment. |
| `BILLETTO_BASE_URL` | Base URL of the Billetto public events API; override only to target a non-default environment. |
| `BILLETTO_CATEGORY` | Optional Billetto category slug to filter by. |
| `BILLETTO_SUBCATEGORY` | Optional Billetto subcategory slug to filter by within the chosen category. |
| `BILLETTO_EVENT_TYPE` | Optional Billetto event-type filter. |
| `BILLETTO_REGION` | Optional Billetto region filter. |
| `BILLETTO_SUBREGION` | Optional Billetto subregion filter within the chosen region. |
| `BILLETTO_MACROREGION` | Optional Billetto macro-region filter. |
| `BILLETTO_POSTAL_CODE` | Optional postal-code filter. |
| `BILLETTO_ORGANIZER_ID` | Optional filter restricting events to a single Billetto organizer ID. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-billetto-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `MQTT_BROKER_URL` | MQTT broker URL (`mqtt://` or `mqtts://host:port`). |
| `MQTT_USERNAME` | Username for MQTT `password` auth mode. |
| `MQTT_PASSWORD` | Password for MQTT `password` auth mode. |
| `MQTT_CLIENT_ID` | Stable MQTT client identifier; set a unique value per running instance. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra ID (Azure Event Grid). |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-billetto-amqp:latest`)

| Variable | Purpose |
|---|---|
| `AMQP_BROKER_URL` | AMQP 1.0 connection URL shortcut (host, port, TLS, credentials). |
| `AMQP_ADDRESS` | AMQP destination address (queue/topic/entity) to publish to. |
| `AMQP_AUTH_MODE` | AMQP authentication mode — `password` (SASL PLAIN), `entra` (Service Bus + Microsoft Entra CBS), or `sas` (SAS-token CBS). |
| `AMQP_ENTRA_CLIENT_ID` | Managed-identity client ID for AMQP `entra` auth mode (optional). |
| `AMQP_SAS_KEY_NAME / AMQP_SAS_KEY` | Shared Access key name and key, required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_ENTRA_AUDIENCE` | Token audience for `entra` mode (default `https://servicebus.azure.net/.default`). |
| `AMQP_HOST` | AMQP broker host (component-level alternative to `AMQP_BROKER_URL`). |
| `AMQP_PASSWORD` | SASL PLAIN password, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_PORT` | AMQP broker port (default `5672`, or `5671` with TLS). |
| `AMQP_TLS` | Set `true` to use TLS (`amqps`) for the component-level connection. |
| `AMQP_USERNAME` | SASL PLAIN username, used when `AMQP_AUTH_MODE=password` (default). |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-amqp.json` — AMQP deployment targeting an existing AMQP 1.0 broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbilletto%2Fazure-template-amqp.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbilletto%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbilletto%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbilletto%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbilletto%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fbilletto%2Fazure-template.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
