# CAP Alerts

[Events](EVENTS.md) · [Container contract](CONTAINER.md) · [Source contract](xreg/cap-alerts.xreg.json)

Emergency managers, broadcasters, public-safety dashboards, insurers, and critical-infrastructure operators use Common Alerting Protocol (CAP) feeds to decide when to warn people, reroute crews, correlate cross-border hazards, and preserve an auditable alert record. `cap-alerts` is the configuration-driven generalization of the repo's bespoke `dwd`, `meteoalarm`, `noaa-nws`, and `nws-alerts` feeders: one bridge polls a file-based catalog of public CAP XML, Atom/CAP, or CAP-equivalent JSON feeds and emits normalized CloudEvents while preserving provider extensions.

The packaged catalog ships two enabled, key-less sources migrated from the original inline default: US NWS active alerts and MeteoAlarm Belgium. Add more agencies by copying the catalog and selecting entries with `CAP_SELECT`.

## Transports

| App | Image | Transport | Default shape |
| --- | --- | --- | --- |
| `cap_alerts` | `ghcr.io/clemensv/real-time-sources-cap-alerts:latest` | Kafka/Event Hubs | Structured CloudEvents on one configured topic. |
| `cap_alerts_mqtt` | `ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest` | MQTT 5 | Binary CloudEvents under the generated CAP topic tree. |
| `cap_alerts_amqp` | `ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest` | AMQP 1.0 | Binary CloudEvents to one queue/topic address. |

## Event model

- `CapAlert` telemetry is keyed by `{cap_source_id}/{identifier}`.
- `CapZone` reference data is keyed by `{cap_source_id}/{zone_id}` and is emitted before alerts when a configured source exposes a zone metadata endpoint.
- CAP extension lists (`eventCode`, `parameter`, `geocode`, `code`) are preserved as name/value arrays. Typed compatibility fields (`same_codes`, `ugc_codes`, `vtec`, `awareness_level`, `awareness_type`) are convenience copies only.

## Quick start

```powershell
docker pull ghcr.io/clemensv/real-time-sources-cap-alerts:latest
docker pull ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest
```

Kafka/Event Hubs:

```powershell
docker run --rm -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=cap-alerts" -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-cap-alerts:latest
```

MQTT 5:

```powershell
docker run --rm -e MQTT_BROKER_URL="broker:1883" -e MQTT_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-cap-alerts-mqtt:latest
```

AMQP 1.0:

```powershell
docker run --rm -e AMQP_HOST="broker" -e AMQP_ADDRESS="cap-alerts" -e AMQP_USERNAME="user" -e AMQP_PASSWORD="secret" ghcr.io/clemensv/real-time-sources-cap-alerts-amqp:latest
```

## Configuring sources

| Variable | Description | Default |
| --- | --- | --- |
| `CAP_SOURCES_FILE` | Path to a catalog JSON file. Use this for durable source lists mounted into containers. | packaged `cap_alerts_core/sources/cap-sources.json` |
| `CAP_SELECT` | Selector for catalog entries: comma-separated `name` values in requested order, `*` for every entry including disabled templates, or unset for `enabled: true` only. | unset |
| `CAP_SOURCES` | Legacy inline JSON source list, `@file`, or path. When set, it takes precedence over `CAP_SOURCES_FILE`; it is **not** the selector because that name was already used by the legacy inline list. | unset |

### Catalog format

`cap_alerts_core/sources/cap-sources.json` is a JSON object with a `sources` array. A bare JSON list is still accepted for legacy `CAP_SOURCES`.

