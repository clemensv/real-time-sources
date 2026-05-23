# JAXA P-Tree Himawari SST/Ocean Products

- **Country/Region**: Japan / Asia-Pacific (Himawari-8/9 full disk)
- **Endpoint**: `https://www.eorc.jaxa.jp/ptree/` (Web map interface, no public API detected)
- **Protocol**: Web map tiles (not machine-readable API)
- **Auth**: None (public web viewer)
- **Format**: Rendered map tiles (PNG), not raw data
- **Freshness**: 10 minutes (SST), hourly (aerosol, chlorophyll)
- **Docs**: https://www.eorc.jaxa.jp/ptree/index.html
- **Score**: 5/18

## Overview

The JAXA P-Tree (Physical value Tree) is a web-based visualization platform that displays near-real-time ocean and atmospheric products derived from Himawari-8/9 AHI data. Products include sea surface temperature (SST), chlorophyll-a concentration, aerosol optical thickness, wildfire detection, cloud optical thickness, and short-wave radiation.

The platform uses Himawari AHI imagery as input and generates derived ocean and atmospheric parameters through JAXA algorithms. SST updates every 10 minutes (matching Himawari full-disk cadence), while other products update hourly or daily.

**Critical limitation**: P-Tree is a **web map viewer only** — it renders map tiles for human visualization and does not expose a machine-readable data API. The underlying data is not available for programmatic download.

## Endpoint Analysis

**Web map interface confirmed** — https://www.eorc.jaxa.jp/ptree/index.html loads a JavaScript map viewer showing Himawari-derived products overlaid on background maps.

**No public API detected**:
- No REST endpoint documented
- No OpenAPI/Swagger spec
- No data download links
- No THREDDS/OPeNDAP/ERDDAP catalog
- JavaScript code makes tile requests to internal JAXA servers (likely WMS or proprietary tile service)

**Tile requests** appear to follow a pattern like:
```
https://www.eorc.jaxa.jp/ptree/tiles/{product}/{timestamp}/{z}/{x}/{y}.png
```

But these are rendered PNG tiles, not raw data values. Tile endpoints are likely rate-limited and intended for web map rendering, not programmatic access.

**Products displayed**:
- Sea Surface Temperature (SST) — 10-minute updates, night mode available
- Chlorophyll-a concentration — hourly
- Aerosol Optical Thickness (AOT) — hourly
- Short-wave radiation — daily
- Wild Fire detection — hourly
- Cloud optical thickness — hourly
- Cloud type (ISCCP classification) — hourly
- Ocean weather forecast (JAXA/JAMSTEC collaboration)
- Ocean analysis (JAXA/RIKEN collaboration)

**Time series graph feature**: The web interface allows clicking a point to generate a time-series graph of a product over a selected time window (up to 3 days for 10-minute data, 1 month for daily data). This suggests the underlying data is stored in a time-series database, but there is no public query API.

## Why This Scores Low

1. **No machine-readable API**: P-Tree is a web map viewer, not a data service. Tile endpoints are for rendering, not data access.
2. **No documented data download**: JAXA does not provide a public mechanism to download the raw SST/chlorophyll/AOT grids that P-Tree visualizes.
3. **Scraping map tiles is fragile**: While technically possible to scrape PNG tiles and reverse-engineer pixel values, this violates the intended use and is brittle (no schema, no stable tile coordinate system, rate limits unknown).
4. **Data may be available elsewhere**: Some P-Tree products (e.g., SST, chlorophyll) may be published through G-Portal or other JAXA data systems, but not in near-real-time.

## Verdict

**❌ Skip** — P-Tree is not a viable candidate for a real-time data bridge. It is a visualization tool, not a data API. The rendered map tiles are unsuitable for machine ingestion.

**Alternative path**: If the underlying SST/chlorophyll/AOT products are published through G-Portal (JAXA's data portal) or JAXA FTP servers in near-real-time, those would be better candidates. Investigate:
1. G-Portal (https://gportal.jaxa.jp) — requires registration, primarily archive data
2. JAXA EORC data servers — may have FTP or HTTP download for specific products
3. Himawari L2 products on AWS (checked earlier: `AHI-L2-FLDK-ISatSS` exists for SST) — this is the better entry point

**Recommendation**: Pursue Himawari L2 SST product from the AWS S3 mirror (`noaa-himawari9/AHI-L2-FLDK-ISatSS/`) instead of P-Tree web tiles.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Value | 2 | SST, chlorophyll, AOT are valuable ocean/atmospheric parameters |
| Freshness | 2 | 10-minute SST, hourly other products — good cadence |
| Openness | 0 | No public data API, web map viewer only |
| Schema Clarity | 0 | Rendered PNG tiles, no structured data schema |
| Machine-Readability | 0 | Not machine-readable — map tiles for human consumption |
| Repo-Fit | 1 | Domain fit (ocean/atmosphere), but not bridgeable without a data API |

**Score: 5/18** — Not viable. Pursue Himawari L2 products on AWS instead.
