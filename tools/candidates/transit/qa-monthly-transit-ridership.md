# Qatar Public Transport Ridership (Monthly)

- **Country/Region**: Qatar
- **Endpoint**: `https://www.data.gov.qa/api/explore/v2.1/catalog/datasets/public-transport-users/records?limit=24&order_by=date+desc`
- **Protocol**: OpenDataSoft REST / JSON
- **Auth**: None
- **Format**: JSON
- **Freshness**: Monthly (updated each month with previous month's totals)
- **Docs**: https://data.gov.qa (OpenDataSoft platform)
- **Score**: 8/18

## Overview

Qatar's **Ministry of Transport** publishes monthly ridership statistics for all public
transport modes on the national open data portal (data.gov.qa). The dataset covers:
- **Karwa/Mowasalat buses** (public bus network operated by Mowasalat)
- **Doha Metro** (Red, Green, Gold lines — opened 2019 for FIFA 2022)
- **Lusail Tram** (light rail in Lusail City — opened 2019)

**Data fields**:
- `date`: Month (YYYY-MM format)
- `bus`: Number of bus passengers (millions)
- `metro`: Number of Doha Metro passengers (millions)
- `tram`: Number of Lusail Tram passengers (thousands)
- `total`: Total public transport passengers (millions)

**Dataset size**: Historical monthly data from Metro/Tram opening (May 2019) to present.

**Update frequency**: Monthly (data for month N is typically published in month N+1).

## Endpoint Analysis

**Live test successful** — API returned recent ridership data:

```json
{
  "total_count": 85,
  "results": [
    {
      "date": "2026-01",
      "bus": 3.8,
      "metro": 6.1,
      "tram": 133,
      "total": 10.03
    },
    {
      "date": "2025-12",
      "bus": 3.5,
      "metro": 5.9,
      "tram": 125,
      "total": 9.53
    },
    {
      "date": "2025-11",
      "bus": 3.6,
      "metro": 6.0,
      "tram": 128,
      "total": 9.73
    }
  ]
}
```

**Observations**:
- **Metro dominates**: 6.1M riders/month (61% of total) vs 3.8M bus (38%) and 133K tram (1%)
- **Seasonal variation**: Ridership drops in summer (extreme heat, 45-50°C) and peaks in
  winter (comfortable weather, 15-25°C)
- **Tram units**: Tram ridership in thousands, not millions (133K = 0.133M)
- **Growth trend**: Ridership has grown since Metro opening in 2019, stabilized post-pandemic

**Query parameters**:
- `limit`: Number of months returned
- `order_by`: Sort field + direction (e.g., `date desc` for most recent first)
- `where`: SQL-style filter (e.g., `where=metro>5.0` for high Metro ridership months)
- `select`: Field selection
- `group_by`: Aggregation (e.g., annual totals)

**Example queries**:
```
# Last 12 months
GET /records?limit=12&order_by=date+desc

# Months with >10M total riders
GET /records?where=total>10.0&order_by=date+desc

# Annual totals (group by year)
GET /records?select=substring(date,1,4) as year,sum(bus) as bus_annual,sum(metro) as metro_annual&group_by=year
```

## Integration Notes

- **Polling interval**: 30 days (monthly updates; poll once per month, e.g., 5th of each month)
- **CloudEvents subject**: `transit/ridership/{mode}/{month}` or `transit/ridership/total/{month}`
- **Kafka key**: `{date}` → `2026-01` (one event per month)
- **Entity model**: Monthly aggregate time series (not per-trip, per-station, or real-time)
- **License**: CC BY 4.0 (stated on data.gov.qa)
- **Overlap check**: The repo has a **GTFS bridge** for real-time transit (vehicle positions,
  arrival predictions). This dataset is **aggregate monthly totals**, not real-time. It's a
  different granularity and use case.
- **Use case**: High-level transit performance tracking, policy analysis, annual reporting,
  FIFA 2022 legacy infrastructure utilization analysis

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Monthly updates (fails daily threshold) |
| Openness | 3 | No auth, CC BY 4.0, OpenDataSoft standard API |
| Stability | 2 | Government-run portal, stable platform |
| Structure | 2 | Typed JSON with schema |
| Identifiers | 1 | Month identifier (simple but unique) |
| Additive value | 0 | Aggregate data; real-time GTFS-RT is more valuable and not available |

**Verdict**: **Not recommended** due to monthly update frequency (repo threshold is sub-daily).
This dataset is **too coarse** for real-time bridging.

**Why this matters despite low score**:
- **FIFA 2022 legacy infrastructure**: The Doha Metro (Red/Green/Gold lines) and Lusail Tram
  were built for the World Cup. Monthly ridership data is the **only public transit data
  available** for Qatar — there is **no GTFS-RT feed** for real-time vehicle positions or
  arrival predictions.
- **Data gap**: The research agent confirmed that:
  - **Doha Metro GTFS-RT**: Not published (zero Qatar entries in MobilityData global catalog)
  - **Mowasalat GTFS**: Not published (site returns 403; no GTFS registered)
  - **Qatar Rail portal** (qr.com.qa): DNS failure (site unreachable)
- **Implication**: Qatar's modern, FIFA-built transit system **has no public real-time data**.
  Monthly aggregates are the only available indicator.

**Recommendation**: Document this dataset as a **negative finding** — Qatar transit
infrastructure exists but lacks real-time data APIs. Include in final report under "Data
Gaps" or "FIFA 2022 Legacy Infrastructure — Missing Real-Time Feeds."

**Context for FIFA 2022**:
- **Doha Metro**: 3 lines (Red, Green, Gold), 37 stations, opened May 2019 (6 months before
  FIFA deadline), ridership ~6M/month
- **Lusail Tram**: 4 lines, 25 stations, opened Dec 2019, serves Lusail City (FIFA stadiums,
  Lusail Iconic Stadium), ridership ~130K/month
- **Karwa buses**: Expanded network for FIFA 2022, free shuttles during tournament, ridership
  ~3.8M/month
- **Missing**: Real-time vehicle tracking, arrival predictions, occupancy, service alerts —
  all standard GTFS-RT features that were presumably available during FIFA 2022 for
  operational purposes but not published publicly

**Comparison with other countries**:
- **Norway** (digitraffic): Real-time public transport (bus, tram, ferry) via GTFS-RT
- **UK** (TfL Open Data): Real-time bus/tube positions, arrivals, crowding
- **USA** (hundreds of agencies): GTFS + GTFS-RT widely published
- **Qatar**: Modern infrastructure, zero real-time public data

**Possible future development**: If Qatar Rail or Mowasalat publish GTFS-RT in the future,
it would be a **high-value addition** to the repo (FIFA-legacy smart-city infrastructure,
covering a region with minimal existing transit data).
