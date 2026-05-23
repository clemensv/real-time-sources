# Copernicus CAMS Global Fire Assimilation System (GFAS)

- **Country/Region**: Global
- **Endpoint**: https://ads.atmosphere.copernicus.eu/datasets/cams-global-fire-emissions-gfas
- **Protocol**: CDS API
- **Auth**: Free ADS account
- **Format**: GRIB / NetCDF
- **Freshness**: Daily, 1-day latency
- **Score**: 11/18

## Overview

GFAS assimilates MODIS/VIIRS fire radiative power (FRP) to produce daily **biomass burning emission estimates**:

- **Burnt area** (km²/day)
- **Fire radiative power** (MW)
- **Emissions**: CO, CO₂, NOx, PM2.5, BC, OC (tons/day per grid cell)
- **0.1° resolution** (~10 km)

GFAS emissions drive CAMS atmospheric composition forecasts (smoke, air quality impacts).

## Verdict

⚠️ **Maybe** — Daily **gridded emissions** (0.1° × 3,600 × 1,800 cells = 6.5M grid points).
Bulk download model (NetCDF ~100 MB/day). Not streaming.

| Criterion | Score |
|-----------|-------|
| Value | 2 (derived product, not raw observations) |
| Freshness | 1 (daily, 1-day lag) |
| Openness | 2 |
| Schema | 3 |
| Machine-readability | 1 (CDS async API) |
| Repo fit | 2 (could aggregate by country/region) |

**Total: 11/18** — **Skip**. Prefer **EFFIS active fires** (near-real-time points) over GFAS (daily grids).