| Field | Required | Description |
| --- | --- | --- |
| `name` | catalog only | Stable selector name used by `CAP_SELECT`. |
| `enabled` | catalog only | `true` entries run when `CAP_SELECT` is unset; `false` entries are templates or opt-in sources. |
| `description` | catalog only | Human-readable agency/feed description. |
| `cap_source_id` | yes | Stable source identifier emitted in CloudEvents subjects and keys. |
| `url` | yes | CAP XML, Atom/CAP, CAP directory, or supported provider JSON endpoint. |
| `format` | no | `nws-json`, `atom-cap`, `cap-xml`, `cap-directory`, or `dwd-directory`; default `cap-xml`. |
| `zone_url` | no | Optional provider metadata endpoint used to emit `CapZone` reference events. |
| `auth_env` | no | Name of an environment variable whose value is sent as the `Authorization` header. |
| `auth_header` | no | Authorization header value; may contain `${ENV_VAR}` placeholders expanded at runtime. |

### Selecting sources

Unset `CAP_SELECT` runs only enabled catalog entries:

```powershell
-e CAP_SELECT=""
```

Run entries in an explicit order:

```powershell
-e CAP_SELECT="meteoalarm-belgium,nws-us-active-alerts"
```

Run every entry, including disabled templates:

```powershell
-e CAP_SELECT="*"
```

Unknown names fail fast with `ValueError` and the known-name list.

### Bring your own catalog

Copy the packaged catalog, edit entries, and mount it into the container:

```powershell
docker run --rm `
  -v ${PWD}\cap-sources.json:/config/cap-sources.json:ro `
  -e CAP_SOURCES_FILE="/config/cap-sources.json" `
  -e CAP_SELECT="nws-us-active-alerts" `
  -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=cap-alerts" `
  -e KAFKA_ENABLE_TLS=false `
  ghcr.io/clemensv/real-time-sources-cap-alerts:latest
```

For key-protected feeds, keep secrets in environment variables and reference them from the catalog, for example `"auth_header": "Bearer ${CAP_FEED_TOKEN}"`.

### Known CAP sources

| Source | URL | Feeder status |
| --- | --- | --- |
| US National Weather Service / NOAA active alerts | `https://api.weather.gov/alerts/active` | Shipped enabled as `nws-us-active-alerts` (`nws-json`). |
| MeteoAlarm Belgium Atom/CAP | `https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-belgium` | Shipped enabled as `meteoalarm-belgium` (`atom-cap`). |
| MeteoAlarm national feeds — Ireland, France, Spain, Germany, Austria, Italy, Netherlands, Portugal, Switzerland, Poland | `https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-{country}` | Shipped disabled as `meteoalarm-{country}` (`atom-cap`); aggregate the national met services (Met Éireann, Météo-France, AEMET, DWD, GeoSphere, KNMI, IPMA, MeteoSwiss, IMGW). Add the name to `CAP_SELECT` to enable. |
| DWD CAP warning directory | `https://opendata.dwd.de/weather/alerts/cap/COMMUNEUNION_DWD_STAT/` | Available for custom catalogs; the repo also has a bespoke `dwd` feeder. |
| GDACS CAP/RSS disaster alerts | `https://www.gdacs.org/xml/gdacs_cap.xml` | Available for custom catalogs after validating parsing for its RSS/CAP shape. |
| Environment and Climate Change Canada CAP datamart | `https://dd.weather.gc.ca/alerts/cap/` | Available for custom catalogs; verify the current regional directory/file shape before enabling. |
| Australian Bureau of Meteorology public warnings | `http://www.bom.gov.au/fwo/IDZ00059.warnings_national.xml` | Available for custom catalogs where network access permits; verify BOM terms and format before enabling. |

## Deploy

[![Deploy Kafka BYO connection](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template.json)
[![Deploy Event Hubs](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template-with-eventhub.json)
[![Deploy MQTT BYO broker](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template-mqtt.json)
[![Deploy Event Grid MQTT](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template-with-eventgrid-mqtt.json)
[![Deploy Service Bus AMQP](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fcap-alerts%2Fazure-template-with-servicebus.json)

See [CONTAINER.md](CONTAINER.md) for the full runtime and authentication contract.
