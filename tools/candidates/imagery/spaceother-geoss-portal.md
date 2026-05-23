# GEOSS Portal (Group on Earth Observations System of Systems)

- **Country/Region**: Global (multi-agency aggregator)
- **Endpoint**: `https://www.geoportal.org/` (portal), various APIs per data provider
- **Protocol**: Varies (OGC WMS/WCS/WFS, OpenSearch, STAC, proprietary APIs)
- **Auth**: Varies by data provider (mostly free registration)
- **Format**: Varies (GeoTIFF, NetCDF, HDF, JSON, XML)
- **Freshness**: Varies (aggregates NRT and historical sources)
- **Docs**: https://www.earthobservations.org/geoss.php
- **Score**: 6/18

## Overview

GEOSS (Global Earth Observation System of Systems) is a **multi-agency coordination initiative** connecting Earth observation data from **100+ national space agencies, meteorological services, and research institutions** worldwide. The **GEOSS Portal** provides a **federated search** across distributed catalogs, but it is **not a data host** — it redirects users to upstream sources.

GEOSS aggregates:
- Satellite imagery (Sentinel, Landsat, MODIS, national missions)
- Weather/climate data (ECMWF, NOAA, JMA, CMA)
- In-situ observations (WMO stations, ocean buoys, air quality sensors)
- Derived products (land cover, DEM, soil moisture, vegetation indices)

**Key limitation**: GEOSS is a **search portal**, not a **data distribution service**. It indexes metadata from upstream providers and links to their download endpoints. Each provider has **different APIs, auth schemes, and data formats**.

## Endpoint Analysis

**GEOSS Portal verified** — `https://www.geoportal.org/` provides federated search.

However:
- **No unified API** — Each data provider has its own endpoint (ESA, USGS, NOAA, JMA, DLR, CNES, etc.)
- **Metadata-only** — GEOSS does not host data, only links to upstream sources
- **Inconsistent schemas** — No common STAC or OGC standard (each provider uses their own format)
- **No NRT guarantees** — GEOSS indexes both NRT and historical data (latency varies by provider)

**Example search workflow**:
1. User searches GEOSS Portal for "Sentinel-2 over Amazon, last 7 days"
2. Portal queries **Copernicus Data Space**, **AWS Open Data**, **Google Earth Engine** (multiple backends)
3. Portal returns **metadata records** with links to upstream download endpoints
4. User follows link to **Copernicus Data Space STAC API** (or other provider)
5. User authenticates and downloads from **upstream source** (not GEOSS)

**GEOSS acts as a discovery layer**, not a data layer.

## Why Weak

1. **Not a data source** — GEOSS is a **search portal** (metadata aggregator), not a data distribution service.
2. **No unified API** — Each upstream provider has different APIs (STAC, OGC, proprietary).
3. **No NRT guarantees** — Latency depends on upstream sources (GEOSS does not control this).
4. **Inconsistent metadata** — No common schema (each provider uses their own format).
5. **Redundant** — For real-time feeds, **direct integration** with upstream sources (Copernicus, USGS, INPE, NOAA) is better than going through GEOSS intermediary.

## Integration Notes

**Not recommended** — GEOSS adds **no value** for a real-time data repo. Direct integration with upstream sources is better:
- **Sentinel-1/2/3/5P/6** → Copernicus Data Space STAC
- **Landsat** → Element84 Earth Search or USGS LandsatLook
- **MODIS/VIIRS** → NASA Earthdata or Planetary Computer
- **INPE DETER** → TerraBrasilis WFS (direct)

GEOSS is useful for **human users** (web search across multiple catalogs) but **not for automated bridges** (too many upstream APIs to integrate).

## Verdict

**REJECT (not a data source)** — GEOSS is a **metadata aggregator**, not a **data distribution service**. For a real-time data repo, **direct integration** with upstream sources (Copernicus, USGS, INPE, NOAA, CNES) is better.

**Recommended**: Skip GEOSS Portal. Integrate directly with primary sources covered in this research.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 1 | Federated search across 100+ providers, but no unified data access |
| Freshness | 1 | Varies by upstream provider (GEOSS does not control latency) |
| Openness | 1 | Mostly open, but auth varies by provider |
| Schema clarity | 0 | No common schema (each provider uses their own format) |
| Machine-readability | 1 | Varies by provider (STAC, OGC, proprietary APIs) |
| Repo fit | 2 | Metadata-only (not a data source), redundant with direct integration |
