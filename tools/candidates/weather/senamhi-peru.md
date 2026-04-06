# SENAMHI Peru — Weather & Hydrology

**Country/Region**: Peru (national)
**Publisher**: SENAMHI — Servicio Nacional de Meteorología e Hidrología del Perú
**API Endpoint**: `https://www.senamhi.gob.pe/?p=estaciones` (under maintenance)
**Documentation**: https://www.senamhi.gob.pe/
**Protocol**: Web portal
**Auth**: N/A (under maintenance)
**Data Format**: HTML
**Update Frequency**: Hourly (automatic stations)
**License**: Peruvian government

## What It Provides

SENAMHI operates Peru's national meteorological and hydrological observation network. Peru's geography creates extraordinary climate diversity:

- **Pacific coast**: Hyper-arid desert (Atacama-Sechura) — some stations record zero rainfall for years
- **Andes**: Extreme altitude gradients (0 to 6,768m); glacial monitoring critical for water supply
- **Amazon basin**: Eastern slopes (selva) receive 3,000–5,000 mm/year rainfall
- **El Niño**: Peru is ground zero for ENSO events — coastal warming and extreme rainfall

SENAMHI provides:
- **Meteorological data**: Temperature, humidity, precipitation, wind, radiation from 600+ stations
- **Hydrological data**: River levels and discharge, critical for Lima's water supply (desert city of 10M+ people)
- **Glacial monitoring**: Andean glacier retreat tracking (Cordillera Blanca, Quelccaya ice cap)
- **UV radiation**: Extreme UV levels at altitude (some of the highest on Earth)
- **Agrometeorological**: Crop-critical weather data

## API Details

```
https://www.senamhi.gob.pe/?p=estaciones
```

Response (2026-04-06):
> **Página en mantenimiento**
> Lamentamos las molestias y agradecemos su comprensión

The data portal was under maintenance during testing. Historical access has been through web forms with station-by-station queries (not a bulk API).

## Integration Notes

- Lima's dependence on Andean glacier melt and intermittent Pacific rivers makes hydrology data critical for 10M+ people
- Peru's UV radiation data (at 4,000m+ altitude) would be unique in this repository
- El Niño monitoring is globally significant — Peru is the reference location for ENSO
- SENAMHI data quality is considered good for the region
- No alternative API or open data portal found

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Automatic stations exist; portal under maintenance |
| Openness | 0 | Under maintenance; no API even when operational (web forms) |
| Stability | 1 | Government agency; web infrastructure fragile |
| Structure | 1 | Station-by-station web queries; no bulk API |
| Identifiers | 1 | Station codes known |
| Additive Value | 3 | El Niño ground zero; Andean glaciers; extreme UV; Lima water supply |
| **Total** | **7/18** | |

## Verdict

⏭️ **Skip** — Under maintenance and historically web-form-only (no REST API). Peru's climate data is scientifically invaluable (El Niño, glaciers, extreme UV, desert-to-rainforest gradients), but programmatic access has never been straightforward. Revisit after maintenance period.
