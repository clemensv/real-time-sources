# IDEAM Colombia — Hydrological Stations via datos.gov.co

**Country/Region**: Colombia (national)
**Publisher**: IDEAM via datos.gov.co (Socrata)
**API Endpoint**: Multiple datasets on `https://www.datos.gov.co/resource/`
**Documentation**: https://www.datos.gov.co/
**Protocol**: REST (Socrata SODA 2.1)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Near-real-time
**License**: Colombian open data

## Overview — datos.gov.co IDEAM Dataset Inventory

This document catalogs all confirmed IDEAM datasets on datos.gov.co with near-real-time data.

### Confirmed Working Datasets

| Resource ID | Parameter | Most Recent Data | Verified |
|-------------|-----------|-----------------|----------|
| `s54a-sgyg` | Precipitation (mm) | 2026-04-05 23:59 | ✅ |
| `62tk-nxj5` | Atmospheric pressure (hPA) | 2026-04-05 23:58 | ✅ |
| `sbwg-7ju4` | Air temperature 2m (°C) | Historical | ✅ (data stale) |

The precipitation and pressure datasets showed data within 24 hours of the query. Temperature data appeared historical during testing.

### Common Schema

All datasets share the same column structure:
- `codigoestacion` — Station code
- `codigosensor` — Sensor type code
- `fechaobservacion` — ISO 8601 timestamp
- `valorobservado` — Observed value (string)
- `nombreestacion` — Station name
- `departamento` — Department (state)
- `municipio` — Municipality
- `zonahidrografica` — Hydrographic zone
- `latitud` / `longitud` — Coordinates
- `descripcionsensor` — Sensor description
- `unidadmedida` — Unit of measurement

### Hydrographic Zones Represented

Colombia's water resources span five major basins:
- **Alto Magdalena** (Bogotá, upper Magdalena valley)
- **Cauca** (Western Andes, coffee region)
- **Sinú** (Caribbean coast)
- **Caquetá** (Amazon basin)
- **Atrato-Darién** (Pacific/Caribbean, Chocó — wettest region on Earth)

### SoQL Query Examples

```
# Recent precipitation in Bogotá
?$where=departamento='BOGOTÁ' AND fechaobservacion>'2026-04-05'
&$order=fechaobservacion DESC&$limit=100

# All stations with data in the Amazon basin
?$where=zonahidrografica='CAQUETÁ'&$select=DISTINCT codigoestacion,nombreestacion

# Temporal aggregation
?$select=date_trunc_ymd(fechaobservacion) as day,avg(valorobservado) as avg_value
&$group=day&$order=day DESC
```

## Integration Notes

- A single Socrata adapter handles all IDEAM datasets — just change the resource ID
- The `zonahidrografica` field provides built-in basin classification
- Colombia has ~2,600 hydrometeorological stations, but not all report to these datasets
- Socrata rate limits: 1,000 requests/hour without app token
- The common schema means one CloudEvents type definition covers all three datasets

## Feasibility Rating

See individual documents:
- [colombia-ideam-hydro.md](../hydrology/colombia-ideam-hydro.md) — 15/18
- [colombia-ideam-weather.md](../weather/colombia-ideam-weather.md) — 14/18

Combined approach: **15/18** (single adapter, multiple resource IDs)
