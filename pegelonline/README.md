# PegelOnline → Apache Kafka, MQTT/UNS & AMQP 1.0

## Overview

**PegelOnline** is a bridge that polls the German WSV PegelOnline REST API
and re-emits both the station catalog and the live water-level measurements
as CloudEvents. The source ships in three transport variants from a single
upstream poller:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-pegelonline-kafka` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `{station_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-pegelonline-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | Unified-Namespace topic tree under `hydro/de/wsv/pegelonline/{water}/{station}/...`, JSON body, CloudEvent attributes as MQTT 5 user properties, retained at QoS 1 |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-pegelonline-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs) | Single AMQP node (queue/topic), binary CloudEvents, SASL PLAIN for generic brokers or Microsoft Entra ID via AMQP CBS for Service Bus / Event Hubs |

Both variants share:

* The upstream poller (`pegelonline_core`).
* The xRegistry contract (`xreg/pegelonline.xreg.json`).
* The CloudEvents schemas for the `Station` reference event and the
  `CurrentMeasurement` telemetry event.

## Key Features
- **Station catalog** emitted at startup as reference CloudEvents.
- **Live water-level measurements** with ETag-aware polling and per-station
  dedup state.
- **Three transport binaries** with identical configuration knobs upstream
  (polling interval, state file, once-mode).
- **Microsoft Event Hubs / Fabric Event Stream** ready via standard
  connection strings (Kafka variant).
- **Unified Namespace** ready out of the box with retained MQTT 5.0 binary
  CloudEvents (MQTT variant).
- **Azure Service Bus / Event Hubs over AMQP 1.0 with Microsoft Entra ID**
  (no SAS-key rotation) via the AMQP variant's CBS put-token flow.

## Repository Layout

```
pegelonline/
  xreg/pegelonline.xreg.json     # shared xRegistry contract
  pegelonline_core/              # transport-agnostic poller
  pegelonline_kafka/             # Kafka feeder application
  pegelonline_mqtt/              # MQTT/UNS feeder application
  pegelonline_amqp/              # AMQP 1.0 feeder application
  pegelonline_producer/          # xrcg-generated Kafka producer
  pegelonline_mqtt_producer/     # xrcg-generated MQTT producer
  pegelonline_amqp_producer/     # xrcg-generated AMQP producer
  Dockerfile.kafka               # builds the Kafka feeder image
  Dockerfile.mqtt                # builds the MQTT feeder image
  Dockerfile.amqp                # builds the AMQP feeder image
  tests/                         # unit + integration tests
```

## Quick start with Docker

### Kafka

```bash
docker run --rm \
  -e CONNECTION_STRING="$EVENT_HUBS_CONNECTION_STRING" \
  ghcr.io/clemensv/real-time-sources-pegelonline-kafka:latest
```

### MQTT / UNS

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtts://broker.example.com:8883 \
  -e MQTT_USERNAME=alice \
  -e MQTT_PASSWORD=secret \
  ghcr.io/clemensv/real-time-sources-pegelonline-mqtt:latest
```

Topics published (retained, QoS 1):

```
hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/info          # Station reference
hydro/de/wsv/pegelonline/{water_shortname}/{station_id}/water-level   # CurrentMeasurement telemetry
```

The legacy single-image deployment (`Dockerfile`) has been retired in favor
of the two transport-specific images above. Existing Kafka-side environment
variables (`CONNECTION_STRING`, `KAFKA_*`, `SASL_*`, `POLLING_INTERVAL`,
`STATE_FILE`, `ONCE_MODE`) are preserved unchanged on the Kafka variant.

## Local development

For a packaged install, consider using the [CONTAINER.md](CONTAINER.md) instructions.

## How to Use

After installation, the tool can be run using the `pegelonline` command. It supports multiple subcommands:
- **List Stations (`list`)**: Fetch and display all available monitoring stations.
- **Get Water Level (`level`)**: Retrieve the current water level for a specific station.
- **Feed Stations (`feed`)**: Continuously poll PegelOnline API for water levels and send updates to a Kafka topic.

### **List Stations (`list`)**

Fetches and displays all available monitoring stations from the PegelOnline API.

#### Example Usage:

```bash
pegelonline list
```

### **Get Water Level (`level`)**

Retrieves the current water level for the specified station.

- `shortname`: The short name of the station to query.

#### Example Usage:

```bash
pegelonline level <station_shortname>
```

### **Feed Stations (`feed`)**

Polls the PegelOnline API for water level measurements and sends them as
CloudEvents to a Kafka topic. The events are formatted using CloudEvents
structured JSON format and described in [EVENTS.md](EVENTS.md).

- `--kafka-bootstrap-servers`: Comma-separated list of Kafka bootstrap servers.
- `--kafka-topic`: Kafka topic to send messages to.
- `--sasl-username`: Username for SASL PLAIN authentication.
- `--sasl-password`: Password for SASL PLAIN authentication.
- `--connection-string`: Microsoft Event Hubs or Microsoft Fabric Event Stream [connection string](#connection-string-for-microsoft-event-hubs-or-fabric-event-streams) (overrides other Kafka parameters).
- `--polling-interval`: Interval in seconds between API polling requests
  (default is 60 seconds; the data is for most stations is only updated once
  every 6 minutes, but different for each station).

#### Example Usage:

```bash
pegelonline feed --kafka-bootstrap-servers "<bootstrap_servers>" --kafka-topic "<topic_name>" --sasl-username "<username>" --sasl-password "<password>" --polling-interval 60
```

Alternatively, using a connection string for Microsoft Event Hubs or Microsoft Fabric Event Streams:

```bash
pegelonline feed --connection-string "<your_connection_string>" --polling-interval 60
```

### Connection String for Microsoft Event Hubs or Fabric Event Streams

The connection string format is as follows:

```
Endpoint=sb://<your-event-hubs-namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy-name>;SharedAccessKey=<access-key>;EntityPath=<event-hub-name>
```

When provided, the connection string is parsed to extract the Kafka configuration parameters:
- **Bootstrap Servers**: Derived from the `Endpoint` value.
- **Kafka Topic**: Derived from the `EntityPath` value.
- **SASL Username and Password**: The username is set to `'$ConnectionString'`, and the password is the entire connection string.

### Environment Variables
The tool supports the following environment variables to avoid passing them via the command line:
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers (comma-separated list).
- `KAFKA_TOPIC`: Kafka topic for publishing.
- `SASL_USERNAME`: SASL username for Kafka authentication.
- `SASL_PASSWORD`: SASL password for Kafka authentication.
- `CONNECTION_STRING`: Microsoft Event Hubs or Microsoft Fabric Event Stream connection string.
- `POLLING_INTERVAL`: Polling interval in seconds.

## State Management

The tool handles state internally for efficient API polling and sending updates.

## Deploying into Azure Container Instances

You can deploy this bridge directly to Azure Container Instances. Two deployment
options are available:

### Option 1: Bring your own Event Hub

Deploy the container and provide your own Azure Event Hubs or Fabric Event
Streams connection string. The template creates a storage account and file share
for persistent state.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template.json)

### Option 2: Deploy with a new Event Hub

Deploy the container together with a new Event Hub namespace (Standard SKU, 1
throughput unit) and event hub. The connection string is automatically
configured.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fpegelonline%2Fazure-template-with-eventhub.json)
