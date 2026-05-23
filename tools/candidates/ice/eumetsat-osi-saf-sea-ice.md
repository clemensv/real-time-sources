# EUMETSAT OSI SAF Sea Ice Products

- **Country/Region**: Global (polar regions — Arctic and Antarctic)
- **Endpoint**: `https://osi-saf.eumetsat.int/products`, FTP: `ftp.osi-saf.org`
- **Protocol**: FTP, THREDDS, REST (planned), NetCDF file download
- **Auth**: None (open CC-BY-4.0 license)
- **Format**: NetCDF-4 (CF-1.6 compliant), GRIB2, HDF5
- **Freshness**: Daily (sea ice concentration, edge), 2x daily (drift), hourly (some products)
- **Docs**: https://osi-saf.eumetsat.int
- **Score**: 11/18

## Overview

The Ocean and Sea Ice Satellite Application Facility (OSI SAF) produces operational sea ice products from microwave radiometers (AMSR-2, SSMIS) and scatterometers (ASCAT) on polar-orbiting satellites. Key NRT products include:

- **Sea Ice Concentration (OSI-401-d, OSI-408-a)**: Gridded Arctic/Antarctic sea ice fraction (0-100%)
- **Sea Ice Edge (OSI-402-c, OSI-403-c)**: Boundary between open water and ice-covered regions
- **Sea Ice Type (OSI-403-d)**: First-year vs. multi-year ice classification
- **Sea Ice Drift (OSI-405-c)**: Daily ice motion vectors (Polar Stereographic grids)
- **Sea Ice Emissivity**: Brightness temperature products for data assimilation

These products are critical for:
- **Arctic shipping**: Safe navigation through ice-covered waters (Northern Sea Route, Northwest Passage)
- **Climate monitoring**: Sea ice extent is a key climate indicator (Arctic amplification)
- **Fisheries**: Ice edge is a biological hotspot (phytoplankton blooms, marine mammals)
- **Search and rescue**: Ice drift forecasting for accident response

## Endpoint Analysis

**Primary Distribution**: FTP server at `ftp.osi-saf.org` (anonymous access):
```
ftp://ftp.osi-saf.org/prod/ice/
  /edge/
  /conc/
  /drift/
  /type/
```

**Directory structure** (probed via anonymous FTP):
```
/prod/ice/conc/
  /OSI-401-d/2024/06/
    ice_conc_nh_polstere-100_multi_202406150000.nc
    ice_conc_sh_polstere-100_multi_202406150000.nc
```

**Update cadence**:
- Sea ice concentration: Daily (updated ~12:00 UTC for previous day)
- Sea ice edge: Daily
- Sea ice drift: 2x daily (00:00 and 12:00 UTC products)
- Sea ice type: Daily (Arctic only)

**THREDDS Data Server** (planned): OSI SAF is migrating to THREDDS for OPeNDAP/HTTP access. Not yet operational as of mid-2024.

**No REST API**: Product discovery requires FTP directory listing or RSS feeds. No JSON metadata API.

## Schema / Sample

**Sea Ice Concentration NetCDF** (OSI-401-d):
```
dimensions:
    xc = 1120 (Polar Stereographic X)
    yc = 1120 (Polar Stereographic Y)
    time = 1

variables:
    float ice_conc(time, yc, xc)
        long_name: "sea ice area fraction"
        units: "%"
        standard_name: "sea_ice_area_fraction"
        valid_range: 0.0, 100.0
        
    int status_flag(time, yc, xc)
        flag_meanings: "ice open_water land lake ambiguous error"
        flag_values: 1, 5, 10, 15, 20, 30
```

**Sea Ice Drift NetCDF** (OSI-405-c):
```json
{
  "grid_cell": "i245_j367",
  "latitude": 78.234,
  "longitude": -15.678,
  "time": "2024-06-15T00:00:00Z",
  "dX_km": 12.5,
  "dY_km": -8.3,
  "drift_uncertainty_km": 2.1,
  "status_flag": "nominal"
}
```

Derived event model for bridging:
- **Subject/Key**: Grid cell ID (Polar Stereographic i/j indices) or lat/lon bucket
- **Message groups**: Concentration updates, drift updates, edge updates
- **Challenge**: Gridded products, not point observations — need to decide on event granularity

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 1 | Daily (not sub-hourly; some products 2x daily) |
| **Openness** | 3 | No auth, CC-BY-4.0 license, anonymous FTP |
| **Stability** | 3 | Operational EUMETSAT SAF since 1997 |
| **Structure** | 3 | NetCDF-4, CF-1.6, documented |
| **Identifiers** | 1 | Gridded data (no natural entity IDs; must create grid-cell keys) |
| **Additive value** | 0 | Repo has no sea ice yet, but daily cadence is slow |

**Strengths**:
- **Open and stable**: Anonymous FTP, 25+ year operational record, EUMETSAT backing
- **Climate relevance**: Sea ice is an Essential Climate Variable (ECV)
- **Arctic shipping boom**: Northern Sea Route traffic up 10x since 2010
- **Polar gap coverage**: Microwave sensors work in darkness (polar night)

**Use cases**:
- Track daily sea ice extent anomalies (Arctic summer minimum trends)
- Monitor ice drift for shipping route planning
- Combine with AIS vessel tracking (repo has `digitraffic-maritime`, `kystverket-ais`) to show ships near ice edge

## Limitations

1. **Daily cadence**: Most products update once per day (previous day's analysis). This is slower than sub-hourly weather/hydro feeds. Ice drift is 2x daily. Not "real-time" in the sub-minute sense, but operationally useful.

2. **Gridded vs. point**: Products are raster grids (100 km or 10 km resolution), not point observations. To stream as events, must either:
   - Emit entire grid as single event (large payload)
   - Tile grid into cells and emit cell-level events (sparse for open ocean)
   - Emit only ice edge polyline (derived product)

3. **No REST API**: FTP-only distribution. Bridge would poll FTP directory for new files. THREDDS migration is planned but not live.

4. **Latency**: Products represent previous day's conditions (T-1 day). For shipping, forecast products (from numerical models) are more actionable than analysis products.

5. **Identifier challenge**: No natural entity IDs. Could key by grid cell (i,j) or lat/lon bin, but this creates 1M+ artificial entities for full polar grids.

6. **Overlap with NSIDC**: US NSIDC distributes similar products (SSMIS sea ice concentration). OSI SAF adds ASCAT-derived products and European provenance.

## Verdict

**MARGINAL** (11/18) — Strong on openness and stability, but **daily cadence** and **gridded format** limit real-time utility. Sea ice concentration changes slowly (days to weeks), so daily updates are scientifically appropriate but don't fit the repo's sub-hourly streaming focus.

**Better OSI SAF candidates** with higher freshness:
- **OSI SAF ocean surface winds** (ASCAT) — 2x daily swath products, sub-orbital granularity
- **OSI SAF sea surface temperature** — hourly/3-hourly composites

**If pursuing sea ice**:
- Emit ice edge polyline (WKT LineString) as single event per day per hemisphere
- Emit drift vectors only for cells with significant ice cover (>15%)
- Combine with numerical sea ice forecasts (ECMWF SEAS or CMEMS) for forward-looking events

**Status**: Low priority due to daily cadence. Consider **OSI SAF winds** or **SST** instead for higher-frequency NRT feeds.
