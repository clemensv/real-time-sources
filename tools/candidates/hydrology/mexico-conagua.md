# Mexico CONAGUA (National Water Commission)

**Country/Region**: Mexico
**Publisher**: Comisión Nacional del Agua (CONAGUA)
**API Endpoint**: `https://sih.conagua.gob.mx/` (web portal, behind Cloudflare)
**Documentation**: https://www.gob.mx/conagua
**Protocol**: Web portal (behind WAF challenge)
**Auth**: N/A (web-only, Cloudflare challenge)
**Data Format**: HTML
**Update Frequency**: Real-time to daily
**Station Count**: 5000+ hydrometric stations (historical), ~800 automated
**License**: Mexican government open data

## What It Provides

CONAGUA operates Mexico's national hydrological network:
- **SIH (Sistema de Información Hidrológica)** — hydrological information system
- Real-time water levels in major rivers
- Reservoir storage and operations (164 major dams)
- Rainfall monitoring network
- Groundwater level monitoring

## API Details

### Web portals (all behind Cloudflare WAF)
- `https://sih.conagua.gob.mx/Nacional/Mapa` — returns Cloudflare challenge page
- `https://www.conagua.gob.mx/Atlas/mapa/13/index_svg.html` — returns Cloudflare challenge
- `https://app.conagua.gob.mx/bandeja.aspx` — behind challenge

All CONAGUA domains are protected by a Cloudflare Web Application Firewall that requires browser JavaScript execution to pass a proof-of-work challenge.

### Mexican open data portal
The Mexican government open data platform at datos.gob.mx may have CONAGUA datasets, but these are typically static downloads rather than real-time APIs.

## Freshness Assessment

- CONAGUA operates real-time monitoring across Mexico
- Data exists behind web portals but not API-accessible
- Cloudflare WAF prevents programmatic access to any CONAGUA endpoint

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | All endpoints behind Cloudflare WAF challenge |
| Data Richness | 3 | Comprehensive: rivers, reservoirs, groundwater, rainfall |
| Freshness | 2 | Real-time data exists behind portal |
| Station Coverage | 3 | 5000+ historical stations, 800+ automated |
| Documentation | 0 | No API documentation |
| License/Access | 0 | Cloudflare WAF blocks all programmatic access |
| **Total** | **8/18** | |

## Notes

- Mexico has one of Latin America's most extensive hydrological networks but zero API access
- The Cloudflare WAF protection is aggressive — even basic HTTP requests are challenged
- 164 major dams are a critical water management concern (drought monitoring)
- CONAGUA data may be accessible via Mexico's datos.gob.mx open data portal as bulk downloads
- The WAF challenge is a significant barrier that cannot be bypassed ethically
