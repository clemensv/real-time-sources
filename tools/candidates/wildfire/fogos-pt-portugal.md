# Fogos.pt — Portugal Community Fire Tracker

**Country/Region**: Portugal
**Publisher**: Fogos.pt (community project, open source)
**API Endpoint**: `https://api.fogos.pt/v1/now`
**Documentation**: https://api.fogos.pt/ (inferred from endpoint patterns)
**Protocol**: REST
**Auth**: Currently none; transitioning to token-based authentication
**Data Format**: JSON
**Update Frequency**: Near real-time (sourced from ANEPC civil protection data)
**License**: Apache 2.0 (source code)

## What It Provides

Fogos.pt is a community-maintained real-time fire tracking system for Portugal. It wraps data from ANEPC (Autoridade Nacional de Emergência e Proteção Civil) — Portugal's civil protection authority — into a clean JSON REST API. Given that Portugal experiences severe wildfire seasons (the country was devastated by fires in 2017, 2023, and 2024), this is a high-value regional source.

The API provides:
- Active fire incidents across Portugal with coordinates, timestamps, and status
- Fire warnings and alerts
- Statistics on current fire activity

## API Details

### Endpoints

| Endpoint | Description | Status |
|---|---|---|
| `https://api.fogos.pt/v1/now` | Current active fires | ✅ 200 OK |
| `https://api.fogos.pt/v1/now/data` | Active fire data (alternative format) | ✅ 200 OK |
| `https://api.fogos.pt/v1/warnings` | Active fire warnings | ✅ 200 OK |
| `https://api.fogos.pt/v1/stats` | Fire statistics | ✅ 200 OK |

Rate limiting observed — aggressive polling triggers 429 responses.

### ICNF GIS — Historical Burned Areas

```
https://sigservices.icnf.pt/
```

- **Protocol**: ArcGIS FeatureServer
- **Content**: Burned areas 1975–2019, fire severity (Sentinel-2 derived)
- **Auth**: Public endpoints in DFCI folder
- **Coverage**: Continental Portugal

## Freshness Assessment

Near real-time. Fogos.pt pulls data from ANEPC and provides it through a clean JSON API. Data is confirmed live as of 2026-04-06. Rate limiting is in place (429 on aggressive polling), and the project is transitioning to token-based authentication.

## Entity Model

- **Fire Incident** — active fire with location (coordinates), timestamp, status, municipality
- **Warning** — fire-related warnings and alerts
- **Historical Burned Area** — polygon features from ICNF with date, extent, severity

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Near real-time, sourced from civil protection |
| Openness | 2 | Currently open, but transitioning to token auth |
| Stability | 2 | Community project — well-maintained but no SLA |
| Structure | 3 | Clean JSON REST API |
| Identifiers | 2 | Incident-level data with locations |
| Additive Value | 2 | Unique Portuguese incident-level data with civil protection context |
| **Total** | **14/18** | |

## Notes

- Fogos.pt is the best real-time source for Portuguese wildfire incidents — it's a community project that emerged from Portugal's severe fire seasons.
- The transition to token-based auth may limit future access — monitor for changes.
- ICNF provides excellent historical/archival GIS data via ArcGIS but is not a real-time feed.
- The official ANEPC portal is primarily an SPA without exposed machine-readable endpoints — Fogos.pt provides the data bridge.
- For satellite-based Portuguese fire detection, EFFIS/GWIS and NASA FIRMS are better options. Fogos.pt adds the on-the-ground civil protection perspective.
- Source code is Apache 2.0 licensed — the API itself may have different terms.
