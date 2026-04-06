# IPMA — Instituto Português do Mar e da Atmosfera

**Country/Region**: Portugal (including Azores and Madeira)
**Publisher**: IPMA (Portuguese Institute for Sea and Atmosphere)
**API Endpoint**: `https://api.ipma.pt/open-data/`
**Documentation**: https://api.ipma.pt/ (terms), endpoints discoverable at `https://api.ipma.pt/open-data/`
**Protocol**: REST (static JSON files)
**Auth**: None (fully open, no registration required)
**Data Format**: JSON
**Update Frequency**: Multiple times daily (forecasts), hourly (observations)
**License**: Free for personal and public non-commercial use with attribution

## What It Provides

IPMA provides simple, static JSON endpoints for Portuguese weather data:

- **City forecasts (daily)**: Day 0 through day 4 forecasts for ~27 locations across mainland Portugal, Azores, and Madeira. Parameters: min/max temperature, precipitation probability, wind direction/speed class, weather type code.

- **Station observations**: Hourly meteorological observations from automatic weather stations across Portugal. Parameters: temperature, humidity, wind speed/direction, precipitation, radiation, pressure.

- **Sea conditions**: Wave forecasts and sea state data.

- **UV index**: Daily UV forecasts.

- **Weather type reference data**: Lookup tables for weather type codes and wind direction codes.

## API Details

Endpoints follow a simple static file pattern — no query parameters needed:

**Forecasts:**
```
https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/hp-daily-forecast-day0.json
https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/hp-daily-forecast-day1.json
```

**Observations:**
```
https://api.ipma.pt/open-data/observation/meteorology/stations/observations.json
```

The forecast response includes:
- `owner`: "IPMA"
- `country`: "PT"
- `forecastDate`: ISO date
- `dataUpdate`: ISO datetime of last update
- `data[]`: Array of location forecasts with `globalIdLocal` (station/city ID), lat/lon, weather parameters

Observation response is keyed by timestamp → station ID → parameter values.

Probed both endpoints and got fresh data:
- Forecast: `forecastDate: "2026-04-06"`, `dataUpdate: "2026-04-06T09:31:03"`
- Observations: Timestamped data from the current day

## Freshness Assessment

- Forecasts update multiple times daily (at least twice, typically early morning and late morning).
- Observations are hourly, with the JSON containing the most recent hour's data for all stations.
- The `dataUpdate` field in forecasts provides an exact freshness timestamp.
- Response sizes are small (a few KB), enabling frequent polling.

## Entity Model

- **Location**: Identified by `globalIdLocal` (7-digit numeric code), with lat/lon
- **Forecast**: Daily granularity with min/max temp, precipitation probability, weather type, wind class
- **Observation**: Hourly per station with temp, humidity, wind, precipitation, radiation, pressure
- **Weather type**: Numeric code mapped via reference endpoint to descriptions

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly observations, daily forecasts updated few times/day |
| Openness | 3 | No auth, no registration, fully open JSON endpoints |
| Stability | 2 | Government institute; simple static files are robust but undocumented |
| Structure | 3 | Clean JSON, simple flat structure, easy to parse |
| Identifiers | 2 | `globalIdLocal` codes are stable but not WMO standard |
| Additive Value | 2 | Portugal + Azores + Madeira coverage; small but fills Iberian gap |
| **Total** | **14/18** | |

## Notes

- One of the simplest weather APIs to integrate — just fetch a JSON URL. No auth, no query parameters, no pagination.
- The `-99.0` sentinel value indicates missing data (common in observation responses).
- Coverage extends to the Azores and Madeira archipelagos — unique Atlantic island coverage.
- Documentation is minimal. The endpoint structure must be discovered by exploration.
- The license restricts commercial use ("sem finalidades lucrativas"), which may limit some applications.
- Weather type codes need to be cross-referenced with a lookup table for human-readable descriptions.
- Very lightweight — suitable as a simple "small-country" weather data source.
