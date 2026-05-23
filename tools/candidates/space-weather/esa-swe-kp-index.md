# ESA Space Weather Service Network Kp Index

- **Country/Region**: Global
- **Endpoint**: https://swe.ssa.esa.int/kp-index
- **Protocol**: Web portal (HTML), possible API
- **Auth**: Free account likely required
- **Format**: JSON (if API exists), HTML
- **Freshness**: 3-hour Kp (updated every 3 hours)
- **Score**: 10/18

## Overview

ESA SSA (Space Situational Awareness) Space Weather Service Network provides:

- **Kp index** — planetary geomagnetic activity (0–9 scale)
- **Solar wind** — speed, density, Bz (north-south component)
- **Solar flares** — M-class, X-class events
- **Coronal mass ejections (CMEs)**
- **Radiation belt electrons**

The **Kp index** is derived from ground magnetometer networks (INTERMAGNET) and updated every 3 hours.

## Verdict

⏭️ **Reference** — ESA SWE portal is **informational/visual**, not a data API. Kp index is
**already available** from authoritative sources:

- **NOAA SWPC** (Space Weather Prediction Center) — real-time Kp, JSON API
- **GFZ Potsdam** — official Kp calculation center, FTP/HTTP data
- **INTERMAGNET** — raw magnetometer data (1-second)

**Skip** ESA SWE. Use **NOAA SWPC** or **INTERMAGNET** instead (better APIs).

| Criterion | Score |
|-----------|-------|
| Value | 3 |
| Freshness | 2 (3-hour) |
| Openness | 1 (portal, unclear if API) |
| Schema | 1 |
| Machine-readability | 1 |
| Repo fit | 2 (global index, single value every 3h) |

**Total: 10/18** — **Skip**. Redundant with NOAA/GFZ sources.
