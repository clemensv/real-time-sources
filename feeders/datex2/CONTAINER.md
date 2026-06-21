# DATEX II Kafka, MQTT, and AMQP containers

DATEX II containers turn European road-traffic XML publications into CloudEvents for operational traffic dashboards, traveler-information services, safety analytics, and event-driven digital twins.

## Image contract

| Image | Dockerfile | Transport | State share |
| --- | --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-datex2:latest` | `Dockerfile` | Kafka/Event Hubs | Optional `DATEX2_STATE_FILE` / `STATE_FILE`. |
| `ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5 | Stateless per run; broker retained state stores LKV. |
| `ghcr.io/clemensv/real-time-sources-datex2-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 | Stateless per run. |

## Common environment

| Variable | Description | Default |
| --- | --- | --- |
| `DATEX2_ENDPOINTS` | JSON list of endpoint registry entries: `id`, `url`, `publication`, optional `country`, `operator`, `auth_header`. | NDW sample endpoints |
| `DATEX2_MOCK` | Emit deterministic sample DATEX II events for tests. | `false` |
| `MAX_RECORDS_PER_FAMILY` | Caps records per event family during one cycle. | `25` |
| `POLLING_INTERVAL` | Seconds between polling cycles for Kafka container. | `300` |
| `LOG_LEVEL` | Python logging level. | `INFO` |
| `DATEX2_STATE_FILE` | Optional DATEX II-specific persistent dedupe state file path for Kafka/Event Hubs deployments. | unset |
| `STATE_FILE` | Optional generic persistent dedupe state file path for Kafka/Event Hubs deployments. | unset |
| `ONCE_MODE` | Run one polling cycle and exit. | `false` |

## Kafka

Set `CONNECTION_STRING=BootstrapServer=broker:9092;EntityPath=topic` and `KAFKA_ENABLE_TLS=false` for local Kafka, or pass an Event Hubs-compatible connection string.

Additional variables: `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `KAFKA_ENABLE_TLS`, `SASL_USERNAME`, `SASL_PASSWORD`, `SASL_MECHANISM`, `CLIENT_ID`, `GROUP_ID`.

```powershell
docker pull ghcr.io/clemensv/real-time-sources-datex2:latest
docker run --rm -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=datex2" -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-datex2:latest
```

## MQTT 5

Set `MQTT_BROKER_URL`, `MQTT_AUTH_MODE`, and optional username/password or TLS settings.

Additional variables: `MQTT_ENABLE_TLS`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CA_FILE`, `MQTT_CLIENT_ID`, `MQTT_AUTH_MODE`, `MQTT_TOKEN_SCOPE`, `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`.

```powershell
docker pull ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest
docker run --rm -e MQTT_BROKER_URL="broker:1883" -e MQTT_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest
```

## AMQP 1.0

Set `AMQP_HOST`, `AMQP_ADDRESS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, and `AMQP_TLS`. The AMQP producer uses binary CloudEvents content mode.

Additional variables: `AMQP_BROKER_URL`, `AMQP_PORT`, `AMQP_AUTH_MODE`, `AMQP_SAS_KEY_NAME`, `AMQP_SAS_KEY`, `AMQP_SAS_TOKEN_TTL_SECONDS`, `AMQP_ENTRA_AUDIENCE`, `AMQP_ENTRA_CLIENT_ID`, `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`.

```powershell
docker pull ghcr.io/clemensv/real-time-sources-datex2-amqp:latest
docker run --rm -e AMQP_HOST="broker" -e AMQP_ADDRESS="datex2" -e AMQP_USERNAME="user" -e AMQP_PASSWORD="secret" ghcr.io/clemensv/real-time-sources-datex2-amqp:latest
```

## Azure deployment templates

[![Deploy Kafka BYO connection](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template.json)
[![Deploy Event Hubs](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-eventhub.json)
[![Deploy MQTT BYO broker](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-mqtt.json)
[![Deploy Event Grid MQTT](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-eventgrid-mqtt.json)
[![Deploy Service Bus AMQP](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-servicebus.json)

See [EVENTS.md](EVENTS.md) for event types, subjects, and transport bindings.
