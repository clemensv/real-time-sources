# Saudi National Center for Environmental Compliance (NCEC) - Air Quality Monitoring

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: `https://ncec.gov.sa/` (API paths guessed, WAF-protected)
- **Protocol**: REST (assumed)
- **Auth**: Unknown (WAF blocks programmatic access)
- **Format**: JSON (assumed)
- **Freshness**: Real-time (dashboard updates continuously)
- **Docs**: None public
- **Score**: 6/18

## Overview

The National Center for Environmental Compliance (المركز الوطني للامتثال البيئي, NCEC) is Saudi Arabia's environmental enforcement authority, responsible for monitoring air quality, industrial emissions, water quality, and compliance with environmental regulations. NCEC was established in 2019 when the former General Authority for Meteorology and Environmental Protection (GAMEP) was restructured into NCM (meteorology) and NCEC (environmental compliance).

NCEC operates an air quality monitoring network across Saudi Arabia's major urban and industrial areas. The public-facing dashboard displays:
- **7 air quality monitoring stations** (as of 2024)
- Real-time Air Quality Index (AQI) values
- Station locations and status
- Health categories (Healthy, Moderate, Unhealthy for Sensitive Groups, Unhealthy, Hazardous, Dangerous)

Saudi Arabia faces significant air quality challenges:
- **Dust and sandstorms** — natural PM10 sources from the Rub' al Khali (Empty Quarter) and Syrian Desert
- **Industrial emissions** — Jubail Industrial City, Yanbu, Ras Tanura oil refineries
- **Urban pollution** — vehicle emissions in Riyadh (pop. 7M+), Jeddah, Dammam
- **Desertification** — expanding desert encroachment increases airborne dust
- **Hajj/Umrah periods** — concentrated vehicle traffic in Makkah/Madinah

## Endpoint Analysis

**Dashboard**: `https://ncec.gov.sa/ar/mediacenter/aqmonitoring/pages/default.aspx`

**Attempted API probes**:
```
GET https://ncec.gov.sa/api/aqi
GET https://ncec.gov.sa/api/stations
```

**Response**: Both returned **Request Rejected** HTML with WAF (Web Application Firewall) support ID. The WAF is blocking programmatic access, indicating either:
1. The API paths are incorrect
2. API access requires pre-registration or IP whitelisting
3. No public API exists; the dashboard fetches data through internal services

**HEAD requests**:
```
HEAD https://ncec.gov.sa/api/aqi → 200 OK, text/html
HEAD https://ncec.gov.sa/api/stations → 200 OK, text/html
```

The 200 responses suggest these paths exist but return HTML (likely the WAF rejection page), not JSON.

**Dashboard inspection**: The public dashboard at `https://ncec.gov.sa/` shows a real-time map with station markers. The underlying data is likely loaded via AJAX or WebSocket, but the JavaScript is minified and the endpoints are not documented.

**Station count**: The dashboard header states **"عدد المحطات 7"** (Number of stations: 7). This is a very limited network for a country of 35 million people and 2.15 million km². For comparison:
- US EPA AirNow: ~2,000 stations
- European EEA: ~4,000 stations
- China MEE: ~1,500 cities with multiple stations each

The 7 stations likely cover:
- Riyadh (capital)
- Jeddah (commercial hub)
- Dammam/Khobar (Eastern Province oil region)
- Jubail (industrial city)
- Possibly Makkah, Madinah, or Yanbu

## Integration Notes

- **WAF barrier**: The primary obstacle is the Web Application Firewall blocking programmatic access. This is a common pattern for Saudi government websites that were not designed for API usage.
- **No public API documentation**: NCEC does not publish API docs, developer portals, or data download pages.
- **Dashboard scraping**: The dashboard is a SharePoint page with embedded JavaScript. Scraping is technically feasible but fragile and against most ToS.
- **Alternative: AQICN aggregation**: The global Air Quality Index aggregator (AQICN.org) sometimes integrates with national networks. NCEC data may be available through this channel.
- **Limited station count**: Even if API access is obtained, 7 stations provide only coarse coverage. The value is low compared to denser networks like OpenAQ, Sensor.Community, or PurpleAir.
- **Unique value**: Saudi-specific industrial monitoring (Jubail, Yanbu refineries) and dust storm tracking are not available elsewhere.

## Comparison with Alternatives

| Source | Coverage | Stations | Auth | Status |
|--------|----------|----------|------|--------|
| **NCEC** | Saudi Arabia | ~7 | WAF-blocked | Unknown API |
| OpenAQ | Global (includes KSA) | 15,000+ | None | Active |
| AQICN | Global | 30,000+ | None (web) / key (API) | Active |
| Sensor.Community | Crowdsourced | 15,000+ | None | Active |
| PurpleAir | Crowdsourced | 20,000+ | Free key | Active |

OpenAQ and AQICN likely already aggregate the handful of NCEC stations that report to international networks. Building a dedicated NCEC bridge adds minimal value unless it exposes industrial or dust-specific parameters not shared internationally.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Dashboard shows real-time updates |
| Openness | 0 | WAF blocks all programmatic access; no public API |
| Stability | 1 | Government agency, but no API commitment |
| Structure | 1 | Assumed JSON behind the dashboard |
| Identifiers | 1 | Station IDs likely exist but not exposed |
| Additive value | 0 | Minimal station count; likely already in OpenAQ |

**Total: 6/18**

**Verdict**: ❌ **Skip** — The WAF barrier and absence of public API documentation make this infeasible without official NCEC cooperation. The limited station count (7) and likely overlap with OpenAQ provide minimal additive value. If NCEC publishes API docs or grants programmatic access in the future, reassess. For Saudi Arabia air quality, **use OpenAQ** which already aggregates international-reporting Saudi stations.
