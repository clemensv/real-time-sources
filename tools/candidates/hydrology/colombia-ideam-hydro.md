# Colombia IDEAM Hydrology — via datos.gov.co Socrata API

**Country/Region**: Colombia (national)
**Publisher**: IDEAM — Instituto de Hidrología, Meteorología y Estudios Ambientales
**API Endpoint**: `https://www.datos.gov.co/resource/s54a-sgyg.json`
**Documentation**: https://www.datos.gov.co/ (Socrata Open Data API — SODA)
**Protocol**: REST (Socrata SODA 2.1)
**Auth**: None (rate-limited without app token)
**Data Format**: JSON, CSV, GeoJSON
**Update Frequency**: Near-real-time (~minutes, data through 2026-04-05 23:59 confirmed)
**License**: Colombian open data (datos.gov.co)

## What It Provides

IDEAM operates Colombia's national hydrometeorological network. This Socrata dataset (`s54a-sgyg`) contains automatic station telemetry data including precipitation readings from stations across the country.

Colombia's hydrology is extraordinarily diverse:
- **Pacific coast**: Among the wettest places on Earth (Chocó receives 8,000+ mm/year)
- **Amazon basin**: Southern Colombia drains into the Amazon
- **Orinoco basin**: Eastern plains drain to Venezuela
- **Magdalena-Cauca**: Main Andean river system, critical for 70%+ of population
- **Caribbean coast**: Flooding from Sierra Nevada de Santa Marta

## API Details

Standard Socrata SODA 2.1 API:

### Precipitation Data (most recent)
```
GET https://www.datos.gov.co/resource/s54a-sgyg.json?$limit=3&$order=fechaobservacion DESC
```

Response (verified live 2026-04-06):

```json
[
  {
    "codigoestacion": "2120000131",
    "codigosensor": "0240",
    "fechaobservacion": "2026-04-05T23:59:00.000",
    "valorobservado": "0",
    "nombreestacion": "COL. ANTONIO GARCIA",
    "departamento": "BOGOTÁ",
    "municipio": "BOGOTÁ D.C",
    "zonahidrografica": "ALTO MAGDALENA",
    "latitud": "4.545",
    "longitud": "-74.13944",
    "descripcionsensor": "PRECIPITACIÓN",
    "unidadmedida": "mm"
  }
]
```

### Atmospheric Pressure / Weather Data
```
GET https://www.datos.gov.co/resource/62tk-nxj5.json?$limit=3&$order=fechaobservacion DESC
```

Returns pressure data with same near-real-time timestamps.

### Temperature Data
```
GET https://www.datos.gov.co/resource/sbwg-7ju4.json?$limit=3
```

Air temperature (2m) from automatic stations.

### Socrata Query Features

Full SoQL query language:
- `$where=fechaobservacion > '2026-04-05T00:00:00'` — temporal filtering
- `$where=departamento='BOGOTÁ'` — geographic filtering
- `$select=codigoestacion,fechaobservacion,valorobservado` — field selection
- `$group=departamento` — aggregation
- `$limit=1000&$offset=0` — pagination

## Entity Model

- **codigoestacion**: Station code (unique identifier)
- **codigosensor**: Sensor type code
- **fechaobservacion**: Observation timestamp (ISO 8601)
- **valorobservado**: Observed value (string — needs numeric parsing)
- **nombreestacion**: Station name (Spanish)
- **departamento**: Colombian department (state equivalent)
- **municipio**: Municipality
- **zonahidrografica**: Hydrographic zone
- **latitud / longitud**: Decimal degrees
- **descripcionsensor**: Sensor description (Spanish)
- **unidadmedida**: Unit of measurement

## Freshness Assessment

Data confirmed through 2026-04-05 23:59 (approximately 22 hours before query). This is near-real-time automatic telemetry data — stations report at sub-hourly intervals. The Socrata platform serves data with minimal latency from IDEAM's upload schedule.

## Integration Notes

- Socrata SODA is a well-known, well-documented API standard used by hundreds of open data portals worldwide
- Three separate datasets provide precipitation (`s54a-sgyg`), atmospheric pressure (`62tk-nxj5`), and temperature (`sbwg-7ju4`)
- Rate limits: 1,000 requests/hour without app token; higher with free registration
- Field names are in Spanish; a mapping layer is needed
- `valorobservado` is a string field — needs numeric parsing and validation
- Poll interval recommendation: 15–30 minutes
- CloudEvents mapping: batch of station readings per poll cycle, or one CloudEvent per station observation

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Near-real-time automatic station data |
| Openness | 3 | No auth required; Socrata standard; Colombian open data |
| Stability | 2 | datos.gov.co is stable but dataset resource IDs could change |
| Structure | 2 | Clean JSON via Socrata; field names in Spanish; values as strings |
| Identifiers | 2 | Station codes are stable; sensor codes need mapping |
| Additive Value | 3 | Only source for Colombia hydrology; Amazon/Orinoco/Magdalena basins |
| **Total** | **15/18** | |

## Verdict

✅ **Build** — This is a strong candidate. Near-real-time hydrometeorological data from Colombia via a well-documented Socrata API with no authentication required. The three datasets (precipitation, pressure, temperature) provide comprehensive coverage of Colombia's diverse hydrological regions. Socrata's SoQL query language enables efficient temporal polling. The Socrata adapter pattern is highly reusable across hundreds of open data portals worldwide.
