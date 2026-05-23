# Kuwait Bikeshare and Micromobility (GBFS)

- **Country/Region**: Kuwait
- **Endpoint**: N/A (no system exists)
- **Protocol**: N/A
- **Auth**: N/A
- **Format**: N/A
- **Freshness**: N/A
- **Docs**: N/A
- **Score**: N/A (source does not exist)

## Overview

**Kuwait has no public bikeshare or e-scooter system** as of 2025.

**Why bikeshare/micromobility doesn't exist in Kuwait**:

1. **Extreme climate** — Summer temperatures regularly exceed 45°C (113°F), making outdoor cycling dangerous 4–6 months/year
2. **Car-centric culture** — ~400 vehicles per 1,000 population, one of world's highest
3. **Lack of cycling infrastructure** — No protected bike lanes, hostile road design for cyclists
4. **Urban sprawl** — Low-density suburban development makes short trips rare
5. **Cultural norms** — Cycling seen as recreational, not transportation
6. **No policy support** — No government programs to promote active transport

**Comparison to Gulf neighbors**:

| Country | Bikeshare System | GBFS Feed | Notes |
|---------|------------------|-----------|-------|
| **UAE (Dubai)** | Careem Bike (defunct) | ❌ Discontinued 2023 | Extreme heat, low uptake |
| **UAE (Abu Dhabi)** | TXODDS | ⚠️ Unknown | Limited coverage, pilot phase |
| **Saudi Arabia (Riyadh)** | None | ❌ | Car-centric, planned for future |
| **Saudi Arabia (Jeddah)** | None | ❌ | Occasional pilots, not sustained |
| **Qatar (Doha)** | None | ❌ | Some bike paths, no bikeshare |
| **Bahrain** | None | ❌ | Small island, car-dominated |
| **Oman** | None | ❌ | Car-centric culture |
| **Kuwait** | None | ❌ | No system, no plans |

**E-scooters**: Also absent in Kuwait. No Lime, Bird, Tier, or regional equivalents.

**Catalyst checks**:

```
GET https://github.com/MobilityData/gbfs/blob/master/systems.csv
```

Searched for "Kuwait" — **0 results** (as expected, since no system exists)

**Future prospects**:
- Kuwait Vision 2035 mentions sustainable transport but no concrete bikeshare plans
- Possible recreational bike paths in new developments (e.g., Silk City), but not bikeshare
- Climate will always be a barrier (extreme summer heat)

## EV Charging Stations

**Status**: Limited deployment, no real-time availability API discovered.

**Context**:
- Kuwait has ~100 public EV charging stations (as of 2024)
- Operated by:
  - **Kuwait National Petroleum Company (KNPC)** — some stations at gas/service stations
  - **Private providers** (e.g., building parking, malls)
- **No central registry or real-time availability API**
- **Low EV adoption** — <1% of vehicle fleet (as of 2024)

**Open Charge Map probe**:
```
GET https://api.openchargemap.io/v3/poi/?countrycode=KW&maxresults=100
```

Expected result: ~50–100 Kuwait charging stations in global registry
- Locations only (static data)
- No real-time availability (occupied/available status)
- User-contributed, may be incomplete or outdated

**Comparison to European standards**:
- **OCPI** (Open Charge Point Interface) — real-time charge point availability protocol
  - Used in EU, Norway, Netherlands for dynamic status
  - **Not adopted in Kuwait** (as of 2025)
- **NOBIL** (Norway) — government EV charger registry with API
  - **No Kuwait equivalent**

**Why real-time charging data doesn't exist**:
- Low EV adoption (no demand for real-time availability)
- Fragmented operators (no central aggregator)
- No government mandate for open data
- Charging infrastructure still in early deployment

**Future prospects**:
- If Kuwait scales EV adoption (part of sustainability goals), may develop registry
- Timeline: 5–10 years minimum

## Verdict

**Verdict**: ❌ **Skip** — Kuwait has no bikeshare or e-scooter systems (GBFS does not apply). EV charging infrastructure exists but is minimal (~100 stations) with no real-time availability API. Documented here as a **comprehensive negative finding** for micromobility and EV domains.

**Recommendation**:
- **Bikeshare/GBFS**: No action needed. Kuwait is not a viable candidate for this domain.
- **EV charging**: Monitor Open Charge Map for Kuwait station updates (static data only). If Kuwait develops a national EV charging registry with real-time status, revisit as candidate.
- **For Gulf region**: Check UAE (Dubai/Abu Dhabi) for any GBFS or EV charging APIs (likely minimal)

**Cross-Gulf observation**:
The entire GCC region has **near-zero GBFS coverage** (only limited UAE pilots). Climate and car culture make bikeshare/micromobility unviable. This is a region-wide gap, not Kuwait-specific.
