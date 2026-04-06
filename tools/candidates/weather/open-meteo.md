# Open-Meteo — Open-Source Weather API

**Country/Region**: Global (aggregates multiple national model outputs)
**Publisher**: Open-Meteo (Patrick Zippenfenig, open-source project hosted in Switzerland)
**API Endpoint**: `https://api.open-meteo.com/v1/forecast`
**Documentation**: https://open-meteo.com/en/docs
**Protocol**: REST API
**Auth**: None for non-commercial use (API key for commercial use at >10,000 req/day)
**Data Format**: JSON
**Update Frequency**: Hourly updates (model-dependent), 15-minute resolution available
**License**: CC BY 4.0 for non-commercial; commercial license available

## What It Provides

Open-Meteo is an open-source weather API that aggregates and serves data from multiple national weather models worldwide:

- **Current weather**: Real-time current conditions from a "best match" of models.
- **Hourly forecasts**: Up to 16 days ahead. Parameters: temperature, humidity, dew point, apparent temperature, precipitation, rain, snow, weather code (WMO standard), pressure, cloud cover, visibility, wind speed/direction/gusts, UV index, solar radiation, soil temperature/moisture, and many more.
- **Daily forecasts**: Min/max temperature, sunrise/sunset, precipitation sum, wind max, UV max, etc.
- **Historical weather**: Reanalysis data going back decades.
- **Air quality**: PM2.5, PM10, ozone, NO₂, SO₂, CO, dust, pollen.
- **Marine/wave forecasts**: Wave height, period, direction.
- **Climate projections**: CMIP6 climate model data.
- **Flood forecasts**: GloFAS river discharge forecasts.
- **Ensemble forecasts**: Multiple ensemble models.

Models include: ECMWF IFS/AIFS, DWD ICON, NOAA GFS/HRRR, Météo-France ARPEGE/AROME, JMA, UKMO, Environment Canada, BOM ACCESS, and more.

## API Details

Simple REST API with query parameters:
```
https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true
```

Probed response:
```json
{
  "latitude": 52.52,
  "longitude": 13.42,
  "current_weather": {
    "time": "2026-04-06T10:15",
    "temperature": 10.5,
    "windspeed": 23.6,
    "winddirection": 291,
    "is_day": 1,
    "weathercode": 2
  }
}
```

Key parameters:
- `latitude`, `longitude`: Location (required)
- `hourly`: Comma-separated list of hourly variables
- `daily`: Comma-separated list of daily variables
- `current_weather`: Boolean for current conditions
- `timezone`: Timezone for response
- `models`: Select specific weather model(s)
- `forecast_days`: Number of forecast days (1–16)

No pagination. Responses are compact, array-based JSON.

## Freshness Assessment

- Current weather updates approximately every 15 minutes.
- Forecast data updates with each model run (varies by model, but typically 4–6× daily).
- The probed endpoint returned data timestamped within the last 15 minutes.
- Latency from model run to API availability is model-dependent (1–3 hours typically).

## Entity Model

- **Location**: Arbitrary lat/lon point (snaps to nearest grid cell)
- **Current weather**: Single most-recent observation/analysis
- **Time series**: Arrays of hourly or daily values with associated time array
- **Model**: Selectable underlying NWP model for the forecast

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15-minute current weather updates, frequent forecast refreshes |
| Openness | 3 | No auth for non-commercial, CC BY 4.0, open-source |
| Stability | 2 | Community-driven project, not a government agency |
| Structure | 3 | Extremely clean JSON API, simple parameters, no auth hassle |
| Identifiers | 1 | Lat/lon only, no station concept, no stable entity IDs |
| Additive Value | 3 | Global coverage, multi-model access, one-stop shop |
| **Total** | **15/18** | |

## Notes

- Open-Meteo is the most developer-friendly weather API available — dead simple, no auth, clean JSON.
- However, it is a derived/aggregated source — the underlying data comes from national met services.
- For real-time-sources research, the primary national sources are preferred, but Open-Meteo is valuable as a reference integration pattern.
- The project is open-source (GitHub) and can be self-hosted.
- WMO weather codes in responses follow an international standard.
- The `models` parameter allows selecting specific national models, giving fine control over data provenance.
- Commercial use above 10,000 requests/day requires a paid API key.
- No push/streaming capability — polling only.
