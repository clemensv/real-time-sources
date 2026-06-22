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
| `OPENAQ_SOURCES_FILE` | no | packaged catalog | Path to an OpenAQ query-slice catalog JSON file. See [README.md#configuring-sources](README.md#configuring-sources). |
| `OPENAQ_SOURCES` | no | enabled entries | Comma-separated catalog entry `name`s, or `*` for all entries including disabled examples. Unset runs entries with `enabled: true`. |
| `OPENAQ_COUNTRIES` | no | unset | Legacy single-query override: comma-separated ISO alpha-2 country filters. Takes precedence over the catalog when set. |
| `OPENAQ_LOCATIONS` | no | — | Legacy single-query override: comma-separated OpenAQ location ids; overrides country paging. Takes precedence over the catalog when set. |
| `OPENAQ_BBOX` | no | — | Legacy single-query override: WGS84 bbox `minLon,minLat,maxLon,maxLat`. Takes precedence over the catalog when set. |
| `OPENAQ_PAGE_LIMIT` | no | `25` | Locations per API page for legacy queries and catalog slices that omit `page_limit`. |
| `OPENAQ_MAX_PAGES` | no | `1` | Max pages per country/bbox per reference refresh for legacy queries and catalog slices that omit `max_pages`. |
| `POLL_INTERVAL` | no | `900` | Seconds between latest-measurement polls. |
| `REFERENCE_REFRESH_INTERVAL` | no | `21600` | Seconds between Location/Sensor catalog refreshes. |
| `STATE_FILE` | no | user home | JSON dedupe file. |
| `OPENAQ_MOCK` | no | `false` | Emit deterministic synthetic events and exit once. |
| `LOG_LEVEL` | no | `INFO` | Python logging level. |
| `ONCE_MODE` | `true` runs a single polling cycle and exits. Required for Fabric notebook hosting and useful for smoke tests. |  |  |

> **Rate-limit sizing:** OpenAQ documents free-tier limits of 60 requests/minute and 2,000 requests/hour. Defaults (`OPENAQ_PAGE_LIMIT=25`, `OPENAQ_MAX_PAGES=1`, `POLL_INTERVAL=900`) are about 104 requests/hour; increase `POLL_INTERVAL` or pin `OPENAQ_LOCATIONS` before scaling toward hundreds of locations.

## Configuring sources

The default image includes `openaq_core/sources/openaq-sources.json`. Each entry is a named query slice against the single global OpenAQ API v3 base `https://api.openaq.org/v3`, not a separate server. The enabled `us-all` slice uses `countries=US` and preserves the previous default behavior; set `OPENAQ_SOURCES` to select names from that catalog, or mount your own JSON file and set `OPENAQ_SOURCES_FILE`.

Catalog entries support `name`, `enabled`, `description`, optional `countries`, optional `locations`, optional `bbox`, optional `page_limit`, and optional `max_pages`. The shared API key stays in `OPENAQ_API_KEY` and is sent as `X-API-Key`; register at `https://explore.openaq.org/register`. String fields can use `${ENV_VAR}` placeholders, but do not store API keys in the catalog. The full catalog format, selection rules, and known query-slice table live in [README.md#configuring-sources](README.md#configuring-sources).

Example with a mounted catalog:

```powershell
docker run --rm `
  -v ${PWD}\my-openaq.sources.json:/app/openaq-sources.json:ro `
  -e OPENAQ_SOURCES_FILE="/app/openaq-sources.json" `
  -e OPENAQ_SOURCES="india,us-all" `
  -e OPENAQ_API_KEY="<secret>" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=openaq" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-openaq:latest
```

Quick legacy override without a catalog (`OPENAQ_COUNTRIES` still defaults to `US` in this path when only `OPENAQ_BBOX` is supplied):

```powershell
docker run --rm `
  -e OPENAQ_COUNTRIES="BE,NL" `
  -e OPENAQ_API_KEY="<secret>" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=openaq" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-openaq:latest
```

### Catalog format

```json
{
  "sources": [
    {
      "name": "us-all",
      "enabled": true,
      "description": "United States OpenAQ locations.",
      "countries": "US"
    }
  ]
}
```

| Field | Required | Description |
| --- | ---: | --- |
| `name` | yes | Stable selector used by `OPENAQ_SOURCES`. |
| `enabled` | no | Defaults to `true`; disabled examples are skipped unless selected or `OPENAQ_SOURCES=*`. |
| `description` | yes | Human-readable geography and filter intent. |
| `countries` | no | ISO alpha-2 country code or comma/list of codes for `/v3/locations`. |
| `locations` | no | OpenAQ location id or comma/list of ids. |
| `bbox` | no | WGS84 bbox `minLon,minLat,maxLon,maxLat`. |
| `page_limit`, `max_pages` | no | Per-slice paging overrides. |

### Selecting query slices

- Unset `OPENAQ_SOURCES` runs entries with `enabled: true`.
- `OPENAQ_SOURCES=india,us-all` runs only those named slices, in that order.
- `OPENAQ_SOURCES=*` loads every entry, including disabled examples.
- Unknown names fail fast with a `ValueError` listing known names.

### API key

Register at `https://explore.openaq.org/register`, set `OPENAQ_API_KEY`, and all selected slices share that one key. The key is not part of the catalog.

### Known query slices

| Catalog name | Enabled | Query shape | Notes |
| --- | ---: | --- | --- |
| `us-all` | yes | `countries=US` | Default slice preserving legacy behavior. |
| `eu-west` | no | `bbox=-10.50,41.00,15.50,56.50` | Western Europe bounding-box example. |
| `india` | no | `countries=IN` | Single-country example. |
| `california-bay-area` | no | `bbox=-123.10,36.80,-121.50,38.40` | Regional example with paging overrides. |
| `africa` | no | `bbox=-20.00,-35.00,52.00,38.00` | Pan-African bounding box; coverage depends on current OpenAQ station availability. |
| `bahrain` | no | `countries=BH` | Bahrain country slice; coverage conditional on station availability. |
| `kuwait` | no | `countries=KW` | Kuwait country slice; coverage conditional on station availability. |
| `oman` | no | `countries=OM` | Oman country slice; coverage conditional on station availability. |

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
| `MQTT_CLIENT_ID` | MQTT client identifier. |  |  |
| `MQTT_HOST` | MQTT broker host (component-level alternative to `MQTT_BROKER_URL`). |  |  |
| `MQTT_PORT` | MQTT broker port (component-level alternative to `MQTT_BROKER_URL`). |  |  |

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
| `AMQP_CONTENT_MODE` | `binary` (default) or `structured` CloudEvents content mode. |  |  |

```powershell
docker pull ghcr.io/clemensv/real-time-sources-openaq-amqp:latest
docker run --rm -e AMQP_BROKER_URL=amqp://artemis:artemis@host.docker.internal:5672/openaq -e OPENAQ_MOCK=true ghcr.io/clemensv/real-time-sources-openaq-amqp:latest
```
