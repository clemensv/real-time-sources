# Mekong River Commission — Hydrological Monitoring (Update)

**Country/Region**: Mekong Basin (Cambodia, Laos, Thailand, Vietnam; China, Myanmar as dialogue partners)
**Publisher**: Mekong River Commission (MRC)
**API Endpoint**: `https://portal.mrcmekong.org/` (Angular SPA), `https://monitoring.mrcmekong.org/`
**Documentation**: https://portal.mrcmekong.org/
**Protocol**: Angular SPA with backend API
**Auth**: Unknown (SPA-gated)
**Data Format**: SPA renders charts/maps; backend JSON
**Update Frequency**: Daily water level observations; hourly during floods
**License**: MRC data sharing agreement

## Update: April 2026 Re-Probe

Building on the existing `mekong-river-commission.md` candidate, this document records findings from the April 2026 re-probe.

### Portal Structure

The MRC Data Portal at `portal.mrcmekong.org` is an Angular SPA (confirmed by page source — Angular application shell with Leaflet maps). The SPA loads from `/` and handles all routing client-side. Direct API calls to paths like `/api/hydrology/stations` return the SPA shell (HTML), not data.

### Backend API Discovery

The Angular application likely calls backend APIs at a different base URL or with specific headers/tokens. Without browser-level inspection, the exact API endpoints remain undiscovered.

### Alternative: Open Development Mekong

The CKAN-based portal at `data.opendevelopmentmekong.net` has a working API:
```
GET https://data.opendevelopmentmekong.net/api/3/action/package_list
```
Returns a massive list of dataset identifiers. However, this is primarily policy/governance data rather than real-time hydrology.

### Mekong River's Significance

The Mekong is the world's most productive inland fishery (4.4M tonnes/year) and the 12th longest river. It's under extreme pressure from:
- 11+ mainstream dams (mostly in Laos and China)
- Chinese Lancang cascade (8 dams on upper Mekong)
- Climate change altering monsoon patterns
- Saltwater intrusion in Vietnam's delta

Real-time water level data is critical for:
- Flood early warning in Cambodia and Vietnam
- Fish migration monitoring
- Irrigation management for 60M+ basin residents
- Dam release coordination

## Updated Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily water levels; hourly during floods; but API hidden behind SPA |
| Openness | 1 | SPA blocks direct API access; no documentation |
| Stability | 2 | Intergovernmental institution (since 1995); well-funded |
| Structure | 1 | Angular SPA suggests JSON backend; but inaccessible |
| Identifiers | 2 | Station codes; MRC station numbering system |
| Additive Value | 3 | Transboundary river; 60M+ basin population; fisheries; dam impacts |
| **Total** | **11/18** (unchanged) | |

## Integration Notes

- Browser-based network inspection would reveal the backend API URLs
- MRC may provide API access through institutional partnership
- Nepal's BIPAD portal provides an example of how similar data (river monitoring) can be exposed via clean REST API
- The Mekong data gap contrasts with Europe's well-documented river monitoring (EFAS, Pegelonline, etc.)

## Verdict

Still promising but still locked behind the SPA. The MRC data is critically important for transboundary water management in Southeast Asia. The Angular SPA architecture strongly implies a JSON backend API exists — it's just not documented for public consumption. Recommend pursuing through MRC institutional channels or browser-based API discovery.
