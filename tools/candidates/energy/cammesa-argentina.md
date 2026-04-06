# CAMMESA Argentina — Grid Operator

**Country/Region**: Argentina (national)
**Publisher**: CAMMESA — Compañía Administradora del Mercado Mayorista Eléctrico
**API Endpoint**: Various `https://cammesaweb.cammesa.com/` and `https://api.cammesa.com/` (all 404)
**Documentation**: https://cammesaweb.cammesa.com/
**Protocol**: REST (suspected ASP.NET/Angular SPA)
**Auth**: Unknown (API endpoints not found)
**Data Format**: Unknown
**Update Frequency**: Real-time (dashboard updates)
**License**: Argentine government entity

## What It Provides

CAMMESA operates Argentina's wholesale electricity market and national grid dispatch. Argentina has the third-largest economy in South America with a diverse energy mix:

- **Thermal**: ~60% (natural gas dominant — Argentina has Vaca Muerta shale gas)
- **Hydro**: ~25% (including major dams on the Paraná system; Yacyretá binational with Paraguay)
- **Nuclear**: ~7% (Atucha I, II, and Embalse plants — Argentina has indigenous nuclear technology)
- **Wind**: Growing rapidly in Patagonia (some of the best wind resources on Earth)
- **Solar**: Growing in the northwest Andean region (Jujuy, Salta)

The CAMMESA website displays real-time demand, generation by fuel type, and regional breakdowns.

## API Details

Extensive probing failed to locate working API endpoints:

```
https://api.cammesa.com/demanda-svc/demanda/ObtenerDemandaYTemperatura → 404
https://api.cammesa.com/pub-svc/public/findDocumentosByNombreAndFecha → 404
https://cammesaweb.cammesa.com/demanda-svc/demanda/ObtenerDemandaYTemperatura → 404
https://cammesaweb.cammesa.com/generacion-api/api/generacion → HTML (download page)
https://cammesaweb.cammesa.com/renov-api/renovables/ObtieneGeneracion → 404
https://portalbi.cammesa.com/portal-bi/PortalBI/PublicoGeneral/Demanda → Connection failed
https://demanda.cammesa.com/demanda/ → Connection failed
```

The `generacion-api` endpoint returned an HTML download page (dated 2021), suggesting the API structure has changed. The Portal BI uses internal APIs that are not publicly accessible.

### Alternative: datos.gob.ar

Argentina's open data portal (datos.gob.ar) returned 403 during testing. May host CAMMESA data.

## Integration Notes

- Argentina's grid is interconnected with Brazil, Uruguay, Paraguay, and Chile
- Vaca Muerta shale gas is transforming Argentina's energy landscape
- Patagonian wind resources rival North Sea and US Great Plains
- The nuclear program (three plants operational) is unique in South America
- CAMMESA's Portal BI visual dashboard clearly has underlying APIs — they're just not publicly documented or accessible

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Dashboard shows real-time data, but no API access |
| Openness | 0 | All probed endpoints returned 404 or connection failures |
| Stability | 1 | Government entity; API paths appear to have changed |
| Structure | 1 | Likely JSON behind the SPA but inaccessible |
| Identifiers | 1 | Unknown |
| Additive Value | 3 | Argentina is South America's 3rd largest grid; nuclear + Vaca Muerta + Patagonian wind |
| **Total** | **7/18** | |

## Verdict

⏭️ **Skip for now** — No working API endpoints found despite extensive probing. CAMMESA clearly has internal APIs powering their dashboard. The API paths may have been restructured. Revisit with browser dev tools to capture actual API calls from the SPA. Argentina's grid data is inherently valuable — nuclear, shale gas, and Patagonian wind make it unique.
