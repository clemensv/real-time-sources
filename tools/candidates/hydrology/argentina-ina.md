# Argentina INA Hydrological Alert System

**Country/Region**: Argentina
**Publisher**: Instituto Nacional del Agua (INA) — National Water Institute
**API Endpoint**: `https://alerta.ina.gob.ar/ina/` (directory-style data access)
**Documentation**: https://alerta.ina.gob.ar/ina/
**Protocol**: HTTP file server / REST-like directory listing
**Auth**: None (public directories)
**Data Format**: Mixed (directory listings, graphics, CSV/data files)
**Update Frequency**: Daily to sub-daily (varies by product)
**Station Count**: Covers major Argentine river basins (Paraná, Paraguay, Uruguay, Río de la Plata)
**License**: Argentine government data

## What It Provides

INA's alert system (Sistema de Alerta Hidrológico) provides hydrological monitoring and forecasting for Argentina's major river systems. The server exposes a directory-based data structure:

- **Hydrology data** (`07-DATOS_HIDRO/`) — water level graphics, time series, scenarios
- **Forecasts** (`08-PRONOSTICOS/`) — hydrological forecasts
- **Daily/weekly reports** — maps and data products
- **Satellite data** (MODIS, LANDSAT, GPM, SMAP) — remote sensing products
- **River-specific data** (Río de la Plata, Uruguay)
- **pydrodelta** — Python-based hydrological modeling tool

## API Details

### Directory listing
```
GET https://alerta.ina.gob.ar/ina/
```
Returns HTML directory listing with timestamped subdirectories:
- `07-DATOS_HIDRO/` — hydrological data products (most recent: 2025-02-26)
- `08-PRONOSTICOS/` — forecasts (most recent: 2026-03-12)
- `42-RIODELAPLATA/` — Río de la Plata specific data
- `52-URUGUAY/` — Uruguay river data
- `pydrodelta/` — modeling code/output

### Hydrology data subdirectories
```
GET https://alerta.ina.gob.ar/ina/07-DATOS_HIDRO/
```
Contains:
- `GRAFICOS_ALTURA/` — water level charts
- `GRAFICOS_ESCENARIOS/` — scenario forecasts
- `GRAFICOS_WEB/` — web-formatted graphics
- `MAPAS_RESERVORIOS/` — reservoir maps (updated 2026-04-05)
- `DAILYSTATS/`, `MONTHLYSTATS/` — statistical summaries
- `series/` — time series data

### No REST API
Despite extensive probing of `/api/`, `/a6/`, and other URL patterns, no structured REST/JSON API was found. The system is primarily a file server with directory listings.

## Freshness Assessment

- Forecast data updated as recently as 2026-03-12
- Reservoir maps updated 2026-04-05
- Daily/weekly map products actively maintained
- Time series and graphics suggest ongoing operational use
- The `pydrodelta` modeling tool shows active development (2026-03-12)

## Entity Model

- **River system**: Paraná, Paraguay, Uruguay, Río de la Plata
- **Station**: gauging stations along major rivers
- **Products**: water level graphics, scenario forecasts, reservoir maps
- **Statistics**: daily stats, monthly stats, multi-year comparisons
- Data is primarily in graphical/map format rather than structured time series

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 1 | Directory listing only; no structured REST API |
| Data Richness | 2 | Rich hydrology products but mostly graphics/maps |
| Freshness | 2 | Active updates but not machine-readable real-time feed |
| Station Coverage | 2 | Major Argentine river basins (Paraná, Plata, Uruguay) |
| Documentation | 1 | No API docs; directory structure is self-documenting |
| License/Access | 2 | Public access, no auth required |
| **Total** | **10/18** | |

## Notes

- INA is Argentina's authoritative hydrological institution
- The file server approach is unusual but functional for data distribution
- `pydrodelta` (Python hydrological model) suggests technical sophistication
- Graphics-heavy output (PNG charts, maps) limits machine-readable integration
- The `DAILYSTATS` and `MONTHLYSTATS` directories may contain CSV/data files (not probed in depth)
- Río de la Plata and Uruguay river data have dedicated sections
- WHOS-Plata (WMO) may provide a more structured API to access Argentine hydrological data
- The `series/` directory likely contains the most useful structured data but was not fully explored
- Integration would likely require parsing specific file formats rather than calling a REST API
