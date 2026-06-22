# ERDDAP container images — Kafka, MQTT, and AMQP

[Project overview](README.md) · [Event schemas](EVENTS.md) · [KQL schema](kql/erddap.kql) · [Deploy portal](https://clemensv.github.io/real-time-sources#erddap)

The ERDDAP images poll configured keyless or authenticated ERDDAP tabledap TimeSeries datasets, emit dataset/station reference data first, then stream generic observation CloudEvents.

## Image contract

| Image tag | Transport | Dockerfile | State |
|---|---|---|---|
| `ghcr.io/clemensv/real-time-sources-erddap-kafka:latest` | Kafka/Event Hubs/Fabric | `Dockerfile.kafka` | `STATE_FILE` |
| `ghcr.io/clemensv/real-time-sources-erddap-mqtt:latest` | MQTT 5.0 | `Dockerfile.mqtt` | `STATE_FILE` |
| `ghcr.io/clemensv/real-time-sources-erddap-amqp:latest` | AMQP 1.0 | `Dockerfile.amqp` | `STATE_FILE` |

Base image: `python:3.10-slim`. Entry points: `python -m erddap_kafka feed`, `python -m erddap_mqtt feed`, `python -m erddap_amqp feed`.

## Common environment

| Variable | Default | Description |
|---|---|---|
| `ERDDAP_SOURCES_FILE` | Packaged catalog | Path to an ERDDAP source catalog JSON file. |
| `ERDDAP_SELECT` | unset | Comma-separated catalog `name` values, `*` for all entries, or unset for enabled-only. |
| `ERDDAP_SOURCES` | unset | Legacy inline semicolon list, JSON array/object, `@file`, or path. When set, it takes precedence over the catalog and is not the selector. |
| `ERDDAP_MOCK` | `false` | Use the checked-in offline tabledap fixture and exit after one cycle. |
| `POLLING_INTERVAL` | `300` | Seconds between tabledap polling cycles. |
| `REFERENCE_REFRESH_INTERVAL` | `21600` | Seconds between dataset/station reference refreshes. |
| `STATE_FILE` | `~/.erddap_state.json` | Dedupe state file; mount a volume in containers. |
| `ONCE_MODE` | `false` | Exit after one poll cycle; used by tests and Fabric Notebook hosting. |
| `LOG_LEVEL` |  | Standard Python logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default `INFO`. |
| `POLL_INTERVAL` |  | Seconds between poll cycles. |

### Catalog format

The packaged catalog lives at `erddap_core/sources/erddap-sources.json` inside the image. Mount a copy and point `ERDDAP_SOURCES_FILE` at it when you want to add or replace sources:

```json
{
  "sources": [
    {
      "name": "ioos-sensors-sun2",
      "enabled": true,
      "description": "IOOS Sensors ERDDAP CORMP SUN2 station tabledap observations.",
      "erddap_id": "ioos-sensors",
      "base_url": "https://erddap.sensors.ioos.us/erddap",
      "dataset_id": "org_cormp_sun2",
      "variables": ["sea_water_temperature", "sea_water_practical_salinity"],
      "station_id_variable": "station",
      "time_constraint": "time>=max(time)-1day",
      "auth_header": null
    }
  ]
}
```

| Field | Required | Description |
|---|---:|---|
| `name` | Yes | Stable catalog selector name. |
| `enabled` | No | Runs when `ERDDAP_SELECT` is unset; defaults to `true`. |
| `description` | No | Operator-facing notes. |
| `erddap_id` | Yes | Stable source identifier used in CloudEvent subjects and keys. |
| `base_url` | Yes | ERDDAP server root URL. |
| `dataset_id` | Yes | ERDDAP tabledap datasetID. |
| `variables` | Yes | Dataset variables to request. |
| `station_id_variable` | No | Station/platform identifier variable for TimeSeries datasets. |
| `time_constraint` | No | ERDDAP tabledap constraint; defaults to `time>=max(time)-1day`. |
| `auth_header` | No | Optional Authorization header; supports `${ENV_VAR}` interpolation. |

### Selecting sources

Unset `ERDDAP_SELECT` to run enabled catalog entries only. Set it to a comma-separated allow-list to run named entries in the requested order:

```powershell
docker run --rm `
  -v ${PWD}\erddap-sources.json:/catalog/erddap-sources.json:ro `
  -e ERDDAP_SOURCES_FILE=/catalog/erddap-sources.json `
  -e ERDDAP_SELECT=ioos-sensors-sun2 `
  ghcr.io/clemensv/real-time-sources-erddap-kafka:latest
```

Set `ERDDAP_SELECT=*` to include disabled templates. The legacy `ERDDAP_SOURCES` variable is still accepted for existing deployments and has precedence when set, so the selector is intentionally named `ERDDAP_SELECT`.

### Keeping secrets out of the catalog

Use `${ENV_VAR}` placeholders for sensitive string fields such as `auth_header`, then pass the secret at runtime:

```json
"auth_header": "Bearer ${ERDDAP_TOKEN}"
```

```powershell
docker run --rm `
  -v ${PWD}\erddap-sources.json:/catalog/erddap-sources.json:ro `
  -e ERDDAP_SOURCES_FILE=/catalog/erddap-sources.json `
  -e ERDDAP_SELECT=private-erddap `
  -e ERDDAP_TOKEN=$env:ERDDAP_TOKEN `
  ghcr.io/clemensv/real-time-sources-erddap-kafka:latest
```

### Known ERDDAP servers

ERDDAP is a widely deployed oceanographic and environmental table server. This feeder polls only `tabledap` datasets, not `griddap`.

| Operator | ERDDAP root |
|---|---|
| IOOS Sensors | `https://erddap.sensors.ioos.us/erddap` |
| NOAA CoastWatch West Coast Node | `https://coastwatch.pfeg.noaa.gov/erddap` |
| NOAA PMEL | `https://data.pmel.noaa.gov/pmel/erddap` |
| NOAA Atlantic Oceanographic and Meteorological Laboratory | `https://cwcgom.aoml.noaa.gov/erddap` |
| EMODnet Physics | `https://erddap.emodnet-physics.eu/erddap` |
| Australian Integrated Marine Observing System | `https://erddap.imos.org.au/erddap` |
| Ocean Tracking Network | `https://members.oceantrack.org/erddap` |
| NANOOS / NWEM | `https://nwem.apl.uw.edu/erddap` |
| University of Hawaii Sea Level Center | `https://uhslc.soest.hawaii.edu/erddap` |

#### Ready-to-enable catalog entries

These packaged entries are disabled by default. Select them explicitly with `ERDDAP_SELECT=<name>` when you are ready to poll the upstream dataset.

| Region | Entry name | Server | Dataset ID | Status |
|---|---|---|---|---|
| Global marine telemetry | `otn-tracking` | Ocean Tracking Network | `otn_aat_detections` | Ready-to-enable |
| US — Puget Sound | `nanoos-puget-sound-orca2` | NANOOS / NWEM | `orca2_L1_profiles` | Ready-to-enable |
| Europe | `emodnet-physics-sea-level` | EMODnet Physics | `EP_ERD_INT_SLEV_AL_TS_NRT` | Ready-to-enable |
| Global tide gauges | `uhslc-hourly-fast` | University of Hawaii Sea Level Center | `global_hourly_fast` | Ready-to-enable |

## Kafka

```bash
docker run --rm -e CONNECTION_STRING='BootstrapServer=host:9092;EntityPath=erddap' -e KAFKA_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-erddap-kafka:latest
```

Kafka variables: `CONNECTION_STRING`, `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `KAFKA_ENABLE_TLS`, `SASL_USERNAME`, `SASL_PASSWORD`.

## MQTT

```bash
docker run --rm -e MQTT_BROKER_URL='broker:1883' -e MQTT_ENABLE_TLS=false ghcr.io/clemensv/real-time-sources-erddap-mqtt:latest
```

MQTT variables: `MQTT_BROKER_URL`, `MQTT_ENABLE_TLS`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CA_FILE`, `MQTT_CLIENT_ID`. Event Grid namespace deployments use the MQTT image and Entra-capable template generated for this repo.

## AMQP 1.0

```bash
docker run --rm -e AMQP_BROKER_URL='amqp://user:pass@broker:5672/erddap' ghcr.io/clemensv/real-time-sources-erddap-amqp:latest
```

AMQP variables: `AMQP_BROKER_URL`, `AMQP_HOST`, `AMQP_PORT`, `AMQP_ADDRESS`, `AMQP_TLS`, `AMQP_USERNAME`, `AMQP_PASSWORD`, `AMQP_AUTH_MODE`, `AMQP_ENTRA_AUDIENCE`, `AMQP_ENTRA_CLIENT_ID`.

## Azure and Fabric

The catalog exposes five Azure templates (Kafka BYO/Event Hubs, MQTT BYO/Event Grid, AMQP Service Bus) and a Fabric Notebook option. The notebook uses the same Kafka bridge in `--once` mode and resolves the Eventstream connection string at runtime; it does not store `CONNECTION_STRING` as a parameter.
