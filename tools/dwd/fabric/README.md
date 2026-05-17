# DWD Fabric Extension

This directory **extends** the basic per-source Fabric setup produced by
[`tools/deploy-fabric/deploy-fabric.ps1`](../../deploy-fabric/README.md) with
DWD-specific KQL assets, a Spark Structured Streaming notebook
(`dwd_ingest`) and a Spark Notebook destination on the eventstream so
the file-reference events can be expanded into Lakehouse bronze bytes,
silver Delta rows and gold Cloud Optimized GeoTIFFs ready for
[Fabric Maps](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/map/about-layers).

## What the basic setup gives you

Running `tools/deploy-fabric/deploy-fabric.ps1 -Source dwd ...` already
deploys:

- An Azure Container Instance running the `dwd` bridge.
- An Event Hub + Eventstream (`dwd-ingest`) consuming it.
- A KQL database (default name `dwd`) in your Eventhouse with the
  generic `_cloudevents_dispatch` landing table receiving every DWD
  CloudEvent.

This DWD extension is what you run **next**.

## What this extension adds

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Eventstream  dwd-ingest                                                    │
│   ├─ source       dwd-input  (Custom Endpoint, populated by basic setup)    │
│   ├─ stream       dwd-ingest-stream                                          │
│   ├─ destination  dispatch-kql      ── _cloudevents_dispatch (basic)        │
│   └─ destination  dwd-ingest-notebook  ── Spark Notebook  (added here)      │
└──────────────────┬──────────────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  KQL database  dwd                                                          │
│   _cloudevents_dispatch                       (basic)                       │
│   StationMetadata + Latest                                                  │
│   AirTemperature10Min  / Precipitation10Min  / Wind10Min  / Solar10Min      │
│   ExtremeWind10Min  / ExtremeTemperature10Min  / HourlyObservation          │
│   WeatherAlert  + Latest                                                    │
│   RadarProductCatalog  / RadarFileProduct                                   │
│   ForecastModelCatalog / IconD2ForecastFile                                 │
│   CogCatalog            (gold tier, written by dwd_ingest notebook)         │
│   Functions:  map_stations, map_obs_latest, map_cap_active,                 │
│               map_radar_latest_index, map_icon_d2_latest_index              │
└──────────────────┬──────────────────────────────────────────────────────────┘
                   │
                   ▼ (Spark Structured Streaming, foreachBatch)
┌─────────────────────────────────────────────────────────────────────────────┐
│  Lakehouse                                                                  │
│   Files/bronze/radar/<product>/yyyy=…/mm=…/dd=…/HH=…/<file>                 │
│   Files/bronze/icon-d2/run=…/lead=…/<param>/<level_type>/<level>/<file>     │
│   Files/gold/radar_cog/...   (Cloud Optimized GeoTIFF, EPSG:3857)           │
│   Files/gold/icon-d2_cog/... (Cloud Optimized GeoTIFF, EPSG:3857)           │
│   Files/_checkpoints/dwd_ingest/  (streaming checkpoint)                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Files in this directory

| File | Description |
|---|---|
| `dwd.kql` | Typed tables (one per `DE.DWD.*` CloudEvents type) with update policies fanning out of `_cloudevents_dispatch`, materialized "Latest" views, the gold `CogCatalog` table, and the `map_*` KQL functions used as Fabric Maps vector layer sources. |
| `setup.ps1` | Applies `dwd.kql`, builds + uploads `dwd_ingest.ipynb` via the shared `tools/deploy-fabric/deploy-fabric-notebook.ps1`, and adds the notebook as a Spark Notebook destination on the existing `dwd-ingest` eventstream (preview). |
| `notebook/build_notebook.py` | Programmatic builder for the `dwd_ingest` notebook (regeneration source of truth). |
| `notebook/dwd_ingest.ipynb` | Generated streaming notebook. Drains the eventstream, fetches `file_url` for radar + ICON-D2 events, writes bronze bytes, renders selected fields to COG, and ingests `CogCatalog` rows. |

## Prerequisites

- `tools/deploy-fabric/deploy-fabric.ps1 -Source dwd ...` has already run
  successfully in the target workspace.
- A **Lakehouse** exists in the workspace (any name — `setup.ps1` picks the
  first one or accepts `-LakehouseName`).
- A **Fabric Environment** (recommended) attached to the workspace with
  the GIS decoders installed: `cfgrib`, `eccodes`, `h5py`, `rasterio`,
  `rio-cogeo`. Without these the notebook still lands bronze bytes but
  skips COG rendering.
- Azure CLI is logged in (`az login`) with rights to call the Fabric REST API.

## Usage

```powershell
./setup.ps1 `
    -WorkspaceId  "c98acd97-4363-4296-8323-b6ab21e53903" `
    -EventhouseId "dbfd2819-2879-4ae7-bff2-95619ad7b8e7"
```

After `setup.ps1` finishes, open the `dwd-ingest` Eventstream in the
Fabric portal and **Publish** so the new Spark Notebook destination starts
its Structured Streaming job. Open the `dwd_ingest` notebook to see
batch-by-batch progress in the cell output.

To re-apply KQL only (e.g. after editing `dwd.kql`):

```powershell
./setup.ps1 -WorkspaceId ... -EventhouseId ... -SkipNotebook
```

To regenerate the notebook from source without uploading:

```powershell
python notebook/build_notebook.py
```

## Example queries

```kusto
// Latest air temperature per station (input for map_obs_latest layer).
AirTemperature10MinLatest
| top 20 by timestamp desc

// Active CAP alerts (input for map_cap_active layer).
map_cap_active()
| project identifier, severity, headline, area_desc, expires

// Newest radar composite COG path per product (drives a Fabric Maps imagery layer).
map_radar_latest_index()
| project product, valid_time, cog_path, bbox

// Newest ICON-D2 t_2m COG at any pressure / level.
map_icon_d2_latest_index("t_2m", "single-level", "2")
```

## Fabric Maps composition (example)

Build a Fabric Map with these layers (bottom → top):

1. **Basemap** — Azure Maps **Hybrid**.
2. **Imagery layer** — ICON-D2 `t_2m` COG. Source = OneLake file at
   `map_icon_d2_latest_index("t_2m", "single-level", "2") | project cog_path`,
   opacity 0.6.
3. **Imagery layer** — latest radar `wn` composite COG.
   Source = `map_radar_latest_index() | where product == "wn"`.
4. **Vector layer (polygons)** — `map_cap_active()` styled by `severity`.
5. **Vector layer (points)** — `map_obs_latest()` sized by `precipitation_height`.

See `dwd/FABRIC.md` for the end-to-end design narrative and rationale.
