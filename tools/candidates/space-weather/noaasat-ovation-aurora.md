# NOAA SWPC OVATION Aurora 30-Minute Forecast

- **Country/Region**: USA / Global (aurora oval regions)
- **Endpoint**: `https://services.swpc.noaa.gov/json/ovation_aurora_latest.json`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON (gridded forecast)
- **Freshness**: 30-minute forecast updated every few minutes
- **Docs**: https://www.swpc.noaa.gov/products/aurora-30-minute-forecast
- **Score**: 13/18

## Overview

NOAA SWPC publishes 30-minute aurora forecasts using the **OVATION** (Oval Variation, Assessment, Tracking, Intensity, and Online Nowcasting) model. OVATION predicts auroral intensity and location based on real-time solar wind measurements from DSCOVR/ACE at L1. The forecast shows the predicted aurora oval boundary and intensity in 1° latitude × 1° MLT (magnetic local time) bins.

Aurora forecasts are used for:
- **Public aurora viewing**: Notifying enthusiasts when aurora may be visible at lower latitudes
- **Aviation operations**: Polar route HF radio blackout warnings
- **Photography planning**: Optimal viewing time/location
- **Tourism**: Aurora tourism industry (Alaska, Iceland, Norway, Canada, New Zealand)

The OVATION model is driven by solar wind Bz (north-south IMF component) and density. Southward Bz triggers geomagnetic substorms that energize the aurora oval.

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://services.swpc.noaa.gov/json/ovation_aurora_latest.json
```

Response: Single JSON object with gridded forecast.

Sample structure:
```json
{
  "Forecast Time": "2026-05-23 08:30:00",
  "Data Format": "Latitude, Longitude, Aurora",
  "coordinates": [
    [65.5, -135.0, 2],
    [66.0, -135.0, 3],
    [66.5, -135.0, 4],
    ...
  ]
}
```

**Fields:**
- `Forecast Time`: Predicted time (UTC) for this aurora snapshot
- `Data Format`: Description of coordinate array structure
- `coordinates`: Array of `[latitude, longitude, aurora_intensity]` triplets

**Aurora intensity scale**: 0-10 (unitless; higher = brighter aurora)

**Grid resolution**: ~1° latitude × longitude bins around the aurora oval

**Key model**: `{lat}/{lon}` — gridded forecast, not entity-keyed.

**Volume**: 1 forecast snapshot updated every few minutes; each snapshot contains ~1,000-5,000 grid cells.

## Schema / Sample

```json
{
  "Forecast Time": "2026-05-23 08:30:00",
  "Data Format": "Latitude, Longitude, Aurora",
  "coordinates": [
    [67.0, -150.0, 5],
    [67.5, -150.0, 6],
    [68.0, -150.0, 4]
  ]
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2/3 | High public interest (aurora viewing), moderate operational use |
| Freshness | 3/3 | 30-minute forecast updated continuously (every few minutes) |
| Openness | 3/3 | No auth, no rate limits, stable SWPC endpoint |
| Schema Clarity | 3/3 | Clean JSON with lat/lon/intensity grid |
| Machine-Readability | 3/3 | JSON, straightforward parsing |
| Repo Fit | -1/3 | **Gridded forecast** (not entity-keyed time series) — keying model unclear |

**Total: 13/18**

- High public engagement potential (aurora alerts)
- 30-minute lead time is useful for real-time notifications
- Updated every few minutes (responsive to solar wind changes)
- Clean JSON structure
- No authentication required
- **However**: Gridded forecast model doesn't align well with entity-keyed events
- Not a sensor time series (it's a model output grid)

## Limitations

- **Gridded forecast** — no natural "station ID" or entity key
- Forecast skill degrades during extreme storms (model saturation)
- Resolution is coarse (~1° bins)
- Intensity scale is unitless (not directly comparable to scientific measures like Rayleigh)
- 30-minute lead time is short for travel planning
- Coverage is polar regions only (aurora oval, ~60-75° geomagnetic latitude)

## Verdict

**CONSIDER** — Aurora forecast has high public appeal and clean JSON structure. However, the **gridded forecast model** presents a keying challenge (no stable entity IDs). Potential approaches:
1. Emit the entire grid as a single "forecast update" event (loses spatial granularity)
2. Treat each grid cell as an entity (thousands of Kafka keys — not meaningful)
3. Pre-define "aurora viewing locations" (e.g., Fairbanks, Tromsø, Yellowknife) and extract forecasts for those points

Option 3 is feasible but requires use-case-specific configuration. **Lower priority** unless there's demand for aurora alerting. Alternatively, the existing `noaa-goes` bridge could add a "latest aurora forecast" snapshot if the grid-as-event model is acceptable. **Defer** for now due to gridded-data keying mismatch.
