# Energy & Electricity Grid — Candidate Data Sources

Scouted: 2026-04-06

This index covers real-time electricity generation, load, pricing, and grid data APIs from around the world.

**Already implemented in repo**: `entsoe/` (ENTSO-E Transparency Platform — European TSOs)

## Candidate Summary

| # | Slug | Source | Region | Freshness | Open? | Score | Priority |
|---|------|--------|--------|-----------|-------|-------|----------|
| 1 | [eia-grid-monitor](eia-grid-monitor.md) | US EIA Hourly Electric Grid Monitor | US (all BAs) | Hourly | API key (free) | **18/18** | ★★★ |
| 2 | [elexon-bmrs](elexon-bmrs.md) | Elexon BMRS | Great Britain | 30 min | No auth | **18/18** | ★★★ |
| 3 | [carbon-intensity-uk](carbon-intensity-uk.md) | Carbon Intensity API (NGESO) | Great Britain | 30 min | No auth | **17/18** | ★★★ |
| 4 | [energidataservice-dk](energidataservice-dk.md) | Energi Data Service (Energinet) | Denmark + Nordics | 1 min | No auth | **17/18** | ★★★ |
| 5 | [rte-eco2mix](rte-eco2mix.md) | RTE éCO2mix | France | 15 min | Quota | **16/18** | ★★☆ |
| 6 | [aemo-nemweb](aemo-nemweb.md) | AEMO NEMWeb | Australia (NEM) | 5 min | Public files | **16/18** | ★★☆ |
| 7 | [fingrid](fingrid.md) | Fingrid Open Data | Finland | 3 min | API key (free) | **15/18** | ★★☆ |
| 8 | [electricity-maps](electricity-maps.md) | Electricity Maps API | Global (~200 zones) | 5-15 min | Commercial | **15/18** | ★☆☆ |
| 9 | [nyiso](nyiso.md) | NYISO MIS | New York State | 5 min | Public files | **15/18** | ★☆☆ |
| 10 | [pjm-data-miner](pjm-data-miner.md) | PJM Data Miner 2 | Eastern US (13 states) | Hourly | Free account | **14/18** | ★☆☆ |
| 11 | [caiso-oasis](caiso-oasis.md) | CAISO OASIS | California | 5 min | Public | **14/18** | ★☆☆ |
| 12 | [ieso-ontario](ieso-ontario.md) | IESO Data Directory | Ontario, Canada | 5 min | Public files | **14/18** | ★☆☆ |
| 13 | [ercot](ercot.md) | ERCOT MIS | Texas | 5-15 min | Public (403 issues) | **14/18** | ★☆☆ |
| 14 | [ree-esios](ree-esios.md) | REE e·sios | Spain | 10 min | API issues | **12/18** | ☆☆☆ |

## Tier 1 — Implement First

These sources have clean JSON APIs, no or minimal auth, excellent freshness, and broad coverage:

### EIA Grid Monitor (eia-grid-monitor.md) — **18/18**
The single most valuable source for US electricity data. One REST API covers all ~70 US balancing authorities with hourly demand, generation by fuel type, and interchange. Free API key, clean JSON, well-documented. This alone supersedes the need for individual CAISO/ERCOT/PJM/NYISO/MISO/SPP/ISO-NE integrations for most use cases.

### Elexon BMRS (elexon-bmrs.md) — **18/18**
The UK's electricity market data platform. No auth required, clean JSON/XML/CSV, OpenAPI 3.0 spec. Half-hourly generation by fuel type, balancing mechanism data, system prices. Verified working with live data.

### Carbon Intensity UK (carbon-intensity-uk.md) — **17/18**
Beautifully designed, zero-auth REST API for GB carbon intensity with regional breakdown across 17 DNO areas. Pairs perfectly with Elexon BMRS.

### Energi Data Service (energidataservice-dk.md) — **17/18**
Denmark's minute-by-minute power system data. No auth, clean JSON, with real-time CO2, wind, solar, exchange flows, and Nordic spot prices. Verified working endpoint.

## Tier 2 — Strong Candidates

### RTE éCO2mix (rte-eco2mix.md) — **16/18**
France's 15-minute generation mix with exceptional sub-fuel detail (3 types of hydro, 3 types of gas, on/offshore wind). Opendatasoft API. Quota limit of 50k calls/month.

### AEMO NEMWeb (aemo-nemweb.md) — **16/18**
Australia's 5-minute dispatch data. File-based (CSV in ZIP) rather than JSON API, but uniquely valuable for Southern Hemisphere coverage and very high renewable penetration data.

### Fingrid (fingrid.md) — **15/18**
Finland's TSO with 3-minute real-time data including grid frequency. Free API key required. Good Nordic coverage complement to Energi Data Service.

## Tier 3 — Lower Priority

### Electricity Maps (electricity-maps.md) — **15/18**
Global aggregator with ~200 zones. Commercial license for production use. Better to go to primary sources directly unless global coverage is specifically needed.

### US ISOs: NYISO, PJM, CAISO, ERCOT — **14-15/18**
All provide granular zonal/nodal data, but EIA Grid Monitor covers their BA-level data in a single clean API. These are only needed for nodal pricing or market-specific data not in EIA.

### IESO Ontario (ieso-ontario.md) — **14/18**
Canadian coverage. XML-only file-based system. Useful for Canada-US grid interconnection context.

### REE e·sios (ree-esios.md) — **12/18**
Spanish grid data. API was returning errors during testing — may need direct investigation or use ENTSO-E as alternative path.

## Not Individually Documented (Covered by Other Sources)

| Source | Why Not Separate | Covered By |
|--------|------------------|------------|
| MISO | EIA covers MISO hourly data | eia-grid-monitor |
| SPP | EIA covers SPP hourly data | eia-grid-monitor |
| ISO-NE | EIA covers ISNE hourly data | eia-grid-monitor |
| Nord Pool | Prices available via Energi Data Service | energidataservice-dk |
| Statnett (Norway) | Refers to ENTSO-E for data; statistics delayed 2+ months | entsoe |
| Svenska Kraftnät (Sweden) | Statistics delayed, no real-time API | entsoe |
| National Grid ESO (UK) | Data portal inaccessible; carbon-intensity-uk + elexon-bmrs cover GB | carbon-intensity-uk, elexon-bmrs |
| Open Power System Data | Historical bulk downloads, not real-time | N/A (reference data) |

## Geographic Coverage Map

```
Americas:     EIA (US-wide), IESO (Ontario), NYISO/PJM/CAISO/ERCOT (US nodal)
Europe:       ENTSO-E (pan-EU), Elexon+Carbon Intensity (GB), Energinet (DK),
              RTE (FR), Fingrid (FI), REE (ES)
Asia-Pacific: AEMO (Australia)
Global:       Electricity Maps (aggregator)
```

## Recommended Implementation Order

1. **eia-grid-monitor** — Unlocks all US balancing authorities in one integration
2. **elexon-bmrs** — UK market data, no auth, instant access
3. **carbon-intensity-uk** — UK carbon intensity, pairs with Elexon
4. **energidataservice-dk** — Danish/Nordic real-time grid, no auth
5. **rte-eco2mix** — French generation mix
6. **aemo-nemweb** — Australian NEM (different format, broader coverage)
7. **fingrid** — Finnish TSO data
8. Remaining candidates as needed for specific regional coverage
