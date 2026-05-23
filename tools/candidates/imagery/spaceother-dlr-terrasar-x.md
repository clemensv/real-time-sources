# DLR TerraSAR-X / TanDEM-X (Germany X-Band SAR)

- **Country/Region**: Global (Germany-operated)
- **Endpoint**: `https://eoweb.dlr.de/` (EOC Geoservice), commercial via Airbus
- **Protocol**: WMS, WCS, Catalog API
- **Auth**: Academic/research proposals (free for science), commercial licenses (paid)
- **Format**: GeoTIFF, HDF5, COSAR (DLR format)
- **Freshness**: Hours to days (operational mission, science tasking priority)
- **Docs**: https://www.dlr.de/en/eoc/missions-projects/terrasar-x
- **Score**: 9/18

## Overview

TerraSAR-X (TSX, launched 2007) and TanDEM-X (TDX, launched 2010) are **Germany's X-band SAR satellites** (9.6 GHz) providing **1m resolution** (spotlight mode) to **18m resolution** (ScanSAR). TanDEM-X flies in close formation with TerraSAR-X for **bistatic interferometry** (single-pass InSAR for DEM generation).

The constellation is operated by **DLR (German Aerospace Center)** with **Airbus Defence and Space** as the commercial data distributor.

**Data access tiers**:
- **Scientific use** — Free via **proposal-based access** (DLR Earth Observation Center, ~2-4 week approval)
- **Commercial use** — Paid licenses via **Airbus (Geostore)** (expensive, enterprise pricing)
- **Public archive** — **Limited open data** (sample scenes, DEM products)

**Open products**:
- **TanDEM-X DEM** — Global 12m/30m/90m digital elevation models (static, not NRT)
- **Sample scenes** — Urban areas, disaster sites (limited coverage)

**Restricted products** (commercial or scientific proposal):
- **Raw SAR imagery** (SLC, MGD, GEC)
- **InSAR pairs** (TanDEM-X bistatic)
- **Emergency tasking** (disasters, rapid response)

## Endpoint Analysis

**EOC Geoservice verified** — `https://geoservice.dlr.de/` provides WMS/WCS for **TanDEM-X DEM** and sample scenes.

However:
- **No STAC** — Custom catalog, WMS/WCS only
- **No NRT SAR imagery** — Raw scenes require proposal or commercial license
- **DEM is static** — Global DEM is a **one-time product** (2010-2015 acquisition), not updated
- **Sample scenes sparse** — ~100 scenes globally (not continuous monitoring)

**Airbus Geostore** (commercial) — `https://www.intelligence-airbusds.com/geostore/` provides search + order API, but requires enterprise subscription.

## Why Strong (if accessible)

1. **1m X-band SAR** — Finest SAR resolution globally (better than Umbra 25cm in some modes).
2. **Bistatic InSAR** — TanDEM-X formation enables **single-pass DEM** (no temporal decorrelation).
3. **TanDEM-X DEM** — **Global 12m DEM** is highest-resolution open DEM globally (Copernicus DEM 30m is next-best).
4. **Disaster tasking** — DLR activates emergency response for major events (earthquakes, floods, volcanoes).

## Limitations

- **Not open data** — Raw SAR imagery requires **scientific proposal** (free but slow approval) or **commercial license** (expensive).
- **DEM is static** — TanDEM-X DEM is a **historical product** (2010-2015), not NRT.
- **No STAC/API** — WMS/WCS only for DEM, no programmatic SAR catalog.
- **Sample scenes sparse** — ~100 scenes globally (not continuous monitoring).
- **Commercial via Airbus** — Full access requires enterprise subscription (expensive).

## Integration Notes

**Feasible only for TanDEM-X DEM** (static):
1. Download global DEM tiles from `https://geoservice.dlr.de/`
2. Emit one-time catalog to Kafka (static product, no updates)
3. **Not a real-time feed** (DEM is 2010-2015 snapshot)

**Not feasible for NRT SAR imagery** — Requires proposal approval (weeks) or commercial license (expensive). Out of scope for open-data repo.

## Verdict

**CONDITIONAL ACCEPT (TanDEM-X DEM only)** — The **global 12m DEM** is a **high-value static product**, but it's **not real-time** (2010-2015 snapshot). Raw SAR imagery is **restricted** (proposal or commercial license).

**Recommended**:
- **Add TanDEM-X DEM** as a **static baseline product** (one-time ingestion, no polling)
- **Skip raw SAR imagery** (not open data)

**Alternative**: For **open X-band SAR**, use **Umbra** or **Capella** open data (sample scenes). For **continuous SAR**, use **Sentinel-1** (C-band, fully open).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 3 | 1m X-band SAR, bistatic InSAR, global 12m DEM |
| Freshness | 0 | DEM is static (2010-2015), raw SAR requires proposal/license |
| Openness | 1 | DEM is open, raw SAR is restricted (proposal or commercial) |
| Schema clarity | 2 | WMS/WCS for DEM, but no STAC for SAR |
| Machine-readability | 2 | GeoTIFF (DEM), HDF5 (SAR), but no API for SAR |
| Repo fit | 1 | DEM is static (one-time), raw SAR is restricted (not open) |
