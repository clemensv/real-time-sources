# Elexon BMRS (Balancing Mechanism Reporting Service)

**Country/Region**: Great Britain (England, Scotland, Wales)
**Publisher**: Elexon Ltd (on behalf of National Grid ESO)
**API Endpoint**: `https://data.elexon.co.uk/bmrs/api/v1/`
**Documentation**: https://data.elexon.co.uk/swagger/index.html (OpenAPI 3.0)
**Protocol**: REST
**Auth**: None (open access, no API key required)
**Data Format**: JSON, XML, CSV
**Update Frequency**: Half-hourly (per settlement period, every 30 minutes)
**License**: Creative Commons CC-BY 4.0

## What It Provides

The BMRS is the UK electricity market's central data publication platform. It publishes granular data on the GB Balancing Mechanism — how the grid is kept in balance in real time.

Key datasets:

- **Generation outturn by fuel type** — Half-hourly generation summary broken down by fuel (CCGT, nuclear, wind, solar, biomass, coal, hydro, oil, OCGT, interconnectors)
- **Balancing mechanism dynamic data** — Per-BMU (Balancing Mechanism Unit) dynamic parameters (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)
- **System prices** — Imbalance prices and system buy/sell prices
- **Demand and forecasts** — National demand outturn and forecasts
- **Interconnector flows** — Flows on interconnectors to France (IFA, IFA2), Netherlands, Belgium, Norway (NSL/VKL), Ireland

## API Details

Fully RESTful API with OpenAPI 3.0 specification. No authentication required.

```
GET https://data.elexon.co.uk/bmrs/api/v1/generation/outturn/summary?format=json
```

Returns current half-hourly generation by fuel type:

```json
[{
  "startTime": "2026-04-05T16:00:00Z",
  "settlementPeriod": 35,
  "data": [
    {"fuelType": "WIND", "generation": 12124},
    {"fuelType": "NUCLEAR", "generation": 5070},
    {"fuelType": "CCGT", "generation": 2525},
    {"fuelType": "BIOMASS", "generation": 953}
  ]
}]
```

Generation values are in MW. Additional endpoints cover balancing actions, system prices, demand forecasts, and per-unit data.

Key endpoints:
- `/generation/outturn/summary` — Current generation mix
- `/balancing/dynamic` — Per-BMU dynamic data
- `/balancing/settlement/system-price` — System prices
- `/demand/outturn` — Demand data

Supports `format=json|xml|csv` query parameter.

## Freshness Assessment

Data is published every 30 minutes aligned to GB settlement periods. The generation summary endpoint returns the latest available periods automatically. Data freshness is excellent — typically within one settlement period of real time. This is a live operational data feed from the grid operator.

## Entity Model

- **Settlement Period**: Half-hour slots numbered 1-50 per day (48 standard, +2 for clock changes)
- **BMU (Balancing Mechanism Unit)**: Individual generating units identified by NGC or Elexon IDs (e.g., `2__HFLEX001`)
- **Fuel Type**: WIND, NUCLEAR, CCGT, BIOMASS, COAL, OCGT, OIL, NPSHYD, INTFR, INTNED, INTNEM, INTELEC, INTIFA2, INTVKL, OTHER
- **Generation**: MW output per settlement period

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Half-hourly, near-real-time |
| Openness | 3 | No authentication needed, CC-BY license |
| Stability | 3 | Regulated market operator, OpenAPI spec, versioned API |
| Structure | 3 | Clean JSON/XML/CSV, OpenAPI 3.0 documented |
| Identifiers | 3 | Standard BMU IDs, NGESO fuel type codes |
| Additive Value | 3 | Deep balancing mechanism data unique to GB market |
| **Total** | **18/18** | |

## Notes

- No API key required — fully open access, which is exceptional for a market data platform.
- The Swagger/OpenAPI spec at `/swagger/v1/swagger.json` enables auto-generated client code.
- Rate limiting is in place (HTTP 429) but generous for reasonable use.
- This replaces the legacy BMRS API (bmreports.com) which required registration.
- Interconnector data provides cross-border flow visibility (France, Netherlands, Belgium, Norway).
- Consider pairing with the Carbon Intensity API (separate candidate) for emissions context.
