# Capella SAR Open Data Program

- **Country/Region**: Global (sample sites)
- **Endpoint**: `https://www.capellaspace.com/community/capella-open-data/` (portal), AWS S3 buckets
- **Protocol**: HTTP/S3 (static file hosting)
- **Auth**: None (public S3 buckets)
- **Format**: GeoTIFF (COG), HDF5, SICD, SIDD
- **Freshness**: Static archive (sample collections, irregular updates)
- **Docs**: https://www.capellaspace.com/community/capella-open-data/
- **Score**: 9/18

## Overview

Capella Space operates a commercial **X-band SAR constellation** providing **50cm resolution** imagery. The **Open Data Program** releases sample SAR scenes for select locations under permissive licensing (varies by collection, typically CC BY 4.0 or Open Government License).

Sample collections include:
- San Francisco Bay Area (urban, multi-temporal)
- Houston (urban + port infrastructure)
- Hurricane Laura damage (Louisiana, 2020)
- Beirut explosion (2020)
- Ukraine conflict areas (2022)
- Turkey-Syria earthquake (2023)

**Key modes**:
- **Spotlight** — 50cm resolution, small AOI (5×5 km)
- **Stripmap** — 1m resolution, larger swaths (20×50 km)
- **Sliding Spotlight** — 60cm resolution, extended coverage (10×20 km)

## Endpoint Analysis

**Open Data portal verified** — `https://www.capellaspace.com/community/capella-open-data/` lists collections with download links.

Each collection hosted in AWS S3:
```
s3://capella-open-data/san-francisco/
  ├── CAPELLA_C02_SP_GEO_HH_20210315_...tif (GeoTIFF, COG)
  ├── CAPELLA_C02_SP_SICD_HH_20210315_...h5 (SICD, HDF5)
  └── metadata.json
```

**Access**:
```bash
wget https://capella-open-data.s3.us-west-2.amazonaws.com/san-francisco/CAPELLA_C02_SP_GEO_HH_20210315.tif

aws s3 ls s3://capella-open-data/ --no-sign-request
```

**No API or STAC** — Static archive, manual discovery.

## Stable Identifiers

Scene IDs embedded in filenames (e.g., `CAPELLA_C02_SP_GEO_HH_20210315_..._1234`). Keyed by `{site}/{scene_id}`.

## Why Strong

1. **50cm SAR** — High resolution (better than Sentinel-1 10m, 20× better).
2. **Multi-temporal** — San Francisco Bay has ~50 scenes (2019-2023), enables change detection.
3. **Open license** — Most collections CC BY 4.0 (commercial use allowed).
4. **SICD/SIDD** — NGA standard formats for SAR processing pipelines.

## Limitations

- **Sparse coverage** — ~15 sample sites globally (not continuous monitoring).
- **Static archive** — No regular updates (sporadic disaster activations).
- **No API/STAC** — Manual discovery, no automated catalog.
- **Variable licensing** — Some collections have restricted licenses (check per-collection).
- **Commercial service** — Full-access requires enterprise subscription (expensive).

## Integration Notes

**Pattern**: Static collection indexer (one-time ingestion, no polling).

1. Scrape portal for collection list
2. List S3 buckets per site
3. Extract metadata from filenames and `metadata.json`
4. Emit one-time catalog of scenes to Kafka

**Message groups**:
- `capella_sar_scenes` — keyed by `{site}/{scene_id}`
- Payload: Metadata (bbox, resolution, mode, polarization, date, S3 URL)

## Verdict

**WEAK ACCEPT (static archive utility)** — Similar to Umbra: **high-resolution SAR** (50cm) but **sparse coverage** and **static**. Useful for **urban change detection** (San Francisco multi-temporal stack) and **disaster damage assessment**, but not a continuous real-time feed.

**Recommended IF**:
- Users need high-resolution SAR for specific sites (San Francisco, Houston, disaster zones)
- Static archive indexing is acceptable
- Multi-temporal stacks (San Francisco) enable time-series analysis

**Skip IF**:
- Continuous global monitoring is priority (use Sentinel-1 instead)
- Users need broader coverage (Capella samples cover <0.01% of Earth)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2 | 50cm SAR (high-res), multi-temporal (San Francisco), but sparse |
| Freshness | 0 | Static archive, irregular updates (not real-time) |
| Openness | 2 | Mostly CC BY 4.0, some restricted licenses (variable) |
| Schema clarity | 1 | Minimal metadata, no STAC |
| Machine-readability | 2 | GeoTIFF (COG), SICD/SIDD (NGA standards), no API |
| Repo fit | 0 | Static archive, sparse coverage (not continuous feed) |
