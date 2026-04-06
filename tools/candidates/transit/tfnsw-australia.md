# Transport for NSW — Australia Open Data

**Country/Region**: Australia (New South Wales)
**Publisher**: Transport for NSW (TfNSW)
**API Endpoint**: `https://api.transport.nsw.gov.au/v1/`
**Documentation**: https://opendata.transport.nsw.gov.au/
**Protocol**: GTFS-RT (Protobuf) + REST/JSON + SIRI-FM (Facility Monitoring)
**Auth**: API key required (free registration — 63,000+ registered users)
**Data Format**: Protobuf (GTFS-RT), JSON (REST), XML (SIRI)
**Update Frequency**: Real-time — GTFS-RT updated every ~15 s; REST predictions real-time
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

## What It Provides

Transport for NSW is Australia's most comprehensive transit open data platform — arguably the gold standard in the Asia-Pacific region. With 63,000+ registered users and 34+ billion API hits, it's a massive, proven platform. It covers:

- **Sydney Trains**: suburban/intercity rail — real-time positions and predictions
- **Sydney Metro**: automated metro — real-time
- **Sydney Buses**: 300+ routes — real-time GPS and ETAs
- **Sydney Light Rail**: real-time
- **Sydney Ferries**: harbor ferry — real-time vessel positions
- **NSW TrainLink**: regional rail across the state
- **Private bus operators**: across Greater Sydney and regional NSW
- **Opal card system**: trip planner integration

## API Details

### GTFS-RT Feeds

- `GET /v1/gtfs/vehiclepos/sydneytrains` — vehicle positions (trains)
- `GET /v1/gtfs/vehiclepos/buses` — vehicle positions (buses)
- `GET /v1/gtfs/vehiclepos/ferries` — ferry positions
- `GET /v1/gtfs/vehiclepos/lightrail` — light rail positions
- `GET /v1/gtfs/realtime/sydneytrains` — trip updates
- `GET /v1/gtfs/alerts/sydneytrains` — service alerts

Separate feeds per mode — standard GTFS-RT protobuf.

### REST API

- `GET /v1/tp/departure_mon?outputFormat=rapidJSON&name_dm={stopId}` — departure monitor at a stop
- `GET /v1/tp/trip?outputFormat=rapidJSON&name_origin=...&name_destination=...` — trip planning
- `GET /v1/tp/stop_finder?outputFormat=rapidJSON&name_sf=...` — stop search

### SIRI Facility Monitoring

TfNSW publishes SIRI-FM (Facility Monitoring) for elevator and escalator status — one of the few transit agencies with real-time accessibility infrastructure data.

API key goes in `Authorization: apikey {key}` header. Rate limits: generous (34B hits suggests liberal limits).

## Freshness Assessment

Excellent. TfNSW is one of the most actively maintained transit data platforms globally. The scale (34 billion API hits, 63,000 users, 14,000 applications) speaks to reliability. Real-time coverage is strong across all Sydney modes — trains, buses, ferries, light rail, metro all have GPS-based real-time tracking.

## Entity Model

- **GTFS-RT standard**: TripUpdate (stop_time_update with arrival/departure delay), VehiclePosition (lat/lon, bearing, speed, trip, current_stop), Alert (informed_entity, cause, effect, text)
- **REST entities**: departure monitor returns departures with real-time flag, delay, platform, transport mode, operator
- **SIRI-FM**: FacilityCondition (elevator/escalator ID, status, location, last update time)
- IDs follow TfNSW's GTFS system — operator-prefixed route/stop IDs

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Comprehensive real-time across all Sydney modes               |
| Openness        | 2     | Free API key required — easy registration, CC BY 4.0          |
| Stability       | 3     | Massively proven platform (34B hits, 63K users, 14K apps)     |
| Structure       | 3     | Standard GTFS-RT + well-documented REST + SIRI-FM             |
| Identifiers     | 3     | GTFS-compatible IDs throughout                                |
| Additive Value  | 2     | SIRI-FM for accessibility is unique; GTFS-RT part covered by existing bridge|
| **Total**       | **16/18** |                                                           |

## Notes

- TfNSW's SIRI Facility Monitoring (elevator/escalator status) is genuinely rare — few transit agencies publish real-time accessibility infrastructure data. This alone makes it a distinctive candidate.
- The platform's scale (34 billion API hits) makes it one of the most battle-tested transit APIs anywhere.
- Other Australian states have similar (smaller) platforms: PTV Victoria (Melbourne), TransLink Queensland (Brisbane), Transperth (Perth) — all publish GTFS-RT. TfNSW is the largest and most open.
- The REST API uses EFA (Electronic Fare Allocation) — the same journey planner engine used by many European transit authorities.
- Ferry tracking is a nice differentiator — GTFS-RT vehicle positions for harbor ferries in Sydney Harbour.
