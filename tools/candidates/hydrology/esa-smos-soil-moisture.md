# ESA SMOS Soil Moisture NRT

- **Country/Region**: Global land
- **Endpoint**: https://smos-diss.eo.esa.int/
- **Protocol**: FTP, HTTP download
- **Auth**: Free ESA EO-SSO account
- **Format**: NetCDF, BUFR
- **Freshness**: 3-hour NRT
- **Score**: 10/18

## Overview

SMOS (Soil Moisture and Ocean Salinity) L-band radiometer provides:

- **Soil moisture** (0–5 cm depth, volumetric %)
- **NRT products**: 3-hour latency after sensing
- **~40 km resolution** (coarse but unique L-band capability)
- **Global coverage** every 3 days

Used for: drought monitoring, flood forecasting (soil saturation), agricultural water management.

## Verdict

⏭️ **Reference** — SMOS delivers **gridded soil moisture** (40 km global grid). 3-day revisit
means sparse temporal coverage. Better suited to **aggregation by river basin or agricultural
region** than point streaming. ESA distribution via FTP is bulk-download oriented.

| Criterion | Score |
|-----------|-------|
| Value | 3 (hydrological, agricultural) |
| Freshness | 2 (3-hour NRT) |
| Openness | 1 (account required, FTP) |
| Schema | 3 |
| Machine-readability | 1 (FTP bulk) |
| Repo fit | 0 (coarse grid, 3-day revisit) |

**Total: 10/18** — **Skip**. Coarse resolution + sparse revisit makes it unsuitable for
real-time streaming. Consider **in-situ soil moisture networks** instead (COSMOS-UK, USDA, etc.).
