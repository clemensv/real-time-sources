# Microsoft Planetary Computer STAC API

- **Country/Region**: Global (Microsoft Azure)
- **Endpoint**: `https://planetarycomputer.microsoft.com/api/stac/v1/`
- **Protocol**: STAC 1.0.0 (SpatioTemporal Asset Catalog)
- **Auth**: None (free tier); Azure auth for private data
- **Format**: JSON, GeoTIFF, COG, Zarr, NetCDF (varies by collection)
- **Freshness**: Hours to days (Landsat 8/9 NRT ~12h, Sentinel-2 L2A ~1-3d, GOES ~hourly)
- **Docs**: https://planetarycomputer.microsoft.com/docs/overview/about
- **Score**: 16/18

## Overview

The Microsoft Planetary Computer is a cloud-native geospatial platform hosting petabytes of open Earth observation data on Azure. The STAC API aggregates 50+ collections including Landsat Collection 2, Sentinel-1/2, MODIS, VIIRS, ASTER, GOES-16/17, Copernicus DEM, ESA WorldCover, NAIP, and derived products like ALOS World 3D and HydroSHEDS. All imagery is cloud-optimized (COG/Zarr), indexed in a queryable STAC catalog, and available for free via the Data API.

The platform is designed for analytics at scale — Python SDK (`pystac-client`, `planetary-computer`), Jupyter notebooks, Dask integration, and Azure compute co-location. Data freshness varies: GOES is near-real-time (hourly), Landsat 8/9 NRT arrives within 12 hours, Sentinel-2 L2A typically 1-3 days. This is the **de facto standard for cloud-based multi-mission EO access** in the Azure ecosystem.

Key collections for NRT monitoring:
- **Landsat 8/9 Level-2 Collection 2** — 30m optical, 16-day repeat (NRT scenes ~12h latency)
- **Sentinel-2 L2A** — 10-20m multispectral, 5-day revisit (~1-3d latency)
- **Sentinel-1 GRD** — C-band SAR, all-weather, ~3-day latency
- **GOES-16/17** — Geostationary weather imagery, 10-60min cadence
- **MODIS/VIIRS** — Daily global composites, atmosphere/ocean/land products
- **HLS (Harmonized Landsat Sentinel-2)** — NASA's 30m daily surface reflectance composite
- **Sentinel-3 OLCI/SLSTR** — Ocean color, SST, fire radiative power
- **ESA WorldCover 10m** — Annual land cover (static baseline, not NRT)

## Endpoint Analysis

**STAC API verified** — the root endpoint returns a fully compliant STAC 1.0.0 catalog with search, collections, queryables, and OGC Features conformance.

Collections endpoint tested:
```
GET https://planetarycomputer.microsoft.com/api/stac/v1/collections
```

Returns 50+ collections with full metadata (temporal extent, spatial extent, assets, providers, license).

**Example: Query recent Landsat 8 scenes over Australia**
```bash
curl -X POST "https://planetarycomputer.microsoft.com/api/stac/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "collections": ["landsat-c2-l2"],
    "bbox": [115, -35, 155, -10],
    "datetime": "2024-01-01T00:00:00Z/..",
    "limit": 10
  }'
```

Returns GeoJSON FeatureCollection with STAC items. Each item includes:
- `id`: Landsat scene ID (e.g., `LC08_L2SP_090084_20240115_02_T1`)
- `geometry`: Scene footprint (GeoJSON Polygon)
- `properties.datetime`: Acquisition timestamp (ISO 8601)
- `properties.eo:cloud_cover`: Cloud percentage
- `properties.platform`: `landsat-8` or `landsat-9`
- `assets`: COG links for all bands (coastal, blue, green, red, NIR, SWIR, thermal, QA)

All assets are **cloud-optimized GeoTIFFs (COG)** accessible via HTTP range requests — no need to download full scenes.

**Authentication**: The STAC catalog is **fully open** (no auth). Individual asset URLs require a SAS token for blob storage access, which can be obtained via:
```python
from planetary_computer import sign_url
signed_url = sign_url(item.assets["red"].href)
```

The Python SDK (`planetary-computer`) handles signing transparently. SAS tokens are **free for public data** — no Azure subscription required.

**Data access patterns**:
1. **STAC search** → filter by time, bbox, cloud cover, platform
2. **Asset retrieval** → COG subset via GDAL VSI or `rasterio.open(signed_url)`
3. **Batch processing** → Dask + `odc-stac` for parallel chunk reads
4. **OGC services** → The Data API also exposes Tile and Map endpoints (WMTS-like)

## Schema/Sample

**STAC Item structure** (Landsat 8 L2 example):
```json
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "LC08_L2SP_090084_20240115_02_T1",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[...]]
  },
  "bbox": [115.5, -32.1, 118.2, -30.0],
  "properties": {
    "datetime": "2024-01-15T02:15:43.123Z",
    "platform": "landsat-8",
    "instruments": ["oli", "tirs"],
    "eo:cloud_cover": 12.4,
    "landsat:wrs_path": "090",
    "landsat:wrs_row": "084",
    "landsat:collection_category": "T1",
    "landsat:collection_number": "02",
    "proj:epsg": 32750,
    "view:sun_azimuth": 98.5,
    "view:sun_elevation": 58.2
  },
  "assets": {
    "coastal": {
      "href": "https://landsateuwest.blob.core.windows.net/.../B1.TIF",
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": ["data"],
      "eo:bands": [{"name": "coastal", "common_name": "coastal"}]
    },
    "red": {
      "href": "https://landsateuwest.blob.core.windows.net/.../B4.TIF",
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": ["data"],
      "eo:bands": [{"name": "red", "common_name": "red"}]
    },
    "qa_pixel": {
      "href": "https://landsateuwest.blob.core.windows.net/.../QA_PIXEL.TIF",
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": ["cloud", "cloud-shadow", "snow-ice", "water-mask"]
    }
  },
  "links": [
    {"rel": "self", "href": "..."},
    {"rel": "collection", "href": "..."}
  ]
}
```

