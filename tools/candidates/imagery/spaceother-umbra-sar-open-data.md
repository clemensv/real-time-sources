# Umbra SAR Open Data Program

- **Country/Region**: Global (sample sites)
- **Endpoint**: `https://umbra.space/open-data` (portal), AWS S3 buckets per site
- **Protocol**: HTTP/S3 (static file hosting)
- **Auth**: None (public S3 buckets)
- **Format**: GeoTIFF (COG), SICD, SIDD (NGA standards)
- **Freshness**: Static archive (sample collections, not continuous monitoring)
- **Docs**: https://umbra.space/open-data, https://docs.umbra.space/
- **Score**: 8/18

## Overview

Umbra is a **commercial SAR operator** with a constellation of X-band (9.6 GHz) synthetic aperture radar satellites providing **25cm resolution** (finest commercial SAR available). The **Open Data Program** releases sample SAR imagery for select locations (urban areas, infrastructure, disaster sites) under Creative Commons BY 4.0 license.

The program provides **ultra-high-resolution SAR** for research, algorithm development, and humanitarian applications. However, coverage is **sparse** (only sample sites, not continuous global monitoring) and **static** (one-time releases, not updated).

**Sample sites** (as of 2024):
- Hong Kong (urban, 25cm)
- Paris (urban, 25cm)
- Sydney (urban, 25cm)
- Los Angeles (urban, 25cm)
- Hurricane Ida damage (Louisiana, 2021)
- Ukraine conflict areas (Mariupol, Kyiv, 2022)
- Turkey-Syria earthquake (2023)

## Endpoint Analysis

**Open Data portal verified** — `https://umbra.space/open-data` lists sample collections with S3 download links.

Each collection includes:
- GeoTIFF (COG-compatible)
- SICD (Sensor Independent Complex Data, NGA standard for SAR)
- SIDD (Sensor Independent Derived Data, amplitude/phase products)
- Metadata (JSON, XML)

**Example S3 structure** (Hong Kong sample):
```
s3://umbra-open-data/hong-kong/
  ├── hong-kong_25cm_spotlight_20230915.tif (GeoTIFF, COG)
  ├── hong-kong_25cm_spotlight_20230915.sicd (SICD, HDF5)
  ├── hong-kong_25cm_spotlight_20230915.sidd (SIDD, NITF)
  └── metadata.json
```

**Accessing data**:
```bash
# HTTP download
wget https://umbra-open-data.s3.amazonaws.com/hong-kong/hong-kong_25cm_spotlight_20230915.tif

# AWS CLI
aws s3 ls s3://umbra-open-data/ --no-sign-request
aws s3 sync s3://umbra-open-data/hong-kong/ ./local/ --no-sign-request
```

**No API** — Static file repository. No STAC catalog, no search endpoint.

## Stable Identifiers

Scene IDs are collection-specific (e.g., `hong-kong_25cm_spotlight_20230915`). Suitable for Kafka keys: `{site}/{collection_id}`.

## Why Strong

1. **Ultra-high resolution** — 25cm SAR is **2× better than Capella** (50cm) and **40× better than Sentinel-1** (10m). Finest commercial SAR available.
2. **X-band** — Higher frequency than Sentinel-1 C-band. Better for urban infrastructure, vehicle detection, change detection.
3. **Open license** — CC BY 4.0 (commercial use allowed with attribution).
4. **NGA standard formats** — SICD/SIDD are DoD/intelligence community standards. Interoperable with SAR processing toolchains.

## Limitations

- **Sparse coverage** — Only ~10-20 sample sites globally. Not a continuous monitoring system.
- **Static archive** — One-time releases. No regular updates for sample sites.
- **No API** — Manual discovery (HTML page scraping). No STAC, no automated catalog.
- **Disaster-focus** — Most samples are disaster response (hurricanes, earthquakes, conflicts). Limited general-purpose coverage.
- **Commercial imagery** — Sample data is free, but **full-access subscriptions** are expensive (enterprise pricing, not public).

## Integration Notes

**Recommended bridge pattern**: **Static collection indexer** (one-time ingestion)

1. **Site enumeration** — Scrape `https://umbra.space/open-data` for collection list (HTML parsing).
2. **S3 bucket listing** — For each site, list S3 bucket contents (`aws s3 ls`).
3. **Metadata extraction** — Download `metadata.json` for each scene.
4. **Message groups** — One group for SAR scenes:
   - `umbra_sar_scenes` — keyed by `{site}/{collection_id}`
   - Subject: `umbra-opendata/scene/{site}/{collection_id}`
   - Payload: Scene metadata (bbox, resolution, polarization, acquisition_date, S3 URLs)
5. **One-time ingestion** — Emit all scenes at bridge startup. No polling (static archive).

**Why not continuous monitoring?** Umbra Open Data is a **static archive**, not a real-time feed. New collections appear sporadically (every few months, tied to disaster activations or marketing campaigns).

## Verdict

**WEAK ACCEPT (static archive utility)** — Umbra Open Data provides **ultra-high-resolution SAR** (25cm, finest available), but coverage is **sparse** (sample sites only) and **static** (no regular updates).

**Recommended IF**:
- The repo wants **ultra-high-resolution SAR** for urban change detection, infrastructure mapping, or disaster damage assessment
- Users accept **limited coverage** (sample sites only, not global)
- Static archive indexing (one-time ingestion) is acceptable

**Skip IF**:
- The repo prioritizes **continuous real-time monitoring** (Umbra is a static archive)
- Global coverage is required (Umbra samples cover <0.01% of Earth)
- Users need **affordable commercial SAR** (Umbra full-access is expensive; Sentinel-1 is free)

Alternative: For **continuous open SAR**, use **Sentinel-1 GRD** (10m, global, daily revisit, fully open) via Copernicus Data Space or Earth Search.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2 | Ultra-high-resolution SAR (25cm), but sparse coverage (sample sites) |
| Freshness | 0 | Static archive, no regular updates (not real-time) |
| Openness | 3 | CC BY 4.0 (commercial use allowed), public S3 buckets |
| Schema clarity | 1 | Minimal metadata (JSON), no STAC (manual catalog) |
| Machine-readability | 2 | GeoTIFF (COG), SICD/SIDD (NGA standards), but no API |
| Repo fit | 0 | Static archive (not continuous feed), sparse coverage |
