<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# GDACS

<sub>earthquakes, floods, cyclones, volcanoes, droughts · Kafka · MQTT · AMQP · <a href="https://www.gdacs.org/">upstream</a> · <a href="https://www.gdacs.org/xml/rss.xml">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-3_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — earthquakes, floods, cyclones, volcanoes, droughts

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#gdacs) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/gdacs.kql) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.gdacs.org/)

</td></tr></table>
<!-- source-hero:end -->

This container image provides a bridge between the [Global Disaster Alert and
Coordination System (GDACS)](https://www.gdacs.org) RSS feed and Apache Kafka,
Azure Event Hubs, and Fabric Event Streams. The bridge polls GDACS for disaster
alerts worldwide and forwards them to the configured Kafka endpoints.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.gdacs.org/>
- API / data documentation: <https://www.gdacs.org/xml/rss.xml>

<!-- upstream-links:end -->

## GDACS

The [Global Disaster Alert and Coordination System](https://www.gdacs.org) is a
joint initiative of the United Nations and the European Commission that provides
near-real-time alerts about natural disasters around the world, including
earthquakes, tropical cyclones, floods, volcanic eruptions, forest fires, and
droughts. The RSS feed is updated within minutes of event detection.

## Functionality

The bridge polls the GDACS RSS feed at regular intervals (default: 5 minutes)
and writes disaster alert events to a Kafka topic as
[CloudEvents](https://cloudevents.io/) in JSON format, documented in
[EVENTS.md](EVENTS.md).

State tracking ensures only new or updated alert episodes are emitted. The
bridge persists a state file mapping each event+episode combination to its
version number, so restarts do not cause duplicate emissions.

## Database Schemas and Handling

If you want to build a full data pipeline with all events ingested into a
database, the integration with Fabric Eventhouse and Azure Data Explorer is
described in [DATABASE.md](../DATABASE.md).

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-gdacs:latest
```

To use it as a base image in a Dockerfile:

```dockerfile
FROM ghcr.io/clemensv/real-time-sources-gdacs:latest
```

## Image contract

| Image | Dockerfile | Transport | Persistent state |
|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-gdacs:latest` | `Dockerfile` | Kafka / Event Hubs | Yes (`GDACS_STATE_FILE`) |
| `ghcr.io/clemensv/real-time-sources-gdacs-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 | Yes (`STATE_FILE` when configured) |
| `ghcr.io/clemensv/real-time-sources-gdacs-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 | Yes (`STATE_FILE`) |

## Using the Container Image

The container defines a command that starts the bridge, reading disaster alerts
from the GDACS RSS feed and writing them to Kafka, Azure Event Hubs, or Fabric
Event Streams.

### With a Kafka Broker

Ensure you have a Kafka broker configured with TLS and SASL PLAIN
authentication. Run the container with the following command:

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='gdacs' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-gdacs:latest
```

### With Azure Event Hubs or Fabric Event Streams

Use the connection string from Azure Event Hubs or Microsoft Fabric Event
Streams:

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-gdacs:latest
```

## Environment Variables

### Common (all images)

| Variable | Description |
|---|---|
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Source configuration

| Variable | Description |
|---|---|
| `GDACS_MQTT_STATE_FILE` | Path to the MQTT image dedupe state file (default `~/.gdacs_mqtt_state.json`). |
| `GDACS_POLL_INTERVAL` | Seconds between GDACS disaster-feed polls (default `300`). |
| `MAX_SIZE` | Maximum number of records to fetch and emit per poll cycle (default `1000`). |
| `STATION_FILTER` | Comma-separated event/area identifiers to include; empty includes all. |
| `GDACS_MOCK` | Set to a truthy value to emit deterministic offline GDACS sample data (offline testing / Docker E2E). |
| `GDACS_SAMPLE_MODE` | Set to a truthy value to emit a bundled GDACS sample payload once (offline testing). |

| Variable | Description | Required |
|---|---|---|
| `CONNECTION_STRING` | Azure Event Hubs or Fabric Event Stream connection string | Yes (or use `KAFKA_BOOTSTRAP_SERVERS`) |
| `GDACS_CONNECTION_STRING` | Feeder-specific alias for `CONNECTION_STRING`; Azure templates set both so the bridge works with either name. | No |
| `KAFKA_BOOTSTRAP_SERVERS` | Comma-separated list of Kafka bootstrap servers | Yes (or use `CONNECTION_STRING`) |
| `KAFKA_TOPIC` | Kafka topic name (default from connection string) | No |
| `SASL_USERNAME` | SASL PLAIN username | No |
| `SASL_PASSWORD` | SASL PLAIN password | No |
| `GDACS_STATE_FILE` | Path to persist seen-event state | No |
| `LOG_LEVEL` | Logging level (default: `INFO`) | No |
| `KAFKA_ENABLE_TLS` | Enable TLS for Kafka (default: `true`) | No |

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgdacs%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgdacs%2Fazure-template-with-eventhub.json)

## MQTT/Unified Namespace image

A sibling MQTT container image, `ghcr.io/clemensv/real-time-sources-gdacs-mqtt:latest`, publishes the same source events as MQTT 5.0 binary-mode CloudEvents. It uses the xRegistry MQTT messagegroup `GDACS.Alerts.mqtt` and the source-specific Unified Namespace topic tree described in [EVENTS.md](EVENTS.md).

### Run against a generic MQTT 5 broker

```shell
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-gdacs-mqtt:latest
```

### MQTT environment variables

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL including host, port, and TLS scheme, for example `mqtt://host:1883` or `mqtts://host:8883`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Optional username/password credentials for brokers that require user authentication. Leave unset for anonymous brokers. |
| `MQTT_CLIENT_ID` | Optional MQTT client identifier. Set it explicitly on shared brokers and Event Grid namespaces. |
| `MQTT_CONTENT_MODE` | CloudEvents content mode, `binary` by default. Keep `binary` for MQTT 5 user-property metadata. |
| `POLLING_INTERVAL` | Source polling interval in seconds, when supported by the feeder. |
| `STATE_FILE` | Optional path for source dedupe/checkpoint state, when the feeder maintains local state. |
| topic prefix | Fixed by the xRegistry contract, not an environment variable. Root: `alerts/intl/gdacs/gdacs`. |
| retain default | Per message in xRegistry; see the topic table below. |
| QoS default | Per message in xRegistry; MQTT messages in this source use QoS 1 unless noted otherwise. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra ID (Azure Event Grid). |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |

### MQTT topic patterns

| Topic pattern | Message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `alerts/intl/gdacs/gdacs/{event_type}/{alert_color}/{country}/{event_id}/alert` | `GDACS.DisasterAlert` | `false` | `1` | `` |

### Subscription patterns

```text
# Everything from this source
alerts/intl/gdacs/gdacs/#
```

### MQTT Azure deployment

Deploy the MQTT container against an existing MQTT 5 broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgdacs%2Fazure-template-mqtt.json)

Deploy the MQTT container with a new Azure Event Grid namespace MQTT broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fgdacs%2Fazure-template-with-eventgrid-mqtt.json)

