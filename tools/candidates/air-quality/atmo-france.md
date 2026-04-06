# Atmo France (French AASQA Air Quality Networks)

**Country/Region**: France
**Publisher**: Atmo France (federation of AASQAs — Associations Agréées de Surveillance de la Qualité de l'Air)
**API Endpoint**: `https://admindata.atmo-france.org/api/` (Atmo Data) and regional AASQA APIs
**Documentation**: https://data-atmo-france.opendata.arcgis.com/ (ArcGIS open data hub)
**Protocol**: REST (ArcGIS Feature Services), various regional APIs
**Auth**: Varies by AASQA (some open, some require registration)
**Data Format**: JSON (ArcGIS), CSV
**Update Frequency**: Hourly
**License**: Licence Ouverte / Open Licence 2.0 (French government)

## What It Provides

France's air quality monitoring is operated by a network of regional AASQAs (Approved Air Quality Monitoring Associations), federated under Atmo France. Each AASQA operates its own monitoring stations and may provide its own API. Key regional agencies include:
- **Airparif** (Île-de-France / Paris region) — the largest and best-known
- **AtmoSud** (Provence-Alpes-Côte d'Azur)
- **Atmo Auvergne-Rhône-Alpes**
- **Atmo Hauts-de-France**
- **Air Pays de la Loire**
- Others covering all French regions

Atmo France provides a national aggregation through an ArcGIS-based open data portal with ~700+ monitoring stations nationwide. Pollutants include PM10, PM2.5, NO₂, O₃, SO₂, and the French ATMO index.

## API Details

- **National Open Data Hub**: `https://data-atmo-france.opendata.arcgis.com/`
  - ArcGIS Feature Services for stations, measurements, indices
  - GeoJSON, CSV exports
- **Airparif** (Paris):
  - Website: https://www.airparif.fr/
  - Data available via API (registration may be required)
  - Covers Île-de-France with ~70 stations
- **AtmoSud** (PACA):
  - Website: https://www.atmosud.org/
  - Open data available
- **National Index (ATMO)**: French composite AQI calculated from PM10, PM2.5, NO₂, O₃, SO₂
  - Scale: 1 (Bon/Good) to 6 (Extrêmement mauvais/Extremely poor)
- **Regional APIs**: Each AASQA may expose different API patterns — no single national REST API

## Freshness Assessment

Hourly measurements are available through the national ArcGIS portal and individual AASQA websites. The ATMO index is calculated daily. Real-time data availability varies by AASQA. The ArcGIS portal provides the most accessible aggregated view.

## Entity Model

- **AASQA** → regional association (Airparif, AtmoSud, etc.)
- **Station** → id, name, AASQA, region, coordinates, type (traffic/industrial/background)
- **Component** → pollutant (PM10, PM2.5, NO₂, O₃, SO₂)
- **Measurement** → station × component × datetime → value (µg/m³)
- **ATMO Index** → location × date → index value (1-6)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly data available |
| Openness | 2 | National portal is open; some AASQAs require registration |
| Stability | 2 | Federated structure means varying API quality; ArcGIS is stable |
| Structure | 2 | ArcGIS Feature Services are standardised but complex; no simple REST JSON |
| Identifiers | 2 | Station codes vary by AASQA; national dataset on ArcGIS provides some consistency |
| Additive Value | 2 | France-wide; partially in EEA/OpenAQ; ATMO index is unique |
| **Total** | **13/18** | |

## Notes

- France's federated AASQA model means there is no single national REST API — this is the main integration challenge.
- The ArcGIS open data hub (`data-atmo-france.opendata.arcgis.com`) is the best single entry point for national data.
- Airparif (Paris) is the most prominent AASQA and has the most sophisticated data infrastructure.
- The ATMO index uses a 1-6 scale that differs from other countries' AQI scales — conversion tables are needed.
- ArcGIS Feature Services support spatial queries, attribute filters, and pagination — powerful but requires ArcGIS REST API knowledge.
- French government open data licence (Licence Ouverte 2.0) is broadly permissive, similar to CC BY.
- For simplest integration, use OpenAQ or EEA as intermediaries — they already ingest most French station data.
