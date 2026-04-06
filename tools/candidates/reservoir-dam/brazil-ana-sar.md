# Brazil ANA — Sistema de Acompanhamento de Reservatórios (SAR)

**Country/Region**: Brazil
**Publisher**: Agência Nacional de Águas e Saneamento Básico (ANA — National Water and Sanitation Agency)
**API Endpoint**: `https://www.ana.gov.br/sar/` (web portal); `https://www.ana.gov.br/sar/api/` (API, if available)
**Documentation**: https://www.ana.gov.br/sar/
**Protocol**: Web portal; possible REST API
**Auth**: Unknown (likely none for public data)
**Data Format**: HTML/PDF (portal); potentially JSON/CSV via API
**Update Frequency**: Daily (operational reservoir monitoring)
**License**: Brazilian government open data

## What It Provides

The SAR (Sistema de Acompanhamento de Reservatórios — Reservoir Monitoring System) was created by ANA in 2013 and launched in 2014. It provides operational monitoring of Brazil's major reservoirs, organized into three modules:

1. **Sistema Interligado Nacional (SIN)** — National Interconnected System (hydroelectric reservoirs)
2. **Nordeste e Semiárido** — Northeast and Semi-Arid region reservoirs (critical water supply)
3. **Outros Sistemas Hídricos** — Other water systems

Data includes:
- **Reservoir storage volume** (hm³ — cubic hectometres) and **percentage full**
- **Inflow and outflow** rates
- **Water level / elevation**
- **Operational status** of major reservoirs

Brazil has one of the world's largest hydroelectric systems, and the SIN module alone covers dozens of major reservoirs. The Nordeste module is critical for monitoring water scarcity in Brazil's drought-prone northeast.

## API Details

The primary access is through the web portal at `https://www.ana.gov.br/sar/`. ANA also publishes data through:

- **Portal HidroWeb**: `https://www.snirh.gov.br/hidroweb/` — historical hydrological data
- **Telemetria (Real-time Telemetry)**: `https://www.snirh.gov.br/telemetria/` — real-time hydrological monitoring
- **Open Data Portal**: `https://dados.ana.gov.br/` — ANA's open data portal

The telemetry system may provide a more structured API for real-time data. The SAR portal itself is primarily web-based with reports and dashboards.

ANA's broader SNIRH (Sistema Nacional de Informações sobre Recursos Hídricos) infrastructure is the umbrella system for all water data in Brazil.

## Freshness Assessment

Good for the portal — daily updates of reservoir status. The telemetry system provides sub-daily real-time data for flow and level stations. However, programmatic API access is not well-documented.

## Entity Model

- **Reservoir**: name, river basin, state, capacity (hm³), module (SIN/Nordeste/Other)
- **Observation**: date, storage volume (hm³), percentage full, inflow (m³/s), outflow (m³/s)
- **System**: grouping (SIN, Nordeste, Other)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily updates on portal; real-time via telemetry system |
| Openness | 2 | Public portal; API documentation unclear |
| Stability | 3 | National water agency, operational since 2014 |
| Structure | 1 | Web portal oriented; API discoverability is poor |
| Identifiers | 2 | ANA reservoir/station codes; SNIRH codes |
| Additive Value | 3 | Brazil's massive hydroelectric system — unique global-scale data |
| **Total** | **13/18** | |

## Notes

- Brazil's hydroelectric system is the third-largest in the world, making this data globally significant for energy markets and climate monitoring.
- The main challenge is programmatic access — ANA's systems are oriented toward web portals and PDF reports rather than APIs.
- The `dados.ana.gov.br` open data portal may provide downloadable datasets but not real-time API access.
- The SNIRH telemetry system (`snirh.gov.br/telemetria/`) is the most promising path for real-time data access and warrants further investigation.
- Portuguese language throughout — all documentation, station names, and data labels are in Portuguese.
- The Nordeste reservoir monitoring is particularly important — the region's water crisis has been a major policy issue, and this data directly informs water rationing decisions.
