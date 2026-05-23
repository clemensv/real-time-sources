# ESA Sentinel-3 Ocean Color / Sea Surface Temperature NRT

- **Country/Region**: Global oceans
- **Endpoint**: https://dataspace.copernicus.eu/odata/v1/Products
- **Protocol**: OData / STAC
- **Auth**: OAuth (free CDSE)
- **Format**: NetCDF
- **Freshness**: 3-hour NRT
- **Score**: 12/18

## Overview

Sentinel-3 (S3A, S3B) carries OLCI (Ocean and Land Colour Instrument) and SLSTR (Sea and Land
Surface Temperature Radiometer):

- **OLCI L2 water products** — chlorophyll-a, TSM (total suspended matter), ocean color (3-hour NRT)
- **SLSTR L2 SST** — Sea Surface Temperature (3-hour NRT)
- **300m spatial resolution** (OLCI), 1km (SLSTR SST)

NRT products support:
- Harmful algal bloom detection
- Ocean productivity monitoring
- Marine heatwave tracking
- Coastal water quality

## Verdict

⚠️ **Maybe** — Same **granule-notification pattern** as Sentinel-5P/2. Each granule covers large
ocean swaths (1,200 × 3,000 km). Not station-based.

| Criterion | Score |
|-----------|-------|
| Value | 3 |
| Freshness | 2 (3-hour NRT) |
| Openness | 2 |
| Schema | 3 (NetCDF CF) |
| Machine-readability | 2 |
| Repo fit | 0 (orbital swath, grid data) |

**Total: 12/18** — Build as notification if satellite granule pattern is adopted. Otherwise **skip**.
