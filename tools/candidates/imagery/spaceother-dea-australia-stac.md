# Digital Earth Australia (DEA) - Geoscience Australia

- **Country/Region**: Australia
- **Endpoint**: `https://explorer.dea.ga.gov.au/stac/`
- **Protocol**: STAC 1.1.0, WMS, WCS, OGC API
- **Auth**: None (fully open)
- **Format**: GeoTIFF (COG), NetCDF, Zarr
- **Freshness**: Days to weeks (Landsat/Sentinel-2 ARD ~3-7d, Water Observations ~weekly, derived products monthly-annual)
- **Docs**: https://www.dea.ga.gov.au/, https://knowledge.dea.ga.gov.au/
- **Score**: 14/18

## Overview

Digital Earth Australia (DEA) is Geoscience Australia's operational Earth observation platform providing **analysis-ready data (ARD)** for the Australian continent. The STAC API indexes 100+ collections including Landsat 5/7/8/9 ARD, Sentinel-2 A/B/C ARD, Sentinel-1 gamma0, water observations (WOfS), fractional cover, intertidal elevation, mangrove extent, land cover, and coastline change products.

All data is **Australia-specific** — global coverage is not available. The platform's strength is **derived products** that are operationally maintained for Australian environmental monitoring: water extent time series, tidal composites, coastline dynamics, burned area, and fuel moisture content. These products are **unique** — not available in global STAC catalogs like Planetary Computer or Earth Search.

Key collections for NRT monitoring:
- **ga_ls8c_ard_3 / ga_ls9c_ard_3** — Landsat 8/9 ARD (NBART + observational attributes) ~3-7 day latency
- **ga_s2am_ard_3 / ga_s2bm_ard_3 / ga_s2cm_ard_3** — Sentinel-2 A/B/C ARD (NBART) ~3-7 day latency
- **ga_s2_fmc_3_v1** — Sentinel-2 Fuel Moisture Content (wildfire risk indicator) ~weekly updates
- **ga_s2_ba_provisional_3** — Sentinel-2 Burned Area (provisional) ~weekly during fire season
- **ga_ls_wo_3** — Water Observations from Space (WOfS) — Landsat-based water extent ~weekly
- **ga_s2_wo_provisional_3** — Sentinel-2 Water Observations (provisional) ~weekly
- **s1_gamma0_geotif_scene** — Sentinel-1 Gamma0 backscatter (SAR) ~3-5 day latency

## Endpoint Analysis

**STAC API verified** — the root endpoint returns a STAC 1.1.0 catalog with 100+ collections.

Collections tested:
```
GET https://explorer.dea.ga.gov.au/stac/collections
```

Returns extensive collection list including Landsat ARD, Sentinel-2 ARD, Sentinel-1 SAR, ASTER derivatives, DEMs, land cover, water observations, fractional cover, mangrove extent, intertidal topography, and bathymetry.

**Example: Query recent Landsat 9 ARD over Sydney**
```bash
curl -X POST "https://explorer.dea.ga.gov.au/stac/search" \
  -H "Content-Type: application/json" \
  -d '{
    "collections": ["ga_ls9c_ard_3"],
    "bbox": [150.5, -34.5, 151.5, -33.5],
    "datetime": "2024-01-01T00:00:00Z/..",
    "limit": 10
  }'
```

Returns STAC items with:
- `id`: Scene ID (e.g., `ga_ls9c_ard_3-0-0_090084_2024-01-15_final`)
- `geometry`: Scene footprint (Landsat WRS-2 grid cell)
- `properties.datetime`: Acquisition timestamp
- `properties.eo:cloud_cover`: Cloud percentage
- `properties.odc:product`: `ga_ls9c_ard_3`
- `properties.landsat:wrs_path` / `landsat:wrs_row`: 090 / 084
- `assets`: COG links for NBART bands (coastal, blue, green, red, NIR, SWIR1, SWIR2), QA masks, and observational attributes (solar/view angles)

All assets are **cloud-optimized GeoTIFFs** hosted in AWS S3 (Sydney region) or DEA's own storage. Public access via HTTPS.

**Example asset URL**:
```
https://data.dea.ga.gov.au/baseline/ga_ls9c_ard_3/090/084/2024/01/15/ga_ls9c_ard_3-0-0_090084_2024-01-15_final_band04.tif
```

**Data access patterns**:
1. **STAC search** → filter by collection, time, bbox, path/row
2. **COG retrieval** → `rasterio.open()` for HTTP range reads
3. **ODC (Open Data Cube)** integration → DEA Notebooks environment provides `datacube` Python API for virtual products and time-series queries

**Unique feature: arrivals catalog** — The STAC API includes an `/arrivals` endpoint showing the most recently ingested scenes:
```
GET https://explorer.dea.ga.gov.au/stac/catalogs/arrivals
```

This is useful for discovering new data without time-range queries.

## Schema/Sample

