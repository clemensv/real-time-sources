# Energy & Electricity Grid — Candidate Data Sources

Scouted: 2026-04-06, expanded 2026-07-15

This index covers real-time electricity generation, load, pricing, and grid data APIs from around the world.

**Already implemented in repo**: `entsoe/` (ENTSO-E Transparency Platform — European TSOs)

## Candidate Summary

| # | Slug | Source | Region | Freshness | Open? | Score | Priority |
|---|------|--------|--------|-----------|-------|-------|----------|
| 1 | [eia-grid-monitor](eia-grid-monitor.md) | US EIA Hourly Electric Grid Monitor | US (all BAs) | Hourly | API key (free) | **18/18** | ★★★ |
| 2 | [elexon-bmrs](elexon-bmrs.md) | Elexon BMRS | Great Britain | 30 min | No auth | **18/18** | ★★★ |
| 3 | [energy-charts-info](energy-charts-info.md) | Energy-Charts API (Fraunhofer ISE) | Pan-European (40+ countries) | 15 min | No auth | **18/18** | ★★★ |
| 4 | [carbon-intensity-uk](carbon-intensity-uk.md) | Carbon Intensity API (NGESO) | Great Britain | 30 min | No auth | **17/18** | ★★★ |
| 5 | [energidataservice-dk](energidataservice-dk.md) | Energi Data Service (Energinet) | Denmark + Nordics | 1 min | No auth | **17/18** | ★★★ |
| 6 | [rte-eco2mix](rte-eco2mix.md) | RTE éCO2mix | France | 15 min | Quota | **16/18** | ★★☆ |
| 7 | [ons-brazil](ons-brazil.md) | ONS Brazil | Brazil (4 subsystems) | ~1 min | No auth | **16/18** | ★★☆ |
| 8 | [aemo-nemweb](aemo-nemweb.md) | AEMO NEMWeb | Australia (NEM) | 5 min | Public files | **16/18** | ★★☆ |
| 9 | [fingrid](fingrid.md) | Fingrid Open Data | Finland | 3 min | API key (free) | **15/18** | ★★☆ |
| 10 | [electricity-maps](electricity-maps.md) | Electricity Maps API | Global (~200 zones) | 5-15 min | Commercial | **15/18** | ★☆☆ |
| 11 | [watttime](watttime.md) | WattTime Marginal Emissions | Global (US focus) | 5 min | Free tier limited | **15/18** | ★☆☆ |
| 12 | [kepco-kpx](kepco-kpx.md) | KPX / KEPCO Open API | South Korea | 5 min | API key (free, Korean) | **15/18** | ★☆☆ |
| 13 | [ember-climate](ember-climate.md) | Ember Global Electricity Data | Global (200+ countries) | Monthly | CC BY 4.0 | **15/18** | ★☆☆ |
| 14 | [nyiso](nyiso.md) | NYISO MIS | New York State | 5 min | Public files | **15/18** | ★☆☆ |
| 15 | [pjm-data-miner](pjm-data-miner.md) | PJM Data Miner 2 | Eastern US (13 states) | Hourly | Free account | **14/18** | ★☆☆ |
| 16 | [caiso-oasis](caiso-oasis.md) | CAISO OASIS | California | 5 min | Public | **14/18** | ★☆☆ |
| 17 | [ieso-ontario](ieso-ontario.md) | IESO Data Directory | Ontario, Canada | 5 min | Public files | **14/18** | ★☆☆ |
| 18 | [eirgrid-smartgrid](eirgrid-smartgrid.md) | EirGrid Smart Grid Dashboard | Ireland (all-island) | 15 min | No auth (flaky) | **14/18** | ★☆☆ |
| 19 | [smard-de](smard-de.md) | SMARD (Bundesnetzagentur) | Germany (TSO zones) | 15 min | No auth | **14/18** | ★☆☆ |
| 20 | [aeso-alberta](aeso-alberta.md) | AESO | Alberta, Canada | 1 min | API key (free) | **14/18** | ★☆☆ |
| 21 | [gridstatus-io](gridstatus-io.md) | GridStatus.io | US (all ISOs) | 5 min | Commercial | **14/18** | ★☆☆ |
| 22 | [ercot](ercot.md) | ERCOT MIS | Texas | 5-15 min | Public (403 issues) | **14/18** | ★☆☆ |
| 23 | [nord-pool](nord-pool.md) | Nord Pool | Nordic/Baltic/EU | Daily auction | API deprecated (410) | **13/18** | ☆☆☆ |
| 24 | [xm-colombia](xm-colombia.md) | XM Colombia | Colombia | Hourly | POST API (public) | **13/18** | ☆☆☆ |
| 25 | [transpower-nz](transpower-nz.md) | Transpower NZ | New Zealand | 5 min | Dashboard only | **13/18** | ☆☆☆ |
| 26 | [occto-japan](occto-japan.md) | OCCTO / JEPX | Japan | Hourly | CSV downloads | **13/18** | ☆☆☆ |
| 27 | [ree-esios](ree-esios.md) | REE e·sios | Spain | 10 min | API issues | **12/18** | ☆☆☆ |
| 28 | [eskom-loadshedding](eskom-loadshedding.md) | Eskom Load Shedding | South Africa | Real-time | No auth | **12/18** | ☆☆☆ |
| 29 | [epex-spot](epex-spot.md) | EPEX SPOT | Central Western Europe | Real-time | Commercial only | **12/18** | ☆☆☆ |
| 30 | [cenace-mexico](cenace-mexico.md) | CENACE | Mexico | Hourly | Portal only | **12/18** | ☆☆☆ |
| 31 | [epias-exist-turkey](epias-exist-turkey.md) | EPIAS/EXIST | Turkey | 15 min | Blocked/unclear | **11/18** | ☆☆☆ |
| 32 | [nldc-india](nldc-india.md) | Grid-India / NLDC | India | 5-15 min | Geo-restricted? | **11/18** | ☆☆☆ |
| 33 | [bc-hydro-hq](bc-hydro-hq.md) | BC Hydro / Hydro-Québec | BC + Quebec, Canada | 5-15 min | Dashboard only | **11/18** | ☆☆☆ |
| 34 | [coes-peru](coes-peru.md) | COES SINAC | Peru | Hourly | Portal only | **11/18** | ☆☆☆ |

