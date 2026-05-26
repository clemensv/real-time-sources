# Digitraffic Maritime container deployment guide

> See also: [README.md](README.md) · [EVENTS.md](EVENTS.md)

This source ships three container variants.

## Images

| Variant | Image | Dockerfile | Runtime command |
|---|---|---|---|
| Kafka | `ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest` | `Dockerfile` | `python -m digitraffic_maritime stream` |
| MQTT | `ghcr.io/clemensv/real-time-sources-digitraffic-maritime-mqtt:latest` | `Dockerfile.mqtt` | `python -m digitraffic_maritime_mqtt feed` |
| AMQP | `ghcr.io/clemensv/real-time-sources-digitraffic-maritime-amqp:latest` | `Dockerfile.amqp` | `python -m digitraffic_maritime_amqp feed` |

## Kafka variant

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `CONNECTION_STRING` | yes* | Event Hubs / Fabric style connection string (`BootstrapServer=...;EntityPath=...` also supported) |
| `KAFKA_BOOTSTRAP_SERVERS` | yes* | Kafka bootstrap servers when `CONNECTION_STRING` is not used |
| `KAFKA_TOPIC` | yes* | Kafka topic |
| `SASL_USERNAME` / `SASL_PASSWORD` | optional | SASL PLAIN credentials |
| `DIGITRAFFIC_SUBSCRIBE` | no | `location,metadata` or subset |
| `DIGITRAFFIC_FILTER_MMSI` | no | Comma-separated MMSI filter |
| `DIGITRAFFIC_FLUSH_INTERVAL` | no | Flush cadence |
| `DIGITRAFFIC_PORTCALL_POLL_INTERVAL` | no | Poll interval for `port-calls` mode |
| `DIGITRAFFIC_PORTCALL_STATE_FILE` | no | State file path |

\* provide either `CONNECTION_STRING`, or the Kafka trio.

### Run

```bash
docker run --rm \
  -e CONNECTION_STRING='BootstrapServer=<host:9092>;EntityPath=digitraffic-maritime' \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime:latest
```

## MQTT variant

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `MQTT_BROKER_URL` | yes | Broker URL (`mqtt://host:1883` or `mqtts://host:8883`) |
| `MQTT_ENABLE_TLS` | no | Force TLS (`true`/`false`) |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | no | Username/password auth |
| `MQTT_CA_FILE` | no | Custom CA bundle |
| `MQTT_CLIENT_ID` | no | MQTT client id override |
| `MQTT_CONTENT_MODE` | no | `binary` (default) or `structured` |
| `DIGITRAFFIC_MODE` | no | `stream` (default) or `port-calls` |
| `ONCE_MODE` | no | Exit after first emitted cycle/message |

### Run

```bash
docker run --rm \
  -e MQTT_BROKER_URL='mqtt://broker:1883' \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime-mqtt:latest
```

## AMQP variant

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `AMQP_BROKER_URL` | yes* | AMQP URL (`amqp://user:pass@host:5672/address`) |
| `AMQP_HOST` / `AMQP_PORT` / `AMQP_ADDRESS` | yes* | Host tuple alternative to URL |
| `AMQP_AUTH_MODE` | no | `password` (default) or `entra` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | conditional | SASL PLAIN credentials |
| `AMQP_ENTRA_AUDIENCE` | conditional | AAD scope for `entra` mode |
| `AMQP_ENTRA_CLIENT_ID` | no | User-assigned managed identity client id |
| `AMQP_TLS` | no | TLS toggle |
| `AMQP_CONTENT_MODE` | no | `binary` (default) or `structured` |
| `DIGITRAFFIC_MODE` | no | `stream` (default) or `port-calls` |
| `ONCE_MODE` | no | Exit after first emitted cycle/message |

\* provide `AMQP_BROKER_URL`, or host/port/address.

### Run

```bash
docker run --rm \
  -e AMQP_BROKER_URL='amqp://user:password@broker:5672/digitraffic-maritime' \
  ghcr.io/clemensv/real-time-sources-digitraffic-maritime-amqp:latest
```

## Azure deploy buttons

### Kafka

[![Deploy to Azure + EH](https://img.shields.io/badge/Azure-Container%20%2B%20Event%20Hub-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-eventhub.json)
[![Deploy to Azure (BYO EH)](https://img.shields.io/badge/Azure-Container%20(BYO%20Event%20Hub)-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template.json)

### MQTT

[![Deploy MQTT (BYO broker)](https://img.shields.io/badge/Azure-MQTT%20BYO%20Broker-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-mqtt.json)
[![Deploy MQTT + Event Grid](https://img.shields.io/badge/Azure-MQTT%20%2B%20Event%20Grid-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-eventgrid-mqtt.json)

### AMQP

[![Deploy AMQP + Service Bus](https://img.shields.io/badge/Azure-AMQP%20%2B%20Service%20Bus-0078D4?logo=microsoftazure&logoColor=white)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fdigitraffic-maritime%2Fazure-template-with-servicebus.json)

## Notes

- Digitraffic data terms require attribution to Fintraffic/digitraffic.fi.
- Streaming reliability depends on upstream MQTT and Portnet API availability.
- Event Grid MQTT guidance: <https://learn.microsoft.com/azure/event-grid/mqtt-overview>
