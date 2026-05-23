# NOAA GOES Differential Electron Flux (SWPC)

- **Country/Region**: USA / Global (space-based)
- **Endpoint**: `https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-7-day.json`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON
- **Freshness**: 5-minute cadence
- **Docs**: https://www.swpc.noaa.gov/products/goes-electron-flux
- **Score**: 16/18

## Overview

NOAA SWPC publishes real-time differential electron flux measurements from GOES satellites' Magnetospheric Electron Detector (MagEIS) instruments. GOES spacecraft measure energetic electrons in multiple energy channels from ~30 keV to ~4 MeV. Electron flux monitoring is critical for satellite operations and space weather forecasting.

Electron flux products are used for:
- **Satellite anomaly prediction**: High-energy electrons cause deep dielectric charging (single-event upsets, component failures)
- **Radiation belt dynamics**: Tracking outer Van Allen belt intensification
- **Geomagnetic storm monitoring**: Electron injections during substorms
- **Spacecraft design**: Statistical environment models for radiation shielding

Electron flux can increase by 2-3 orders of magnitude during geomagnetic storms. Prolonged exposure to >1 MeV electrons damages solar panels and electronics.

The SWPC API provides 7 days of differential electron flux across 8-11 energy channels per satellite, measured at 5-minute intervals.

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-7-day.json
```

Response: JSON array of ~20,000 measurements (7 days × 288 intervals/day × ~10 channels).

Sample record:
```json
{
  "time_tag": "2026-05-23T08:00:00Z",
  "satellite": 18,
  "flux": 1.234E+02,
  "energy": "40-50 keV",
  "channel": "E1"
}
```

**Fields:**
- `time_tag`: ISO 8601 timestamp (UTC)
- `satellite`: GOES satellite number (18, 19)
- `flux`: Differential electron flux (particles/cm²/s/sr/keV)
- `energy`: Energy range (keV) — e.g., "800-1000 keV"
- `channel`: Detector channel ID (E1-E11)

**Key model**: `{satellite}/{channel}` (e.g., "18/E5") — stable per detector/energy band.

**Volume**: ~10 records per 5-minute interval per satellite, ~2,880 events/day.

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | Critical for satellite operations and radiation belt science |
| Freshness | 3/3 | 5-minute cadence, continuous monitoring |
| Openness | 3/3 | No auth, no rate limits, stable SWPC endpoint |
| Schema Clarity | 3/3 | Clean JSON, well-documented channels |
| Machine-Readability | 3/3 | JSON array, straightforward parsing |
| Repo Fit | 1/3 | Space weather present, but electron flux is incremental to proton/X-ray |

**Total: 16/18**

- Operationally significant for satellite operators
- Multi-channel spectral measurements
- 5-minute resolution captures storm dynamics
- Stable keying by satellite + channel
- No authentication required
- Not yet covered by existing `noaa-goes` bridge

## Limitations

- Data is 7-day rolling window
- Interpretation requires knowledge of flux thresholds for satellite risk
- Background cosmic ray electrons present even during quiet periods
- Channel/energy mappings vary between GOES-18 and GOES-19

## Verdict

**CONSIDER** — High-quality electron flux data with 5-minute cadence and clean JSON. However, **value is incremental** given that X-ray flux and proton flux are higher-priority space weather streams. Electron flux is important for satellite operators but less directly tied to public-facing alerts than solar flares or radiation storms. **Lower priority** than X-ray/proton flux. Include if comprehensive space weather coverage is desired. Polled endpoint; HTTP GET every 5 minutes.
