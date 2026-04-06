# INPE Programa Queimadas (Brazil Fire Monitoring Program)

**Country/Region**: Brazil / South America
**Publisher**: INPE — Instituto Nacional de Pesquisas Espaciais (National Institute for Space Research)
**API Endpoint**: `https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/`
**Documentation**: https://terrabrasilis.dpi.inpe.br/queimadas/portal/
**Protocol**: Web application with file downloads / WMS
**Auth**: None (public access)
**Data Format**: CSV, Shapefile, KML
**Update Frequency**: Daily (reference satellite: AQUA afternoon pass)
**License**: Open government data (Brazil)

## What It Provides

INPE's Programa Queimadas is Brazil's official fire/burn monitoring program. It provides:

- **Active fire detections** (focos de calor) — Satellite-derived hotspots across South America
- **Burnt area mapping** — Aggregated burnt area statistics
- **Fire risk indices** — Regional fire danger ratings
- **Statistics dashboards** — Country, state, municipality, and biome-level aggregations

The reference satellite is AQUA (afternoon pass) for consistent statistical comparisons. Additional satellites (GOES, NOAA, Suomi-NPP, etc.) provide supplementary detections.

## API Details

INPE's fire data is primarily accessed through the BD Queimadas portal and TerraBrasilis platform:

**BD Queimadas portal (query interface):**
```
https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/
```

**Statistics dashboard:**
```
https://terrabrasilis.dpi.inpe.br/queimadas/situacao-atual/
```

**File downloads** are available through the portal with filters by:
- Date range
- Satellite
- Country / state / municipality
- Biome

The portal is primarily a JavaScript-rendered web application. Direct REST API access was not discoverable during testing — data is served through the portal UI and file downloads rather than a programmatic API.

**WMS layers** may be available through:
```
https://terrabrasilis.dpi.inpe.br/geoserver/
```

## Freshness Assessment

Moderate. Daily updates from satellite overpasses. The reference AQUA satellite provides one afternoon pass per day. Multiple other satellites extend detection frequency. Statistics are updated daily.

## Entity Model

Fire detection (foco) records typically include:
- Location (latitude, longitude)
- Satellite name
- Detection date and time
- Municipality, state, country
- Biome
- Fire Radiative Power (FRP)
- Days without rain
- Precipitation data
- Risk level

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily satellite updates |
| Openness | 2 | Public but portal-based, no clean REST API |
| Stability | 2 | Government program but web portal dependency |
| Structure | 1 | No discoverable REST API, JS-rendered portal |
| Identifiers | 1 | No persistent fire IDs in detections |
| Additive Value | 2 | South America / Brazil focus, biome context |
| **Total** | **10/18** | |

## Notes

- The portal is heavily JavaScript-rendered, making automated access difficult.
- For programmatic access to Brazilian fire data, NASA FIRMS covering South America is likely more accessible.
- The biome-level analysis (Cerrado, Amazon, etc.) is unique context not available elsewhere.
- ProCerrado project (World Bank-funded) provides enhanced Cerrado monitoring.
- The statistics pages provide good aggregated views but are not API-friendly.
- Consider as a supplementary/context source rather than a primary data feed.
