# Wikimedia EventStreams RecentChange container images

Related docs:

- [README.md](README.md) — source context, quick-start flow, and deployment guidance.
- [EVENTS.md](EVENTS.md) — event families, CloudEvents types, and payload schemas.

## Why this container

These images package the Wikimedia EventStreams RecentChange bridge runtime so teams can run a production feeder with consistent event contracts across Kafka, MQTT, and AMQP transports.

## What ships in the box

| Image | Dockerfile | Purpose |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest` | `Dockerfile` | Kafka-compatible publishing path |
| `ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5.0 publishing path |
| `ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 publishing path |

## Image contract

| Aspect | Kafka | MQTT | AMQP |
|---|---|---|---|
| Base image | `python:3.10-slim` | `python:3.10-slim` | `python:3.10-slim` |
| Default command | `CMD ["python", "-m", "wikimedia_eventstreams", "feed"]` | `CMD ["python", "-m", "wikimedia_eventstreams_mqtt", "feed"]` | `CMD ["python", "-m", "wikimedia_eventstreams_amqp", "feed"]` |
| Delivery format | CloudEvents to Kafka topic | CloudEvents to MQTT topic tree | CloudEvents to AMQP address |
| Shared contract | \- | Uses same xRegistry event model | Uses same xRegistry event model |

## Kafka image quick start

```bash
docker run --rm   -e CONNECTION_STRING="<connection-string>"   ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest
```

## MQTT image quick start

```bash
docker run --rm   -e MQTT_BROKER_URL="mqtts://<broker>:8883" -e MQTT_USERNAME="<user>" -e MQTT_PASSWORD="<password>"   ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-mqtt:latest
```

## AMQP image quick start

```bash
docker run --rm   -e AMQP_BROKER_URL="amqp://<user>:<password>@<broker>:5672/wikimedia-eventstreams"   ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-amqp:latest
```

## Environment variable matrix

### Kafka image (`ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams:latest`)

| Variable | Purpose |
|---|---|
| `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS` | Core configuration for this image variant. |
| `KAFKA_TOPIC` | Core configuration for this image variant. |
| `WIKIMEDIA_EVENTSTREAMS_USER_AGENT` | Core configuration for this image variant. |
| `WIKIMEDIA_EVENTSTREAMS_STATE_FILE` | Core configuration for this image variant. |
| `WIKIMEDIA_EVENTSTREAMS_DEDUPE_SIZE` | Core configuration for this image variant. |
| `WIKIMEDIA_EVENTSTREAMS_MAX_RETRY_DELAY` | Core configuration for this image variant. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `MQTT_BROKER_URL` | Core configuration for this image variant. |
| `MQTT_USERNAME` | Core configuration for this image variant. |
| `MQTT_PASSWORD` | Core configuration for this image variant. |
| `MQTT_CLIENT_ID` | Core configuration for this image variant. |
| `WIKIMEDIA_EVENTSTREAMS_URL` | Core configuration for this image variant. |
| `WIKIMEDIA_EVENTSTREAMS_USER_AGENT` | Core configuration for this image variant. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-wikimedia-eventstreams-amqp:latest`)

| Variable | Purpose |
|---|---|
| `AMQP_BROKER_URL` | Core configuration for this image variant. |
| `AMQP_ADDRESS` | Core configuration for this image variant. |
| `AMQP_AUTH_MODE` | Core configuration for this image variant. |
| `AMQP_CONTENT_MODE` | Core configuration for this image variant. |
| `WIKIMEDIA_EVENTSTREAMS_URL` | Core configuration for this image variant. |
| `WIKIMEDIA_EVENTSTREAMS_USER_AGENT` | Core configuration for this image variant. |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template-with-eventhub.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fwikimedia-eventstreams%2Fazure-template.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
