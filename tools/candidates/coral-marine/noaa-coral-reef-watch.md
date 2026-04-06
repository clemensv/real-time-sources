# NOAA Coral Reef Watch
**Country/Region**: Global (tropical and subtropical)
**Publisher**: NOAA Coral Reef Watch (CRW) / NESDIS
**API Endpoint**: `https://coralreefwatch.noaa.gov/product/5km/` (data products)
**Documentation**: https://coralreefwatch.noaa.gov/product/5km/index.php
**Protocol**: HTTP file access / ERDDAP / OPeNDAP / WMS
**Auth**: None
**Data Format**: NetCDF, GeoTIFF, PNG, ASCII
**Update Frequency**: Daily (satellite-derived)
**License**: US Government public domain

## What It Provides
NOAA Coral Reef Watch provides the world's primary satellite-based coral bleaching heat stress monitoring system (Daily Global 5km v3.1):
- **Sea Surface Temperature (SST)** — daily CoralTemp 5km
- **SST Anomaly** — departure from climatological mean
- **Coral Bleaching HotSpot** — SST exceeding bleaching threshold
- **Degree Heating Week (DHW)** — accumulated thermal stress (key bleaching predictor)
- **Bleaching Alert Area** — 5-level alert system (No Stress → Alert Level 2)
- **SST Trend** — 7-day temperature trend
- **4-Month Bleaching Outlook** — probabilistic forecast

Products are available globally at 5km resolution, covering all tropical coral reef areas.

## API Details
- **Current data products**: `https://coralreefwatch.noaa.gov/data_current/5km/v3.1_op/daily/{format}/`
- **Format options**: `png/` (images), `nc/` (NetCDF), `geotiff/` (GeoTIFF), `txt/` (ASCII grids)
- **Regional products**: Tropics, Global, East, West, Pacific, Indian, South Atlantic, Coral Triangle, Caribbean, Florida, Hawaii, Great Barrier Reef
- **ERDDAP access**: `https://coastwatch.pfeg.noaa.gov/erddap/` — NOAA's ERDDAP server with CRW datasets
- **OPeNDAP**: NetCDF data available via OPeNDAP for subsetting
- **Virtual Stations**: Time series data for ~220 reef sites worldwide
- **THREDDS catalog**: `https://pae-paha.pacioos.hawaii.edu/thredds/catalog.html` (mirrored data)

## Freshness Assessment
Good. Satellite data is processed and published daily. The 5km product uses near real-time satellite SST data (CoralTemp). Products are typically available by early morning UTC for the previous day. The 4-month outlook updates weekly.

## Entity Model
- **Grid Cell** (5km resolution, lat/lon, all products indexed by pixel)
- **Virtual Station** (site ID, name, lat/lon, country, reef name — ~220 global sites)
- **Product** (SST, SST Anomaly, HotSpot, DHW, Bleaching Alert Area, SST Trend)
- **Alert Level** (0=No Stress, 1=Watch, 2=Warning, 3=Alert Level 1, 4=Alert Level 2)
- **Time Series** (daily values per station or grid cell)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily satellite products |
| Openness | 3 | Public domain, no auth |
| Stability | 3 | NOAA operational product since 2000 |
| Structure | 2 | NetCDF/GeoTIFF primary, limited JSON |
| Identifiers | 2 | Grid coordinates, ~220 virtual station IDs |
| Additive Value | 3 | Only global coral bleaching monitoring system |
| **Total** | **15/18** | |

## Notes
- ERDDAP provides the most developer-friendly access with subsetting and format conversion
- NetCDF is the standard scientific format but requires specialized libraries to parse
- Virtual Stations (time series for specific reef sites) are the most bridge-friendly data format
- The ~220 reef sites cover all major reef regions globally
- DHW (Degree Heating Week) is the critical metric for predicting coral bleaching events
- Data has been continuous since 1985 (reprocessed historical) with the v3.1 algorithm
