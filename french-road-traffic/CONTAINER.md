# French Road Traffic container images

This document covers the published OCI container images for the French Road Traffic feeder, their environment-variable contract, authentication modes, and one-click Azure deployments.

Companion docs:

- [README.md](README.md) — source overview, value framing, and deployment options.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and routing details.

## Why this container

French mobility operations, transport ministries, traffic-information providers, and navigation systems rely on Bison Futé measurements and situation feeds for network monitoring and disruption handling. These containers package polling, event normalization, dedupe, and transport-specific publishing so teams can run production ingestion without custom bridge code.

## What ships in the box

| Image | Transport | Runtime entrypoint |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-french-road-traffic` | Kafka | `python -m french_road_traffic feed` |
| `ghcr.io/clemensv/real-time-sources-french-road-traffic-mqtt` | MQTT | `python -m french_road_traffic_mqtt feed` |
| `ghcr.io/clemensv/real-time-sources-french-road-traffic-amqp` | AMQP | `python -m french_road_traffic_amqp feed` |

The image set shares a single xRegistry contract and publishes the same event families listed in [EVENTS.md](EVENTS.md).

## Image contract

| Aspect | Value |
|---|---|
| Base image | Source Dockerfiles (`Dockerfile*`) currently use Python slim bases (Kafka may differ from MQTT/AMQP in some sources). |
| Entry point | `python -m <source>{,_mqtt,_amqp} feed` per image. |
| Exposed ports | None (outbound publisher only). |
| Signals | Graceful process termination on `SIGTERM`. |
| Persistent state | `STATE_FILE` (mount `/state` volume for restart-safe dedupe). |
| Tags | `latest`, plus immutable release/sha tags from GHCR publishing workflows. |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-french-road-traffic:latest
docker pull ghcr.io/clemensv/real-time-sources-french-road-traffic-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-french-road-traffic-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/french-road-traffic.json \
  -e KAFKA_BOOTSTRAP_SERVERS=<host:port> \
  -e KAFKA_TOPIC=french-road-traffic \
  -e SASL_USERNAME=<username> \
  -e SASL_PASSWORD=<password> \
  ghcr.io/clemensv/real-time-sources-french-road-traffic:latest
```

### With Azure Event Hubs / Fabric Event Stream connection string

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/french-road-traffic.json \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-french-road-traffic:latest
```

## Using the MQTT image

### Generic MQTT 5 broker (username/password)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/french-road-traffic.json \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-french-road-traffic-mqtt:latest
```

### Azure Event Grid namespace MQTT broker (Entra OAUTH2-JWT)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/french-road-traffic.json \
  -e MQTT_BROKER_URL='mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-french-road-traffic-mqtt:latest
```

## Using the AMQP image

### Generic AMQP 1.0 broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/french-road-traffic.json \
  -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/french-road-traffic' \
  ghcr.io/clemensv/real-time-sources-french-road-traffic-amqp:latest
```

### Azure Service Bus / Event Hubs (Entra CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/french-road-traffic.json \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='french-road-traffic' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-french-road-traffic-amqp:latest
```

### Azure Service Bus emulator / SAS namespaces (SAS CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/french-road-traffic.json \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='french-road-traffic' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-french-road-traffic-amqp:latest
```

## Environment variables

### Common

| Variable | Description |
|---|---|
| `STATE_FILE` | Path to persisted poll/dedupe state file. |
| `POLLING_INTERVAL` | Polling interval in seconds (where supported by the runtime variant). |
| `ONCE_MODE` | Run one poll cycle and exit (used by notebook scheduling). |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs / Fabric style connection string (overrides bootstrap/SASL fields). |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker list. |
| `KAFKA_TOPIC` | Kafka topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | Set `false` for plaintext Kafka links. |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` or `MQTT_HOST`/`MQTT_PORT` | MQTT broker endpoint. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Password auth for generic brokers. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra`. |
| `MQTT_ENTRA_CLIENT_ID` / `MQTT_ENTRA_AUDIENCE` | Entra token configuration for Event Grid MQTT. |
| `MQTT_CLIENT_ID` | MQTT client identifier. |
| `MQTT_CONTENT_MODE` | `binary` or `structured` CloudEvents payload mode. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` or `AMQP_HOST`/`AMQP_PORT`/`AMQP_TLS` | AMQP broker endpoint. |
| `AMQP_ADDRESS` | Queue/topic/address target. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials (`password` mode). |
| `AMQP_ENTRA_CLIENT_ID` / `AMQP_ENTRA_AUDIENCE` | Entra CBS token configuration. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS token material for emulator/SAS namespaces. |

## Deploying into Azure Container Instances

### MQTT — bring your own broker

Deploy MQTT against an existing MQTT 5.0 broker endpoint.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid MQTT broker

Deploy MQTT plus an Event Grid namespace broker and managed-identity role assignment.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

Deploy Kafka plus a new Event Hubs namespace and event hub.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template-with-eventhub.json)

### Kafka — bring your own Event Hub / Kafka

Deploy the Kafka container with your own Event Hubs/Fabric/Event Stream connection string.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffrench-road-traffic%2Fazure-template.json)

## Related

- [README.md](README.md) — project overview and hosting options.
- [EVENTS.md](EVENTS.md) — event contract and schema details.
- [`xreg/french_road_traffic.xreg.json`](xreg/french_road_traffic.xreg.json) — authoritative contract source.
