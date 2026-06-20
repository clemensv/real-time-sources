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

## Configuration

Set `ERDDAP_SOURCES` to semicolon-separated entries or a JSON file via `@path`:

```text
erddap_id|base_url|dataset_id|variables|station_id_variable|time_constraint
```

Example default:

```text
ioos-sensors|https://erddap.sensors.ioos.us/erddap|org_cormp_sun2|sea_water_temperature,sea_water_practical_salinity|station|time>=max(time)-1day
```

Use `ERDDAP_MOCK=true` for deterministic offline E2E fixtures. Optional authenticated servers can pass an Authorization header in JSON configuration; no secret is needed for the shipped default.

## Upstream audit summary

ERDDAP exposes `allDatasets.json` catalog discovery, `info/{datasetID}/index.json` metadata, `tabledap/{datasetID}.json` table data, and `griddap` arrays. This feeder keeps tabledap TimeSeries/TimeSeriesProfile datasets, emits metadata as reference events, polls with time constraints and `orderBy("time")`, and drops griddap by design.
