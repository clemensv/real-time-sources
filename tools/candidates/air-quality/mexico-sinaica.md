# Mexico SINAICA (Sistema Nacional de Información de la Calidad del Aire)

**Country/Region**: Mexico
**Publisher**: INECC (Instituto Nacional de Ecología y Cambio Climático) / SEMARNAT
**API Endpoint**: `https://sinaica.inecc.gob.mx/` (web portal; internal API)
**Documentation**: https://sinaica.inecc.gob.mx/
**Protocol**: Web application (internal JSON API)
**Auth**: None for web; internal API endpoints may require specific URL patterns
**Data Format**: JSON (internal), CSV (downloads)
**Update Frequency**: Hourly
**License**: Mexican government open data

## What It Provides

SINAICA is Mexico's national air quality information system, aggregating data from monitoring networks in major metropolitan areas (Mexico City/ZMVM, Guadalajara, Monterrey, Puebla, León, Toluca, and 30+ other cities). It provides hourly measurements of PM10, PM2.5, O₃, NO₂, SO₂, CO, and the Mexican Air Quality Index (IMECA/AQI). Mexico City's network alone has ~40 stations, making it one of the densest urban monitoring systems in Latin America.

## API Details

- **Web Portal**: `https://sinaica.inecc.gob.mx/`
- **Data Access**: Primarily through the web portal's internal JavaScript API endpoints
  - No officially documented public REST API was found
  - Data downloads available in CSV/Excel format from the portal
- **Metropolitan Networks**: Each city operates its own network feeding into SINAICA
  - Mexico City (SIMAT/RAMA): ~40 stations, most comprehensive
  - Monterrey: ~10 stations
  - Guadalajara: ~10 stations
  - 30+ other cities with varying station counts
- **IMECA/AQI Scale**: Mexican air quality index used for public communication
- **Pollutants**: PM10, PM2.5, O₃, NO₂, SO₂, CO

## Freshness Assessment

Hourly data is available on the web portal with typical delays of 1-2 hours. Historical data can be downloaded. The portal appears to use internal JSON APIs for its interactive maps, which could potentially be reverse-engineered but are not officially documented.

## Entity Model

- **Network** → metropolitan area monitoring network (e.g., ZMVM, Monterrey, Guadalajara)
- **Station** → id, name, network, coordinates, type
- **Measurement** → station × pollutant × datetime → value (µg/m³)
- **IMECA** → station × datetime → index value

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly data on portal |
| Openness | 1 | No documented public API; web scraping or CSV download required |
| Stability | 2 | Government-operated but informal API access |
| Structure | 1 | No structured API; internal endpoints not documented |
| Identifiers | 2 | Station codes within each network |
| Additive Value | 2 | Major Latin American country; Mexico City is a key AQ hotspot |
| **Total** | **11/18** | |

## Notes

- The main challenge is the absence of a documented public API. SINAICA appears to expose internal JSON endpoints that power its web portal, but these are undocumented and may change without notice.
- Mexico City's air quality is globally significant due to its altitude (2,240 m), population (22M metro), and ozone issues.
- For programmatic access, consider using OpenAQ (which ingests some Mexican station data) or AQICN as intermediaries.
- CSV/Excel downloads from the portal are the most reliable data access method for historical analysis.
- The portal had some endpoint issues during testing (404 errors), suggesting possible infrastructure changes.
