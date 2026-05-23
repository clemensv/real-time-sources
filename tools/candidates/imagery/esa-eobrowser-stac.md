# Copernicus Browser STAC Search

- **Country/Region**: Global
- **Endpoint**: https://browser.dataspace.copernicus.eu/stac
- **Protocol**: STAC API
- **Auth**: None (search), OAuth (download)
- **Format**: JSON (STAC), imagery via download
- **Freshness**: Same as CDSE (hours to days depending on product)
- **Score**: 11/18

## Overview

**EO Browser** (https://browser.dataspace.copernicus.eu/) is the user-friendly interface to
Copernicus Data Space Ecosystem. It provides:

- **STAC API** endpoint for searching all Sentinel missions
- **Visual interface** for browsing imagery
- **Time-lapse creation**
- **Scripting layer** for custom image processing

The **STAC API** is the machine-readable entry point:

```
GET https://browser.dataspace.copernicus.eu/stac/search
POST with filters (spatial, temporal, collection)
```

## Verdict

⏭️ **Reference** — EO Browser STAC is a **discovery tool** for Copernicus imagery, but the
underlying data is the same as **CDSE OData/STAC** already covered (Sentinel-1/2/3/5P).
**Redundant** — use CDSE directly.

| Criterion | Score |
|-----------|-------|
| Value | 2 (discovery interface) |
| Freshness | 2 |
| Openness | 2 |
| Schema | 3 (STAC standard) |
| Machine-readability | 3 |
| Repo fit | -1 (same as CDSE, redundant) |

**Total: 11/18** — **Skip**. Use CDSE OData/STAC instead (same backend).
