# ENTSO-E Transparency Platform container images

Related docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://transparency.entsoe.eu/>
- API / data documentation: <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html>

<!-- upstream-links:end -->

- [README.md](README.md) — source context, quick-start flow, and deployment guidance.
- [EVENTS.md](EVENTS.md) — event families, CloudEvents types, and payload schemas.

## Why this container

These images package the ENTSO-E Transparency Platform bridge runtime so teams can run a production feeder with consistent event contracts across Kafka, MQTT, and AMQP transports.

## What ships in the box

| Image | Dockerfile | Purpose |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest` | `Dockerfile` | Kafka-compatible publishing path |
| `ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 publishing path |
| `ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 publishing path |

## Image contract

| Aspect | Kafka | MQTT | AMQP |
|---|---|---|---|
| Base image | `python:3.10-slim` | `python:3.10-slim` | `python:3.10-slim` |
| Default command | `CMD ["python", "-m", "entsoe_kafka", "feed"]` | `CMD ["python", "-m", "entsoe_mqtt", "feed"]` | `CMD ["python", "-m", "entsoe_amqp", "feed"]` |
| Delivery format | CloudEvents to Kafka topic | CloudEvents to MQTT topic tree | CloudEvents to AMQP address |
| Shared contract | \- | Uses same xRegistry event model | Uses same xRegistry event model |

## Kafka image quick start

```bash
docker run --rm   -e ENTSOE_SECURITY_TOKEN="<token>" -e CONNECTION_STRING="<connection-string>"   ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest
```

## MQTT image quick start

```bash
docker run --rm   -e ENTSOE_SECURITY_TOKEN="<token>" -e MQTT_BROKER_URL="mqtt://<broker>:1883"   ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest
```

## AMQP image quick start

```bash
docker run --rm   -e ENTSOE_SECURITY_TOKEN="<token>" -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/entsoe"   ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest
```

## Environment variable matrix

### Kafka image (`ghcr.io/clemensv/real-time-sources-entsoe-kafka:latest`)

| Variable | Purpose |
|---|---|
| `ENTSOE_SECURITY_TOKEN` | Core configuration for this image variant. |
| `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS` | Core configuration for this image variant. |
| `KAFKA_TOPIC` | Core configuration for this image variant. |
| `ENTSOE_DOMAINS` | Core configuration for this image variant. |
| `ENTSOE_DOCUMENT_TYPES` | Core configuration for this image variant. |
| `ENTSOE_CROSS_BORDER_PAIRS` | Core configuration for this image variant. |
| `POLLING_INTERVAL` | Core configuration for this image variant. |
| `STATE_FILE` | Core configuration for this image variant. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-entsoe-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `ENTSOE_SECURITY_TOKEN` | Core configuration for this image variant. |
| `MQTT_BROKER_URL` | Core configuration for this image variant. |
| `MQTT_AUTH_MODE` | Core configuration for this image variant. |
| `MQTT_USERNAME / MQTT_PASSWORD` | Core configuration for this image variant. |
| `MQTT_ENTRA_CLIENT_ID` | Core configuration for this image variant. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-entsoe-amqp:latest`)

| Variable | Purpose |
|---|---|
| `ENTSOE_SECURITY_TOKEN` | Core configuration for this image variant. |
| `AMQP_BROKER_URL` | Core configuration for this image variant. |
| `AMQP_ADDRESS` | Core configuration for this image variant. |
| `AMQP_AUTH_MODE` | Core configuration for this image variant. |
| `AMQP_ENTRA_CLIENT_ID` | Core configuration for this image variant. |
| `AMQP_SAS_KEY_NAME / AMQP_SAS_KEY` | Core configuration for this image variant. |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-amqp.json` — AMQP deployment targeting an existing AMQP 1.0 broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-amqp.json)
- `azure-template-mqtt-eg.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-mqtt-eg.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fentsoe%2Fazure-template.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
