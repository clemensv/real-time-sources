# BOM Water Storage Dashboard (Australia)

**Country/Region**: Australia (all states and territories)
**Publisher**: Bureau of Meteorology (BOM), Australian Government
**API Endpoint**: `https://www.bom.gov.au/water/dashboards/#/water-storages` (web dashboard)
**Documentation**: https://www.bom.gov.au/water/dashboards/
**Protocol**: Web application (JavaScript SPA with internal JSON API)
**Auth**: None for the dashboard; BOM Water Data Online (Kisters WISKI) services may have terms
**Data Format**: JSON (internal API), presented via web dashboard
**Update Frequency**: Daily to weekly
**License**: CC BY 3.0 AU

## What It Provides

BOM's Water Storage Dashboard provides comprehensive status of major water storages (reservoirs, dams) across all Australian states and territories. It tracks:

- **Current storage volume** (ML — megalitres) and **percentage full**
- **Historical storage trends** (multi-year charts)
- **Storage capacity** for each dam/reservoir
- **Grouped views** by state, city supply system, or river basin

Major storages covered include: Warragamba Dam (Sydney), Thomson Reservoir (Melbourne), Wivenhoe Dam (Brisbane), Mount Bold Reservoir (Adelaide), Mundaring Weir (Perth), Darwin River Dam, and hundreds more.

## API Details

The dashboard is a JavaScript SPA (AngularJS-based) that loads data from internal BOM API endpoints. The main water data infrastructure uses **Kisters WISKI** (Water Information System Kisters):

**Water Data Online API** (Kisters KiWIS):
```
https://www.bom.gov.au/waterdata/services?service=kisters&type=queryServices&request=getStationList&datasource=0&format=json&returnfields=station_name,station_no&parametertype_name=Storage+Volume
```

However, testing showed that storage-related queries via the Kisters API returned empty result sets. The dashboard likely uses a separate internal API not publicly documented.

The dashboard's internal API endpoints (observable via browser network inspection) serve JSON data for:
- State-level storage summaries
- Individual storage details
- Time-series storage percentage data

These internal endpoints are not officially documented or guaranteed stable.

## Freshness Assessment

Good for the dashboard (daily/weekly updates of storage levels). However, the lack of a publicly documented API for the storage data specifically is a significant limitation. The BOM Water Data Online (Kisters) system is oriented more toward river flow/level data.

## Entity Model

- **Storage**: name, state, river basin, capacity (ML), current volume (ML), percentage full
- **Supply System**: group of storages serving a city/region (e.g., "Sydney Water Supply")
- **TimeSeries**: date, storage volume, percentage full

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily/weekly updates |
| Openness | 2 | Dashboard is public; underlying API is undocumented |
| Stability | 3 | Government-operated, critical water management infrastructure |
| Structure | 1 | SPA dashboard; Kisters API exists but storage queries return empty; internal API undocumented |
| Identifiers | 2 | BOM station numbers; some cross-refs to state water agency IDs |
| Additive Value | 3 | Comprehensive national Australian water storage data in one place |
| **Total** | **13/18** | |

## Notes

- The dashboard itself is excellent — comprehensive, well-designed, and covers all major Australian storages. The problem is programmatic access.
- BOM's Kisters WISKI system is the underlying data platform, but the specific parameter type names and time series names for storage data are not well-documented.
- It may be worth investigating the BOM's Water Regulations data reporting — water storage operators are required to report to BOM under the Water Act 2007, and this data may be accessible through different endpoints.
- For individual state-level data, state water agencies (WaterNSW, Melbourne Water, etc.) may provide better-documented APIs.
- The CC BY 3.0 AU license covers BOM data generally, which is positive for reuse.
