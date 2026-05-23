# NOAA SWPC Planetary K-index Forecast

- **Country/Region**: USA / Global
- **Endpoint**: `https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON (tabular array)
- **Freshness**: 3-hourly forecast updated every few hours
- **Docs**: https://www.swpc.noaa.gov/products/planetary-k-index
- **Score**: 14/18

## Overview

NOAA SWPC publishes 3-day forecasts of the planetary K-index (Kp), a global measure of geomagnetic activity. Kp is derived from magnetometer stations worldwide and ranges from 0 (quiet) to 9 (extreme storm). SWPC forecasters issue Kp predictions based on solar wind models, CME arrival forecasts, and historical patterns.

Kp forecast is used for:
- **Aurora visibility predictions**: Kp ≥ 5 brings aurora to mid-latitudes
- **Power grid operations**: Kp ≥ 7 risks transformer damage (geomagnetically induced currents)
- **Satellite operations**: Kp ≥ 6 increases atmospheric drag
- **HF radio propagation**: Kp ≥ 4 degrades polar HF communications

The Kp forecast is a **model output** (not satellite data), but it's **driven by** satellite solar wind measurements from DSCOVR/ACE. This is distinct from the **observed Kp** time series (already in `noaa-goes` bridge).

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json
```

Response: JSON array of ~80 forecast entries (3 days × 8 3-hour bins/day).

**Data structure**: Array of arrays (CSV-like), with first row as header.

Sample:
```json
[
  ["time_tag", "kp"],
  ["2026-05-23 09:00:00", "3"],
  ["2026-05-23 12:00:00", "3"],
  ["2026-05-23 15:00:00", "4"],
  ["2026-05-23 18:00:00", "4"],
  ...
]
```

**Fields** (row 0 = header):
- `time_tag`: Forecast valid time (UTC)
- `kp`: Predicted Kp index (0-9, integer or decimal)

**Forecast horizon**: 3 days ahead (27 bins)

**Update frequency**: Every few hours (when forecasters issue new predictions)

**Key model**: `{time_tag}` — single forecast time series.

**Volume**: ~8 forecast bins/day, ~56 bins/week.

## Schema / Sample

```json
["2026-05-23 21:00:00", "5"]
```

Parsed:
```
{
  "time_tag": "2026-05-23 21:00:00",
  "kp": 5
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | **Primary public-facing geomagnetic storm forecast** |
| Freshness | 2/3 | Updated every few hours (not continuous like obs data) |
| Openness | 3/3 | No auth, no rate limits, stable SWPC endpoint |
| Schema Clarity | 3/3 | Clean tabular structure, simple format |
| Machine-Readability | 3/3 | JSON array (header + data rows) |
| Repo Fit | 0/3 | **Model forecast** (not satellite observations) — different paradigm than sensor streams |

**Total: 14/18**

- Kp forecast is the **most widely used** geomagnetic storm prediction
- Drives public aurora alerts and aviation/power grid warnings
- 3-day horizon is useful for planning
- Clean JSON structure
- No authentication required
- **However**: This is a **forecast model output**, not satellite telemetry
- Repo is focused on **observational data streams**, not forecast products
- Lower event volume (8 updates/day vs. 1,440 for observed Kp)

## Limitations

- **Forecast** (model output), not observations
- 3-hourly resolution (coarse compared to 1-minute solar wind data)
- Forecast skill degrades beyond 24 hours
- Human forecaster input (not purely algorithmic)
- Integer Kp values (loss of granularity compared to observed Kp with fractional precision)
- No uncertainty quantification (no confidence intervals or ensemble spread)

## Verdict

**SKIP** — While Kp forecast is operationally valuable and has clean JSON, it's a **forecast model output** rather than an **observational data stream**. This repo focuses on real-time or near-real-time sensor/satellite observations, not model predictions. The **observed Kp** time series (with fractional precision and 1-minute/3-hour cadence) is already in the `noaa-goes` bridge. Adding the forecast would be redundant and deviates from the repo's observational focus. **Defer** unless the repo expands scope to include forecast products. If added, it should be clearly marked as "forecast" to distinguish from observational streams.
