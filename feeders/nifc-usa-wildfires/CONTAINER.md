<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/us.png" alt="United States" width="64" height="48"><br>
<sub><b>United States</b></sub>
</td>
<td valign="middle">

# NIFC USA Wildfires

<sub>active wildfire incidents, NIFC · Kafka · MQTT · AMQP · <a href="https://www.nifc.gov/">upstream</a> · <a href="https://data-nifc.opendata.arcgis.com/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> United States — active wildfire incidents, NIFC

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#nifc-usa-wildfires) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/nifc-usa-wildfires.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.nifc.gov/)

</td></tr></table>
<!-- source-hero:end -->

This container image provides a bridge between the [National Interagency Fire
Center (NIFC)](https://www.nifc.gov/) ArcGIS Feature Service and Apache Kafka,
Azure Event Hubs, and Fabric Event Streams. The bridge fetches active wildfire
incident data and forwards them to the configured Kafka endpoints.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.nifc.gov/>
- API / data documentation: <https://data-nifc.opendata.arcgis.com/>

<!-- upstream-links:end -->

## NIFC USA Wildfires

The [NIFC](https://www.nifc.gov/) provides real-time wildfire incident data
from the Integrated Reporting of Wildland-Fire Information (IRWIN) system via
an ArcGIS Feature Service. The data includes fire location, size, containment
status, cause, personnel, and structural damage.

## Functionality

The bridge polls the NIFC ArcGIS Feature Service at regular intervals (default:
every 5 minutes) and writes wildfire incident events to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest
```

## Image contract

| Image tag | Transport | Dockerfile | Persistent state share |
|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest` | Kafka / Event Hubs | `Dockerfile` | Yes - stores `NIFC_LAST_POLLED_FILE` dedupe state |
| `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires-mqtt:latest` | MQTT 5 | `Dockerfile.mqtt` | No |
| `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | Yes - stores `STATE_FILE` dedupe state |

## Using the Container Image

The container defines a command that starts the bridge, reading wildfire data
from the NIFC feed and writing it to Kafka, Azure Event Hubs, or Fabric Event
Streams.

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to connect to Azure Event Hubs
or Fabric Event Streams.

### `KAFKA_BOOTSTRAP_SERVERS`

The address of the Kafka broker (e.g., `broker1:9092,broker2:9092`).

### `KAFKA_TOPIC`

The Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `LOG_LEVEL`

The logging level. Default: `INFO`.

### `NIFC_LAST_POLLED_FILE`

The file path where the bridge stores the IDs of previously processed incidents
to avoid duplication after restarts. Default:
`~/.nifc_usa_wildfires_last_polled.json`.

### `NIFC_USA_WILDFIRES_SAMPLE_MODE`

Emit built-in sample wildfire incidents instead of polling the live NIFC feed.
Accepts `1`, `true`, or `yes`.

### `KAFKA_ENABLE_TLS`

Enable TLS for Kafka connections. Default: `true`. Set to `false` for
unencrypted connections.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnifc-usa-wildfires%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fnifc-usa-wildfires%2Fazure-template-with-eventhub.json)


## MQTT and AMQP companion feeders

This source now ships separate Kafka, MQTT, and AMQP containers. The MQTT companion publishes binary-mode CloudEvents to `wildfire/us/nifc/nifc-usa-wildfires/{state}/{status}/{irwin_id}/incident`, where `status` is one of `active`, `contained`, `controlled`, or `out`. The AMQP companion publishes the same CloudEvents to AMQP 1.0 brokers or Azure Service Bus using the IRWIN id subject and `state`/`status` application properties.

Images: `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires-mqtt:latest`, `ghcr.io/clemensv/real-time-sources-nifc-usa-wildfires-amqp:latest`. Deployment templates: `azure-template-mqtt.json`, `azure-template-with-eventgrid-mqtt.json`, `azure-template-with-servicebus.json`, and `infra/azure-template-amqp.json`.
