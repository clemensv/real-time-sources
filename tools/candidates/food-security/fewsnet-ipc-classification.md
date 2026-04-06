# FEWS NET IPC Food Security Classifications

- **Country/Region**: Sub-Saharan Africa (20+ countries)
- **Endpoint**: `https://fdw.fews.net/api/ipcphase/?format=json&country=KE`
- **Protocol**: REST
- **Auth**: None
- **Format**: JSON
- **Freshness**: Quarterly (IPC analysis cycles)
- **Docs**: https://fews.net/fews-data/333
- **Score**: 13/18

## Overview

The Integrated Food Security Phase Classification (IPC) is the global standard for
food security analysis. FEWS NET publishes IPC classifications through their API for
all monitored African countries. Each classification maps a geographic area to a food
security phase from 1 (Minimal) to 5 (Famine).

When an area transitions from Phase 3 (Crisis) to Phase 4 (Emergency), that's a
signal that lives are at stake. This data drives humanitarian funding and response.

Covered African countries include: Kenya, Ethiopia, Somalia, South Sudan, Sudan, Nigeria,
Niger, Mali, Chad, Burkina Faso, DRC, Mozambique, Madagascar, Malawi, Zimbabwe, Uganda,
Tanzania, Senegal, Mauritania, Cameroon.

## Endpoint Analysis

**API root verified** — the `/api/ipcphase/` endpoint is documented and accessible.
Direct queries to the IPC endpoints timed out during testing, likely due to large
result sets without proper pagination.

Related endpoints that were verified:
- `/api/market/` — ✅ Live, returns market locations with coordinates
- `/api/country/` — Lists all monitored countries
- `/api/ipcpopulation/` — Population counts per IPC phase

IPC Phase meanings:
| Phase | Classification | Meaning |
|-------|---------------|---------|
| 1 | Minimal | Adequate food access |
| 2 | Stressed | Marginally able to meet food needs |
| 3 | Crisis | Acute food insecurity |
| 4 | Emergency | Severe food insecurity |
| 5 | Famine | Mass starvation and death |

## Integration Notes

- **Quarterly polling**: IPC analyses are published on a quarterly cycle per country.
  Poll monthly and emit events only on new classifications.
- **Change detection**: The critical signal is phase transitions — a region moving
  from Phase 2 to Phase 3, or Phase 3 to Phase 4. These should be high-priority events.
- **Population data**: Pair phase classifications with population data to calculate
  the number of people affected — this adds impact context to the CloudEvent.
- **Geographic resolution**: IPC data is typically at admin-2 (district) level in
  Africa, providing granular spatial coverage.
- **Timeout handling**: The API can be slow with large queries. Use country-specific
  queries with reasonable limits.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Quarterly updates |
| Openness | 3 | No auth, USAID public data |
| Stability | 3 | USAID-backed, operational since 1985 |
| Structure | 2 | JSON API but slow/timeout-prone |
| Identifiers | 2 | FNID system, geographic unit IDs |
| Richness | 2 | Phase classification + population counts |
