# IGEPN Ecuador — Instituto Geofísico de la Escuela Politécnica Nacional

**Country/Region**: Ecuador (national)
**Publisher**: Instituto Geofísico, Escuela Politécnica Nacional (IG-EPN)
**API Endpoint**: `https://www.igepn.edu.ec/` (403 on all API paths tested)
**Documentation**: https://www.igepn.edu.ec/
**Protocol**: Unknown (website blocked for automated access)
**Auth**: N/A (403 on all attempts)
**Data Format**: Unknown
**Update Frequency**: Near-real-time (website presumably updates)
**License**: Ecuadorian government/university entity

## What It Provides

IGEPN is Ecuador's national geophysical institute, responsible for monitoring earthquakes and volcanoes. Ecuador is uniquely positioned:

- **Subduction zone**: Nazca plate diving under the South American plate along the coast
- **Active volcanoes**: Cotopaxi (near Quito), Tungurahua, Reventador, Sangay — among the most active in the Americas
- **Galápagos Islands**: Volcanic hotspot with unique monitoring requirements (Sierra Negra, Wolf, Fernandina)

Ecuador detects hundreds of earthquakes monthly and monitors ~80 potentially active volcanoes.

## API Details

All tested endpoints returned 403 Forbidden:

```
GET https://www.igepn.edu.ec/sismos/sismos-ultimo-sismo → 403
GET https://www.igepn.edu.ec/api/ultimo-sismo → 403
GET https://www.igepn.edu.ec/servicios/api/v1/earthquakes/last → 403
GET https://www.igepn.edu.ec/eq/eventos → 403
GET https://cdsb.igepn.edu.ec/eq/events → Connection failed
```

The website appears to use Cloudflare or similar WAF protection that blocks non-browser requests.

## Freshness Assessment

Unable to assess — all endpoints blocked.

## Integration Notes

- IGEPN is a critical source for Galápagos and Andean volcanic monitoring
- Ecuador's volcanoes threaten Quito (population 2.8 million) directly
- Larger events (M4+) are available via USGS and EMSC
- Volcanic activity is partially captured by MIROVA satellite thermal monitoring
- An FDSN endpoint may exist but was not found during testing

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Likely near-real-time but unverifiable |
| Openness | 0 | 403 on all endpoints |
| Stability | 1 | Government institute, but no API access |
| Structure | 0 | Cannot assess |
| Identifiers | 0 | Cannot assess |
| Additive Value | 3 | Galápagos! Unique volcanic hotspot monitoring |
| **Total** | **5/18** | |

## Verdict

⏭️ **Skip** — All endpoints blocked with 403. The scientific value is exceptional (Galápagos volcanoes alone justify monitoring), but there's no programmatic access path. Larger events are available via USGS/EMSC. Revisit if IGEPN opens an API or FDSN node.
