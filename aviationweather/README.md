# AviationWeather.gov feeder

This feeder turns the upstream AviationWeather.gov weather data into a real-time CloudEvents stream over Apache Kafka, MQTT 5.0 (Unified Namespace), or AMQP 1.0.

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://aviationweather.gov/>
- API / data documentation: <https://aviationweather.gov/data/api/>

<!-- upstream-links:end -->

Companion docs:

- [CONTAINER.md](CONTAINER.md) — published container images, environment variables, and one-click Azure deployments.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and per-transport routing.
> [!IMPORTANT]
> Always mount a volume for `AVIATIONWEATHER_LAST_POLLED_FILE`. Without a persisted state file, the poller restarts cold and may republish already-seen records.

## Why this bridge

This source wraps the upstream AviationWeather.gov APIs into a contract-first event stream so consumers can subscribe instead of implementing custom polling, pagination, dedupe, retry, and schema handling in every downstream system.

- **Operational dashboards** — subscribe to `aviationweather` events for near-real-time situational awareness and KPI tracking.
- **Data engineering pipelines** — land validated CloudEvents in Eventhouse/ADX/lakehouse without polling the upstream API directly.
- **Alerting and automation** — trigger workflow actions from fresh `AviationWeather.gov` observations and advisories.
- **Cross-domain analytics** — correlate weather signals with transport, safety, energy, or hydrology feeders from this repository.
- **Research and compliance archives** — keep a durable, replayable stream with stable subject/key identity (`{icao_id}`).

## Overview

**AviationWeather.gov** is a poll-based bridge. The source ships in 3 transport variants from a shared upstream poller:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-aviationweather` | Apache Kafka 2.x compatible (incl. Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic, JSON CloudEvents (binary mode), key = `{icao_id}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-aviationweather-mqtt` | MQTT 5.0 broker (incl. Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT, Microsoft Fabric Real-Time Hub MQTT broker) | UNS topic template `(see xreg endpoint options)`, QoS 1 CloudEvents with MQTT 5 user properties |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-aviationweather-amqp` | AMQP 1.0 (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs) | Single AMQP node `aviationweather`, binary CloudEvents, SASL PLAIN / Entra CBS / SAS CBS auth modes |

All variants share:

- The upstream polling runtime in this source folder.
- The xRegistry contract at `xreg/aviationweather.xreg.json`.
- The same CloudEvents event families and identity model.

## Key features

- Contract-first CloudEvents output aligned with the xRegistry manifest.
- Stateful poller with dedupe/resume support via `AVIATIONWEATHER_LAST_POLLED_FILE`.
- Transport parity across Kafka, MQTT, and AMQP with the same event semantics.
- Ready for Azure Event Hubs / Fabric Event Streams connection strings.

## Repository layout

```text
aviationweather/
  xreg/
  kql/
  notebook/
  tests/
  Dockerfile
  Dockerfile.amqp
  Dockerfile.mqtt
  aviationweather/
  aviationweather_amqp/
  aviationweather_amqp_producer/
  aviationweather_mqtt/
  aviationweather_mqtt_producer/
  aviationweather_producer/
  azure-template-amqp.json
```

## Prerequisites

- Docker 20.10+ (or any OCI-compatible runtime).
- Outbound network access to the upstream AviationWeather.gov API endpoints.
- Network access to your target broker(s).
- A writable host directory mounted at `/state` to persist `AVIATIONWEATHER_LAST_POLLED_FILE` across restarts.

## Quick start with Docker

> [!IMPORTANT]
> Always mount a volume for `AVIATIONWEATHER_LAST_POLLED_FILE`. Without a persisted state file, the poller restarts cold and may republish already-seen records.

### Kafka

```bash
docker run --rm   -v "$PWD/state:/state"   -e AVIATIONWEATHER_LAST_POLLED_FILE=/state/aviationweather.json   -e CONNECTION_STRING="<event-hubs-connection-string>"   ghcr.io/clemensv/real-time-sources-aviationweather:latest
```

### MQTT (Unified Namespace)

```bash
docker run --rm   -v "$PWD/state:/state"   -e AVIATIONWEATHER_LAST_POLLED_FILE=/state/aviationweather.json   -e MQTT_BROKER_URL=mqtts://<broker-host>:8883   -e MQTT_USERNAME=<username>   -e MQTT_PASSWORD=<password>   ghcr.io/clemensv/real-time-sources-aviationweather-mqtt:latest
```

Topic template:

```text
(see xreg endpoint options)
```

### AMQP 1.0

```bash
docker run --rm   -v "$PWD/state:/state"   -e AVIATIONWEATHER_LAST_POLLED_FILE=/state/aviationweather.json   -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/aviationweather'   ghcr.io/clemensv/real-time-sources-aviationweather-amqp:latest
```

For full authentication matrices (Kafka SASL/Event Hubs, MQTT password/Entra, AMQP password/Entra/SAS), see [CONTAINER.md](CONTAINER.md).

## Configuration reference

The complete environment-variable matrix for all images is documented in [CONTAINER.md](CONTAINER.md). Docker entrypoints are taken from image `CMD` values (`["python", "-m", "aviationweather"]`, `["python", "-m", "aviationweather_mqtt", "feed"]`, `["python", "-m", "aviationweather_amqp", "feed"]`).

## Data model

This feeder emits the following event families:

- **`Station`**
- **`Metar`**
- **`Sigmet`**

Identity follows the xRegistry key/subject model (`{icao_id}`) and is consistent across transports.

## Deploying into Microsoft Fabric

AviationWeather.gov supports Fabric end-to-end: events flow into a Fabric Event Stream custom endpoint, and the source KQL script in `kql/` materializes typed tables and update policies in Eventhouse.

Two hosting models are supported using the deploy buttons on the [project portal](https://clemensv.github.io/real-time-sources/#aviationweather).

### Fabric Notebook feeder

A scheduled notebook in [`notebook/`](notebook/) runs the poller inside the Fabric workspace using the per-source Fabric Environment produced by `tools/deploy-fabric/deploy-feeder-notebook.ps1`. Runtime diagnostics and persisted state are written to OneLake.

[![Deploy Fabric Notebook](https://img.shields.io/badge/Fabric-Notebook%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#aviationweather/fabric-notebook)

### Fabric ACI feeder

Use `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source aviationweather` to run the container continuously in Azure Container Instances while targeting a Fabric Event Stream custom endpoint.

[![Deploy Fabric ACI](https://img.shields.io/badge/Fabric-Container%20Feeder-117865?logo=microsoftfabric&logoColor=white)](https://clemensv.github.io/real-time-sources/#aviationweather/fabric-aci)

## Deploying into Azure Container Instances

### AMQP — bring your own AMQP broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-amqp.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Faviationweather%2Fazure-template.json)

## Next steps

- Review [EVENTS.md](EVENTS.md) before implementing consumers.
- Use [CONTAINER.md](CONTAINER.md) for full environment-variable and authentication details.
- Validate deployment choices (Notebook vs ACI vs direct Azure templates) against your latency and operations requirements.
