# DATEX II real-time traffic feeder

[Events](EVENTS.md) · [Container contract](CONTAINER.md) · [Source contract](xreg/datex2.xreg.json)

DATEX II is the European road-traffic exchange standard used by traffic-management centres to share incidents, roadworks, speed/flow observations, and measurement-site catalogues. This generalized feeder polls a configurable registry of DATEX II XML endpoints and emits normalized CloudEvents so transport operators, journey-planning teams, digital twins, and road-safety analysts can consume multiple road authorities through one contract.

## Scope and upstream hit list

Kept for this build: `SituationPublication`, `MeasuredDataPublication`, `MeasurementSiteTablePublication`, and a future slot for `PredefinedLocationsPublication` reference data. NDW free endpoints studied include incidents/planning feeds, `trafficspeed`, `traveltime`, and `measurement_current` site tables. Bison Futé/French feeders were studied for measured flow and road-event situation profiles. Dropped for now: parking, EV charging, VMS/MSI/DRIP sign-display profiles, and provider-specific non-traffic metadata; those remain later DATEX II profile groups and the existing bespoke feeders are not folded in this PR.

## Transports

| App | Image | Transport | Default shape |
| --- | --- | --- | --- |
| `datex2_kafka` | `ghcr.io/clemensv/real-time-sources-datex2:latest` | Kafka/Event Hubs | Structured CloudEvents on one configured topic. |
| `datex2_mqtt` | `ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest` | MQTT 5 | Binary CloudEvents under `traffic/{country}/{operator}/datex2/...`. |
| `datex2_amqp` | `ghcr.io/clemensv/real-time-sources-datex2-amqp:latest` | AMQP 1.0 | Binary CloudEvents to one queue/topic address. |

