# CoastWatch ERDDAP Satellite SST (GeoPolar VIIRS NRT)

- **Country/Region**: USA / Global
- **Endpoint**: `https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisGeoPolarSSTN5NRT.json`
- **Protocol**: ERDDAP (REST over HTTP)
- **Auth**: None
- **Format**: JSON, CSV, NetCDF (client-selectable)
- **Freshness**: Daily (near-real-time processing)
- **Docs**: https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisGeoPolarSSTN5NRT.html
- **Score**: 11/18

## Overview

NOAA CoastWatch operates ERDDAP (Environmental Research Division's Data Access Program) servers that provide unified access to satellite-derived ocean products. The GeoPolar SST product blends data from **VIIRS** (Visible Infrared Imaging Radiometer Suite) aboard JPSS satellites (Suomi-NPP, NOAA-20, NOAA-21) and **geostationary satellites** (GOES-16/18) to produce near-real-time global sea surface temperature fields at ~5km resolution.

ERDDAP SST products are used for:
- **Fisheries management**: SST fronts indicate productive zones
- **Marine navigation**: Route planning to avoid temperature extremes
- **Climate monitoring**: Ocean heat content trends
- **Coral reef health**: Thermal stress detection (bleaching alerts)
- **Hurricane forecasting**: SST drives tropical cyclone intensification

ERDDAP provides **gridded** data (lat/lon/time cubes), not point observations. The service supports:
- **Multiple output formats**: JSON, CSV, NetCDF, GeoTIFF, KML
- **Subsetting**: Spatial/temporal constraints via URL parameters
- **OPeNDAP protocol**: Industry-standard data access

## Endpoint Analysis

**ERDDAP endpoint structure:**

```
https://coastwatch.pfeg.noaa.gov/erddap/griddap/{datasetID}.{format}?{variables}[{constraints}]
```

Example (last day of SST for a small region):
```
GET https://coastwatch.pfeg.noaa.gov/erddap/griddap/nesdisGeoPolarSSTN5NRT.json?analysed_sst[(last)][(29):(31)][(-123):(-121)]
```

Response: JSON object with `table.columnNames` and `table.rows`.

**Dataset ID**: `nesdisGeoPolarSSTN5NRT` (NESDIS Geostationary + Polar SST, Night, 5km, Near-Real-Time)

**Variables**:
- `analysed_sst`: Analyzed sea surface temperature (°C)
- `analysis_error`: Estimated error (°C)
- `mask`: Land/ice/sea mask
- `sea_ice_fraction`: Fractional sea ice coverage (0-1)

**Dimensions**:
- `time`: Days since 1970-01-01
- `latitude`: -90 to 90, ~0.05° resolution
- `longitude`: -180 to 180, ~0.05° resolution

**Key model**: `{time}/{lat}/{lon}` — gridded data, not entity-keyed.

**Volume**: Global daily grids are **massive** (~7,200 × 3,600 pixels = 25M cells). Practical use requires spatial subsetting.

## Schema / Sample

JSON response (subset query):
```json
{
  "table": {
    "columnNames": ["time", "latitude", "longitude", "analysed_sst"],
    "columnTypes": ["String", "float", "float", "float"],
    "rows": [
      ["2026-05-22T12:00:00Z", 29.0, -123.0, 15.2],
      ["2026-05-22T12:00:00Z", 29.0, -122.95, 15.3],
      ...
    ]
  }
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | Critical for fisheries, navigation, climate, coral health |
| Freshness | 2/3 | Daily updates (NRT processing, not sub-hourly) |
| Openness | 3/3 | No auth, no rate limits, NOAA open data |
| Schema Clarity | 2/3 | ERDDAP is well-documented, but gridded data model differs from point sensors |
| Machine-Readability | 2/3 | JSON available, but gridded queries are complex |
| Repo Fit | -1/3 | **Gridded raster data** (not entity/sensor time series) — poor keying model |

**Total: 11/18**

- ERDDAP is powerful and well-designed
- Multi-satellite blended SST is scientifically robust
- Output format flexibility (JSON, CSV, NetCDF)
- Global coverage
- **However**: Gridded data model doesn't align with this repo's entity-keyed event paradigm
- No stable "sensor ID" or "grid cell ID" for Kafka keying
- Queries return arrays of lat/lon/value tuples, not time series for named entities
- Daily cadence is lower than repo's typical sub-hourly targets

## Limitations

- **Gridded data model** — no natural entity key (entire grid updates daily)
- **Massive full-grid size** — 25M cells/day (requires aggressive spatial subsetting)
- **Daily cadence** — not sub-hourly or minute-level
- Query syntax is complex for gridded constraints
- ERDDAP is designed for scientific data access, not event streaming
- No WebSocket or streaming API (HTTP GET only)
- Interpretation requires oceanographic context (SST anomaly vs. absolute)

## Verdict

**SKIP** — While ERDDAP satellite SST products are scientifically valuable and well-architected, the **gridded raster data model** is incompatible with this repo's entity-keyed event stream paradigm. There's no natural "station ID" or "sensor ID" to use as a Kafka key. Bridging ERDDAP SST would require either:
1. Emitting the entire 25M-cell grid daily as a single "event" (not viable)
2. Treating each grid cell as an entity (25M Kafka keys — not meaningful)
3. Pre-defining regions of interest and tracking SST for those zones

Option 3 is feasible (e.g., "Atlantic hurricane main development region SST"), but it's **use-case-specific** rather than a general bridge. **Defer** unless there's demand for pre-defined ocean region monitoring. ERDDAP is better suited to pull-based scientific workflows than push-based event streams.