## AMQP 1.0 companion

### AMQP environment variables

| Variable | Description |
|---|---|
| `AMQP_HOST` | AMQP broker host (component-level alternative to `AMQP_BROKER_URL`). |
| `AMQP_ADDRESS` | AMQP node (queue / topic) name to publish to. |
| `AMQP_AUTH_MODE` | `password` (default), `entra` for Microsoft Entra ID via AMQP CBS (Service Bus / Event Hubs), or `sas` for SAS-token CBS. |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |
| `AMQP_ENTRA_AUDIENCE` | Token audience for `entra` mode (default `https://servicebus.azure.net/.default`). |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |
| `AMQP_PORT` | AMQP broker port (default `5672`, or `5671` with TLS). |
| `AMQP_TLS` | Set `true` to use TLS (`amqps`) for the component-level connection. |
| `AMQP_USERNAME` | SASL PLAIN username, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_PASSWORD` | SASL PLAIN password, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name (e.g. `RootManageSharedAccessKey`). Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_SAS_KEY` | SAS key value (base64-encoded shared secret). Required when `AMQP_AUTH_MODE=sas`. |


This source also ships an AMQP 1.0 companion feeder (`Dockerfile.amqp`) alongside the Kafka and MQTT variants. It publishes the same CloudEvents to a single AMQP address named after the source, with CloudEvent `subject` and AMQP application properties mirroring the Kafka key/MQTT topic axes for broker-side filtering. Use `azure-template-with-servicebus.json` to deploy the AMQP feeder to Azure Service Bus with Entra ID/CBS authentication, or set `AMQP_BROKER_URL` for a generic AMQP 1.0 broker.
