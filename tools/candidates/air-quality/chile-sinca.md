# Chile SINCA (Sistema de Información Nacional de Calidad del Aire)

**Country/Region**: Chile
**Publisher**: Ministerio del Medio Ambiente (Ministry of Environment)
**API Endpoint**: `https://sinca.mma.gob.cl/` (web portal)
**Documentation**: https://sinca.mma.gob.cl/
**Protocol**: Web application (no public API confirmed)
**Auth**: N/A
**Data Format**: Web/CSV (downloads)
**Update Frequency**: Hourly (on web portal)
**License**: Chilean government open data

## What It Provides

SINCA is Chile's national air quality information system, operated by the Ministry of Environment. It aggregates data from monitoring stations across Chilean cities, with a focus on Santiago (which has some of the worst air quality in South America due to thermal inversions and geographic basin effects). The network covers PM10, PM2.5, O₃, NO₂, SO₂, and CO. Chile's monitoring is concentrated in the central zone (Santiago, Valparaíso, Rancagua) and in cities with industrial or mining activity (Antofagasta, Calama, Temuco).

## API Details

- **Web Portal**: `https://sinca.mma.gob.cl/`
- **Data Access**: Web portal with interactive maps and charts; data downloads in CSV/Excel
  - No public REST API was confirmed during testing (various endpoints returned 401/404)
  - The portal likely uses internal APIs for its JavaScript frontend
- **Station Types**: EMRP (Red de Monitoreo), stations by region
- **Key Cities**: Santiago (~30 stations), Temuco, Rancagua, Antofagasta, Valparaíso, Concepción
- **Pollutants**: PM10, PM2.5, O₃, NO₂, SO₂, CO
- **Air Quality Index**: ICAP (Índice de Calidad del Aire por Partículas) for PM2.5 and PM10

## Freshness Assessment

The web portal shows hourly data for active stations. Historical data is downloadable. No structured API for real-time data was found — access requires web portal interaction or CSV downloads.

## Entity Model

- **Region** → Chilean administrative region
- **Station** → id, name, region, coordinates, type
- **Measurement** → station × pollutant × datetime → value (µg/m³)
- **ICAP** → particulate air quality index

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Hourly data on portal but no API access |
| Openness | 1 | No public API; web-only or CSV download |
| Stability | 2 | Government-operated portal |
| Structure | 0 | No structured data access; web scraping required |
| Identifiers | 1 | Station names on portal; no documented ID scheme |
| Additive Value | 2 | Chile/Santiago — important South American AQ hotspot |
| **Total** | **8/18** | |

## Notes

- Santiago's air quality is a significant public health issue, particularly PM2.5 during winter inversions. The geographic basin traps pollution.
- SINCA returned 401 (Unauthorized) for API-style endpoints during testing, suggesting either authenticated access or deprecated paths.
- For programmatic access to Chilean air quality data, use OpenAQ (which ingests some Chilean stations) or AQICN.
- Temuco in southern Chile has some of the worst PM2.5 levels in the country due to wood-burning heating.
- Chile's monitoring network is less extensive than Mexico's or Brazil's but covers the most polluted areas.
