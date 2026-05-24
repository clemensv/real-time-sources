# VATSIM Live Data Feed Bridge to Apache Kafka, Azure Event Hubs, and Fabric Event Streams

This container image provides a bridge between the VATSIM virtual aviation
network live data feed and Apache Kafka, Azure Event Hubs, and Fabric Event
Streams. The bridge polls pilot positions, controller positions, and network
status and writes them to a Kafka topic.

## VATSIM Data Feed

VATSIM (Virtual Air Traffic Simulation Network) is a free online network where
virtual pilots and air traffic controllers connect to simulate real-world
aviation. The data feed at `https://data.vatsim.net/v3/vatsim-data.json`
provides a JSON snapshot of all connected clients, updated every ~15 seconds.
No authentication is required.

## Functionality

The bridge polls the VATSIM data feed and writes pilot positions, controller
positions, and network status to a Kafka topic as structured JSON
[CloudEvents](https://cloudevents.io/). Events are described in
[EVENTS.md](EVENTS.md). The bridge deduplicates by callsign so only changed
positions are emitted.

## Installing the Container Image

Pull the container image from the GitHub Container Registry:

```shell
$ docker pull ghcr.io/clemensv/real-time-sources-vatsim:latest
```

## Using the Container Image

### With a Kafka Broker

```shell
$ docker run --rm \
    -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>' \
    -e KAFKA_TOPIC='<kafka-topic>' \
    -e SASL_USERNAME='<sasl-username>' \
    -e SASL_PASSWORD='<sasl-password>' \
    ghcr.io/clemensv/real-time-sources-vatsim:latest
```

### With Azure Event Hubs or Fabric Event Streams

```shell
$ docker run --rm \
    -e CONNECTION_STRING='<connection-string>' \
    ghcr.io/clemensv/real-time-sources-vatsim:latest
```

## Environment Variables

### `CONNECTION_STRING`

An Azure Event Hubs-style connection string used to establish a connection.

### `KAFKA_BOOTSTRAP_SERVERS`

Comma-separated list of Kafka bootstrap servers.

### `KAFKA_TOPIC`

Kafka topic where messages will be produced.

### `SASL_USERNAME`

Username for SASL PLAIN authentication.

### `SASL_PASSWORD`

Password for SASL PLAIN authentication.

### `POLLING_INTERVAL`

Polling interval in seconds (default: 60).

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-eventhub.json)

## MQTT/Unified Namespace image

A sibling MQTT container image, `ghcr.io/clemensv/real-time-sources-vatsim-mqtt:latest`, publishes the same source events as MQTT 5.0 binary-mode CloudEvents. It uses the xRegistry MQTT messagegroup `net.vatsim.mqtt` and the source-specific Unified Namespace topic tree described in [EVENTS.md](EVENTS.md).

### Run against a generic MQTT 5 broker

```shell
docker run --rm \
    -e MQTT_BROKER_URL='mqtts://broker.example.com:8883' \
    -e MQTT_USERNAME='<username>' \
    -e MQTT_PASSWORD='<password>' \
    ghcr.io/clemensv/real-time-sources-vatsim-mqtt:latest
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
| topic prefix | Fixed by the xRegistry contract, not an environment variable. Root: `aviation-network/intl/vatsim/vatsim/pilots`. |
| retain default | Per message in xRegistry; see the topic table below. |
| QoS default | Per message in xRegistry; MQTT messages in this source use QoS 1 unless noted otherwise. |

### MQTT topic patterns

| Topic pattern | Message type | Retained | QoS | Expiry seconds |
|---|---|---|---|---|
| `aviation-network/intl/vatsim/vatsim/pilots/{callsign}/pilot-position` | `net.vatsim.PilotPosition` | `false` | `1` | `` |
| `aviation-network/intl/vatsim/vatsim/controllers/{callsign}/controller-position` | `net.vatsim.ControllerPosition` | `false` | `1` | `` |
| `aviation-network/intl/vatsim/vatsim/facilities/{facility}/facility-status` | `net.vatsim.NetworkStatus` | `false` | `1` | `` |

### Subscription patterns

```text
# Everything from this source
aviation-network/intl/vatsim/vatsim/pilots/#
```

### MQTT Azure deployment

Deploy the MQTT container against an existing MQTT 5 broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-mqtt.json)

Deploy the MQTT container with a new Azure Event Grid namespace MQTT broker:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fvatsim%2Fazure-template-with-eventgrid-mqtt.json)
