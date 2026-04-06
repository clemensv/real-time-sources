# CENAPRED Mexico — Disaster Alerts

**Country/Region**: Mexico (national)
**Publisher**: CENAPRED — Centro Nacional de Prevención de Desastres
**API Endpoint**: `https://www.cenapred.unam.mx/` (connection timeout)
**Documentation**: https://www.cenapred.unam.mx/
**Protocol**: Unknown (server unreachable)
**Auth**: N/A
**Data Format**: Unknown
**Update Frequency**: Event-driven
**License**: Mexican government

## What It Provides

CENAPRED is Mexico's national disaster prevention center, managing the Semáforo de Alerta Volcánica (Volcanic Alert Traffic Light) and coordinating multi-hazard early warning. Mexico faces an exceptional range of natural hazards:

- **Volcanic**: Popocatépetl (5,426m, 25 million people live within 100 km), Colima (most active), plus Citlaltépetl, Nevado de Toluca, San Martín Tuxtla
- **Seismic**: Pacific subduction (see ssn-mexico.md)
- **Hurricane**: Both Pacific and Atlantic/Caribbean coasts
- **Flooding**: Major river systems (Grijalva-Usumacinta, Pánuco) + tropical rainfall
- **Landslides**: Mountainous terrain + deforestation + intense rainfall

### Semáforo de Alerta Volcánica

The most valuable CENAPRED product is the volcanic alert traffic light for Popocatépetl:
- **Verde (Green)**: Normal activity
- **Amarillo Fase 1/2/3 (Yellow)**: Increased activity / approach to eruption
- **Rojo (Red)**: Major eruption in progress

Popocatépetl's alert status affects 25+ million people and can ground flights at Mexico City's airport.

## API Details

```
https://www.cenapred.unam.mx/ → Connection timeout
https://www.cenapred.unam.mx/reportes/sismos.json → Connection timeout
```

Server unreachable during testing — same connectivity issues as SSN (both hosted at UNAM).

## Integration Notes

- Popocatépetl is one of the world's most dangerous volcanoes by population exposure
- The volcanic traffic light system is a structured alert that maps naturally to CloudEvents
- CENAPRED's multi-hazard approach (volcanoes + earthquakes + hurricanes + floods) is comprehensive
- Mexico's hurricane exposure to both ocean basins is unique
- datos.gob.mx was also unreachable during testing

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Presumably real-time alerts |
| Openness | 0 | Connection timeout |
| Stability | 1 | Government institution (UNAM infrastructure) |
| Structure | 1 | Volcanic traffic light is inherently structured |
| Identifiers | 1 | Volcano IDs are standard |
| Additive Value | 3 | Popocatépetl + 25M population exposure |
| **Total** | **7/18** | |

## Verdict

⏭️ **Skip** — Server unreachable (UNAM infrastructure issues). Popocatépetl's volcanic traffic light would be an excellent CloudEvents source if accessible. Smithsonian GVP and VAAC Washington provide partial coverage. Revisit when servers are accessible.
