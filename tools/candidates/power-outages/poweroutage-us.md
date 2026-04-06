# PowerOutage.us
**Country/Region**: United States
**Publisher**: PowerOutage.us (independent aggregator)
**API Endpoint**: `https://poweroutage.us/` (web scraping) — no public API
**Documentation**: https://poweroutage.us/about
**Protocol**: Web (HTML/JavaScript) — data scraped from 1000+ utility outage maps
**Auth**: N/A (no public API)
**Data Format**: HTML (web portal), internal JSON (not public)
**Update Frequency**: Near real-time (aggregates utility outage data every few minutes)
**License**: Proprietary — data aggregated from utility companies

## What It Provides
PowerOutage.us aggregates power outage data from over 1,000 electric utility companies across all 50 US states:
- Current outage counts by state, county, and utility
- Outage trends over time (1h, 6h, 24h, 7d)
- Percentage of customers affected
- Historical outage data
- Storm impact tracking
- Per-utility outage counts

## API Details
- **No public API** — the site aggregates by scraping individual utility outage maps
- **Web portal**: `https://poweroutage.us/` — interactive maps and tables
- **State view**: `https://poweroutage.us/area/state/{state}` — per-state breakdown
- **County view**: `https://poweroutage.us/area/county/{fips}` — per-county data
- **Internal data**: The site uses JavaScript to load JSON data for the map, but this is not a public API
- **Data sources**: Individual utility outage management systems (OMS)

## Freshness Assessment
Good. The site updates every few minutes by polling utility outage feeds. However, there is no public API, making automated integration difficult without scraping. The aggregation is the unique value — individual utilities all have their own incompatible outage reporting formats.

## Entity Model
- **State** (name, total customers, customers out, percentage)
- **County** (FIPS code, name, state, total customers, customers out)
- **Utility** (name, state, customers tracked, customers out)
- **Trend** (timestamp, outage count, time interval)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Near real-time aggregation |
| Openness | 0 | No public API, scraping required |
| Stability | 2 | Independent project, not guaranteed |
| Structure | 1 | Web-only, would need scraping |
| Identifiers | 2 | FIPS codes for counties, utility names |
| Additive Value | 3 | Unique US-wide outage aggregation |
| **Total** | **11/18** | |

## Notes
- The main value is the aggregation of 1000+ utility outage feeds into one view
- No public API means integration would require web scraping (fragile, possibly against ToS)
- Individual utility outage feeds could be integrated directly but vary wildly in format
- Some utilities use Kubra/OMS platforms that have more structured data feeds
- DOE (Department of Energy) publishes some outage data via EIA but it's not real-time
- Consider as a lower-priority candidate due to API access limitations
