# Argentina SMN (Servicio Meteorológico Nacional)

**Country/Region**: Argentina
**Publisher**: SMN (Servicio Meteorológico Nacional)
**API Endpoint**: `https://ws.smn.gob.ar/map_items/weather`
**Documentation**: Minimal — endpoints discoverable through the SMN website
**Protocol**: REST (JSON)
**Auth**: None (public endpoints)
**Data Format**: JSON
**Update Frequency**: Real-time observations (synoptic schedule)
**License**: Argentine public data

## What It Provides

Argentina's national meteorological service exposes real-time weather observations through a JSON API that powers their web map interface:

- **Current Weather Observations** (`/map_items/weather`): Real-time synoptic observations from weather stations across Argentina and Antarctic bases. Parameters include:
  - Temperature (°C)
  - Relative humidity (%)
  - Atmospheric pressure (hPa)
  - Wind speed (km/h) and direction (compass text in Spanish)
  - Visibility (km)
  - Weather description (Spanish — e.g., "Cubierto con neblina", "Parcialmente nublado")
  - Soil temperature (where available)
  - Weather code (numeric, corresponding to WMO weather codes)

- **Station Network Coverage**:
  - Major cities and airports across Argentina
  - Patagonian stations (Ushuaia, Río Grande)
  - Antarctic bases (Base Marambio, Base Belgrano II)
  - Malvinas/Falkland Islands (Puerto Argentino)
  - Mountain stations (Chapelco, Villa La Angostura)

## API Details

Direct JSON endpoint — fetches all station observations in a single request:
```
GET https://ws.smn.gob.ar/map_items/weather
```

Response is a JSON array of station objects, each containing:
- Station metadata: `_id`, `lid`, `fid`, `int_number` (WMO station number), `name`, `province`, `lat`/`lon`
- Weather data: nested `weather` object with all parameters
- `updated`: Unix timestamp of observation
- `dist` and `zoom`: UI rendering hints

Station identifiers include both internal IDs (`lid`, `fid`) and international WMO station numbers (`int_number`, e.g., 87544 for Pehuajó).

No authentication. No pagination — the entire station set is returned in one response.

## Freshness Assessment

- Observations follow the standard WMO synoptic schedule (every 3 or 6 hours at main stations).
- Probed live — received data with `updated` timestamps.
- Data appears to be the latest available synoptic report per station.
- Some stations may have older timestamps if they report less frequently.

## Entity Model

- **Station**: Internal ID (`lid`/`fid`) + WMO number (`int_number`) + name + province + lat/lon.
- **Observation**: Temperature, humidity, pressure, wind, visibility, weather description + code.
- **Timestamp**: Unix epoch in `updated` field.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Synoptic schedule (3–6 hourly), not minute-level |
| Openness | 3 | No auth, direct JSON endpoint |
| Stability | 2 | Government service, but API is undocumented and appears to be a web backend |
| Structure | 2 | JSON but inconsistent — some fields null, descriptions in Spanish only |
| Identifiers | 3 | WMO station numbers (international standard), internal IDs |
| Additive Value | 3 | Argentina + Patagonia + Antarctica; unique Southern Hemisphere coverage |
| **Total** | **15/18** | |

## Notes

- The geographic coverage is exceptional — from subtropical Salta (latitude -24°) to Antarctic Base Belgrano II (latitude -77°), spanning 53 degrees of latitude.
- Antarctic station data (Marambio, Belgrano II) is especially rare and valuable in open data.
- The API appears to be the backend for SMN's web map — undocumented but functional. Stability risk: could change without notice.
- Weather descriptions are in Spanish only (no English translation in the API).
- WMO station numbers enable cross-referencing with GTS data and international databases.
- The `forecast` field exists in the schema but was null in probed responses — forecasts may be available through a separate endpoint.
- Argentina's diverse geography (tropical, pampas, mountains, desert, glacial, Antarctic) makes this data scientifically interesting.
