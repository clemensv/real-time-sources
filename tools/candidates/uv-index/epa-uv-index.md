# EPA UV Index Hourly Forecast

- **Country/Region**: United States
- **Publisher**: US Environmental Protection Agency (EPA)
- **Endpoint**: `https://data.epa.gov/efservice/getEnvirofactsUVHOURLY/ZIP/{zipcode}/JSON`
- **Protocol**: REST
- **Auth**: None
- **Format**: JSON, XML, CSV
- **Freshness**: Daily forecast with hourly values
- **Docs**: https://www.epa.gov/enviro/web-services
- **Score**: 15/18

## Overview

The EPA provides hourly UV Index forecasts for any US ZIP code through its Envirofacts REST API. The UV Index is critical for outdoor activity planning — it tells users when sun exposure is safe and when protection is needed. For a Puget Sound free-time advisor, this data helps recommend optimal outdoor activity windows and sun safety precautions.

## API Details

**Base URL:** `https://data.epa.gov/efservice/getEnvirofactsUVHOURLY/ZIP/{zipcode}/JSON`

**Key Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `getEnvirofactsUVHOURLY/ZIP/{zip}/JSON` | Hourly UV forecast for ZIP code |
| `getEnvirofactsUVDAILY/ZIP/{zip}/JSON` | Daily UV index summary |
| `getEnvirofactsUVHOURLY/CITY/{city}/STATE/{st}/JSON` | By city/state |

**Puget Sound ZIP Codes:** 98101 (Seattle), 98402 (Tacoma), 98110 (Bainbridge Island), 98225 (Bellingham)

**Verified Response (2026-04-08, ZIP 98101):**
```json
[
  {"ORDER": 1, "ZIP": "98101", "CITY": "Seattle", "STATE": "WA", "DATE_TIME": "Apr/08/2026 04 AM", "UV_VALUE": 0},
  {"ORDER": 2, "ZIP": "98101", "CITY": "Seattle", "STATE": "WA", "DATE_TIME": "Apr/08/2026 05 AM", "UV_VALUE": 0},
  {"ORDER": 3, "ZIP": "98101", "CITY": "Seattle", "STATE": "WA", "DATE_TIME": "Apr/08/2026 06 AM", "UV_VALUE": 0},
  {"ORDER": 8, "ZIP": "98101", "CITY": "Seattle", "STATE": "WA", "DATE_TIME": "Apr/08/2026 11 AM", "UV_VALUE": 4},
  {"ORDER": 10, "ZIP": "98101", "CITY": "Seattle", "STATE": "WA", "DATE_TIME": "Apr/08/2026 01 PM", "UV_VALUE": 5}
]
```

**UV Index Scale:**
- 0-2: Low (safe for most people)
- 3-5: Moderate (protection recommended)
- 6-7: High (protection essential)
- 8-10: Very High (avoid midday sun)
- 11+: Extreme (stay indoors)

## Freshness Assessment

Good. Forecasts are generated daily by NOAA and served through the EPA API. Hourly values cover the full daylight period. Data is forecast-based, not measured — but the NWS UV forecast model is well-calibrated and operationally reliable.

## Entity Model

- **Forecast** — ZIP code, city, state, date/time, UV value
- **Location** — ZIP-code keyed (US only)
- **Time Series** — Hourly values for the forecast day

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily forecast; hourly granularity but not real-time measured |
| Openness | 3 | No auth, US public domain |
| Stability | 3 | EPA federal agency, long-running Envirofacts service |
| Structure | 3 | Simple flat JSON, easy to parse |
| Identifiers | 2 | ZIP-code keyed; ORDER field for hourly sequence |
| Additive Value | 2 | Unique UV data not covered by weather APIs |
| **Total** | **15/18** | |

## Notes

- Very simple to integrate: single GET request returns full day's UV forecast.
- No rate limit documentation found, but federal API — reasonable use expected.
- Complements weather forecasts: even on warm cloudy days in Seattle, UV can be moderate.
- Summer in Seattle can see UV Index 7-9 (high to very high) which is relevant for outdoor safety.
- Alternative: OpenUV.io (free API key required) provides real-time calculated UV with more parameters but is a third-party service.
