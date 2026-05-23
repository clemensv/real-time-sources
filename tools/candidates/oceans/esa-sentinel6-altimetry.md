# ESA Sentinel-6 Michael Freilich Sea Level NRT

- **Country/Region**: Global oceans
- **Endpoint**: https://dataspace.copernicus.eu/odata/v1/Products
- **Protocol**: OData / STAC
- **Auth**: OAuth
- **Format**: NetCDF
- **Freshness**: 3-6 hour NRT
- **Score**: 11/18

## Overview

Sentinel-6 (launched 2020, continuing Jason series) measures **global sea level** via radar altimetry:

- **NRT products**: 3–6 hour latency
- **Sea surface height anomaly** (cm) relative to mean sea level
- **Significant wave height** (m)
- **Wind speed** (m/s)
- **Geophysical corrections** applied (tides, atmospheric pressure, wet troposphere)

Sentinel-6 flies the same orbit as Jason-3 for climate continuity.

## Verdict

⏭️ **Reference** — Altimetry provides **along-track point measurements** (~6 km spacing along
satellite ground track). Not a station network or grid. Each orbit delivers ~10,000 measurements
globally. Better suited to scientific archives (AVISO, NASA PO.DAAC) than real-time streaming.

| Criterion | Score |
|-----------|-------|
| Value | 3 (sea level rise, climate monitoring) |
| Freshness | 2 (3–6 hour NRT) |
| Openness | 2 |
| Schema | 3 |
| Machine-readability | 2 |
| Repo fit | -1 (orbital along-track, no stable station IDs) |

**Total: 11/18** — **Skip**. Orbital geometry doesn't fit repo model. Use **tide gauge networks**
(IOC SLSMF, NOAA CO-OPS) instead for station-based sea level.
