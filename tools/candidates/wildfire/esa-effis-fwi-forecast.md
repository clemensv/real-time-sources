# EFFIS Fire Weather Index (FWI) Forecast

- **Country/Region**: Europe, global (GWIS)
- **Endpoint**: https://maps.effis.emergency.copernicus.eu/effis?service=WMS&layers=ecmwf.fwi
- **Protocol**: WMS (PNG tiles), WCS (raster data)
- **Auth**: None
- **Format**: GeoTIFF (via WCS)
- **Freshness**: Daily (1-day forecast from ECMWF)
- **Score**: 13/18

## Overview

EFFIS publishes **Fire Weather Index (FWI)** forecasts derived from ECMWF meteorological models:

- **FWI** — composite fire danger index (0–100+)
- **ISI** — Initial Spread Index (ignition potential)
- **BUI** — Build-Up Index (fuel availability)
- **FFMC** — Fine Fuel Moisture Code (surface fuel)
- **DMC** — Duff Moisture Code (organic layer)
- **DC** — Drought Code (deep fuel layers)
- **1-day and 10-day forecasts**, daily updates
- **8 km resolution** (ECMWF grid)

FWI is the European standard for fire danger rating (Canadian Forest Service system).

## Verdict

✅ **Build** — FWI forecast data is available via **WCS** (Web Coverage Service) as GeoTIFF.
Can poll daily and extract country/region-level FWI statistics (mean, max) or specific
fire-prone zones.

**Event model**:
- Subject: `fire/weather/{country}/{region}` or `fire/weather/{grid_cell}`
- Payload: daily FWI values (FWI, ISI, BUI, FFMC, DMC, DC), anomaly vs. climatology
- Type: `eu.copernicus.effis.fwi.forecast`

| Criterion | Score |
|-----------|-------|
| Value | 3 (fire danger forecasting, prevention) |
| Freshness | 2 (daily forecast updates) |
| Openness | 3 (WCS publicly accessible, no auth) |
| Schema | 2 (GeoTIFF raster, well-documented indices) |
| Machine-readability | 2 (WCS protocol) |
| Repo fit | 1 (grid data, extract regions manually) |

**Total: 13/18** — ✅ **Build**. Extract FWI for pre-selected European fire-prone regions
(Iberia, Mediterranean, Balkans) and emit daily forecast events. Complements EFFIS active fires.
