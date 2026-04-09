# WA Ecology Smoke Forecast

- **Country/Region**: US — Washington State
- **Publisher**: Washington State Department of Ecology
- **Endpoint**: `https://gis.ecology.wa.gov/serverext/rest/services/AQ/SmokeForecast/FeatureServer/0`
- **Protocol**: REST (ArcGIS FeatureServer)
- **Auth**: None
- **Format**: JSON, GeoJSON
- **Freshness**: Updated multiple times daily during fire season; daily or less outside fire season
- **Docs**: https://gis.ecology.wa.gov/serverext/rest/services/AQ/SmokeForecast/FeatureServer
- **Score**: 14/18

## Overview

The Washington Department of Ecology provides a machine-learning-enhanced smoke forecast as an ArcGIS FeatureServer. The forecast predicts PM2.5 concentrations from wildfire smoke across Washington State, typically for up to 5 days during fire season (June–October) and 2 days otherwise. This is critically important for Puget Sound outdoor activity planning: wildfire smoke regularly impacts Seattle/Tacoma air quality in August–September, sometimes reaching hazardous levels.

## API Details

**Base URL:** `https://gis.ecology.wa.gov/serverext/rest/services/AQ/SmokeForecast/FeatureServer/0`

**Query Endpoint:**
```
GET /query?where=1=1&outFields=*&f=json
```

**Also available as MapServer:**
```
https://gis.ecology.wa.gov/serverext/rest/services/AQ/SmokeForecast/MapServer
```

**Query Parameters:**
- `where` — SQL filter (e.g., `1=1` for all, or spatial/temporal filter)
- `outFields` — Field selection (`*` for all)
- `f` — Format: `json`, `geojson`, `pjson`
- `geometry` — Spatial filter (envelope, point, polygon)
- `outSR` — Output spatial reference
- `resultRecordCount` — Limit results

**Response Fields Include:**
- Forecast date/time
- Smoke class / PM2.5 concentration range
- Polygon geometry (forecast zones)
- Forecast model metadata

**Additional Ecology AQ Services:**
```
https://gis.ecology.wa.gov/serverext/rest/services/AQ/
```
Contains multiple air quality layers including monitoring stations and current observations.

## Freshness Assessment

Good during fire season (June–October), when forecasts are updated multiple times per day with new model runs. Outside fire season, updates are less frequent. The service is operationally critical during wildfire events when smoke can change rapidly.

## Entity Model

- **Forecast Zone** — Polygon geometry covering a geographic area
- **Forecast** — Predicted PM2.5 concentration class, valid date/time
- **Model Run** — Metadata about the forecast model and input data

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Multiple daily updates during fire season; less outside |
| Openness | 3 | No auth, state government data |
| Stability | 2 | State agency GIS service; ArcGIS infrastructure is reliable |
| Structure | 2 | ArcGIS JSON with geometry; requires polygon handling |
| Identifiers | 2 | Forecast zone IDs from geometry; no simple string keys |
| Additive Value | 3 | Unique smoke forecast data critical for PNW outdoor planning |
| **Total** | **14/18** | |

## Notes

- Wildfire smoke is arguably the #1 outdoor activity disruptor in the Puget Sound area during summer/fall. The "Smoketember" phenomenon (August–September smoke events) can persist for weeks.
- Complements EPA AirNow (current conditions) with forecast capability — knowing when smoke will arrive or clear is more actionable than current readings alone.
- ArcGIS FeatureServer protocol is well-established and many libraries support it.
- Polygon-based forecasts need spatial intersection to determine impact at a specific location.
- The Washington Smoke Blog (wasmoke.blogspot.com) provides human-readable context but no machine API.
- Consider pairing with NASA FIRMS (active fire detections) for a complete smoke picture.
