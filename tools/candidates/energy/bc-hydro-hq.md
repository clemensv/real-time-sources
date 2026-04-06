# BC Hydro / Hydro-Québec — Canadian Provincial Utilities

**Country/Region**: British Columbia and Quebec, Canada
**Publisher**: BC Hydro (British Columbia) / Hydro-Québec (Quebec)
**API Endpoint**: Various (see below)
**Documentation**: BC Hydro: https://www.bchydro.com/energy-in-bc/operations/transmission/transmission-system.html; Hydro-Québec: https://www.hydroquebec.com/generation/
**Protocol**: Web portals with some JSON endpoints
**Auth**: None for public dashboards
**Data Format**: JSON, HTML
**Update Frequency**: 5-15 minutes (real-time dashboards)
**License**: Publicly accessible (Crown corporations)

## What It Provides

BC Hydro and Hydro-Québec are Canada's two largest hydroelectric utilities, together representing massive clean energy systems.

### BC Hydro
- **Real-time generation**: Predominantly hydro (~95%), with some thermal
- **Reservoir levels**: Major reservoir storage levels (critical for operations)
- **Demand**: BC system demand
- **Interchange**: Cross-border flows with Alberta (AESO) and US (Bonneville Power)

### Hydro-Québec
- **Generation**: Massive hydro system (~36,000 MW installed hydro capacity — larger than most countries)
- **Demand**: Quebec system demand
- **Interchange**: Cross-border flows with Ontario (IESO), New York (NYISO), New England (ISO-NE), New Brunswick, and Newfoundland/Labrador
- **Reservoir levels**: Including the massive La Grande complex in James Bay

## API Details

**BC Hydro**: The system status page at bchydro.com shows real-time data. Behind it, JSON endpoints may be available:

```
https://www.bchydro.com/energy-in-bc/operations/transmission/transmission-system.html
(Web dashboard with embedded data)
```

**Hydro-Québec**: Generation page at hydroquebec.com:

```
https://www.hydroquebec.com/generation/
(Web dashboard — data loaded client-side)
```

Neither utility provides a formally documented public REST API. Data access requires either:
1. Screen scraping the dashboard pages
2. Reverse-engineering the JavaScript data endpoints
3. Using OASIS (Open Access Same-time Information System) for transmission data

Hydro-Québec's data is partially available through OASIS:
```
https://www.oasis.oati.com/HQTE/HQTEdoc/HQTEmain.html
```

## Freshness Assessment

Dashboard data updates every 5-15 minutes. Hydro-Québec's generation page shows near-real-time reservoir levels and generation output. BC Hydro's transmission system page shows current system conditions.

## Entity Model

- **System**: BC Hydro (British Columbia), HQ (Hydro-Québec)
- **Fuel Type**: Hydro (dominant), Thermal (minor), Wind (growing in QC)
- **Reservoir**: Named reservoirs with levels in meters or GWh of stored energy
- **Interchange**: Named interconnections (e.g., Phase II tie to New England, Châteauguay to NYISO)
- **Time**: PST/PDT (BC), EST/EDT (Quebec)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time dashboards but no API |
| Openness | 1 | No documented API; web scraping or OASIS required |
| Stability | 2 | Crown corporations (government-owned), stable institutions |
| Structure | 1 | Dashboard-only access, no verified JSON endpoints |
| Identifiers | 2 | Standard interchange partner names, reservoir names |
| Additive Value | 3 | Critical for Canadian coverage; HQ is world's largest hydro utility |
| **Total** | **11/18** | |

## Notes

- Hydro-Québec operates the largest hydroelectric system in the world — the La Grande complex alone has ~16,000 MW of capacity. Understanding its operations gives insight into the world's largest single clean energy system.
- Quebec's exports to New England and New York are a major decarbonization pathway for the US Northeast (see NYISO's Champlain Hudson Power Express project).
- BC Hydro's reservoir data is operationally critical — the province runs almost entirely on hydro, making it highly sensitive to snowpack and rainfall.
- For Canadian grid coverage: AESO (Alberta) + IESO (Ontario) + BC Hydro + Hydro-Québec + NB Power would cover ~90% of Canadian generation.
- The lack of public APIs from these utilities is a significant gap. OASIS provides some transmission data but not generation mix details.
