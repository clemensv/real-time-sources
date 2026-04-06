# Chile DGA / SNIA Water Resources

**Country/Region**: Chile
**Publisher**: Dirección General de Aguas (DGA), Ministerio de Obras Públicas
**API Endpoint**: `https://snia.mop.gob.cl/BNAConsultas/reportes` (403 Forbidden)
**Documentation**: https://dga.mop.gob.cl/
**Protocol**: Web portal
**Auth**: N/A (403 on API attempts)
**Data Format**: HTML / download files
**Update Frequency**: Daily to monthly
**Station Count**: 1000+ stations
**License**: Chilean government data

## What It Provides

Chile's DGA operates the national water monitoring network:
- River water level and discharge monitoring
- Reservoir storage
- Groundwater level monitoring
- Water quality
- Snow water equivalent (critical for Andean snowmelt)

Chile's unique geography (4,300 km long, Andes to Pacific) creates diverse hydrological conditions.

## API Details

### SNIA Portal
- `https://snia.mop.gob.cl/BNAConsultas/reportes` — returns 403 Forbidden
- The SNIA (Sistema Nacional de Información del Agua) provides data download after registration

### DGA Website
- `https://dga.mop.gob.cl/` — informational website with links to data services
- Historical data available for download (not real-time API)

## Freshness Assessment

- DGA operates real-time monitoring but access is restricted
- Historical data downloadable after registration
- No real-time API access confirmed

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | 403 Forbidden on data endpoints |
| Data Richness | 2 | Water levels, discharge, groundwater, snow |
| Freshness | 1 | Historical downloads; no real-time API |
| Station Coverage | 2 | 1000+ stations across Chile's diverse geography |
| Documentation | 1 | Spanish-language website documentation |
| License/Access | 0 | 403 Forbidden; registration may be required |
| **Total** | **6/18** | |

## Notes

- Chile's Andean snowmelt hydrology is critical for South American water resources
- Access restrictions prevent programmatic integration
- Registration on SNIA may enable data download (not tested)
- Chile's open data initiatives may improve access in the future
