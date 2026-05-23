# Qatar Weather Forecast (Open-Meteo)

- **Country/Region**: Qatar (Doha)
- **Endpoint**: `https://api.open-meteo.com/v1/forecast?latitude=25.28&longitude=51.52&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weathercode,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&hourly=temperature_2m,precipitation,weathercode,wind_speed_10m&timezone=Asia/Qatar`
- **Protocol**: REST / JSON
- **Auth**: None
- **Format**: JSON
- **Freshness**: Current block updates every ~15 minutes; hourly forecasts updated hourly
- **Docs**: https://open-meteo.com/en/docs
- **Score**: 14/18

## Overview

Open-Meteo provides free access to global numerical weather prediction (NWP) models for any
location worldwide. For Qatar, this provides:
- **Current conditions** (15-minute updates): temperature, humidity, wind, pressure, precipitation
- **Hourly forecasts** (7 days): temperature, precipitation, wind, weather code
- **Daily forecasts** (16 days): max/min temperature, sunrise/sunset, precipitation sum

The service aggregates multiple NWP models (ECMWF IFS, GFS, ICON, MeteoFrance) and selects
the best-performing model for each region. For the Middle East, ECMWF IFS typically provides
the highest accuracy.

**Qatar climate context**:
- **Summer** (May-Sep): Extreme heat (40-50°C), high humidity (50-90%), minimal rainfall
- **Winter** (Dec-Feb): Mild (15-25°C), occasional rain, lower humidity
- **Shamal winds**: Strong north/northwest winds in spring and summer, bringing dust
- **Precipitation**: <80 mm/year, concentrated in winter; summer is bone-dry

Qatar Meteorological Department (qweather.gov.qa) is the official national weather service,
but their website and APIs are **not publicly accessible** (DNS/TLS failures during discovery).
Open-Meteo fills this gap with free, real-time weather data for Qatar.

## Endpoint Analysis

**Live test successful** — API returned current weather for Doha:

```json
{
  "latitude": 25.28,
  "longitude": 51.52,
  "generationtime_ms": 0.234,
  "utc_offset_seconds": 10800,
  "timezone": "Asia/Qatar",
  "timezone_abbreviation": "AST",
  "elevation": 10.0,
  "current_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "relative_humidity_2m": "%",
    "apparent_temperature": "°C",
    "precipitation": "mm",
    "rain": "mm",
    "weathercode": "wmo code",
    "surface_pressure": "hPa",
    "wind_speed_10m": "km/h",
    "wind_direction_10m": "°",
    "wind_gusts_10m": "km/h"
  },
  "current": {
    "time": "2025-05-22T15:00",
    "temperature_2m": 35.8,
    "relative_humidity_2m": 48,
    "apparent_temperature": 37.2,
    "precipitation": 0.0,
    "rain": 0.0,
    "weathercode": 0,
    "surface_pressure": 1009.9,
    "wind_speed_10m": 21.2,
    "wind_direction_10m": 330,
    "wind_gusts_10m": 32.4
  },
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C",
    "precipitation": "mm",
    "weathercode": "wmo code",
    "wind_speed_10m": "km/h"
  },
  "hourly": {
    "time": ["2025-05-22T00:00", "2025-05-22T01:00", ...],
    "temperature_2m": [28.5, 29.1, 30.2, 32.0, 34.5, 35.8, ...],
    "precipitation": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ...],
    "weathercode": [0, 0, 0, 0, 0, 0, ...],
    "wind_speed_10m": [18.0, 19.5, 20.1, 21.0, 21.2, ...]
  }
}
```

**Key observations**:
- **Temperature**: 35.8°C (typical for May in Qatar; not yet peak summer)
- **Apparent temperature** (feels-like): 37.2°C (heat index from humidity)
- **Wind**: 21.2 km/h from 330° (NNW), gusts to 32.4 km/h — **shamal wind pattern**
- **Weather code**: 0 = clear sky (WMO standard codes)
- **Precipitation**: 0.0 mm (expected; May is dry season)
- **Pressure**: 1009.9 hPa (normal for sea level)

