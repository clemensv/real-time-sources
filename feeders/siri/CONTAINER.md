# SIRI container images

[📘 **Overview**](README.md) · [📑 **Event schemas**](EVENTS.md) · [🗄️ **KQL schema**](kql/siri.kql)

This document covers the published OCI images for the generic `siri` feeder, their environment-variable contract, and the Azure deployment templates shipped with the source.

## Images

| Image | Transport | Default destination |
| --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-siri-kafka` | Apache Kafka | topic `siri` |
| `ghcr.io/clemensv/real-time-sources-siri-mqtt` | MQTT 5.0 / UNS | `transit/siri/...` |
| `ghcr.io/clemensv/real-time-sources-siri-amqp` | AMQP 1.0 | node `siri` |

## Image contract

| Aspect | Value |
| --- | --- |
| Base image | `python:3.10-slim` |
| Entry points | `python -m siri_kafka feed`, `python -m siri_mqtt feed`, `python -m siri_amqp feed` |
| Persistent state | `STATE_FILE` |
| Poll cadence | `POLLING_INTERVAL` seconds (default `30`) |
| Shared source config | `SIRI_PROVIDER`, `SIRI_URL`, `SIRI_API_KEY`, `SIRI_OPERATORS`, `SIRI_DATA_TYPES` |

## Shared source settings

| Variable | Description |
| --- | --- |
| `SIRI_PROVIDER` | `bods`, `trafiklab`, or `custom` (default `bods`) |
| `SIRI_URL` | Optional BODS override, Trafiklab URL template, or required direct custom URL |
| `SIRI_API_KEY` | Provider API key |
| `SIRI_OPERATORS` | Optional comma-separated operator filter / Trafiklab template expansion values |
| `SIRI_DATA_TYPES` | Comma-separated `vm,et,sx`; default `vm` |
| `POLLING_INTERVAL` | Poll interval in seconds |
| `STATE_FILE` | Restart-safe dedupe state file |
| `ONCE_MODE` | Run one polling cycle and exit |

## Kafka image

Additional variables:

| Variable | Description |
| --- | --- |
| `CONNECTION_STRING` | Event Hubs / Fabric connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka bootstrap server list |
| `KAFKA_TOPIC` | Destination topic (default `siri`) |
| `SASL_USERNAME` / `SASL_PASSWORD` | Credentials when not using `CONNECTION_STRING` |
| `KAFKA_ENABLE_TLS` | `false` disables TLS |

Example:

```bash
docker run --rm \
  -e SIRI_PROVIDER=bods \
  -e SIRI_API_KEY="<bods-api-key>" \
  -e CONNECTION_STRING="<connection-string>" \
  ghcr.io/clemensv/real-time-sources-siri-kafka:latest
```

## MQTT image

Additional variables:

| Variable | Description |
| --- | --- |
| `MQTT_BROKER_URL` | Broker URL (`mqtt://` or `mqtts://`) |
| `MQTT_HOST` / `MQTT_PORT` | Component endpoint settings |
| `MQTT_ENABLE_TLS` | Enable TLS |
| `MQTT_AUTH_MODE` | `anonymous`, `userpass`, or `entra` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | Credentials for `userpass` |
| `MQTT_CLIENT_ID` | MQTT client id |
| `MQTT_ENTRA_CLIENT_ID` / `MQTT_ENTRA_AUDIENCE` | Entra auth settings |

Example:

```bash
docker run --rm \
  -e SIRI_PROVIDER=trafiklab \
  -e SIRI_URL="https://api.trafiklab.se/siri2.x/{data_type}/{operator}" \
  -e SIRI_API_KEY="<trafiklab-api-key>" \
  -e SIRI_OPERATORS="skane/skanetrafiken" \
  -e MQTT_BROKER_URL="mqtts://<broker-host>:8883" \
  -e MQTT_AUTH_MODE=userpass \
  -e MQTT_USERNAME="<username>" \
  -e MQTT_PASSWORD="<password>" \
  ghcr.io/clemensv/real-time-sources-siri-mqtt:latest
```

## AMQP image

Additional variables:

| Variable | Description |
| --- | --- |
| `AMQP_BROKER_URL` | Full AMQP URL form |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_TLS` | Component endpoint settings |
| `AMQP_ADDRESS` | AMQP node/address (default `siri`) |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | Generic broker credentials |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra CBS settings |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS settings |

Example:

```bash
docker run --rm \
  -e SIRI_PROVIDER=custom \
  -e SIRI_URL="https://example.test/siri/vm" \
  -e SIRI_API_KEY="<api-key>" \
  -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker-host>:5672/siri" \
  ghcr.io/clemensv/real-time-sources-siri-amqp:latest
```

## Azure templates

The source ships templates for:

- `azure-template.json` — Kafka container against an existing Kafka/Event Hubs endpoint
- `azure-template-with-eventhub.json` — Kafka container plus a new Event Hubs namespace
- `azure-template-mqtt.json` — MQTT container against an existing broker
- `azure-template-with-eventgrid-mqtt.json` — MQTT container plus an Event Grid namespace broker
- `azure-template-with-servicebus.json` — AMQP container plus a Service Bus namespace

All templates expose `siriProvider`, `siriUrl`, `siriApiKey`, and `siriOperators` parameters.
