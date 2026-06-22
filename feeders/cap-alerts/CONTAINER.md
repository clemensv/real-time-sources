# CAP Alerts Kafka, MQTT, and AMQP containers

[Overview](README.md) · [Events](EVENTS.md) · [Source contract](xreg/cap-alerts.xreg.json)

The `cap-alerts` images poll configured Common Alerting Protocol feeds and publish CloudEvents for alert telemetry plus zone reference data. Emergency operations teams, broadcast alerting systems, insurers, and situational-awareness dashboards can subscribe once and normalize public warnings from agencies that already publish CAP 1.2 or CAP-equivalent JSON.

## Image contract

| Image | Dockerfile | Transport | State share |
| --- | --- | --- | --- |
| `ghcr.io/clemensv/real-time-sources-cap-alerts:latest` | `Dockerfile` / `Dockerfile.kafka` | Kafka/Event Hubs | `STATE_FILE` JSON dedupe state. |
| `ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest` | `Dockerfile.mqtt` | MQTT 5 | `STATE_FILE` JSON dedupe state. |
| `ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest` | `Dockerfile.amqp` | AMQP 1.0 | `STATE_FILE` JSON dedupe state. |

## Common environment

| Variable | Description | Default |
| --- | --- | --- |
| `CAP_SOURCES_FILE` | Path to a catalog JSON file mounted into the container. | packaged catalog |
| `CAP_SELECT` | Comma-separated catalog `name` selector, `*` for all entries, or unset for `enabled: true` only. | unset |
| `CAP_SOURCES` | Legacy inline JSON source list, `@file`, or path. Takes precedence over `CAP_SOURCES_FILE`; not used as selector because it already held inline JSON. | unset |
| `CAP_ALERTS_MOCK` | Use deterministic fixture and exit once for tests. | `false` |
| `POLL_INTERVAL` | Seconds between alert polling cycles. | `300` |
| `REFERENCE_REFRESH_INTERVAL` | Seconds between zone-reference refreshes. | `21600` |
| `STATE_FILE` | JSON dedupe state keyed by `cap_source_id/identifier`. | per-image home file |
| `ONCE_MODE` | Run one cycle and exit. | `false` |
| `LOG_LEVEL` | Python logging level. | `INFO` |

## Configuring sources

### Catalog format

`CAP_SOURCES_FILE` points at a JSON object with a `sources` array. Each entry may contain:

| Field | Required | Description |
| --- | --- | --- |
| `name` | catalog only | Stable selector name for `CAP_SELECT`. |
| `enabled` | catalog only | Runs by default when `true`; disabled entries are templates or opt-in sources. |
| `description` | catalog only | Human-readable source description. |
| `cap_source_id` | yes | Stable source identifier used in subjects and keys. |
| `url` | yes | CAP XML, Atom/CAP, CAP directory, or supported provider JSON endpoint. |
| `format` | no | `nws-json`, `atom-cap`, `cap-xml`, `cap-directory`, or `dwd-directory`; default `cap-xml`. |
| `zone_url` | no | Optional zone/reference endpoint. |
| `auth_env` | no | Environment-variable name whose value is sent as `Authorization`. |
| `auth_header` | no | Authorization header value, with `${ENV_VAR}` expansion at load time. |

### Selecting sources

- Unset `CAP_SELECT`: run only entries where `enabled` is `true`.
- `CAP_SELECT="nws-us-active-alerts,meteoalarm-belgium"`: run named entries in that order.
- `CAP_SELECT="*"`: run all catalog entries, including disabled templates.

Unknown names fail fast with a `ValueError` that includes known names.

### Bring your own catalog

```powershell
docker run --rm `
  -v ${PWD}\cap-sources.json:/config/cap-sources.json:ro `
  -e CAP_SOURCES_FILE="/config/cap-sources.json" `
  -e CAP_SELECT="nws-us-active-alerts" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=cap-alerts" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-cap-alerts:latest
