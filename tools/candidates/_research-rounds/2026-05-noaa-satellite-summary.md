# NOAA Satellite NRT Feeds — Research Summary

**Research scope**: NOAA satellite missions and satellite-derived products (US operational meteorological + environmental satellites and their public NRT APIs/streams)

**Date**: 2026-05-23  
**Agent**: NOAA Satellite NRT Research (parallel fleet member)  
**Total candidates assessed**: 15

---

## Executive Summary

**Counts by Verdict:**
- **STRONGLY RECOMMEND**: 1 (Propagated Solar Wind — perfect 18/18 score)
- **RECOMMEND**: 2 (GOES X-ray Flux, GOES Proton Flux — both 17/18)
- **CONSIDER**: 4 (GOES Magnetometer, GOES Electron Flux, F10.7 Solar Flux, FIRMS VIIRS Fire)
- **SKIP**: 8 (GLM Lightning, GOES ABI, JPSS S3, Kp Forecast, DSCOVR EPIC, CoastWatch SST, Coral Reef Watch, OVATION Aurora)

**Key findings:**
1. **SWPC JSON APIs are exceptional** — 1-5 minute cadence, clean JSON, zero auth, 17-18/18 scores
2. **S3 NetCDF4/HDF5 products are incompatible** — Binary raster files (MB to GB scale) don't fit repo's HTTP+JSON event model
3. **Gridded data products lack entity keys** — SST grids, aurora forecasts, imagery don't align with repo's entity-keyed paradigm
4. **Top recommendation**: Propagated Solar Wind (18/18) — most operationally significant space weather stream

---

## Topic-Grouped Candidates

### Space Weather (8 candidates)

| Candidate | Score | Verdict | Key Strength |
|-----------|-------|---------|--------------|
| Propagated Solar Wind | 18/18 | **STRONGLY RECOMMEND** | Primary input for geomagnetic storm forecasting, 1-min cadence |
| GOES X-ray Flux | 17/18 | **RECOMMEND** | Solar flare detection, 1-min cadence, operational alerts |
| GOES Proton Flux | 17/18 | **RECOMMEND** | Radiation storm forecasting, 5-min cadence, aviation safety |
| GOES Magnetometer | 16/18 | **CONSIDER** | Geomagnetic field, 1-min cadence (incremental to K-index) |
| GOES Electron Flux | 16/18 | **CONSIDER** | Satellite charging risk, 5-min cadence (lower priority) |
| F10.7 Solar Flux | 15/18 | **CONSIDER** | Solar activity index, 3x daily (lower cadence) |
| OVATION Aurora Forecast | 13/18 | **SKIP** | Gridded forecast model (keying challenge) |
| Kp Forecast | 14/18 | **SKIP** | Forecast (not observations), 3-hourly |

### Imagery (2 candidates)

| Candidate | Score | Verdict | Key Strength |
|-----------|-------|---------|--------------|
| DSCOVR EPIC | 14/18 | **SKIP** | 12-36 hour latency (not NRT) |
| GOES ABI | 10/18 | **SKIP** | 300-600 MB NetCDF4 rasters (incompatible) |

### Lightning (1 candidate)

| Candidate | Score | Verdict | Key Strength |
|-----------|-------|---------|--------------|
| GOES GLM | 12/18 | **SKIP** | 5-15 MB NetCDF4 files every 20 sec (format mismatch) |

### Oceans (2 candidates)

| Candidate | Score | Verdict | Key Strength |
|-----------|-------|---------|--------------|
| CoastWatch ERDDAP SST | 11/18 | **SKIP** | Gridded raster (no entity key) |
| Coral Reef Watch | 9/18 | **SKIP** | Daily + 1-2 day latency, gridded NetCDF4 |

### Weather (1 candidate)

| Candidate | Score | Verdict | Key Strength |
|-----------|-------|---------|--------------|
| JPSS S3 (VIIRS/ATMS/CrIS) | 8/18 | **SKIP** | 1-200 MB NetCDF4/HDF5 files (incompatible) |

### Wildfire (1 candidate)

| Candidate | Score | Verdict | Key Strength |
|-----------|-------|---------|--------------|
| FIRMS VIIRS Fire | 13/18 | **CONSIDER** | Requires free API key, NASA-hosted, 3-hr latency |

---

## Top 5 Picks (by operational value + repo fit)

1. **NOAA SWPC Propagated Solar Wind** (18/18) — **STRONGLY RECOMMEND**  
   1-minute solar wind + IMF from DSCOVR/ACE with Earth-arrival propagation. Primary driver of geomagnetic storm forecasting. Clean JSON, zero auth.

2. **NOAA GOES X-ray Flux** (17/18) — **RECOMMEND**  
   1-minute X-ray flux in two energy bands from GOES satellites. Primary observable for solar flare detection and classification (A/B/C/M/X scale). Drives space weather alerts.

