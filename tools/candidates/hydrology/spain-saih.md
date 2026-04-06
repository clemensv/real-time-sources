# Spain SAIH (Automatic Hydrological Information Systems)

**Country/Region**: Spain
**Publisher**: Confederaciones Hidrográficas (River Basin Authorities) under MITECO
**API Endpoint**: Various regional portals (no unified API)
**Documentation**: https://www.saihduero.es/ , https://saihtajo.chtajo.es/ , etc.
**Protocol**: Web portals (SPA) — no public REST API found
**Auth**: N/A (web-only access)
**Data Format**: HTML
**Update Frequency**: 15 minutes (per SAIH protocol)
**Station Count**: 3000+ stations nationwide across all basins
**License**: Spanish government data

## What It Provides

Spain's SAIH system is one of Europe's most comprehensive real-time hydrological monitoring networks. Each of Spain's river basin confederations operates its own SAIH portal:

- **SAIH Ebro** (saihebro.com) — Ebro basin, NE Spain
- **SAIH Duero** (saihduero.es) — Duero basin, NW Spain
- **SAIH Tajo** (saihtajo.chtajo.es) — Tajo/Tagus basin, central Spain
- **SAIH Guadalquivir** (saihguadalquivir.com) — Guadalquivir basin, S Spain
- **SAIH Segura** (saihsegura.com) — Segura basin, SE Spain
- **SAIH Júcar** — Júcar basin, E Spain
- **SAIH Guadiana** — Guadiana basin, SW Spain
- **SAIH Miño-Sil** — Galicia

Data includes:
- Real-time water levels at river gauges
- Reservoir storage (% capacity)
- Rainfall stations
- Dam inflow/outflow

## API Details

### SAIH Duero (confirmed accessible)
The portal at `https://www.saihduero.es/datos-tiempo-real` renders real-time data including reservoir storage percentages for all Duero basin dams.

### SAIH Tajo (confirmed accessible)
The portal at `https://saihtajo.chtajo.es/` is a modern SPA (Leaflet maps, D3/C3 charts, Onsen UI) that loads data dynamically. Backend API endpoints were probed but returned "pagina no existe" for various URL patterns.

### SAIH Ebro, Guadalquivir, Segura
Connection failures in testing — these portals may be intermittently available or behind network restrictions.

### No public API
Despite extensive probing of URL patterns (`/api/`, `/rest/`, `/geojson/`, `/ajax/`), no public machine-readable API was found for any SAIH portal. All data appears to be delivered through server-rendered HTML or SPA-internal JavaScript calls.

## Freshness Assessment

- SAIH systems are designed for 15-minute real-time updates
- Duero portal confirmed showing current reservoir data
- Tajo portal loads but backend API is not publicly accessible
- Other portals intermittently available

## Entity Model

- **Basin (Confederación)**: Ebro, Duero, Tajo, Guadalquivir, Segura, Júcar, Guadiana, Miño-Sil
- **Station**: name, type (river gauge, dam, rain gauge), location
- **Reservoir**: name, province, capacity, current storage (%)
- **Observation**: timestamp, water level (cm), flow (m³/s), rainfall (mm)

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | No public API; web-only access via HTML/SPA |
| Data Richness | 3 | Comprehensive: water levels, reservoir storage, rainfall, discharge |
| Freshness | 3 | 15-minute SAIH protocol updates |
| Station Coverage | 3 | 3000+ stations across all Spanish river basins |
| Documentation | 0 | No API documentation exists |
| License/Access | 1 | Public web data but no structured API access |
| **Total** | **10/18** | |

## Notes

- Spain has one of Europe's richest hydrological monitoring networks — frustratingly inaccessible via API
- Each basin authority operates independently, making unified access even harder
- The SAIH Tajo portal is the most modern (2024+ redesign) but still no public API
- Web scraping is theoretically possible but fragile due to SPA architecture and varied portal designs
- Spain's open data portal (datos.gob.es) may have downloadable datasets but not real-time feeds
- The EU INSPIRE directive should eventually require WFS/WCS service endpoints for this data
- Consider monitoring Spanish open data policy developments — API access may improve
- Previously dismissed but re-investigated with same conclusion: no public API available
