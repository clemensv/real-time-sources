# Colombia IDEAM Weather — via datos.gov.co Socrata API

**Country/Region**: Colombia (national)
**Publisher**: IDEAM — Instituto de Hidrología, Meteorología y Estudios Ambientales
**API Endpoint**: `https://www.datos.gov.co/resource/62tk-nxj5.json` (pressure), `https://www.datos.gov.co/resource/sbwg-7ju4.json` (temperature)
**Documentation**: https://www.datos.gov.co/
**Protocol**: REST (Socrata SODA 2.1)
**Auth**: None (rate-limited without app token)
**Data Format**: JSON, CSV
**Update Frequency**: Near-real-time (~minutes latency)
**License**: Colombian open data

## What It Provides

IDEAM automatic weather stations across Colombia reporting atmospheric pressure and air temperature via the national open data portal (datos.gov.co). Colombia's weather is shaped by its equatorial position, Andean topography, and influence from both Pacific and Caribbean oceans.

### Atmospheric Pressure Dataset (62tk-nxj5)

```
GET https://www.datos.gov.co/resource/62tk-nxj5.json?$limit=3&$order=fechaobservacion DESC
```

Response (verified 2026-04-06):
```json
[
  {
    "codigoestacion": "0026125061",
    "codigosensor": "0258",
    "fechaobservacion": "2026-04-05T23:58:00.000",
    "valorobservado": "879.3",
    "nombreestacion": "AEROPUERTO EL EDEN -",
    "departamento": "QUINDÍO",
    "municipio": "ARMENIA",
    "zonahidrografica": "CAUCA",
    "latitud": "4.454722222",
    "longitud": "-75.76638889",
    "descripcionsensor": "GPRS - PRESIÓN ATMOSFÉRICA",
    "unidadmedida": "hPA"
  }
]
```

### Temperature Dataset (sbwg-7ju4)

```
GET https://www.datos.gov.co/resource/sbwg-7ju4.json?$limit=3
```

Returns air temperature at 2m height from automatic stations.

## Integration Notes

- Same Socrata platform and query patterns as the hydrology dataset (see colombia-ideam-hydro.md)
- Airport stations (AEROPUERTO...) provide WMO-comparable data quality
- Colombia has ~2,600 hydrometeorological stations — coverage is extensive
- Pressure values show altitude effects clearly (Armenia at 879 hPa = ~1,500m elevation)
- A single Socrata adapter handles all IDEAM datasets with different resource IDs
- This source complements the precipitation data in the hydrology dataset

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Near-real-time (~minutes) |
| Openness | 3 | No auth, Socrata standard |
| Stability | 2 | datos.gov.co stable; resource IDs may change |
| Structure | 2 | Clean JSON; Spanish field names; strings for values |
| Identifiers | 2 | Station codes stable |
| Additive Value | 2 | Complements hydrology; tropical equatorial weather station network |
| **Total** | **14/18** | |

## Verdict

✅ **Build** (bundle with hydrology) — Same adapter, different resource IDs. Build as part of a generic datos.gov.co/Socrata IDEAM integration. The atmospheric pressure and temperature data complement the precipitation dataset.
