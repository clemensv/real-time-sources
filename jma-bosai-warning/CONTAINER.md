# JMA Bosai Warning Container

The Kafka container polls Japan Meteorological Agency public Bosai weather warning and tsunami alert JSON feeds and publishes structured CloudEvents to Kafka-compatible endpoints. `Dockerfile.mqtt` builds the MQTT/UNS weather-warning feeder.

## Environment

Required: one of `CONNECTION_STRING` or `KAFKA_BOOTSTRAP_SERVERS`.

Optional:

- `KAFKA_TOPIC_WARNING` (default `jma-bosai-warning`)
- `KAFKA_TOPIC_TSUNAMI` (default `jma-bosai-tsunami`)
- `POLLING_INTERVAL_WARNING` (default `60` seconds)
- `POLLING_INTERVAL_TSUNAMI` (default `30` seconds)
- `OFFICE_METADATA_REFRESH_HOURS` (default `720`)
- `STATE_FILE` (default `.\state\jma-bosai-warning.json`)
- `KAFKA_ENABLE_TLS` (set `false` for plain Kafka)

## Run

Kafka:

```powershell
docker build -t jma-bosai-warning ./jma-bosai-warning
docker run --rm -e CONNECTION_STRING="BootstrapServer=host.docker.internal:9092;EntityPath=jma-bosai-warning" -e KAFKA_ENABLE_TLS=false jma-bosai-warning
```

MQTT/UNS:

```powershell
docker build -f ./jma-bosai-warning/Dockerfile.mqtt -t jma-bosai-warning-mqtt ./jma-bosai-warning
docker run --rm -e MQTT_BROKER_URL="mqtt://host.docker.internal:1883" jma-bosai-warning-mqtt
```

The MQTT feeder publishes retained office references to `alerts/jp/jma/jma-bosai-warning/{prefecture}/REFERENCE/{office_code}/{area_code}/office` and non-retained warning records to `alerts/jp/jma/jma-bosai-warning/{prefecture}/{severity}/{office_code}/{area_code}/warning`.

For Azure Event Hubs or Fabric Event Streams, pass the full connection string in `CONNECTION_STRING`. Events are CloudEvents; see `EVENTS.md` for schemas and keys.

## AMQP 1.0 container

The AMQP companion image publishes the same `Jma Bosai Warning` CloudEvents to a generic AMQP 1.0 broker, Azure Service Bus with Entra ID CBS, or a SAS-token Service Bus-compatible endpoint.

```bash
docker pull ghcr.io/clemensv/real-time-sources-jma-bosai-warning-amqp:latest
```

### Generic AMQP broker (SASL PLAIN)

```bash
docker run --rm   -e AMQP_BROKER_URL=amqp://broker:5672   -e AMQP_USERNAME=admin   -e AMQP_PASSWORD=admin   -e AMQP_ADDRESS=jma-bosai-warning   ghcr.io/clemensv/real-time-sources-jma-bosai-warning-amqp:latest
```

### Azure Service Bus (Entra ID)

```bash
docker run --rm   -e AMQP_HOST=<namespace>.servicebus.windows.net   -e AMQP_PORT=5671   -e AMQP_TLS=true   -e AMQP_ADDRESS=jma-bosai-warning   -e AMQP_AUTH_MODE=entra   -e AMQP_ENTRA_AUDIENCE=https://servicebus.azure.net/.default   ghcr.io/clemensv/real-time-sources-jma-bosai-warning-amqp:latest
```

### Service Bus emulator / SAS CBS

```bash
docker run --rm   -e AMQP_HOST=servicebus-emulator   -e AMQP_PORT=5672   -e AMQP_ADDRESS=jma-bosai-warning   -e AMQP_AUTH_MODE=sas   -e AMQP_SAS_KEY_NAME=RootManageSharedAccessKey   -e AMQP_SAS_KEY=<base64-key>   ghcr.io/clemensv/real-time-sources-jma-bosai-warning-amqp:latest
```

| Variable | Description | Default |
|---|---|---|
| `AMQP_BROKER_URL` | Optional AMQP URI for generic brokers. | unset |
| `AMQP_HOST` / `AMQP_PORT` | Broker host and port when no URI is supplied. | `localhost` / `5672` |
| `AMQP_ADDRESS` | Queue/topic/address to publish to. | `jma-bosai-warning` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for `AMQP_AUTH_MODE=password`. | unset |
| `AMQP_TLS` | Use TLS (`true`, `1`, or `yes`). | `false` |
| `AMQP_AUTH_MODE` | `password`, `entra`, or `sas`. | `password` |
| `AMQP_ENTRA_AUDIENCE` / `AMQP_ENTRA_CLIENT_ID` | Entra token scope and optional managed identity client ID. | Service Bus scope / unset |
| `AMQP_SAS_KEY_NAME` / `AMQP_SAS_KEY` | SAS CBS credentials. | unset |
| `AMQP_CONTENT_MODE` | CloudEvents content mode: `binary` or `structured`. | `binary` |

[![Deploy AMQP to Azure Service Bus](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Fjma-bosai-warning%2Fazure-template-amqp.json)

