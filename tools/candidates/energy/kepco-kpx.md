# KEPCO — Korea Electric Power Corporation (South Korea)

**Country/Region**: South Korea
**Publisher**: KEPCO (Korea Electric Power Corporation) / KPX (Korea Power Exchange)
**API Endpoint**: `https://openapi.kpx.or.kr/` (KPX Open API)
**Documentation**: https://openapi.kpx.or.kr (Korean language)
**Protocol**: REST
**Auth**: API key (free registration, Korean portal)
**Data Format**: JSON, XML
**Update Frequency**: 5 minutes (real-time), hourly (prices)
**License**: Publicly accessible (Korean government open data policy)

## What It Provides

KPX (Korea Power Exchange) operates South Korea's electricity market under KEPCO, the vertically integrated state utility. South Korea has the world's 9th largest electricity generation capacity and a uniquely structured market.

Available data via KPX Open API:

- **Real-time generation**: By fuel type (nuclear, coal, LNG, oil, hydro, renewable, pumped storage)
- **System demand**: Real-time electricity demand
- **SMP (System Marginal Price)**: Electricity wholesale price by settlement period
- **Reserve margin**: Operating reserves and system adequacy
- **Power trading**: Market clearing quantities and prices
- **Renewable generation**: Wind and solar output (growing rapidly from a low base)

South Korea's Open Data Portal (data.go.kr) also provides electricity-related datasets from multiple agencies.

## API Details

The KPX Open API requires registration at their portal (Korean language):

```
GET https://openapi.kpx.or.kr/openapi/realTimeGenerating
    ?serviceKey=YOUR_KEY
```

The registration process is through data.go.kr (Korea's central open data portal) and requires a Korean-language account setup. Documentation is primarily in Korean.

Alternative access: Korea's open data portal (data.go.kr) indexes KPX datasets alongside data from KEPCO, MOTIE (Ministry of Trade, Industry and Energy), and the Korea Energy Agency.

## Freshness Assessment

Real-time generation data updates every 5 minutes. SMP prices are settled hourly. Forecast data is published day-ahead. The KPX operates a centralized dispatch model, so data reflects the actual dispatch decisions.

## Entity Model

- **Fuel Type**: Nuclear (원자력), Coal (석탄), LNG (가스), Oil (유류), Hydro (수력), Renewable (신재생), Pumped Storage (양수)
- **Price**: SMP in KRW/kWh (Korean won per kilowatt-hour)
- **Region**: Single price zone (South Korea operates as one market zone)
- **Time**: KST (UTC+9)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute real-time updates |
| Openness | 2 | Free API key via data.go.kr; registration in Korean |
| Stability | 3 | Government-backed (KEPCO is state-owned), formal open data portal |
| Structure | 2 | JSON/XML API, but documentation is Korean-language only |
| Identifiers | 2 | KPX-specific codes, Korean fuel type names |
| Additive Value | 3 | Only source for South Korea's grid — 9th largest globally, nuclear-heavy |
| **Total** | **15/18** | |

## Notes

- South Korea's generation mix is unique: ~30% nuclear, ~40% coal/gas, with aggressive targets for renewable growth (nuclear renaissance + offshore wind).
- The single-price-zone market structure is simpler than multi-zone European markets.
- Korean-language documentation is the main barrier for non-Korean developers.
- KEPCO's vertically integrated structure (generation, transmission, distribution, retail) means KPX data effectively covers the entire power sector.
- South Korea's electricity demand pattern is highly seasonal (summer cooling, winter heating) and industrially driven (Samsung, Hyundai, POSCO steel, etc.).
