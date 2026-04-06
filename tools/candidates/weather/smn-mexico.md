# Mexico SMN / CONAGUA — Weather Service

**Country/Region**: Mexico (national)
**Publisher**: SMN — Servicio Meteorológico Nacional (part of CONAGUA)
**API Endpoint**: `https://smn.conagua.gob.mx/` (connection timeout)
**Documentation**: https://smn.conagua.gob.mx/
**Protocol**: Unknown (server unreachable)
**Auth**: Unknown
**Data Format**: Unknown
**Update Frequency**: Real-time (weather service)
**License**: Mexican government

## What It Provides

Mexico's SMN (Servicio Meteorológico Nacional) is the national weather service, operated under CONAGUA (Comisión Nacional del Agua). Mexico's meteorological monitoring is critical due to:

- **Tropical cyclones**: Dual exposure — Pacific (more frequent) and Atlantic/Caribbean/Gulf
- **Hurricane season**: June–November; Mexico is one of the most hurricane-impacted countries
- **Monsoon**: North American Monsoon affects northwestern Mexico
- **Temperature extremes**: Desert heat in the north, tropical in the south
- **Altitude effects**: Mexico City at 2,240m; Guadalajara at 1,566m — significant altitude weather
- **Drought**: Northern Mexico under persistent drought

### CONAGUA Hydrology

CONAGUA also operates Mexico's hydrological monitoring network:
- River levels and discharge (already documented in hydrology/mexico-conagua.md)
- Reservoir storage (critical for water supply in arid north)
- Groundwater levels (Mexico City's subsidence from groundwater extraction)

## API Details

```
https://smn.conagua.gob.mx/webservices/?method=1 → Connection timeout
https://smn.conagua.gob.mx/tools/GUI/webservices/?method=1 → Connection timeout
https://api.conagua.gob.mx/informacion-hidrologica/v1/estaciones → Connection timeout
```

All SMN/CONAGUA endpoints were unreachable during testing. The `webservices` paths suggest API endpoints exist but the servers are down.

### Alternative: datos.gob.mx

Mexico's open data portal was also unreachable:
```
https://datos.gob.mx/ → Connection timeout
```

## Integration Notes

- Mexico's hurricane vulnerability makes weather data critically important
- The dual-ocean tropical cyclone exposure is unique
- datos.gob.mx historically hosted CONAGUA and SMN datasets
- Mexico City's weather station network would be valuable for the 22M metro area
- CONAGUA hydrology data is already documented separately (mexico-conagua.md)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Weather service presumably real-time |
| Openness | 0 | All endpoints unreachable |
| Stability | 1 | Government service; significant downtime |
| Structure | 1 | `webservices` path suggests API exists |
| Identifiers | 1 | WMO station codes likely used |
| Additive Value | 2 | Dual-ocean hurricane exposure; 130M population |
| **Total** | **6/18** | |

## Verdict

⏭️ **Skip** — Server infrastructure unreachable. SMN/CONAGUA web services likely exist but are down. Revisit when servers recover. Mexico's hurricane data is important but NOAA/NWS provides excellent coverage of Mexico-bound storms.