**WMO Weather Codes** (international standard):
- 0 = Clear sky
- 1, 2, 3 = Mainly clear, partly cloudy, overcast
- 45, 48 = Fog
- 51-67 = Precipitation (drizzle, rain, snow)
- 71-77 = Snow
- 80-99 = Showers, thunderstorms

For Qatar, common codes: 0 (clear), 1-3 (clouds), 45 (fog/haze from dust), 80-82 (rare rain showers).

**Additional parameters** available:
- `is_day` (1 = day, 0 = night, useful for solar panel monitoring)
- `cloud_cover` (% sky coverage)
- `visibility` (meters)
- `evapotranspiration` (mm, relevant for agriculture/irrigation)
- `soil_temperature_0cm`, `soil_moisture_0_to_1cm` (surface soil conditions)
- `uv_index` (UV radiation, high in Qatar year-round)

**Multi-location**: Can request multiple lat/lon points in a single call.

**Daily forecast** (not shown in example):
```
&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,wind_speed_10m_max
```

Returns 16-day daily summary.

## Integration Notes

- **Polling interval**: 15 minutes for `current` block; 60 minutes for `hourly`
- **CloudEvents subject**: `weather/doha` or `weather/{lat}_{lon}`
- **Kafka key**: Location identifier (e.g., `doha` or `25.28_51.52`)
- **Entity model**: Grid point time series (not station-based, but model output for coordinates)
- **Data source**: Open-Meteo aggregates ECMWF IFS (primary for Middle East), GFS, ICON, MeteoFrance AROME/ARPEGE
- **License**: CC BY 4.0
- **Overlap check**: The repo has **DWD** (German weather), **NOAA NWS** (US weather), **NOAA NDBC** (US buoy weather). A **global weather bridge** using Open-Meteo would extend coverage to any location worldwide, including regions without national met service APIs (like Qatar).
- **Comparison with official sources**: Qatar Met Department (qweather.gov.qa) is inaccessible. METAR data (aviationweather.gov) provides airport-specific observations but only 3 stations in Qatar and limited parameters (no soil moisture, UV index, etc.). Open-Meteo provides richer parameterization and any-location coverage.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Current block ~15 min; hourly forecasts every hour |
| Openness | 3 | No auth, free tier (10k requests/day), CC BY 4.0 |
| Stability | 3 | Open-Meteo operational service, multi-model backend |
| Structure | 2 | Typed JSON with units metadata |
| Identifiers | 2 | Lat/lon grid points (stable but not named station IDs) |
| Additive value | 2 | Extends weather coverage to global (beyond DWD, NOAA) |

**Verdict**: Recommended as a **global weather bridge** using Open-Meteo's multi-model
forecast API. Qatar (Doha at 25.28°N, 51.52°E) would be the initial configuration, but the
bridge could cover any city/location worldwide. This fills geographic gaps in the repo's
weather coverage.

**Use cases**:
- Public weather dashboard for Qatar (alternative to inaccessible national met service)
- Heat stress monitoring (apparent temperature, humidity)
- Dust storm tracking (cross-reference low visibility with dust AQ parameter)
- Solar/renewable energy forecasting (cloud cover, solar radiation)
- Agriculture/irrigation planning (evapotranspiration, soil moisture)
- Outdoor event planning (FIFA-legacy stadiums, sporting events)

**Qatar-specific value**:
- Shamal wind forecasting (critical for aviation, dust transport, desalination intake clogging)
- Heat wave early warning (summer temperatures routinely exceed 45°C)
- Rare precipitation events (flash floods can occur with <10mm rain due to poor drainage in Doha)

**Comparison with METAR**: METARs provide **observations** (what's happening now at the airport).
Open-Meteo provides **forecasts** (what's expected in the next hours/days) plus richer current
conditions (soil moisture, UV index, etc.). Both are complementary — METAR for aviation-grade
ground truth, Open-Meteo for broader parameter coverage and forecasting.
