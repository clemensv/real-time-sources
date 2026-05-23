# EUMETSAT LSA SAF Land Surface Temperature (LST)

- **Country/Region**: Europe, Africa (MSG disk), Global (Metop swaths)
- **Endpoint**: FTP: `landsaf.ipma.pt`, WMS
- **Protocol**: FTP, HDF5/NetCDF, WMS
- **Auth**: Free registration
- **Format**: HDF5, NetCDF-4
- **Freshness**: 15 minutes (MSG), 3-hourly (Metop)
- **Docs**: https://landsaf.ipma.pt/en/products/land-surface-temperature/
- **Score**: 11/18

## Overview

LSA SAF produces land surface temperature from thermal IR channels:

| Product | Description | Cadence | Resolution | Coverage |
|---------|-------------|---------|------------|----------|
| **LST** | MSG land surface temp | 15 min | 3 km | MSG disk |
| **MLST** | Metop LST (polar) | ~100 min | 1 km | Global swaths |

LST applications:
- **Urban heat islands**: City temperature vs. rural
- **Agricultural stress**: High LST during droughts damages crops
- **Wildfire risk**: Dry, hot surfaces increase fire danger
- **Energy demand**: Cooling/heating load forecasting

## Why Weak for Event Streaming

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 3 | 15 minutes (MSG) |
| **Openness** | 2 | Free registration |
| **Stability** | 3 | Operational LSA SAF |
| **Structure** | 3 | HDF5/NetCDF |
| **Identifiers** | 0 | Gridded field (no natural entities) |
| **Additive value** | 0 | Continuous field, not point events |

## Verdict

**SKIP** (11/18) — LST is a continuous gridded field, not point events. While 15-minute cadence is good, the lack of natural entity identifiers (no stations, no fires, no storms) makes it unsuitable for event streaming.

**Exception**: Could emit LST anomaly hotspots (cells >3 std dev above normal) for extreme heat events, but this is a derived product requiring climatology baseline.

**Better LSA SAF candidate**: **Fire Radiative Power** (FRP) — already covered, point detections with natural events.