**Stable identifiers**: Landsat scene IDs are globally unique and stable. Key structure: `{platform}_{processing_level}_{path}_{row}_{acquisition_date}_{collection}_{category}`

## Why Strong

1. **Multi-mission NRT consolidation** — Landsat, Sentinel, GOES, MODIS/VIIRS all queryable via a single STAC endpoint. Eliminates the need to maintain 5+ separate upstream integrations.
2. **Cloud-native substrate** — COG/Zarr assets, HTTP range requests, Dask-friendly chunking. The repo's Kafka bridge can fetch pixel subsets without downloading full scenes.
3. **Free and fully open** — No API keys, no rate limits, no commercial restrictions. The SAS token mechanism is transparent and automatable.
4. **Battle-tested at scale** — Microsoft runs this for Azure sustainability and AI workloads. Uptime is institutional-grade.
5. **Harmonized metadata** — STAC extensions (eo, projection, view, SAR, scientific) normalize heterogeneous missions into a consistent schema. Perfect fit for xRegistry message groups.
6. **Python-first tooling** — `pystac-client`, `planetary-computer`, `odc-stac` integrate seamlessly with the repo's existing stack.

The key limitation is **latency** — this is a cloud aggregator, not the ground segment. Landsat NRT (~12h) and Sentinel-2 L2A (~1-3d) are slower than direct USGS/ESA feeds. But the **coverage breadth** (50+ collections, harmonized access) makes this a single integration that unlocks dozens of missions.

**This is the cloud-era equivalent of the EarthData login wall going away** — open STAC, no auth, multi-PB catalog.

## Limitations

- **Not truly real-time** — Landsat NRT is ~12h, Sentinel-2 L2A is 1-3 days. Direct ground segment feeds (USGS Landsat RT, ESA Sentinel Hub) are faster.
- **No L1 or raw data** — Only analysis-ready data (L2 atmospherically corrected). If the repo needs raw DN values or L1C, this won't work.
- **SAS token complexity** — While free, the token signing step adds a dependency on the `planetary-computer` Python package. Could break if Microsoft changes the signing API.
- **Azure-centric** — Data is hosted in Azure West Europe and West US. Egress from AWS or GCP incurs cross-cloud transfer costs (though STAC metadata queries are free).
- **No push notifications** — STAC is pull-only. The bridge must poll `/search` with `datetime` filters to discover new scenes. No SNS/webhook for new arrivals.
- **HLS collection is static** — Despite being a "daily" product, the HLS catalog on Planetary Computer lags weeks behind NASA's live CMR feed.

## Integration Notes

**Recommended bridge pattern**: **Multi-collection poller** (one bridge, multiple message groups)

1. **Collection enumeration** — The bridge config declares a list of target collections (`landsat-c2-l2`, `sentinel-2-l2a`, `goes-16`, etc.) and AOIs.
2. **Polling loop** — Every N minutes, query `/search` for each collection with `datetime=lastPollTime/..` and a bbox or global coverage.
3. **Delta detection** — Track `item.id` in persistent state (SQLite or Kafka compacted topic). Emit only unseen scenes.
4. **Message groups** — One xreg message group per collection family:
   - `landsat_scenes` — keyed by `{platform}/{path}/{row}/{date}` (WRS-2 grid cell + date)
   - `sentinel2_tiles` — keyed by `{tile_id}/{date}` (MGRS tile)
   - `goes_frames` — keyed by `{satellite}/{channel}/{scan_time}`
5. **Asset selection** — The CloudEvent payload includes scene metadata + asset HREFs. Downstream consumers fetch COG subsets as needed.
6. **Reference data** — STAC collections themselves (static metadata about platform, bands, EPSG) could be emitted as reference events at startup.

**Why not just expose the STAC API directly?** Kafka adds:
- Durability (scenes persist in topic, replays possible)
- Ordering (time-series guarantees per key)
- Fan-out (multiple consumers without re-polling STAC)
- Enrichment (bridge could pre-compute cloud masks, AOI intersections, data quality scores)

**Alternative**: For **true NRT** (sub-hour), combine this with direct USGS Landsat RT (not in Planetary Computer) or ESA SciHub (already in repo scope). Use Planetary Computer for historical backfill and multi-mission coverage.

## Verdict

**STRONG ACCEPT** — This is a **Tier-1 cloud aggregator** that consolidates 50+ EO missions into a single, free, open, STAC-compliant endpoint. While not the fastest for any individual mission, the **breadth** (Landsat + Sentinel-1/2/3 + GOES + MODIS + VIIRS + DEM) and **ease of integration** (one STAC client, COG-native, Python SDK) make it a **force multiplier** for the repo.

Recommended as the **primary EO imagery source** for multi-mission coverage, with direct ground-segment feeds (USGS Landsat RT, ESA Sentinel Hub) added later for latency-critical use cases.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Multi-mission consolidation (Landsat + Sentinel + GOES + MODIS/VIIRS) |
| Freshness | 2 | Landsat NRT ~12h, Sentinel-2 ~1-3d, GOES ~hourly (not sub-minute) |
| Openness | 3 | Fully open, no API keys, free SAS tokens for public data |
| Schema clarity | 3 | STAC 1.0.0, eo/projection/view extensions, well-documented |
| Machine-readability | 3 | JSON, GeoJSON, COG, Zarr — all cloud-native formats |
| Repo fit | 2 | STAC is pull-only (poll required), but COG assets are Kafka-friendly |
