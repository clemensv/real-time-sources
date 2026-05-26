# GraceDB container images

This document covers the published container images for the GraceDB feeder. For overview and business context see [README.md](README.md); for event-contract details see [EVENTS.md](EVENTS.md).

## Why this container

GraceDB superevents are key inputs for multi-messenger astronomy alerting and analysis workflows. This feeder republishes candidate alerts as CloudEvents.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-gracedb` | Kafka | Polls upstream and publishes CloudEvents to one topic |
| `ghcr.io/clemensv/real-time-sources-gracedb-mqtt` | MQTT 5.0 | Publishes CloudEvents to xRegistry-mapped topics |
| `ghcr.io/clemensv/real-time-sources-gracedb-amqp` | AMQP 1.0 | Publishes CloudEvents to one AMQP address |

## Image contract

| Aspect | Value |
|---|---|
| Base image | `python:3.10-slim` |
| Default entrypoint | `python -m gracedb feed; python -m gracedb_mqtt feed; python -m gracedb_amqp feed` |
| Exposed ports | none — outbound publisher only |
| Signals | exits on `SIGTERM`; in-flight poll cycle is completed/flushed before shutdown where supported |
| State | Kafka: GRACEDB_LAST_POLLED_FILE; MQTT: GRACEDB_MQTT_LAST_POLLED_FILE; AMQP: GRACEDB_AMQP_LAST_POLLED_FILE. Mount `/state` when state is used. |
| Tags | `:latest` (mainline), plus immutable release/SHA tags published in GHCR. |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-gracedb:latest
docker pull ghcr.io/clemensv/real-time-sources-gracedb-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-gracedb-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e GRACEDB_LAST_POLLED_FILE=/state/gracedb.json \
  -e KAFKA_BOOTSTRAP_SERVERS='<broker:9093>' \
  -e KAFKA_TOPIC='<topic>' \
  -e SASL_USERNAME='<username>' \
  -e SASL_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-gracedb:latest
```

### With Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e GRACEDB_LAST_POLLED_FILE=/state/gracedb.json \
  -e CONNECTION_STRING='<connection-string>' \
  ghcr.io/clemensv/real-time-sources-gracedb:latest
```

## Using the MQTT image

### With username/password authentication

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e GRACEDB_MQTT_LAST_POLLED_FILE=/state/gracedb-mqtt.json \
  -e MQTT_BROKER_URL='mqtts://<broker-host>:8883' \
  -e MQTT_USERNAME='<username>' \
  -e MQTT_PASSWORD='<password>' \
  ghcr.io/clemensv/real-time-sources-gracedb-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Entra)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e GRACEDB_MQTT_LAST_POLLED_FILE=/state/gracedb-mqtt.json \
  -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883' \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  -e MQTT_CLIENT_ID='<unique-client-id>' \
  ghcr.io/clemensv/real-time-sources-gracedb-mqtt:latest
```

## Using the AMQP image

### With Microsoft Entra ID (AMQP CBS)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e GRACEDB_AMQP_LAST_POLLED_FILE=/state/gracedb-amqp.json \
  -e AMQP_HOST='<namespace>.servicebus.windows.net' \
  -e AMQP_PORT=5671 -e AMQP_TLS=true \
  -e AMQP_ADDRESS='gracedb' \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default' \
  -e AMQP_ENTRA_CLIENT_ID='<managed-identity-client-id>' \
  ghcr.io/clemensv/real-time-sources-gracedb-amqp:latest
```

### With SAS token CBS (Service Bus emulator / SAS-only namespaces)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e GRACEDB_AMQP_LAST_POLLED_FILE=/state/gracedb-amqp.json \
  -e AMQP_HOST='servicebus-emulator' \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS='gracedb' \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey' \
  -e AMQP_SAS_KEY='<sas-key>' \
  ghcr.io/clemensv/real-time-sources-gracedb-amqp:latest
```

## Environment variables

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs/Fabric-style or Kafka-style connection string. |
| `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC` | Explicit Kafka destination. |
| `SASL_USERNAME`, `SASL_PASSWORD` | SASL PLAIN credentials when needed. |
| `KAFKA_ENABLE_TLS` | Set `false` for plaintext Kafka. |
| `ONCE_MODE` | Run one cycle and exit (where supported). |
| State variable | `GRACEDB_LAST_POLLED_FILE` |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_USERNAME`, `MQTT_PASSWORD` | Optional broker credentials. |
| `MQTT_CLIENT_ID` | Optional explicit client ID. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured` where supported. |
| State variable | `GRACEDB_MQTT_LAST_POLLED_FILE` |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Broker URL (`amqp://` or `amqps://`). |
| `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS` | Component-level AMQP endpoint settings. |
| `AMQP_USERNAME`, `AMQP_PASSWORD` | SASL PLAIN credentials (if used). |
| `AMQP_AUTH_MODE` | Auth mode where supported (`password`/`entra`/`sas`). |
| `AMQP_TLS` | Enable TLS where supported. |
| State variable | `GRACEDB_AMQP_LAST_POLLED_FILE` |

## Deploying into Microsoft Fabric

Fabric notebook and Fabric ACI hosting are both supported:

- Notebook: `tools/deploy-fabric/deploy-feeder-notebook.ps1 -Source gracedb ...`
- ACI: `tools/deploy-fabric/deploy-fabric-aci.ps1 -Source gracedb ...`

Portal links:

- [Fabric Notebook](https://clemensv.github.io/real-time-sources/#gracedb/fabric-notebook)
- [Fabric ACI](https://clemensv.github.io/real-time-sources/#gracedb/fabric-aci)

## Deploying into Azure Container Instances

### AMQP — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-amqp.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template-with-eventhub.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fgracedb%2Fazure-template.json)

## Related
- [README.md](README.md) — source overview, use cases, and quick start.
- [EVENTS.md](EVENTS.md) — event contract and schema details.
- [`xreg/gracedb.xreg.json`](xreg/gracedb.xreg.json) — authoritative manifest.
