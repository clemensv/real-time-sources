# Lithuania LHMT Hydro API

**Country/Region**: Lithuania
**Publisher**: Lietuvos hidrometeorologijos tarnyba (LHMT) — Lithuanian Hydrometeorological Service
**API Endpoint**: `https://api.meteo.lt/v1/hydro-stations`
**Documentation**: https://api.meteo.lt (same pattern as their well-documented meteo API)
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Hourly
**Station Count**: ~70 hydrometric stations
**License**: Open data (Lithuanian government open data policy)

## What It Provides

Real-time hourly water level and water temperature observations for Lithuanian rivers, lakes, and the Curonian Lagoon (Kuršių marios). Stations cover major rivers: Nemunas, Neris, Šventoji, Minija, Dubysa, Šešupė, Nevėžis, and the Baltic Sea coast.

## API Details

Three-level REST API with clean JSON responses:

### List all stations
```
GET https://api.meteo.lt/v1/hydro-stations
```
Returns array of station objects with `code`, `name`, `waterBody`, and `coordinates` (lat/lon).

### Station details
```
GET https://api.meteo.lt/v1/hydro-stations/{station-code}
```
Returns station metadata including the water body name and coordinates.

### Observations for a specific date
```
GET https://api.meteo.lt/v1/hydro-stations/{station-code}/observations/measured/{YYYY-MM-DD}
```
Returns hourly observations with:
- `observationTimeUtc` — ISO timestamp in UTC
- `waterLevel` — water level in cm
- `waterTemperature` — water temperature in °C

### Example response (observations)
```json
{
  "station": {
    "code": "nemajunu-vms",
    "name": "Nemajūnų VMS",
    "waterBody": "Nemunas",
    "coordinates": {"latitude": 54.554227, "longitude": 24.072006}
  },
  "observations": [
    {"observationTimeUtc": "2026-04-06 00:00:00", "waterLevel": 71.7, "waterTemperature": 4.2},
    {"observationTimeUtc": "2026-04-06 01:00:00", "waterLevel": 71.8, "waterTemperature": 4.3}
  ]
}
```

## Freshness Assessment

- Hourly updates confirmed — observations appear within the current hour
- Data verified live on 2026-04-06 with current-day readings
- Same API infrastructure as the well-maintained meteo.lt weather API

## Entity Model

- **Station**: code (slug), name, waterBody, coordinates (lat/lon)
- **Observation**: observationTimeUtc, waterLevel (cm), waterTemperature (°C)
- Water bodies are river/lake/lagoon names (Nemunas, Neris, Kuršių marios, etc.)

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 3 | Clean REST, JSON, no auth, consistent slug-based URLs |
| Data Richness | 2 | Water level + temperature only; no discharge or flow data |
| Freshness | 3 | Hourly updates, current-day data available |
| Station Coverage | 2 | ~70 stations covering a small country |
| Documentation | 2 | Follows same pattern as documented meteo API; hydro-specific docs sparse |
| License/Access | 3 | Open, no auth, no rate limiting observed |
| **Total** | **15/18** | |

## Notes

- Station codes are human-readable slugs (e.g., `nemajunu-vms`, `kauno-vms`) — excellent for URL construction
- The API follows the exact same pattern as `api.meteo.lt/v1/stations` (weather stations), suggesting a well-maintained platform
- Baltic state context: Latvia and Estonia lack equivalent public APIs, making this the only Baltic hydro API
- Small but clean — ideal for a lightweight adapter with minimal complexity
- Water body names provide natural grouping (Nemunas basin stations, Neris basin, etc.)
