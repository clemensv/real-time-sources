# ENTSO-E Transparency Platform Bridge

Grid operators, energy traders, analysts, and public-sector planners use ENTSO-E Transparency Platform data to track European electricity demand, generation, prices, hydro storage, installed capacity, and cross-border physical flows. This feeder polls the ENTSO-E REST API, parses IEC 62325 XML documents, checkpoints high-water marks per market area, and emits CloudEvents for downstream operational dashboards, market analytics, compliance archives, and real-time intelligence systems.

## Transports

| Variant | Image | Delivery shape | Deployment templates |
|---|---|---|---|
| Kafka | `ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest` | Structured CloudEvents to Kafka/Event Hubs/Fabric Event Streams topic `entsoe-transparency` | `Dockerfile.kafka`, `azure-template.json`, `azure-template-with-eventhub.json` |
| MQTT/UNS | `ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest` | MQTT 5 binary-mode CloudEvents under `energy/eu/entsoe/transparency/...` | `Dockerfile.mqtt`, `azure-template-mqtt.json`, `azure-template-mqtt-eg.json` |
| AMQP 1.0 | `ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest` | AMQP 1.0 binary-mode CloudEvents to address `entsoe` | `Dockerfile.amqp`, `azure-template-amqp.json` |

Kafka is the log-oriented default for replayable analytics pipelines. MQTT/UNS is useful for lightweight subscribers that want a hierarchical topic tree by domain, PSR type, and cross-border pair. AMQP 1.0 serves queue/topic consumers on ActiveMQ Artemis, RabbitMQ AMQP 1.0, Qpid Dispatch, Azure Service Bus, or Event Hubs.

## Event families

The bridge covers A75 actual generation per type, A44 day-ahead prices, A65 actual total load, A69 wind/solar forecast, A70 load forecast margin, A71 generation forecast, A72 reservoir filling, A73 actual generation, A74 wind/solar generation, A68 installed generation capacity per type, and A11 cross-border physical flows. Event contracts are in [EVENTS.md](EVENTS.md).

## Quick start

```bash
# Kafka / Event Hubs / Fabric Event Streams
docker run --rm -e ENTSOE_SECURITY_TOKEN='<token>' -e CONNECTION_STRING='<event-hubs-or-fabric-connection-string>' ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest

# MQTT broker
docker run --rm -e ENTSOE_SECURITY_TOKEN='<token>' -e MQTT_BROKER_URL='mqtt://broker:1883' ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest

# AMQP generic broker
docker run --rm -e ENTSOE_SECURITY_TOKEN='<token>' -e AMQP_BROKER_URL='amqp://user:pass@broker:5672/entsoe' ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest
```

## Configuration

Common variables: `ENTSOE_SECURITY_TOKEN`, `ENTSOE_DOMAINS`, `ENTSOE_DOCUMENT_TYPES`, `ENTSOE_CROSS_BORDER_PAIRS`, `POLLING_INTERVAL`, `ENTSOE_LOOKBACK_HOURS`, `STATE_FILE`, `ONCE_MODE`.

Kafka uses `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME`, `SASL_PASSWORD`, `KAFKA_ENABLE_TLS`.
MQTT uses `MQTT_BROKER_URL`, `MQTT_AUTH_MODE`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_TLS`/`MQTT_ENABLE_TLS`, `MQTT_CLIENT_ID`, `MQTT_ENTRA_CLIENT_ID`, `MQTT_ENTRA_AUDIENCE`.
AMQP uses `AMQP_BROKER_URL` or `AMQP_HOST`/`AMQP_PORT`/`AMQP_ADDRESS`, `AMQP_AUTH_MODE`, `AMQP_USERNAME`, `AMQP_PASSWORD`, `AMQP_TLS`, `AMQP_ENTRA_CLIENT_ID`, `AMQP_ENTRA_AUDIENCE`, `AMQP_SAS_KEY_NAME`, `AMQP_SAS_KEY`.
See [CONTAINER.md](CONTAINER.md) for container deployment details.

## Repository layout

- `entsoe_core/` — shared ENTSO-E API acquisition, XML parsing, delta state, sample corpus.
- `entsoe_kafka/`, `entsoe_mqtt/`, `entsoe_amqp/` — transport-specific applications.
- `entsoe_producer/`, `entsoe_mqtt_producer/`, `entsoe_amqp_producer/` — generated xrcg producers (do not edit by hand).
- `Dockerfile.kafka`, `Dockerfile.mqtt`, `Dockerfile.amqp` — transport images.
- `xreg/entsoe.xreg.json` — authoritative CloudEvents/xRegistry contract.

## Azure deployment

[![Kafka BYO Event Hub](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template.json)
[![Kafka + Event Hub](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-eventhub.json)
[![MQTT BYO Broker](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-mqtt.json)
[![MQTT Event Grid](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-mqtt-eg.json)
[![AMQP Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-amqp.json)
