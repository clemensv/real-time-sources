# Energy-Charts API (Fraunhofer ISE)

**Country/Region**: Pan-European (40+ countries)
**Publisher**: Fraunhofer Institute for Solar Energy Systems (ISE)
**API Endpoint**: `https://api.energy-charts.info/`
**Documentation**: https://api.energy-charts.info (Swagger UI with OpenAPI 3.1 spec)
**Protocol**: REST
**Auth**: None (public, rate-limited; commercial access available)
**Data Format**: JSON
**Update Frequency**: 15 minutes (quarter-hourly resolution for DE; hourly for most others)
**License**: CC BY 4.0 (attribution to Energy-Charts.info required)

## What It Provides

This is arguably the single most valuable European electricity data API outside of ENTSO-E. Fraunhofer ISE aggregates data from ENTSO-E, national TSOs, and Bundesnetzagentur into a clean, unified REST API covering 40+ countries with no authentication required.

Endpoints:

- `/public_power` — Net electricity production by fuel type (solar, wind onshore/offshore, nuclear, lignite, hard coal, gas, hydro run-of-river, hydro reservoir, pumped storage, biomass, geothermal, waste, others). Also returns load, residual load, and renewable share of generation/load.
- `/public_power_forecast` — Forecasts for solar, wind onshore, wind offshore, and load (current, intraday, day-ahead)
- `/total_power` — Total net production including industrial self-supply (Germany only)
- `/installed_power` — Installed capacity by fuel type, annual
- `/price` — Day-ahead spot prices by bidding zone (40+ zones: DE-LU, AT, FR, ES, NL, NO1-NO5, SE1-SE4, DK1/DK2, IT subzones, etc.)
- `/cbet` — Cross-border electricity trading (commercial schedules) between countries
- `/cbpf` — Cross-border physical flows
- `/signal` — Grid carbon signal (traffic light: 0=green/use now, 1=yellow, 2=red/reduce)
- `/ren_share_forecast` — Renewable share forecast with solar/wind onshore/offshore breakdown

Available countries include: de, at, ch, nl, be, fr, es, pt, it, gr, pl, cz, hu, dk, se, no, fi, ee, lt, lv, ie, uk, bg, hr, ro, rs, si, sk, ba, me, mk, al, cy, mt, ge, am, az, by, md, ua, ru, xk, lu, tr — plus `eu` (European Union aggregate) and `all` (all of Europe).

## API Details

Simple query-string parameters, no auth headers:

```
GET https://api.energy-charts.info/public_power
    ?country=de
    &start=2025-06-01T00:00+02:00
    &end=2025-06-01T01:00+02:00
```

Timestamps support ISO 8601 (with timezone), daily format (`2025-06-01`), or UNIX seconds. If no dates provided, returns current day.

Response:

```json
{
  "unix_seconds": [1748728800, 1748729700, 1748730600, ...],
  "production_types": [
    {"name": "Wind onshore", "data": [7665.4, 7910.9, 8334.1, ...]},
    {"name": "Solar", "data": [0.0, 0.0, 0.0, ...]},
    {"name": "Fossil gas", "data": [2760.2, 2662.1, 2450.8, ...]},
    {"name": "Load", "data": [37867.0, 37261.1, 36759.7, ...]},
    {"name": "Renewable share of generation", "data": [52.0, 53.9, 56.1, ...]}
  ],
  "deprecated": false
}
```

Price endpoint:

```
GET https://api.energy-charts.info/price?bzn=DE-LU&start=2025-06-01&end=2025-06-01
→ {"unix_seconds": [...], "price": [92.53, 85.22, ...], "unit": "EUR / MWh"}
```

Signal endpoint:

```
GET https://api.energy-charts.info/signal?country=de
→ {"unix_seconds": [...], "share": [...], "signal": [2, 2, ..., 1, 1, 0, 0, ...]}
```

Cross-border flows:

```
GET https://api.energy-charts.info/cbet?country=de&start=2025-06-01&end=2025-06-01
→ {"unix_seconds": [...], "countries": [{"name": "Austria", "data": [...]}, {"name": "France", "data": [...]}, ...]}
```

## Freshness Assessment

Quarter-hourly (15-min) resolution for Germany and several major countries; hourly for smaller countries. Data typically available within 15-60 minutes of real time. Forecasts (solar, wind, load) extend into the future. The `deprecated` flag on each response gives advance warning before endpoint changes — they promise 6 months' notice.

## Entity Model

- **Country**: ISO 3166-1 alpha-2 codes (de, at, fr, etc.) plus special codes (eu, all, nie)
- **Bidding Zone**: European bidding zone codes (DE-LU, NO1-NO5, SE1-SE4, DK1, DK2, IT-North, etc.)
- **Production Type**: Standardized fuel type names (consistent across countries)
- **Time**: UNIX seconds array — parallel to data arrays
- **Value**: MW (generation/load) or EUR/MWh (prices) or percentage (renewable shares)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15-min resolution for major countries, hourly for others |
| Openness | 3 | No auth required, CC BY 4.0, public rate limits |
| Stability | 3 | Fraunhofer ISE (German government research institute), OpenAPI 3.1 spec, versioned releases |
| Structure | 3 | Clean JSON, consistent schema across all endpoints and countries |
| Identifiers | 3 | Standard ISO country codes, European bidding zone codes |
| Additive Value | 3 | 40+ countries in ONE API — massively simplifies European coverage |
| **Total** | **18/18** | |

## Notes

- This is the European equivalent of EIA Grid Monitor — one API to rule them all.
- Verified working with live data for DE, AT, CH, NL, PL, IT, HU, CZ, NO, SE, ES, GR, DK, and others.
- For many individual European TSOs (TenneT, 50Hertz, Amprion, TransnetBW, APG, PSE, ČEPS, MAVIR, ADMIE, Swissgrid), this API provides their generation data in a unified format — no need for individual TSO integrations.
- Price data includes attribution to Bundesnetzagentur / SMARD.de in the response.
- Rate limits apply for public access. Contact `leonhard.gandhi@ise.fraunhofer.de` for commercial/higher-volume access.
- Turkey (tr) is listed but returned 400 during testing — may have limited data availability.
- The `/signal` endpoint is a ready-made "when to use electricity" indicator — green/yellow/red based on renewable share.
- Cross-border flow data (`/cbet`, `/cbpf`) is exceptionally useful for understanding European grid interconnection.
