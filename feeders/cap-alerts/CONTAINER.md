# CAP Alerts container images (Kafka, MQTT, AMQP)

[README](README.md) · [EVENTS](EVENTS.md) · [CONTAINER](CONTAINER.md)

The `cap-alerts` images poll configured public Common Alerting Protocol feeds and publish CloudEvents for alert telemetry plus zone reference data. Emergency operations teams, broadcast alerting systems, insurers, and situational-awareness dashboards can subscribe once and normalize public warnings from agencies that already publish CAP 1.2.

## Image contract

| Tag | Transport | Dockerfile | State share |
|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-cap-alerts:latest` | Kafka | `Dockerfile` / `Dockerfile.kafka` | `STATE_FILE` |
| `ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest` | MQTT 5 | `Dockerfile.mqtt` | `STATE_FILE` |
| `ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | `STATE_FILE` |

## Common environment

| Variable | Default | Description |
|---|---|---|
| `CAP_SOURCES` | built-in NWS + MeteoAlarm Belgium | JSON array of CAP source configs `{cap_source_id,url,format,zone_url}`. |
| `CAP_ALERTS_MOCK` | `false` | Use deterministic fixture and exit once for tests. |
| `POLL_INTERVAL` | `300` | Seconds between alert polling cycles. |
| `REFERENCE_REFRESH_INTERVAL` | `21600` | Seconds between zone-reference refreshes. |
| `STATE_FILE` | per-image home file | JSON dedupe state keyed by `cap_source_id/identifier`. |
| `ONCE_MODE` | `false` | Run one cycle and exit; used by Fabric notebook and E2E. |
| `LOG_LEVEL` | `INFO` | Python logging level. |

## Kafka

```powershell
docker run --rm -e CONNECTION_STRING="BootstrapServer=host:9092;EntityPath=cap-alerts" -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-cap-alerts:latest
```

Kafka variables: `CONNECTION_STRING`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `SASL_USERNAME`, `SASL_PASSWORD`, `KAFKA_ENABLE_TLS`.

| Variable | Default | Description |
|---|---|---|
| `CONNECTION_STRING` | required for published image | Kafka/Event Hubs connection string, including `BootstrapServer=host:port;EntityPath=topic` for local Kafka. |
| `KAFKA_BOOTSTRAP_SERVERS` | none | Plain Kafka bootstrap server list when not using `CONNECTION_STRING`. |
| `KAFKA_TOPIC` | `cap-alerts` | Kafka topic for both `CapZone` and `CapAlert` CloudEvents. |
| `KAFKA_ENABLE_TLS` | `true` | Set `false` for local plaintext Kafka. |
| `SASL_USERNAME` / `SASL_PASSWORD` | none | Optional Kafka SASL credentials. |

## MQTT

```powershell
docker run --rm -e MQTT_BROKER_URL="broker:1883" -e MQTT_AUTH_MODE=anonymous ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest
```

MQTT variables: `MQTT_BROKER_URL`, `MQTT_AUTH_MODE`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_ENABLE_TLS`, `MQTT_CA_FILE`, `MQTT_CLIENT_ID`.

| Variable | Default | Description |
|---|---|---|
| `MQTT_BROKER_URL` | `localhost:1883` | MQTT broker host[:port] or `mqtt://`/`mqtts://` URL. |
| `MQTT_AUTH_MODE` | `anonymous` | `anonymous` or `userpass` for generic MQTT brokers. |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | none | MQTT user/password credentials when `MQTT_AUTH_MODE=userpass`. |
| `MQTT_ENABLE_TLS` | `false` | Enable TLS for MQTT broker connections. |
| `MQTT_CA_FILE` | none | Optional CA bundle path. |
| `MQTT_CLIENT_ID` | generated | Optional MQTT client-id prefix. |

## AMQP 1.0

```powershell
docker run --rm -e AMQP_BROKER_URL="amqp://user:pass@broker:5672/cap-alerts" ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest
```

AMQP variables: `AMQP_BROKER_URL`, `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, `AMQP_TLS`, `AMQP_CONTENT_MODE`.

| Variable | Default | Description |
|---|---|---|
| `AMQP_BROKER_URL` | `localhost:5672` | Generic AMQP broker URL; may include user/password. |
| `AMQP_HOST` / `AMQP_PORT` | parsed from URL | Explicit AMQP host and port overrides. |
| `AMQP_ADDRESS` | `cap-alerts` | AMQP target address/queue/topic. |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | parsed from URL | SASL PLAIN credentials for generic brokers. |
| `AMQP_TLS` | `false` | Enable TLS and default port 5671. |
| `AMQP_CONTENT_MODE` | `binary` | CloudEvents AMQP content mode. |

## Deploy to Azure

Templates are generated from the repository catalog: Kafka BYO/Event Hubs, MQTT BYO/Event Grid namespace, and AMQP Service Bus variants.

- `azure-template.json` — bring your own Kafka/Event Hubs connection string.
- `azure-template-with-eventhub.json` — provision Event Hubs and run the Kafka image.
- `azure-template-mqtt.json` — bring your own MQTT 5 broker.
- `azure-template-with-eventgrid-mqtt.json` — provision Event Grid MQTT broker and run the MQTT image.
- `azure-template-with-servicebus.json` — provision Service Bus and run the AMQP image.
