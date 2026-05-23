# Saudi Data and AI Authority (SDAIA) - Open Data Portal

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: `https://data.gov.sa` / `https://api.data.gov.sa`
- **Protocol**: REST (assumed, CKAN-like portal)
- **Auth**: Unknown (varies by dataset)
- **Format**: JSON, CSV, Excel (varies by dataset)
- **Freshness**: Varies by dataset (mostly batch, some may be hourly+)
- **Docs**: https://api.data.gov.sa/about-en.html
- **Score**: 8/18

## Overview

The **Saudi Data and AI Authority** (الهيئة السعودية للبيانات والذكاء الاصطناعي, SDAIA) is the central authority for Saudi Arabia's digital transformation under Vision 2030. SDAIA manages:

- **National Data Management Office** (NDMO) — Data governance, standards, sharing
- **National Center for AI** (NCAI) — AI research, deployment
- **Saudi Open Data Platform** — data.gov.sa (government datasets)

**data.gov.sa** is Saudi Arabia's federal open data portal, aggregating datasets from ministries and agencies. The portal launched in 2017 and has been expanded significantly under Vision 2030.

**Comparison with other national portals**:

| Portal | Country | Datasets | API? | Real-time data? |
|--------|---------|----------|------|-----------------|
| **data.gov.sa** | Saudi Arabia | ~500+ | ✅ Yes | ❓ Some |
| data.gov | USA | ~300,000+ | ✅ Yes | ✅ Many |
| data.gouv.fr | France | ~50,000+ | ✅ Yes | ✅ Some |
| data.gov.uk | UK | ~50,000+ | ✅ Yes | ✅ Some |
| data.gov.au | Australia | ~100,000+ | ✅ Yes | ✅ Some |

Saudi Arabia's portal is **smaller** than mature Western portals but is growing rapidly.

## Endpoint Analysis

**Main portal**: `https://data.gov.sa`

The portal provides dataset browsing, search, and downloads. Datasets cover:
- Demographics and population
- Economic indicators
- Health statistics
- Education
- Transportation
- Environment
- Energy
- Government services

**API portal**: `https://api.data.gov.sa`

SDAIA maintains a separate API portal at `https://api.data.gov.sa` with documentation pages:
- `https://api.data.gov.sa/index-ar.html` (Arabic)
- `https://api.data.gov.sa/about-en.html` (English)

**Probe attempt**: The explore agent reported timeouts when trying to access the API portal from the remote environment. The portal **exists** but may be geo-restricted, rate-limited, or temporarily down.

**Likely architecture**: Based on the URL structure and global trends, data.gov.sa likely uses:
- **CKAN** (Comprehensive Knowledge Archive Network) — The open-source data portal platform used by data.gov (US), data.gov.uk, data.gov.au, and 100+ other national portals.
- **REST API** — CKAN exposes a standard REST API at `/api/3/action/` for searching datasets, downloading resources, etc.

**Expected CKAN endpoints** (not yet confirmed):
```
GET https://data.gov.sa/api/3/action/package_list
GET https://data.gov.sa/api/3/action/package_search?q=weather
GET https://data.gov.sa/api/3/action/package_show?id={dataset-id}
```

## Potential Real-Time Datasets

Open data portals typically host **batch datasets** (annual reports, census data, PDFs). However, some modern portals include **live APIs** for real-time data:

**Possible real-time datasets on data.gov.sa**:
1. **NCEC air quality** — If NCEC's 7 AQI stations are exposed
2. **NCM weather observations** — If NCM shares station data
3. **SEC electricity load** — If grid load data is published
4. **SAPTCO bus schedules** — If GTFS feeds exist
5. **Riyadh Metro** — If GTFS-RT is published
6. **Mawani port statistics** — Vessel arrivals (likely batch, not real-time)
7. **Traffic incidents** — Road traffic events from Ministry of Transport
8. **Water quality** — If any continuous monitoring exists

**Batch datasets** (low value for this repo):
- Population statistics
- Economic indicators
- Annual reports
- Geospatial datasets (shapefiles)

## Integration Notes

- **Portal inaccessible during probing**: The API portal timed out, so the full dataset catalog was not retrieved. This could be:
  - **Geo-restriction** (blocking non-Saudi IPs)
  - **Rate limiting** (aggressive WAF)
  - **Temporary downtime**
- **CKAN assumption**: If data.gov.sa uses CKAN, it has a **standard REST API** for searching and downloading datasets programmatically.
- **Dataset-by-dataset evaluation**: Open data portals are **meta-sources** — they aggregate datasets from many agencies. Each dataset must be evaluated individually for freshness, format, and value.
- **Most datasets are batch**: National portals skew toward annual/quarterly datasets (census, budgets, health statistics). Real-time feeds are rare.
- **Unique value**: Saudi-specific datasets (Hajj statistics, oil production, desalination) may be globally unique even if batch.

**Recommended approach**:
1. **Catalog scan**: Use the CKAN API (if accessible) to retrieve the full dataset list.
2. **Filter by update frequency**: Identify datasets marked as "real-time," "hourly," "daily," or "live."
3. **Probe each dataset**: Download sample data to assess format, structure, and identifiers.
4. **Build dataset-specific bridges**: If a high-value real-time dataset exists (e.g., NCEC AQI, SEC load), build a dedicated bridge for it, not a generic data.gov.sa bridge.

**Example workflow**:
```python
# 1. List all datasets
GET https://data.gov.sa/api/3/action/package_list

# 2. Search for weather-related datasets
GET https://data.gov.sa/api/3/action/package_search?q=weather

# 3. Get dataset metadata
GET https://data.gov.sa/api/3/action/package_show?id=ncm-weather-stations

# 4. Download resource (CSV, JSON, etc.)
GET {resource_url}
```

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Varies by dataset; most are batch, some may be hourly+ |
| Openness | 2 | Portal is public; individual datasets may require auth or have licenses |
| Stability | 3 | SDAIA is the national data authority; portal is permanent infrastructure |
| Structure | 2 | Varies by dataset (CSV, JSON, Excel, PDF) |
| Identifiers | 1 | Varies by dataset; many lack stable IDs |
| Additive value | 1 | Portal is a meta-source; real value is in individual datasets |

**Total: 11/18** (average across datasets)  
**Actual: 8/18** (penalized for inaccessible portal and mostly batch data)

**Verdict**: ⏭️ **Reference** — data.gov.sa is a **meta-source** that should be **monitored for real-time datasets**, but is **not a standalone source** to build a bridge for. 

**Recommended action**:
1. **Catalog scan**: Access the portal (from a Saudi IP if needed) and retrieve the full dataset catalog via CKAN API.
2. **Filter for real-time**: Identify datasets with update frequencies of hourly or better.
3. **Build dataset-specific bridges**: If a high-value real-time dataset is found (e.g., NCEC AQI, SEC load, NCM weather), build a dedicated bridge for that **specific dataset**, not a generic portal scraper.
4. **Monitor for new datasets**: Check data.gov.sa quarterly for new real-time feeds (Riyadh Metro, SAPTCO GTFS, etc.).

**Do not build** a generic "data.gov.sa" bridge — instead, use the portal as a **discovery tool** to find specific real-time datasets, then build dedicated bridges for those.

**Priority real-time datasets to search for**:
- NCEC air quality (7 stations)
- SEC electricity load
- NCM weather observations
- Riyadh Metro GTFS-RT
- SAPTCO bus GTFS
- Desalination plant output (SWCC)
- Water network monitoring (NWC)
