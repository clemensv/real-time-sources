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
DWD bridge ──Kafka / Event Hub──▶ Fabric Eventstream "dwd-stream"
                                          │
                ┌─────────────────────────┼─────────────────────────────┐
                ▼                         ▼                             ▼
        Eventhouse table         Spark Notebook destination     Lakehouse Delta sink
        dwd_events_raw           dwd_ingest  (preview)         (optional, for inline
        (audit / KQL)            Structured Streaming job       channels only)
                                          │
                                          ▼
                          ┌───────────────┴────────────────┐
                          ▼                                ▼
                Files/bronze/<channel>/...     Tables/silver.*    Files/gold/*_cog/...
                (raw upstream bytes)           (parsed Delta)      (Cloud Optimized
                                                                    GeoTIFF for maps)
```

The Eventstream **Spark Notebook destination** (preview, Dec 2025)
runs a notebook as a continuous Structured Streaming job that consumes
the stream directly — no Activator / Pipeline hop is required. See
[Add a Spark Notebook destination to an
Eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-destination-spark-notebook).

## Why streaming, not per‑event triggering

ICON‑D2 emits thousands of file‑reference events per 3‑hour model cycle.
A per‑event Activator → Pipeline → Notebook fan‑out would saturate
capacity and pay cold‑start cost per file. A single long‑running
streaming notebook with `foreachBatch` and bounded HTTP concurrency
fetches efficiently and respects DWD usage guidance.

## Eventstream wiring

1. Create an Eventstream `dwd-stream` with a **Custom Endpoint** source
   bound to the bridge's Kafka topic `dwd` (or to an Event Hub the
   bridge writes to).
2. Add two destinations:
   - **Eventhouse table** `dwd_events_raw` — raw event log for KQL
     exploration, replay, and as the source for vector map layers.
   - **Spark Notebook** `dwd_ingest` — the streaming worker described
     below.
3. Optional: a no‑code Event Processor stage that splits by `type`
   into per‑family streams if you prefer one notebook per family
   instead of a single router.

## Per‑channel pipeline

| Channel | Event payload | Fetch needed? | Bronze layout (`Files/`) | Silver Delta (`Tables/`) | Decoder |
|---|---|---|---|---|---|
| 10‑min observations | Inline rows | No | optional raw JSON for replay | `silver.obs_10min` partitioned by `station_id`, `date(ts)` | already parsed by bridge |
| Station metadata | Inline | No | — | `silver.dim_station` (SCD‑1, MERGE on `station_id`) | already parsed |
| CAP alerts | Inline parsed + raw XML | No | `Files/bronze/cap/yyyy=…/mm=…/dd=…/<msgId>.xml` (audit copy) | `silver.cap_alert` + `silver.cap_alert_area` | already parsed |
| Radar composite | `file_url` + product metadata | **Yes** | `Files/bronze/radar/<product>/yyyy=…/mm=…/dd=…/HH/<file_name>` | `silver.radar_product` (metadata only in v1) | `h5py` / `wradlib` for ODIM‑H5; `eccodes` / `pdbufr` for BUFR |
| ICON‑D2 forecast | `file_url` + run/lead/level/param | **Yes** | `Files/bronze/icon-d2/run=YYYYMMDDHH/lead=NNN/<param>/<level_type>/<file_name>` | `silver.icon_d2_file` (parsed GRIB headers) | `cfgrib` (xarray) or `pygrib`; bz2 streamed via `bz2.open` |

### Streaming notebook skeleton

```python
from concurrent.futures import ThreadPoolExecutor

stream = spark.readStream.format("eventstream").load()

def fetch_and_land(row):
    # 1) anonymous HTTPS GET of row.file_url with If-None-Match
    # 2) write bytes to Files/bronze/<channel>/...  (atomic .tmp + rename)
    # 3) compute sha256 + size; decode headers for silver row
    # 4) optionally render a Cloud Optimized GeoTIFF into Files/gold/...
    ...

def process_batch(df, epoch_id):
    rows = df.filter("type LIKE 'io.dwd.icon-d2.%'").collect()
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(fetch_and_land, rows))
    silver_df = spark.createDataFrame(results)
    (silver_df.write.format("delta").mode("append")
        .partitionBy("run", "parameter")
        .saveAsTable("silver.icon_d2_file"))

(stream.writeStream
   .foreachBatch(process_batch)
   .option("checkpointLocation", "Files/_checkpoints/icon_d2")
   .trigger(processingTime="30 seconds")
   .start())
```

### Idempotency & state

- Natural key: `file_url` + upstream `Last-Modified` / `ETag`.
- Silver tables use `MERGE INTO` on that key so retries and replays
  don't duplicate.
- Streaming checkpoint at `Files/_checkpoints/<channel>/` gives
  exactly‑once semantics relative to the Eventstream offset.
- Bronze writes are atomic (`.tmp` then rename) and skipped when the
  target exists with matching size + sha256.

### Scale & throttling

- Bounded `ThreadPoolExecutor` per batch (≈16 workers for ICON‑D2,
  fewer for radar where individual files can be ~10 MB).
- Backpressure via `trigger(processingTime=…)`.
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
  the streaming notebook's `foreachBatch`.
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
| Eventstream destinations | Eventhouse `dwd_events_raw` **and** Spark Notebook `dwd_ingest` |
| Notebook layout | One streaming notebook per channel family; shared helpers via `%run` |
| Radar silver | Metadata-only in v1; per‑pixel materialization on demand |
| ICON‑D2 parameters to render as COG (v1) | `t_2m`, `tot_prec`, `td_2m`, `u_10m`, `v_10m`, `ww` |
| COG projection | **EPSG:3857** (Web Mercator, native to Azure Maps) |
| Gold COG retention | Radar 7 days; ICON‑D2 last 4 runs (rolling) |

## Related Microsoft Learn docs

- [Add a Spark Notebook destination to an Eventstream (preview)](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/add-destination-spark-notebook)
- [Fabric Maps layers](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/map/about-layers)
- [Apache Spark in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute)
- [Use Microsoft Fabric Notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)
