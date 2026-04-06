# DSCOVR Real-Time Solar Wind

**Country/Region**: Global (L1 Lagrange point measurements)
**Publisher**: NOAA Space Weather Prediction Center
**API Endpoint**: `https://services.swpc.noaa.gov/products/solar-wind/`
**Documentation**: https://www.swpc.noaa.gov/products/real-time-solar-wind
**Protocol**: REST (JSON)
**Auth**: None
**Data Format**: JSON (arrays of arrays)
**Update Frequency**: ~1 minute (real-time telemetry from L1)
**License**: Public domain (US government)

## What It Provides

DSCOVR (Deep Space Climate Observatory) and its predecessor ACE sit at the L1 Lagrange point — about 1.5 million km sunward of Earth — measuring the solar wind before it hits our magnetosphere. This provides a 15-60 minute warning of incoming space weather. The NOAA SWPC publishes this data as continuously-updated JSON files covering plasma (density, speed, temperature) and magnetic field (Bx, By, Bz, Bt) measurements.

This is the canary in the coal mine for geomagnetic storms. When the Bz component swings strongly negative, you've got about 30 minutes before the aurora starts — and before HF radio propagation goes haywire.

## API Details

- **Plasma 7-day**: `GET /products/solar-wind/plasma-7-day.json` — density (p/cm³), speed (km/s), temperature (K)
- **Mag 7-day**: `GET /products/solar-wind/mag-7-day.json` — Bx, By, Bz (nT), Bt (nT), lat, lon
- **Plasma 2-hour**: `GET /products/solar-wind/plasma-2-hour.json` — higher-resolution recent window
- **Mag 2-hour**: `GET /products/solar-wind/mag-2-hour.json`
- **Plasma 6-hour/1-day**: Also available at corresponding intervals
- **Summary**: `GET /products/summary/solar-wind-speed.json` — single latest value
- **No auth required**: Public JSON endpoints
- **Format**: First row is headers, remaining rows are data `[timestamp, value1, value2, ...]`
- **No rate limit**: Static JSON files updated every minute

## Freshness Assessment

Data points arrive at ~1-minute cadence. The JSON files are regenerated continuously. The 2-hour window files are small and fast to fetch. The summary endpoint returns a single JSON object with the latest speed reading and timestamp.

Confirmed live: plasma data showed entries up to 2026-04-06 11:14:00 (within 3 minutes of query), with solar wind speed at 518-553 km/s. Magnetic field data confirmed with Bz at -4.95 nT. Summary endpoint returned speed=543 km/s at 11:15:00 UTC.

## Entity Model

- **Plasma measurement**: `time_tag` (UTC), `density` (p/cm³), `speed` (km/s), `temperature` (K)
- **Magnetic field**: `time_tag`, `bx_gsm`, `by_gsm`, `bz_gsm` (nT in GSM coordinates), `bt` (total field), `lon_gsm`, `lat_gsm`
- **Summary**: Single `proton_speed` value with `time_tag`

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | ~1 minute cadence, data within minutes of measurement at L1 |
| Openness | 3 | No auth, public domain, static JSON files |
| Stability | 3 | NOAA operational infrastructure, mission-critical for space weather forecasting |
| Structure | 2 | Array-of-arrays format (header row + data rows); simple but not self-describing |
| Identifiers | 2 | Timestamps are the primary key; no event IDs |
| Additive Value | 3 | Unique L1 solar wind data — only source for upstream space weather measurements |
| **Total** | **16/18** | |

## Notes

- Confirmed live with three endpoints — plasma, mag, and summary all returning fresh data.
- Solar wind speed was elevated (518-553 km/s; nominal is ~400) during testing, consistent with the active SWPC alert about elevated electron flux.
- The array-of-arrays JSON format is simple but requires positional parsing. First row is always headers.
- Multiple time windows available (2h, 6h, 1d, 3d, 7d) — choose based on polling frequency.
- Pairs beautifully with NOAA DONKI (CME events), NASA GCN (if a CME source is solar), and radio propagation sources (DSCOVR Bz directly predicts HF blackouts).
- The Enlil model animations (`/products/animations/enlil.json`) provide CME arrival predictions — confirmed accessible.
