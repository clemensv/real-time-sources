# SIATA Medellín — Environmental Early Warning System

**Country/Region**: Colombia (Valle de Aburrá / Medellín metropolitan area)
**Publisher**: SIATA — Sistema de Alerta Temprana de Medellín y el Valle de Aburrá
**API Endpoint**: `https://siata.gov.co/` (no API found)
**Documentation**: https://siata.gov.co/siata_nuevo/
**Protocol**: Unknown
**Auth**: Unknown
**Data Format**: Unknown
**Update Frequency**: Minute-by-minute (per website description)
**License**: Área Metropolitana del Valle de Aburrá + Alcaldía de Medellín

## What It Provides

SIATA is one of the most sophisticated urban environmental monitoring systems in Latin America. It provides minute-by-minute hydrometeorological monitoring for Medellín and the Valle de Aburrá — a narrow Andean valley at 1,500m elevation where air quality is a critical issue.

Monitored parameters include:
- **Weather**: Temperature, humidity, pressure, wind, precipitation (radar + rain gauges)
- **Air quality**: PM2.5, PM10, ozone, NO2 — Medellín's valley topography traps pollutants
- **Hydrology**: River levels, flood early warning (flash flood risk in steep Andean valleys)
- **Lightning**: Real-time lightning detection
- **Landslides**: Soil moisture monitoring for landslide risk

SIATA was established with support from EPM (Empresas Públicas de Medellín) and ISAGEN (hydroelectric company).

## API Details

No working API endpoints found during testing. The website (`siata.gov.co/siata_nuevo/`) loads a JavaScript SPA with map layers. Attempted API paths returned 404.

Historical data may be available by request (the website mentions a data download process via email to contacto@siata.gov.co).

## Integration Notes

- Medellín's air quality crisis (valley inversion trapping pollutants) makes this data socially critical
- The system combines radar, rain gauges, air quality sensors, and soil moisture — extremely comprehensive
- Flash flood risk in the Valle de Aburrá is a life-safety concern (steep terrain + intense tropical rainfall)
- SIATA is a model for urban environmental monitoring in developing countries
- The combination of air quality + hydrology + weather in one system is unique

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Minute-by-minute per documentation, but no API |
| Openness | 0 | No API found; data-by-request model |
| Stability | 2 | Well-funded multi-agency system |
| Structure | 0 | Cannot assess |
| Identifiers | 0 | Cannot assess |
| Additive Value | 3 | Unique comprehensive urban monitoring system; Andean valley air quality |
| **Total** | **7/18** | |

## Verdict

⏭️ **Skip for now** — No programmatic access despite the system being clearly sophisticated. The SPA loads data dynamically — reverse engineering the JavaScript to find API endpoints could yield results. The minute-by-minute data and comprehensive sensor network make this worth revisiting.
