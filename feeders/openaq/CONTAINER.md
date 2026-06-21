# OpenAQ containers (Kafka, MQTT, AMQP)

[📘 README](README.md) · [📑 Events](EVENTS.md) · [↗ OpenAQ API docs](https://docs.openaq.org/)

OpenAQ CloudEvents support public-health alerting, epidemiological exposure analysis, smart-city air-quality maps, and compliance dashboards. The containers poll configurable OpenAQ API v3 location selections and emit reference data (`Location`, `Sensor`) before telemetry (`Measurement`).

## Image contract

| Image tag | Transport | Dockerfile | State share |
|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-openaq:latest` | Kafka/Event Hubs | `Dockerfile` / `Dockerfile.kafka` | Optional `STATE_FILE` for dedupe |
| `ghcr.io/clemensv/real-time-sources-openaq-mqtt:latest` | MQTT 5 | `Dockerfile.mqtt` | Optional `STATE_FILE` for dedupe |
| `ghcr.io/clemensv/real-time-sources-openaq-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | Optional `STATE_FILE` for dedupe |

## Common OpenAQ environment

| Variable | Required | Default | Description |
|---|---:|---|---|
| `OPENAQ_API_KEY` | live only | — | OpenAQ API key sent as `X-API-Key`. Not required with `OPENAQ_MOCK=true`. |
| `OPENAQ_COUNTRIES` | no | `US` | Comma-separated ISO alpha-2 country filters. |
| `OPENAQ_LOCATIONS` | no | — | Comma-separated OpenAQ location ids; overrides country paging. |
| `OPENAQ_BBOX` | no | — | WGS84 bbox `minLon,minLat,maxLon,maxLat`. |
| `OPENAQ_PAGE_LIMIT` | no | `25` | Locations per API page. |
| `OPENAQ_MAX_PAGES` | no | `1` | Max pages per country/bbox per reference refresh. |

> **Rate-limit sizing:** OpenAQ documents free-tier limits of 60 requests/minute and 2,000 requests/hour. Defaults (`OPENAQ_PAGE_LIMIT=25`, `OPENAQ_MAX_PAGES=1`, `POLL_INTERVAL=900`) are about 104 requests/hour; increase `POLL_INTERVAL` or pin `OPENAQ_LOCATIONS` before scaling toward hundreds of locations.
| `POLL_INTERVAL` | no | `900` | Seconds between latest-measurement polls. |
| `REFERENCE_REFRESH_INTERVAL` | no | `21600` | Seconds between Location/Sensor catalog refreshes. |
| `STATE_FILE` | no | user home | JSON dedupe file. |
| `OPENAQ_MOCK` | no | `false` | Emit deterministic synthetic events and exit once. |
| `LOG_LEVEL` | no | `INFO` | Python logging level. |

## Kafka / Event Hubs

| Variable | Required | Default | Description |
|---|---:|---|---|
| `CONNECTION_STRING` | yes* | — | `BootstrapServer=host:port;EntityPath=topic` or Event Hubs-compatible connection string. |
| `KAFKA_BOOTSTRAP_SERVERS` | yes* | — | Explicit bootstrap servers when not using `CONNECTION_STRING`. |
| `KAFKA_TOPIC` | no | `openaq` | Topic name when not supplied by `EntityPath`. |
| `KAFKA_ENABLE_TLS` | no | `true` | Set `false` for local plaintext Kafka. |
| `SASL_USERNAME`, `SASL_PASSWORD` | no | — | SASL PLAIN credentials. |

```powershell
docker pull ghcr.io/clemensv/real-time-sources-openaq:latest
docker run --rm -e CONNECTION_STRING -e KAFKA_ENABLE_TLS=false -e OPENAQ_MOCK=true ghcr.io/clemensv/real-time-sources-openaq:latest
```

## MQTT 5

| Variable | Required | Default | Description |
|---|---:|---|---|
| `MQTT_BROKER_URL` | yes | — | Broker `host:port` or URI. |
| `MQTT_ENABLE_TLS` | no | `false` | Enable TLS. |
| `MQTT_AUTH_MODE` | no | `anonymous` | `anonymous`, `userpass`, `tls-cert`, or `entra`. |
| `MQTT_USERNAME`, `MQTT_PASSWORD` | conditional | — | Username/password auth or Event Grid client name. |
| `MQTT_CLIENT_CERT`, `MQTT_CLIENT_KEY`, `MQTT_CA_FILE` | conditional | — | TLS client certificate auth. |
| `MQTT_ENTRA_CLIENT_ID`, `MQTT_ENTRA_AUDIENCE` | conditional | `https://eventgrid.azure.net/` | Event Grid namespace MQTT Entra auth. |

```powershell
docker pull ghcr.io/clemensv/real-time-sources-openaq-mqtt:latest
docker run --rm -e MQTT_BROKER_URL=host.docker.internal:1883 -e OPENAQ_MOCK=true ghcr.io/clemensv/real-time-sources-openaq-mqtt:latest
```

## AMQP 1.0

| Variable | Required | Default | Description |
|---|---:|---|---|
| `AMQP_BROKER_URL` | yes* | — | `amqp://user:pass@host:5672/openaq` convenience URI. |
| `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS` | yes* | `openaq` address | Explicit broker settings. |
| `AMQP_AUTH_MODE` | no | `password` | `password`, `entra`, or `sas`. |
| `AMQP_USERNAME`, `AMQP_PASSWORD` | conditional | — | SASL PLAIN credentials. |
| `AMQP_ENTRA_CLIENT_ID`, `AMQP_ENTRA_AUDIENCE` | conditional | Service Bus scope | Azure managed identity auth. |
| `AMQP_SAS_KEY_NAME`, `AMQP_SAS_KEY` | conditional | — | SAS CBS auth / Service Bus emulator. |
| `AMQP_TLS` | no | `false` | Use TLS / AMQPS. |

```powershell
docker pull ghcr.io/clemensv/real-time-sources-openaq-amqp:latest
docker run --rm -e AMQP_BROKER_URL=amqp://artemis:artemis@host.docker.internal:5672/openaq -e OPENAQ_MOCK=true ghcr.io/clemensv/real-time-sources-openaq-amqp:latest
```
