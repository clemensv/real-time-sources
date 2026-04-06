# AESO — Alberta Electric System Operator (Canada)

**Country/Region**: Alberta, Canada
**Publisher**: AESO (Alberta Electric System Operator)
**API Endpoint**: `https://api.aeso.ca/report/v1/` (also `https://www.aeso.ca/ets/`)
**Documentation**: https://api.aeso.ca (developer portal)
**Protocol**: REST
**Auth**: API key (free registration at AESO developer portal)
**Data Format**: JSON, CSV
**Update Frequency**: 1 minute (real-time merit order), hourly (pool price)
**License**: Publicly accessible (Alberta regulatory requirement)

## What It Provides

AESO operates the wholesale electricity market and manages the transmission grid for the province of Alberta, Canada. Alberta's deregulated energy-only market has unique characteristics — it's the only province with a fully competitive wholesale market.

Available data:

- **Pool Price**: Real-time wholesale electricity price ($/MWh) — updates every minute
- **Supply/Demand**: Current generation and load, real-time merit order
- **Generation by fuel type**: Coal (being phased out), gas, wind, solar, hydro, biomass, other
- **Current Supply Demand (CSD)**: Real-time generation by individual plant
- **Interchange**: Cross-border flows with BC, Saskatchewan, and Montana (US)
- **Forecast**: Short-term demand and price forecasts
- **Adequacy**: System reserve margins and alerts

## API Details

The AESO developer portal at `api.aeso.ca` provides a REST API requiring a free API key:

```
GET https://api.aeso.ca/report/v1/csd/generation/current
Headers:
  X-API-Key: YOUR_KEY
```

The website at `aeso.ca/ets/` also serves data as JSON via its Energy Trading System (ETS) display:

```
GET https://www.aeso.ca/ets/ets?contentType=json
→ (Returns HTML-like content with generation/demand data)
```

During testing, `api.aeso.ca` was unreachable (connection refused), while `www.aeso.ca/ets/` returned a response with generation and capacity data (though the response format was unclear — possibly HTML mixed with data).

## Freshness Assessment

Pool price and merit order data update every minute. Generation data updates in real-time. Alberta's market settles at 1-minute intervals (unique among North American ISOs — most use 5-minute intervals), making AESO's data exceptionally granular.

## Entity Model

- **Pool Price**: $/MWh (Canadian dollars), per minute
- **Generator**: Individual plant IDs with fuel type, capacity, and current output
- **Fuel Type**: Gas, Coal, Wind, Solar, Hydro, Biomass, Other, Dual Fuel
- **Interchange**: BC, SK, MT flows in MW
- **Time**: Mountain Time (UTC-7/UTC-6 DST)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 1-minute pool price, real-time generation |
| Openness | 2 | Free API key required; API was unreachable during testing |
| Stability | 2 | Government-mandated, but API connectivity issues observed |
| Structure | 2 | API endpoint returned connection errors; ETS page format unclear |
| Identifiers | 2 | Generator codes are AESO-specific, standard fuel types |
| Additive Value | 3 | Only source for Alberta's unique energy-only market; Canadian gap coverage |
| **Total** | **14/18** | |

## Notes

- Alberta's electricity market is unique in North America: energy-only (no capacity market), 1-minute settlement, and highly gas-dependent with rapidly growing wind and solar.
- The `api.aeso.ca` domain may have been experiencing temporary issues during testing. The developer portal typically provides good documentation and a straightforward API key registration process.
- Alberta is not covered by EIA Grid Monitor (US only) and only partially by IESO (Ontario only).
- For Canadian coverage: AESO (Alberta) + IESO (Ontario) + BC Hydro + Hydro-Québec would provide comprehensive cross-Canada grid data.
- AESO data is also consumed by WattTime for Alberta marginal emissions calculations.
