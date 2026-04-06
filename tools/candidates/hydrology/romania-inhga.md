# Romania INHGA (National Institute of Hydrology and Water Management)

**Country/Region**: Romania
**Publisher**: INHGA (Institutul Național de Hidrologie și Gospodărire a Apelor)
**API Endpoint**: `https://www.hidro.ro/` (redirected portal)
**Documentation**: https://www.inhga.ro/
**Protocol**: WordPress site (no structured API)
**Auth**: N/A
**Data Format**: HTML
**Update Frequency**: Daily hydrological reports
**Station Count**: 500+ gauging stations
**License**: Romanian government data

## What It Provides

Romania's hydrological monitoring covers:
- Danube river water levels (Romania has 1,075 km of Danube)
- Tributary river monitoring (Olt, Mureș, Siret, Prut, Jiu, etc.)
- Flood forecasting and warning
- Daily hydrological bulletins

## API Details

### Web access
- `https://www.inhga.ro/` — main site, redirects to `https://www.hidro.ro/`
- `https://www.hidro.ro/` — WordPress-based portal
- `https://www.hidro.ro/wp-json/` — WordPress REST API (standard WP endpoints, not hydrology data)
- `https://apele-romane.ro/` — DNS failure

### No structured API
The WordPress REST API at hidro.ro provides standard content management endpoints (pages, posts) but no hydrological data API.

### Probed endpoints
- `https://hidroinfo.ro/api/stations` — connection failure
- WordPress REST API present but contains CMS content only

## Freshness Assessment

- INHGA publishes daily hydrological reports on the website
- Data exists but in PDF/HTML bulletin format, not machine-readable
- Romania is a key Danube basin country with extensive monitoring

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | WordPress site only; no hydrology API |
| Data Richness | 2 | Rich monitoring network but data locked in bulletins |
| Freshness | 1 | Daily bulletins; no real-time API |
| Station Coverage | 2 | 500+ stations on Danube and tributaries |
| Documentation | 0 | No API documentation |
| License/Access | 1 | Public website; no structured access |
| **Total** | **6/18** | |

## Notes

- Romania is critical for Danube hydrology but lacks public API
- The ICPDR (International Commission for the Protection of the Danube River) aggregates Danube data from member states but also lacks a public API
- Romania's extensive river network (including 1,075 km of Danube) represents significant data
- Consider monitoring EU open data developments that may force API availability
