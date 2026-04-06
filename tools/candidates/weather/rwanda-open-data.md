# Rwanda Open Data Portal

- **Country/Region**: Rwanda
- **Endpoint**: `https://data.gov.rw`
- **Protocol**: REST (Next.js/CKAN-based)
- **Auth**: None (public data portal)
- **Format**: JSON, CSV, Excel
- **Freshness**: Varies by dataset (monthly to annual)
- **Docs**: https://data.gov.rw
- **Score**: 9/18

## Overview

Rwanda is widely recognized as Africa's most digitally progressive government. The
national open data portal at data.gov.rw provides access to government datasets across
sectors including health, agriculture, economy, education, and infrastructure.

While the portal doesn't offer real-time streaming data, it demonstrates Africa's most
mature open data governance framework. The data is structured, well-documented, and
regularly updated.

## Endpoint Analysis

**Verified live** — the portal loads a modern Next.js application (confirmed by page source).
The underlying data platform appears to be a custom "Data Sharing Platform" rather than
standard CKAN.

The portal is expected to expose API endpoints for dataset discovery and download:
```
GET /api/datasets — Dataset catalog
GET /api/datasets/{id} — Individual dataset metadata
GET /api/datasets/{id}/download — Data download
```

Potential real-time or near-real-time datasets:
- Health facility statistics (daily/weekly reporting)
- Agricultural market prices (weekly)
- Economic indicators (monthly)
- Environmental monitoring (potentially real-time)

Rwanda's digital infrastructure (4G coverage >95%, widespread mobile money) suggests
the potential for real-time government data is high, even if current API offerings
are limited.

## Integration Notes

- **Emerging potential**: Rwanda's digital ambitions mean this portal will likely evolve
  toward real-time APIs. Worth monitoring for API improvements.
- **Health data**: Rwanda's health information system (HMIS) is among Africa's most
  mature, with community health workers reporting via mobile devices. If this data
  becomes API-accessible, it's extremely valuable.
- **Weather gap**: Rwanda lacks its own weather API, but TAHMO and Open-Meteo cover
  the country well.
- **Smart city**: Kigali has invested in smart city infrastructure — traffic,
  environmental monitoring, and waste management data may become available.
- **Model for Africa**: Rwanda's approach is being replicated in other African countries.
  Document this as a template for future African data portal integrations.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Monthly to annual updates |
| Openness | 3 | Public portal, no auth |
| Stability | 2 | Government-backed, modern infrastructure |
| Structure | 1 | Web portal, API details unclear |
| Identifiers | 1 | Dataset IDs |
| Richness | 1 | Multi-sector but limited real-time |
