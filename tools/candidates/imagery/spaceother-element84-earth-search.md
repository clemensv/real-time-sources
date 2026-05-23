# Element84 Earth Search STAC API

- **Country/Region**: Global (AWS us-west-2)
- **Endpoint**: `https://earth-search.aws.element84.com/v1/`
- **Protocol**: STAC 1.0.0 (SpatioTemporal Asset Catalog)
- **Auth**: None (fully open)
- **Format**: JSON, GeoTIFF (COG)
- **Freshness**: Hours to days (Landsat Collection 2 ~12-24h, Sentinel-2 L2A/L1C ~1-3d, Sentinel-1 GRD ~3d)
- **Docs**: https://www.element84.com/earth-search/
- **Score**: 16/18

## Overview

Element84 Earth Search is an open STAC API indexing public satellite imagery on AWS (Registry of Open Data). It provides a unified query interface for Landsat Collection 2 Level-2, Sentinel-2 L2A and L1C, Sentinel-1 GRD, NAIP aerial imagery, and Copernicus DEM. All assets are **cloud-optimized GeoTIFFs (COG)** hosted in AWS S3 public buckets — no authentication required.

This is the **AWS-native counterpart** to Microsoft Planetary Computer STAC. While Planetary Computer is broader (50+ collections), Earth Search focuses on the **core optical + SAR missions** (Landsat, Sentinel-1/2) with excellent data freshness and AWS co-location. It's the default STAC endpoint for AWS-based EO workflows and is maintained by Element84 (the company behind stac-server and FilmDrop).

Key collections:
- **landsat-c2-l2** — Landsat 8/9 Level-2 surface reflectance (30m, 16-day repeat, ~12-24h latency)
- **sentinel-2-l2a** — Sentinel-2 L2A atmospherically corrected (10-20m, 5-day revisit, ~1-3d latency)
- **sentinel-2-l1c** — Sentinel-2 L1C top-of-atmosphere reflectance (faster than L2A, ~1-2d)
- **sentinel-1-grd** — Sentinel-1 C-band SAR Ground Range Detected (10m, all-weather, ~3d latency)
- **cop-dem-glo-30** — Copernicus DEM 30m global (static baseline)
- **naip** — USDA National Agriculture Imagery Program (US only, 60cm, annual updates)

## Endpoint Analysis

**STAC API verified** — the root endpoint returns a fully compliant STAC 1.0.0 catalog with 9 collections.

Collections tested:
```
GET https://earth-search.aws.element84.com/v1/collections
```

Returns:
```json
{
  "collections": [
    {
      "id": "landsat-c2-l2",
      "title": "Landsat Collection 2 Level-2",
      "description": "Landsat Collection 2 Level-2 atmospherically corrected surface reflectance",
      "extent": {
        "spatial": {"bbox": [[-180, -90, 180, 90]]},
        "temporal": {"interval": [["2013-03-18T00:00:00Z", null]]}
      },
      "license": "proprietary",
      "providers": [...],
      "summaries": {
        "platform": ["landsat-8", "landsat-9"],
        "eo:cloud_cover": [0, 100]
      }
    },
    {
      "id": "sentinel-2-l2a",
      "title": "Sentinel-2 Level-2A",
      "extent": {
        "temporal": {"interval": [["2015-06-27T00:00:00Z", null]]}
      },
      "license": "proprietary",
      "providers": [{"name": "ESA", ...}]
    },
    {
      "id": "sentinel-1-grd",
      "title": "Sentinel-1 Level-1 Ground Range Detected (GRD)",
      "extent": {
        "temporal": {"interval": [["2014-10-10T00:00:00Z", null]]}
      }
    }
  ]
}
```

**Example: Query recent Sentinel-2 L2A over the Amazon**
```bash
curl -X POST "https://earth-search.aws.element84.com/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "collections": ["sentinel-2-l2a"],
    "bbox": [-70, -10, -60, 0],
    "datetime": "2024-01-01T00:00:00Z/..",
    "query": {
      "eo:cloud_cover": {"lt": 20}
    },
    "limit": 10
  }'
```

