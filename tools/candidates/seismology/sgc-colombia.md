# SGC Colombia — Servicio Geológico Colombiano

**Country/Region**: Colombia (national)
**Publisher**: Servicio Geológico Colombiano (SGC)
**API Endpoint**: `https://www.sgc.gov.co/sismos/ultimos-sismos` (SPA), `https://api.sgc.gov.co/fdsnws/event/1/` (403)
**Documentation**: https://www.sgc.gov.co/sismos
**Protocol**: REST / FDSN (blocked)
**Auth**: N/A (endpoints blocked)
**Data Format**: HTML (SPA/React)
**Update Frequency**: Near-real-time (website updates)
**License**: Colombian government entity

## What It Provides

SGC operates Colombia's national seismological network. Colombia sits at the junction of the Nazca, Caribbean, and South American plates — a tectonically complex region with both subduction (Pacific coast) and continental collision (Andes). The country also has active volcanoes monitored by SGC (Nevado del Ruiz, Galeras, etc.).

The SGC website displays:
- Recent earthquakes with magnitude, depth, location
- Felt report information
- Volcanic monitoring alerts

## API Details

### FDSN Endpoint
```
GET https://api.sgc.gov.co/fdsnws/event/1/query?format=text&limit=5
→ 403 Forbidden
```

The FDSN endpoint exists but returns 403. This may indicate IP-based access control, authentication requirements, or temporary restriction.

### Website (SPA)
```
https://www.sgc.gov.co/sismos/ultimos-sismos
```

The earthquake page is a React SPA (`main.e1d8797f.js`) that renders client-side. The HTML response is an empty `<div id="root">` shell. The actual API calls are embedded in the JavaScript bundle and likely hit internal endpoints. Reverse engineering the SPA's API calls would be needed to extract data programmatically.

### Alternative: datos.gov.co

Colombia's open data portal (datos.gov.co) hosts IDEAM hydrometeorological data via Socrata. SGC seismic data may also appear there — worth checking periodically.

## Freshness Assessment

The website appears to update in near-real-time. However, no programmatic access was confirmed during testing. The FDSN endpoint being 403 is the key blocker.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Website updates near-real-time, but no API access |
| Openness | 0 | FDSN returns 403; SPA requires reverse engineering |
| Stability | 1 | Government entity, but API access is blocked |
| Structure | 1 | Would be FDSN standard if accessible |
| Identifiers | 1 | Unknown without API access |
| Additive Value | 2 | Important tectonic region; Pacific subduction + Andes |
| **Total** | **7/18** | |

## Verdict

⏭️ **Skip for now** — The FDSN endpoint exists but is blocked (403). The website is a React SPA requiring JavaScript execution to extract data. Colombia's seismicity is covered by USGS and EMSC for larger events. Revisit periodically — the FDSN endpoint may become publicly accessible. SGC is a well-funded government agency; open data policies in Colombia are improving.
