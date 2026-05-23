# ISRO MOSDAC INSAT-3D/3DR Weather Imagery

- **Country/Region**: India / Indian Ocean region
- **Endpoint**: https://mosdac.gov.in (Meteorological and Oceanographic Satellite Data Archival Centre)
- **Protocol**: Web portal download (registration required)
- **Auth**: Registration required (Indian institutions preferred, international difficult)
- **Format**: IMG (proprietary INSAT format), HDF5 (planned)
- **Freshness**: 30 minutes (full disk), 15 minutes (sector)
- **Docs**: https://mosdac.gov.in
- **Score**: 4/18

## Overview

INSAT-3D (launched 2013) and INSAT-3DR (launched 2016) are Indian geostationary meteorological satellites stationed at 82°E and 74°E respectively. They carry 6-channel imagers and 19-channel atmospheric sounders, providing weather imagery, sea surface temperature, outgoing longwave radiation (OLR), and atmospheric temperature/moisture profiles over the Indian Ocean region.

MOSDAC (Meteorological and Oceanographic Satellite Data Archival Centre) at the Space Applications Centre (SAC), Indian Space Research Organisation (ISRO), is the primary distribution point for INSAT data.

**Critical barriers**:
1. **Registration required** — MOSDAC requires user registration with institutional affiliation
2. **Indian institutions strongly preferred** — international users report registration difficulties
3. **Proprietary IMG format** — INSAT data historically distributed in proprietary .IMG format, not standard NetCDF/HDF5
4. **No public API** — web portal download only, no REST API or cloud storage
5. **Limited English documentation** — data format specs and access guides are sparse

## Endpoint Analysis

**MOSDAC portal verified** — https://mosdac.gov.in is the official portal (loads as "Loading..." placeholder page, suggesting heavy JavaScript or login wall).

**Data access**:
1. **Web portal** — search by satellite/product/time, add to cart, download (requires login)
2. **No FTP server** — no public FTP mentioned in documentation
3. **No API** — no REST API, no OGC services

**Registration process** (based on user reports and documentation):
- Submit registration form online with institutional email and affiliation
- **Strong preference for Indian government/academic institutions** — international users may face rejection or indefinite delays
- Some users report waiting weeks or months for approval, or never receiving approval
- No indication of programmatic access (API keys) after registration

**Products available**:
- **INSAT-3D/3DR Imager** — 6 channels (VIS, SWIR, MIR, WV, TIR1, TIR2), 1–4 km resolution, 30-minute full disk
- **INSAT-3D/3DR Sounder** — 19 channels for atmospheric profiling
- **Derived products** — SST, OLR, cloud motion winds, CAPE, total precipitable water, etc.
- **SCATSAT-1** — scatterometer ocean wind data (separate mission, also on MOSDAC)
- **Megha-Tropiques** — Indo-French precipitation mission data
- **Oceansat-2/3** — ocean color data

**Data format**: Historically, INSAT data was distributed in a proprietary .IMG format. ISRO has been transitioning to HDF5/NetCDF, but it's unclear what percentage of products are available in standard formats.

**Freshness**: INSAT-3D full disk every 30 minutes, sector scans every 15 minutes. This is slower than Himawari (10 min) or GK-2A (10 min), but reasonable for a mid-2010s GEO satellite.

## Why Openness is a Problem

1. **Registration barrier is severe**: International users report difficulty obtaining MOSDAC accounts. Even Indian users report approval delays.
2. **No public cloud mirror**: Unlike Himawari (AWS), INSAT data is not openly redistributed.
3. **Proprietary data formats**: .IMG format is ISRO-specific, requires custom readers. HDF5 transition is incomplete.
4. **No programmatic access**: Web portal only, manual cart-and-download workflow.
5. **Documentation gaps**: English-language user guides are limited; format specifications hard to find.

## Comparison to Other Geostationary Satellites

| Satellite | Coverage | Cadence | Open Access | Score |
|-----------|----------|---------|-------------|-------|
| Himawari-9 | Western Pacific | 10 min | ✅ AWS S3, no auth | 14/18 |
| GK-2A | East Asia | 10 min | ❌ No cloud mirror | 6/18 |
| INSAT-3D | Indian Ocean | 30 min | ❌ Registration barrier | **4/18** |
| GOES-16 | Americas | 10 min | ✅ AWS S3, no auth | 14/18 |

INSAT-3D fills a unique geographic niche (Indian Ocean, South Asia), but the access barriers are prohibitive.

## Verdict

**❌ Skip** — INSAT-3D/3DR data is **not viable** for this repo due to:
- Severe registration barrier (Indian institutions preferred, international users often rejected)
- No public API or cloud storage
- Proprietary data formats (IMG)
- Web portal-only access (not machine-readable)

**Recommendation**: Do not pursue INSAT-3D unless:
1. ISRO opens MOSDAC registration to international users with clear approval timelines
2. INSAT data is mirrored to AWS/Azure/GCP with open access (unlikely)
3. A partner institution in India can provide proxy access

**Alternative for Indian Ocean coverage**: Check if any INSAT-derived products are available through:
- **Bhuvan** (https://bhuvan.nrsc.gov.in) — ISRO's geoportal, may have real-time layers (but likely WMS tiles, not data)
- **VEDAS** (https://vedas.sac.gov.in) — ISRO's Earth observation portal, has API Centre (registration required)
- **EUMETSAT** — EU/India data sharing (EUMETSAT may redistribute select INSAT products)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2 | Covers Indian Ocean / South Asia (unique geography), but older sensor (6 bands vs 16) |
| Freshness | 2 | 30-minute full disk (slower than Himawari/GOES), 15-minute sector |
| Openness | 0 | Registration required, Indian institutions preferred, international access difficult — **severe barrier** |
| Schema Clarity | 0 | Proprietary IMG format, HDF5 transition incomplete, sparse docs |
| Machine-Readability | 0 | Web portal only, no API, no cloud storage |
| Repo-Fit | 0 | Access barriers make it non-viable despite unique geography |

**Score: 4/18** — Not viable. Registration barriers and proprietary formats disqualify INSAT-3D.
