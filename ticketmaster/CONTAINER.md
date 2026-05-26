# Ticketmaster Discovery API container images

Related docs:

- [README.md](README.md) — source context, quick-start flow, and deployment guidance.
- [EVENTS.md](EVENTS.md) — event families, CloudEvents types, and payload schemas.

> [!WARNING]
> You are responsible for complying with Ticketmaster Terms, branding rules, and rate limits when using or redistributing this data.

## Why this container

These images package the Ticketmaster Discovery API bridge runtime so teams can run a production feeder with consistent event contracts across Kafka, MQTT, and AMQP transports.

## What ships in the box

| Image | Dockerfile | Purpose |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-ticketmaster:latest` | `Dockerfile` | Kafka-compatible publishing path |
| `ghcr.io/clemensv/real-time-sources-ticketmaster-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 publishing path |
| `ghcr.io/clemensv/real-time-sources-ticketmaster-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 publishing path |

## Image contract

| Aspect | Kafka | MQTT | AMQP |
|---|---|---|---|
| Base image | `python:3.10-slim` | `python:3.10-slim` | `python:3.10-slim` |
| Default command | `CMD ["python", "-m", "ticketmaster", "feed"]` | `CMD ["python", "-m", "ticketmaster_mqtt", "feed"]` | `CMD ["python", "-m", "ticketmaster_amqp", "feed"]` |
| Delivery format | CloudEvents to Kafka topic | CloudEvents to MQTT topic tree | CloudEvents to AMQP address |
| Shared contract | \- | Uses same xRegistry event model | Uses same xRegistry event model |

## Kafka image quick start

```bash
docker run --rm   -e TICKETMASTER_API_KEY="<api-key>" -e CONNECTION_STRING="<connection-string>"   ghcr.io/clemensv/real-time-sources-ticketmaster:latest
```

## MQTT image quick start

```bash
docker run --rm   -e TICKETMASTER_API_KEY="<api-key>" -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-ticketmaster-mqtt:latest
```

## AMQP image quick start

```bash
docker run --rm   -e TICKETMASTER_API_KEY="<api-key>" -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/ticketmaster"   ghcr.io/clemensv/real-time-sources-ticketmaster-amqp:latest
```

## Environment variable matrix

### Kafka image (`ghcr.io/clemensv/real-time-sources-ticketmaster:latest`)

| Variable | Purpose |
|---|---|
| `TICKETMASTER_API_KEY` | Core configuration for this image variant. |
| `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS` | Core configuration for this image variant. |
| `KAFKA_TOPIC` | Core configuration for this image variant. |
| `COUNTRY_CODES` | Core configuration for this image variant. |
| `POLL_INTERVAL` | Core configuration for this image variant. |
| `REFERENCE_REFRESH` | Core configuration for this image variant. |
| `STATE_FILE` | Core configuration for this image variant. |
| `KAFKA_ENABLE_TLS` | Core configuration for this image variant. |
| `TICKETMASTER_CITY` | Core configuration for this image variant. |
| `TICKETMASTER_VENUE_ID` | Core configuration for this image variant. |
| `TICKETMASTER_ATTRACTION_ID` | Core configuration for this image variant. |
| `TICKETMASTER_SEGMENT_ID` | Core configuration for this image variant. |
| `TICKETMASTER_GENRE_ID` | Core configuration for this image variant. |
| `TICKETMASTER_SUB_GENRE_ID` | Core configuration for this image variant. |
| `TICKETMASTER_MARKET_ID` | Core configuration for this image variant. |
| `TICKETMASTER_POSTAL_CODE` | Core configuration for this image variant. |
| `TICKETMASTER_LOCALE` | Core configuration for this image variant. |
| `TICKETMASTER_SORT` | Core configuration for this image variant. |
| `TICKETMASTER_PAGE_SIZE` | Core configuration for this image variant. |
| `TICKETMASTER_START_DATETIME` | Core configuration for this image variant. |
| `TICKETMASTER_END_DATETIME` | Core configuration for this image variant. |
| `TICKETMASTER_LOOKAHEAD_DAYS` | Core configuration for this image variant. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-ticketmaster-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `TICKETMASTER_API_KEY` | Core configuration for this image variant. |
| `MQTT_BROKER_URL` | Core configuration for this image variant. |
| `MQTT_USERNAME` | Core configuration for this image variant. |
| `MQTT_PASSWORD` | Core configuration for this image variant. |
| `MQTT_CLIENT_ID` | Core configuration for this image variant. |
| `COUNTRY_CODES` | Core configuration for this image variant. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-ticketmaster-amqp:latest`)

| Variable | Purpose |
|---|---|
| `TICKETMASTER_API_KEY` | Core configuration for this image variant. |
| `AMQP_BROKER_URL` | Core configuration for this image variant. |
| `AMQP_ADDRESS` | Core configuration for this image variant. |
| `AMQP_AUTH_MODE` | Core configuration for this image variant. |
| `COUNTRY_CODES` | Core configuration for this image variant. |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-amqp.json` — AMQP deployment targeting an existing AMQP 1.0 broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-amqp.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fticketmaster%2Fazure-template.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
