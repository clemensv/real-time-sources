# ESA Sentinel-2 Near-Real-Time Imagery

- **Country/Region**: Global
- **Endpoint**: https://dataspace.copernicus.eu/odata/v1/Products (CDSE)
- **Protocol**: OData / STAC API
- **Auth**: OAuth (free CDSE account)
- **Format**: JPEG2000 (L1C), GeoTIFF (L2A), SAFE archives
- **Freshness**: 2–6 hours latency (NRT publications)
- **Docs**: https://documentation.dataspace.copernicus.eu/
- **Score**: 12/18

## Overview

Sentinel-2 is ESA's high-resolution optical Earth observation mission (2 satellites: S2A, S2B).
Delivers **10m multispectral imagery** with 5-day global revisit:

- **L1C** — Top-of-atmosphere reflectance (raw radiance calibrated to reflectance)
- **L2A** — Bottom-of-atmosphere reflectance (atmospherically corrected, cloud/shadow masked)
- **13 spectral bands** — Visible, NIR, SWIR (10m, 20m, 60m resolution)

Use cases: agriculture (crop health, NDVI), land cover change, urban monitoring, disaster response.

**NRT publication**: Granules published 2–6 hours after acquisition.

## Verdict

⚠️ **Maybe** — Sentinel-2 imagery is **100+ MB per granule** (100×100 km tiles). Not suitable
for inline Kafka streaming. Better as **granule-notification events** (similar to Sentinel-5P pattern):

- Event per new tile publication (subject: `satellite/sentinel-2/{tile_id}`)
- Payload: tile metadata + S3 download URL
- Consumers fetch imagery from CDSE S3

| Criterion | Score |
|-----------|-------|
| Value | 3 (global high-res optical imagery) |
| Freshness | 2 (2–6 hour NRT) |
| Openness | 2 (OAuth required) |
| Schema | 2 (STAC metadata, JPEG2000 imagery) |
| Machine-readability | 2 (STAC API, OData) |
| Repo fit | 1 (tile grid, not station-based; bulk imagery) |

**Total: 12/18** — Build as **granule-notification pattern** if repo adopts satellite data model.