Sources are defined in a checked-in catalog file and selected with an environment variable — see [Configuring sources](#configuring-sources). Set `DATEX2_MOCK=true` for deterministic local and Docker E2E validation.

Fabric notebook hosting is included via `notebook/datex2-feed.ipynb` and can be deployed with `tools/deploy-fabric/deploy-feeder-notebook.ps1`.

## Configuring sources

The feeder ships a checked-in source catalog at `datex2_core/datex2_core/sources/datex2.sources.json`. Each entry is a pollable DATEX II XML endpoint. Use the catalog for repeatable deployments and keep `DATEX2_ENDPOINTS` as a one-off override.

| Variable | Description | Default |
| --- | --- | --- |
| `DATEX2_SOURCES_FILE` | Path to a JSON catalog of DATEX II source entries. Mount your own copy to poll road authorities not shipped by default. | Packaged catalog |
| `DATEX2_SOURCES` | Comma-separated catalog entry `name`s to run, or `*` for every entry including disabled templates. When unset, entries with `enabled: true` run. | enabled entries |
| `DATEX2_ENDPOINTS` | Legacy inline JSON endpoint list or `@file`. Takes precedence over the catalog whenever it is set. | unset |

### Catalog format

```json
{
  "description": "DATEX II source catalog...",
  "sources": [
    {
      "name": "ndw-trafficspeed",
      "enabled": true,
      "description": "NDW (Netherlands) measured traffic speed and flow.",
      "id": "ndw",
      "url": "https://opendata.ndw.nu/trafficspeed.xml.gz",
      "publication": "MeasuredDataPublication",
      "country": "nl",
      "operator": "ndw"
    }
  ]
}
```

| Field | Required | Description |
| --- | --- | --- |
| `name` | ✅ | Stable catalog selector used by `DATEX2_SOURCES`. |
| `enabled` | ❌ | Defaults to `true`; disabled entries are skipped unless `DATEX2_SOURCES=*` or selected by name. |
| `description` | ✅ | Human-readable summary of the feed. |
| `id` | ✅ | Short supplier identifier used in event keys and subjects. |
| `url` | ✅ | DATEX II XML endpoint URL (plain or gzipped). |
| `publication` | ✅ | DATEX II publication type, e.g. `MeasuredDataPublication`, `SituationPublication`, `MeasurementSiteTablePublication`. |
| `country` | ❌ | ISO country code used in MQTT topics and event metadata. |
| `operator` | ❌ | Operator label used in MQTT topics and event metadata. |
| `auth_header` | ❌ | Optional `Authorization` header value; use `${ENV_VAR}` placeholders for secrets. |

### Selecting sources

- Unset `DATEX2_SOURCES` — poll every catalog entry with `enabled: true` (the four NDW feeds).
- `DATEX2_SOURCES=ndw-trafficspeed,cita-luxembourg-a6` — poll only those entries, in that order.
- `DATEX2_SOURCES=*` — load every entry, including disabled templates.
- Unknown names fail fast with a `ValueError` that lists the known names.

### Keeping secrets out of the catalog

Write `${ENV_VAR}` placeholders in string fields (for example `"auth_header": "Bearer ${TRAFIKVERKET_KEY}"`) and provide the secret at runtime; the loader expands them from the environment at load time.

### Known DATEX II sources

DATEX II is published by many European road authorities. This feeder ships the four no-auth NDW (Netherlands) feeds enabled, three open CITA Luxembourg motorway corridors disabled, and a disabled key-protected Trafikverket (Sweden) template; add other publishers by copying the catalog and choosing the publication that matches the contract.

| Catalog name | Status | Publisher | Public URL / notes |
| --- | --- | --- | --- |
| `ndw-measurement-sites` | Shipped enabled | Nationaal Dataportaal Wegverkeer (NL) | `https://opendata.ndw.nu/measurement_current.xml.gz` — MeasurementSiteTablePublication reference data. |
| `ndw-trafficspeed` | Shipped enabled | NDW (NL) | `https://opendata.ndw.nu/trafficspeed.xml.gz` — MeasuredDataPublication speed/flow. |
| `ndw-traveltime` | Shipped enabled | NDW (NL) | `https://opendata.ndw.nu/traveltime.xml.gz` — MeasuredDataPublication travel times. |
| `ndw-roadworks` | Shipped enabled | NDW (NL) | `https://opendata.ndw.nu/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz` — SituationPublication roadworks and events. |
| `cita-luxembourg-a6` | Shipped disabled | CITA Luxembourg (LU) | `https://www.cita.lu/info_trafic/datex/trafficstatus_a6` — A6 corridor MeasuredDataPublication. Other corridors: `trafficstatus_a1/a3/a4/a7/a13/b40`. |
| `cita-luxembourg-a1` | Shipped disabled | CITA Luxembourg (LU) | `https://www.cita.lu/info_trafic/datex/trafficstatus_a1` — A1 corridor. |
| `cita-luxembourg-a4` | Shipped disabled | CITA Luxembourg (LU) | `https://www.cita.lu/info_trafic/datex/trafficstatus_a4` — A4 corridor. |
| `trafikverket-sweden` | Shipped disabled template | Trafikverket (SE) | Key-protected DATEX II; register at `https://data.trafikverket.se/`, export `TRAFIKVERKET_KEY`, then set the requested feed `url`. |
| not shipped | Custom DATEX II publisher | Any national/regional road authority | Copy an entry, set `url` + `publication`, add `auth_header` for key-protected feeds. |

Parking (`ParkingStatusPublication`) and EV-charging DATEX II profiles are out of scope for this feeder's parser, which targets situation, measured-data, and measurement-site publications.

## Quick start

```powershell
docker pull ghcr.io/clemensv/real-time-sources-datex2:latest
docker pull ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest
docker pull ghcr.io/clemensv/real-time-sources-datex2-amqp:latest
```

Kafka/Event Hubs:

```powershell
docker run --rm -e CONNECTION_STRING="BootstrapServer=broker:9092;EntityPath=datex2" -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-datex2:latest
```

MQTT 5:

```powershell
docker run --rm -e MQTT_BROKER_URL="broker:1883" -e MQTT_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-datex2-mqtt:latest
```

AMQP 1.0:

```powershell
docker run --rm -e AMQP_HOST="broker" -e AMQP_ADDRESS="datex2" -e AMQP_USERNAME="user" -e AMQP_PASSWORD="secret" ghcr.io/clemensv/real-time-sources-datex2-amqp:latest
```

## Deploy

[![Deploy Kafka BYO connection](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template.json)
[![Deploy Event Hubs](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-eventhub.json)
[![Deploy MQTT BYO broker](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-mqtt.json)
[![Deploy Event Grid MQTT](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-eventgrid-mqtt.json)
[![Deploy Service Bus AMQP](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fclemensv%2Freal-time-sources%2Fmain%2Ffeeders%2Fdatex2%2Fazure-template-with-servicebus.json)

See [CONTAINER.md](CONTAINER.md) for the full environment-variable contract and authentication options.
