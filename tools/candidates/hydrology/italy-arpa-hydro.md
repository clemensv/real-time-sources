# Italy ISPRA / Regional ARPA Agencies — Hydrology

**Country/Region**: Italy
**Publisher**: ISPRA (national), Regional ARPA agencies (Lombardia, Piemonte, Veneto, Emilia-Romagna)
**API Endpoint**: No public API found
**Documentation**: Various regional portals
**Protocol**: Web portals (HTML/SPA)
**Auth**: N/A
**Data Format**: HTML only
**Update Frequency**: 15-30 minutes (regional monitoring networks)
**Station Count**: 1000+ across all regions
**License**: Italian government data

## What It Provides

Italy's hydrological monitoring is fragmented across national and regional agencies:

### ISPRA (National)
- **IdroGEO** (idrogeo.isprambiente.it) — national landslide and flood hazard platform
- Focused on hazard assessment and risk indicators, not real-time water levels
- Open source (GNU AGPL v3) but primarily a GIS visualization tool

### Regional ARPA agencies
- **ARPA Lombardia** — rivers.arpalombardia.it (connection failures in testing)
- **ARPA Piemonte** — arpa.piemonte.it (opendata section returned 404)
- **ARPA Veneto** — arpa.veneto.it (connection failures)
- **ARPA Emilia-Romagna** — allertameteo.regione.emilia-romagna.it (HTML alert portal, no API)
- **ARPA Friuli Venezia Giulia**, **ARPA Toscana**, etc.

Each region operates independently with different portal technologies and no common API standard.

## API Details

### Endpoints probed (all failed)
- `https://rivers.arpalombardia.it/` — connection failure
- `https://www.arpa.piemonte.it/opendata` — 404
- `https://www.arpa.veneto.it/bollettini/meteo/h24/dati_idrometeo.php` — connection failure
- `https://allertameteo.regione.emilia-romagna.it/livello-idrometrico` — HTML-only portal
- `https://allertameteo.regione.emilia-romagna.it/api/idrometri` — 404
- `https://allertameteo.regione.emilia-romagna.it/o/api/allerta/get-sensor-values-no-alarm?...` — 404
- `https://dati.isprambiente.it/id/` — 404

### IdroGEO
The national IdroGEO platform is open-source (GitLab) and serves as a hazard/risk platform, not a real-time water level API. It focuses on:
- Landslide inventory (IFFI)
- Flood hazard maps
- Risk indicators

## Freshness Assessment

- Regional monitoring networks operate in real-time (15-30 minute updates)
- Data is visible on web portals but not accessible via API
- Italy's INSPIRE implementation may eventually mandate WFS endpoints
- Emilia-Romagna's alert platform uses Liferay CMS with no public API layer

## Entity Model

- **Region**: Lombardia, Piemonte, Veneto, Emilia-Romagna, etc.
- **Station**: idrometro (water level gauge), name, river, coordinates
- **Observation**: timestamp, water level, flow, alert thresholds

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | No public API found across any agency |
| Data Richness | 2 | Rich monitoring data exists behind web portals |
| Freshness | 2 | Real-time data exists but not API-accessible |
| Station Coverage | 3 | 1000+ stations across Italian regions |
| Documentation | 0 | No API documentation |
| License/Access | 1 | Public web access; no structured data access |
| **Total** | **8/18** | |

## Notes

- Italy's hydrological data is frustratingly fragmented across 20+ regional agencies
- No national-level real-time water level API exists (unlike France's Hub'Eau or Germany's PegelOnline)
- ISPRA's IdroGEO is open source but focused on hazard assessment, not real-time monitoring
- Individual regions may have hidden APIs behind their SPAs — further investigation with browser devtools would be needed
- The EU Water Framework Directive and INSPIRE should eventually drive API availability
- South Tyrol (Bolzano/Bozen) may have separate open data (German-speaking, Austrian-influenced data culture)
- This represents a significant gap in European hydrology API coverage
