# OpenAQ generalized air-quality feeder

[📑 Events](EVENTS.md) · [🐳 Container](CONTAINER.md) · [↗ OpenAQ API docs](https://docs.openaq.org/)

OpenAQ aggregates air-quality observations from government, research, and community monitoring networks worldwide. Public-health teams, epidemiologists, smart-city operators, regulatory analysts, and climate dashboards use these feeds to trigger smoke/pollution alerts, compare neighborhoods, audit compliance, and correlate exposure with health outcomes. This generalized feeder turns OpenAQ API v3 locations, sensors, and latest measurements into CloudEvents so one configurable bridge can serve many country, city, provider, and bounding-box slices instead of one bespoke feeder per jurisdiction.

## Upstream audit summary

OpenAQ API v3 base URL is `https://api.openaq.org/v3`; most endpoints require an API key in the `X-API-Key` header. The checked `c:\rts-creds\test-creds.json` did not contain a usable OpenAQ key during implementation, so live payload probing returned HTTP 401 and the contract is grounded in the published OpenAPI document at `https://api.openaq.org/openapi.json`.

| API family | Endpoint(s) | Keep/drop | Reason |
|---|---|---|---|
| Locations | `/v3/locations`, `/v3/locations/{id}` | Keep as `Location` | Reference catalog for monitoring sites; stable `location_id`. |
| Sensors | `/v3/locations/{id}/sensors`, `/v3/sensors/{id}` | Keep as `Sensor` | Reference catalog for parameter-specific streams; stable `sensor_id`. |
| Latest measurements | `/v3/locations/{id}/latest` | Keep as `Measurement` | Near-real-time latest value per sensor/location; efficient polling target. |
| Raw measurements | `/v3/sensors/{id}/measurements` | Drop for this feeder | Historical/query endpoint; this poller emits latest real-time state. |
| Aggregations | `/hours`, `/days`, `/years` variants | Drop | Derived historical summaries, not the latest telemetry stream. |
| Parameters/countries/providers/licenses/owners/instruments/manufacturers | collection/detail endpoints | Drop as events | Taxonomy/reference dimensions are embedded in Location/Sensor fields needed for streaming use. |
| Flags | `/locations/{id}/flags`, `/sensors/{id}/flags` | Drop for v1 | Quality flag summary is represented on measurements; full flag windows are operational metadata rather than latest telemetry. |

OpenAQ parameter metadata supplies the parameter name and `units`; common pollutants include `pm25`, `pm10`, `o3`, `no2`, `so2`, `co`, and `bc`, with values commonly in `µg/m³` and sometimes `ppm`/`ppb` depending on source. Coordinates are WGS 84 decimal degrees. Data licensing and attribution are source-specific through OpenAQ license/attribution metadata; downstream users should display OpenAQ and original-source attribution. OpenAQ documents free-tier limits of 60 requests/minute and 2,000 requests/hour with `X-RateLimit-*` headers. The default `POLL_INTERVAL=900` seconds plus `REFERENCE_REFRESH_INTERVAL=21600` keeps the default `OPENAQ_PAGE_LIMIT=25`, `OPENAQ_MAX_PAGES=1` configuration around 104 requests/hour, with wide margin. Larger configurations (for example 500 locations at a 15-minute poll) approach the hourly limit; increase `POLL_INTERVAL`, lower `OPENAQ_MAX_PAGES`, or pin `OPENAQ_LOCATIONS` for broad deployments.

## Transports

| Image | Transport | Use case |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-openaq:latest` | Kafka / Event Hubs | Replayable analytics stream keyed by location and sensor ids. |
| `ghcr.io/clemensv/real-time-sources-openaq-mqtt:latest` | MQTT 5 | Retained latest-value Unified Namespace topics for dashboards and edge subscribers. |
| `ghcr.io/clemensv/real-time-sources-openaq-amqp:latest` | AMQP 1.0 | Queue/topic consumers on Service Bus, Artemis, RabbitMQ AMQP 1.0, or Qpid Dispatch. |

## Configuration quick start

```powershell
# Kafka/Event Hubs
$env:CONNECTION_STRING='BootstrapServer=localhost:9092;EntityPath=openaq'
$env:KAFKA_ENABLE_TLS='false'
$env:OPENAQ_COUNTRIES='BE,NL'
docker run --rm -e CONNECTION_STRING -e KAFKA_ENABLE_TLS -e OPENAQ_COUNTRIES ghcr.io/clemensv/real-time-sources-openaq:latest

# MQTT
$env:MQTT_BROKER_URL='localhost:1883'
docker run --rm -e MQTT_BROKER_URL -e OPENAQ_COUNTRIES ghcr.io/clemensv/real-time-sources-openaq-mqtt:latest

# AMQP
$env:AMQP_BROKER_URL='amqp://artemis:artemis@localhost:5672/openaq'
docker run --rm -e AMQP_BROKER_URL -e OPENAQ_COUNTRIES ghcr.io/clemensv/real-time-sources-openaq-amqp:latest
```

Use `OPENAQ_API_KEY` for live OpenAQ access. Use `--mock` or `OPENAQ_MOCK=true` for hermetic tests; it emits one Location, one Sensor, and one Measurement without network access.

## Configuring sources

The feeder ships a checked-in query-slice catalog at `openaq_core/openaq_core/sources/openaq-sources.json`. Each catalog entry is a named OpenAQ API v3 query against the single global API base `https://api.openaq.org/v3`; entries are not separate servers. Use the catalog for repeatable deployments and keep `OPENAQ_COUNTRIES`, `OPENAQ_LOCATIONS`, and `OPENAQ_BBOX` as one-off legacy overrides.

| Variable | Purpose | Default |
| --- | --- | --- |
| `OPENAQ_SOURCES_FILE` | Path to a JSON catalog with OpenAQ query-slice entries. Mount your own copy when you need private deployment-specific country, location-id, or bounding-box selections. | Packaged catalog |
| `OPENAQ_SOURCES` | Comma-separated catalog entry `name`s to run, or `*` for every entry including disabled examples. When unset, entries with `enabled: true` run. | enabled entries |
| `OPENAQ_API_KEY` | Shared OpenAQ API key sent as the `X-API-Key` header for every selected slice. Register at `https://explore.openaq.org/register`. | unset |
| `OPENAQ_COUNTRIES` | Legacy single-query override: comma-separated ISO 3166-1 alpha-2 countries. Takes precedence over the catalog when set. | unset; packaged `us-all` slice matches previous `US` behavior |
| `OPENAQ_LOCATIONS` | Legacy single-query override: comma-separated OpenAQ location ids; overrides country discovery in that ad-hoc query. Takes precedence over the catalog when set. | unset |
| `OPENAQ_BBOX` | Legacy single-query override: WGS84 bbox `minLon,minLat,maxLon,maxLat`. Takes precedence over the catalog when set. | unset |
| `OPENAQ_PAGE_LIMIT` | Default locations per API page for legacy queries and catalog entries that omit `page_limit`. | `25` |
| `OPENAQ_MAX_PAGES` | Default max pages per reference refresh for legacy queries and catalog entries that omit `max_pages`. | `1` |

`OPENAQ_COUNTRIES`, `OPENAQ_LOCATIONS`, and `OPENAQ_BBOX` still work exactly for quick tests and take precedence over the catalog whenever any of them is set. In that legacy path, `OPENAQ_COUNTRIES` still defaults to `US` if only `OPENAQ_BBOX` is supplied.

### Catalog format

```json
{
  "description": "OpenAQ query-slice catalog...",
  "sources": [
    {
      "name": "us-all",
      "enabled": true,
      "description": "United States OpenAQ locations.",
      "countries": "US"
    },
    {
      "name": "eu-west",
      "enabled": false,
      "description": "Western Europe bounding-box example.",
      "bbox": "-10.50,41.00,15.50,56.50",
      "page_limit": 50,
      "max_pages": 2
    }
  ]
}
```

| Field | Required | Description |
| --- | ---: | --- |
| `name` | ✅ | Stable catalog selector used by `OPENAQ_SOURCES`. |
| `enabled` | ❌ | Defaults to `true`; disabled examples are skipped unless `OPENAQ_SOURCES=*` or selected by name. |
| `description` | ✅ | Human-readable geography, filter intent, and access notes. |
| `countries` | ❌ | ISO 3166-1 alpha-2 country code or comma/list of codes for `/v3/locations`. |
| `locations` | ❌ | OpenAQ location id or comma/list of ids. Location ids bypass country paging and fetch `/v3/locations/{id}`. |
| `bbox` | ❌ | WGS84 bounding box `minLon,minLat,maxLon,maxLat` passed to `/v3/locations`. |
| `page_limit` | ❌ | Per-slice page size for location discovery; defaults to `OPENAQ_PAGE_LIMIT`. |
| `max_pages` | ❌ | Per-slice max pages for location discovery; defaults to `OPENAQ_MAX_PAGES`. |

String fields support `${ENV_VAR}` expansion, but the shared API key should normally stay in `OPENAQ_API_KEY`, not in the catalog.

### Selecting query slices

- Unset `OPENAQ_SOURCES` — poll every catalog entry with `enabled: true`.
- `OPENAQ_SOURCES=india,us-all` — poll only those named query slices, in that order.
- `OPENAQ_SOURCES=*` — load every entry, including disabled examples. This is mostly useful for validation after editing a private catalog.
- Unknown names fail fast with a `ValueError` that lists known names.

### API key

OpenAQ API v3 uses one API key for the global API, sent in the `X-API-Key` header. Register for a key at `https://explore.openaq.org/register`, then provide it as `OPENAQ_API_KEY`; all selected query slices share that key. Do not put keys in `openaq-sources.json` unless you intentionally add a future per-slice override, and then use `${ENV_VAR}` placeholders rather than literal secrets.

### Known query slices

These example slices are checked into the default catalog. They are query filters against `https://api.openaq.org/v3`, not separate OpenAQ servers.

| Catalog name | Enabled | Query shape | Notes |
| --- | ---: | --- | --- |
| `us-all` | ✅ | `countries=US` | Default slice; preserves the previous `OPENAQ_COUNTRIES=US` behavior. |
| `eu-west` | ❌ | `bbox=-10.50,41.00,15.50,56.50` | Western Europe bounding-box example. |
| `india` | ❌ | `countries=IN` | Single-country example for India. |
| `california-bay-area` | ❌ | `bbox=-123.10,36.80,-121.50,38.40`, `page_limit=50`, `max_pages=2` | Regional smoke and urban air-quality example. |
| `africa` | ❌ | `bbox=-20.00,-35.00,52.00,38.00` | Pan-African bounding box; coverage depends on current OpenAQ station availability per country. |
| `bahrain` | ❌ | `countries=BH` | Bahrain country slice; coverage conditional on OpenAQ station availability. |
| `kuwait` | ❌ | `countries=KW` | Kuwait country slice (OpenAQ countries_id 119); coverage conditional on station availability. |
| `oman` | ❌ | `countries=OM` | Oman country slice; coverage conditional on OpenAQ station availability. |

## Fabric notebook hosting

Poll-based hosting is available through `notebook/openaq-feed.ipynb` and `tools/deploy-fabric/deploy-feeder-notebook.ps1`; the notebook resolves the Eventstream connection string at runtime and runs `openaq feed --once` on a schedule.
