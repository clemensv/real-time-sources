# XM — Operador del Sistema y Administrador del Mercado (Colombia)

**Country/Region**: Colombia
**Publisher**: XM S.A. E.S.P. (Colombian system operator and market administrator)
**API Endpoint**: `https://servapibi.xm.com.co/` (business intelligence API)
**Documentation**: https://www.xm.com.co/consumo/en/information-portal
**Protocol**: REST (Power BI-backed)
**Auth**: None for public portal data
**Data Format**: JSON
**Update Frequency**: Hourly (generation/demand), daily (prices)
**License**: Publicly accessible (Colombian regulatory requirement)

## What It Provides

XM operates Colombia's National Interconnected System (SIN) and administers the wholesale electricity market. Colombia's grid is ~70% hydroelectric, making it highly sensitive to weather patterns — especially El Niño/La Niña cycles.

Available data:

- **Generation**: By fuel type (hydro, thermal, wind, solar, biomass, cogeneration) and by plant
- **Demand**: National and regional demand
- **Spot price (Bolsa)**: Hourly wholesale electricity price (COP/kWh)
- **Contract prices**: Bilateral contract market data
- **Reservoirs**: Hydro reservoir levels (critical for a hydro-dominated system)
- **Interchange**: Cross-border flows with Ecuador and Venezuela
- **Losses**: Transmission and distribution losses
- **Reliability charges**: Capacity market data

## API Details

XM's data portal uses Power BI as its backend, with data accessible through a business intelligence API:

```
POST https://servapibi.xm.com.co/hourly
Content-Type: application/json

{
  "MetricId": "Gene",
  "StartDate": "2025-06-01",
  "EndDate": "2025-06-01",
  "Entity": "Sistema"
}
```

The API uses POST requests with metric identifiers. Known MetricIds include:
- `Gene` — Generation
- `DemaSIN` — System demand
- `PrecBolsa` — Spot price
- `AporEner` — Energy contributions (reservoir inflows)
- `VolUtil` — Useful reservoir volume

XM also provides data through their public portal at sinergox.xm.com.co and their main website's information section.

## Freshness Assessment

Generation and demand data updates hourly. Spot prices are published for the previous day. Reservoir levels update daily. The data reflects the actual dispatch of Colombia's grid with a lag of a few hours for generation data.

## Entity Model

- **System**: SIN (National Interconnected System), ZNI (Non-Interconnected Zones)
- **Agent**: Individual generators and retailers
- **Plant**: Power plant name and fuel type
- **Resource**: Individual generating unit
- **Metric**: Generation (MWh), Demand (MWh), Price (COP/kWh), Volume (GWh of reservoir)
- **Time**: Colombia time (UTC-5, no DST)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly generation, daily prices |
| Openness | 2 | Public data, POST-based API (no auth), but Power BI backend adds complexity |
| Stability | 2 | Government-mandated entity, but Power BI backend could be restructured |
| Structure | 2 | JSON responses, but Power BI wrapper adds unpredictability |
| Identifiers | 2 | XM-specific plant and agent codes |
| Additive Value | 3 | Only source for Colombia's grid — major Latin American hydro economy |
| **Total** | **13/18** | |

## Notes

- Colombia's grid is a fascinating case: ~70% hydro means El Niño events (which reduce rainfall) can trigger energy crises — the country has experienced electricity rationing during severe droughts.
- The cross-border flows with Ecuador and Venezuela reflect complex geopolitical and economic dynamics.
- XM's data quality is generally good — Colombia has a well-regulated electricity market by Latin American standards.
- The Power BI-backed API is unusual but functional — it's essentially a business intelligence query interface rather than a traditional REST API.
- Consider XM alongside ONS Brazil and CENACE Mexico for comprehensive Latin American grid coverage.
