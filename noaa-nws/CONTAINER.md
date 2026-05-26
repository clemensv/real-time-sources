# NOAA NWS container images

This document covers the published OCI container images for the NOAA NWS feeder, their environment-variable contract, authentication modes, and one-click Azure deployments. For the project overview see [README.md](README.md); for the CloudEvents contract see [EVENTS.md](EVENTS.md).
## Why this container

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.weather.gov/>
- API / data documentation: <https://www.weather.gov/documentation/services-web-api>

<!-- upstream-links:end -->

These images package the poller, contract-generated producers, and transport adapters so you can run NOAA NWS ingestion as a containerized workload without writing custom bridge code.

## What ships in the box

| Image | Transport | Default behavior |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-noaa-nws` | Apache Kafka 2.x | JSON CloudEvents (binary mode), key = `{station_id}` |
| `ghcr.io/clemensv/real-time-sources-noaa-nws-mqtt` | MQTT 5.0 | Topic template `(see xreg endpoint options)`, QoS 1, CloudEvent attrs as MQTT properties |
| `ghcr.io/clemensv/real-time-sources-noaa-nws-amqp` | AMQP 1.0 | AMQP node `noaa-nws`, binary CloudEvents, password/Entra/SAS auth |

Event families emitted by these images:

- **`WeatherAlert`**
- **`Zone`**
- **`ObservationStation`**
- **`WeatherObservation`**

## Image contract

| Aspect | Value |
| --- | --- |
| Base image | `python:3.12-slim` (multi-arch `linux/amd64`, `linux/arm64`) |
| Default entry point | Kafka `["python", "-m", "noaa_nws"]`; MQTT `["python", "-m", "noaa_nws_mqtt", "feed"]`; AMQP `["python", "-m", "noaa_nws_amqp", "feed"]` |
| Exposed ports | none — outbound publisher only |
| Signals | graceful shutdown on `SIGTERM` |
| Persistent state | `NWS_LAST_POLLED_FILE` (mount `/state` to persist dedupe/resume) |
| Image tags | `:latest`, `:v<semver>`, and `:sha-<git-sha>` |

## Installing the container images

```bash
docker pull ghcr.io/clemensv/real-time-sources-noaa-nws:latest
docker pull ghcr.io/clemensv/real-time-sources-noaa-nws-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-noaa-nws-amqp:latest
```

## Using the Kafka image

### With a Kafka broker

```bash
docker run --rm   -v "$PWD/state:/state"   -e NWS_LAST_POLLED_FILE=/state/noaa-nws.json   -e KAFKA_BOOTSTRAP_SERVERS='<kafka-bootstrap-servers>'   -e KAFKA_TOPIC='<kafka-topic>'   -e SASL_USERNAME='<sasl-username>'   -e SASL_PASSWORD='<sasl-password>'   ghcr.io/clemensv/real-time-sources-noaa-nws:latest
```

### With Azure Event Hubs or Fabric Event Streams

```bash
docker run --rm   -v "$PWD/state:/state"   -e NWS_LAST_POLLED_FILE=/state/noaa-nws.json   -e CONNECTION_STRING='<connection-string>'   ghcr.io/clemensv/real-time-sources-noaa-nws:latest
```

## Using the MQTT image

### With a generic MQTT 5 broker (username/password)

```bash
docker run --rm   -v "$PWD/state:/state"   -e NWS_LAST_POLLED_FILE=/state/noaa-nws.json   -e MQTT_BROKER_URL='mqtts://<broker-host>:8883'   -e MQTT_USERNAME='<username>'   -e MQTT_PASSWORD='<password>'   ghcr.io/clemensv/real-time-sources-noaa-nws-mqtt:latest
```

### With Azure Event Grid namespace MQTT broker (Microsoft Entra JWT)

```bash
docker run --rm   -v "$PWD/state:/state"   -e NWS_LAST_POLLED_FILE=/state/noaa-nws.json   -e MQTT_BROKER_URL='mqtts://<ns>.<region>-1.ts.eventgrid.azure.net:8883'   -e MQTT_AUTH_MODE=entra   -e MQTT_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>'   -e MQTT_CLIENT_ID='<unique-client-id>'   ghcr.io/clemensv/real-time-sources-noaa-nws-mqtt:latest
```

## Using the AMQP image

### Generic AMQP 1.0 brokers (SASL PLAIN)

```bash
docker run --rm   -v "$PWD/state:/state"   -e NWS_LAST_POLLED_FILE=/state/noaa-nws.json   -e AMQP_BROKER_URL='amqp://<user>:<password>@<broker-host>:5672/noaa-nws'   ghcr.io/clemensv/real-time-sources-noaa-nws-amqp:latest
```

### Azure Service Bus / Event Hubs (Microsoft Entra ID via CBS)

```bash
docker run --rm   -v "$PWD/state:/state"   -e NWS_LAST_POLLED_FILE=/state/noaa-nws.json   -e AMQP_HOST='<namespace>.servicebus.windows.net'   -e AMQP_PORT=5671 -e AMQP_TLS=true   -e AMQP_ADDRESS='noaa-nws'   -e AMQP_AUTH_MODE=entra   -e AMQP_ENTRA_AUDIENCE='https://servicebus.azure.net/.default'   -e AMQP_ENTRA_CLIENT_ID='<user-assigned-managed-identity-client-id>'   ghcr.io/clemensv/real-time-sources-noaa-nws-amqp:latest
```

### Azure Service Bus emulator / SAS-only namespaces (SAS-token CBS)

```bash
docker run --rm   -v "$PWD/state:/state"   -e NWS_LAST_POLLED_FILE=/state/noaa-nws.json   -e AMQP_HOST='servicebus-emulator'   -e AMQP_PORT=5672   -e AMQP_ADDRESS='noaa-nws'   -e AMQP_AUTH_MODE=sas   -e AMQP_SAS_KEY_NAME='RootManageSharedAccessKey'   -e AMQP_SAS_KEY='<sas-key>'   ghcr.io/clemensv/real-time-sources-noaa-nws-amqp:latest
```

## Environment variables

### Common (all images)

| Variable | Description |
|---|---|
| `NWS_LAST_POLLED_FILE` | Path to the dedupe/resume state file. Mount `/state` so it survives restarts. |
| `POLLING_INTERVAL` | Seconds between polling cycles. |

### Kafka image

| Variable | Description |
|---|---|
| `CONNECTION_STRING` | Event Hubs / Fabric Event Stream connection string (overrides bootstrap settings). |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker list when not using `CONNECTION_STRING`. |
| `KAFKA_TOPIC` | Target topic. |
| `SASL_USERNAME` / `SASL_PASSWORD` | SASL PLAIN credentials. |
| `KAFKA_ENABLE_TLS` | `false` disables TLS (default `true`). |

### MQTT image

| Variable | Description |
|---|---|
| `MQTT_BROKER_URL` | Broker URL (e.g. `mqtts://host:8883`). |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for password mode. |
| `MQTT_AUTH_MODE` | `password` (default) or `entra`. |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed identity client id. |
| `MQTT_CLIENT_ID` | Unique MQTT client identifier. |
| `MQTT_CONTENT_MODE` | `binary` (default) or `structured`. |

### AMQP image

| Variable | Description |
|---|---|
| `AMQP_BROKER_URL` | Full broker URL (`amqp://` / `amqps://`). |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Host-style configuration when not using URL. |
| `AMQP_ADDRESS` | Target AMQP node (queue/topic/address). |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `password` mode. |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra ID token settings for `entra` mode. |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS-token inputs for `sas` mode. |
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured`. |

## Deploying into Azure Container Instances

### AMQP — bring your own AMQP broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-amqp.json)

### MQTT — bring your own broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-mqtt.json)

### MQTT — provision a new Event Grid namespace MQTT broker

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-with-eventgrid-mqtt.json)

### Kafka — provision a new Event Hub

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-with-eventhub.json)

### AMQP — provision a new Azure Service Bus namespace

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template-with-servicebus.json)

### Kafka — bring your own Event Hub / Kafka

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fnoaa-nws%2Fazure-template.json)

## Related

- [README.md](README.md) — project overview, use cases, and quick-start paths.
- [EVENTS.md](EVENTS.md) — CloudEvents contract, schemas, and routing metadata.
- [`xreg/noaa_nws.xreg.json`](xreg/noaa_nws.xreg.json) — source contract used for generated producers and EVENTS.md.