## Tier 1 — Implement First

These sources have clean JSON APIs, no or minimal auth, excellent freshness, and broad coverage:

### EIA Grid Monitor (eia-grid-monitor.md) — **18/18**
The single most valuable source for US electricity data. One REST API covers all ~70 US balancing authorities with hourly demand, generation by fuel type, and interchange. Free API key, clean JSON, well-documented. This alone supersedes the need for individual CAISO/ERCOT/PJM/NYISO/MISO/SPP/ISO-NE integrations for most use cases.

### Elexon BMRS (elexon-bmrs.md) — **18/18**
The UK's electricity market data platform. No auth required, clean JSON/XML/CSV, OpenAPI 3.0 spec. Half-hourly generation by fuel type, balancing mechanism data, system prices. Verified working with live data.

### Energy-Charts API (energy-charts-info.md) — **18/18** ★ NEW
The European equivalent of EIA Grid Monitor — and then some. Fraunhofer ISE's API covers **40+ European countries** with generation by fuel type, spot prices (40+ bidding zones), cross-border flows, renewable share forecasts, and a grid carbon signal. No auth. Clean JSON. OpenAPI 3.1 spec. CC BY 4.0. Verified working for DE, AT, CH, NL, PL, IT, HU, CZ, NO, SE, ES, GR, DK, and more. This single API effectively supersedes the need for individual TSO integrations for TenneT, 50Hertz, Amprion, TransnetBW, APG, PSE, ČEPS, MAVIR, ADMIE, Swissgrid, and most other European operators.

### Carbon Intensity UK (carbon-intensity-uk.md) — **17/18**
Beautifully designed, zero-auth REST API for GB carbon intensity with regional breakdown across 17 DNO areas. Pairs perfectly with Elexon BMRS.

### Energi Data Service (energidataservice-dk.md) — **17/18**
Denmark's minute-by-minute power system data. No auth, clean JSON, with real-time CO2, wind, solar, exchange flows, and Nordic spot prices. Verified working endpoint.

## Tier 2 — Strong Candidates

### RTE éCO2mix (rte-eco2mix.md) — **16/18**
France's 15-minute generation mix with exceptional sub-fuel detail (3 types of hydro, 3 types of gas, on/offshore wind). Opendatasoft API. Quota limit of 50k calls/month.

### ONS Brazil (ons-brazil.md) — **16/18** ★ NEW
Brazil's national grid operator provides real-time (~1 min) generation by fuel type across four subsystems, with international interchange and inter-regional flow data. No auth, clean JSON. Verified working with live data showing 43+ GW of generation including 21 GW hydro, 10 GW wind, and 12 GW solar. Uniquely valuable for Southern Hemisphere and developing-world coverage.

### AEMO NEMWeb (aemo-nemweb.md) — **16/18**
Australia's 5-minute dispatch data. File-based (CSV in ZIP) rather than JSON API, but uniquely valuable for Southern Hemisphere coverage and very high renewable penetration data.

