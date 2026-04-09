# Seattle Real-Time Fire 911 Calls

- **Country/Region**: US — Seattle, WA
- **Publisher**: City of Seattle / Seattle Fire Department
- **Endpoint**: `https://data.seattle.gov/resource/kzjm-xkqj.json`
- **Protocol**: REST (Socrata SODA API)
- **Auth**: None (app token optional for higher rate limits)
- **Format**: JSON, CSV, XML, GeoJSON
- **Freshness**: Real-time (~5 minute updates)
- **Docs**: https://dev.socrata.com/ and https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj
- **Score**: 16/18

## Overview

The City of Seattle publishes real-time Fire Department 911 dispatch data through its Socrata-powered Open Data portal. Every fire, medical, and rescue call dispatched by the Seattle 911 center appears in this feed within approximately 5 minutes. This is highly relevant for a free-time advisor: active incidents near parks, trails, or recreation areas can affect safety and accessibility.

## API Details

**Base URL:** `https://data.seattle.gov/resource/kzjm-xkqj.json`

**SODA API Query Examples:**

| Query | URL |
|-------|-----|
| Latest 10 incidents | `?$limit=10&$order=datetime DESC` |
| Active incidents in last hour | `?$where=datetime > '2024-01-15T14:00:00'&$order=datetime DESC` |
| Filter by type | `?$where=type='Aid Response'` |
| Bounding box (area filter) | `?$where=within_box(report_location, 47.6, -122.4, 47.7, -122.3)` |

**Fields:**
- `address` — Street address of incident
- `type` — Incident type (e.g., "Aid Response", "Medic Response", "Auto Fire Alarm", "Brush Fire")
- `datetime` — Dispatch timestamp (ISO 8601)
- `latitude`, `longitude` — Location coordinates
- `report_location` — GeoJSON point
- `incident_number` — Unique identifier (e.g., "F240012345")

**Verified Response (2026-04-08):**
```json
[
  {
    "address": "917 34th Ave",
    "type": "Aid Response",
    "datetime": "2026-04-08T11:48:00.000",
    "latitude": "47.610508",
    "longitude": "-122.289373",
    "report_location": {
      "type": "Point",
      "coordinates": [-122.289373, 47.610508]
    },
    "incident_number": "F260046617"
  }
]
```

## Freshness Assessment

Excellent. Data is updated every ~5 minutes as new 911 dispatches occur. Incidents appear in the feed almost immediately after dispatch. This is among the freshest open data feeds in the Seattle area.

## Entity Model

- **Incident** — incident_number, type, datetime, address, lat/lon
- **Type** — categorical incident classification (Fire, Aid, Medic, Hazmat, etc.)
- **Location** — address + GeoJSON point

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | ~5 minute updates, near real-time |
| Openness | 3 | No auth required, US city open data |
| Stability | 3 | Seattle Open Data portal, Socrata-backed, active since 2010+ |
| Structure | 3 | Clean JSON with geo fields, SODA query support |
| Identifiers | 2 | incident_number is stable; no persistent entity beyond single call |
| Additive Value | 2 | Safety awareness for outdoor activity planning |
| **Total** | **16/18** | |

## Notes

- Covers fire, EMS, and rescue calls. Does NOT cover police calls (those were in a separate dataset that appears to have been removed/restructured).
- The Socrata SODA API supports powerful filtering: spatial queries, time ranges, type filtering — all useful for a geo-aware advisor tool.
- Rate limits are generous without an app token (~1000 requests/hour); with a free app token, higher.
- This data pairs well with NWS weather alerts for a comprehensive safety picture.
- Incident types relevant for outdoor activities: "Brush Fire", "Water Rescue", "Hazmat", "MVI - Loss of Life", etc.
