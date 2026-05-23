# ESA BIOMASS Forest Biomass SAR

- **Country/Region**: Global forests (tropical focus)
- **Endpoint**: TBD (mission launched Nov 2024, data products expected 2025–2026)
- **Protocol**: TBD (likely CDSE OData/STAC)
- **Auth**: OAuth (expected)
- **Format**: NetCDF, GeoTIFF (expected)
- **Freshness**: TBD (mission in commissioning phase)
- **Score**: TBD (provisional 8/18)

## Overview

**BIOMASS**, launched November 2024, is ESA's first P-band SAR mission for measuring
**forest above-ground biomass**:

- **P-band SAR** (435 MHz) — penetrates forest canopy
- **Forest height** mapping
- **Biomass density** (tons/hectare)
- **Forest disturbance** detection
- **Tropical forest focus** (Amazon, Congo, SE Asia)

Mission goal: improve carbon stock estimates for climate policy (REDD+, Paris Agreement).

## Verdict

⏭️ **Reference** — **Mission too new** (Nov 2024 launch, data products not yet operational
as of Jan 2026). Biomass products will likely be **annual or seasonal updates**, not
near-real-time. P-band SAR data is **highly specialized** and requires expert processing.

**Skip** — not NRT, not general-purpose, mission still in commissioning.

| Criterion | Provisional Score |
|-----------|-------------------|
| Value | 2 (niche: forestry, carbon accounting) |
| Freshness | 0 (annual/seasonal products expected) |
| Openness | 2 |
| Schema | 2 |
| Machine-readability | 1 |
| Repo fit | 0 (annual grids, not streaming) |

**Provisional total: ~7/18** — **Skip**.