### Fingrid (fingrid.md) — **15/18**
Finland's TSO with 3-minute real-time data including grid frequency. Free API key required. Good Nordic coverage complement to Energi Data Service.

## Tier 3 — Specialized / Regional

### WattTime (watttime.md) — **15/18** ★ NEW
Marginal emissions data (MOER) — the CO2 impact of the next MWh consumed. Free tier limited to signal index (0-100); full data requires paid subscription. Powers Google Cloud and Microsoft carbon-aware computing. Unique value: marginal vs. average emissions.

### KEPCO/KPX (kepco-kpx.md) — **15/18** ★ NEW
South Korea's power exchange provides 5-minute generation data and system marginal prices. Free API key via data.go.kr (Korean registration). World's 9th largest grid, ~30% nuclear.

### Ember Climate (ember-climate.md) — **15/18** ★ NEW
Global reference dataset covering 200+ countries with monthly generation, annual capacity, and emissions data. CC BY 4.0. Not real-time — value is in cross-country comparable analysis and historical context. The definitive source for global energy transition tracking.

### Electricity Maps (electricity-maps.md) — **15/18**
Global aggregator with ~200 zones. Commercial license for production use. Better to go to primary sources directly unless global coverage is specifically needed.

### EirGrid Smart Grid Dashboard (eirgrid-smartgrid.md) — **14/18** ★ NEW
Ireland's all-island grid with unique SNSP (System Non-Synchronous Penetration) metric. WCF service endpoint, no auth. Wind data verified working, but other endpoints returned 503. Ireland has world-leading wind penetration.

### SMARD (smard-de.md) — **14/18** ★ NEW
Bundesnetzagentur's energy market data portal for Germany. Authoritative source with German TSO zone breakdown (50Hertz, Amprion, TenneT, TransnetBW). File-based access pattern. For most uses, energy-charts.info is friendlier.

### AESO Alberta (aeso-alberta.md) — **14/18** ★ NEW
Alberta's unique 1-minute-settlement energy-only market. Free API key. Critical for Canadian coverage alongside IESO Ontario.

### GridStatus.io (gridstatus-io.md) — **14/18** ★ NEW
Commercial US grid data aggregator normalizing all ISO feeds. Also has an open-source Python library (`gridstatus` on PyPI) for direct ISO scraping. Value is in normalization and sub-hourly data.

### US ISOs: NYISO, PJM, CAISO, ERCOT — **14-15/18**
All provide granular zonal/nodal data, but EIA Grid Monitor covers their BA-level data in a single clean API. These are only needed for nodal pricing or market-specific data not in EIA.

### IESO Ontario (ieso-ontario.md) — **14/18**
Canadian coverage. XML-only file-based system. Useful for Canada-US grid interconnection context.

## Tier 4 — Lower Priority / Difficult Access

### Nord Pool (nord-pool.md) — **13/18** ★ NEW
Legacy public API confirmed decommissioned (HTTP 410 Gone). Prices now available via energy-charts.info and ENTSO-E. Commercial-only for direct access.

### XM Colombia (xm-colombia.md) — **13/18** ★ NEW
Colombian grid operator with POST-based Power BI API. Hydro-dominated (~70%) system vulnerable to El Niño. Interesting for Latin American coverage.

### Transpower NZ (transpower-nz.md) — **13/18** ★ NEW
New Zealand's ~80% renewable grid (hydro + geothermal). Dashboard data exists but no verified JSON API. EMI portal may provide better access.

### OCCTO/JEPX Japan (occto-japan.md) — **13/18** ★ NEW
Japan's unique 50/60 Hz split grid across 10 utility areas. Portal-based access with CSV downloads. JEPX provides market prices. World's 3rd largest economy.

### Eskom Load Shedding (eskom-loadshedding.md) — **12/18** ★ NEW
South Africa's rolling blackout status as a bare integer. Simple but culturally significant — millions check this daily. Pair with EskomSePush for better API.

### EPIAS/EXIST Turkey (epias-exist-turkey.md) — **11/18** ★ NEW
Turkish transparency platform. SPA frontend with WAF protection blocked API probing. Turkey bridges Europe and Asia with growing renewables.

### Grid-India / NLDC (nldc-india.md) — **11/18** ★ NEW
India's national grid operator. Endpoints unreachable (possibly geo-restricted). World's 3rd largest grid undergoing massive solar expansion.

### REE e·sios (ree-esios.md) — **12/18**
Spanish grid data. API was returning errors during testing — Spain is now covered by energy-charts.info.

