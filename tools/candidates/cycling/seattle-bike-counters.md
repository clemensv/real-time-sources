# Seattle SDOT Bicycle Counters

- **Country/Region**: US — Seattle, WA
- **Publisher**: Seattle Department of Transportation (SDOT)
- **Endpoint**: `https://data.seattle.gov/resource/65db-xm6k.json`
- **Protocol**: REST (Socrata SODA API)
- **Auth**: None (app token optional)
- **Format**: JSON, CSV, XML
- **Freshness**: Hourly updates
- **Docs**: https://data.seattle.gov/Transportation/Fremont-Bridge-Bicycle-Counter/65db-xm6k
- **Score**: 13/18

## Overview

Seattle DOT operates permanent bicycle counters at key cycling corridors, with the Fremont Bridge counter being the flagship dataset. The counter uses inductive loop sensors to count bicycles crossing in both directions (northbound/southbound) with hourly granularity. This data is useful for a free-time advisor to understand cycling activity levels, commute patterns, and as a proxy for weather-friendliness of outdoor activities.

## API Details

**Base URL:** `https://data.seattle.gov/resource/65db-xm6k.json`

**SODA Query Examples:**

| Query | URL |
|-------|-----|
| Latest reading | `?$order=date DESC&$limit=1` |
| Last 24 hours | `?$where=date > '2024-01-14T00:00:00'&$order=date DESC` |
| Daily totals | `?$select=date_trunc_ymd(date) as day, sum(fremont_bridge_nb) as nb, sum(fremont_bridge_sb) as sb&$group=day&$order=day DESC&$limit=7` |

**Fields:**
- `date` — ISO 8601 timestamp (hourly buckets)
- `fremont_bridge` — Total bike count for the hour
- `fremont_bridge_nb` — Northbound count
- `fremont_bridge_sb` — Southbound count

**Verified Response:**
```json
[
  {
    "date": "2026-02-28T23:00:00.000",
    "fremont_bridge": "67",
    "fremont_bridge_nb": "55",
    "fremont_bridge_sb": "12"
  }
]
```

**Additional Counters:**
SDOT maintains additional counter datasets:
- `https://data.seattle.gov/resource/u38e-ybnc.json` — Burke-Gilman Trail (NE 70th St)
- `https://data.seattle.gov/resource/4qej-qvrz.json` — Broadway Cycle Track
- `https://data.seattle.gov/resource/j4vh-b42a.json` — 2nd Ave Cycle Track
- `https://data.seattle.gov/resource/mefu-7eau.json` — Chief Sealth Trail

## Freshness Assessment

Good. Data is recorded hourly and published to the open data portal with minimal delay. During the daytime, you can expect the previous hour's count to be available within the current hour. Historical data goes back to 2012.

## Entity Model

- **Counter** — Fixed location sensor with directional channels
- **Reading** — Timestamp (hourly), count per direction, total
- **Location** — Fremont Bridge (47.648, -122.350) and other fixed points

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Hourly aggregates, not minute-level |
| Openness | 3 | No auth, city open data |
| Stability | 2 | Socrata platform, active since 2012; sensor hardware can fail |
| Structure | 2 | Simple flat records; numeric strings (not typed numbers) |
| Identifiers | 2 | Implicit by dataset; no cross-counter ID scheme |
| Additive Value | 2 | Unique cycling activity data for Seattle |
| **Total** | **13/18** | |

## Notes

- Best treated as a contextual/informational feed rather than a critical decision input.
- High bike counts correlate with good weather — can serve as a proxy for "nice day to be outside."
- Summer peak days see 5,000+ bikes across Fremont Bridge; winter lows can be under 500.
- Multiple counter datasets could be aggregated into a single bridge with a counter-location dimension.
- The Socrata SODA API supports aggregation queries directly, reducing client-side processing.
