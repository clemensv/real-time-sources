# EskomSePush API (South Africa Loadshedding)

- **Country/Region**: South Africa
- **Endpoint**: `https://developer.sepush.co.za/business/2.0/`
- **Protocol**: REST
- **Auth**: API key (free tier: 50 requests/day)
- **Format**: JSON
- **Freshness**: Real-time (loadshedding status updates within minutes)
- **Docs**: https://eskomsepush.gumroad.com/l/api
- **Score**: 14/18

## Overview

EskomSePush is the most popular loadshedding app in South Africa, used by millions to
track rolling blackout schedules. Their API provides a clean JSON interface to loadshedding
data that the raw Eskom endpoints don't — including area-specific schedules, search,
and current status with timestamps.

This is the downstream enrichment layer over the raw Eskom GetStatus endpoint. Where
Eskom gives you a bare integer, EskomSePush gives you structured schedules, area names,
and event timing.

## Endpoint Analysis

**Probed** — returns 403 without API key (expected behavior, confirms auth requirement).

Documented endpoints:
| Endpoint | Description |
|---|---|
| `GET /business/2.0/status` | Current national loadshedding status |
| `GET /business/2.0/area?id={area_id}` | Schedule for specific area |
| `GET /business/2.0/areas_search?text={query}` | Search for areas by name |
| `GET /business/2.0/areas_nearby?lat={lat}&lon={lon}` | Find nearby areas |
| `GET /business/2.0/topics_nearby?lat={lat}&lon={lon}` | Topics near location |
| `GET /business/2.0/check` | API key allowance check |

Expected status response:
```json
{
  "status": {
    "capetown": {
      "name": "City of Cape Town",
      "next_stages": [
        {"stage": "2", "stage_start_timestamp": "..."}
      ],
      "stage": "0",
      "stage_updated": "2026-04-06T..."
    },
    "eskom": {
      "name": "National",
      "stage": "0",
      "stage_updated": "2026-04-06T..."
    }
  }
}
```

## Integration Notes

- **API key required**: Free tier allows 50 requests/day. For a polling bridge checking
  status every 5 minutes, this is insufficient (288 requests/day). A paid tier is needed,
  or combine with the free raw Eskom endpoint.
- **Hybrid approach**: Use the free Eskom GetStatus endpoint for high-frequency polling
  (stage changes), and EskomSePush for schedule enrichment on change events.
- **Area schedules**: The real value is area-specific schedules — which suburbs lose
  power when. This enables location-specific CloudEvents.
- **Cape Town separate**: Cape Town runs its own loadshedding schedule separate from
  Eskom, and the API reflects this distinction.
- **Already catalogued**: This source appears in the existing candidates. This document
  adds Africa-focused context.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time status updates |
| Openness | 1 | API key required, rate-limited free tier |
| Stability | 3 | Well-maintained commercial API |
| Structure | 3 | Clean JSON with timestamps |
| Identifiers | 2 | Area IDs are internal to ESP |
| Richness | 2 | Status + schedules + area search |
