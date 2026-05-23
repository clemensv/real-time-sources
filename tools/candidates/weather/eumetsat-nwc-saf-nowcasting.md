# EUMETSAT NWC SAF Cloud and Precipitation Nowcasting Products

- **Country/Region**: Europe, Africa, Atlantic (MSG disk), Global (polar swaths)
- **Endpoint**: `https://www.nwcsaf.org`, EUMETSAT Data Store, EUMETCast
- **Protocol**: File-based (NetCDF, HDF5), WMS visualization, EUMETCast broadcast
- **Auth**: Free for research/NMS use (registration required)
- **Format**: NetCDF-4, HDF5
- **Freshness**: 15 minutes (MSG products), 3-hourly (polar products)
- **Docs**: https://www.nwcsaf.org
- **Score**: 13/18

## Overview

The Nowcasting SAF (NWC SAF) produces **automated cloud analysis and precipitation nowcasts** from geostationary (MSG SEVIRI) and polar-orbiting (Metop AVHRR, Sentinel-3 SLSTR, NOAA-20/21 VIIRS) satellites. The software package (**NWC/GEO** and **NWC/PPS**) is distributed to national meteorological services for local processing, but EUMETSAT also generates and distributes operational products.

**Key MSG (geostationary) products** (15-minute cadence):

| Product | Full Name | Description |
|---------|-----------|-------------|
| **CT** | Cloud Type | Fractional/opaque cloud, type classification (18 classes) |
| **CTTH** | Cloud Top Temperature & Height | Cloud top pressure, temperature, height |
| **PC** | Precipitating Clouds | Precipitation intensity (mm/h), type (convective/stratiform) |
| **CRR** | Convective Rainfall Rate | Instantaneous rainfall rate from convection |
| **ASII** | ASII Severe Convection | Hail, overshooting tops, lightning potential |
| **RDT** | Rapid Development Thunderstorms | Growing convective cells, tracking |

**Why nowcasting matters**:
- **Severe weather warnings**: Hail, tornadoes, flash floods (0-6 hour lead time)
- **Aviation**: Convective cloud tops hazard for aircraft
- **Renewable energy**: Solar PV output depends on cloud type/thickness
- **Flood forecasting**: Rainfall nowcasts feed hydrological models

NWC SAF fills the gap between **radar** (high resolution, limited range) and **numerical weather models** (global coverage, but 6+ hour lead time). It provides **Europe/Africa-wide nowcasting** at 15-minute cadence.

## Endpoint Analysis

**Distribution channels**:

1. **EUMETCast**: Primary operational channel (DVB-S broadcast). Requires ground station hardware. **Not suitable for HTTP/Kafka bridge**.

2. **EUMETSAT Data Store**: Selected NWC SAF products available via Data Store API with free registration:
   ```
   GET https://api.eumetsat.int/data/browse/collections?q=NWC
   ```

3. **NMS redistribution**: Some national met services (DWD, Météo-France, Met Office) may republish NWC SAF products via their own portals/APIs. Not standardized.

4. **EUMETView WMS**: Visualization only (not data access):
   ```
   https://view.eumetsat.int/geoserver/wms?layers=nwc:CT
   ```

**Challenge**: NWC SAF products are **primarily distributed via EUMETCast**. The Data Store may have delayed or subset products. **FTP/HTTP access is limited** compared to OSI SAF or H SAF.

**Update cadence**:
- MSG products: Every 15 minutes (SEVIRI repeat cycle)
- Latency: ~20-30 minutes from observation
- File size: 5-50 MB (NetCDF grids for full MSG disk)

## Schema / Sample

**Cloud Type (CT) NetCDF**:
```
dimensions:
    num_rows_acquisition_grid = 3712
    num_columns_acquisition_grid = 3712

variables:
    byte ct(num_rows_acquisition_grid, num_columns_acquisition_grid)
        long_name: "Cloud type"
        flag_meanings: "not_processed cloud_free snow_contaminated sea_ice very_low_cumuliform very_low_stratiform low_cumuliform low_stratiform medium_cumuliform medium_stratiform high_opaque high_semitransparent very_high_opaque very_high_semitransparent fractional_clouds undefined"
        flag_values: 0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20
```

