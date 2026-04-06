# USGS Volcano Hazards Program / HANS (Hazard Alert Notification System)

**Country/Region**: United States and territories
**Publisher**: USGS (United States Geological Survey) — Volcano Hazards Program
**API Endpoint**: `https://volcanoes.usgs.gov/hans2/api/`
**Documentation**: https://volcanoes.usgs.gov/hans2/api/
**Protocol**: REST (JSON)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: As events occur (alert level changes, VAN/VONA issuances)
**License**: US Government public domain

## What It Provides

The USGS Volcano Hazards Program monitors ~161 potentially active volcanoes across the United States through a network of volcano observatories (AVO, CVO, HVO, YVO, CNMI). The HANS (Hazard Alert Notification System) API provides:

- **Volcano alert levels** — Current alert status for all monitored US volcanoes (Normal, Advisory, Watch, Warning)
- **Aviation color codes** — Green, Yellow, Orange, Red
- **Volcano Activity Notices (VAN)** — Notifications of significant activity changes
- **Volcano Observatory Notices for Aviation (VONA)** — Aviation-specific alerts
- **Volcano information** — Location, type, observatory assignment

## API Details

The HANS API is documented and REST-based:

**Base URL:**
```
https://volcanoes.usgs.gov/hans2/api/
```

**Available sub-APIs:**
- `/api/map/` — Map-related data
- `/api/notice/` — Volcano notices (VAN/VONA)
- `/api/volcano/` — Volcano metadata and current status
- `/api/search/` — Search functionality
- `/api/research/` — Research data
- `/api/other/` — Additional endpoints

**Query volcanos:**
```
GET https://volcanoes.usgs.gov/hans2/api/volcano/
```
Returns JSON array (was empty `[]` during testing — may be empty when no alerts active, or may require parameters).

**Query notices:**
```
GET https://volcanoes.usgs.gov/hans2/api/notice/
```
(Returns 400 — likely requires parameters like observatory, date range, or volcano ID)

**Public-facing portal:**
```
https://volcanoes.usgs.gov/hans-public/
```

## Freshness Assessment

Good for alert-based data. Alert level changes and VAN/VONA notices are published in near real-time as volcanic conditions change. However, during periods of quiescence the API may return minimal data. The system is event-driven — data flow correlates with volcanic activity.

## Entity Model

**Volcano:**
- Volcano ID / name
- Location (coordinates)
- Volcano type
- Monitoring observatory (AVO, CVO, HVO, YVO, CNMI)
- Current alert level (Normal/Advisory/Watch/Warning)
- Current aviation color code (Green/Yellow/Orange/Red)

**Notice (VAN/VONA):**
- Notice type and ID
- Volcano reference
- Issue date/time
- Alert level and color code
- Narrative text describing activity
- Hazard description

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Event-driven, near real-time when activity occurs |
| Openness | 3 | Public domain, no auth |
| Stability | 3 | USGS — official US government monitoring |
| Structure | 2 | REST JSON API exists but documentation is sparse |
| Identifiers | 3 | Volcano IDs, notice IDs, observatory codes |
| Additive Value | 3 | Authoritative US volcanic alert data |
| **Total** | **16/18** | |

## Notes

- The API exists and is documented at a high level, but specific parameter requirements are not well-documented. Testing returned empty results or 400 errors.
- The public-facing HANS portal (hans-public) provides a human-readable view of the same data.
- Five USGS volcano observatories cover different US regions: Alaska (AVO), Cascades (CVO), Hawaii (HVO), Yellowstone (YVO), and CNMI.
- Alert level changes are relatively rare events — most US volcanoes are at "Normal" most of the time.
- Consider also the USGS earthquake API (`earthquake.usgs.gov`) for volcanic seismicity data.
- RSS feeds may also be available as an alternative to the JSON API.
