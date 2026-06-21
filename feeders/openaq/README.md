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

## Fabric notebook hosting

Poll-based hosting is available through `notebook/openaq-feed.ipynb` and `tools/deploy-fabric/deploy-feeder-notebook.ps1`; the notebook resolves the Eventstream connection string at runtime and runs `openaq feed --once` on a schedule.
