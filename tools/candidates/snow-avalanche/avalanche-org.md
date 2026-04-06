# Avalanche.org (US National Avalanche Center)
**Country/Region**: United States
**Publisher**: US Forest Service National Avalanche Center (NAC)
**API Endpoint**: `https://api.avalanche.org/v2/public/products`
**Documentation**: https://avalanche.org/avalanche-encyclopedia/ (limited API docs)
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Daily (during winter season, per avalanche center)
**License**: US Government public domain

## What It Provides
Avalanche.org aggregates avalanche forecasts from ~22 US avalanche centers into a single platform:
- Avalanche danger ratings (1-5 North American scale) by zone
- Avalanche problem descriptions
- Forecast discussions and travel advice
- Avalanche observations and reports
- Weather data relevant to avalanche conditions
- Educational content

## API Details
- **Products endpoint**: `GET /v2/public/products?type=forecast&center_id={centerId}`
- **Center IDs**: `CAIC` (Colorado), `NWAC` (Northwest), `SAC` (Sierra), `BTAC` (Bridger-Teton), etc.
- **Product types**: `forecast`, `warning`, `watch`, `special`
- **Forecast zones**: Each center has multiple forecast zones
- **Observation reports**: `GET /v2/public/observations`

Note: API returned PHP memory exhaustion errors at probe time, suggesting the v2 API may be under maintenance or experiencing issues. The API structure is documented and has been used by third-party apps.

## Freshness Assessment
Moderate. Forecasts are published daily during winter season by each participating avalanche center. Not all centers publish on the same schedule. The API aggregates across centers but may have reliability issues.

## Entity Model
- **Product** (id, type, center_id, published_time, expires_time)
- **Forecast** (danger ratings by zone, elevation band, and day)
- **AvalancheProblem** (type, likelihood, size, aspect, elevation)
- **Center** (center_id, name, state, url, forecast zones)
- **Observation** (observer, date, location, avalanche details)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily, seasonal |
| Openness | 2 | No auth, but API stability unclear |
| Stability | 1 | PHP errors at probe time, API seems fragile |
| Structure | 2 | JSON, but inconsistent across centers |
| Identifiers | 2 | Center IDs stable, zone IDs vary |
| Additive Value | 3 | US-wide avalanche forecast aggregation |
| **Total** | **12/18** | |

## Notes
- The v2 API appears to have reliability issues (memory exhaustion errors observed)
- Individual avalanche center websites may be more reliable than the aggregator API
- Could pair with SNOTEL data for combined snow/avalanche picture
- Worth monitoring for API stability before committing to an integration
- Some centers also publish via RSS/XML feeds
