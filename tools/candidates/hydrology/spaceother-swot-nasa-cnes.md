# NASA/CNES SWOT (Surface Water and Ocean Topography Mission)

- **Country/Region**: Global oceans + large lakes/rivers
- **Endpoint**: `https://podaac.jpl.nasa.gov/` (NASA PO.DAAC), AVISO+ (CNES), Copernicus Marine
- **Protocol**: OPeNDAP, HTTPS, S3 (AWS Open Data), STAC (experimental)
- **Auth**: None for PO.DAAC (NASA Earthdata login optional for bulk), AVISO+ requires registration
- **Format**: NetCDF (CF-compliant)
- **Freshness**: Near-real-time (~6-12 hours for NRT products, ~2-3 days for science products)
- **Docs**: https://swot.jpl.nasa.gov/, https://podaac.jpl.nasa.gov/SWOT
- **Score**: 15/18

## Overview

SWOT (launched December 2022) is a **NASA/CNES joint mission** providing **unprecedented high-resolution ocean and freshwater topography**. The Ka-band Radar Interferometer (KaRIn) measures **sea surface height (SSH)** and **river/lake water level** at **2D coverage** (not just along-track like traditional altimeters).

**Key innovations**:
- **120km swath** — 2D mapping (vs. nadir-only altimeters like Jason-3, Sentinel-6)
- **15m resolution** (rivers/lakes) to **1km resolution** (ocean SSH)
- **Inland water** — First altimetry mission designed for **rivers, lakes, reservoirs** (not just oceans)
- **Ocean mesoscale eddies** — Resolves 15-30km features (vs. ~100km for Jason-3)

**Data products**:
- **L2_HR_RiverSP** — River water level (15m resolution, centerline + width)
- **L2_HR_LakeSP** — Lake/reservoir water level (100m grid)
- **L2_LR_SSH** — Low-resolution ocean SSH (1km grid, NRT)
- **L3_SSH** — Gridded ocean SSH (merged with Jason-3, Sentinel-3, Sentinel-6)
- **L4_SSH** — Gap-filled global ocean SSH (daily grids, delayed-mode)

## Endpoint Analysis

**NASA PO.DAAC verified** — `https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_RIVERSP_2.0` (example)

Data distributed via:
1. **NASA PO.DAAC** — Primary archive (`https://podaac.jpl.nasa.gov/`)
2. **AVISO+** — CNES mirror (`https://www.aviso.altimetry.fr/`)
3. **Copernicus Marine** — Integrated ocean products (`https://data.marine.copernicus.eu/`)
4. **AWS Open Data** — Public S3 buckets (experimental STAC)

**Example: Download SWOT river water level (L2_HR_RiverSP)**
```
wget https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-protected/SWOT_L2_HR_RIVERSP_2.0/SWOT_L2_HR_RiverSP_Reach_012_001_20231201T123456_20231201T124556_PIB0_01.nc
```

**NetCDF structure** (L2_HR_RiverSP):
```
dimensions:
  reach_id = UNLIMITED (river reaches, ~2.5 million globally)
  
variables:
  int64 reach_id(reach_id)
    long_name = "Unique reach identifier"
  
  float wse(reach_id)
    long_name = "Water surface elevation"
    units = "m"
    standard_name = "water_surface_height_above_reference_datum"
  
  float width(reach_id)
    long_name = "River width"
    units = "m"
  
  float slope(reach_id)
    long_name = "Water surface slope"
    units = "m/m"
  
  float area_total(reach_id)
    long_name = "Total water area"
    units = "m^2"
  
  float time(reach_id)
    units = "seconds since 2000-01-01"
```

**Stable identifiers**: `reach_id` for rivers (permanent IDs from SWORD global river database). Ocean grids keyed by `{lat}/{lon}/{time}`.

## Why Strong

1. **Unique inland water capability** — First altimetry mission designed for **rivers, lakes, reservoirs** (not just oceans). Fills gap in hydrology monitoring.
2. **High resolution** — 15m for rivers, 1km for ocean SSH (vs. 25km for Jason-3).
3. **2D coverage** — 120km swath (vs. nadir-only for Jason-3/Sentinel-6).
4. **NRT latency** — 6-12 hours for NRT products (competitive with Sentinel-3).
5. **Open data** — NASA public domain, AVISO+ free registration, AWS S3 public buckets.

## Limitations

- **Young mission** — Launched December 2022, still in calibration/validation phase (some products provisional).
- **21-day repeat** — Lower temporal resolution than daily MODIS/VIIRS or 5-day Sentinel-2 (but unprecedented spatial resolution for altimetry).
- **Cloud-independent** — Ka-band radar (all-weather), but **no optical imagery** (combine with Sentinel-2 for visual context).
- **Complex products** — L2 river/lake products require hydrology expertise (not beginner-friendly).
- **No STAC (yet)** — NASA PO.DAAC has experimental STAC, but most access via OPeNDAP or direct download.

## Integration Notes

**Pattern**: **OPeNDAP poller** or **S3 bucket monitor**

1. Query NASA PO.DAAC for new L2_HR_RiverSP / L2_HR_LakeSP / L2_LR_SSH granules
2. Download NetCDF files (or subset via OPeNDAP)
3. Extract reach-level water level, width, slope for rivers
4. Emit to Kafka

**Message groups**:
- `swot_river_reaches` — keyed by `{reach_id}` (permanent river ID)
- Subject: `swot/river/{reach_id}`
- Payload: Water level, width, slope, area, timestamp

**Reference data**:
- SWORD river database (2.5 million reaches globally) — emit at startup (reach metadata: name, basin, length, mean width)

**Why add SWOT if AVISO+ already covers ocean altimetry?** SWOT adds **inland water** (rivers, lakes) which AVISO+ does not provide. Ocean SSH products are complementary (higher resolution than Jason-3, but lower revisit).

## Verdict

**STRONG ACCEPT** — SWOT is a **unique inland water monitoring source** (rivers, lakes, reservoirs) with **unprecedented resolution** (15m) and **NRT latency** (6-12 hours). The **river water level** products fill a major gap in global hydrology monitoring (complementary to in-situ USGS gauges).

**Recommended as the primary satellite hydrology source** for rivers and lakes. For **ocean altimetry**, SWOT complements AVISO+ (higher resolution, but lower revisit).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | Unique inland water (rivers, lakes), high-res ocean SSH, 2D swath |
| Freshness | 3 | NRT products 6-12h, science products 2-3d |
| Openness | 3 | NASA public domain, AVISO+ free registration, AWS S3 public buckets |
| Schema clarity | 3 | NetCDF CF-compliant, well-documented variables |
| Machine-readability | 2 | NetCDF, OPeNDAP (not STAC/JSON, but standard geospatial) |
| Repo fit | 1 | OPeNDAP polling or S3 monitoring required (not REST/STAC) |
