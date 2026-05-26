# UK EA Flood Monitoring container images

This document covers the published OCI container images for the UK EA Flood Monitoring feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://environment.data.gov.uk/flood-monitoring/doc/reference>
- API / data documentation: <https://environment.data.gov.uk/flood-monitoring/doc/reference>

<!-- upstream-links:end -->

## Why this container

The UK EA Flood Monitoring source is exposed as a polling API upstream. These container images package polling cadence control, stateful dedupe, CloudEvents production, and transport/auth wiring so operators can deploy a ready-to-run feeder instead of building source-specific integration code.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring` | Apache Kafka 2.x | JSON CloudEvents on one topic; key template `{station_reference}` |
| `ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring-mqtt` | MQTT 5.0 | Unified-Namespace topic template `(see EVENTS.md)` |
| `ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring-amqp` | AMQP 1.0 | Binary CloudEvents to AMQP node `uk-ea-flood-monitoring` |

Event families in this source:

- **UK.Gov.Environment.EA.FloodMonitoring** — `Station`, `Reading`.

## Image contract

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` (source Dockerfiles) |
| Default entry point | Kafka `["python", "-m", "uk_ea_flood_monitoring", "feed"]`; MQTT `["python", "-m", "uk_ea_flood_monitoring_mqtt", "feed"]`; AMQP `["python", "-m", "uk_ea_flood_monitoring_amqp", "feed"]` |
| Exposed ports | none — outbound publisher only |
| Signals | process exits cleanly on `SIGTERM` |
| Persistent state | `STATE_FILE`; mount a host volume for restart-safe dedupe/checkpoint behavior |
| Image tags | `:latest` and immutable release/sha tags published from repository CI |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring:latest
docker pull ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring-amqp:latest
```

## Using the Kafka image

### With a Kafka broker (SASL/PLAIN)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-ea-flood-monitoring.json \
  -e KAFKA_BOOTSTRAP_SERVERS="<host:port>" \
  -e KAFKA_TOPIC="<topic>" \
  -e SASL_USERNAME="<username>" \
  -e SASL_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring:latest
```

### With Azure Event Hubs / Fabric Event Streams

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-ea-flood-monitoring.json \
  -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring:latest
```

## Using the MQTT image

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-ea-flood-monitoring.json \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-ea-flood-monitoring.json \
  -e MQTT_BROKER_URL="mqtts://<namespace>.<region>-1.ts.eventgrid.azure.net:8883" \
  -e MQTT_AUTH_MODE=entra \
  -e MQTT_ENTRA_CLIENT_ID="<user-assigned-managed-identity-client-id>" \
  -e MQTT_CLIENT_ID="<unique-client-id>" \
  ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring-mqtt:latest
```

## Using the AMQP image

### With AMQP 1.0 and Microsoft Entra ID (CBS put-token)

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-ea-flood-monitoring.json \
  -e AMQP_HOST="<namespace>.servicebus.windows.net" \
  -e AMQP_PORT=5671 \
  -e AMQP_TLS=true \
  -e AMQP_ADDRESS="uk-ea-flood-monitoring" \
  -e AMQP_AUTH_MODE=entra \
  -e AMQP_ENTRA_AUDIENCE="https://servicebus.azure.net/.default" \
  -e AMQP_ENTRA_CLIENT_ID="<user-assigned-managed-identity-client-id>" \
  ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring-amqp:latest
```

### With AMQP 1.0 and SAS-token CBS

```bash
docker run --rm \
  -v "$PWD/state:/state" \
  -e STATE_FILE=/state/uk-ea-flood-monitoring.json \
  -e AMQP_HOST="servicebus-emulator" \
  -e AMQP_PORT=5672 \
  -e AMQP_ADDRESS="uk-ea-flood-monitoring" \
  -e AMQP_AUTH_MODE=sas \
  -e AMQP_SAS_KEY_NAME="RootManageSharedAccessKey" \
  -e AMQP_SAS_KEY="<sas-key>" \
  ghcr.io/clemensv/real-time-sources-uk-ea-flood-monitoring-amqp:latest
```

## Environment variables

### Kafka image

| Variable | Description |
|---|---|
| `STATE_FILE` | Path to dedupe/checkpoint state file. |
| `CONNECTION_STRING` | Event Hubs/Fabric-style connection string (optional alternative to explicit Kafka variables). |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list. |
| `KAFKA_TOPIC` | Kafka destination topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL/PLAIN credentials for Kafka. |
| `POLLING_INTERVAL` | Poll interval in seconds. |

### MQTT image

| Variable | Description |
|---|---|
| `STATE_FILE` | Path to dedupe/checkpoint state file. |
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`). |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for `MQTT_AUTH_MODE=password`. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra`. |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID. |
| `MQTT_CLIENT_ID` | MQTT client ID (must be unique per broker). |
| `POLLING_INTERVAL` | Poll interval in seconds. |

### AMQP image

| Variable | Description |
|---|---|
| `STATE_FILE` | Path to dedupe/checkpoint state file. |
| `AMQP_BROKER_URL` | Full AMQP URL form (`amqp://` or `amqps://`). |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component endpoint settings when URL form is not used. |
| `AMQP_ADDRESS` | AMQP node/address name. |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra-ID CBS settings. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS-token CBS settings. |
| `POLLING_INTERVAL` | Poll interval in seconds. |

## Deploying into Azure Container Instances

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fuk-ea-flood-monitoring%2Fazure-template.json)

## Related

- [README.md](README.md) — project overview and deployment options.
- [EVENTS.md](EVENTS.md) — CloudEvents contract and schema details.
- [`xreg/uk_ea_flood_monitoring.xreg.json`](xreg/uk_ea_flood_monitoring.xreg.json) — source contract used to generate producer bindings.
