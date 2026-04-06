# Slovakia SHMÚ Hydrology

**Country/Region**: Slovakia
**Publisher**: Slovenský hydrometeorologický ústav (SHMÚ) — Slovak Hydrometeorological Institute
**API Endpoint**: `https://www.shmu.sk/en/?page=1&id=hydrology` (web portal)
**Documentation**: https://www.shmu.sk/
**Protocol**: Web portal (PHP/HTML)
**Auth**: N/A
**Data Format**: HTML
**Update Frequency**: Daily reports, real-time on web portal
**Station Count**: ~300 gauging stations
**License**: Slovak government data

## What It Provides

SHMÚ operates Slovakia's national hydrological monitoring network:
- **Daily hydrological reports** with water levels at key stations
- **Hydrological forecasts** for major rivers (Dunaj/Danube, Váh, Hron, etc.)
- **Flood activity degrees** (stupne povodňovej aktivity)
- **Water temperature** at selected stations
- **Snow condition** monitoring
- **Water gauge stations** real-time display

## API Details

### Web portal
The SHMÚ website provides hydrology data through PHP-rendered pages:
```
https://www.shmu.sk/en/?page=1&id=hydrology&lid=hydro_data
```

### Probed for API
- `https://www.shmu.sk/api/v1/hydrology/stations` — 404
- No structured REST API found
- Data rendered server-side in HTML tables

### Data products
- Daily hydrological report (text/tables)
- Hydrological forecasts for Morava river
- Water gauge station interactive map
- Precipitation totals
- Snow information

## Freshness Assessment

- Daily reports published on the website
- Real-time gauge readings visible on interactive map
- Flood warnings are actively maintained
- Data exists but locked in web portal

## Entity Model

- **Station**: name, river, location, parameters
- **Observation**: timestamp, water level, flow
- **Flood activity level**: 1-3 degree system
- **River**: Dunaj (Danube), Váh, Hron, Nitra, Morava, etc.

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | No public API found |
| Data Richness | 2 | Water levels, forecasts, flood degrees, snow, temperature |
| Freshness | 2 | Daily reports; real-time on web portal |
| Station Coverage | 2 | ~300 stations in a small country |
| Documentation | 1 | Website navigation in English available |
| License/Access | 1 | Public website; no structured data access |
| **Total** | **8/18** | |

## Notes

- Slovakia is a Danube basin country with Bratislava on the Danube
- SHMÚ also provides reporting to Hungary downstream
- No public API despite having a modern website
- The interactive map suggests JavaScript-driven data loading — devtools inspection might reveal hidden APIs
- Neighbouring Czech Republic (CHMI) has an implemented adapter — similar Danube basin monitoring
- Consider as future candidate if API access becomes available
