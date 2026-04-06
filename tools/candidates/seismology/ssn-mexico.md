# SSN Mexico — Servicio Sismológico Nacional

**Country/Region**: Mexico (national)
**Publisher**: Servicio Sismológico Nacional, UNAM
**API Endpoint**: `https://ssn.unam.mx/` (connection timeout)
**Documentation**: https://ssn.unam.mx/
**Protocol**: Unknown (server unreachable)
**Auth**: N/A
**Data Format**: Unknown
**Update Frequency**: Near-real-time (normally)
**License**: UNAM/Mexican government

## What It Provides

The SSN (Servicio Sismológico Nacional) operates Mexico's national seismograph network from UNAM's Instituto de Geofísica. Mexico is one of the most seismically active countries in the Americas:

- **Pacific subduction**: Cocos plate subducting under the North American plate along the Pacific coast
- **Guerrero seismic gap**: A 200+ km section of the subduction zone that hasn't ruptured since 1911 — considered a major seismic hazard for Mexico City
- **Intraslab earthquakes**: Deep events beneath central Mexico that severely affect Mexico City due to the ancient lakebed amplification effect (devastating in 1985 and 2017)
- **Transform faulting**: Gulf of California spreading center

Mexico detects hundreds of earthquakes monthly, and Mexico City's unique geology (built on a drained lakebed) makes seismic monitoring critical for 22+ million residents.

## API Details

```
GET https://ssn.unam.mx/ → Connection timeout
GET https://ssn.unam.mx/json/catalogo-2026.json → Connection timeout
GET https://www2.ssn.unam.mx:8080/catalogo-json → Connection timeout
```

SSN's servers were unreachable during testing. This may be:
- Temporary downtime
- Geographic IP restrictions (blocking non-Mexican IPs)
- Server infrastructure issues

The SSN website historically provided HTML tables and some JSON endpoints for recent earthquakes.

## Freshness Assessment

Unable to assess — server unreachable.

## Integration Notes

- Mexico's SASMEX early warning system is separate from SSN and not publicly accessible
- USGS and EMSC capture Mexican events M4+ with good coverage
- Mexico is part of the Pacific Ring of Fire with very high seismicity
- datos.gob.mx was also unreachable during testing

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Presumably real-time but server unreachable |
| Openness | 0 | Connection timeout |
| Stability | 1 | UNAM institution, but server issues |
| Structure | 1 | Historical JSON endpoints known to exist |
| Identifiers | 1 | Unknown without access |
| Additive Value | 2 | Major seismic zone; Mexico City vulnerability |
| **Total** | **6/18** | |

## Verdict

⏭️ **Skip** — Server unreachable. Mexico's seismicity is well-covered by USGS/EMSC for M4+ events. Revisit when SSN servers are accessible — they historically offered usable JSON. The Guerrero gap and Mexico City vulnerability make this a scientifically important source if it becomes available.
