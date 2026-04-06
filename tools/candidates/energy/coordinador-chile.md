# CEN / Coordinador Eléctrico Nacional — Chile Energy Grid

**Country/Region**: Chile (national — Sistema Eléctrico Nacional / SEN)
**Publisher**: Coordinador Eléctrico Nacional (CEN)
**API Endpoint**: `https://www.coordinador.cl/` (403), `https://sipub.coordinador.cl/` (404)
**Documentation**: https://www.coordinador.cl/operacion/graficos/operacion-real/
**Protocol**: REST (WordPress + internal API)
**Auth**: Unknown (403 on all API paths)
**Data Format**: Unknown (likely JSON behind WordPress frontend)
**Update Frequency**: Real-time (dashboard updates)
**License**: Chilean government entity

## What It Provides

CEN operates Chile's unified national electric system (SEN, merged from the former SIC and SING in 2017). Chile's energy grid is distinctive:

- **Solar**: World-class solar resources in the Atacama Desert (highest irradiance on Earth); over 10 GW installed
- **Wind**: Patagonian and coastal wind resources growing rapidly
- **Hydro**: Traditional Andean hydro (declining share due to drought and environmental concerns)
- **Copper mining demand**: Chile is the world's largest copper producer; mining consumes ~30% of electricity
- **Green hydrogen**: Chile is positioning as a global green hydrogen producer using Atacama solar and Patagonian wind
- **Geography**: 4,300 km long, narrow grid — extreme transmission challenges

### Energía Abierta

Chile's energy open data portal (energiaabierta.cl / datos.energiaabierta.cl) was unreachable during testing. This portal is known to host generation, demand, and pricing data.

## API Details

All tested endpoints returned 403 or failed:

```
https://www.coordinador.cl/operacion/graficos/operacion-real/generacion-real-del-sistema/ → 403
https://www.coordinador.cl/wp-json/cen/v1/generacion-real → 403
https://www.coordinador.cl/wp-json/wpenapi/v1/real-generation → 403
https://sipub.coordinador.cl/api/v1/recursos/generacion_centrales_tecnologia_real → 404
https://infotecnica.coordinador.cl/api/v1/data/real-operation → 404
https://cen.coordinador.cl/api/v1/generacion → Connection failed
https://energiaabierta.cl/ → Connection failed
https://datos.energiaabierta.cl/ → Connection failed
```

The coordinador.cl website uses WordPress with a WAF that blocks automated requests. The sipub and infotecnica subdomains have API paths but returned 404.

## Integration Notes

- Chile's Atacama solar irradiance makes it one of the most important renewable energy markets globally
- The grid's extreme length (4,300 km) creates unique congestion and transmission constraint data
- datos.gob.cl has a dataset listing for "Generación Eléctrica Real" suggesting open data exists somewhere
- CEN publishes operational reports — the data exists but programmatic access is blocked
- Combined with CSN seismic data and SERNAGEOMIN volcanic data, Chile's infrastructure monitoring is compelling

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Dashboard shows real-time; API not accessible |
| Openness | 0 | 403/404 on all endpoints; energiaabierta.cl unreachable |
| Stability | 2 | Government entity with known open data portal |
| Structure | 1 | WordPress + internal API; unknown format |
| Identifiers | 1 | Unknown |
| Additive Value | 3 | World-class solar; green hydrogen; copper mining demand |
| **Total** | **9/18** | |

## Verdict

⚠️ **Maybe** — The data exists and is published on dashboards, but API access is blocked. Chile has robust open data policies — energiaabierta.cl is a dedicated energy open data portal that was temporarily unreachable. Worth revisiting when the portal is accessible. The Atacama solar and green hydrogen story makes this inherently compelling.
