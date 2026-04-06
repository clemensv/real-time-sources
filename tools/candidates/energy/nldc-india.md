# NLDC/Grid-India — National Load Despatch Centre (India)

**Country/Region**: India (national grid)
**Publisher**: Grid-India (formerly POSOCO — Power System Operation Corporation)
**API Endpoint**: `https://nrldc.in/` (and regional LDCs: srldc.in, wrldc.in, erldc.in, nerldc.in)
**Documentation**: https://nrldc.in, https://www.grid-india.in
**Protocol**: REST / file downloads
**Auth**: None for public dashboards
**Data Format**: JSON (dashboard widgets), PDF/Excel (reports)
**Update Frequency**: 5-15 minutes (dashboard), daily (reports)
**License**: Publicly accessible (Indian government entity)

## What It Provides

Grid-India (rebranded from POSOCO in 2023) operates India's national grid through five Regional Load Despatch Centres (RLDCs) coordinated by the National Load Despatch Centre (NLDC). India has the world's third-largest electricity grid.

Available data:

- **All-India Generation**: Total generation by fuel type (thermal, hydro, nuclear, renewable)
- **Regional breakdown**: Five regions — Northern (NRLDC), Southern (SRLDC), Western (WRLDC), Eastern (ERLDC), North-Eastern (NERLDC)
- **Demand/supply**: Real-time system demand and supply balance
- **Frequency**: Grid frequency (50 Hz target, typically 49.90-50.05)
- **Interchange**: Inter-regional power flows
- **Renewable generation**: Real-time wind and solar output (rapidly growing)
- **Merit order dispatch**: Which generators are running and in what priority

## API Details

The NLDC websites serve dashboard widgets via internal JSON APIs. During testing, the endpoints were unreachable:

```
GET https://nrldc.in/api/getWidgetData?widgetName=ALLINDIAGENERATION → Connection failed
```

The sites may be geo-restricted or experiencing connectivity issues from outside India. Alternative data access paths:

1. **MERIT India** (http://meritindia.in/) — Merit order dispatch data with API
2. **Renewable Energy Certificate** portal — REC trading data
3. **Vidyut PRAVAH** app — Government's real-time power sector dashboard (available on Google Play/App Store, may have underlying API)
4. **National Power Portal** (https://npp.gov.in/) — Generation and transmission data

## Freshness Assessment

Dashboard data on NLDC sites updates every 5-15 minutes when accessible. Daily reports are published the following morning. India's growing real-time data infrastructure is improving freshness, but many datasets are still delivered as daily PDF/Excel reports.

## Entity Model

- **Region**: NR (Northern), SR (Southern), WR (Western), ER (Eastern), NER (North-Eastern)
- **State**: Individual Indian state data (each state has a State Load Despatch Centre)
- **Fuel Type**: Thermal (coal, gas, diesel, lignite), Hydro, Nuclear, Renewable (wind, solar, small hydro, biomass)
- **Generator**: Individual plant names and IDs
- **Time**: IST (UTC+5:30)
- **Values**: MW

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 5-15 min on dashboards, but programmatic access unverified |
| Openness | 1 | Endpoints unreachable from outside India; may be geo-restricted |
| Stability | 2 | Government entity, but infrastructure reliability is variable |
| Structure | 1 | Dashboard-only access observed; no public API documentation |
| Identifiers | 2 | Standard Indian grid region codes, plant IDs |
| Additive Value | 3 | India is world's 3rd largest grid, no other programmatic source |
| **Total** | **11/18** | |

## Notes

- India's grid is undergoing a massive transformation: coal still dominates (~70% of thermal capacity) but solar is growing explosively (target: 500 GW renewable by 2030).
- The grid operates at 50 Hz but historically with wider frequency excursions than European grids — frequency data is particularly interesting.
- India's regional load dispatch structure (5 RLDCs) mirrors the country's electrical geography and inter-regional transfer constraints.
- The MERIT India portal (meritindia.in) may provide a more accessible API for merit order and dispatch data.
- Alternative: IEX (Indian Energy Exchange) at iexindia.com provides market clearing prices and volumes — may have a more accessible API.
- The Vidyut PRAVAH mobile app's backend API could be reverse-engineered for real-time data access.