### Additional documented candidates with limited API access:

- [CENACE Mexico](cenace-mexico.md) ★ NEW — **12/18** — Portal-only access, ASP.NET WebForms
- [EPEX SPOT](epex-spot.md) ★ NEW — **12/18** — Commercial only; prices available via ENTSO-E
- [BC Hydro / Hydro-Québec](bc-hydro-hq.md) ★ NEW — **11/18** — Dashboard only, no API
- [COES Peru](coes-peru.md) ★ NEW — **11/18** — Portal-based, small market

## Not Individually Documented (Covered by Other Sources)

| Source | Why Not Separate | Covered By |
|--------|------------------|------------|
| MISO | EIA covers MISO hourly data | eia-grid-monitor |
| SPP | EIA covers SPP hourly data | eia-grid-monitor |
| ISO-NE | EIA covers ISNE hourly data | eia-grid-monitor |
| Statnett (Norway) | Generation mix available via energy-charts.info (country=no) | energy-charts-info, entsoe |
| Svenska Kraftnät (Sweden) | Generation mix available via energy-charts.info (country=se) | energy-charts-info, entsoe |
| TenneT (DE/NL) | German zones in SMARD; NL via energy-charts.info (country=nl) | energy-charts-info, smard-de |
| 50Hertz / Amprion / TransnetBW | German TSO zones available via SMARD and energy-charts.info | energy-charts-info, smard-de |
| APG (Austria) | Austrian data via energy-charts.info (country=at) | energy-charts-info |
| PSE (Poland) | Polish data via energy-charts.info (country=pl) | energy-charts-info |
| ČEPS (Czech Republic) | Czech data via energy-charts.info (country=cz) | energy-charts-info |
| MAVIR (Hungary) | Hungarian data via energy-charts.info (country=hu) | energy-charts-info |
| Terna (Italy) | Italian data via energy-charts.info (country=it) | energy-charts-info |
| ADMIE (Greece) | Greek data via energy-charts.info (country=gr) | energy-charts-info |
| Swissgrid (Switzerland) | Swiss data via energy-charts.info (country=ch) | energy-charts-info |
| National Grid ESO (UK) | carbon-intensity-uk + elexon-bmrs cover GB; also energy-charts.info (country=uk) | carbon-intensity-uk, elexon-bmrs |
| Open Power System Data | Historical bulk downloads, not real-time | N/A (reference data) |
| IRENA | Annual capacity statistics, not real-time; covered by Ember for analysis | ember-climate |
| CO2signal | Powered by Electricity Maps; use primary sources instead | electricity-maps |
| ENTSO-E SFTP | Bulk historical data; REST API already implemented | entsoe |

## Geographic Coverage Map

```
Americas:     EIA (US-wide), IESO (Ontario), AESO (Alberta), BC Hydro, Hydro-Québec,
              NYISO/PJM/CAISO/ERCOT (US nodal), GridStatus.io (US aggregator),
              ONS (Brazil), XM (Colombia), CENACE (Mexico), COES (Peru)
Europe:       ENTSO-E (pan-EU), Energy-Charts (40+ countries!),
              Elexon+Carbon Intensity (GB), Energinet (DK), RTE (FR),
              Fingrid (FI), EirGrid (IE), SMARD (DE zones), REE (ES),
              Nord Pool/EPEX (prices), EPIAS (Turkey)
Asia-Pacific: AEMO (Australia), OCCTO/JEPX (Japan), KPX (South Korea),
              Grid-India/NLDC (India), Transpower (New Zealand)
Africa:       Eskom (South Africa)
Global:       Electricity Maps (aggregator), WattTime (emissions),
              Ember (reference data)
```

## Recommended Implementation Order

1. **eia-grid-monitor** — Unlocks all US balancing authorities in one integration
2. **energy-charts-info** — Unlocks 40+ European countries in one integration ★ NEW
3. **elexon-bmrs** — UK market data, no auth, instant access
4. **carbon-intensity-uk** — UK carbon intensity, pairs with Elexon
5. **energidataservice-dk** — Danish/Nordic real-time grid, no auth
6. **ons-brazil** — Brazil's real-time grid, no auth, clean JSON ★ NEW
7. **rte-eco2mix** — French generation mix (detail beyond energy-charts)
8. **aemo-nemweb** — Australian NEM (different format, broader coverage)
9. **fingrid** — Finnish TSO data
10. **watttime** — Marginal emissions for carbon-aware applications ★ NEW
11. **ember-climate** — Global reference dataset for context ★ NEW
12. Remaining candidates as needed for specific regional coverage
