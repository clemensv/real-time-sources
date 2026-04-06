# Hungary OVF Water Level Data (vizugy.hu)

**Country/Region**: Hungary
**Publisher**: Országos Vízügyi Főigazgatóság (OVF) — General Directorate of Water Management
**API Endpoint**: `https://www.vizugy.hu/` (web portal) / `https://data.vizugy.hu/` (newer data platform, auth-gated)
**Documentation**: https://www.vizugy.hu/
**Protocol**: HTML / REST (behind auth)
**Auth**: Bearer token required for data.vizugy.hu API
**Data Format**: HTML (public), JSON (behind auth)
**Update Frequency**: 15 minutes to hourly
**Station Count**: 500+ water gauge stations (vízmérce)
**License**: Hungarian government data

## What It Provides

Comprehensive real-time water level data for all Hungarian rivers, lakes, and canals:
- Water levels (cm) at 500+ gauge stations
- Coverage of the Danube, Tisza, Balaton, and all Hungarian tributaries
- River kilometer (fkm) positions for each station
- 15-minute to hourly update frequency
- Historical time series and hourly graphs

## API Details

### Public web access
The main portal at `vizugy.hu` provides water level data as server-rendered HTML tables. The URL pattern:
```
https://www.vizugy.hu/?mapModule=OpVizallas&SzervezetKod=0&mapData=VizmerceLista
```
Returns an HTML table with columns:
- Vízmérce (gauge name) — links to individual station graphs
- Vízfolyás (water body name)
- Szelvény (river km)
- Időpont (timestamp)
- Vízállás (water level in cm)

Each station has a UUID identifier (e.g., `16496185-97AB-11D4-BB62-00508BA24287`) used in URLs:
```
?mapModule=OpGrafikon&AllomasVOA={UUID}&mapData=OrasIdosor
```

### Newer API platform (auth-gated)
A newer platform at `data.vizugy.hu` was discovered with:
- `https://data.vizugy.hu/AuthApi/auth/token` — token endpoint (origin-restricted)
- `https://vmservice.vizugy.hu/vraquery/Vra/InternetVmo/{id}/false` — station data (bearer token required)
- `https://vmservice.vizugy.hu/vraquery/TS/TsShortList` — time series (POST, bearer token required)

These endpoints return JSON but require authentication that is tied to the web portal session.

### Example data (extracted from HTML)
```
Station: Baja, River: Duna (Danube), km: 1478.700, Time: 2026.04.06 12:00, Level: 132 cm
Station: Algyő, River: Tisza, km: 192.660, Time: 2026.04.06 12:15, Level: 115 cm
Station: Balaton átlag, River: Balaton, km: 0.000, Time: 2026.04.06 07:00, Level: 90 cm
```

## Freshness Assessment

- Data confirmed fresh with 2026-04-06 timestamps
- Updates range from 15-minute intervals (major stations) to hourly
- Live data visible on public web portal
- Underlying API infrastructure is modern (Vue.js frontend, REST API backend)

## Entity Model

- **Station (Vízmérce)**: UUID, name, water body (Vízfolyás), river kilometer (Szelvény)
- **Organization (Területi igazgatóság)**: regional water management directorates
- **Observation**: timestamp (Időpont), water level in cm (Vízállás)
- **Water body**: Duna (Danube), Tisza, Balaton, Rába, Dráva, canals, etc.

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 1 | No public REST API; data only via HTML scraping or auth-gated endpoints |
| Data Richness | 2 | Water levels at 500+ stations; no discharge data in public view |
| Freshness | 3 | 15-minute updates confirmed |
| Station Coverage | 3 | 500+ stations covering entire Hungarian hydrological network |
| Documentation | 0 | No API documentation; endpoint structure discovered via probing |
| License/Access | 1 | Public web data but no open API; auth required for structured access |
| **Total** | **10/18** | |

## Notes

- Hungary is a key Danube basin country — the Danube, Tisza, and Balaton are all covered
- The HTML rendering is consistent enough for reliable scraping but this is fragile
- Station UUIDs are stable identifiers — good for tracking
- Regional directorates (12 territorial organizations) manage different parts of the network
- The newer data.vizugy.hu platform suggests an API is being developed but not yet public
- Alternative: ICPDR (International Commission for the Protection of the Danube River) may aggregate Hungarian data, but no public API was found there either
- Hungarian language throughout — station names, water body names, UI text
