# Oman National Centre for Statistics & Information (data.gov.om)

- **Country/Region**: Sultanate of Oman
- **Endpoint**: `https://data.gov.om` (Knoema-based portal)
- **Protocol**: Web portal (Knoema API possibly available with registration)
- **Auth**: None for public portal access
- **Format**: CSV, Excel downloads; potentially JSON via Knoema API
- **Freshness**: Varies by dataset (mostly monthly/quarterly/annual statistics; unclear if any real-time feeds)
- **Docs**: https://data.gov.om
- **Score**: 4/18 (estimated; needs dataset exploration)

## Overview

The **National Centre for Statistics and Information (NCSI)** operates **data.gov.om**, Oman's official open data portal. The portal is built on the **Knoema** platform (a commercial data aggregation and visualization service now owned by S&P Global) and hosts datasets from multiple Omani government entities.

Typical data domains in national open data portals include:
- **Demographics and census** (population, households)
- **Economic indicators** (GDP, inflation, trade)
- **Health statistics** (hospitals, disease surveillance)
- **Education** (schools, enrollment)
- **Transport** (vehicle registrations, accidents, potentially traffic counts)
- **Energy** (electricity consumption, potentially generation)
- **Environment** (emissions, potentially air quality or water quality)
- **Agriculture** (crop production, livestock)

For a **real-time data bridge**, the relevant question is: **Does data.gov.om host any datasets with sub-daily update frequencies?** National statistical portals typically focus on **monthly, quarterly, or annual aggregates** (batch data), not real-time sensor feeds. However, some portals do publish:
- Real-time air quality (from environment ministries)
- Hourly electricity demand (from grid operators)
- Daily water reservoir levels (from water authorities)
- Traffic incident logs (from police or transport ministries)

These would be the target datasets if present.

## Endpoint Analysis

**Portal accessible but dataset enumeration needed** — the data.gov.om homepage loaded successfully during testing (2026-05-23), showing a Knoema-based interface with:
- Data by topics (categories)
- Visualization of the day (dashboard)
- Key indicators (economic/social metrics)

However, the **specific datasets** available were not explored during initial discovery. To assess real-time data potential, the following steps are needed:

1. **Browse the data catalog** at `https://data.gov.om/en-us/pages/data-catalog` or similar
2. **Identify datasets with update frequencies of daily or higher** (hourly, sub-hourly, real-time)
3. **Check for API access** — Knoema platforms sometimes provide RESTful APIs for dataset queries (e.g., `https://data.gov.om/api/1.0/data/...`) but API documentation may be behind registration or not publicly advertised

### Potential High-Value Datasets (if they exist):
- **Air quality monitoring** (hourly PM2.5, PM10, O₃, NO₂ from Environment Authority stations)
- **Electricity grid demand** (5-minute or hourly load from OETC or Mazoon/Nama Power)
- **Water reservoir levels** (daily or weekly from Ministry of Agriculture/Water Resources)
- **Traffic incidents or flow counts** (real-time from Royal Oman Police or municipalities)
- **Port vessel arrivals** (daily berth occupancy from Salalah, Sohar, Duqm ports)
- **Health surveillance** (daily disease case counts from Ministry of Health)

Most national statistical portals do **not** host real-time sensor data — that typically lives on domain-specific portals (e.g., environment authority for air quality, grid operator for electricity, met service for weather). data.gov.om is likely a **statistical aggregation portal** rather than a real-time telemetry platform.

## Integration Notes

- **Knoema API**: If the portal uses standard Knoema infrastructure, it may support API queries like:
  ```
  GET https://data.gov.om/api/1.0/data/{dataset_id}?time={date_range}&region={filter}
  ```
  However, Knoema API access is often gated by:
  - User registration (free account)
  - API rate limits (requests per day)
  - Some datasets restricted to authenticated users or paid tiers
  
  Public documentation of the Knoema API for data.gov.om was not found during initial discovery.

- **Overlap with domain-specific sources**: If data.gov.om does host real-time datasets (e.g., air quality), those same datasets may also be available from the **originating agency** (e.g., Environment Authority direct API). In general, it's better to bridge the **primary source** (domain agency) rather than an aggregator portal, because:
  - Primary sources update faster (no aggregation lag)
  - Primary sources have stable schemas (aggregators may reformat or sample data)
  - Primary sources are authoritative (aggregators may introduce errors or delays)

- **Additive value**: Without exploring the catalog, it's unclear whether data.gov.om offers any datasets **not available from other Oman sources**. It may be a **discovery tool** (catalog of available datasets) rather than a bridge target itself.

- **Next steps for assessment**:
  1. Visit https://data.gov.om and browse "Data Catalog" or "Datasets" section
  2. Filter by update frequency: "Daily", "Hourly", "Real-time"
  3. Identify any datasets matching the repo's freshness criteria (higher than daily)
  4. Check each dataset for:
     - Download format (CSV vs. API)
     - Stable identifiers (station IDs, sensor codes, etc.)
     - Primary source attribution (which ministry/agency publishes it?)
  5. If a real-time dataset is found, investigate whether the **primary agency** (e.g., Environment Authority) has a direct API that bypasses the aggregator portal

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Unknown; national statistical portals typically monthly/quarterly (daily at best) |
| Openness | 2 | Public portal access, but API access may require registration; Knoema may have rate limits |
| Stability | 2 | Knoema is a commercial platform (stable infrastructure), but portal-specific config can change |
| Structure | 0 | Unknown; likely CSV/Excel downloads, possibly JSON API if Knoema API is enabled |
| Identifiers | 0 | Unknown; depends on datasets |
| Additive value | 0 | Unknown; national portals typically aggregate existing agency data, not primary sources |

**Verdict**: ⚠️ Maybe

**Rationale**: data.gov.om is Oman's official open data portal and **could** host real-time datasets from government agencies, but **dataset catalog exploration is required** to confirm. National statistical portals typically focus on monthly/quarterly/annual aggregates (batch, not real-time), but exceptions exist (e.g., some portals publish daily traffic counts, hourly electricity demand, or real-time air quality if the originating agency provides it).

**Recommended next steps**:
1. **Manually browse the data.gov.om catalog** to identify any datasets with update frequencies of daily or higher.
2. If real-time or near-real-time datasets are found (e.g., air quality, electricity, water, traffic), **check the dataset's metadata for the primary source** (which Omani agency publishes it).
3. **Investigate the primary agency's own website** for a direct API. If the agency has a real-time API, bridge that source directly rather than scraping CSV downloads from the aggregator portal.
4. If data.gov.om provides a **Knoema API** for structured queries (JSON), test the API and check rate limits, authentication requirements, and schema stability.

**If real-time datasets with stable APIs are found, upgrade to ✅ Build. If only batch data (monthly/quarterly), downgrade to ❌ Skip.**

**Low priority for immediate discovery** — focus on domain-specific sources (met service, seismic network, ports, electricity grid operators) before returning to this aggregator portal.
