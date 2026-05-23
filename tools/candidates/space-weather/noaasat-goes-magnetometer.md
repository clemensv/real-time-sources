# NOAA GOES Magnetometer (SWPC)

- **Country/Region**: USA / Global (space-based)
- **Endpoint**: `https://services.swpc.noaa.gov/json/goes/primary/magnetometers-7-day.json`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON
- **Freshness**: 1-minute cadence
- **Docs**: https://www.swpc.noaa.gov/products/goes-magnetometer
- **Score**: 16/18

## Overview

NOAA publishes real-time magnetometer measurements from GOES satellites in geostationary orbit. GOES magnetometers measure the local magnetic field in three orthogonal directions: parallel (Hp), perpendicular-east (He), and perpendicular-north (Hn). These measurements detect geomagnetic disturbances caused by solar wind interactions with Earth's magnetosphere.

Magnetometer data from geostationary orbit provides early warning of:
- **Geomagnetic storms**: Sudden compressions or reconfigurations of Earth's magnetic field
- **Substorms**: Localized energy releases in the magnetotail
- **Magnetopause crossings**: Satellite entering/exiting Earth's magnetosphere
- **Ring current dynamics**: Inner magnetosphere particle populations

The total field magnitude and individual components are used to trigger NOAA geomagnetic storm alerts (G-scale) and to validate ground-based magnetometer networks.

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://services.swpc.noaa.gov/json/goes/primary/magnetometers-7-day.json
```

Response: JSON array of ~10,000 measurements (7 days × 1440 minutes).

Sample record:
```json
{
  "time_tag": "2026-05-23T07:47:00Z",
  "satellite": 19,
  "He": 50.682857513427734,
  "Hp": 83.48089599609375,
  "Hn": -0.9409253597259521,
  "total": 97.66627502441406,
  "arcjet_flag": false
}
```

**Fields:**
- `time_tag`: ISO 8601 timestamp (UTC)
- `satellite`: GOES satellite number (18, 19)
- `He`: East component of magnetic field (nT)
- `Hp`: Parallel component (nT)
- `Hn`: North component (nT)
- `total`: Total field magnitude (nT)
- `arcjet_flag`: Boolean flag indicating satellite maneuver interference

**Key model**: `{satellite}` (e.g., "19") — one time series per GOES satellite.

**Volume**: ~1 record/minute per satellite, ~1,440 events/satellite/day.

## Schema / Sample

```json
{
  "time_tag": "2026-05-23T07:48:00Z",
  "satellite": 19,
  "He": 50.64368438720703,
  "Hp": 83.6470718383789,
  "Hn": -0.8634705543518066,
  "total": 97.78739166259766,
  "arcjet_flag": false
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | Critical for geomagnetic storm detection and magnetosphere science |
| Freshness | 3/3 | 1-minute cadence, continuous monitoring |
| Openness | 3/3 | No auth, no rate limits, stable SWPC endpoint |
| Schema Clarity | 3/3 | Clean JSON, well-documented vector components |
| Machine-Readability | 3/3 | JSON array, straightforward parsing |
| Repo Fit | 1/3 | Space weather present, but magnetometer adds incremental value over K-index |

**Total: 16/18**

- Provides in-situ magnetic field measurements from geostationary orbit
- Complements ground-based magnetometer networks
- Arcjet flag provides quality control metadata
- Vector components enable scientific analysis of field direction
- 1-minute resolution captures substorm dynamics
- No authentication required

## Limitations

- Data is 7-day rolling window
- Arcjet thruster firings contaminate measurements periodically (flagged)
- Satellite maneuvers and eclipses can introduce gaps
- Single-point measurements (not a network like ground magnetometers)
- Interpretation requires knowledge of quiet-day baseline
- Less directly actionable than X-ray flux or proton flux (alerts derived from multi-input models)

## Verdict

**CONSIDER** — High-quality magnetometer data with 1-minute cadence and clean JSON structure. However, **value is incremental** given that `noaa-goes` bridge already ingests planetary K-index (which is derived from ground magnetometer networks). GOES magnetometer is more specialized (for magnetosphere scientists and advanced space weather analysis) and less directly tied to operational alerts than X-ray or proton flux. **Lower priority** unless there's demand for in-situ geomagnetic field measurements. Polled endpoint; HTTP GET every 60 seconds.
