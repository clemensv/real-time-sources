# NOAA GOES X-ray Flux (SWPC)

- **Country/Region**: USA / Global (space-based)
- **Endpoint**: `https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json`
- **Protocol**: REST (JSON)
- **Auth**: None
- **Format**: JSON
- **Freshness**: 1-minute cadence
- **Docs**: https://www.swpc.noaa.gov/products/goes-x-ray-flux
- **Score**: 17/18

## Overview

The NOAA Space Weather Prediction Center (SWPC) publishes real-time X-ray flux measurements from the GOES satellite constellation's Solar X-ray Imager (SXI) instruments. GOES satellites monitor the Sun continuously from geostationary orbit, measuring X-ray emissions in two energy bands: 0.05-0.4 nm (short) and 0.1-0.8 nm (long). These measurements are critical for detecting solar flares, which are classified from A to X based on peak flux intensity.

X-ray flux data drives space weather alerts that protect satellite operations, power grids, aviation, and GPS systems. A sudden spike in X-ray emissions indicates a solar flare, with M-class and X-class flares posing risks to Earth's ionosphere and magnetosphere.

The SWPC API provides 7 days of rolling data at 1-minute resolution. Currently monitored satellites: GOES-16 (GOES-East), GOES-18 (GOES-West), GOES-19 (operational reserve).

## Endpoint Analysis

**Endpoint verified live:**

```
GET https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json
```

Response: JSON array of ~20,000 measurements (7 days × 1440 min/day × 2 energy bands).

Sample record:
```json
{
  "time_tag": "2026-05-23T07:45:00Z",
  "satellite": 18,
  "flux": 1.0624817150528543E-06,
  "observed_flux": 1.078627633432916E-06,
  "electron_correction": 1.6145847325788054E-08,
  "electron_contaminaton": false,
  "energy": "0.1-0.8nm"
}
```

**Fields:**
- `time_tag`: ISO 8601 timestamp (UTC)
- `satellite`: GOES satellite number (16, 18, 19)
- `flux`: Corrected X-ray flux (W/m²)
- `observed_flux`: Raw measured flux (W/m²)
- `electron_correction`: Electron contamination correction applied (W/m²)
- `electron_contaminaton`: Boolean flag for electron interference
- `energy`: Energy band ("0.05-0.4nm" or "0.1-0.8nm")

**Key model**: `{satellite}/{energy}` (e.g., "18/0.1-0.8nm") — stable combination for time-series partitioning.

**Volume**: ~2 records/minute (2 energy bands), ~2,880 events/day.

## Schema / Sample

```json
{
  "time_tag": "2026-05-23T07:47:00Z",
  "satellite": 18,
  "flux": 1.0694394632082549E-06,
  "observed_flux": 1.085674171008577E-06,
  "electron_correction": 1.623471135303589E-08,
  "electron_contaminaton": false,
  "energy": "0.1-0.8nm"
}
```

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3/3 | Critical for space weather forecasting; drives flare alerts |
| Freshness | 3/3 | 1-minute cadence, updated continuously |
| Openness | 3/3 | No auth, no rate limits, stable NOAA endpoint |
| Schema Clarity | 3/3 | Clean JSON, well-documented fields, stable structure |
| Machine-Readability | 3/3 | JSON array, straightforward parsing |
| Repo Fit | 2/3 | Space weather domain already present (noaa-goes for K-index), but X-ray flux is distinct product |

**Total: 17/18**

- Scientifically significant: solar flare detection is the primary driver of space weather alerts
- Operational value: used by satellite operators, airlines, grid operators
- Stable entity model: satellite + energy band keying is clean
- High-quality JSON with metadata (corrections, flags)
- 1-minute temporal resolution is excellent for event detection
- No authentication required
- Currently **not covered** by existing `noaa-goes` bridge (that one has K-index, solar wind, and alerts — but not X-ray flux time series)

## Limitations

- Data is 7-day rolling window (historical archive requires NCEI queries)
- Electron contamination affects short-band measurements during certain satellite orientations
- Satellite assignments change over time (GOES-16 was decommissioned, GOES-19 became operational)
- No real-time alert correlation in the JSON (alerts are separate endpoint)
- Scientific unit (W/m²) requires context for interpretation (A/B/C/M/X flare classification)

## Verdict

**RECOMMEND** — High-value space weather product with 1-minute cadence, clean JSON, stable keying, and zero auth barriers. Fills gap in current `noaa-goes` bridge which focuses on geomagnetic indices and alerts but lacks the X-ray flux time series. X-ray data is the **primary observable** for solar flares and should be bridged. Polled endpoint; simple HTTP GET every 60 seconds with delta detection.
