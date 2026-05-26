# NOAA SWPC L1 Propagated Solar Wind → Apache Kafka, MQTT/UNS & AMQP 1.0

## Why this bridge

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.swpc.noaa.gov/>
- API / data documentation: <https://services.swpc.noaa.gov/>

<!-- upstream-links:end -->

NOAA Space Weather Prediction Center (**SWPC**) publishes the
[propagated solar wind](https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json)
product: the L1 solar-wind time series forward-projected to predicted
Earth arrival. L1 is the Sun-Earth Lagrange point about 1.5 million km
sunward of Earth. NOAA DSCOVR is the operational primary; NASA ACE is the
backup.

This bridge turns that rolling REST document into a first-class real-time
event stream so operational consumers can subscribe instead of polling:

- **Geomagnetic-storm forecasting** — `propagated_time_tag` gives the
  predicted Earth-arrival time of the observed L1 solar-wind parcel.
- **Power-grid operations** — sustained southward Bz is an input to GIC
  threat assessments and geomagnetic-storm procedures.
- **Aviation and maritime operations** — HF radio blackouts and navigation
  impacts can be correlated with the same SWPC input used by forecasters.
- **Satellite operations** — radiation and geomagnetic activity models can
  ingest a deduped, typed feed instead of scraping the SWPC JSON file.
- **Fabric Eventhouse / ADX / data lakes** — keep the full minute-level
  time series for replay, alerting and model development.

The bridge does the polling, cold-start backfill, state-file dedupe,
CloudEvents mapping, JsonStructure schema contract and transport-specific
partitioning.

## Overview

**NOAA SWPC L1** polls one upstream endpoint and emits one CloudEvent type
in three transport variants:

| Variant | Container image | Transport | Default delivery shape |
|---|---|---|---|
| **Kafka** | `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-kafka:latest` | Apache Kafka 2.x compatible (Azure Event Hubs, Microsoft Fabric Event Streams, Confluent Cloud) | One topic `noaa-swpc-l1`, JSON CloudEvents (binary mode), key = `{spacecraft}` |
| **MQTT** | `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-mqtt:latest` | MQTT 5.0 broker (Mosquitto, EMQX, HiveMQ, Azure Event Grid MQTT) | Retained QoS-1 CloudEvents on `space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind` |
| **AMQP** | `ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest` | AMQP 1.0 (RabbitMQ AMQP 1.0, ActiveMQ Artemis, Qpid Dispatch, Azure Service Bus, Azure Event Hubs) | Single address `noaa-swpc-l1`, binary CloudEvents, AMQP subject and `x-opt-partition-key` = `{spacecraft}` |

All variants share:

* The transport-agnostic poller (`noaa_swpc_l1_core`).
* The xRegistry contract (`xreg/noaa_swpc_l1.xreg.json`).
* The `gov.noaa.swpc.l1.PropagatedSolarWind` JsonStructure schema.

## Upstream API

The bridge reads:

```text
GET https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json
```

The response is an array-of-arrays. Row 0 is the column header:

```text
time_tag, speed, density, temperature, bx, by, bz, bt, vx, vy, vz, propagated_time_tag
```

Rows 1..N are one observation per minute for a seven-day rolling window.
Upstream timestamps are `YYYY-MM-DD HH:MM:SS.fff` with implicit UTC; the
bridge normalizes them to RFC 3339 UTC. Numeric fields are nullable and
partial rows are emitted rather than skipped.

## Data model

The single event type is:

* `gov.noaa.swpc.l1.PropagatedSolarWind` — one minute-resolution L1 row
  containing:
  * plasma: `speed`, `density`, `temperature`
  * magnetic field in GSM coordinates: `bx`, `by`, `bz`, `bt`
  * bulk velocity in GSM coordinates: `vx`, `vy`, `vz`
  * timestamps: `time_tag` at L1 and `propagated_time_tag` at predicted
    Earth arrival
  * synthetic spacecraft channel: `spacecraft` (`dscovr` by default,
    `ace` reserved for backup failover)

The identity model is intentionally stable and low-cardinality:

| Context | Value |
|---|---|
| CloudEvent subject | `{spacecraft}` |
| Kafka key | `{spacecraft}` |
| MQTT topic segment | `{spacecraft}` |
| AMQP subject | `{spacecraft}` |
| AMQP partition annotation | `x-opt-partition-key = {spacecraft}` |

