<!-- source-hero:begin -->
<table width="100%"><tr>
<td width="80" valign="middle" align="center">
<img src="https://flagcdn.com/64x48/un.png" alt="Global" width="64" height="48"><br>
<sub><b>Global</b></sub>
</td>
<td valign="middle">

# Ticketmaster

<sub>concerts, sports, theater, arts via Discovery API · Kafka · MQTT · AMQP · <a href="https://www.ticketmaster.com/">upstream</a> · <a href="https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/">API docs</a></sub>

<img align="middle" alt="Kafka" src="https://img.shields.io/badge/-Kafka-231f20?style=flat-square"> <img align="middle" alt="MQTT" src="https://img.shields.io/badge/-MQTT-660066?style=flat-square"> <img align="middle" alt="AMQP" src="https://img.shields.io/badge/-AMQP-1a4a78?style=flat-square">
&nbsp;
<img align="middle" src="https://img.shields.io/badge/Azure-6_templates-0078d4?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Fabric-ACI-117865?style=flat-square"> <img align="middle" src="https://img.shields.io/badge/Docker-3_images-2496ed?style=flat-square">
&nbsp;
<a href="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml"><img align="middle" alt="build" src="https://github.com/clemensv/real-time-sources/actions/workflows/build_containers.yml/badge.svg"></a>

> Global — concerts, sports, theater, arts via Discovery API

