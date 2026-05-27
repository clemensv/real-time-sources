<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Any" width="64" height="48"><br>
<sub><b>Any</b></sub>
</td>
<td valign="middle">

# RSS Feeds

<sub>configurable RSS/Atom feed URLs or OPML files · Kafka · MQTT · AMQP · <a href="https://www.rssboard.org/rss-specification">upstream</a> · <a href="https://www.rssboard.org/rss-specification">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-2_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Any — configurable RSS/Atom feed URLs or OPML files

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#rss) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/feeds.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.rssboard.org/rss-specification)

</td></tr></table>
<!-- source-hero:end -->

Related docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.rssboard.org/rss-specification>
- API / data documentation: <https://www.rssboard.org/rss-specification>

<!-- upstream-links:end -->

- [README.md](README.md) — source context, quick-start flow, and deployment guidance.
- [EVENTS.md](EVENTS.md) — event families, CloudEvents types, and payload schemas.

## Why this container

These images package the RSS/Atom bridge runtime so teams can run a production feeder with consistent event contracts across Kafka, MQTT, and AMQP transports.

## What ships in the box

| Image | Dockerfile | Purpose |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-rss:latest` | `Dockerfile` | Kafka-compatible publishing path |
| `ghcr.io/clemensv/real-time-sources-rss-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 publishing path |
| `ghcr.io/clemensv/real-time-sources-rss-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 publishing path |

## Image contract

| Aspect | Kafka | MQTT | AMQP |
|---|---|---|---|
| Base image | `python:3.10-slim` | `python:3.10-slim` | `python:3.10-slim` |
| Default command | `CMD ["python", "-m", "rssbridge", "process"]` | `CMD ["python", "-m", "rssbridge_mqtt", "process"]` | `CMD ["python", "-m", "rssbridge_amqp", "feed"]` |
| Delivery format | CloudEvents to Kafka topic | CloudEvents to MQTT topic tree | CloudEvents to AMQP address |
| Shared contract | \- | Uses same xRegistry event model | Uses same xRegistry event model |

## Kafka image quick start

```bash
docker run --rm   -e CONNECTION_STRING="<connection-string>" -e FEED_URLS="https://example.com/feed.xml"   ghcr.io/clemensv/real-time-sources-rss:latest
```

## MQTT image quick start

```bash
docker run --rm   -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>" -e FEED_URLS="https://example.com/feed.xml"   ghcr.io/clemensv/real-time-sources-rss-mqtt:latest
```

## AMQP image quick start

```bash
docker run --rm   -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/rss" -e FEED_URLS="https://example.com/feed.xml"   ghcr.io/clemensv/real-time-sources-rss-amqp:latest
```

## Environment variable matrix

### Kafka image (`ghcr.io/clemensv/real-time-sources-rss:latest`)

| Variable | Purpose |
|---|---|
| `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS` | Core configuration for this image variant. |
| `KAFKA_TOPIC` | Core configuration for this image variant. |
| `SASL_USERNAME / SASL_PASSWORD` | Core configuration for this image variant. |
| `KAFKA_ENABLE_TLS` | Core configuration for this image variant. |
| `FEED_URLS` | Core configuration for this image variant. |
| `STATE_DIR` | Core configuration for this image variant. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-rss-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `MQTT_BROKER_URL` | Core configuration for this image variant. |
| `MQTT_USERNAME` | Core configuration for this image variant. |
| `MQTT_PASSWORD` | Core configuration for this image variant. |
| `MQTT_CLIENT_ID` | Core configuration for this image variant. |
| `MQTT_CONTENT_MODE` | Core configuration for this image variant. |
| `FEED_URLS` | Core configuration for this image variant. |
| `STATE_DIR` | Core configuration for this image variant. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-rss-amqp:latest`)

| Variable | Purpose |
|---|---|
| `AMQP_BROKER_URL` | Core configuration for this image variant. |
| `AMQP_ADDRESS` | Core configuration for this image variant. |
| `AMQP_AUTH_MODE` | Core configuration for this image variant. |
| `AMQP_CONTENT_MODE` | Core configuration for this image variant. |
| `FEED_URLS` | Core configuration for this image variant. |
| `STATE_DIR` | Core configuration for this image variant. |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Frss%2Fazure-template-with-eventhub.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Frss%2Fazure-template.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