Returns STAC items with:
- `id`: Sentinel-2 tile ID (e.g., `S2B_20LLP_20240115_0_L2A`)
- `geometry`: Tile footprint (100×100km MGRS grid cell)
- `properties.datetime`: Acquisition timestamp
- `properties.eo:cloud_cover`: Cloud percentage (0-100)
- `properties.s2:mgrs_tile`: MGRS tile ID (e.g., `20LLP`)
- `assets`: COG links for all 10-60m bands (B01-B12, SCL, AOT, WVP)

All asset URLs point to **public S3 buckets**:
```
s3://sentinel-cogs/sentinel-s2-l2a-cogs/20/L/LP/2024/1/S2B_20LLP_20240115_0_L2A/B04.tif
```

**No authentication required** — assets are publicly readable. HTTP access works via:
```
https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/...
```

**Data access patterns**:
1. **STAC search** → filter by collection, time, bbox, cloud cover, platform
2. **COG retrieval** → `rasterio.open()` or GDAL `/vsicurl/` for HTTP range reads
3. **Batch processing** → `odc-stac` or `stackstac` for xarray-based chunk processing

## Schema/Sample

**STAC Item structure** (Sentinel-2 L2A example):
```json
{
  "type": "Feature",
  "stac_version": "1.0.0",
  "id": "S2B_20LLP_20240115_0_L2A",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[-70.5, -5.1], [-69.4, -5.1], [-69.4, -4.0], [-70.5, -4.0], [-70.5, -5.1]]]
  },
  "bbox": [-70.5, -5.1, -69.4, -4.0],
  "properties": {
    "datetime": "2024-01-15T14:23:41Z",
    "platform": "sentinel-2b",
    "constellation": "sentinel-2",
    "instruments": ["msi"],
    "eo:cloud_cover": 8.3,
    "s2:mgrs_tile": "20LLP",
    "s2:water_percentage": 0.12,
    "s2:snow_ice_percentage": 0,
    "s2:cloud_shadow_percentage": 2.1,
    "s2:vegetation_percentage": 89.4,
    "s2:processing_baseline": "05.09",
    "proj:epsg": 32720,
    "grid:code": "MGRS-20LLP"
  },
  "assets": {
    "B04": {
      "href": "https://sentinel-cogs.s3.us-west-2.amazonaws.com/.../B04.tif",
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": ["data"],
      "gsd": 10,
      "eo:bands": [{"name": "B04", "common_name": "red", "center_wavelength": 0.665}]
    },
    "SCL": {
      "href": "https://sentinel-cogs.s3.us-west-2.amazonaws.com/.../SCL.tif",
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": ["data"],
      "gsd": 20,
      "title": "Scene Classification Map"
    }
  }
}
```

**Stable identifiers**: Sentinel-2 uses MGRS tile IDs (e.g., `20LLP`) which are globally unique grid cells. Landsat uses WRS-2 path/row. Both are stable and suitable for Kafka keys.

**Key structure for xreg**:
- Landsat: `{platform}/{path}/{row}/{date}` (e.g., `landsat-8/090/084/2024-01-15`)
- Sentinel-2: `{tile_id}/{date}` (e.g., `20LLP/2024-01-15`)
- Sentinel-1: `{mode}/{polarization}/{orbit}/{date}` (e.g., `IW/VV/12345/2024-01-15`)

## Why Strong

1. **AWS-native** — Data is in `us-west-2`, perfect for AWS Lambda/Batch/Fargate bridges. No cross-cloud egress costs.
2. **Core missions only** — Focuses on Landsat + Sentinel-1/2, the **workhorses of operational EO**. No clutter from experimental or static datasets.
3. **Fully open** — No API keys, no SAS tokens, no auth dance. Public S3 buckets are directly accessible.
4. **Fast updates** — Sentinel-2 L1C appears in 1-2 days, L2A in 1-3 days. Landsat C2L2 in 12-24 hours. Competitive with ground-segment portals.
5. **Battle-tested** — Element84 runs this for AWS Public Dataset Program. Uptime is institutional-grade.
6. **STAC 1.0.0 native** — Clean, standard-compliant API. No vendor lock-in.

