# open.africa — Pan-African Open Data Platform

- **Country/Region**: Pan-African (54 countries)
- **Endpoint**: `https://africaopendata.org/api/3/action/package_search?q={query}&rows=10`
- **Protocol**: REST (CKAN API)
- **Auth**: None
- **Format**: JSON (CKAN standard), datasets in CSV/JSON/XML
- **Freshness**: Varies by dataset (some regularly updated, many static)
- **Docs**: https://docs.ckan.org/en/latest/api/
- **Score**: 11/18

## Overview

open.africa (africaopendata.org) is the continent's largest open data aggregation
platform, built on CKAN. It harvests datasets from national portals, NGOs, research
institutions, and international organizations across Africa.

The platform contains 198 results for "real-time" queries, spanning transport, health,
economy, agriculture, and environmental domains. While most datasets are static,
the platform provides a unified discovery layer for African open data.

## Endpoint Analysis

**Verified live** — the CKAN API returns structured JSON:

```
GET https://africaopendata.org/api/3/action/package_search?q=real-time&rows=5
```

Returns:
```json
{
  "success": true,
  "result": {
    "count": 198,
    "results": [
      {
        "title": "Database Commuting Time",
        "notes": "National Household Travel Survey...",
        "organization": "Code for South Africa",
        "resources": [
          {"format": "CSV", "url": "..."},
          {"format": "JSON", "url": "..."},
          {"format": "XML", "url": "..."}
        ]
      }
    ]
  }
}
```

Key CKAN API endpoints:
| Endpoint | Description |
|---|---|
| `/api/3/action/package_search?q=` | Search datasets |
| `/api/3/action/package_show?id=` | Get dataset details |
| `/api/3/action/organization_list` | List organizations |
| `/api/3/action/tag_list` | List tags |
| `/api/3/action/group_list` | List groups/categories |

Useful queries for real-time candidates:
- `q=weather+africa`
- `q=electricity+grid`
- `q=transport+real-time`
- `q=water+level`
- `q=air+quality`

## Integration Notes

- **Discovery platform**: Use open.africa as a discovery tool to find new African data
  sources. The CKAN API makes this automatable.
- **Harvest sources**: Many datasets are harvested from original portals (Code for South
  Africa, Kenya Open Data, etc.). Follow the source URLs for the most current data.
- **Quality varies**: Datasets range from well-maintained government statistics to
  stale one-off uploads. Check `metadata_modified` dates.
- **CKAN standard**: The API follows CKAN conventions, making it compatible with any
  CKAN client library.
- **Periodic scanning**: Set up a periodic scan for new African datasets with real-time
  characteristics. This is meta-research tooling.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Varies, mostly static datasets |
| Openness | 3 | No auth, CKAN standard API |
| Stability | 2 | NGO-maintained platform |
| Structure | 3 | CKAN standard JSON API |
| Identifiers | 1 | CKAN dataset IDs |
| Richness | 1 | Meta-platform, quality varies |
