# Seattle Street Closures (SDOT)

- **Country/Region**: US — Seattle, WA
- **Publisher**: City of Seattle / Seattle Department of Transportation (SDOT)
- **Endpoint**: `https://data.seattle.gov/resource/ium9-iqtc.json`
- **Protocol**: REST (Socrata SODA API)
- **Auth**: None (app token optional)
- **Format**: JSON, CSV, XML, GeoJSON
- **Freshness**: Near real-time (updated as permits are issued/modified)
- **Docs**: https://data.seattle.gov/Built-Environment/Street-Closures/ium9-iqtc
- **Score**: 13/18

## Overview

The City of Seattle publishes street closure data through its open data portal. This dataset includes construction closures, special events (block parties, parades), utility work, and other right-of-way impacts. For a free-time advisor, this data helps route users around closures and alerts them to events (block parties, festivals) that may themselves be recreational opportunities.

## API Details

**Base URL:** `https://data.seattle.gov/resource/ium9-iqtc.json`

**SODA Query Examples:**

| Query | URL |
|-------|-----|
| Active closures today | `?$where=start_date <= '2024-01-15' AND end_date >= '2024-01-15'` |
| Recent closures | `?$order=start_date DESC&$limit=20` |
| By type | `?$where=permit_type='Construction'` |
| By street | `?$where=street_on like '%PIKE%'` |

**Key Fields:**
- `permit_number` — Unique identifier
- `permit_type` — "Construction", "Play Street", "Special Event", "Utility"
- `project_name` — Description of closure
- `project_description` — Detailed description
- `start_date` / `end_date` — Closure period
- `street_on` — Affected street
- Day-of-week fields: `monday`, `tuesday`, etc. — Hours for each day

**Verified Response:**
```json
[
  {
    "permit_number": "SUFUN0006067",
    "permit_type": "Play Street",
    "project_name": "Block Party | Wednesdays 7/14/26-9/8/26 | 119TH AVE NE b/t NE 97TH ST & NE 98TH ST",
    "project_description": "19th AVE NE Summer Play Street...",
    "start_date": "2026-07-14T00:00:00.000",
    "end_date": "2026-09-08T00:00:00.000",
    "wednesday": "5PM-8PM",
    "street_on": "19TH AVE NE"
  }
]
```

## Freshness Assessment

Fair to Good. Data updates as new permits are issued or modified. Active construction and event closures are typically reflected within hours. The data is permit-based rather than sensor-based, so it represents planned closures rather than real-time road conditions.

## Entity Model

- **Closure** — permit_number, type, project name/description
- **Schedule** — start_date, end_date, day-of-week hours
- **Location** — street_on, cross streets (text-based, not geocoded)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Updated as permits change; not real-time sensor data |
| Openness | 3 | No auth, city open data |
| Stability | 2 | Socrata platform, active dataset |
| Structure | 2 | Socrata JSON; day-of-week schedule fields are text, not structured |
| Identifiers | 2 | permit_number is stable; location is text-based |
| Additive Value | 2 | Local road closure context for Seattle activity planning |
| **Total** | **13/18** | |

## Notes

- The schedule format (day-of-week text fields like "5PM-8PM") would need parsing.
- Location data is text-based (street names and cross streets), not geocoded coordinates — spatial queries would require geocoding.
- "Play Street" and "Special Event" permits are interesting: they represent recreational opportunities (block parties, festivals) rather than just obstacles.
- Additional SDOT GIS data is available through Seattle GeoData ArcGIS portal for geocoded layers.
- Could pair with WSDOT traffic data for a comprehensive road conditions picture.
