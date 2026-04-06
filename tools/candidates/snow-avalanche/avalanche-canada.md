# Avalanche Canada
**Country/Region**: Canada (British Columbia, Alberta, Yukon, national parks)
**Publisher**: Avalanche Canada (non-profit, funded by Parks Canada and provinces)
**API Endpoint**: None (web portal at `https://www.avalanche.ca/`)
**Documentation**: https://www.avalanche.ca/ (public forecasts)
**Protocol**: Web portal (CMS-based)
**Auth**: None for public forecasts
**Data Format**: HTML (no JSON API discovered)
**Update Frequency**: Daily during winter season
**License**: Public forecasts freely available

## What It Provides
Avalanche Canada is the national avalanche warning service for Canada, providing:
- **Avalanche forecasts** for ~15 forecast regions across western Canada
- **Danger ratings** (1-5 European/North American scale) by elevation band
- **Avalanche problems** (storm slab, wind slab, persistent slab, deep persistent, wet, cornices)
- **Travel advice** for backcountry users
- **Mountain Information Network (MIN)** — crowdsourced field observations
- **Incident reports** and accident investigation data
- **Training resources** and safety information

Coverage regions include: Sea-to-Sky, South Coast, South Columbia, North Columbia, Cariboos, Glacier National Park, Banff/Yoho/Kootenay, Jasper, Kananaskis, Waterton, Purcells, Lizard Range, Flathead, and more.

## API Details
- **Web portal**: `https://www.avalanche.ca/forecasts` — forecast region selection
- **Individual forecast**: `https://www.avalanche.ca/forecasts/{region-slug}` (HTML)
- **MIN submissions**: Crowdsourced observations (no public API found)
- **Probed endpoints** (all returned 404):
  - `/api/forecasts`
  - `/api/bulletin-archive/`
  - `/api/bulletin-archive/2026`
  - `/api/min/submissions`
- **CMS backend**: Uses Prismic CMS (detected from HTML source: `api/v2/documents/search?ref=...`)
- **No Swagger/OpenAPI documentation found**

## Probe Results
```
https://www.avalanche.ca/: HTTP 200 (HTML)
/api/forecasts: HTTP 404
/api/bulletin-archive/: HTTP 404
/api/bulletin-archive/2026: HTTP 404
CMS: Prismic (api/v2/documents)
Assessment: Web portal only, no public REST API
```

## Freshness Assessment
Good (seasonal). Forecasts are published daily during the winter season (typically November through April). Evening forecasts with morning updates for high-traffic periods. The Mountain Information Network provides near real-time crowdsourced observations.

## Entity Model
- **Forecast Region** (slug, name, province, elevation bands)
- **Danger Rating** (1-5 by alpine/treeline/below-treeline elevation bands)
- **Avalanche Problem** (type, likelihood, size, aspect, elevation)
- **MIN Observation** (location, date, observer, conditions, photos)
- **Advisory** (special advisories for unusual conditions)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily during season |
| Openness | 1 | No API — web portal only, CMS-backed |
| Stability | 3 | National institution, Parks Canada funding |
| Structure | 1 | HTML only, Prismic CMS backend |
| Identifiers | 2 | Region slugs in URLs |
| Additive Value | 3 | Only source for Canadian avalanche forecasts |
| **Total** | **12/18** | |

## Notes
- Different organization from avalanche.org (US) — this is the Canadian national service
- Prismic CMS backend means data is structured internally but not exposed via public API
- The Mountain Information Network (MIN) is a unique crowdsourced observation system
- Integration would require HTML scraping or reverse-engineering the Prismic API
- Consider contacting Avalanche Canada about data access for developers
- Pairs with EAWS/ALBINA (Europe) and avalanche.org (US) for cross-continent coverage
