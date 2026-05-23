# NOAA JPSS S3 Archive (VIIRS/ATMS/CrIS/OMPS)

- **Country/Region**: USA / Global
- **Endpoint**: S3 bucket `s3://noaa-jpss/` (VIIRS, ATMS, CrIS, OMPS, CERES)
- **Protocol**: S3 (AWS Open Data Program)
- **Auth**: None (public S3 bucket)
- **Format**: NetCDF4, HDF5
- **Freshness**: 3-hour latency (NRT products)
- **Docs**: https://registry.opendata.aws/noaa-jpss/
- **Score**: 8/18

## Overview

The Joint Polar Satellite System (JPSS) is NOAA's polar-orbiting constellation (Suomi-NPP, NOAA-20, NOAA-21) carrying advanced instruments for atmospheric, ocean, and land monitoring. JPSS data is published via AWS S3 as part of NOAA's Big Data Program.

**Instruments:**
- **VIIRS** (Visible Infrared Imaging Radiometer Suite): 22-channel imagery (day/night band, active fire, SST, ocean color, vegetation, snow/ice)
- **ATMS** (Advanced Technology Microwave Sounder): Temperature and moisture profiles
- **CrIS** (Cross-track Infrared Sounder): High-resolution atmospheric soundings
- **OMPS** (Ozone Mapping and Profiler Suite): Ozone column and profile
- **CERES** (Clouds and the Earth's Radiant Energy System): Earth radiation budget

JPSS products are used for:
- **Numerical weather prediction**: Temperature/moisture soundings for forecast models
- **Wildfire detection**: VIIRS 375m active fire product
- **Air quality**: OMPS ozone, aerosol optical depth
- **Ocean monitoring**: SST, ocean color (chlorophyll)
- **Snow/ice mapping**: Snow cover extent, sea ice concentration

## Endpoint Analysis

**S3 bucket structure:**

```
s3://noaa-jpss/VIIRS_Imagery/SNPP_Day_Night_Band/
s3://noaa-jpss/VIIRS_Fires/SNPP_VIIRS_I-Band_375m_Active_Fire/
s3://noaa-jpss/ATMS/
s3://noaa-jpss/CrIS/
```

Example file:
```
VNP14IMG_A2026143_0648_001.hdf
```

**Data formats**: NetCDF4, HDF5 (binary satellite data) — **not JSON**.

**File sizes**: Vary widely by product:
- VIIRS imagery: 5-50 MB per granule
- ATMS soundings: 1-5 MB per granule
- CrIS soundings: 50-200 MB per granule
- OMPS: 1-10 MB per granule

**Temporal coverage**: NRT (3-hour latency) + historical archive back to 2011 (Suomi-NPP launch).

**Volume**: Thousands of files per day (depends on product).

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | **Critical for weather forecasting** and environmental monitoring |
| Freshness | 2/3 | 3-hour latency (NRT processing) |
| Openness | 3/3 | No auth, AWS Open Data, free egress |
| Schema Clarity | 1/3 | NetCDF4/HDF5 complex structures (requires domain knowledge) |
| Machine-Readability | 1/3 | Binary formats (not JSON) — requires specialized libraries |
| Repo Fit | -2/3 | **Binary raster/sounding files** (MB to 100s of MB) — incompatible with JSON event model |

**Total: 8/18**

- JPSS is NOAA's **flagship polar-orbiting constellation**
- Provides critical inputs for weather forecasts
- AWS S3 delivery is robust
- **However**: Binary NetCDF4/HDF5 files (not JSON)
- Large file sizes (MB to 100s of MB)
- Gridded/swath/profile data (not entity-keyed time series)
- No REST API or JSON-based access layer

## Limitations

- **Binary formats** (NetCDF4, HDF5) — not JSON-parseable
- **Large file sizes** (1-200 MB per granule)
- **Gridded/swath data** — no natural entity key
- 3-hour NRT latency (not real-time)
- Polar orbit coverage gaps (revisit time 6-12 hours at mid-latitudes)
- Requires specialized libraries (xarray, h5py, satpy)
- Complex calibration/geolocation processing needed

## Verdict

**SKIP** — JPSS S3 data is scientifically critical but fundamentally incompatible with this repo's HTTP+JSON polling model. The **binary NetCDF4/HDF5 files** (1-200 MB each) and **gridded/swath data structures** don't align with entity-keyed event streams. A JPSS bridge would require:
1. Polling S3 for new granules
2. Downloading MB-scale binary files
3. Parsing NetCDF4/HDF5 with specialized libraries
4. Extracting point/grid data
5. Transforming to events

This represents a **different integration pattern** (S3 file processor vs. REST poller). **Defer** unless the repo adds support for satellite file processing pipelines. Alternative: If NOAA publishes **derived JSON products** from JPSS (e.g., "ATMS temperature profile for these 1,000 locations"), those would be viable.
