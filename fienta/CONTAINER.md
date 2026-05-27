<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/eu.png" alt="Europe" width="64" height="48"><br>
<sub><b>Europe</b></sub>
</td>
<td valign="middle">

# Fienta

<sub>ticketed public events with sale-status signals · Kafka · MQTT · AMQP · <a href="https://fienta.com/">upstream</a> · <a href="https://fienta.com/api-public-events">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Europe — ticketed public events with sale-status signals

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#fienta) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/fienta.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://fienta.com/)

</td></tr></table>
<!-- source-hero:end -->

Related docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://fienta.com/>
- API / data documentation: <https://fienta.com/api-public-events>

<!-- upstream-links:end -->

- [README.md](README.md) — source context, quick-start flow, and deployment guidance.
- [EVENTS.md](EVENTS.md) — event families, CloudEvents types, and payload schemas.

> [!IMPORTANT]
> Redistribution and downstream use must comply with [Fienta Terms of Service](https://fienta.com/terms).

## Why this container

These images package the Fienta Public Events bridge runtime so teams can run a production feeder with consistent event contracts across Kafka, MQTT, and AMQP transports.

## What ships in the box

| Image | Dockerfile | Purpose |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-fienta:latest` | `Dockerfile` | Kafka-compatible publishing path |
| `ghcr.io/clemensv/real-time-sources-fienta-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 publishing path |
| `ghcr.io/clemensv/real-time-sources-fienta-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 publishing path |

## Image contract

| Aspect | Kafka | MQTT | AMQP |
|---|---|---|---|
| Base image | `python:3.10-slim` | `python:3.10-slim` | `python:3.10-slim` |
| Default command | `CMD ["python", "-m", "fienta", "feed"]` | `CMD ["python", "-m", "fienta_mqtt", "feed"]` | `CMD ["python", "-m", "fienta_amqp", "feed"]` |
| Delivery format | CloudEvents to Kafka topic | CloudEvents to MQTT topic tree | CloudEvents to AMQP address |
| Shared contract | \- | Uses same xRegistry event model | Uses same xRegistry event model |

## Kafka image quick start

```bash
docker run --rm   -e CONNECTION_STRING="<connection-string>" -e FIENTA_COUNTRY="EE" -e FIENTA_LOCALE="en"   ghcr.io/clemensv/real-time-sources-fienta:latest
```

## MQTT image quick start

```bash
docker run --rm   -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-fienta-mqtt:latest
```

## AMQP image quick start

```bash
docker run --rm   -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/fienta"   ghcr.io/clemensv/real-time-sources-fienta-amqp:latest
```

## Environment variable matrix

### Kafka image (`ghcr.io/clemensv/real-time-sources-fienta:latest`)

| Variable | Purpose |
|---|---|
| `CONNECTION_STRING` | Core configuration for this image variant. |
| `KAFKA_ENABLE_TLS` | Core configuration for this image variant. |
| `FIENTA_STATE_FILE` | Core configuration for this image variant. |
| `FIENTA_COUNTRY` | Core configuration for this image variant. |
| `FIENTA_LOCALE` | Core configuration for this image variant. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-fienta-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `MQTT_BROKER_URL` | Core configuration for this image variant. |
| `MQTT_USERNAME` | Core configuration for this image variant. |
| `MQTT_PASSWORD` | Core configuration for this image variant. |
| `MQTT_CLIENT_ID` | Core configuration for this image variant. |
| `FIENTA_COUNTRY` | Core configuration for this image variant. |
| `FIENTA_LOCALE` | Core configuration for this image variant. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-fienta-amqp:latest`)

| Variable | Purpose |
|---|---|
| `AMQP_BROKER_URL` | Core configuration for this image variant. |
| `AMQP_ADDRESS` | Core configuration for this image variant. |
| `AMQP_AUTH_MODE` | Core configuration for this image variant. |
| `FIENTA_COUNTRY` | Core configuration for this image variant. |
| `FIENTA_LOCALE` | Core configuration for this image variant. |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-amqp.json` — AMQP deployment targeting an existing AMQP 1.0 broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-amqp.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffienta%2Fazure-template.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
