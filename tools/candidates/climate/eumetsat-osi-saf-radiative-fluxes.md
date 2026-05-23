# EUMETSAT OSI SAF Radiative Fluxes and Energy Budget

- **Country/Region**: Arctic Ocean (polar cap coverage)
- **Endpoint**: FTP: `ftp.osi-saf.org`, THREDDS (planned)
- **Protocol**: FTP, NetCDF download
- **Auth**: None (anonymous FTP, CC-BY-4.0)
- **Format**: NetCDF-4
- **Freshness**: Daily
- **Docs**: https://osi-saf.eumetsat.int
- **Score**: 8/18

## Overview

OSI SAF produces daily Arctic radiative flux products:
- **Shortwave downwelling radiation** at surface
- **Longwave downwelling radiation**
- **Net radiative flux**

These support:
- **Arctic energy budget**: Sea ice melt/growth modeling
- **Climate monitoring**: Polar amplification (Arctic warming 2x global rate)

## Why Weak

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Freshness** | 0 | Daily — **not NRT** |
| **Openness** | 3 | Anonymous FTP, CC-BY-4.0 |
| **Stability** | 3 | Operational OSI SAF |
| **Structure** | 2 | NetCDF-4 |
| **Identifiers** | 0 | Gridded field |
| **Additive value** | 0 | Daily cadence, climate timescale |

## Verdict

**SKIP** (8/18) — Daily cadence, not near-real-time. Climate research product.

**Better OSI SAF candidates**: ASCAT winds (90-min), SST (hourly) — already covered.