**STAC Item structure** (Landsat 9 ARD example):
```json
{
  "type": "Feature",
  "stac_version": "1.1.0",
  "id": "ga_ls9c_ard_3-0-0_090084_2024-01-15_final",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[150.5, -34.5], [152.8, -34.5], [152.8, -32.3], [150.5, -32.3], [150.5, -34.5]]]
  },
  "properties": {
    "datetime": "2024-01-15T23:47:32Z",
    "platform": "landsat-9",
    "instruments": ["oli", "tirs"],
    "eo:cloud_cover": 15.2,
    "landsat:wrs_path": "090",
    "landsat:wrs_row": "084",
    "landsat:collection_number": "02",
    "odc:product": "ga_ls9c_ard_3",
    "odc:region_code": "090084",
    "proj:epsg": 32756,
    "dea:dataset_maturity": "final"
  },
  "assets": {
    "nbart_coastal_aerosol": {
      "href": "https://data.dea.ga.gov.au/.../band01.tif",
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": ["data"],
      "eo:bands": [{"name": "coastal_aerosol", "common_name": "coastal"}]
    },
    "nbart_red": {
      "href": "https://data.dea.ga.gov.au/.../band04.tif",
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": ["data"],
      "eo:bands": [{"name": "red", "common_name": "red"}]
    },
    "oa_fmask": {
      "href": "https://data.dea.ga.gov.au/.../oa_fmask.tif",
      "type": "image/tiff; application=geotiff; profile=cloud-optimized",
      "roles": ["metadata"],
      "title": "Fmask cloud/shadow/water/snow classification"
    }
  }
}
```

**Stable identifiers**: Landsat WRS-2 path/row + date. Sentinel-2 MGRS tile + date. Both are suitable for Kafka keys.

## Why Strong

1. **Australia-specific operational products** — Water observations, fuel moisture content, burned area, intertidal elevation, mangrove extent are **not available in global STAC catalogs**. DEA is the authoritative source for Australian environmental monitoring.
2. **ARD quality** — NBART (Nadir BRDF Adjusted Reflectance) is more rigorous than standard L2A. Observational attributes (solar/view angles, terrain shadow) enable advanced corrections.
3. **Fully open** — No API keys, no rate limits. Public S3 buckets.
4. **STAC 1.1.0** — Latest spec version, advanced query support (CQL2).
5. **Open Data Cube integration** — The platform is built on ODC, enabling virtual products, time-series analysis, and compositing.

The key limitation is **geographic scope** — this is **Australia-only**. For global coverage, use Planetary Computer or Earth Search.

## Limitations

- **Australia-only** — No data outside Australian EEZ / land territory. Not useful for global monitoring.
- **Slower than global STAC** — Landsat/Sentinel ARD appears in 3-7 days, vs. 1-3 days on Earth Search. Processing overhead for NBART is significant.
- **No L1 data** — Only ARD (atmospherically corrected + BRDF adjusted). If raw DN values are needed, use Earth Search or Planetary Computer.
- **Provisional products lag** — Burned area and Sentinel-2 water observations are marked "provisional" and update weekly, not daily.
- **No push notifications** — STAC is pull-only. Bridge must poll `/search` or `/arrivals`.
- **Derived products are static or slow** — Land cover is annual, fractional cover is monthly-seasonal. Only water observations and fuel moisture are near-real-time.

## Integration Notes

**Recommended bridge pattern**: **Australia-focused poller**

1. **Collection config** — Bridge targets Australian AOI (bbox `[112, -44, 154, -10]`) and DEA-specific collections.
2. **Polling loop** — Every 30-60 minutes, query `/arrivals` or `/search` with `datetime=lastPoll/..`.
3. **Message groups** — One per collection family:
   - `landsat_ard_scenes` — keyed by `{platform}/{path}/{row}/{date}`
   - `sentinel2_ard_tiles` — keyed by `{tile}/{date}`
   - `water_observations` — keyed by `{path}/{row}/{date}` (Landsat grid)
   - `fuel_moisture` — keyed by `{tile}/{date}` (Sentinel-2 grid)
   - `burned_area` — keyed by `{tile}/{date}`
4. **Reference data** — Emit STAC collection metadata at startup (bands, EPSG, coverage).

**Why add this if Earth Search has Landsat/Sentinel?** DEA's **derived products** are unique:
- **WOfS (Water Observations from Space)** — Operational water extent time series, validated against ground truth
- **Fuel Moisture Content** — Directly relevant for wildfire risk modeling
- **Burned Area** — Operational fire scar mapping
- **Intertidal elevation** — Coastal zone monitoring

These are not available in raw Landsat/Sentinel feeds. The repo could add DEA as a **second-tier source** for Australian environmental monitoring, alongside global STAC for raw imagery.

**Alternative**: For **true NRT water observations**, query DEA's WOfS provisional API (if exposed via OGC or WMS) instead of STAC. STAC may lag behind the operational WMS layers.

## Verdict

**CONDITIONAL ACCEPT** — This is a **Tier-2 regional source** with **unique derived products** (water observations, fuel moisture, burned area) that are operationally maintained for Australia. The STAC API is excellent (1.1.0, COG-native, open), but **geographic scope is narrow** (Australia-only) and **latency is slower** than global STAC (3-7 days for ARD vs. 1-3 days on Earth Search).

Recommended **only if the repo wants Australian-specific environmental products**. For global Landsat/Sentinel-2 coverage, use Planetary Computer or Earth Search instead.

If the repo adds a **regional focus** (e.g., a dedicated Australian data stream for forestry, agriculture, or coastal monitoring), DEA is the authoritative source.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Unique derived products (WOfS, fuel moisture, burned area) not in global STAC |
| Freshness | 2 | ARD ~3-7d, derived products weekly-monthly (slower than global STAC) |
| Openness | 3 | Fully open, no auth, public S3 buckets |
| Schema clarity | 3 | STAC 1.1.0, well-documented, ODC metadata extensions |
| Machine-readability | 3 | JSON, GeoJSON, COG, NetCDF |
| Repo fit | 0 | Australia-only (narrow geographic scope limits global repo utility) |
