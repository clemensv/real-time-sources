# UTE Uruguay — Energy Grid

**Country/Region**: Uruguay (national)
**Publisher**: UTE — Administración Nacional de Usinas y Trasmisiones Eléctricas
**API Endpoint**: Various `https://www.ute.com.uy/` (404), `https://apps.ute.com.uy/` (404)
**Documentation**: https://www.ute.com.uy/
**Protocol**: Unknown
**Auth**: Unknown
**Data Format**: Unknown
**Update Frequency**: Real-time (dashboard)
**License**: Uruguayan state enterprise

## What It Provides

Uruguay is one of the world's most remarkable renewable energy success stories. The country generates **~97% of its electricity from renewables**, primarily:

- **Wind**: ~40% (Uruguay went from 0% to 40% wind in a decade, 2008–2018)
- **Hydro**: ~30% (Salto Grande binational with Argentina, Rincón del Bonete, Baygorria, Palmar)
- **Biomass/Biogas**: ~15% (agricultural residues, forestry)
- **Solar**: ~5% and growing
- **Thermal**: ~3% (backup only, used during droughts)

UTE is both the generation operator and the transmission/distribution utility — a vertically integrated state enterprise.

## API Details

No working API endpoints found:

```
https://www.ute.com.uy/energia-en-tiempo-real → 404
https://www.ute.com.uy/SgesWeb/api/Demanda/Actual → 404
https://apps.ute.com.uy/SgesWeb/api/Demanda/Actual → 404
https://apidatos.ute.com.uy/api/v1/generacion → Connection failed
https://opendata.ute.com.uy/api/3/action/package_list → Connection failed
```

UTE has a known open data initiative (datos abiertos) but endpoints were unreachable during testing.

## Integration Notes

- Uruguay's 97% renewable grid makes it a unique case study for the energy transition
- The country's rapid wind buildout is a model studied worldwide
- Salto Grande (binational with Argentina, 1,890 MW) generates significant cross-border flows
- Uruguay exports electricity to Argentina and Brazil during surplus periods
- A working UTE API would be exceptionally valuable for energy transition researchers
- Open data policies in Uruguay (AGESIC — the government's digital agency) are strong

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Dashboard shows real-time but no API |
| Openness | 0 | All endpoints returned 404 or connection failed |
| Stability | 1 | State enterprise; known open data initiative |
| Structure | 0 | Cannot assess |
| Identifiers | 0 | Cannot assess |
| Additive Value | 3 | 97% renewable — one of the world's greenest grids |
| **Total** | **5/18** | |

## Verdict

⏭️ **Skip for now** — No working endpoints. Uruguay's grid data is uniquely valuable for energy transition analysis (97% renewable!). The open data initiative exists but wasn't accessible. Revisit — AGESIC is pushing open data across Uruguayan government agencies.