```

For secrets, keep values out of the file and use placeholders such as `"auth_header": "Bearer ${CAP_FEED_TOKEN}"`; the loader expands them from the runtime environment.

### Known CAP sources

| Source | URL | Feeder status |
| --- | --- | --- |
| US National Weather Service / NOAA active alerts | `https://api.weather.gov/alerts/active` | Shipped enabled as `nws-us-active-alerts`. |
| MeteoAlarm Belgium Atom/CAP | `https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-belgium` | Shipped enabled as `meteoalarm-belgium`. |
| MeteoAlarm national feeds — Ireland, France, Spain, Germany, Austria, Italy, Netherlands, Portugal, Switzerland, Poland | `https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-{country}` | Shipped disabled as `meteoalarm-{country}`; aggregate the national met services. Add the name to `CAP_SELECT` to enable. |
| DWD CAP warning directory | `https://opendata.dwd.de/weather/alerts/cap/COMMUNEUNION_DWD_STAT/` | Custom-catalog candidate; bespoke `dwd` feeder also exists. |
| GDACS CAP/RSS disaster alerts | `https://www.gdacs.org/xml/gdacs_cap.xml` | Custom-catalog candidate after RSS/CAP parsing validation. |
| Environment and Climate Change Canada CAP datamart | `https://dd.weather.gc.ca/alerts/cap/` | Custom-catalog candidate; verify current regional file shape before enabling. |
| Australian Bureau of Meteorology public warnings | `http://www.bom.gov.au/fwo/IDZ00059.warnings_national.xml` | Custom-catalog candidate where network access permits; verify BOM terms and format before enabling. |

## Kafka / Event Hubs

```powershell
docker pull ghcr.io/clemensv/real-time-sources-cap-alerts:latest
docker run --rm -e CONNECTION_STRING="BootstrapServer=host:9092;EntityPath=cap-alerts" -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-cap-alerts:latest
```

| Variable | Description | Default |
| --- | --- | --- |
| `CONNECTION_STRING` | Kafka/Event Hubs connection string, including `BootstrapServer=host:port;EntityPath=topic` for local Kafka. | unset |
| `KAFKA_BOOTSTRAP_SERVERS` | Plain Kafka bootstrap server list when not using `CONNECTION_STRING`. | unset |
| `KAFKA_TOPIC` | Kafka topic for `CapZone` and `CapAlert` CloudEvents. | `cap-alerts` |
| `KAFKA_ENABLE_TLS` | Set `false` for local plaintext Kafka. | `true` |
| `SASL_USERNAME` / `SASL_PASSWORD` | Optional Kafka SASL credentials. | unset |

## MQTT 5

```powershell
docker pull ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest
docker run --rm -e MQTT_BROKER_URL="broker:1883" -e MQTT_AUTH_MODE=anonymous ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest
```

| Variable | Description | Default |
| --- | --- | --- |
| `MQTT_BROKER_URL` | MQTT broker host[:port] or `mqtt://`/`mqtts://` URL. | `localhost:1883` |
| `MQTT_AUTH_MODE` | `anonymous` or `userpass` for generic MQTT brokers. | `anonymous` |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | MQTT user/password credentials when `MQTT_AUTH_MODE=userpass`. | unset |
| `MQTT_ENABLE_TLS` | Enable TLS for MQTT broker connections. | `false` |
| `MQTT_CA_FILE` | Optional CA bundle path. | unset |
| `MQTT_CLIENT_ID` | Optional MQTT client-id prefix. | generated |

## AMQP 1.0

```powershell
docker pull ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest
docker run --rm -e AMQP_BROKER_URL="amqp://user:pass@broker:5672/cap-alerts" ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest
```

| Variable | Description | Default |
| --- | --- | --- |
| `AMQP_BROKER_URL` | Generic AMQP broker URL; may include user/password. | `localhost:5672` |
| `AMQP_HOST` / `AMQP_PORT` | Explicit AMQP host and port overrides. | parsed from URL |
| `AMQP_ADDRESS` | AMQP target address/queue/topic. | `cap-alerts` |
| `AMQP_USERNAME` / `AMQP_PASSWORD` | SASL PLAIN credentials for generic brokers. | parsed from URL |
| `AMQP_TLS` | Enable TLS and default port 5671. | `false` |
| `AMQP_CONTENT_MODE` | CloudEvents AMQP content mode. | `binary` |

## Azure deployment templates

[![Deploy Kafka BYO connection](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template.json)
[![Deploy Event Hubs](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template-with-eventhub.json)
[![Deploy MQTT BYO broker](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template-mqtt.json)
[![Deploy Event Grid MQTT](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template-with-eventgrid-mqtt.json)
[![Deploy Service Bus AMQP](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template-with-servicebus.json)

See [EVENTS.md](EVENTS.md) for event types, subjects, and transport bindings.
