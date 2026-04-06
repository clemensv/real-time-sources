# Wikipedia Pageviews API

**Country/Region**: Global
**Publisher**: Wikimedia Foundation
**API Endpoint**: `https://wikimedia.org/api/rest_v1/metrics/pageviews/`
**Documentation**: https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews
**Protocol**: REST (JSON)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Daily aggregates with ~1 day lag; per-article and top-pages endpoints
**License**: CC0 (analytics data)

## What It Provides

The Wikimedia Pageviews API exposes aggregate traffic statistics for every page across all Wikimedia projects. You can query top pages by day, per-article view counts over time, and project-level totals. The data covers all access methods (desktop, mobile-web, mobile-app) and distinguishes user traffic from spider/bot traffic.

This isn't a real-time stream in the SSE sense — it's a well-structured REST API that surfaces yesterday's pageview data with roughly 24-hour lag. For near-real-time signals, combine with EventStreams (where edit velocity on a page can proxy for attention spikes).

## API Details

- **Top pages**: `GET /metrics/pageviews/top/{project}/{access}/{year}/{month}/{day}` — returns top 1000 articles by views
- **Per-article**: `GET /metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}` — daily or monthly view counts for a specific page
- **Aggregate**: `GET /metrics/pageviews/aggregate/{project}/{access}/{agent}/{granularity}/{start}/{end}` — project-wide totals
- **No auth required**: Completely open, no API key
- **Rate limit**: Reasonable use; Wikimedia asks for a descriptive `User-Agent` header
- **Response**: Clean JSON with `items` array, each containing `project`, `article`, `views`, `timestamp`

## Freshness Assessment

Data granularity is daily. Yesterday's data is typically available by mid-morning UTC. This isn't sub-second fresh like EventStreams, but for trend detection and attention monitoring, the 24-hour cycle is sufficient. Polling once daily at a fixed time yields consistent, complete datasets.

## Entity Model

- **Project**: Wikimedia project identifier (e.g., `en.wikipedia`, `de.wikipedia`, `commons.wikimedia`)
- **Article**: URL-encoded page title
- **Access**: `all-access`, `desktop`, `mobile-web`, `mobile-app`
- **Agent**: `all-agents`, `user`, `spider`
- **Timestamp**: YYYYMMDDHH format (hour always `00` for daily)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily granularity, ~24h lag |
| Openness | 3 | No auth, no key, CC0 data |
| Stability | 3 | Production Wikimedia infrastructure, stable since 2015 |
| Structure | 3 | Clean JSON, consistent schema, well-documented |
| Identifiers | 3 | Project + article + date form natural composite key |
| Additive Value | 2 | Global attention signal; unique complement to edit streams |
| **Total** | **16/18** | |

## Notes

- Confirmed live: queried top pages for 2026-04-05, returned 999 articles with Main_Page at 7.1M views.
- Per-article endpoint confirmed: "Earth" article returned daily views for April 2026 (11K-18K/day).
- The real power emerges when you correlate pageview spikes with EventStreams edit bursts — a page suddenly getting both views and edits is a strong signal for breaking news or controversy.
- No streaming/push option exists; this is strictly poll-based REST.
