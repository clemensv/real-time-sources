# NOAA 10.7cm Solar Radio Flux

- **Country/Region**: USA / Global (ground + satellite-based)
- **Endpoint**: `https://services.swpc.noaa.gov/json/f107_cm_flux.json`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON
- **Freshness**: 3x daily (morning, noon, afternoon observations)
- **Docs**: https://www.swpc.noaa.gov/products/10-cm-radio-flux
- **Score**: 15/18

## Overview

The 10.7cm (2800 MHz) solar radio flux is a key index of solar activity measured by ground-based radio telescopes. NOAA SWPC publishes these measurements from the Dominion Radio Astrophysical Observatory (DRAO) in Canada and USAF observatories. The flux value correlates with sunspot number, UV radiation, and the overall level of solar activity.

10.7cm flux is used for:
- **Ionospheric modeling**: Radio wave propagation forecasts for HF communications
- **Satellite drag prediction**: Solar flux drives thermospheric density (affects LEO orbits)
- **Space weather indices**: F10.7 is a standard input for atmospheric models
- **Solar cycle monitoring**: Long-term trend tracking (1947-present)

Measurements are reported 3 times per day (morning, noon, afternoon local time at observatory) in Solar Flux Units (SFU, 10^-22 W/m²/Hz). The API includes current flux, 90-day mean, and observation schedule.

**Note**: While measured from ground, this is a **satellite-observable** (solar radio emission) and is often grouped with space weather satellite products. GOES satellites also monitor solar radio bursts.

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://services.swpc.noaa.gov/json/f107_cm_flux.json
```

Response: JSON array of ~120 measurements (3-4 months of 3x/day observations).

Sample record:
```json
{
  "time_tag": "2026-04-12T20:00:00",
  "frequency": 2800,
  "flux": 99.0,
  "reporting_schedule": "Noon",
  "avg_begin_date": "2026-01-13T20:00:00",
  "ninety_day_mean": 135.0,
  "rec_count": 90
}
```

**Fields:**
- `time_tag`: Observation timestamp (UTC)
- `frequency`: Radio frequency (MHz) — always 2800
- `flux`: Solar radio flux (SFU, 10^-22 W/m²/Hz)
- `reporting_schedule`: "Morning", "Noon", or "Afternoon"
- `avg_begin_date`: Start date of 90-day averaging window
- `ninety_day_mean`: 90-day running mean flux (SFU)
- `rec_count`: Number of observations in 90-day window

**Key model**: `{time_tag}` — single time series, keyed by observation time.

**Volume**: ~3 measurements/day, ~90/month.

## Schema / Sample

```json
{
  "time_tag": "2026-04-12T22:00:00",
  "frequency": 2800,
  "flux": 99.0,
  "reporting_schedule": "Afternoon",
  "avg_begin_date": null,
  "ninety_day_mean": null,
  "rec_count": null
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | Critical for ionospheric and satellite drag forecasting |
| Freshness | 2/3 | 3x daily (not sub-hourly, but acceptable for this parameter) |
| Openness | 3/3 | No auth, no rate limits, stable SWPC endpoint |
| Schema Clarity | 3/3 | Clean JSON, well-documented fields |
| Machine-Readability | 3/3 | JSON array, straightforward parsing |
| Repo Fit | 1/3 | Space weather present, but F10.7 is lower cadence and less event-driven |

**Total: 15/18**

- Standard solar activity index used globally
- 75+ year historical record (1947-present)
- 90-day mean included for context
- Operationally significant for satellite operators and radio propagation
- No authentication required
- Simple polling model

## Limitations

- **3x daily cadence** — not continuous like X-ray or proton flux
- Some records have `null` for 90-day mean (afternoon/morning obs don't compute it)
- Ground-based measurement (weather/equipment outages possible)
- Single-frequency measurement (not a full radio spectrum)
- Interpretation requires baseline context (solar min ~70 SFU, solar max ~200+ SFU)
- Less event-driven than flare or proton data

## Verdict

**CONSIDER** — Valuable solar activity index with 75+ year heritage and wide operational use. However, **3x daily cadence** is much lower than other SWPC products (X-ray, proton flux are 1-5 minute). F10.7 is more suited to **daily trend monitoring** than real-time event detection. **Lower priority** than high-cadence space weather streams. If the repo wants comprehensive solar indices, include it; otherwise, **defer** in favor of faster-updating products. Polled endpoint; HTTP GET every 8 hours.
