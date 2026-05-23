# ESA EarthCARE Cloud/Aerosol Products

- **Country/Region**: Global
- **Endpoint**: https://dataspace.copernicus.eu/ (via CDSE when available)
- **Protocol**: OData / STAC (expected)
- **Auth**: OAuth (expected)
- **Format**: NetCDF (expected)
- **Freshness**: TBD (mission launched May 2024, data products ramping up in 2025–2026)
- **Score**: TBD (provisional 10/18)

## Overview

**EarthCARE** (Earth Cloud Aerosol and Radiation Explorer), launched May 2024, carries:

- **Cloud Profiling Radar (CPR)** — vertical cloud structure
- **Atmospheric Lidar (ATLID)** — aerosol/cloud layers
- **Multi-Spectral Imager (MSI)** — cloud imagery
- **Broadband Radiometer (BBR)** — radiation budget

Mission goal: improve cloud/aerosol representation in climate models.

## Verdict

⏭️ **Reference** — **Mission too new** (2024 launch, data products still in commissioning
phase as of Jan 2026). Likely to follow **Sentinel granule-notification pattern** when
operational. **Monitor** for future consideration once Level-2 products are routinely
published and NRT latency is defined.

**Skip for now** — wait for operational data distribution to mature.

| Criterion | Provisional Score |
|-----------|-------------------|
| Value | 3 (unique cloud/aerosol profiling) |
| Freshness | ? (TBD) |
| Openness | 2 (OAuth expected) |
| Schema | 3 (NetCDF expected) |
| Machine-readability | 2 |
| Repo fit | 0 (orbital profiles, not station-based) |

**Provisional total: ~10/18** — **Skip for now**, revisit in 6–12 months.
