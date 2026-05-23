# USGS Landsat Collection 2 Near-Real-Time (NRT)

- **Country/Region**: Global
- **Endpoint**: `https://landsatlook.usgs.gov/stac-server` (LandsatLook STAC), `https://m2m.cr.usgs.gov/api/` (M2M API)
- **Protocol**: STAC 1.0.0 (LandsatLook), JSON-RPC 2.0 (M2M)
- **Auth**: Free USGS EarthExplorer account for M2M, no auth for LandsatLook STAC
- **Format**: GeoTIFF (COG), HDF, tar.gz (Collection 2 bundles)
- **Freshness**: Near-real-time (~12 hours for NRT Tier 1, 3-5 days for standard processing)
- **Docs**: https://www.usgs.gov/landsat-missions, https://landsatlook.usgs.gov/stac-browser
- **Score**: 14/18

## Overview

The USGS Landsat program provides **global 30m multispectral imagery** from Landsat 8 (2013-present) and Landsat 9 (2021-present). **Collection 2** is the latest processing baseline with improved geometric accuracy, radiometric calibration, and cloud/shadow masking.

**Landsat NRT** (Near-Real-Time) products appear **within 12 hours** of acquisition for Tier 1 scenes (best geometric quality). Standard Collection 2 processing (Level-2 atmospherically corrected surface reflectance) completes within 3-5 days.

USGS distributes Landsat via:
1. **LandsatLook STAC** — STAC 1.0.0 catalog (metadata only, no direct download)
2. **M2M API** — Machine-to-Machine JSON-RPC API (search + bulk download)
3. **AWS Open Data** — Public S3 buckets (Collection 2, indexed by Element84 Earth Search)

The **LandsatLook STAC** is the newest interface (2023), providing a **standards-compliant** STAC catalog for Collection 2.

**Key products**:
- **Landsat 8/9 Level-1** — Top-of-atmosphere reflectance + thermal, ~12h NRT
- **Landsat 8/9 Level-2** — Surface reflectance + surface temperature, 3-5 days
- **Analysis Ready Data (ARD)** — Tiled products (5000x5000 pixels, Albers Equal Area), annual mosaics

## Endpoint Analysis

**LandsatLook STAC verified** — `https://landsatlook.usgs.gov/stac-server`

Tested:
```
GET https://landsatlook.usgs.gov/stac-server
```

Returns STAC 1.0.0 catalog with collections:
- `landsat-c2l1` — Collection 2 Level-1 (Landsat 4/5/7/8/9)
- `landsat-c2l2-sr` — Collection 2 Level-2 Surface Reflectance (Landsat 4/5/7/8/9)
- `landsat-c2l2-st` — Collection 2 Level-2 Surface Temperature (Landsat 4/5/7/8/9)

**Example: Query recent Landsat 9 Level-2 over California**
```bash
curl -X POST "https://landsatlook.usgs.gov/stac-server/search" \
  -H "Content-Type: application/json" \
  -d '{
    "collections": ["landsat-c2l2-sr"],
    "bbox": [-124, 32, -114, 42],
    "datetime": "2024-01-01T00:00:00Z/..",
    "query": {
      "eo:cloud_cover": {"lt": 20},
      "platform": {"eq": "LANDSAT_9"}
    },
    "limit": 10
  }'
```

Returns STAC items with:
- `id`: Landsat scene ID (e.g., `LC09_L2SP_042035_20240115_20240119_02_T1`)
- `geometry`: Scene footprint (WRS-2 path/row grid cell, ~185×180 km)
- `properties.datetime`: Acquisition timestamp
- `properties.eo:cloud_cover`: Cloud percentage
- `properties.landsat:wrs_path` / `landsat:wrs_row`: WRS-2 grid coordinates (path 042, row 035)
- `properties.landsat:collection_category`: Tier 1 (best quality) or Tier 2
- `assets`: Links to all bands, QA masks, metadata

**Asset access**:
- **LandsatLook STAC** — Metadata only (no direct download links in assets)
- **M2M API** — Download URLs available after order submission (requires account)
- **AWS Open Data** — Public S3 buckets, indexed by **Element84 Earth Search** (better option)

**Stable identifiers**: Landsat scene IDs are globally unique (e.g., `LC09_L2SP_042035_20240115_20240119_02_T1`). Keyed by `{platform}/{path}/{row}/{date}`.

## Why Strong

1. **Official USGS source** — Authoritative for Landsat data (joint NASA/USGS program).
2. **NRT latency** — Level-1 appears within ~12 hours (competitive with Sentinel-2).
3. **STAC 1.0.0** — LandsatLook STAC is modern, standards-compliant.
4. **Free and open** — Public domain (US government work), no restrictions.
5. **Historical archive** — Landsat 4/5/7/8/9 (1982-present), longest continuous EO record.

## Limitations

- **LandsatLook STAC has no download links** — Assets point to placeholder URLs. Must use M2M API or AWS S3 for downloads.
- **M2M API requires account** — Free but registration + API key management required.
- **Lower resolution than Sentinel-2** — 30m vs. 10m (Sentinel-2 is 3× higher resolution).
- **Longer revisit** — 16 days (Landsat 8+9 combined: 8 days) vs. 5 days (Sentinel-2 A+B).
- **AWS Open Data is faster** — Element84 Earth Search indexes AWS Landsat buckets and provides direct COG download URLs. Better option than LandsatLook STAC.

## Integration Notes

**Recommended**: Use **Element84 Earth Search** instead of LandsatLook STAC or M2M API. Earth Search provides:
- **STAC 1.0.0** with direct COG download URLs (no M2M account required)
- **Public S3 buckets** (no auth)
- **Faster metadata updates** (Earth Search is optimized for cloud-native access)

LandsatLook STAC is **metadata-only** (no download links). M2M API requires **order submission** workflow (async, not real-time).

**If using LandsatLook STAC**:
1. Query STAC for scene metadata
2. Extract scene ID
3. Call M2M API to order download (`downloadOptions`, `downloadRequest`)
4. Poll M2M API for download URL (async job)
5. Download tar.gz bundle from USGS

**If using Element84 Earth Search** (recommended):
1. Query STAC `/search` with `collections=landsat-c2-l2`
2. Extract `assets` with COG URLs (e.g., `https://landsateuwest.blob.core.windows.net/.../B4.TIF`)
3. Download COG directly (no account required)

## Verdict

**CONDITIONAL ACCEPT** — LandsatLook STAC is the **official USGS STAC catalog**, but it's **metadata-only** (no download links). For **actual data access**, use **Element84 Earth Search** (covered separately), which indexes the same Landsat Collection 2 data via AWS S3 with direct COG download URLs.

**Recommended**: Skip LandsatLook STAC, use **Element84 Earth Search** for Landsat Collection 2. Earth Search is **better** (STAC + COG downloads, no auth, faster).

LandsatLook STAC is useful **only if**:
- You need the **official USGS metadata** (Earth Search may have minor schema differences)
- You're already using M2M API for bulk orders (integrated workflow)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Landsat 8/9 Level-1 + Level-2, NRT (~12h) + standard (3-5d) |
| Freshness | 2 | NRT Level-1 ~12h, Level-2 ~3-5d (slower than Sentinel-2) |
| Openness | 3 | Fully open, public domain (US govt), no restrictions |
| Schema clarity | 3 | STAC 1.0.0, well-documented Landsat metadata |
| Machine-readability | 2 | STAC metadata only (no download links, must use M2M or AWS) |
| Repo fit | 1 | Metadata-only STAC, use Element84 Earth Search instead |