`time_tag` is the CloudEvent `time` and a payload field, but it is not the
partition key. This keeps each spacecraft channel ordered on all
transports.

## Event schema

The event contract is documented in [EVENTS.md](EVENTS.md). The
authoritative xRegistry document is
[`xreg/noaa_swpc_l1.xreg.json`](xreg/noaa_swpc_l1.xreg.json). The KQL
schema for Fabric Eventhouse / Azure Data Explorer is
[`kql/noaa_swpc_l1.kql`](kql/noaa_swpc_l1.kql).

## Transports

### Kafka

Use Kafka when you need ordered replay, seven-day backfill into a
persistent log, Fabric Eventhouse / ADX ingestion, or multiple consumer
groups reading the same spacecraft stream independently.

```bash
docker run --rm \
  -e CONNECTION_STRING="$EVENT_HUBS_OR_FABRIC_CONNECTION_STRING" \
  ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-kafka:latest
```

### MQTT / UNS

Use MQTT when you need last-known-value distribution, edge-gateway
integration, UNS topic routing, retained dashboards, or a simple
subscription for the latest propagated solar-wind state.

```bash
docker run --rm \
  -e MQTT_BROKER_URL=mqtts://broker.example.com:8883 \
  -e MQTT_USERNAME=alice \
  -e MQTT_PASSWORD=secret \
  ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-mqtt:latest
```

Published topic (retained, QoS 1):

```text
space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind
```

### AMQP 1.0

Use AMQP when consumers are built around Azure Service Bus or AMQP-native
brokers and need queue semantics, sessions, scheduled delivery,
dead-lettering, or native SB/EH clients. The bridge can authenticate with
SASL PLAIN, Microsoft Entra ID via CBS, or SAS-token CBS.

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://user:pw@broker.example.com:5672/noaa-swpc-l1' \
  ghcr.io/clemensv/real-time-sources-noaa-swpc-l1-amqp:latest
```

For Azure Service Bus or Event Hubs with Microsoft Entra ID, the Service
Bus emulator, or SAS-only namespaces, see
[CONTAINER.md](CONTAINER.md#using-the-amqp-image).

## Configuration reference

The complete list of environment variables for every variant (Kafka /
MQTT / AMQP), every authentication mode, state handling and Azure
deployment shape lives in [CONTAINER.md](CONTAINER.md). Defaults shared by
all transports include:

| Setting | Default |
|---|---|
| `POLLING_INTERVAL` | `60` seconds |
| `BACKFILL_MINUTES` | `5` minutes on cold start |
| `STATE_FILE` | `~/.noaa_swpc_l1_state.json` |
| `SPACECRAFT` | `dscovr` |

## Deploying into Azure Container Instances

Five one-click deployment templates are available.

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-eventhub.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-swpc-l1%2Fazure-template-with-servicebus.json)

## Repository layout

```text
noaa-swpc-l1/
  xreg/noaa_swpc_l1.xreg.json       # shared xRegistry contract
  noaa_swpc_l1_core/                # transport-agnostic acquisition + state
  noaa_swpc_l1_kafka/               # Kafka feeder application
  noaa_swpc_l1_mqtt/                # MQTT/UNS feeder application
  noaa_swpc_l1_amqp/                # AMQP 1.0 feeder application
  noaa_swpc_l1_producer/            # xrcg-generated Kafka producer
  noaa_swpc_l1_mqtt_producer/       # xrcg-generated MQTT producer
  noaa_swpc_l1_amqp_producer/       # xrcg-generated AMQP producer
  Dockerfile.kafka
  Dockerfile.mqtt
  Dockerfile.amqp
  kql/noaa_swpc_l1.kql
  tests/
```

## Development pointers

- Regenerate producers with `generate_producer.ps1` after changing the
  xRegistry contract; do not hand-edit generated producer code.
- The shared acquisition code validates the upstream header exactly and
  raises on header drift.
- Rows are sorted chronologically and emitted only when `time_tag` is
  strictly newer than the stored `last_time_tag`.
- The state file is a single JSON file with key `last_time_tag`.
- See [CONTAINER.md](CONTAINER.md) for deployment behavior and
  [EVENTS.md](EVENTS.md) for the event contract.
