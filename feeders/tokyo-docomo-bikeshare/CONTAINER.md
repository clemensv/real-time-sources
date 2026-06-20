<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/jp.png" alt="Tokyo" width="64" height="48"><br>
<sub><b>Tokyo</b></sub>
</td>
<td valign="middle">

# Tokyo Docomo Bikeshare

<sub>1,794 stations, GBFS 2.3 via ODPT · Kafka · MQTT · AMQP · <a href="https://docomo-cycle.jp/tokyo/">upstream</a> · <a href="https://developer.odpt.org/info">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-2_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Tokyo, Japan — 1,794 stations, GBFS 2.3 via ODPT

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#tokyo-docomo-bikeshare) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://docomo-cycle.jp/tokyo/)

</td></tr></table>
<!-- source-hero:end -->

Related docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://docomo-cycle.jp/tokyo/>
- API / data documentation: <https://developer.odpt.org/info>

<!-- upstream-links:end -->

- [README.md](README.md) — source context, quick-start flow, and deployment guidance.
- [EVENTS.md](EVENTS.md) — event families, CloudEvents types, and payload schemas.

## Why this container

These images package the Tokyo Docomo Bikeshare bridge runtime so teams can run a production feeder with consistent event contracts across Kafka, MQTT, and AMQP transports.

## What ships in the box

| Image | Dockerfile | Purpose |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest` | `Dockerfile` | Kafka-compatible publishing path |
| `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 publishing path |
| `ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 publishing path |

## Image contract

| Aspect | Kafka | MQTT | AMQP |
|---|---|---|---|
| Base image | `python:3.10-slim` | `python:3.10-slim` | `python:3.10-slim` |
| Default command | `CMD ["python", "-m", "tokyo_docomo_bikeshare"]` | `CMD ["python", "-m", "tokyo_docomo_bikeshare_mqtt", "feed"]` | `CMD ["python", "-m", "tokyo_docomo_bikeshare_amqp", "feed"]` |
| Delivery format | CloudEvents to Kafka topic | CloudEvents to MQTT topic tree | CloudEvents to AMQP address |
| Shared contract | \- | Uses same xRegistry event model | Uses same xRegistry event model |

## Kafka image quick start

```bash
docker run --rm   -e CONNECTION_STRING="<connection-string>"   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest
```

## MQTT image quick start

```bash
docker run --rm   -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest
```

## AMQP image quick start

```bash
docker run --rm   -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/tokyo-docomo-bikeshare"   ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest
```

## Environment variable matrix

### Kafka image (`ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare:latest`)

| Variable | Purpose |
|---|---|
| `GBFS_API_KEY` | ODPT access token required by the Tokyo Docomo Bikeshare GBFS feed. Read from the environment and passed only to upstream requests. |
| `CONNECTION_STRING` | Core configuration for this image variant. |
| `KAFKA_ENABLE_TLS` | Core configuration for this image variant. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `MQTT_BROKER_URL` | Core configuration for this image variant. |
| `MQTT_USERNAME` | Core configuration for this image variant. |
| `MQTT_PASSWORD` | Core configuration for this image variant. |
| `MQTT_TLS` | Core configuration for this image variant. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-tokyo-docomo-bikeshare-amqp:latest`)

| Variable | Purpose |
|---|---|
| `AMQP_BROKER_URL or AMQP_HOST/AMQP_PORT/AMQP_ADDRESS` | Core configuration for this image variant. |
| `AMQP_USERNAME` | Core configuration for this image variant. |
| `AMQP_PASSWORD` | Core configuration for this image variant. |
| `AMQP_AUTH_MODE` | Core configuration for this image variant. |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Ftokyo-docomo-bikeshare%2Fazure-template-with-eventgrid-mqtt.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
