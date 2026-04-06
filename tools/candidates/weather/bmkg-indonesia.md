# BMKG Open Data — Indonesia

**Country/Region**: Indonesia
**Publisher**: BMKG (Badan Meteorologi, Klimatologi, dan Geofisika — Indonesian Agency for Meteorology, Climatology, and Geophysics)
**API Endpoint**: `https://api.bmkg.go.id/publik/prakiraan-cuaca`
**Documentation**: https://data.bmkg.go.id/
**Protocol**: REST (JSON)
**Auth**: None (public endpoints, no API key required)
**Data Format**: JSON
**Update Frequency**: 3-hourly forecast timesteps, updated per model run
**License**: Indonesian Open Government Data

## What It Provides

BMKG provides weather forecast data down to village (kelurahan/desa) level for the entire Indonesian archipelago — one of the world's largest countries by area:

- **Weather Forecasts** (`prakiraan-cuaca`): 3-hourly forecasts per village/kelurahan. Parameters include:
  - Temperature (°C)
  - Total cloud cover (%)
  - Precipitation (mm)
  - Weather code and description (bilingual Indonesian/English: "Cerah" / "Sunny", "Berawan" / "Mostly Cloudy", etc.)
  - Wind direction (degrees and compass), wind speed (km/h)
  - Relative humidity (%)
  - Visibility (m) with text classification
  - Analysis date

- **Earthquake Data** (via data.bmkg.go.id): Real-time seismic events — BMKG is Indonesia's earthquake monitoring agency.

- **Early Weather Warnings** (nowcast): District-level (kecamatan) early warnings.

## API Details

The forecast API uses Indonesia's 4-level administrative division codes:
```
GET https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=31.72.02.1003
```

Administrative code hierarchy:
- `adm1`: Province (e.g., 31 = DKI Jakarta)
- `adm2`: Regency/City (e.g., 31.72 = North Jakarta)
- `adm3`: District/Kecamatan
- `adm4`: Village/Kelurahan

Response includes full location metadata (province, city, district, village, lat/lon, timezone) and nested arrays of 3-hourly forecast timesteps grouped by day. Each timestep includes UTC and local datetime, weather icon URL, and bilingual descriptions.

No authentication required for public forecast endpoints.

## Freshness Assessment

- Forecast timesteps at 3-hour intervals (00, 03, 06, 09, 12, 15, 18, 21 UTC).
- Probed live — received forecasts with current `analysis_date` (2026-04-06T00:00:00).
- Data updates with each model run.
- Multi-day forecasts (3+ days) available per request.

## Entity Model

- **Location**: Hierarchical administrative codes (adm1–adm4) + lat/lon + timezone.
- **Forecast Timestep**: datetime (UTC + local) + all weather parameters.
- **Weather Code**: Numeric code (1=Sunny, 2=Partly Cloudy, 3=Mostly Cloudy, etc.) with bilingual descriptions.
- **Time Index**: Sequential hour index within the forecast.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 3-hourly forecast data; observations not exposed through this API |
| Openness | 3 | No auth, public endpoint, bilingual output |
| Stability | 2 | Government agency, but API infrastructure is relatively new |
| Structure | 3 | Clean JSON, hierarchical location codes, bilingual, well-structured |
| Identifiers | 3 | Stable administrative division codes (adm1–adm4), weather codes |
| Additive Value | 3 | Covers 17,000+ islands, 270M people, critical tropical/maritime region |
| **Total** | **16/18** | |

## Notes

- Indonesia's archipelago spans 5,000 km east-west, covering three time zones — coverage from this single API is geographically enormous.
- The village-level (kelurahan) forecast granularity is remarkable — most met services only offer city-level forecasts.
- Bilingual output (Indonesian + English) makes integration straightforward for international users.
- BMKG is also the national earthquake and tsunami warning agency — earthquake data is a valuable bonus.
- The administrative code system (adm1–adm4) aligns with Indonesia's BPS statistical classification, making cross-referencing with demographic data possible.
- Weather icon SVG URLs are included in responses — useful for direct rendering.
- The older XML-based endpoint (`data.bmkg.go.id/DataMKG/`) appears to have been superseded by this newer JSON API.
