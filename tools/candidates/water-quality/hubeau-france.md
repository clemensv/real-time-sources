# Hub'Eau — France Water Quality APIs

**Country/Region**: France (metropolitan + overseas territories — 25,000+ monitoring stations)
**Publisher**: BRGM (Bureau de Recherches Géologiques et Minières) / Eaufrance system
**API Endpoint**: `https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/` (surface water); `https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable/` (drinking water)
**Documentation**: https://hubeau.eaufrance.fr/page/apis
**Protocol**: REST API (JSON/CSV/GeoJSON)
**Auth**: None
**Data Format**: JSON, GeoJSON, CSV
**Update Frequency**: Continuous sync with Naïades database (surface WQ); monthly (drinking water)
**License**: French Open License (Licence Ouverte 2.0)

## What It Provides

Hub'Eau is France's national water data API platform, offering programmatic access to the entire French water information system. Two APIs are particularly relevant for water quality:

### Surface Water Quality (qualite_rivieres)
- **25,400+ monitoring stations** across rivers and lakes
- **265 million analyses** of physico-chemical parameters
- Nutrients (nitrogen, phosphorus), metals, pesticides, organic compounds
- Environmental sampling conditions
- Continuously synchronized with the Naïades reference database

### Drinking Water Quality (qualite_eau_potable)
- **124 million+ analyses** from regulatory sanitary controls
- Results per commune and distribution unit (UDI)
- Bacterial contamination, chemical parameters, compliance status
- Updated monthly; latest data from December 2025

Hub'Eau also provides APIs for: river flow (hydrometry), groundwater quality, groundwater levels, river temperature, coastal water surveillance, hydrobiological data, and fish observations — 13 APIs in total.

## API Details

Clean REST API with standard pagination:

```
# Surface water quality stations
GET https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc?size=20&format=json

# Analyses at a station
GET https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc?code_station=01000158&size=20

# Drinking water results for a commune
GET https://hubeau.eaufrance.fr/api/v1/qualite_eau_potable/resultats_dis?code_commune=30007&size=20

# GeoJSON output for mapping
GET https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc?format=geojson
```

Verified working: station_pc endpoint returns 25,431 stations with full metadata (coordinates, commune, department, region, river, water body). Drinking water returns 124M+ analysis records with parameter codes, values, units, and compliance conclusions.

Pagination: page-based with configurable page size (default 5000, max 20000). Depth limit of 20,000 records per query — use discriminating filters for large result sets.

## Freshness Assessment

Good for surface water quality: continuously synced with Naïades. However, the underlying data is primarily from grab samples (discrete sampling events), not continuous sensors. Sampling frequency varies from monthly to quarterly depending on the station and parameter.

Drinking water quality: monthly updates with most recent data typically 1-2 months old.

Neither API provides real-time continuous sensor data — this is a regulatory monitoring database, not a SCADA-style telemetry system.

## Entity Model

- **Station (station_pc)**: code_station, name, coordinates, commune, department, region, river, water body (masse_deau)
- **Analysis (analyse_pc)**: station, date, parameter (code_parametre SANDRE), value, unit, fraction, qualification
- **Drinking Water (resultats_dis)**: commune, distribution unit (UDI), date, parameter (code_parametre), value, limit, compliance
- **Parameter**: SANDRE code, CAS number, name, type

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Continuous DB sync but underlying data is discrete grab samples, not real-time sensors |
| Openness | 3 | No auth, open license, well-documented |
| Stability | 3 | French government infrastructure; legally mandated under EU WFD |
| Structure | 3 | Excellent REST API; JSON/GeoJSON/CSV; pagination; SANDRE parameter codes |
| Identifiers | 3 | SANDRE station codes, CAS numbers for chemicals, EU water body codes |
| Additive Value | 3 | 25K+ stations; 265M analyses; includes drinking water compliance; overseas territories |
| **Total** | **17/18** | |

## Notes

- Hub'Eau is a model for how national water data should be exposed. Clean REST APIs, multiple formats, no authentication, excellent documentation.
- The 13 API endpoints cover the full water cycle — quality, quantity, groundwater, temperature, coastal, biological. A one-stop shop for French water data.
- SANDRE parameter codes are the French water data standard — cross-referenceable with CAS numbers for chemical identification.
- Drinking water API provides per-commune compliance data — potentially useful for public health applications.
- The French overseas territories (Guadeloupe, Martinique, Réunion, French Guiana, Mayotte) extend coverage to the Caribbean, Indian Ocean, and South America.
- Code examples in Python, R, and PHP are available on GitHub — BRGM actively supports developer adoption.
- API health dashboard at `https://hubeau.eaufrance.fr/status` provides real-time monitoring of all endpoints.