The **key advantage over Planetary Computer** is **AWS co-location** and **simpler auth** (no SAS tokens). For AWS-hosted bridges, this is the natural choice.

## Limitations

- **Narrower collection set** — Only 9 collections vs. 50+ on Planetary Computer. No GOES, MODIS/VIIRS, HLS, or derived products.
- **No NRT geostationary** — GOES/Himawari are missing. For sub-hourly imagery, need a separate source.
- **Sentinel-1 GRD only** — No SLC (Single Look Complex) data. If the repo needs interferometry or polarimetric decomposition, this won't work.
- **License confusion** — Collections are marked `"license": "proprietary"` in STAC metadata, but Landsat/Sentinel are actually public domain (US govt) or CC BY-SA (ESA). This is a metadata bug, not a real restriction.
- **No push notifications** — STAC is pull-only. Bridge must poll `/search` for new scenes.
- **US-centric collections** — NAIP (US aerial imagery) and Copernicus DEM are included, but most other regions lack high-resolution basemaps.

## Integration Notes

**Recommended bridge pattern**: **Multi-collection poller** (same as Planetary Computer)

1. **Collection config** — Bridge declares target collections (`landsat-c2-l2`, `sentinel-2-l2a`, `sentinel-1-grd`) and AOIs.
2. **Polling loop** — Every 15-30 minutes, query `/search` with `datetime=lastPoll/..` and collection filter.
3. **Delta detection** — Track `item.id` in SQLite or Kafka compacted topic. Emit only new scenes.
4. **Message groups** — One per collection family:
   - `landsat_scenes` — keyed by `{platform}/{path}/{row}/{date}`
   - `sentinel2_tiles` — keyed by `{tile}/{date}`
   - `sentinel1_scenes` — keyed by `{mode}/{orbit}/{date}`
5. **Asset metadata** — CloudEvent payload includes scene metadata + COG HREFs. Downstream consumers fetch subsets as needed.
6. **Reference data** — Emit STAC collection metadata (platform, bands, EPSG, coverage) as reference events at startup.

**Why not just expose STAC directly?** Kafka adds:
- **Durability** — Scenes persist in topic, historical replays possible
- **Ordering** — Time-series guarantees per WRS-2 cell or MGRS tile
- **Fan-out** — Multiple consumers without re-polling STAC
- **Enrichment** — Bridge could pre-compute AOI intersections, cloud masks, data quality flags

**Alternative deployment**: For **AWS Lambda**, fetch scenes on-demand via STAC `/search` triggered by S3 SNS notifications (if AWS exposes them for Registry of Open Data buckets). But as of 2024, there's no public SNS topic for Landsat/Sentinel arrivals — polling is required.

## Verdict

**STRONG ACCEPT** — This is the **AWS-native Tier-1 STAC aggregator** for Landsat + Sentinel-1/2. Simpler auth than Planetary Computer (no SAS tokens), excellent data freshness (1-3 days for Sentinel-2 L2A), and perfect AWS co-location. The narrower collection set is actually a feature — focuses on the core optical + SAR missions without clutter.

Recommended as the **primary imagery source for AWS-hosted bridges**. If the bridge runs in Azure, use Planetary Computer instead. If multi-cloud or on-prem, **use both** (Landsat/Sentinel-2 from Earth Search, GOES/MODIS/VIIRS from Planetary Computer).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Landsat 8/9 + Sentinel-1/2 consolidation in one STAC endpoint |
| Freshness | 3 | Landsat ~12-24h, Sentinel-2 L2A ~1-3d, L1C ~1-2d, Sentinel-1 ~3d |
| Openness | 3 | Fully open, public S3 buckets, no auth required |
| Schema clarity | 3 | STAC 1.0.0, eo/projection/SAR extensions, clean metadata |
| Machine-readability | 3 | JSON, GeoJSON, COG — all cloud-native |
| Repo fit | 1 | STAC is pull-only (poll required), but excellent for AWS bridges |
