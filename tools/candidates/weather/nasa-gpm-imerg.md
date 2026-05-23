# NASA GPM IMERG (Global Precipitation Measurement - Integrated Multi-satellitE Retrievals)

- **Country/Region**: Global
- **Endpoint**: `https://gpm.nasa.gov/data/imerg` (GES DISC archive), `https://jsimpsonhttps.pps.eosdis.nasa.gov/text/imerg/` (PPS NRT data)
- **Protocol**: HTTPS file download (HDF5, NetCDF), OPeNDAP
- **Auth**: Earthdata Login (free registration)
- **Format**: HDF5, NetCDF-4
- **Freshness**: 4-hour latency (IMERG Early Run), 14-hour (Late Run), ~4 months (Final Run)
- **Docs**: https://gpm.nasa.gov/data/imerg, https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHHE_07/summary
- **Score**: 13/18

## Overview

The Global Precipitation Measurement (GPM) mission's Integrated Multi-satellitE Retrievals for GPM (IMERG) algorithm combines observations from the GPM Core Observatory satellite, a constellation of partner satellites, and ground-based precipitation gauges to produce global precipitation estimates at 0.1° × 0.1° spatial resolution and 30-minute temporal resolution. Coverage spans 60°N to 60°S (near-global, excluding polar regions).

IMERG generates three products with different latencies:
- **Early Run** — 4-hour latency, forward-propagated only
- **Late Run** — 14-hour latency, forward and backward propagation, microwave calibration
- **Final Run** — ~4 months latency, includes gauge calibration (research quality)

For near real-time applications, **IMERG Early** provides half-hourly global precipitation grids within 4 hours of observation. This is used for flood forecasting, drought monitoring, and agricultural early warning. The product includes precipitation rate (mm/hr), precipitation probability, and quality flags.

## Endpoint Analysis

IMERG data is distributed by NASA's Goddard Earth Sciences Data and Information Services Center (GES DISC) and the Precipitation Processing System (PPS). Access requires **Earthdata Login** (free registration at urs.earthdata.nasa.gov).

**GES DISC OPeNDAP endpoint (example for Early Run):**
```
https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGHHE.07/
```

**PPS HTTPS direct download (NRT):**
```
https://jsimpsonhttps.pps.eosdis.nasa.gov/text/imerg/early/YYYYMM/
```

Files follow naming convention:
```
3B-HHR-E.MS.MRG.3IMERG.20240115-S000000-E002959.0000.V07B.HDF5
           ^     ^                ^
       product  date            half-hour time window
```

**Sample file structure (HDF5):**
- `Grid/precipitationCal` — calibrated precipitation rate (mm/hr), 3600×1800 grid (0.1° resolution)
- `Grid/precipitationUncal` — uncalibrated
- `Grid/randomError` — random error estimate
- `Grid/probabilityLiquidPrecipitation` — likelihood that precip is liquid (not ice/snow)
- `Grid/precipitationQualityIndex` — quality flag (0-100)

**Earthdata Login auth pattern:**
```bash
# Requires Bearer token from Earthdata Login OAuth or Basic Auth with app password
curl -n -c cookies.txt -b cookies.txt \
  "https://jsimpsonhttps.pps.eosdis.nasa.gov/text/imerg/early/202401/3B-HHR-E.MS.MRG.3IMERG.20240115-S000000-E002959.0000.V07B.HDF5"
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 4-hour latency for Early Run — good for daily forecasting but not sub-hourly streaming |
| Openness | 2 | Free Earthdata Login required; registration is instant but auth adds complexity |
| Stability | 3 | NASA/JAXA operational mission, IMERG algorithm since 2014 (GPM launch) |
| Structure | 2 | HDF5/NetCDF-4 with well-documented grid structure, but not JSON/REST |
| Identifiers | 2 | Grid cells (lat/lon bins) are stable; time windows are 30-minute fixed intervals |
| Richness | 2 | Precipitation rate + uncertainty + quality flags + phase (liquid/ice) |

**IMERG is the state-of-the-art global precipitation product.** The 0.1° spatial resolution (~10km at equator) and 30-minute cadence are unmatched for satellite-only global coverage. The 4-hour latency for Early Run is acceptable for operational flood forecasting and drought monitoring.

**Grid-based structure is natural for time-series aggregation.** Each 30-minute file is a global snapshot. A bridge could emit CloudEvents per grid cell, per region of interest (bounding box), or per administrative boundary (e.g., river basin). The stable lat/lon grid makes keying straightforward.

**Complements existing hydrology bridges:** IMERG provides the precipitation *input* to hydrological models; existing repo bridges (USGS-IV, Pegelonline, CHMI) provide the *output* (streamflow, water level). Combining both enables rainfall-runoff analysis.

## Limitations

- **Earthdata Login required.** Free and instant, but adds OAuth/cookie/token handling. Not truly open (no-auth).
- **File-based delivery, not API.** Each 30-minute window is a separate HDF5 file (~50 MB). A bridge must poll the directory listing, download new files, parse HDF5, and extract grid cells. This is heavier infrastructure than JSON REST polling.
- **4-hour latency for Early Run** is too slow for flash flood warnings in small catchments. It's designed for basin-scale (100+ km²) forecasting, not sub-hourly nowcasting.
- **Polar regions excluded** (coverage 60°N–60°S). No Alaska, northern Canada, Scandinavia, Antarctica, Greenland.
- **Volume.** A global grid at 0.1° resolution is 3600×1800 = 6.48 million cells per 30-minute file. Emitting all cells as Kafka events would be impractical. The bridge must filter to regions of interest or aggregate to coarser resolution.
- **No change detection.** Unlike point-sensor data (where you emit only when a gauge reading changes), precipitation grids update every 30 minutes globally. The bridge must decide: emit all cells every cycle? Only cells with precip > threshold? Only deltas vs. previous half-hour?

**Key tradeoff:** IMERG is high-value data, but the file-based HDF5 delivery and global grid volume make it a heavier lift than REST JSON APIs. A bridge would likely target specific regions (e.g., major river basins, drought-prone areas, flood-watch zones) rather than global all-cell emission.

## Final Verdict

**Verdict**: ⚠️ **Maybe**

IMERG is scientifically excellent and operationally valuable, but the file-based HDF5 delivery, Earthdata Login auth, and grid-cell volume make it a more complex bridge than typical REST APIs. It's best suited for region-specific deployment (e.g., "Amazon basin IMERG feed" or "Sahel precipitation tracker") where the value justifies the implementation cost.

If the repo prioritizes point-sensor hydrology (gauges, water levels), IMERG adds upstream context but may be lower priority than extending gauge coverage. If the repo expands to gridded satellite products (which would open the door to MODIS, VIIRS, SMAP, etc.), IMERG is a flagship candidate.

**Recommended if pursued:**
- Regional bridge (e.g., major river basins, drought-watch zones)
- Keying by grid cell (lat/lon bin at 0.1° or coarser aggregation)
- Poll every 30 minutes for new Early Run files
- Emit only cells with precipitation > threshold OR only deltas vs. previous cycle

**Bridge type:** Poller (HTTPS file listing + HDF5 download/parse, 30-minute interval)

**Keying:** Grid cell (lat/lon at 0.1° or aggregated resolution)

**Reference data:** Grid metadata (lat/lon bounds, cell IDs) — static, embedded in HDF5 files
