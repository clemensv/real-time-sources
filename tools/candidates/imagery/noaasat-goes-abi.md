# NOAA GOES Advanced Baseline Imager (ABI) - Full Disk

- **Country/Region**: USA / Western Hemisphere
- **Endpoint**: S3 bucket `s3://noaa-goes16/ABI-L2-MCMIPC/`, `s3://noaa-goes18/ABI-L2-MCMIPF/`
- **Protocol**: S3 (AWS Open Data Program)
- **Auth**: None (public S3 bucket)
- **Format**: NetCDF4
- **Freshness**: 5-15 minutes (varies by scan mode)
- **Docs**: https://www.goes-r.gov/products/baseline-imagery.html
- **Score**: 10/18

## Overview

The Advanced Baseline Imager (ABI) is the primary instrument aboard GOES-R series satellites (GOES-16/17/18/19). ABI is a 16-channel multispectral imager capturing visible, near-IR, and IR imagery of Earth from geostationary orbit. ABI products include:

- **Full Disk**: Entire Western Hemisphere, every 10-15 minutes
- **CONUS**: Continental US, every 5 minutes
- **Mesoscale**: Regional sectors, every 60 seconds

ABI Level 2 Multi-Channel Cloud and Moisture Imagery (MCMIP) products combine channels into RGB composites and derived products (cloud top height, SST, fire detection, volcanic ash, etc.).

ABI imagery is used for:
- **Weather forecasting**: Nowcasting convection, fog, storm tracking
- **Hurricane monitoring**: Eye structure, intensity estimation
- **Wildfire detection**: Active fire identification via IR channels
- **Aviation**: Turbulence, icing, ash cloud detection
- **Oceanography**: SST, ocean color (limited to daytime visible)

## Endpoint Analysis

**S3 bucket structure:**

```
s3://noaa-goes16/ABI-L2-MCMIPC/{YYYY}/{DDD}/{HH}/
s3://noaa-goes18/ABI-L2-MCMIPF/{YYYY}/{DDD}/{HH}/
```

Product codes:
- `MCMIPC` = CONUS (Continental US)
- `MCMIPF` = Full Disk
- `MCMIPM` = Mesoscale (2 sectors: M1, M2)

Example file:
```
OR_ABI-L2-MCMIPF-M6_G18_s20261421200157_e20261421209477_c20261421209551.nc
```

**Data format**: NetCDF4 (HDF5-based), **not JSON**. Each file contains:
- Radiance/reflectance for 16 channels
- Cloud mask, cloud type, cloud top properties
- Derived products (SST, fire mask, volcanic ash)
- Geolocation arrays (lat/lon for each pixel)

**File sizes**:
- Full Disk: ~300-600 MB per file
- CONUS: ~50-100 MB per file
- Mesoscale: ~10-20 MB per file

**Volume**:
- Full Disk: ~100 files/day/satellite (10-15 min cadence) → ~50 GB/day
- CONUS: ~288 files/day (5 min cadence) → ~28 GB/day
- Mesoscale: ~1,440 files/day/sector (1 min cadence) → ~28 GB/day/sector

**Key model**: Gridded imagery (not entity-keyed). Each file is a full raster scene.

## Schema / Sample

NetCDF4 structure (highly simplified):
```
dimensions:
    y = 5424;  // CONUS: 5424 rows
    x = 5424;  // CONUS: 5424 columns

variables:
    float CMI_C01(y, x);  // Channel 1 radiance
    float CMI_C02(y, x);  // Channel 2 radiance
    ...
    float CMI_C16(y, x);  // Channel 16 radiance
    
    int DQF(y, x);  // Data quality flags
    
    // Geolocation
    float x(x);  // Projection x-coordinates
    float y(y);  // Projection y-coordinates
    
    // Derived products
    byte BCM(y, x);  // Binary cloud mask
    byte ACHA_HT(y, x);  // Cloud top height
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | **Cornerstone of weather forecasting**, wildfire/hurricane/aviation |
| Freshness | 3/3 | 1-15 minute cadence depending on mode (excellent) |
| Openness | 3/3 | No auth, AWS Open Data, free egress |
| Schema Clarity | 2/3 | NetCDF4 well-documented but complex (16 channels + derived products) |
| Machine-Readability | 1/3 | NetCDF4 (not JSON) — requires xarray/netCDF4 library |
| Repo Fit | -2/3 | **Massive binary rasters** (300-600 MB/file) — incompatible with repo's JSON event model |

**Total: 10/18**

- ABI is the **most important operational satellite instrument** for US weather
- 1-minute mesoscale scans enable severe weather nowcasting
- AWS S3 delivery is robust and well-maintained
- **However**: Binary raster files (300-600 MB each) are incompatible with this repo's HTTP+JSON polling model
- No pixel-level event stream or REST API alternative

## Limitations

- **Binary NetCDF4 format** — not JSON-parseable
- **Massive file sizes** (300-600 MB for full disk)
- **Gridded imagery** — no natural entity key
- Requires specialized libraries (xarray, netCDF4, satpy for RGB processing)
- No JSON REST API for derived products (e.g., "active fires detected in this image")
- GOES-17 had ABI cooling issues 2018-2022 (degraded IR channels)
- Coverage limited to Western Hemisphere

## Verdict

**SKIP** — While ABI is operationally critical and scientifically invaluable, the **S3 NetCDF4 raster file model** (300-600 MB binary images) is fundamentally incompatible with this repo's event stream paradigm. A potential alternative: if NOAA publishes **derived JSON products** from ABI (e.g., a REST API listing detected fires, cloud top heights by lat/lon points, or volcanic ash plume outlines), those would be viable. But the raw imagery files themselves don't fit. **Defer** unless a JSON-based ABI-derived product API emerges.
