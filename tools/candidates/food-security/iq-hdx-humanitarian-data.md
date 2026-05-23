# HDX (Humanitarian Data Exchange) - Iraq Datasets

- **Country/Region**: Iraq
- **Endpoint**: `https://data.humdata.org/api/3/action/package_search?q=iraq`
- **Protocol**: CKAN API (HTTP REST)
- **Auth**: None for read access
- **Format**: JSON (API), various data formats (CSV, GeoJSON, Shapefile, Excel)
- **Freshness**: Varies by dataset (most are batch/static, some updated weekly/monthly)
- **Docs**: https://data.humdata.org/api/3/
- **Score**: 6/18 (for API); individual datasets vary

## Overview

The Humanitarian Data Exchange (HDX) is a data platform managed by OCHA (UN Office for the Coordination of Humanitarian Affairs). It aggregates humanitarian datasets from UN agencies, NGOs, and governments for crisis response.

For Iraq, HDX hosts datasets on:
- **Displacement** — IOM DTM (Displacement Tracking Matrix) monthly reports on IDPs and returnees
- **Subnational administrative boundaries** — COD-AB (Common Operational Datasets)
- **Conflict events** — ACLED (Armed Conflict Location & Event Data Project)
- **Population** — census estimates, density grids
- **Health facilities** — hospital and clinic locations
- **Refugee statistics** — UNHCR monthly reports
- **Food security** — WFP and FAO assessments

Most HDX datasets for Iraq are **batch updates** (weekly, monthly, or quarterly), **not real-time**.

## Endpoint Analysis

**CKAN API verified** — HDX uses the CKAN open data platform API.

Sample query:
```
GET https://data.humdata.org/api/3/action/package_search?q=iraq&rows=5
```

Response includes dataset metadata:
```json
{
  "success": true,
  "result": {
    "count": 247,
    "results": [{
      "name": "cod-ab-irq",
      "title": "Iraq - Subnational Administrative Boundaries",
      "organization": {
        "name": "ocha-fiss",
        "title": "OCHA Field Information Services Section (FISS)"
      },
      "maintainer": "ocha-fis-data@un.org",
      "data_update_frequency": "365",
      "resources": [...]
    }]
  }
}
```

Key metadata fields:
- `data_update_frequency` — days between updates (365 = annual, 30 = monthly, 7 = weekly)
- `resources` — array of downloadable files (CSV, GeoJSON, XLSX, etc.)

## Datasets Relevant to Iraq

Checked for real-time or near-real-time candidates:

1. **IOM DTM (Displacement Tracking Matrix)** — monthly updates on IDP movements
   - Freshness: Monthly (not real-time)
   - Last update: varies by governorate
   
2. **ACLED conflict events** — requires ACLED API key, not available via HDX in real-time
   
3. **UNHCR refugee statistics** — monthly Excel reports
   - Freshness: Monthly
   
4. **WFP food prices** — monthly market price surveys
   - Freshness: Monthly
   
5. **WHO health facility status** — quarterly updates
   - Freshness: Quarterly

**None of these are real-time.** HDX is a **batch data repository**, not a real-time event stream platform.

## Real-Time Potential

HDX does not host real-time data streams. However:
- **CKAN API can be polled** to detect when datasets are updated (check `metadata_modified` timestamp)
- For a **batch monitoring bridge**, HDX could work: poll for new versions of monthly IDP reports or conflict datasets and emit change events
- But this is **not real-time telemetry** — it's batch file update notification

## Alternative: Direct Agency APIs

For real-time Iraq humanitarian data, go to source agencies:
- **IOM DTM** — https://dtm.iom.int/ (site blocks API access)
- **ACLED** — https://acleddata.com/data-export-tool/ (requires paid API key for real-time)
- **ReliefWeb** — https://api.reliefweb.int/ (humanitarian news/alerts API, checked separately)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Monthly/quarterly batch updates, not real-time |
| Openness | 3 | CKAN API, no auth for read |
| Stability | 2 | OCHA operational, but no formal SLA |
| Structure | 2 | JSON API for metadata, datasets vary (CSV/GeoJSON/XLSX) |
| Identifiers | 1 | Dataset slugs stable, but data within files often lacks IDs |
| Richness | 1 | Metadata-rich, but datasets are static files not event streams |

**Verdict**: ❌ **Skip for real-time bridging** — HDX is a batch data repository, not a real-time stream platform. Iraq datasets are mostly monthly/quarterly updates. The CKAN API could support a **batch file monitor bridge** (poll for dataset updates and emit change events), but that's a different pattern from real-time telemetry. For Iraq discovery, note that HDX aggregates humanitarian data but does not offer real-time feeds. Direct agency APIs (IOM, ACLED, ReliefWeb) are better targets, though most also have batch cadences or paywalls.
