# ERDDAP container images — Kafka, MQTT, and AMQP

[Project overview](README.md) · [Event schemas](EVENTS.md) · [KQL schema](kql/erddap.kql) · [Deploy portal](https://clemensv.github.io/real-time-sources#erddap)

The ERDDAP images poll configured keyless or authenticated ERDDAP tabledap TimeSeries datasets, emit dataset/station reference data first, then stream generic observation CloudEvents.

## Image contract

| Image tag | Transport | Dockerfile | State |
|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-erddap-kafka:latest` | Kafka/Event Hubs/Fabric | `Dockerfile.kafka` | `STATE_FILE` |
| `ghcr.io/clemensv/real-time-sources-erddap-mqtt:latest` | MQTT 5.0 | `Dockerfile.mqtt` | `STATE_FILE` |
| `ghcr.io/clemensv/real-time-sources-erddap-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | `STATE_FILE` |

Base image: `python:3.10-slim`. Entry points: `python -m erddap_kafka feed`, `python -m erddap_mqtt feed`, `python -m erddap_amqp feed`.

## Common environment

| Variable | Default | Description |
|---|---|---|
| `ERDDAP_SOURCES` | IOOS SUN2 default | Semicolon list, JSON array, `@file`, or path describing configured ERDDAP datasets. |
| `ERDDAP_MOCK` | `false` | Use the checked-in offline tabledap fixture and exit after one cycle. |
| `POLLING_INTERVAL` | `300` | Seconds between tabledap polling cycles. |
| `REFERENCE_REFRESH_INTERVAL` | `21600` | Seconds between dataset/station reference refreshes. |
| `STATE_FILE` | `~/.erddap_state.json` | Dedupe state file; mount a volume in containers. |
| `ONCE_MODE` | `false` | Exit after one poll cycle; used by tests and Fabric Notebook hosting. |

## Kafka

```bash
docker run --rm -e CONNECTION_STRING='BootstrapServer=host:9092;EntityPath=erddap' -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-erddap-kafka:latest
```

Kafka variables: `CONNECTION_STRING`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `KAFKA_ENABLE_TLS`, `SASL_USERNAME`, `SASL_PASSWORD`.

## MQTT

```bash
docker run --rm -e MQTT_BROKER_URL='broker:1883' -e MQTT_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-erddap-mqtt:latest
```

MQTT variables: `MQTT_BROKER_URL`, `MQTT_ENABLE_TLS`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CA_FILE`, `MQTT_CLIENT_ID`. Event Grid namespace deployments use the MQTT image and Entra-capable template generated for this repo.

## AMQP 1.0

```bash
docker run --rm -e AMQP_BROKER_URL='amqp://user:pass@broker:5672/erddap' ghcr.io/clemensv/real-time-sources-erddap-amqp:latest
```

AMQP variables: `AMQP_BROKER_URL`, `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS`, `AMQP_TLS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, `AMQP_AUTH_MODE`, `AMQP_ENTRA_AUDIENCE`, `AMQP_ENTRA_CLIENT_ID`.

## Azure and Fabric

The catalog exposes five Azure templates (Kafka BYO/Event Hubs, MQTT BYO/Event Grid, AMQP Service Bus) and a Fabric Notebook option. The notebook uses the same Kafka bridge in `--once` mode and resolves the Eventstream connection string at runtime; it does not store `CONNECTION_STRING` as a parameter.
