# India GRID-INDIA (POSOCO) — National Power Grid Real-Time Data

**Country/Region**: India
**Publisher**: Grid Controller of India (formerly POSOCO — Power System Operation Corporation)
**API Endpoint**: `https://www.grid-india.in/` (web portal — connection failed), `https://vidyutpravah.in/` (public dashboard — connection failed)
**Documentation**: https://www.grid-india.in/, https://vidyutpravah.in/
**Protocol**: Web portals (HTML/JavaScript SPAs)
**Auth**: N/A (no public API discovered)
**Data Format**: HTML, internal JSON via SPA
**Update Frequency**: 5-minute to 15-minute SCADA intervals for grid frequency; hourly for generation mix
**License**: Indian government / regulatory data

## What It Provides

Grid Controller of India (formerly POSOCO, renamed 2022) operates India's national electrical grid — the world's **3rd largest power system** by installed capacity (~430 GW). India's grid is a single synchronous system serving 1.4 billion people across 5 regional grids (Northern, Western, Southern, Eastern, North-Eastern).

### Data Published (via web portals)

- **Grid frequency**: Real-time all-India frequency (target: 50.00 Hz ± 0.05)
- **Total generation**: MW output by region and fuel type (thermal, hydro, nuclear, wind, solar, biomass)
- **Demand-supply position**: Region-wise demand, met demand, surplus/deficit
- **Interstate energy exchange**: Power flows between regions and states
- **Renewable integration**: Solar and wind generation tracking
- **MERIT Order Dispatch**: `meritindia.in` — tracks generation dispatch order

### Vidyut Pravah

The `vidyutpravah.in` dashboard (literally "electricity flow") is the public-facing portal showing:
- All-India demand (MW)
- Current generation by fuel type
- Grid frequency
- Region-wise position
- Solar generation curve

### Probe Results

Both `grid-india.in` and `vidyutpravah.in` returned **connection failures** (fetch failed). The `meritindia.in` dashboard also failed. These sites may have:
1. Geographic restrictions
2. WAF/Cloudflare protection
3. Intermittent availability
4. Heavy JavaScript SPAs that don't respond to simple HTTP fetches

## Entity Model

- **Region**: Northern (NR), Western (WR), Southern (SR), Eastern (ER), North-Eastern (NER)
- **State**: 28 states and 8 UTs with individual generation and demand data
- **Fuel Type**: Coal, gas, diesel, nuclear, hydro, wind, solar, biomass, small hydro
- **Grid Frequency**: System-wide metric in Hz (sampled every few seconds)
- **Inter-Regional Tie Line**: Power flows between regions in MW

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 5-minute SCADA data exists; web dashboards show real-time data |
| Openness | 0 | No public API; connection failures on web portals |
| Stability | 2 | National grid operator; data infrastructure exists but not exposed |
| Structure | 1 | SPAs with internal APIs; no documented public endpoint |
| Identifiers | 2 | Region codes; state codes; fuel type categories standardized |
| Additive Value | 3 | World's 3rd largest grid; 430 GW; massive renewable growth; no current coverage |
| **Total** | **10/18** | |

## Integration Notes

- **Not currently API-viable** — but this is one of the most important energy data gaps
- The existing `nldc-india.md` candidate covers similar data (NLDC is part of Grid-India)
- India's solar generation curve (daily peak ~70 GW) is globally significant for understanding renewable integration
- Alternative: Electricity Maps (electricity-maps.md) aggregates some India grid data
- MERIT India data (meritindia.in) would be extremely valuable for dispatch optimization research
- India's grid frequency is publicly displayed at some substations — scraping possible but not recommended
- India is adding renewable capacity faster than almost any country — tracking this is valuable

## Verdict

Globally important but API-inaccessible. India's power grid is a fascinating real-time data source — 430 GW serving 1.4 billion people with rapidly growing solar/wind integration. The data exists and is shown on web dashboards but isn't exposed through public APIs. This is a gap worth pursuing through official channels, particularly given India's position as the world's fastest-growing major power market.
