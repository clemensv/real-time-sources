# ERDDAP

[🚀 Deploy to Azure](https://clemensv.github.io/real-time-sources#erddap) · [📓 Fabric Notebook](https://clemensv.github.io/real-time-sources#erddap/fabric-notebook) · [🐳 Container contract](CONTAINER.md) · [📑 Event schemas](EVENTS.md) · [🗄️ KQL schema](kql/erddap.kql)

ERDDAP tabledap servers publish real-time oceanographic and environmental station observations from hundreds of agencies. This generalized feeder lets operations teams, coastal scientists, harbor authorities, weather dashboards, and Fabric/ADX analytics users configure a list of ERDDAP servers and datasetIDs once, then subscribe to CloudEvents instead of building one poller per buoy or platform network.

## Scope

**Included:** ERDDAP `tabledap` TimeSeries and TimeSeriesProfile datasets with a `cf_role=timeseries_id` station/platform variable, plus single-station fallback datasets. The shipped default uses the keyless IOOS Sensors server and dataset `org_cormp_sun2`.

**Deliberately skipped:** `griddap`. Gridded satellite/model arrays are large multidimensional rasters, not a station-oriented real-time event stream. They need tiling/chunking semantics outside this feeder.

## Transports

| Image | Transport | Default delivery |
|---|---|---|
| `ghcr.io/clemensv/real-time-sources-erddap-kafka:latest` | Kafka/Event Hubs/Fabric Eventstream | CloudEvents on topic `erddap`, keys `{erddap_id}/{dataset_id}` and `{erddap_id}/{dataset_id}/{station_id}` |
| `ghcr.io/clemensv/real-time-sources-erddap-mqtt:latest` | MQTT 5.0 | UNS topics under `marine/global/erddap/...`; reference events retained |
| `ghcr.io/clemensv/real-time-sources-erddap-amqp:latest` | AMQP 1.0 / Service Bus | Binary CloudEvents on one queue/topic/address |

## Events

* `org.erddap.DatasetMetadata` — reference metadata from `allDatasets` and `/info/{datasetID}/index.json`.
* `org.erddap.StationMetadata` — reference station/platform metadata using the `timeseries_id` variable or dataset fallback.
* `org.erddap.Observation` — generic observation rows with common coordinates and a map of dataset-specific variables. Per-variable units are data because ERDDAP datasets are heterogeneous.

## Configuring sources

ERDDAP uses a packaged file-based source catalog. By default the feeder polls every catalog entry whose `enabled` flag is `true`; the checked-in catalog ships the verified IOOS Sensors SUN2 tabledap dataset, ready-to-enable disabled public datasets, and one disabled authenticated-template entry.

| Variable | Description | Default |
|---|---|---|
| `ERDDAP_SOURCES_FILE` | Path to a JSON catalog file. Use this for a mounted copy of `erddap_core/sources/erddap-sources.json`. | Packaged catalog |
| `ERDDAP_SELECT` | Comma-separated catalog `name` values to run in that order, or `*` to include disabled entries. Unset runs enabled entries only. | unset |
| `ERDDAP_SOURCES` | Legacy inline configuration: semicolon list, JSON array/object, `@file`, or path. When set, it takes precedence over the catalog and is not the selector. | unset |

### Catalog format

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
| `enabled` | No | `true` entries run when `ERDDAP_SELECT` is unset; defaults to `true`. |
| `description` | No | Human-readable notes for operators. |
| `erddap_id` | Yes | Stable source identifier used in CloudEvent subjects and keys. |
| `base_url` | Yes | ERDDAP server root, for example `https://erddap.sensors.ioos.us/erddap`. |
| `dataset_id` | Yes | ERDDAP tabledap datasetID. |
| `variables` | Yes | Observation variable names to request in addition to time/station/coordinate fields. |
| `station_id_variable` | No | TimeSeries station/platform identifier variable, commonly `station` or `platform`; omit for single-station fallback datasets. |
| `time_constraint` | No | ERDDAP tabledap constraint such as `time>=max(time)-1day`. |
| `auth_header` | No | Optional HTTP Authorization header. Supports `${ENV_VAR}` interpolation. |

### Selecting sources

Run the enabled entries in the packaged catalog:

```powershell
docker run --rm ghcr.io/clemensv/real-time-sources-erddap-kafka:latest
```

Run a mounted catalog entry by name:

```powershell
docker run --rm `
  -v ${PWD}\erddap-sources.json:/catalog/erddap-sources.json:ro `
  -e ERDDAP_SOURCES_FILE=/catalog/erddap-sources.json `
  -e ERDDAP_SELECT=ioos-sensors-sun2 `
  ghcr.io/clemensv/real-time-sources-erddap-kafka:latest
```

Set `ERDDAP_SELECT=*` to include disabled template entries after you copy, edit, and intentionally enable or select them. `ERDDAP_SOURCES` remains the legacy inline-list variable and therefore is not reused as the selector.

### Keeping secrets out of the catalog

Catalog string fields expand `${ENV_VAR}` at load time, including `auth_header`. Keep tokens in the container environment or your orchestrator's secret store:

```json
{
  "name": "private-erddap",
  "enabled": true,
  "erddap_id": "private",
  "base_url": "https://example.org/erddap",
  "dataset_id": "REPLACE_WITH_DATASET_ID",
  "variables": ["temperature"],
  "station_id_variable": "station",
  "time_constraint": "time>=max(time)-1day",
  "auth_header": "Bearer ${ERDDAP_TOKEN}"
}
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

ERDDAP is widely deployed for oceanographic and environmental data. This feeder is **tabledap-only**; confirm the dataset is a TimeSeries/TimeSeriesProfile-style table with a station/platform identifier before adding it to the catalog.

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

### Ready-to-enable catalog entries

These entries are checked in with `"enabled": false`, so they do not run by default. Add the entry `name` to `ERDDAP_SELECT` after reviewing the upstream terms and expected event volume.

| Region | Entry name | Server | Dataset ID | Status |
|---|---|---|---|---|
| Global marine telemetry | `otn-tracking` | Ocean Tracking Network | `otn_aat_detections` | Ready-to-enable |
| US — Puget Sound | `nanoos-puget-sound-orca2` | NANOOS / NWEM | `orca2_L1_profiles` | Ready-to-enable |
| Europe | `emodnet-physics-sea-level` | EMODnet Physics | `EP_ERD_INT_SLEV_AL_TS_NRT` | Ready-to-enable |
| Global tide gauges | `uhslc-hourly-fast` | University of Hawaii Sea Level Center | `global_hourly_fast` | Ready-to-enable |

Use `ERDDAP_MOCK=true` for deterministic offline E2E fixtures. No secret is needed for the shipped IOOS default.

## Upstream audit summary

ERDDAP exposes `allDatasets.json` catalog discovery, `info/{datasetID}/index.json` metadata, `tabledap/{datasetID}.json` table data, and `griddap` arrays. This feeder keeps tabledap TimeSeries/TimeSeriesProfile datasets, emits metadata as reference events, polls with time constraints and `orderBy("time")`, and drops griddap by design.
