# ESA CryoSat-2 Sea Ice Thickness

- **Country/Region**: Arctic, Antarctic
- **Endpoint**: https://data-portal.csic.es/ (various archives)
- **Protocol**: FTP, HTTP download
- **Auth**: Free registration for some archives
- **Format**: NetCDF
- **Freshness**: Monthly products (NRT experimental)
- **Score**: 7/18

## Overview

CryoSat-2 (launched 2010) measures **sea ice thickness** via radar altimetry:

- **Arctic and Antarctic**
- **Monthly gridded products** (25 km resolution)
- **NRT experimental products** (weekly, limited availability)
- **Freeboard → thickness conversion** (assumption-dependent)

Critical for: Arctic shipping, climate monitoring, ice forecasting.

## Verdict

❌ **Skip** — Monthly products are too slow. NRT products are experimental and
not widely distributed via stable API. CryoSat data is **specialist-oriented**
(glaciology, polar science) and requires complex processing. **Skip** for
general repo.

| Criterion | Score |
|-----------|-------|
| Value | 2 (polar niche) |
| Freshness | 0 (monthly) |
| Openness | 2 |
| Schema | 2 |
| Machine-readability | 1 |
| Repo fit | 0 (monthly, specialist data) |

**Total: 7/18** — **Skip**.
