# Ingesting DWD Events into Microsoft Fabric

This guide describes the recommended flow for landing the DWD bridge's events
into a **Microsoft Fabric Lakehouse** and exposing the results as
**Fabric Maps** layers.

> **Executable extension:** The design below is realized by
> [`tools/dwd/fabric/`](../tools/dwd/fabric/README.md) — DWD-specific KQL
> assets, a Spark Structured Streaming notebook, and a `setup.ps1` that
> layers them on top of the basic per-source deployment from
> [`tools/deploy-fabric/`](../tools/deploy-fabric/README.md). The rest of
> this document is the design narrative; the executable bits live there.

The bridge emits CloudEvents on Kafka topic `dwd`. Two shapes appear:

- **Inline-data events** — the payload IS the data
  (10‑minute observations, station metadata, CAP alerts already parsed
  by the bridge).
- **File-reference events** — the payload carries a `file_url` pointing
  to an anonymously fetchable resource on `https://opendata.dwd.de/`
  (radar composites, ICON‑D2 GRIB2 forecast files). See
  [Fetching Referenced Files](README.md#fetching-referenced-files) for
  payload-format details.

## Architecture

```
DWD bridge ──Kafka / Event Hub──▶ Fabric Eventstream "dwd-ingest"
                                          │
                ┌─────────────────────────┴──────────────────────────┐
                ▼                                                    ▼
        Eventhouse destination                          Activator destination (optional)
        _cloudevents_dispatch                           dwd-ingest-activator
        (every event, KQL-queryable)                    (rule → "Run Fabric item" → notebook)
                │
                ▼  (update policies in dwd.kql fan rows
                │   into 13 typed tables)
        Typed KQL tables  +  CogCatalog
                │
                ▼  dwd_ingest notebook pulls new rows
                │   since a watermark
        Lakehouse Files/bronze/<channel>/...   Files/gold/*_cog/...
        (raw upstream bytes)                  (Cloud Optimized GeoTIFF
                                               for Fabric Maps)
```

Eventstream destinations are restricted to the types declared in the
official [eventstream definition template](https://github.com/microsoft/fabric-event-streams/blob/main/API%20Templates/eventstream-definition.json):
`Lakehouse`, `Eventhouse`, `Activator`, `AzureDataExplorer`,
`DerivedStream`, `CustomEndpoint`. There is no "Notebook" destination —
notebooks are invoked either on a schedule or by an Activator rule's
"Run Fabric item" action.

## Trigger options for the notebook

| Option | Pros | Cons | When to pick |
|---|---|---|---|
| **Scheduled** (Notebook → Schedule, e.g. every 1–5 min) | Trivial to set up, no extra items, predictable cost. | Latency floor = schedule interval; backlog risk during burst (ICON-D2 model runs). | Default. Good fit for all DWD channels: live observations are 10‑min cadence; ICON-D2 emits in concentrated bursts where micro-latency doesn't matter. |
| **Activator rule** (Eventstream → Activator destination → rule with "Run Fabric item" action) | Event-driven; rule conditions can filter to a specific CloudEvents `type` or threshold. | Each rule fires a notebook job (cold start ~30 s); fan-out per event is expensive for ICON-D2 bursts. | Use for low-volume, high-importance triggers (e.g. fire only on `DE.DWD.Weather.Alert` Severe/Extreme alerts). |
| **Scheduled + Activator** (hybrid) | Scheduled run drains everything; Activator rule provides low-latency notify for selected events. | More moving parts. | Production setups that need both throughput and selective fast-path. |

## Why not per‑event triggering for ICON‑D2

ICON‑D2 emits thousands of file‑reference events per 3‑hour model cycle.
Triggering a notebook per event via Activator would pay cold-start cost
per file and saturate capacity. The scheduled notebook batches the
backlog in one job with bounded HTTP concurrency, respecting DWD usage
guidance.

## Per‑channel pipeline

| Channel | Event payload | Fetch needed? | Bronze layout (`Files/`) | Silver Delta (`Tables/`) | Decoder |
|---|---|---|---|---|---|
| 10‑min observations | Inline rows | No | optional raw JSON for replay | `silver.obs_10min` partitioned by `station_id`, `date(ts)` | already parsed by bridge |
| Station metadata | Inline | No | — | `silver.dim_station` (SCD‑1, MERGE on `station_id`) | already parsed |
| CAP alerts | Inline parsed + raw XML | No | `Files/bronze/cap/yyyy=…/mm=…/dd=…/<msgId>.xml` (audit copy) | `silver.cap_alert` + `silver.cap_alert_area` | already parsed |
| Radar composite | `file_url` + product metadata | **Yes** | `Files/bronze/radar/<product>/yyyy=…/mm=…/dd=…/HH/<file_name>` | `silver.radar_product` (metadata only in v1) | `h5py` / `wradlib` for ODIM‑H5; `eccodes` / `pdbufr` for BUFR |
| ICON‑D2 forecast | `file_url` + run/lead/level/param | **Yes** | `Files/bronze/icon-d2/run=YYYYMMDDHH/lead=NNN/<param>/<level_type>/<file_name>` | `silver.icon_d2_file` (parsed GRIB headers) | `cfgrib` (xarray) or `pygrib`; bz2 streamed via `bz2.open` |

### Notebook skeleton (watermark-driven pull)

```python
import json, requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

# 1) load watermark from Files/_state/dwd_ingest_watermark.json
# 2) KQL query _cloudevents_dispatch | where ['time'] > datetime(<since>)
#    against the Eventhouse query URI (KUSTO_URI)
# 3) classify each event, fan out file-reference events to a fetcher pool
# 4) write bronze bytes, optionally render COG, ingest CogCatalog rows
# 5) advance the watermark to max(time) seen

def fetch_and_land(row):
    # anonymous HTTPS GET of row.data.file_url with If-None-Match
    # write bytes to Files/bronze/<channel>/... (atomic .tmp + rename)
    # compute sha256 + size; decode headers for CogCatalog row
    ...

rows = kql_query(f"_cloudevents_dispatch | where ['time'] > datetime({since}) "
                  "| where type startswith 'DE.DWD.' | order by ['time'] asc")
with ThreadPoolExecutor(max_workers=16) as pool:
    results = list(pool.map(fetch_and_land, rows))
save_watermark(rows[-1]['time'])
```

### Idempotency & state

- Natural key: `file_url` + upstream `Last-Modified` / `ETag`.
- CogCatalog uses `MERGE`-style ingest semantics so retries and replays
  don't duplicate.
- Watermark file `Files/_state/dwd_ingest_watermark.json` is the only
  durable state the notebook keeps; deleting it triggers a full backfill
  bounded by the dispatch table retention.
- Bronze writes are atomic (`.tmp` then rename) and skipped when the
  target exists with matching size + sha256.

### Scale & throttling

- Bounded `ThreadPoolExecutor` per run (≈16 workers for ICON‑D2,
  fewer for radar where individual files can be ~10 MB).
- Backpressure via the notebook schedule interval (more frequent runs =
  smaller batches per run).
- Custom `User-Agent: fabric-dwd-ingest/<workspace>` per DWD guidance.

### Auth & networking

- Upstream `opendata.dwd.de`: anonymous HTTPS, no auth, no key, no
  referer. Range and conditional GET supported.
- Fabric → Lakehouse: workspace managed identity.
- Outbound HTTPS to `opendata.dwd.de` must be reachable from the Spark
  pool (default Fabric egress is open; verify when private link is in
  use).

## Gold tier — Fabric Maps layer outputs

Fabric Maps composes **vector layers** (points / lines / polygons from
Eventhouse KQL or Lakehouse files) and **imagery layers** (Azure Maps
basemap, **Cloud Optimized GeoTIFF in OneLake**, or WMS / WMTS). See
[Fabric Maps layers](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/map/about-layers).

| Channel | Layer kind | Source for the layer | Geometry / format |
|---|---|---|---|
| Stations | Vector — points (static) | Eventhouse view `map.stations` over `silver.dim_station` | `Point(lon, lat)` per station |
| 10‑min observations | Vector — points (live) | KQL function `map.obs_latest()` joined to `dim_station` | Point with `temp`, `precip`, `wind`, `ts` |
| CAP alerts | Vector — polygons (live) | KQL function `map.cap_active()` over `silver.cap_alert_area` | MultiPolygon with severity, headline, expires |
| Radar composite | **Imagery — COG** in OneLake | Decoder writes `Files/gold/radar_cog/<product>/yyyy=…/mm=…/dd=…/HH/<file>.tif` | Reprojected to EPSG:3857, tiled + overviews |
| ICON‑D2 forecast | **Imagery — COG per (parameter, run, lead, level)** | `Files/gold/icon_d2_cog/param=<p>/level=<l>/run=YYYYMMDDHH/lead=NNN.tif` | Reprojected to EPSG:3857, parameter‑specific colormap |

### COG conversion

- Tooling: `rasterio` + `rio-cogeo` (or `gdal_translate -of COG`) inside
  the notebook's per-row handler.
- GRIB2 → `cfgrib` / `xarray` → numpy array → `rasterio.open(..., driver="COG", compress="DEFLATE", predictor=2, overview_levels=[2,4,8,16], blocksize=512)`.
- ODIM‑H5 radar → `wradlib.io.read_odim` → georeferenced grid → COG.
  For native BUFR products (e.g. `pg`) use `eccodes`.
- Output path under `Files/` so a Fabric Map layer can reference the
  COG directly via OneLake.
- Atomic publish: write `<name>.tif.tmp`, rename, then update
  `gold.cog_catalog (channel, product, valid_time, run, lead, file_path, bbox, crs, bytes, sha256)`
  so the map can resolve "latest".

### Eventhouse KQL functions for vector layers

```kusto
.create-or-alter function map.obs_latest() {
    dwd_events_raw
    | where type startswith "io.dwd.obs.10min."
    | summarize arg_max(ts, *) by station_id
    | join kind=inner (silver.dim_station | project station_id, lon, lat) on station_id
}

.create-or-alter function map.cap_active() {
    silver.cap_alert_area
    | where now() between (effective .. expires)
}

.create-or-alter function map.radar_latest_index() {
    gold.cog_catalog
    | where channel == "radar"
    | summarize arg_max(valid_time, *) by product
}

.create-or-alter function map.stations() {
    silver.dim_station | project station_id, name, lon, lat, state
}
```

### Example map composition

- Basemap: Azure Maps **Hybrid**.
- Imagery layer: ICON‑D2 `t_2m` COG at latest run / lead (opacity 0.6).
- Imagery layer (above): latest radar `wn` composite COG.
- Vector layer: `map.cap_active()` polygons styled by severity.
- Vector layer (top): `map.obs_latest()` points sized by precipitation.

## Recommended defaults

| Decision | Recommendation |
|---|---|
| Eventstream destinations | Eventhouse `_cloudevents_dispatch` (mandatory) + Activator (optional, for selective fast-path triggering) |
| Notebook layout | One scheduled notebook (`dwd_ingest`) that classifies events by `type` and dispatches per channel; shared helpers via `%run` |
| Radar silver | Metadata-only in v1; per‑pixel materialization on demand |
| ICON‑D2 parameters to render as COG (v1) | `t_2m`, `tot_prec`, `td_2m`, `u_10m`, `v_10m`, `ww` |
| COG projection | **EPSG:3857** (Web Mercator, native to Azure Maps) |
| Gold COG retention | Radar 7 days; ICON‑D2 last 4 runs (rolling) |

## Related Microsoft Learn docs

- [Eventstream definition template](https://github.com/microsoft/fabric-event-streams/blob/main/API%20Templates/eventstream-definition.json) (authoritative source for valid destination types)
- [Activator (Reflex) overview](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/data-activator-introduction)
- [Activator: run a Fabric item](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/data-activator-trigger-fabric-items)
- [Fabric Maps layers](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/map/about-layers)
- [Apache Spark in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute)
- [Use Microsoft Fabric Notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)
