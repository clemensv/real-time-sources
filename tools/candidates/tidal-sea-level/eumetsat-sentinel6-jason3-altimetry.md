# EUMETSAT Sentinel-6 / Jason-3 Sea Level Altimetry

- **Country/Region**: Global oceans (reference ground track)
- **Endpoint**: EUMETSAT Data Store, Copernicus Marine, AVISO
- **Protocol**: REST API, FTP, NetCDF download
- **Auth**: Free registration
- **Format**: NetCDF-4
- **Freshness**: Near-real-time (~3-6 hours), daily
- **Docs**: https://www.eumetsat.int/sentinel-6
- **Score**: 10/18

## Overview

EUMETSAT distributes **marine altimetry** data from:
- **Sentinel-6 Michael Freilich** (operational, launched 2020)
- **Jason-3** (operational, NOAA/EUMETSAT partnership)

Altimeters measure **sea surface height** (SSH) by radar ranging. Applications:
- **Sea level rise**: Climate monitoring (global mean sea level trend)
- **Ocean currents**: SSH gradients reveal geostrophic currents
- **El Niño monitoring**: Equatorial Pacific SSH anomalies
- **Storm surge**: SSH elevation during tropical cyclones

## Endpoint Analysis

**EUMETSAT Data Store**:
```
GET https://api.eumetsat.int/data/browse/collections?q=Sentinel-6
```

**Update cadence**:
- NRT products: ~3-6 hours from observation
- Repeat cycle: 10 days (each satellite revisits same ground track)
- Along-track sampling: ~7 km

**Latency**: Too slow for storm surge warnings (6-hour lead time insufficient)

## Why Weak for This Repo

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 1 | 3-6 hour latency, 10-day repeat cycle |
| **Openness** | 3 | Free, Copernicus open data |
| **Stability** | 3 | Operational Copernicus/NOAA mission |
| **Structure** | 3 | NetCDF-4, documented |
| **Identifiers** | 0 | Along-track points (no stations) |
| **Additive value** | 0 | Climate timescale, not real-time hazard |

## Verdict

**SKIP** (10/18) — 10-day repeat cycle and 3-6 hour latency make this **not near-real-time**. Altimetry is valuable for climate monitoring but not for event streaming.

**Better alternatives**: Tide gauges (NOAA CO-OPS, IOC SLSMF) provide continuous sea level at fixed stations (sub-hourly updates).
