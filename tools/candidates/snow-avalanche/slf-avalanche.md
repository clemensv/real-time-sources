# SLF Swiss Avalanche Bulletins
**Country/Region**: Switzerland
**Publisher**: WSL Institute for Snow and Avalanche Research SLF
**API Endpoint**: `https://whiterisk.ch/` (data API) / `https://www.slf.ch/en/avalanche-bulletin-and-snow-situation.html`
**Documentation**: https://www.slf.ch/en/avalanche-bulletin-and-snow-situation.html
**Protocol**: REST / CAAML (XML)
**Auth**: None (public bulletin) / WhiteRisk app
**Data Format**: XML (CAAML), JSON (WhiteRisk), HTML
**Update Frequency**: Twice daily (5 PM and 8 AM during winter season)
**License**: Open for non-commercial use

## What It Provides
The SLF provides the official Swiss avalanche bulletin covering:
- Avalanche danger levels (1-5 scale) by region
- Detailed danger description by elevation and aspect
- Avalanche problem types (wind slab, persistent weak layer, wet snow, etc.)
- Snow and weather conditions
- Trend forecasts
- Critical new snow and wind loading assessments

The WhiteRisk platform (web + mobile app) provides interactive maps and additional snow data.

## API Details
- **CAAML XML Bulletin**: `https://www.slf.ch/avalanche/mobile/bulletin_en.xml` (structured avalanche bulletin in CAAML format)
- **WhiteRisk Web**: `https://whiterisk.ch/en/conditions` — interactive danger map
- **CAAMLv6 standard**: International standard for avalanche bulletins (Canadian Avalanche Association Markup Language)
- **Bulletin regions**: Switzerland is divided into ~120 warning regions
- **Additional products**: Snow maps, snow profiles, station data
- **Season**: Regular bulletins from November/December through April/May; summer bulletins only after heavy snowfall

## Freshness Assessment
Good. Bulletins are published twice daily during winter season (5 PM for next day, updated 8 AM). Outside winter, bulletins are only published after significant snowfall events. Push notifications available via WhiteRisk app.

## Entity Model
- **Bulletin** (bulletin ID, publication time, valid time range)
- **DangerRating** (region, elevation, aspect, danger level 1-5)
- **AvalancheProblem** (type, elevation range, aspect, likelihood)
- **WarningRegion** (region ID, name, geometry)
- **SnowProfile** (station, elevation, layer data)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Twice daily, seasonal operation |
| Openness | 2 | Public bulletin, but API not formally documented |
| Stability | 3 | SLF has operated since 1936, gold standard |
| Structure | 3 | CAAML v6 XML standard, well-structured |
| Identifiers | 2 | Region IDs, but no formal API versioning |
| Additive Value | 3 | World-leading avalanche science institution |
| **Total** | **15/18** | |

## Notes
- CAAML (Canadian Avalanche Association Markup Language) is the international XML standard for avalanche data
- SLF is considered the global gold standard for avalanche forecasting
- The WhiteRisk platform may have undocumented JSON APIs worth exploring
- Community observations can be submitted and are used in assessments
- Seasonal operation limits year-round utility
