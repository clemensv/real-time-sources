# Hong Kong Observatory (HKO) Open Data

**Country/Region**: Hong Kong SAR, China
**Publisher**: Hong Kong Observatory (HKO)
**API Endpoint**: `https://data.weather.gov.hk/weatherAPI/opendata/weather.php`
**Documentation**: https://www.hko.gov.hk/en/abouthko/opendata_intro.htm
**Protocol**: REST (simple query parameters)
**Auth**: None (fully open, no API key required)
**Data Format**: JSON
**Update Frequency**: 10 minutes (regional weather), hourly (current conditions), 2× daily (9-day forecast)
**License**: Hong Kong Open Government Data License

## What It Provides

HKO's open data API is one of the best-designed meteorological APIs in Asia — clean JSON, zero auth, real-time data from a dense urban network:

- **Current Weather Report** (`rhrread`): Real-time rainfall by district (18 districts), temperature from ~27 stations, humidity, UV index, weather icon and update time. Updated hourly and on significant change.

- **9-Day Weather Forecast** (`fnd`): Day-by-day forecasts with min/max temperature, humidity range, wind forecast, weather description, forecast icon, and probability of significant rain (PSR). Also includes sea temperature and soil temperature at 0.5m and 1.0m depths.

- **Local Weather Forecast** (`flw`): Textual forecast for today and tomorrow.

- **Weather Warning Information** (`warningInfo`): Detailed severe weather warnings in force — typhoon signals, rainstorm warnings, thunderstorm warnings, etc.

- **Warning Summary** (`warnsum`): Quick summary of active warnings.

- **Regional Weather** — multiple datasets updated every 10 minutes:
  - Temperature by station
  - Rainfall (past hour) by station
  - Visibility (10-minute mean) by station
  - 24-hour temperature difference by station

- **Rainfall Nowcast**: Gridded rainfall nowcast data updated every 12 minutes, covering 2 hours ahead.

- **Lightning Count**: Hourly cloud-to-ground and cloud-to-cloud lightning count over Hong Kong territory.

- **Tropical Cyclone Track**: Real-time typhoon track data when cyclones are active.

- **Earthquake Messages**: Quick earthquake messages for M6.0+ worldwide.

- **South China Coastal Waters Bulletin**: Marine weather, updated 7 times daily.

## API Details

Dead simple. Every endpoint is a single URL with `dataType` and `lang` parameters:
```
GET https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en
```

Supported `dataType` values include: `rhrread` (current), `fnd` (9-day forecast), `flw` (local forecast), `warningInfo`, `warnsum`, `swt` (special weather tips).

Language options: `en` (English), `tc` (Traditional Chinese), `sc` (Simplified Chinese).

No authentication, no rate limits documented, no pagination. Just fetch and parse.

## Freshness Assessment

- Current weather (`rhrread`): Updated approximately every hour and on significant weather change. Contains `updateTime` and `recordTime` fields with ISO 8601 timestamps including timezone.
- Regional observations: Every 10 minutes.
- Rainfall nowcast: Every 12 minutes.
- 9-day forecast: Twice daily and on updates.
- Probed live — received immediate JSON with current timestamps (e.g., `2026-04-06T19:02:00+08:00`).

## Entity Model

- **District/Place**: Named locations (e.g., "Central & Western District", "King's Park") — strings, not numeric IDs.
- **Temperature Reading**: Place + value + unit + recordTime.
- **Rainfall Reading**: Place + max rainfall + unit + time window.
- **Forecast Day**: Date (YYYYMMDD) + wind + weather + temp range + humidity range + icon + PSR.
- **Warning**: Type code + contents + update time.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-minute regional updates, hourly current conditions, real-time warnings |
| Openness | 3 | No auth, no registration, no rate limits documented |
| Stability | 3 | Government observatory (est. 1883), 48-page API documentation PDF |
| Structure | 3 | Clean JSON, simple query parameters, consistent response format |
| Identifiers | 2 | Place names (strings) rather than numeric IDs; forecast dates as YYYYMMDD |
| Additive Value | 3 | South China Sea typhoon tracking, tropical weather, unique lightning/nowcast data |
| **Total** | **17/18** | |

## Notes

- One of the easiest meteorological APIs to integrate. A single HTTP GET returns complete, well-structured JSON.
- Typhoon tracking data is particularly valuable — HKO is one of the WMO Regional Specialized Meteorological Centres for tropical cyclones.
- The 9-day forecast response includes soil temperature and sea temperature — unusual bonus data.
- Place-based rather than station-ID-based identifiers is a minor inconvenience but the names are stable.
- Hong Kong's dense urban weather station network provides neighborhood-level resolution for a city of 7.5 million.
- Bilingual (English/Chinese) API output with a simple `lang` parameter.
- Also provides astronomy data (sunrise/sunset, moonrise/moonset, tides) through the same API pattern.