[🚀 **Deploy to Azure**](https://clemensv.github.io/real-time-sources#ticketmaster) &nbsp;·&nbsp;
[🐳 **docker pull**](CONTAINER.md) &nbsp;·&nbsp;
[📑 **Event schemas**](EVENTS.md) &nbsp;·&nbsp;
[↗ **Upstream**](https://www.ticketmaster.com/)

</td></tr></table>
<!-- source-hero:end -->

Related docs:

<!-- upstream-links:begin -->
## Upstream

- Home page: <https://www.ticketmaster.com/>
- API / data documentation: <https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/>

<!-- upstream-links:end -->

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

### Common (all images)

| Variable | Description |
|---|---|
| `LOG_LEVEL` | Standard Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default `INFO`. |
| `USER_AGENT` | HTTP `User-Agent` header sent on upstream requests. Operators should override the default with their own contact string. |
| `USER_AGENT_CONTACT` | Contact e-mail embedded in the `User-Agent` header for upstream operators. Override the default with your own address. |

### Source configuration

| Variable | Description |
|---|---|
| `SOURCE_MANIFEST` | Advanced: path to the xRegistry manifest the bridge loads at startup; defaults to the packaged copy under `/app/xreg/`. Normally only overridden in custom builds. |

### Kafka image (`ghcr.io/clemensv/real-time-sources-ticketmaster:latest`)

| Variable | Purpose |
|---|---|
| `TICKETMASTER_API_KEY` | **Required.** Ticketmaster Discovery API key used to authenticate upstream event and reference-data requests; obtain it from the Ticketmaster developer portal before deployment. |
| `CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS` | Event Hubs / Fabric connection string (shortcut), or Kafka bootstrap servers (`host:port`) when configuring the broker directly. |
| `KAFKA_TOPIC` | Kafka topic the feeder publishes to. |
| `COUNTRY_CODES` | Comma-separated ISO 3166 country codes to query for events (for example `US,CA,GB`). |
| `POLL_INTERVAL` | Seconds between poll cycles. |
| `REFERENCE_REFRESH` | Seconds between refreshes of reference data (catalog/metadata). |
| `STATE_FILE` | Path to the JSON dedupe/resume state file; mount persistent storage here for long-running deployments. |
| `KAFKA_ENABLE_TLS` | Set `false` to disable TLS for local/plaintext brokers (default `true`). |
| `TICKETMASTER_CITY` | Filter events by city name. |
| `TICKETMASTER_VENUE_ID` | Filter events by Ticketmaster venue ID. |
| `TICKETMASTER_ATTRACTION_ID` | Filter events by Ticketmaster attraction (performer/act) ID. |
| `TICKETMASTER_SEGMENT_ID` | Filter events by segment ID (top-level classification, for example Music or Sports). |
| `TICKETMASTER_GENRE_ID` | Filter events by genre ID within a segment. |
| `TICKETMASTER_SUB_GENRE_ID` | Filter events by sub-genre ID. |
| `TICKETMASTER_MARKET_ID` | Filter events by Ticketmaster market ID (metro area). |
| `TICKETMASTER_POSTAL_CODE` | Filter events by postal/ZIP code. |
| `TICKETMASTER_LOCALE` | Response locale (for example `en-us`). |
| `TICKETMASTER_SORT` | Result sort order (for example `date,asc`). |
| `TICKETMASTER_PAGE_SIZE` | Number of events to request per API page. |
| `TICKETMASTER_START_DATETIME` | Only include events on or after this ISO 8601 datetime. |
| `TICKETMASTER_END_DATETIME` | Only include events on or before this ISO 8601 datetime. |
| `TICKETMASTER_LOOKAHEAD_DAYS` | When no explicit end datetime is set, query this many days ahead. |
| `KAFKA_SASL_USERNAME` | SASL PLAIN username (alias of `SASL_USERNAME`). For Event Hubs use `$ConnectionString`. |
| `KAFKA_SASL_PASSWORD` | SASL PLAIN password (alias of `SASL_PASSWORD`). For Event Hubs use the connection string. |

### MQTT image (`ghcr.io/clemensv/real-time-sources-ticketmaster-mqtt:latest`)

| Variable | Purpose |
|---|---|
| `TICKETMASTER_API_KEY` | **Required.** Ticketmaster Discovery API key used to authenticate upstream event and reference-data requests; obtain it from the Ticketmaster developer portal before deployment. |
| `MQTT_BROKER_URL` | MQTT broker URL (`mqtt://` or `mqtts://host:port`). |
| `MQTT_USERNAME` | Username for MQTT `password` auth mode. |
| `MQTT_PASSWORD` | Password for MQTT `password` auth mode. |
| `MQTT_CLIENT_ID` | Stable MQTT client identifier; set a unique value per running instance. |
| `COUNTRY_CODES` | Comma-separated ISO 3166 country codes to query for events (for example `US,CA,GB`). |
| `MQTT_AUTH_MODE` | `password` (default) or `entra` for MQTT v5 enhanced authentication via Microsoft Entra ID (Azure Event Grid). |
| `MQTT_ENTRA_AUDIENCE` | JWT audience for `entra` auth mode (default `https://eventgrid.azure.net/`). |
| `MQTT_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |

### AMQP image (`ghcr.io/clemensv/real-time-sources-ticketmaster-amqp:latest`)

| Variable | Purpose |
|---|---|
| `TICKETMASTER_API_KEY` | **Required.** Ticketmaster Discovery API key used to authenticate upstream event and reference-data requests; obtain it from the Ticketmaster developer portal before deployment. |
| `AMQP_BROKER_URL` | AMQP 1.0 connection URL shortcut (host, port, TLS, credentials). |
| `AMQP_ADDRESS` | AMQP destination address (queue/topic/entity) to publish to. |
| `AMQP_AUTH_MODE` | AMQP authentication mode — `password` (SASL PLAIN), `entra` (Service Bus + Microsoft Entra CBS), or `sas` (SAS-token CBS). |
| `COUNTRY_CODES` | Comma-separated ISO 3166 country codes to query for events (for example `US,CA,GB`). |
| `AMQP_ENTRA_AUDIENCE` | Token audience for `entra` mode (default `https://servicebus.azure.net/.default`). |
| `AMQP_ENTRA_CLIENT_ID` | Optional user-assigned managed-identity client ID for `entra` mode; otherwise `DefaultAzureCredential` is used. |
| `AMQP_HOST` | AMQP broker host (component-level alternative to `AMQP_BROKER_URL`). |
| `AMQP_PASSWORD` | SASL PLAIN password, used when `AMQP_AUTH_MODE=password` (default). |
| `AMQP_PORT` | AMQP broker port (default `5672`, or `5671` with TLS). |
| `AMQP_SAS_KEY` | SAS key value (base64-encoded shared secret). Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_SAS_KEY_NAME` | SAS policy / key name (e.g. `RootManageSharedAccessKey`). Required when `AMQP_AUTH_MODE=sas`. |
| `AMQP_TLS` | Set `true` to use TLS (`amqps`) for the component-level connection. |
| `AMQP_USERNAME` | SASL PLAIN username, used when `AMQP_AUTH_MODE=password` (default). |

## Azure ARM deployments

Only templates that exist in this source folder are listed below.

- `azure-template-amqp.json` — AMQP deployment targeting an existing AMQP 1.0 broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fticketmaster%2Fazure-template-amqp.json)
- `azure-template-mqtt.json` — MQTT deployment targeting an existing MQTT broker
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fticketmaster%2Fazure-template-mqtt.json)
- `azure-template-with-eventgrid-mqtt.json` — MQTT deployment plus Azure Event Grid namespace broker provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fticketmaster%2Fazure-template-with-eventgrid-mqtt.json)
- `azure-template-with-eventhub.json` — Kafka deployment plus Azure Event Hubs provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fticketmaster%2Fazure-template-with-eventhub.json)
- `azure-template-with-servicebus.json` — AMQP deployment plus Azure Service Bus provisioning
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fticketmaster%2Fazure-template-with-servicebus.json)
- `azure-template.json` — Kafka deployment targeting an existing Kafka/Event Hubs endpoint
  [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fticketmaster%2Fazure-template.json)

## Related

- [README.md](README.md)
- [EVENTS.md](EVENTS.md)
- `xreg/`
