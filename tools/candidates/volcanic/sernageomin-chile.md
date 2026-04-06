# SERNAGEOMIN Chile — Volcanic Monitoring (RNVV)

**Country/Region**: Chile (national)
**Publisher**: SERNAGEOMIN — Servicio Nacional de Geología y Minería
**API Endpoint**: `https://rnvv.sernageomin.cl/` (connection failed), `https://www.sernageomin.cl/red-nacional-de-vigilancia-volcanica/` (connection failed)
**Documentation**: https://www.sernageomin.cl/
**Protocol**: Unknown
**Auth**: N/A
**Data Format**: Unknown
**Update Frequency**: Continuous monitoring
**License**: Chilean government

## What It Provides

Chile has approximately 90 potentially active volcanoes — the second-most of any country after Indonesia. The Chilean volcanic arc stretches 4,300 km along the Andes, with several distinct volcanic zones:

- **Northern Volcanic Zone**: High-altitude stratovolcanoes in the Atacama (Láscar, Ojos del Salado area)
- **Central Volcanic Zone**: Villarrica, Llaima — among the most active in South America
- **Southern Volcanic Zone**: Chaitén (explosive 2008 eruption), Calbuco (2015 eruption)
- **Austral Zone**: Hudson, remote Patagonian volcanoes

SERNAGEOMIN's Red Nacional de Vigilancia Volcánica (RNVV) monitors 45 of these volcanoes with seismic, geodetic, and geochemical instruments. The agency issues Technical Volcanic Alert Levels (Verde/Amarillo/Naranja/Rojo).

### Notable Recent Activity

- **Villarrica** (2,847m): Most active Chilean volcano; lava lake visible in crater; frequent Strombolian eruptions (2015 VEI 2 eruption forced evacuations)
- **Calbuco**: Surprise eruption in April 2015 after 43 years of quiet — demonstrated need for real-time monitoring
- **Nevados de Chillán**: Complex sustained eruption since 2016; dome growth and pyroclastic flows

## API Details

All tested endpoints were unreachable:
```
https://rnvv.sernageomin.cl/volcanologia/api/volcanes → Connection failed
https://www.sernageomin.cl/red-nacional-de-vigilancia-volcanica/ → Connection failed
```

SERNAGEOMIN may use geographic IP restrictions or require specific user agents.

## Integration Notes

- Chile's volcanic monitoring is critical — Villarrica's lava lake is one of only ~5 persistent lava lakes on Earth
- VAAC Buenos Aires covers Chilean volcanic ash advisories
- MIROVA satellite thermal monitoring covers Chilean volcanoes
- The technical alert level system (Verde/Amarillo/Naranja/Rojo) is structured data if accessible
- Combined with CSN seismicity data, a comprehensive Chile geohazard monitoring system could be built

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Presumably real-time but inaccessible |
| Openness | 0 | Connection failures on all endpoints |
| Stability | 1 | Government agency |
| Structure | 0 | Cannot assess |
| Identifiers | 0 | Cannot assess |
| Additive Value | 3 | 90 active volcanoes; Villarrica lava lake; Patagonia |
| **Total** | **5/18** | |

## Verdict

⏭️ **Skip** — Server unreachable. Chile's volcanic data is exceptionally valuable (90 volcanoes, Villarrica lava lake) but not programmatically accessible. MIROVA and VAAC Buenos Aires provide partial coverage.
