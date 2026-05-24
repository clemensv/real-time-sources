# PTWC Tsunami Container

## Quick Start

```bash
docker build -t ptwc-tsunami .
docker run --rm -e CONNECTION_STRING="<your-connection-string>" ptwc-tsunami
```

## Description

This container bridges tsunami bulletins from NOAA's National Tsunami Warning
Center (NTWC) and Pacific Tsunami Warning Center (PTWC) to Kafka-compatible
endpoints (Apache Kafka, Azure Event Hubs, Microsoft Fabric Event Streams) as
CloudEvents.

It polls two Atom XML feeds for seismic event bulletins, parses the XHTML
summaries for structured fields (category, magnitude, affected region), and
emits them as CloudEvents.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | Yes* | Event Hubs / Fabric connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Yes* | Kafka bootstrap servers |
| `KAFKA_TOPIC` | No | Topic name (default: `ptwc-tsunami`) |
| `SASL_USERNAME` | No | SASL username |
| `SASL_PASSWORD` | No | SASL password |
| `PTWC_TSUNAMI_STATE_FILE` | No | State file (default: `~/.ptwc_tsunami_state.json`) |
| `LOG_LEVEL` | No | Logging level (default: `INFO`) |

*One of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS` is required.

## Azure Container Instance

```bash
az container create \
  --resource-group <rg> \
  --name ptwc-tsunami \
  --image ghcr.io/clemensv/real-time-sources/ptwc-tsunami:latest \
  --environment-variables CONNECTION_STRING="<cs>" \
  --restart-policy Always
```

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-eventhub.json)

## MQTT/Unified Namespace image

A sibling MQTT container image, `ghcr.io/clemensv/real-time-sources-ptwc-tsunami-mqtt:latest`, publishes the same source events as MQTT 5.0 binary-mode CloudEvents. It uses the xRegistry MQTT messagegroup `PTWC.Bulletins.mqtt` and the source-specific Unified Namespace topic tree described in [EVENTS.md](EVENTS.md).

### Run against a generic MQTT 5 broker

```shell
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-ptwc-tsunami-mqtt:latest
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
| topic prefix | Fixed by the xRegistry contract, not an environment variable. Root: `alerts/intl/ptwc/ptwc-tsunami`. |
| retain default | Per message in xRegistry; see the topic table below. |
| QoS default | Per message in xRegistry; MQTT messages in this source use QoS 1 unless noted otherwise. |

### MQTT topic patterns

| Topic pattern | Message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `alerts/intl/ptwc/ptwc-tsunami/{basin}/{ptwc_level}/{bulletin_id}/bulletin` | `PTWC.TsunamiBulletin` | `false` | `1` | `` |

### Subscription patterns

```text
# Everything from this source
alerts/intl/ptwc/ptwc-tsunami/#
```

### MQTT Azure deployment

Deploy the MQTT container against an existing MQTT 5 broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-mqtt.json)

Deploy the MQTT container with a new Azure Event Grid namespace MQTT broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fptwc-tsunami%2Fazure-template-with-eventgrid-mqtt.json)
