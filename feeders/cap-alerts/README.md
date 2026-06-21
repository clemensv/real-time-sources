# CAP Alerts

[README](README.md) · [EVENTS](EVENTS.md) · [CONTAINER](CONTAINER.md)

Public-warning teams, emergency managers, insurers, broadcasters, and operational dashboards consume Common Alerting Protocol (CAP) feeds to decide when to warn people, reroute operations, or correlate hazards across borders. `cap-alerts` is a generalized, configuration-driven CAP 1.2 feeder: one bridge can poll multiple public CAP XML, Atom/CAP, or CAP-equivalent JSON feeds and emit normalized CloudEvents without losing provider-specific extensions.

This PR ships a default key-less configuration for US NWS active alerts and a MeteoAlarm Belgium Atom/CAP feed. It does **not** fold or modify the existing bespoke DWD, MeteoAlarm, NOAA NWS, or NWS Alerts feeders.

## Transports

| Image | Transport | Default target |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-cap-alerts:latest` | Kafka | Event Hubs or Kafka-compatible broker |
| `ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest` | MQTT 5 | MQTT broker / Event Grid namespace |
| `ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest` | AMQP 1.0 | Service Bus / AMQP broker |

## Event model

- `CapAlert` telemetry is keyed by `{cap_source_id}/{identifier}`.
- `CapZone` reference data is keyed by `{cap_source_id}/{zone_id}` and is emitted before alerts when a configured source exposes a zone metadata endpoint.
- CAP extension lists (`eventCode`, `parameter`, `geocode`, `code`) are preserved as name/value arrays. Typed compatibility fields (`same_codes`, `ugc_codes`, `vtec`, `awareness_level`, `awareness_type`) are convenience copies only.

## Configuration

Set `CAP_SOURCES` to a JSON array of `{cap_source_id, url, format, zone_url?}`. Supported formats are:

| Format | Use for | Example |
|---|---|---|
| `nws-json` | US NWS `/alerts/active` CAP-equivalent JSON | `https://api.weather.gov/alerts/active` |
| `atom-cap` | Atom indexes whose entries link to CAP XML | MeteoAlarm country feeds |
| `cap-xml` | A URL returning one CAP 1.2 XML document | Agency alert URL |
| `cap-directory` / `dwd-directory` | HTML directories containing CAP XML files | DWD open-data CAP directories |

Use `--mock` or `CAP_ALERTS_MOCK=true` for deterministic no-network E2E parsing of `tests/fixtures/sample-cap.xml`.

## Fabric notebook hosting

Because this is a poll-based feeder, `notebook/cap-alerts-feed.ipynb` follows the PegelOnline notebook pattern and is deployable through `tools/deploy-fabric/deploy-feeder-notebook.ps1`.

## Upstream audit

Reviewed CAP 1.2 standard structure, NWS `/alerts/active` and `/zones`, MeteoAlarm Atom/CAP feeds, and DWD CAP open-data directories. Kept alert telemetry and zone/area metadata where exposed; dropped unrelated non-CAP DWD observations/radar/forecast products because those remain covered by the bespoke DWD feeder and are outside generalized CAP scope.

Public default feeds require no key. NWS API guidance asks clients to identify themselves with a User-Agent; the bridge does so and defaults to a five-minute poll interval, with zone metadata refreshed every six hours. MeteoAlarm and DWD public CAP feeds publish open warning data; operators should still review each upstream's attribution and reuse terms for their deployment region.
