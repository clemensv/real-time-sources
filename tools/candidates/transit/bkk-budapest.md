# BKK Budapest — Hungary Transit Open Data

**Country/Region**: Hungary (Budapest)
**Publisher**: BKK (Budapesti Közlekedési Központ / Centre for Budapest Transport)
**API Endpoint**: `https://go.bkk.hu/gtfsrt/` (GTFS-RT) and `https://go.bkk.hu/api/` (REST)
**Documentation**: https://opendata.bkk.hu/ and https://bkkfutar.docs.apiary.io/
**Protocol**: GTFS-RT (Protobuf) + proprietary REST/JSON (Futár API)
**Auth**: GTFS-RT: appears open (confirmed 200). REST API: API key required (free registration)
**Data Format**: Protobuf (GTFS-RT), JSON (Futár REST)
**Update Frequency**: Real-time — GTFS-RT feeds updated every ~15 s
**License**: Open data (BKK open data license)

## What It Provides

BKK operates one of the largest transit networks in Central Europe: Budapest metro (4 lines), tram (30+ routes including the iconic line 2 along the Danube), bus (200+ routes), trolleybus, suburban rail (HÉV), and river ferry. The open data platform provides:

- **GTFS-RT Trip Updates**: real-time delays, cancellations, schedule deviations
- **GTFS-RT Vehicle Positions**: GPS positions of active vehicles
- **GTFS-RT Service Alerts**: disruptions, detours, service changes
- **Futár REST API**: proprietary JSON API with departures, arrivals, trip details, vehicle tracking

## API Details

### GTFS-RT Feeds

Confirmed working (all returned HTTP 200 with protobuf data):

- `GET /gtfsrt/alerts.pb` — service alerts
- `GET /gtfsrt/trip_updates.pb` — trip updates with delays
- `GET /gtfsrt/vehicle_positions.pb` — vehicle GPS positions

No authentication was required in testing — feeds returned valid protobuf without any API key.

### Futár REST API

The Futár API is BKK's proprietary JSON interface:

- `GET /api/query/v1/ws/otp/api/where/arrivals-and-departures-for-stop.json?stopId=BKK_F00940`
- `GET /api/query/v1/ws/otp/api/where/trip-details.json?tripId=...`
- `GET /api/query/v1/ws/otp/api/where/vehicles-for-route.json?routeId=...`

The REST API requires an API key (`key` parameter) — returned 401 without one. Registration is free through the BKK open data portal.

## Freshness Assessment

Good. GTFS-RT feeds are actively maintained and returned valid data in testing. BKK has been publishing open data since ~2014 and the Futár system (BKK's real-time passenger information system) powers the departure boards across Budapest. Vehicle positions are GPS-based with typical 15–30 s update intervals. Coverage spans all BKK-operated modes.

## Entity Model

- **GTFS-RT TripUpdate**: trip_id, route_id, stop_time_update (arrival/departure delay per stop)
- **GTFS-RT VehiclePosition**: trip reference, lat/lon, bearing, speed, current_stop_sequence, current_status
- **GTFS-RT Alert**: informed_entity (route/stop/trip), cause, effect, header_text, description_text
- **Futár entities**: Stop, Route, Trip, Vehicle — with BKK-specific IDs (`BKK_` prefix)
- References BKK's GTFS static feed for route/stop definitions

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Active GTFS-RT feeds, confirmed live                          |
| Openness        | 3     | GTFS-RT appears unauthenticated; Futár needs free key        |
| Stability       | 2     | Running since ~2014; less formal API versioning than Western European peers |
| Structure       | 3     | Standard GTFS-RT protobuf — plug-and-play with existing bridge|
| Identifiers     | 2     | BKK-specific IDs with `BKK_` prefix; GTFS-compatible         |
| Additive Value  | 1     | GTFS-RT coverable by existing bridge — no new protocol territory|
| **Total**       | **14/18** |                                                           |

## Notes

- BKK Budapest is a good GTFS-RT feed to add to the existing GTFS-RT bridge's curated feed list — a major European capital with solid real-time data.
- The Futár REST API is built on OneBusAway (OBA) — the same framework used by several US transit agencies. This means the API structure is familiar if we ever build an OBA bridge.
- Budapest's tram network is one of the largest in Europe and well-covered by real-time data.
- The GTFS-RT feeds appear to be openly accessible without authentication — this is unusual and valuable.
- HÉV suburban rail (connecting Budapest to surrounding towns) is included in the data.
