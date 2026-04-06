# Singapore NEA Weather API (data.gov.sg)

**Country/Region**: Singapore
**Publisher**: National Environment Agency (NEA) via data.gov.sg
**API Endpoint**: `https://api.data.gov.sg/v1/environment/`
**Documentation**: https://data.gov.sg/datasets?topics=environment
**Protocol**: REST (JSON)
**Auth**: None (fully open, no API key required)
**Data Format**: JSON
**Update Frequency**: 1–5 minutes (real-time station data), 2 hours (area forecasts)
**License**: Singapore Open Data License

## What It Provides

Singapore's environment data portal provides real-time weather observations from a dense network of ~50+ stations across the island, plus area-level forecasts:

- **Air Temperature** (`air-temperature`): Real-time readings from weather stations, updated every minute. Temperature in °C with station metadata (lat/lon).

- **Rainfall** (`rainfall`): Real-time 5-minute rainfall readings from ~50+ rain gauge stations across Singapore. Each station reports rainfall amount in mm.

- **Relative Humidity** (`relative-humidity`): Real-time humidity readings.

- **Wind Speed** (`wind-speed`): Real-time wind observations.

- **Wind Direction** (`wind-direction`): Real-time wind direction.

- **2-Hour Weather Forecast** (`2-hour-weather-forecast`): Area-level forecasts for ~47 planning areas across Singapore (Ang Mo Kio, Bedok, Bishan, etc.) with forecast text (e.g., "Partly Cloudy (Night)").

- **24-Hour Weather Forecast** (`24-hour-weather-forecast`): Island-wide forecast.

- **4-Day Weather Forecast** (`4-day-weather-forecast`): Extended forecast.

- **UV Index** (`uv-index`): Real-time UV index.

- **PM2.5** (`pm25`): Real-time PM2.5 readings.

- **PSI** (`psi`): Pollutant Standards Index.

## API Details

Clean REST API with consistent patterns:
```
GET https://api.data.gov.sg/v1/environment/air-temperature
GET https://api.data.gov.sg/v1/environment/rainfall
GET https://api.data.gov.sg/v1/environment/2-hour-weather-forecast
```

Optional `date_time` or `date` parameter for historical queries:
```
GET https://api.data.gov.sg/v1/environment/air-temperature?date_time=2026-04-06T12:00:00
```

Responses include `metadata` (station list with lat/lon), `items` (timestamped readings), and `api_info` (status). Station readings are nested under each item.

No authentication required. Returns JSON with ISO 8601 timestamps and timezone offsets.

## Freshness Assessment

- Station observations (temperature, rainfall, wind, humidity) update every 1–5 minutes.
- Probed live — received `api_info.status: "healthy"` with timestamp `2026-04-06T19:10:00+08:00`.
- 2-hour forecast updates around each period boundary (every 2 hours).
- Rain gauge data from ~50+ stations provides dense coverage for a small nation.

## Entity Model

- **Station**: String ID (e.g., "S107"), device_id, name, lat/lon location.
- **Reading**: station_id + value, nested under timestamped items.
- **Forecast Area**: Named planning area (e.g., "Ang Mo Kio", "City") with label coordinates.
- **Forecast**: Area + forecast text + valid period (start/end).

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 1-minute updates for temperature, 5-min for rainfall, real-time readings |
| Openness | 3 | No auth, no registration, government open data platform |
| Stability | 3 | Government platform (data.gov.sg), well-maintained, versioned API |
| Structure | 3 | Consistent JSON structure, station metadata embedded, ISO 8601 timestamps |
| Identifiers | 3 | Stable station IDs and device IDs, named planning areas |
| Additive Value | 2 | Singapore-only (tiny coverage area), but exemplary tropical urban monitoring |
| **Total** | **17/18** | |

## Notes

- Possibly the highest-frequency open weather API anywhere — temperature readings every 60 seconds, no auth.
- The dense rain gauge network (~50+ stations on a 728 km² island) provides extraordinary spatial resolution for precipitation monitoring.
- Small geographic coverage (Singapore only), but the data quality and API design make it a reference implementation.
- Air quality data (PM2.5, PSI) alongside weather is valuable for environmental monitoring.
- The data.gov.sg platform also hosts transport, demographics, and infrastructure data — weather is one vertical.
- Excellent candidate for integration if tropical Southeast Asian coverage is needed.
