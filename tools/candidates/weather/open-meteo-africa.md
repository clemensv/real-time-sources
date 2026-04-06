# Open-Meteo Weather API — African Coverage

- **Country/Region**: Pan-African (global coverage, 1km resolution)
- **Endpoint**: `https://api.open-meteo.com/v1/forecast?latitude=-1.2921&longitude=36.8219&current_weather=true`
- **Protocol**: REST
- **Auth**: None (rate-limited; commercial plans available)
- **Format**: JSON
- **Freshness**: Updated every 15 minutes (current weather), hourly forecasts
- **Docs**: https://open-meteo.com/en/docs
- **Score**: 16/18

## Overview

Open-Meteo is a free, open-source weather API that provides high-resolution weather
data for any location globally — including all of Africa. Unlike most national
meteorological services in Africa (which either lack APIs or hide them behind paywalls),
Open-Meteo provides consistent, machine-readable weather data for every African city
and village.

The data comes from multiple numerical weather prediction models, including ECMWF IFS,
DWD ICON, and regional models. For Africa, this means better coverage than any single
national met service can provide.

## Endpoint Analysis

**Verified live** (Nairobi, Kenya):
```json
{
  "latitude": -1.25,
  "longitude": 36.875,
  "elevation": 1668.0,
  "current_weather": {
    "time": "2026-04-06T21:45",
    "temperature": 16.6,
    "windspeed": 7.7,
    "winddirection": 41,
    "is_day": 0,
    "weathercode": 3
  }
}
```

Key parameters for African cities:
```
# Nairobi
?latitude=-1.29&longitude=36.82&current_weather=true

# Lagos
?latitude=6.45&longitude=3.40&current_weather=true

# Cairo
?latitude=30.04&longitude=31.24&current_weather=true

# Johannesburg
?latitude=-26.20&longitude=28.05&current_weather=true

# Addis Ababa
?latitude=9.02&longitude=38.75&current_weather=true

# Dar es Salaam
?latitude=-6.79&longitude=39.28&current_weather=true
```

Extended parameters available: `current=temperature_2m,relative_humidity_2m,rain,
wind_speed_10m,wind_direction_10m,surface_pressure,uv_index`

Also supports hourly and daily forecasts up to 16 days.

## Integration Notes

This is the easiest Africa-wide weather bridge to build:

- **Batch approach**: Define a list of African cities/stations (capital cities, major
  urban areas, agricultural zones). Poll each every 15 minutes.
- **No auth complexity**: Free tier allows 10,000 requests/day. For 50 African cities
  polled every 15 minutes = 4,800 requests/day — well within limits.
- **Rich parameters**: Beyond basic weather, request air quality, soil moisture, and
  UV index — all relevant for African contexts (agriculture, health).
- **Historical data**: Open-Meteo also provides historical weather data through the
  same API structure, useful for anomaly detection.
- **Coordinate-based**: No need for station codes — any lat/lon works. This is a
  major advantage for Africa where station infrastructure is sparse.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15-minute update interval |
| Openness | 3 | No auth for free tier, open-source |
| Stability | 3 | Well-maintained open-source project |
| Structure | 3 | Clean JSON, well-documented parameters |
| Identifiers | 1 | Coordinate-based, no station IDs |
| Richness | 3 | Temperature, humidity, rain, wind, UV, soil moisture |
