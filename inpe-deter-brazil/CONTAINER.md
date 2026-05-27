<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/br.png" alt="Brazil" width="64" height="48"><br>
<sub><b>Brazil</b></sub>
</td>
<td valign="middle">

# INPE DETER Brazil

<sub>Amazon & Cerrado deforestation alerts · Kafka · MQTT · AMQP · <a href="http://terrabrasilis.dpi.inpe.br/">upstream</a> · <a href="http://terrabrasilis.dpi.inpe.br/geoserver/web/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Brazil — Amazon & Cerrado deforestation alerts

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#inpe-deter-brazil) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/inpe_deter_brazil.kql) &nbsp;·&nbsp;
[↗ **Upstream**](http://terrabrasilis.dpi.inpe.br/)

</td></tr></table>
<!-- source-hero:end -->

This container image provides a bridge between [INPE
TerraBrasilis DETER](http://terrabrasilis.dpi.inpe.br/) deforestation alert
feeds and Apache Kafka, Azure Event Hubs, and Fabric Event Streams. The bridge
fetches deforestation alerts from the Amazon and Cerrado biomes and forwards
them to the configured Kafka endpoints.

<!-- upstream-links:begin -->
## Upstream

- Home page: <http://terrabrasilis.dpi.inpe.br/>
- API / data documentation: <http://terrabrasilis.dpi.inpe.br/geoserver/web/>

<!-- upstream-links:end -->

## INPE TerraBrasilis DETER

[INPE DETER](http://terrabrasilis.dpi.inpe.br/) is Brazil's National Institute
for Space Research (INPE) real-time deforestation detection system. It monitors
the Amazon and Cerrado biomes using satellite imagery and publishes detected
deforestation polygons via OGC WFS (Web Feature Service) endpoints.

## Functionality

The bridge polls the INPE DETER WFS endpoints at regular intervals and writes
deforestation alerts to a Kafka topic as [CloudEvents](https://cloudevents.io/)
in JSON format, documented in [EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-inpe-deter-brazil:latest
```

## Using the Container Image

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-inpe-deter-brazil:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-inpe-deter-brazil:latest
```

### With an MQTT 5.0 broker

Use the MQTT image variant to publish binary-mode CloudEvents into the UNS topic tree `deforestation/br/inpe/inpe-deter-brazil/{biome}/{state_slug}/{class_slug}/{alert_id}/alert`:

```shell
$ docker run --rm \
    -e MQTT_BROKER_URL='mqtt://broker:1883' \
    ghcr.io/clemensv/real-time-sources-inpe-deter-brazil-mqtt:latest
```

QoS is 1, retained messages are disabled, and queued PUBLISH packets expire after 7 days. Consumers should deduplicate by `alert_id`.

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker.

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `LOG_LEVEL`

The logging level. Default: `INFO`.

### `MQTT_BROKER_URL`

MQTT broker URL for the MQTT image variant. Supports `mqtt://` and `mqtts://`.

### `MQTT_USERNAME` / `MQTT_PASSWORD` / `MQTT_CLIENT_ID`

Optional MQTT authentication and client identity settings for the MQTT image variant.

### `INPE_BIOMES`

Optional comma-separated biome filter for the MQTT image variant. Defaults to `amazon,cerrado`.

### `INPE_DETER_LAST_POLLED_FILE`

The file path where the bridge stores the last polled state. Default:
`~/.inpe_deter_brazil_last_polled.json`.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template-with-eventhub.json)

## AMQP 1.0 container

The AMQP companion image publishes the same `Inpe Deter Brazil` CloudEvents to a generic AMQP 1.0 broker, Azure Service Bus with Entra ID CBS, or a SAS-token Service Bus-compatible endpoint.

```bash
docker pull ghcr.io/clemensv/real-time-sources-inpe-deter-brazil-amqp:latest
```

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=inpe-deter-brazil   ghcr.io/clemensv/real-time-sources-inpe-deter-brazil-amqp:latest
```

### Azure Service Bus (Entra ID)

```bash
docker run --rm   -e AMQP_HOST=<namespace>.servicebus.windows.net   -e AMQP_PORT=5671   -e AMQP_TLS=true   -e AMQP_ADDRESS=inpe-deter-brazil   -e AMQP_AUTH_MODE=entra   -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default   ghcr.io/clemensv/real-time-sources-inpe-deter-brazil-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm   -e AMQP_HOST=servicebus-emulator   -e AMQP_PORT=5672   -e AMQP_ADDRESS=inpe-deter-brazil   -e AMQP_AUTH_MODE=sas   -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey   -e AMQP_SAS_KEY=<base64-key>   ghcr.io/clemensv/real-time-sources-inpe-deter-brazil-amqp:latest
```

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Optional AMQP URI for generic brokers. | unset |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when no URI is supplied. | `localhost` / `5672` |
| `AMQP_ADDRESS` | Queue/topic/address to publish to. | `inpe-deter-brazil` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | unset |
| `AMQP_TLS` | Use TLS (`true`, `1`, or `yes`). | `false` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra token scope and optional managed identity client ID. | Service Bus scope / unset |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials. | unset |
| `AMQP_CONTENT_MODE` | CloudEvents content mode: `binary` or `structured`. | `binary` |

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Finpe-deter-brazil%2Fazure-template-amqp.json)

