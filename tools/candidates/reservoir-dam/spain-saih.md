# Spanish SAIH (Sistema Automático de Información Hidrológica)

**Country/Region**: Spain (organized by river basin authorities)
**Publisher**: Various Confederaciones Hidrográficas (River Basin Authorities) under the Spanish Ministry for the Ecological Transition (MITECO)
**API Endpoint**: Various per basin authority (e.g., `https://www.saihebro.com/`, `https://www.saihtajo.es/`, etc.)
**Documentation**: https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/sistema-automatico-informacion-hidrologica-saih/
**Protocol**: Web portals; some provide WMS/WFS; no standardized REST API
**Auth**: Varies by basin (generally none for public data)
**Data Format**: HTML, CSV (downloads), some XML/JSON
**Update Frequency**: Real-time (5–15 minute intervals for many stations)
**License**: Spanish government open data (Ley de Reutilización de la Información del Sector Público)

## What It Provides

SAIH is Spain's automated hydrological information system, consisting of telemetry networks operated by each of Spain's river basin authorities (Confederaciones Hidrográficas). Each basin has its own SAIH system providing:

- **Reservoir storage** (hm³ and percentage full) for all major Spanish reservoirs
- **Dam inflow/outflow** rates
- **River flow and stage** at gauging stations
- **Precipitation** from rain gauges
- **Water level** at control points

Major basin authorities with SAIH systems:
- **Ebro** (saihebro.com) — largest network, ~200 reservoirs
- **Tajo/Tagus** (saihtajo.es) — includes Madrid's water supply
- **Guadalquivir** (saihguadalquivir.com)
- **Duero** (saihduero.es)
- **Guadiana** (saihguadiana.com)
- **Segura** (saihsegura.com) — critical water-scarce region
- **Júcar** (saih.chj.es)
- **Cantábrico** — various sub-basins

Spain has approximately 1,200 major dams — the highest density of dams in Europe.

## API Details

Each basin authority operates its own web portal with varying levels of API accessibility:

- Most provide interactive web maps and dashboards
- Some offer CSV/Excel data downloads
- A few provide WMS/WFS geospatial services
- There is no standardized national API across all basins

**MITECO national reservoir reports**: The Ministry publishes weekly national reservoir status reports (Boletín Hidrológico) aggregating data from all basins. These are available as PDFs.

**Data aggregation portals**:
- `https://eportal.miteco.gob.es/websaih/` — national SAIH portal (may provide unified access)
- `https://www.embalses.net/` — third-party aggregator of Spanish reservoir data

## Freshness Assessment

Excellent at the basin level — SAIH stations report in real-time at 5–15 minute intervals. However, national-level aggregation is typically weekly. The individual basin portals are the best path for real-time data.

## Entity Model

- **Basin Authority**: Confederación Hidrográfica name, code, region
- **Reservoir (Embalse)**: name, river, capacity (hm³), basin authority
- **Station**: code, name, type (reservoir/river/rain gauge), lat/lon
- **Observation**: timestamp, storage/flow/level value, units

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time at basin level (5–15 min intervals) |
| Openness | 2 | Public portals; API standardization varies; some portals are hard to scrape |
| Stability | 3 | Government infrastructure, legally mandated flood warning systems |
| Structure | 1 | Fragmented across 10+ basin authorities; no unified API |
| Identifiers | 2 | Basin-specific station codes; MITECO has national reservoir codes |
| Additive Value | 3 | ~1,200 dams — highest density in Europe; unique Mediterranean water mgmt data |
| **Total** | **14/18** | |

## Notes

- The fragmentation across basin authorities is the main challenge. Each operates independently with its own web system, URL patterns, and data formats.
- Spain's reservoir system is critically important — the country frequently faces drought conditions, and reservoir levels are a major political and economic indicator.
- The Ebro basin (saihebro.com) is generally the most technically advanced and may be the best starting point for a pilot integration.
- Third-party sites like embalses.net already aggregate this data and might provide a cleaner scraping target.
- MITECO's eportal may eventually provide unified API access — worth monitoring.
- The relationship to Puertos del Estado is complementary: Puertos covers coastal/tidal, while SAIH covers inland/reservoir.
