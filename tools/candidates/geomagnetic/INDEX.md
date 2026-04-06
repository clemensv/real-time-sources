# Geomagnetic Candidates

Scouted: 2026-04-06 (Round 1), 2026-04-06 (Round 2 — deep dive)

Real-time and archival geomagnetic field data and activity indices.

| Source | Protocol | Auth | Freshness | Total Score | Status |
|--------|----------|------|-----------|-------------|--------|
| [USGS Geomagnetism](usgs-geomagnetism.md) | REST (JSON) | None | 1-minute | **17/18** | ✅ **Build** |
| [INTERMAGNET](intermagnet.md) | HAPI (REST) | None | Minutes-Hours | 16/18 | ✅ Build |
| [GFZ Kp Index](gfz-kp-index.md) | REST | None | 3-hourly | 16/18 | ✅ Build |
| [NOAA SWPC Geomagnetic](noaa-swpc-geomag.md) | REST | None | 1-minute | 16/18 | ✅ Build |
| [NOAA OVATION Aurora](noaa-ovation-aurora.md) | REST (JSON) | None | 30-minute | **16/18** | ✅ **Build** |
| [SuperMAG](supermag.md) | REST | Free reg. | 1-minute | **15/18** | ⚠️ Maybe |
| [FMI Finland Geomag](fmi-finland-geomag.md) | WFS (XML) | Free API key | 10-second | **14/18** | ⚠️ Maybe |
| [BGS WDC Edinburgh](bgs-wdc-edinburgh.md) | Web portal | None | Hours-Months | **13/18** | ⏭️ Skip |
| [WDC for Geomagnetism](wdc-geomagnetism.md) | HTTP/forms | None | Hours-Months | 11/18 | ⏭️ Skip |

## Summary

The deep dive significantly strengthened this domain. The **USGS Geomagnetism Program** emerged as the highest-scoring candidate across all three domains — a modern REST API with OpenAPI/Swagger documentation, GeoJSON observatory metadata, clean JSON timeseries, 1-minute cadence, and US public domain licensing. It's what every geoscience data API should look like.

**NOAA OVATION Aurora** is a unique product — a global aurora probability forecast on a lat/lon grid, updated every 30 minutes. No equivalent exists elsewhere. High public interest (aurora tourism industry) and zero access friction.

Three strong contenders from Round 1 remain at 16/18 each. NOAA SWPC provides the most comprehensive space weather product suite. INTERMAGNET's HAPI endpoint covers 150+ ground observatories. GFZ's Kp index is the authoritative geomagnetic activity measure.

New Round 2 additions:
- **SuperMAG** (15/18) — 500+ magnetometer stations with unique indices (SME, SML). API exists but requires free registration. Best for detailed space physics analysis.
- **FMI Finland** (14/18) — Real-time magnetometer data from the auroral zone via OGC WFS. Requires free API key. Valuable for Nordic/auroral monitoring.
- **BGS WDC Edinburgh** (13/18) — World Data Centre archive, scientifically important but no working public API. Data accessible through INTERMAGNET.

## Candidates Not Reachable / Dismissed (Round 2)

| Candidate | Reason |
|-----------|--------|
| **NRCan (Canada)** | Website loads but data API returned 404. Plot tools are web-form-based only. |
| **DTU Space (Denmark)** | Website accessible but no public data API found. |
| **Tromsø Geophysical Observatory** | Redirects to `geo.phys.uit.no`; website loads but no data API. Magnetogram images (GIF) but no JSON/CSV. |
| **SuperDARN** | Website accessible; academic collaboration with restricted data access. Radar (not magnetometer) data. |

## Recommended Build Order

1. **USGS Geomagnetism** — Best API in the survey; OpenAPI spec; 1-minute real-time data; public domain
2. **NOAA SWPC** — Broadest product suite; Kp, Dst, GOES, solar wind, alerts — all as static JSON
3. **NOAA OVATION Aurora** — Unique aurora forecast product; could extend NOAA SWPC bridge
4. **INTERMAGNET** — HAPI API for 150+ global observatories; scientific reference
5. **GFZ Kp Index** — Authoritative Kp under CC BY 4.0; NOAA mirrors it, so may be redundant

## Architecture Notes

### Complementary Layers

The geomagnetic sources form a clear hierarchy:

| Layer | Source | What It Provides |
|-------|--------|-----------------|
| **Raw measurements** | USGS Geomagnetism, INTERMAGNET, SuperMAG, FMI | Magnetic field components (H, D, Z, F) at specific observatories |
| **Derived indices** | GFZ Kp, NOAA SWPC Dst, SuperMAG SME | Planetary-scale activity indicators computed from multiple stations |
| **Forecast/nowcast** | NOAA OVATION, NOAA SWPC Scales | Predicted aurora location, geomagnetic storm severity |
| **Alerts** | NOAA SWPC Alerts | Operational warnings for satellite operators, power grid, aviation |

A complete space weather monitoring picture requires at least one source from each layer. The recommended build order covers all four.