**Convective Rainfall Rate (CRR) example**:
```json
{
  "type": "eumetsat.nwc-saf.precip.convective-rainfall",
  "source": "nwc-saf/crr/msg-seviri",
  "id": "crr_20240615_120000_n42p5_e012p0",
  "time": "2024-06-15T12:00:00Z",
  "subject": "precip/{lat_bucket}/{lon_bucket}",
  "data": {
    "latitude": 42.52,
    "longitude": 12.01,
    "rainfall_rate_mm_h": 18.5,
    "precip_type": "convective",
    "quality_flag": "good",
    "cloud_top_temp_k": 215.3
  }
}
```

**Event model**:
- Gridded products (3712×3712 for full MSG disk at 3 km)
- **Sparse emission**: Emit only cells with active phenomena (precipitation >0.1 mm/h, severe convection flags, rapidly developing thunderstorms)
- **Object tracking**: RDT product tracks individual convective cells over time (cell ID persistence) — **good candidate for event streaming**

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 3 | 15-minute updates (MSG products) |
| **Openness** | 1 | EUMETCast primary, Data Store access unclear |
| **Stability** | 3 | Operational NWC SAF since 2002 |
| **Structure** | 3 | NetCDF-4, documented schemas |
| **Identifiers** | 2 | Gridded (RDT has cell IDs, others do not) |
| **Additive value** | 1 | Repo has weather alerts; NWC adds nowcast layer |

**Strengths**:
- **15-minute cadence**: Fast enough for severe weather nowcasting
- **Operational critical**: Used by European NMS for warnings
- **Object tracking**: RDT tracks convective cell life cycles (initiation → maturity → decay)
- **Automated interpretation**: Cloud type, precipitation, severe convection — no human analyst needed

**Real-world use**:
- **2021 Germany floods**: NWC SAF PC/CRR detected 30+ mm/h rainfall rates 2 hours before flash flooding
- **Aviation**: EasyJet uses CTTH for turbulence avoidance (thunderstorm tops)
- **Solar energy**: ENERsolar (NWC SAF product) forecasts PV output based on cloud type

## Limitations

1. **EUMETCast dependency**: Primary distribution is broadcast, not HTTP. Data Store availability is **unclear** (needs verification).

2. **Gridded format**: Full disk products are 3712×3712 grids (13.8M cells). Must filter to active phenomena.

3. **No open FTP**: Unlike OSI SAF and H SAF, NWC SAF does not have anonymous FTP.

4. **NMS-focused**: Products designed for operational met services (who have EUMETCast receivers), not public API consumers.

5. **RDT is best candidate**: Rapid Development Thunderstorms (RDT) product tracks individual convective cells with persistent IDs — **this is the one NWC SAF product with natural event entities**. Other products (CT, CTTH, PC, CRR) are gridded fields.

## Verdict

**PROMISING** (13/18) — High freshness and operational value, but **distribution channel is unclear**. **RDT (Rapid Development Thunderstorms) is the standout product** — it tracks individual convective cells with IDs over time.

**Recommended path**:
1. **Verify Data Store access**: Confirm if RDT and CRR are available via EUMETSAT Data Store API
2. **Focus on RDT**: Emit one event per tracked thunderstorm cell (cell ID as key)
3. **Fallback to EUMETView**: If file access is unavailable, poll WMS layers for CRR grid (lower fidelity)
4. **NMS partnership**: Contact a European NMS (DWD, KNMI) to explore access to their NWC SAF output

**Volume estimate** (RDT):
- Summer convective season: ~50-200 active cells over MSG disk
- 15-minute updates: 96 updates/day
- Each cell tracked for ~30-90 minutes → ~10-50 new cells/hour
- **~5,000-10,000 events/day** (one per cell per observation)

**Status**: Conditionally strong, **pending Data Store verification**. RDT is top-tier if accessible.
