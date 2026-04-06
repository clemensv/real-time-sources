# COES — Comité de Operación Económica del Sistema (Peru)

**Country/Region**: Peru
**Publisher**: COES SINAC (Committee for the Economic Operation of the National Interconnected System)
**API Endpoint**: `https://www.coes.org.pe/Portal/portalinformacion/` (information portal)
**Documentation**: https://www.coes.org.pe/Portal/portalinformacion/generacion (Spanish)
**Protocol**: Web portal with embedded charts and file downloads
**Auth**: None for public data
**Data Format**: Excel, CSV (downloads); JavaScript/JSON (dashboard)
**Update Frequency**: Hourly (generation), daily (prices)
**License**: Publicly accessible (Peruvian regulatory requirement)

## What It Provides

COES operates Peru's electricity system (SEIN — Sistema Eléctrico Interconectado Nacional) and administers the wholesale market. Peru's grid has excellent hydro resources and growing solar/wind.

Available data:

- **Generation**: By fuel type (hydro, thermal/gas, wind, solar, biomass) and by individual plant
- **Demand**: System demand by area
- **Marginal cost**: Short-run marginal cost (CMCP) — effectively the spot price
- **Reservoir levels**: Hydro storage across major reservoirs
- **Interchange**: Cross-border flows with Ecuador
- **Frequency**: System frequency
- **Transmission**: Major line flows and congestion

## API Details

COES's data portal is primarily web-based with interactive charts (likely Highcharts or similar). Data can be downloaded as Excel/CSV from the portal pages:

```
https://www.coes.org.pe/Portal/portalinformacion/generacion
https://www.coes.org.pe/Portal/portalinformacion/demanda
https://www.coes.org.pe/Portal/PostOperacion/costosmarg
```

Behind the portal, API calls may be made to backend services for chart data (common pattern — would need browser developer tools to identify endpoints).

No formal REST API documentation has been found. Data access is primarily through the web portal or file downloads.

## Freshness Assessment

Generation data is published with a delay of 1-2 hours (post-operation data). Marginal costs are published daily for the previous day. The portal dashboard shows near-real-time data during active monitoring hours.

## Entity Model

- **System**: SEIN (National Interconnected Electrical System)
- **Area**: Norte (North), Centro (Central), Sur (South)
- **Plant**: Individual generating stations
- **Fuel Type**: Hidráulica, Térmica (gas, diesel), Eólica, Solar, Biomasa
- **Price**: CMCP in USD/MWh (Peru's electricity market uses US dollars)
- **Time**: PET (Peru Time, UTC-5)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 1-2 hour lag for generation, daily for prices |
| Openness | 2 | Public data, but portal-based downloads only |
| Stability | 2 | Government-mandated entity, established since 1993 |
| Structure | 1 | Web portal with file downloads, no REST API |
| Identifiers | 2 | COES-specific plant and area codes |
| Additive Value | 2 | Peru's grid is interesting but small; limited global significance vs. Brazil/Mexico |
| **Total** | **11/18** | |

## Notes

- Peru's electricity market prices in USD (unusual for a non-dollarized economy), making price data directly comparable internationally.
- The Camisea natural gas pipeline transformed Peru's generation mix from hydro-dominated to a mix of hydro and gas.
- Peru is interconnected with Ecuador, and future interconnections with Colombia and Chile are planned.
- For Latin American grid coverage, ONS Brazil and XM Colombia are higher-priority implementations.
- The portal's chart data endpoints could potentially be reverse-engineered for programmatic access.
