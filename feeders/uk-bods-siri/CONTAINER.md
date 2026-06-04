<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/gb.png" alt="England" width="64" height="48"><br>
<sub><b>England</b></sub>
</td>
<td valign="middle">

# UK BODS SIRI

<sub>28,000+ buses · Kafka · MQTT · AMQP · <a href="https://data.bus-data.dft.gov.uk/">upstream</a> · <a href="https://www.gov.uk/government/publications/technical-guidance-publishing-location-data-using-the-bus-open-data-service-siri-vm">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-5_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-Notebook_%2B_ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#uk-bods-siri) &nbsp;·&nbsp;
[📓 **Fabric Notebook**](https://clemensv.github.io/real-time-sources#uk-bods-siri/fabric-notebook) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[🗄️ **KQL schema**](kql/uk-bods-siri.kql)

</td></tr></table>
<!-- source-hero:end -->

This document covers the published OCI container images for the UK BODS SIRI feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

## Upstream

- Home page: <https://data.bus-data.dft.gov.uk/>
- Technical guidance: <https://www.gov.uk/government/publications/technical-guidance-publishing-location-data-using-the-bus-open-data-service-siri-vm>
- Archive reference: <https://data.datalibrary.uk/transport/BODS-ARCHIVE/sirivm/>

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-uk-bods-siri-kafka` | Apache Kafka 2.x | JSON CloudEvents on topic `uk-bods-siri`; telemetry key `{operator_ref}/{vehicle_ref}` |
| `ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt` | MQTT 5.0 | UNS topics `transit/uk/dft/bods/{operator_ref}/{vehicle_ref}/position` and `transit/uk/dft/bods/{operator_ref}/info` |
| `ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp` | AMQP 1.0 | Binary CloudEvents to AMQP node `uk-bods-siri` |

The images poll the BODS AVL bulk archive, emit `uk.gov.dft.bods.Operator` reference events, and emit `uk.gov.dft.bods.VehiclePosition` telemetry events for current vehicle activities.

## Image contract

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` |
| Default entry point | Kafka `python -m uk_bods_siri_kafka feed`; MQTT `python -m uk_bods_siri_mqtt feed`; AMQP `python -m uk_bods_siri_amqp feed` |
| Exposed ports | none — outbound publisher only |
| Persistent state | `STATE_FILE`; mount a host volume for restart-safe dedupe |
| Poll cadence | `POLLING_INTERVAL` seconds (default `30`) |
| Required upstream credential | `BODS_API_KEY` |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-uk-bods-siri-kafka:latest
docker pull ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp:latest
```

## Using the Kafka image

### With a Kafka broker

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e KAFKA_BOOTSTRAP_SERVERS="<host:port>" \
  -e KAFKA_TOPIC="uk-bods-siri" \
  -e SASL_USERNAME="<username>" \
  -e SASL_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-kafka:latest
```

### With Azure Event Hubs or Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-kafka:latest
```

### Kafka environment variables

| Variable | Description |
|---|---|
| `BODS_API_KEY` | Required BODS API key. |
| `OPERATORS` | Optional comma-separated NOC filter. |
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list. |
| `KAFKA_TOPIC` | Kafka destination topic (default `uk-bods-siri`). |
| `SASL_USERNAME` / `SASL_PASSWORD` | Kafka credentials when not using `CONNECTION_STRING`. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS; default `true`. |
| `POLLING_INTERVAL` | Poll interval in seconds. |
| `STATE_FILE` | Path to dedupe state file. |
| `ONCE_MODE` | Run one poll cycle and exit. |

## Using the MQTT image

### With a generic MQTT 5 broker

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_AUTH_MODE=userpass \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883" \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID="<user-assigned-managed-identity-client-id>" \
  -e MQTT_CLIENT_ID="<unique-client-id>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-mqtt:latest
```

### MQTT environment variables

| Variable | Description |
|---|---|
| `BODS_API_KEY` | Required BODS API key. |
| `OPERATORS` | Optional comma-separated NOC filter. |
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_HOST` / `MQTT_PORT` | Component endpoint settings when URL form is not used. |
| `MQTT_ENABLE_TLS` | Enable TLS. |
| `MQTT_AUTH_MODE` | `anonymous`, `userpass`, or `entra`. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for `userpass`. |
| `MQTT_CLIENT_ID` | MQTT client id. |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. |
| `MQTT_ENTRA_AUDIENCE` | Entra JWT audience; default `https://eventgrid.azure.net/`. |
| `POLLING_INTERVAL` | Poll interval in seconds. |
| `STATE_FILE` | Path to dedupe state file. |
| `ONCE_MODE` | Run one poll cycle and exit. |

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuk-bods-siri%2Fazure-template-mqtt.json) [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuk-bods-siri%2Fazure-template-with-eventgrid-mqtt.json)

## Using the AMQP image

### With a generic AMQP 1.0 broker

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/uk-bods-siri" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp:latest
```

### With Azure Service Bus or Event Hubs via Entra ID

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-bods-siri.json \
  -e BODS_API_KEY="<bods-api-key>" \
  -e AMQP_HOST="<namespace>.servicebus.windows.net" \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS="uk-bods-siri" \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE="https://servicebus.azure.net/.default" \
  -e AMQP_ENTRA_CLIENT_ID="<user-assigned-managed-identity-client-id>" \
  ghcr.io/clemensv/real-time-sources-uk-bods-siri-amqp:latest
```

### AMQP environment variables

| Variable | Description |
|---|---|
| `BODS_API_KEY` | Required BODS API key. |
| `OPERATORS` | Optional comma-separated NOC filter. |
| `AMQP_BROKER_URL` | Full AMQP URL form (`amqp://` or `amqps://`). |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component endpoint settings when URL form is not used. |
| `AMQP_ADDRESS` | AMQP node/address name. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | Credentials for generic brokers. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra ID CBS settings. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS-token CBS settings. |
| `POLLING_INTERVAL` | Poll interval in seconds. |
| `STATE_FILE` | Path to dedupe state file. |
| `ONCE_MODE` | Run one poll cycle and exit. |

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuk-bods-siri%2Fazure-template-with-servicebus.json)

## Deploying into Azure Container Instances

### Kafka — bring your own Event Hub / Kafka
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuk-bods-siri%2Fazure-template.json)

### Kafka — provision a new Event Hub
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuk-bods-siri%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuk-bods-siri%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace broker
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuk-bods-siri%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus namespace
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fuk-bods-siri%2Fazure-template-with-servicebus.json)
