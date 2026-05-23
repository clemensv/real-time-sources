# NOAA GOES Differential Proton Flux (SWPC)

- **Country/Region**: USA / Global (space-based)
- **Endpoint**: `https://services.swpc.noaa.gov/json/goes/primary/differential-protons-7-day.json`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON
- **Freshness**: 5-minute cadence
- **Docs**: https://www.swpc.noaa.gov/products/goes-proton-flux
- **Score**: 17/18

## Overview

The NOAA Space Weather Prediction Center (SWPC) publishes real-time differential proton flux measurements from GOES satellites. GOES spacecraft carry energetic particle sensors that measure proton fluxes across multiple energy channels, from low-energy solar energetic particles (SEPs) to high-energy cosmic rays.

Proton flux monitoring is critical for:
- **Radiation storm forecasting**: S1-S5 scale NOAA space weather alerts
- **Aviation safety**: polar route radiation exposure during solar events
- **Satellite operations**: single-event upsets and solar panel degradation
- **Human spaceflight**: crew radiation dose monitoring (ISS, Artemis)

Solar proton events (SPEs) occur when coronal mass ejections (CMEs) or solar flares accelerate particles to relativistic speeds. Proton flux can increase by 3-5 orders of magnitude during major events.

The SWPC API provides 7 days of differential proton flux across 8-11 energy channels per satellite, measured at 5-minute intervals.

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://services.swpc.noaa.gov/json/goes/primary/differential-protons-7-day.json
```

Response: JSON array of ~26,000 measurements (7 days × 288 intervals/day × ~13 channels).

Sample record:
```json
{
  "time_tag": "2026-05-23T07:40:00Z",
  "satellite": 19,
  "flux": 9.358791999147797E-07,
  "energy": "83700-98500 keV",
  "yaw_flip": 0,
  "channel": "P8A"
}
```

**Fields:**
- `time_tag`: ISO 8601 timestamp (UTC)
- `satellite`: GOES satellite number (18, 19)
- `flux`: Differential proton flux (particles/cm²/s/sr/MeV)
- `energy`: Energy range (keV) — e.g., "5800-11000 keV"
- `yaw_flip`: Yaw flip flag (0 or 1) — affects certain channels during satellite maneuvers
- `channel`: Detector channel ID (P2, P3, P4, P5, P6, P7, P8A, P8B, P9, P10, P11)

**Key model**: `{satellite}/{channel}` (e.g., "19/P8A") — stable per detector/energy band.

**Volume**: ~13 records per 5-minute interval (varies by satellite), ~3,744 events/day.

## Schema / Sample

```json
{
  "time_tag": "2026-05-23T07:40:00Z",
  "satellite": 19,
  "flux": 5.510260052687954E-07,
  "energy": "99900-118000 keV",
  "yaw_flip": 0,
  "channel": "P8B"
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | Critical for radiation storm alerts and aviation/spaceflight safety |
| Freshness | 3/3 | 5-minute cadence, continuous monitoring |
| Openness | 3/3 | No auth, no rate limits, stable NOAA SWPC endpoint |
| Schema Clarity | 3/3 | Clean JSON, well-documented channels and energy ranges |
| Machine-Readability | 3/3 | JSON array, straightforward parsing |
| Repo Fit | 2/3 | Space weather domain present, but proton flux not yet bridged |

**Total: 17/18**

- Operationally significant: drives NOAA radiation storm alerts (S-scale)
- Aviation impact: airlines divert polar routes during proton events
- Multi-channel measurements provide full energy spectrum
- Stable keying by satellite + detector channel
- 5-minute resolution is appropriate for radiation storm evolution
- No authentication required
- Currently **not covered** by existing `noaa-goes` bridge

## Limitations

- Data is 7-day rolling window (historical archive requires NCEI)
- Yaw flip flag indicates periods where certain channels may be unreliable
- Channel/energy mappings vary slightly between GOES-18 and GOES-19
- Scientific units require context (flux thresholds for S1-S5 radiation storms)
- Integral flux (single threshold) often used for alerts, whereas this is differential (spectral)
- Background cosmic ray flux present even during quiet periods

## Verdict

**RECOMMEND** — High-value space weather product with 5-minute cadence, clean JSON, stable keying, and zero auth barriers. Proton flux is the **primary observable** for radiation storm forecasting and is operationally significant for aviation and satellite operators. Fills gap in current `noaa-goes` bridge. Polled endpoint; HTTP GET every 5 minutes with delta detection on time_tag.
