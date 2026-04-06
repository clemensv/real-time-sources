# SAIS (Scottish Avalanche Information Service)
**Country/Region**: Scotland (Scottish Highlands)
**Publisher**: Sportscotland / SAIS
**API Endpoint**: `https://api.sais.gov.uk/` (infrastructure detected, not yet live)
**Documentation**: https://www.sais.gov.uk/
**Protocol**: REST (planned, not yet deployed)
**Auth**: Unknown
**Data Format**: Unknown (JSON expected)
**Update Frequency**: Daily during winter season (December–April)
**License**: UK Government open data (expected)

## What It Provides
SAIS provides avalanche and mountain hazard forecasts for six Scottish Highland regions:
- **Lochaber** (Ben Nevis, Aonach Mor, Grey Corries, Mamores)
- **Glen Coe** (Bidean nam Bian, Aonach Eagach, Buachaille Etive Mòr)
- **Creag Meagaidh**
- **Northern Cairngorms**
- **Southern Cairngorms**
- **Torridon**

Each forecast includes:
- Avalanche hazard rating (1-5 European scale)
- Avalanche problem descriptions
- Snowpack commentary
- Weather and wind conditions
- Mountain conditions summary

## API Details
- **Website**: `https://www.sais.gov.uk/` — HTML forecasts (200 OK)
- **API domain**: `https://api.sais.gov.uk/` — returns 200 OK with placeholder content `"# This is needed"`
- **Data domain**: `https://data.sais.gov.uk/` — returns 200 OK with placeholder content `"# This is needed"`
- **Individual forecasts**: `https://www.sais.gov.uk/{region-name}` (HTML)
- **Assessment**: API and data infrastructure has been provisioned but not yet populated

## Probe Results
```
https://www.sais.gov.uk/: HTTP 200 OK (HTML, forecasts visible)
https://api.sais.gov.uk/: HTTP 200 OK (Content: "# This is needed" — placeholder)
https://data.sais.gov.uk/: HTTP 200 OK (Content: "# This is needed" — placeholder)
Assessment: API infrastructure prepared, implementation pending
```

## Freshness Assessment
Unknown for API. Web forecasts are published daily during the winter season (typically December through April). SAIS has operated since 1988, providing consistent seasonal coverage.

## Entity Model (Expected)
- **Region** (name, ID, geographic bounds)
- **Forecast** (date, hazard level, valid period)
- **Avalanche Problem** (type, aspect, elevation)
- **Snowpack** (description, stability assessment)
- **Weather** (wind, temperature, precipitation, visibility)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily during season (web); API not yet live |
| Openness | 2 | API infrastructure exists, placeholder content |
| Stability | 2 | Government service since 1988, API uncertain timing |
| Structure | 1 | HTML only currently; API/data domains ready but empty |
| Identifiers | 2 | Region names as slugs |
| Additive Value | 3 | Only source for Scottish avalanche conditions |
| **Total** | **12/18** | |

## Notes
- The existence of api.sais.gov.uk and data.sais.gov.uk with placeholder content strongly suggests an API is planned
- Monitor these domains for deployment — could become a clean REST API
- Scotland's maritime snow climate produces different avalanche conditions than continental Alps
- SAIS is the only avalanche warning service for the British Isles
- Current web scraping would be the interim integration path
- Six well-defined forecast regions make for a manageable data scope
