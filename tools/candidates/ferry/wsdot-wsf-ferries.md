# Washington State Ferries (WSF) API

- **Country/Region**: US — Puget Sound / Pacific Northwest
- **Publisher**: Washington State Department of Transportation (WSDOT)
- **Endpoint**: `https://www.wsdot.wa.gov/ferries/api/`
- **Protocol**: REST (JSON/XML) and SOAP
- **Auth**: API Access Code (free registration via email)
- **Format**: JSON, XML
- **Freshness**: Real-time (vessel positions update every ~30 seconds, wait times every few minutes)
- **Docs**: https://www.wsdot.wa.gov/ferries/api/terminals/documentation/rest.html
- **Score**: 16/18

## Overview

Washington State Ferries operates the largest ferry system in the US and the third largest in the world, serving Puget Sound with 10 routes and 21 terminals. The WSDOT Traveler Information API provides three separate sub-APIs for ferries:

1. **Vessels API** — Real-time GPS positions, heading, speed, and status for all active vessels
2. **Terminals API** — Terminal information, current wait times, and remaining vehicle capacity
3. **Schedule API** — Planned departures, real-time schedule adjustments

This is essential for a Puget Sound free-time advisor: ferry wait times and schedules directly affect when people can reach islands, parks, and recreation areas.

## API Details

**Base URLs:**
- Vessels: `https://www.wsdot.wa.gov/ferries/api/vessels/rest/`
- Terminals: `https://www.wsdot.wa.gov/ferries/api/terminals/rest/`
- Schedule: `https://www.wsdot.wa.gov/ferries/api/schedule/rest/`

All endpoints require `?apiaccesscode={YOUR_CODE}` parameter.

**Key Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `GET /vessels/rest/vessellocations` | All vessel GPS positions, heading, speed, route |
| `GET /terminals/rest/waittimes` | Current estimated wait times at all terminals |
| `GET /terminals/rest/terminalbasics` | Terminal metadata (name, location, amenities) |
| `GET /schedule/rest/scheduletoday/{routeId}` | Today's schedule for a route |
| `GET /vessels/rest/vesselverbose` | Detailed vessel info (capacity, class, status) |

**Sample Response (Vessel Locations):**
```json
[
  {
    "VesselID": 68,
    "VesselName": "Tacoma",
    "Latitude": 47.6233,
    "Longitude": -122.5098,
    "Speed": 15.2,
    "Heading": 270,
    "InService": true,
    "DepartingTerminalID": 7,
    "ArrivingTerminalID": 3,
    "ScheduledDeparture": "2024-01-15T14:30:00",
    "LeftDock": "2024-01-15T14:32:00",
    "Eta": "2024-01-15T15:05:00"
  }
]
```

**Routes Covered:**
- Seattle–Bainbridge Island
- Seattle–Bremerton
- Edmonds–Kingston
- Mukilteo–Clinton (Whidbey Island)
- Fauntleroy–Vashon–Southworth
- Point Defiance–Tahlequah
- Anacortes–San Juan Islands
- Coupeville–Port Townsend

## Freshness Assessment

Excellent. Vessel positions update approximately every 30 seconds. Terminal wait times are updated every few minutes based on real-time vehicle queue monitoring. Schedule data reflects same-day adjustments. This is one of the most real-time feeds in the Puget Sound area.

## Entity Model

- **Vessel** — VesselID, name, class, capacity, current position/speed/heading
- **Terminal** — TerminalID, name, location, amenities, current wait time
- **Route** — RouteID, description, terminal pair
- **Schedule** — Departure times, annotations, service alerts
- **Wait Time** — Terminal ID, route ID, estimated wait in minutes, timestamp

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Vessel positions ~30s, wait times ~minutes |
| Openness | 3 | Free API key via email, US government data |
| Stability | 3 | WSDOT official API, well-maintained since 2012+ |
| Structure | 3 | Clean REST JSON with typed fields |
| Identifiers | 2 | VesselID, TerminalID, RouteID — numeric but stable |
| Additive Value | 2 | Unique Puget Sound ferry data, complements WSDOT traffic bridge |
| **Total** | **16/18** | |

## Notes

- The repo already has a `wsdot` bridge for traffic data. The ferries API uses the same access code system but different endpoints. Could be a separate bridge or extended into the existing WSDOT bridge.
- GTFS-RT feeds for WSF are also available via OneBusAway (`api.pugetsound.onebusaway.org`), but the native WSDOT API is richer with wait times and vessel details.
- Wait time data is especially valuable: long waits at Anacortes (San Juan Islands) or Fauntleroy can be 2+ hours on summer weekends.
- Community client libraries exist in TypeScript (`ws-dottie`) and Go (`alpineworks.io/wsdot`).
