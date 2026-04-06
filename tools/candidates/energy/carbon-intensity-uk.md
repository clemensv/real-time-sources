# Carbon Intensity API (National Grid ESO)

**Country/Region**: Great Britain (national + 17 DNO regions)
**Publisher**: National Grid ESO, developed with Environmental Defense Fund Europe, University of Oxford, WWF
**API Endpoint**: `https://api.carbonintensity.org.uk/`
**Documentation**: https://carbon-intensity.github.io/api-definitions/
**Protocol**: REST
**Auth**: None (fully open, no API key)
**Data Format**: JSON
**Update Frequency**: Half-hourly (every 30 minutes)
**License**: CC-BY 4.0

## What It Provides

The Carbon Intensity API provides a focused, real-time view of the carbon intensity of electricity generation in Great Britain. It includes both forecast and actual values, making it unique among grid data APIs.

Key endpoints:

- `/intensity` — Current national carbon intensity (forecast + actual, gCO2/kWh) with qualitative index (very low / low / moderate / high / very high)
- `/intensity/date/{date}` — Historical intensity by date
- `/intensity/factors` — Static emission factors by fuel type
- `/generation` — Current national generation mix (percentage by fuel type)
- `/regional` — Carbon intensity and generation mix for 17 regional DNO areas
- `/regional/regionid/{id}` — Per-region data

## API Details

Clean REST API, no authentication:

```
GET https://api.carbonintensity.org.uk/intensity
```

Returns:

```json
{
  "data": [{
    "from": "2026-04-06T09:30Z",
    "to": "2026-04-06T10:00Z",
    "intensity": {
      "forecast": 66,
      "actual": 68,
      "index": "low"
    }
  }]
}
```

Generation mix endpoint:

```
GET https://api.carbonintensity.org.uk/generation
```

Returns:

```json
{
  "data": {
    "from": "2026-04-06T09:30Z",
    "to": "2026-04-06T10:00Z",
    "generationmix": [
      {"fuel": "nuclear", "perc": 19.1},
      {"fuel": "wind", "perc": 17.1},
      {"fuel": "solar", "perc": 29.0},
      {"fuel": "gas", "perc": 8.3},
      {"fuel": "imports", "perc": 22.5},
      {"fuel": "biomass", "perc": 3.9}
    ]
  }
}
```

Regional endpoint returns all 17 DNO regions with per-region intensity and generation mix.

## Freshness Assessment

Updated every 30 minutes, aligned with GB settlement periods. Provides both forecast (ahead-of-time) and actual (measured) values. The forecast is generated using machine learning models trained on weather data, grid demand forecasts, and scheduled generation. Truly real-time.

## Entity Model

- **Time Window**: Half-hourly (from/to UTC timestamps)
- **Intensity**: Forecast and actual in gCO2/kWh, plus categorical index
- **Generation Mix**: Percentage per fuel type (biomass, coal, gas, hydro, imports, nuclear, oil, other, solar, wind)
- **Regions**: 17 DNO regions (Scottish Hydro, SP Distribution, Electricity North West, etc.) identified by regionid (1-17)
- **DNO Region**: Distribution Network Operator area name and shortname

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Half-hourly, real-time with forecasts |
| Openness | 3 | No auth, no key, fully open, CC-BY |
| Stability | 3 | Backed by National Grid ESO, mature API |
| Structure | 3 | Very clean JSON, simple endpoints, well-documented |
| Identifiers | 2 | Region IDs are numeric (1-17), not standard codes |
| Additive Value | 3 | Unique carbon intensity focus with ML forecasting, regional granularity |
| **Total** | **17/18** | |

## Notes

- This is a purpose-built API — clean, fast, and focused on carbon intensity. An absolute gem.
- The regional breakdown to 17 DNO areas is unique — no other API provides this level of geographic carbon intensity granularity.
- The forecast vs. actual pairing enables forward-looking carbon-aware scheduling.
- Pairs perfectly with Elexon BMRS for deeper generation data if needed.
- The API is free and has no documented rate limits, though reasonable use is expected.
- Built as part of a collaboration between National Grid ESO, EDF, Oxford, and WWF.
