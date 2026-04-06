# REE e·sios (Spain)

**Country/Region**: Spain (peninsular, Balearic Islands, Canary Islands)
**Publisher**: Red Eléctrica de España (REE) — Spanish TSO
**API Endpoint**: `https://apidatos.ree.es/en/datos/{category}/{widget}`
**Documentation**: https://www.ree.es/en/datos (data portal), https://apidatos.ree.es (API)
**Protocol**: REST
**Auth**: None (open access)
**Data Format**: JSON
**Update Frequency**: 10 minutes (real-time demand), hourly (generation mix)
**License**: Open data

## What It Provides

REE (now part of Redeia) publishes real-time electricity data for Spain through its data portal and API. Spain's grid is interesting due to high renewable penetration (wind + solar) and its position as a connector between continental Europe and North Africa.

Key data categories:

- **Generation structure** — Generation mix by technology (nuclear, wind, solar PV, solar thermal, hydro, combined cycle, coal, cogeneration, waste, biomass, etc.)
- **Real-time demand** — Actual demand, forecast demand, programmed generation
- **Balance** — Electricity balance (generation, consumption, imports, exports)
- **Exchanges** — Cross-border flows with France, Portugal, Morocco, Andorra
- **Emissions** — CO2 emissions from electricity generation
- **Installed capacity** — By technology
- **Market prices** — Spot market prices

## API Details

RESTful API with category/widget URL structure:

```
GET https://apidatos.ree.es/en/datos/generacion/estructura-generacion
    ?start_date=2024-01-01T00:00
    &end_date=2024-01-02T00:00
    &time_trunc=hour
```

Parameters:
- `start_date`, `end_date` — ISO 8601 datetime range
- `time_trunc` — Aggregation: `hour`, `day`, `month`, `year`
- `geo_trunc` — Geographic: `electric_system`
- `geo_limit` — System: `peninsular`, `canarias`, `baleares`, `ceuta`, `melilla`

Response is structured JSON with typed values, units, and metadata.

Note: During testing, the API returned 400 errors suggesting the endpoint structure may have changed or requires specific parameter combinations. The data portal web interface at ree.es/en/datos works and visualizes the data.

## Freshness Assessment

The real-time demand widget updates every 10 minutes. Generation structure updates hourly. The data portal dashboard shows live demand curves. However, the API's current accessibility needs verification — the web portal may be more reliable than direct API calls.

## Entity Model

- **Electric System**: Peninsular (mainland), Canary Islands, Balearic Islands, Ceuta, Melilla
- **Technology**: Nuclear, wind, solar PV, solar thermal, hydro, combined cycle, coal, cogeneration, waste, biomass, fuel-gas
- **Time**: Hourly or 10-minute intervals
- **Values**: MW (generation/demand), MWh (energy), gCO2eq/kWh (emissions)
- **Exchange**: Per border (France, Portugal, Morocco, Andorra)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 10-minute demand, hourly generation — but API accessibility issues |
| Openness | 2 | No auth required but API currently returning errors |
| Stability | 2 | Government TSO but API seems fragile or under revision |
| Structure | 2 | JSON when working, but endpoint reliability is a concern |
| Identifiers | 2 | Spanish technology names, standard but localized |
| Additive Value | 2 | Spain-specific; high renewable share makes it interesting |
| **Total** | **12/18** | |

## Notes

- The API appears to be undergoing changes or requires specific parameter combinations not well-documented in English.
- The web portal at ree.es/en/datos provides excellent visualizations and may be more reliable for data extraction.
- Spain's grid features very high wind and solar penetration, plus unique solar thermal (CSP) generation.
- Cross-border flows with Morocco (via submarine cable) are unique in Europe.
- The e·sios platform (https://www.esios.ree.es/) is a separate, more comprehensive data portal used by market participants — it may have a more stable API.
- Consider ENTSO-E as a more reliable path to Spanish grid data if the direct API remains problematic.
