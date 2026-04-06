# ERCOT (Electric Reliability Council of Texas)

**Country/Region**: Texas, United States
**Publisher**: ERCOT (Electric Reliability Council of Texas)
**API Endpoint**: `https://www.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId={id}` (MIS)
**Documentation**: https://www.ercot.com/mp/data-products
**Protocol**: HTTP file download + JSON listing endpoint
**Auth**: None for public data (some feeds require market participant account)
**Data Format**: CSV (inside ZIP), XML
**Update Frequency**: 5 minutes (real-time), 15 minutes (system-wide), hourly (prices)
**License**: Public data

## What It Provides

ERCOT operates the Texas grid — the only US state with its own independent grid (not interconnected with the Eastern or Western Interconnections). This makes Texas uniquely self-contained for energy analysis.

Key data categories:

- **System-wide generation by fuel type** — Real-time generation from wind, solar, natural gas, coal, nuclear, hydro, other
- **Real-time prices** — Settlement Point Prices (SPP) at zonal and nodal levels
- **System load** — Actual and forecast system demand
- **Wind/solar generation** — Real-time and forecast output for wind and solar farms
- **Operating reserves** — Responsive reserve, regulation, and non-spinning reserve
- **Outage schedules** — Generation and transmission outage data
- **Ancillary services** — Market clearing prices for reserves

## API Details

ERCOT's data is accessed through the Market Information System (MIS). Reports are listed via a JSON web service:

```
GET https://www.ercot.com/misapp/servlets/IceDocListJsonWS?reportTypeId=13089
```

This returns a JSON listing of available report files (CSV/ZIP) for download. Each report type has a numeric ID.

Key report type IDs:
- 13089 — System-wide Generation by Fuel Type
- 12301 — Real-Time Settlement Point Prices
- 12311 — Day-Ahead Settlement Point Prices
- 13101 — Wind Power Production (actual + forecast)
- 13103 — Solar Power Production
- 12312 — Real-Time System Load

Note: During testing, ercot.com returned 403 errors — the site may use Cloudflare protection or require browser-like headers.

## Freshness Assessment

ERCOT's grid data updates every 5-15 minutes for real-time metrics. System-wide generation by fuel type is published roughly every 15 minutes. Wind and solar forecasts are published hourly. Price data settles every 15 minutes. Texas's isolation means ERCOT is the sole and definitive source for all Texas grid data.

## Entity Model

- **Settlement Point**: Pricing locations (zonal hubs: HB_HOUSTON, HB_NORTH, HB_SOUTH, HB_WEST, etc.)
- **Fuel Type**: Wind, Solar, Natural Gas, Coal, Nuclear, Hydro, Power Storage, Other
- **Load Zone**: 8 weather zones + 4 hub nodes
- **Time**: 15-minute settlement intervals, Central Time

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-15 minute real-time data |
| Openness | 2 | Public but 403 access issues, report-type IDs needed |
| Stability | 3 | Regulatory-mandated grid operator, critical infrastructure |
| Structure | 1 | CSV-in-ZIP via report listing JSON — multi-step access |
| Identifiers | 2 | ERCOT-specific settlement point names |
| Additive Value | 3 | Texas is its own isolated grid — unique coverage |
| **Total** | **14/18** | |

## Notes

- Texas operates as an energy-only market (no capacity market), making price spikes during scarcity events extreme — prices can reach $5,000/MWh or higher.
- The EIA Grid Monitor (`respondent=ERCO`) provides hourly demand, generation, and fuel mix for ERCOT in clean JSON format. Use ERCOT directly for settlement-level price data and more granular wind/solar forecasts.
- The 403 errors from ercot.com may require user-agent spoofing or direct download of known file URLs.
- ERCOT has the highest wind generation capacity in the US and rapidly growing solar — fascinating for renewable energy tracking.
- The February 2021 winter storm (Uri) and subsequent market reforms make ERCOT data particularly interesting for resilience analysis.
