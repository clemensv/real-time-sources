# Mekong River Commission (MRC) Data Portal

**Country/Region**: Mekong Basin (Cambodia, Laos, Thailand, Vietnam; China, Myanmar as dialogue partners)
**Publisher**: Mekong River Commission (MRC)
**API Endpoint**: `https://portal.mrcmekong.org/` (data portal SPA), `https://monitoring.mrcmekong.org/` (monitoring SPA)
**Documentation**: https://portal.mrcmekong.org/api-doc (SPA — not machine-readable)
**Protocol**: Web application (Angular SPA)
**Auth**: Unknown (SPA-gated)
**Data Format**: Web/visual only; underlying API format unknown
**Update Frequency**: Daily (hydrological monitoring data)
**Station Count**: ~50+ monitoring stations along the Mekong mainstream and tributaries
**License**: MRC data sharing agreement

## What It Provides

The MRC operates two web portals for Mekong basin hydrological data:

### Data Portal (portal.mrcmekong.org)
- Historical and current hydrological datasets
- Water quality monitoring
- Fisheries data
- Basin-wide datasets for download

### Monitoring Portal (monitoring.mrcmekong.org)
- Real-time and near-real-time water level monitoring
- Flood and drought situation monitoring
- Station-level hydrographs
- Alert status for key stations

## API Details

### Web portals (SPA)
Both portals are Angular single-page applications:
- `https://portal.mrcmekong.org/api-doc` — API documentation page (renders as SPA, not REST endpoint)
- `https://monitoring.mrcmekong.org/station` — station listing (SPA rendering)

### Backend API (not publicly accessible)
The SPAs presumably use REST/JSON APIs internally, but:
- Direct API endpoint probing returned SPA HTML for all URL patterns
- No public API documentation was found outside the SPA
- Standard patterns (`/api/stations`, `/api/data`) were not responsive

### Data download
Some historical data may be downloadable after registration on the data portal.

## Freshness Assessment

- Monitoring portal shows real-time water level data
- The MRC has operational monitoring infrastructure across 4 countries
- Data sharing depends on member country contributions
- Portal was responsive during testing

## Entity Model

- **Station**: name, location, country, river/tributary
- **Water level**: timestamp, level (m), discharge (m³/s)
- **Basin**: Mekong mainstream and tributaries
- **Country**: Cambodia, Laos, Thailand, Vietnam

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 1 | SPA portals only; no confirmed public REST API |
| Data Richness | 2 | Water levels, quality, fisheries; but access unverified |
| Freshness | 2 | Monitoring portal shows real-time data; API access unclear |
| Station Coverage | 2 | ~50 stations across 4 countries along world's 12th longest river |
| Documentation | 1 | API-doc page exists but is SPA-rendered |
| License/Access | 1 | Registration likely required; MRC data sharing agreement |
| **Total** | **9/18** | |

## Notes

- The Mekong is one of the world's most important transboundary rivers (65 million people in the basin)
- MRC is the primary intergovernmental body for Mekong water management
- Despite having modern web infrastructure, programmatic access appears limited
- Thailand's thaiwater.net API provides Thai portions of the Mekong basin independently
- Vietnam and Cambodia may have national hydrological services not yet discovered
- China's upstream Lancang River data is not shared through MRC
- The `api-doc` route suggests an API exists or is planned
- Worth re-investigating periodically as MRC continues to modernize its data infrastructure