3. **NOAA GOES Proton Flux** (17/18) — **RECOMMEND**  
   5-minute differential proton flux across 8-11 energy channels. Primary input for radiation storm alerts (S-scale). Critical for aviation polar route planning and satellite operations.

4. **NOAA GOES Magnetometer** (16/18) — **CONSIDER**  
   1-minute magnetic field (Hp/He/Hn/total) from geostationary orbit. Geomagnetic storm detection. Lower priority due to overlap with K-index (already in `noaa-goes` bridge).

5. **NOAA GOES Electron Flux** (16/18) — **CONSIDER**  
   5-minute differential electron flux. Satellite charging and radiation belt monitoring. Lower priority than X-ray/proton flux for public-facing alerts.

---

## Coverage Gaps

### Missing NOAA Satellite NRT Products (not found or incompatible)

1. **GOES SUVI (Solar Ultraviolet Imager)** — No JSON API found (images only)
2. **GOES EXIS X-ray Flux** — Covered by primary X-ray endpoint
3. **GOES SEISS (Space Environment In-Situ Suite)** — Partial coverage via electron/proton flux
4. **JPSS VIIRS 375m Fire Detection (NOAA-native)** — NASA FIRMS found (requires API key), no NOAA direct JSON API discovered
5. **NOAA HMS (Hazard Mapping System) Fire/Smoke** — KML files on FTP, no JSON REST API
6. **NESDIS Blended SST** — ERDDAP available but gridded (no entity key)
7. **NOAA Sea Ice Concentration (NSIDC)** — FTP/file-based, no JSON API
8. **NOAA Volcanic Ash Advisory (satellite-derived)** — Text bulletins, no structured JSON
9. **JPSS ATMS/CrIS Temperature/Moisture Soundings** — S3 NetCDF4 only (no JSON API)
10. **NOAA OISST (Optimum Interpolation SST)** — Daily gridded NetCDF4 (no JSON API)

### Protocol Patterns Not Yet Supported by Repo

- **S3 NetCDF4/HDF5 file processing** — GLM, ABI, JPSS, Coral Reef Watch all use this pattern
- **ERDDAP gridded data** — CoastWatch SST (powerful but gridded, not entity-keyed)
- **OPeNDAP/THREDDS** — Coral Reef Watch (file-based access)

---

## Cross-Cutting Observations

### NOAA Big Data Program (AWS S3)

NOAA publishes satellite data via AWS Open Data:
- **GOES-16/17/18/19**: GLM, ABI, SUVI, EXIS, MAG — all NetCDF4, 5-600 MB files
- **JPSS (Suomi-NPP, NOAA-20, NOAA-21)**: VIIRS, ATMS, CrIS, OMPS — NetCDF4/HDF5, 1-200 MB
- **Himawari-8/9** (JMA, not NOAA): Listed in `noaa-himawari` bucket (404 — may be deprecated)
- **MRMS (Multi-Radar Multi-Sensor)**: Not satellite, but listed as `noaa-nws-mrms` (404)

**Compatibility**: S3-based products are **incompatible with this repo's HTTP+JSON polling model** due to binary formats and large file sizes.

### SWPC JSON APIs Are Gold Standard

NOAA SWPC provides **exceptional JSON APIs** for space weather:
- 1-5 minute cadence
- Clean JSON structures (array of objects or header + data rows)
- Zero authentication
- No rate limits
- Stable endpoints (multi-year uptime)
- Well-documented fields

**These are the strongest candidates for this repo.**

### GOES-17 Retirement Note

**GOES-17** had ABI cooling system issues (2018-2022) leading to degraded IR channels. It was replaced by **GOES-19** (launched June 2024, operational since April 2025). Historical GLM/ABI data from GOES-17 has quality flags.

### NASA vs. NOAA Hosting

Some NOAA satellite products are **NASA-hosted**:
- **FIRMS** (Fire Information for Resource Management System): NASA EOSDIS hosts VIIRS fire data from NOAA satellites (Suomi-NPP, NOAA-20)
- **DSCOVR EPIC**: NASA GSFC hosts the API for NOAA's DSCOVR mission

This introduces minor organizational friction (auth, branding) but the data is from NOAA operational satellites.

---

## Recommended Next Steps

1. **Implement Propagated Solar Wind** (18/18) — Highest value, cleanest fit
2. **Implement GOES X-ray Flux** (17/18) — Primary solar flare observable
3. **Implement GOES Proton Flux** (17/18) — Radiation storm forecasting
4. **Evaluate GOES Magnetometer & Electron Flux** — Incremental value to existing `noaa-goes` bridge
5. **Defer S3/NetCDF4 products** (GLM, ABI, JPSS) until repo adds file-processing capability
6. **Monitor for JSON-based fire APIs** — NOAA HMS or VIIRS-derived REST endpoints
