# NOAA SWPC Propagated Solar Wind

- **Country/Region**: USA / Global (L1 spacecraft DSCOVR + ACE)
- **Endpoint**: `https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON (tabular array)
- **Freshness**: 1-minute cadence
- **Docs**: https://www.swpc.noaa.gov/products/real-time-solar-wind
- **Score**: 18/18

## Overview

NOAA SWPC publishes **propagated solar wind** measurements from spacecraft at the Sun-Earth Lagrange point 1 (L1), ~1.5 million km upstream from Earth. Primary sources: **DSCOVR** (NOAA operational) and **ACE** (NASA backup). Solar wind data is propagated forward in time to predict when it will reach Earth's magnetosphere (~30-60 minute lead time).

Solar wind monitoring is critical for:
- **Geomagnetic storm forecasting**: Solar wind speed/density/IMF drive magnetospheric disturbances
- **Aurora predictions**: Southward IMF (Bz < 0) triggers substorms
- **Satellite operations**: Drag and charging risk assessment
- **GPS accuracy**: Ionospheric disturbances degrade positioning

The propagated product includes:
- **Bulk parameters**: Speed, density, temperature
- **Magnetic field**: Bx, By, Bz, Bt (GSM coordinates)
- **Velocity components**: Vx, Vy, Vz (when available)
- **Propagation timestamp**: When this solar wind will reach Earth

This is **the same data source** that the existing `noaa-goes` bridge ingests as "solar wind summary," but that bridge fetches the **current-time snapshot** endpoint. This propagated endpoint provides the **full time series** with 1-minute resolution and forward propagation.

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json
```

Response: JSON array of ~10,000+ rows (7 days × 1440 min/day).

**Data structure**: Array of arrays (CSV-like), with first row as header.

Sample:
```json
[
  ["time_tag", "speed", "density", "temperature", "bx", "by", "bz", "bt", "vx", "vy", "vz", "propagated_time_tag"],
  ["2026-05-16 00:00:00.000", "713.2", "3.90", "352237", "5.61", "-4.21", "1.32", "7.13", null, null, null, "2026-05-16 00:29:39.000"],
  ["2026-05-16 00:01:00.000", "717.8", "4.06", "357248", "5.65", "-3.18", "-1.94", "6.77", null, null, null, "2026-05-16 00:30:28.000"]
]
```

**Fields** (row 0 = header):
- `time_tag`: Observation time at L1 (UTC)
- `speed`: Solar wind speed (km/s)
- `density`: Proton density (particles/cm³)
- `temperature`: Proton temperature (K)
- `bx`, `by`, `bz`: Magnetic field components (nT, GSM coordinates)
- `bt`: Total magnetic field magnitude (nT)
- `vx`, `vy`, `vz`: Velocity components (km/s) — often null
- `propagated_time_tag`: Predicted Earth arrival time (UTC)

**Key model**: `{time_tag}` — single time series keyed by observation time.

**Volume**: ~1 record/minute, ~1,440 events/day.

## Schema / Sample

```json
["2026-05-16 00:02:00.000", "718.1", "4.50", "351916", "5.44", "-3.73", "-2.17", "6.94", null, null, null, "2026-05-16 00:31:27.000"]
```

Parsed:
```
{
  "time_tag": "2026-05-16 00:02:00.000",
  "speed": 718.1,
  "density": 4.50,
  "temperature": 351916,
  "bx": 5.44,
  "by": -3.73,
  "bz": -2.17,
  "bt": 6.94,
  "vx": null,
  "vy": null,
  "vz": null,
  "propagated_time_tag": "2026-05-16 00:31:27.000"
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | **Primary input** for geomagnetic storm forecasting |
| Freshness | 3/3 | 1-minute cadence, continuous real-time stream |
| Openness | 3/3 | No auth, no rate limits, stable SWPC endpoint |
| Schema Clarity | 3/3 | Clean tabular structure, well-documented fields |
| Machine-Readability | 3/3 | JSON array (requires header row parsing, but straightforward) |
| Repo Fit | 3/3 | Perfect fit: high cadence, stable keying, operational significance |

**Total: 18/18**

- **Operationally critical**: This is the #1 input for space weather forecasting
- Propagation model provides 30-60 minute lead time for Earth impacts
- 1-minute cadence captures rapid IMF changes
- Bz (north-south IMF) is the **key parameter** for aurora/substorm prediction
- Clean JSON structure (header + data rows)
- No authentication required
- Existing `noaa-goes` bridge fetches snapshot; this gives full time series

## Limitations

- Data is 7-day rolling window (archive requires NCEI)
- Vx/Vy/Vz are often `null` (DSCOVR doesn't measure all velocity components reliably)
- Propagation model is linear (assumes constant speed from L1 to Earth)
- Single-point measurement (not a network)
- Gaps occur during spacecraft maneuvers or instrument anomalies
- ACE is aging backup (launched 1997, degraded plasma sensor)

## Verdict

**STRONGLY RECOMMEND** — Perfect 18/18 score. This is the **most operationally significant space weather data stream** available. Solar wind Bz is the primary driver of geomagnetic storms and aurora. 1-minute cadence, clean JSON, zero auth, and strong repo fit. The existing `noaa-goes` bridge fetches a snapshot; this endpoint provides the **full 7-day time series** with propagation metadata. High priority for implementation. Polled endpoint; HTTP GET every 60 seconds with delta detection on `time_tag`.
