# DLR EnMAP (Environmental Mapping and Analysis Program) - Hyperspectral

- **Country/Region**: Global (Germany-operated)
- **Endpoint**: `https://www.enmap.org/` (portal), FTP download
- **Protocol**: FTP, HTTPS, WCS (OGC)
- **Auth**: Free registration for science users, commercial licenses for enterprise
- **Format**: GeoTIFF, ENVI (hyperspectral standard)
- **Freshness**: Weeks to months (tasking-based, not continuous monitoring)
- **Docs**: https://www.enmap.org/, https://www.enmap.org/data_access/
- **Score**: 10/18

## Overview

EnMAP (Environmental Mapping and Analysis Program) is **Germany's hyperspectral satellite** (launched 2022) providing **30m resolution** imagery with **228 spectral bands** (420-2450nm, visible to short-wave infrared). Hyperspectral data enables **detailed material identification** (minerals, vegetation species, water quality, soil types) beyond RGB/multispectral imagery.

**Key applications**:
- **Mineral mapping** — Identify ore bodies, mineral exploration (geology)
- **Vegetation species classification** — Distinguish crop types, forest species (agriculture, forestry)
- **Water quality** — Chlorophyll, suspended sediment, algae blooms (limnology, coastal monitoring)
- **Soil properties** — Organic carbon, moisture, texture (soil science)
- **Urban materials** — Asphalt types, roofing materials, concrete composition (urban planning)

**Data access**:
- **Science users** — Free via proposal-based access (DLR review, ~2-4 week approval)
- **Commercial users** — Paid licenses via DLR or distributors
- **Public archive** — Limited sample scenes (not continuous monitoring)

## Endpoint Analysis

**EnMAP portal verified** — `https://www.enmap.org/data_access/` provides catalog search.

However:
- **Tasking-based** — EnMAP is **not a continuous monitoring mission**. Data is acquired via **tasking requests** (users submit AOI + date range, DLR schedules acquisition if feasible).
- **No STAC** — Custom catalog, FTP/HTTPS download only.
- **Science proposal required** — Free access for research, but requires application + approval (weeks).
- **Sample scenes sparse** — ~500 scenes globally (2022-2024), limited public access.

**Data format**:
- **L1B** — Top-of-atmosphere radiance (228 bands)
- **L1C** — Orthorectified radiance
- **L2A** — Bottom-of-atmosphere reflectance (atmospherically corrected)
- **ENVI format** — Hyperspectral standard (binary + header file)
- **GeoTIFF** — RGB quicklooks (true color, false color)

**Stable identifiers**: Scene IDs (e.g., `ENMAP01-____L2A-DT0000012345_20240115T102030Z_001_V010300_...`). Keyed by `{scene_id}` or `{date}/{orbit}`.

## Why Strong (if accessible)

1. **Hyperspectral** — 228 bands (vs. 4-13 for multispectral). Enables **material-level classification** (not just land cover).
2. **30m resolution** — Competitive with Landsat (30m), better than most hyperspectral (PRISMA 30m, Hyperion 30m, DESIS 30m).
3. **Science-quality** — Radiometric + geometric calibration traceable to SI standards (metrological-grade).
4. **Free for science** — Proposal-based access (no cost for approved research).

## Limitations

- **Tasking-based** — Not continuous monitoring. Users request specific AOIs (no global archive).
- **Weeks to months latency** — Tasking + acquisition + processing can take 1-3 months (not NRT).
- **Science proposal required** — Free but slow approval (2-4 weeks). Not instant access.
- **Narrow swath** — 30km swath (vs. 185km for Landsat, 290km for Sentinel-2). Limited coverage per overpass.
- **16-day revisit** — Same as Landsat (but tasking conflicts mean actual revisit is longer).
- **No public STAC** — FTP/HTTPS download only, no cloud-native access.

## Integration Notes

**Not feasible for NRT repo** — EnMAP is **tasking-based** with **weeks to months latency**. Not a continuous real-time feed.

**Possible use case**: If the repo wants to add a **static hyperspectral archive** (sample scenes for algorithm development, material classification benchmarks), EnMAP could be indexed. But it's **not a real-time source**.

## Verdict

**REJECT (not real-time)** — EnMAP is a **high-value hyperspectral mission** (228 bands, 30m resolution), but it's **tasking-based** with **weeks to months latency**. Not suitable for a near-real-time data repo.

**Recommended**: Skip EnMAP for the repo. For **continuous multispectral monitoring**, use Sentinel-2 (13 bands, 10m, 5-day revisit, NRT). For **hyperspectral research**, EnMAP is excellent but requires direct user engagement (proposal submission, tasking requests).

**Possible exception**: If the repo adds a **static hyperspectral baseline** (one-time ingestion of sample scenes for algorithm validation), EnMAP could be included. But it's not a real-time feed.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | 228-band hyperspectral, 30m resolution, material-level classification |
| Freshness | 0 | Tasking-based, weeks to months latency (not NRT) |
| Openness | 2 | Free for science (proposal required), commercial licenses for enterprise |
| Schema clarity | 2 | ENVI format (hyperspectral standard), but no STAC |
| Machine-readability | 2 | GeoTIFF, ENVI (standard formats), but FTP-only (no API) |
| Repo fit | 1 | Tasking-based, not continuous monitoring (not real-time) |
