# SBB / Open Transport Data Switzerland

**Country/Region**: Switzerland (national)
**Publisher**: SBB CFF FFS / Swiss Federal Office of Transport (BAV/OFT) via opentransportdata.swiss
**API Endpoint**: `https://transport.opendata.ch/v1/` (community) and `https://api.opentransportdata.swiss/` (official)
**Documentation**: https://opentransportdata.swiss/en/cookbook/ and https://transport.opendata.ch/docs.html
**Protocol**: REST/JSON (community API), OJP / SIRI / GTFS-RT (official platform)
**Auth**: Community API: none. Official platform: free API key via api-manager.opentransportdata.swiss
**Data Format**: JSON (community), XML/OJP (official), Protobuf (GTFS-RT)
**Update Frequency**: Real-time — community API shows live delays; official GTFS-RT updated every ~20 s
**License**: Open data — community API: MIT. Official: Swiss Open Government Data license

## What It Provides

Switzerland has two complementary open transit data ecosystems:

### transport.opendata.ch (Community API)
An unofficial but widely-used REST API wrapping SBB's journey planner. Returns real-time stationboard data, connections, and journey planning with delay information. Covers all Swiss public transport: SBB trains, PostBus, city trams/buses (ZVV Zurich, BVB Basel, TPG Geneva, BERNMOBIL), mountain railways, lake ferries.

### opentransportdata.swiss (Official Platform)
The official Swiss government open data platform providing:
- **GTFS-RT**: Trip updates and service alerts for Swiss rail
- **SIRI-SX**: Situation exchange (disruptions) — Switzerland uses SIRI natively for alerts
- **OJP (Open Journey Planner)**: CEN standard for journey planning queries
- **HRDF**: Timetable data in SBB's HAFAS Raw Data Format
- **NeTEx**: Static network data

## API Details

### Community API (transport.opendata.ch)

- `GET /v1/stationboard?station=Bern&limit=10` — departures from a station with real-time delays
- `GET /v1/connections?from=Zurich&to=Bern` — journey planning
- `GET /v1/locations?query=Basel` — station search

Returns clean JSON with delay information in `prognosis` fields. Confirmed working — tested with Bern station, returns scheduled times + real-time prognosis data.

### Official Platform (opentransportdata.swiss)

- GTFS-RT feeds via API manager (API key required)
- SIRI-SX for disruption messaging
- OJP endpoint for standards-compliant journey queries
- Real-time occupancy data (1st/2nd class capacity predictions)

## Freshness Assessment

Good. The community API returns real-time delay predictions for trains (the `prognosis` object includes predicted departure times when available). The official platform's GTFS-RT and SIRI-SX feeds provide structured real-time updates. Swiss trains are famously punctual, but when delays occur, the real-time data captures them accurately. Bus/tram real-time coverage varies by operator — urban operators (ZVV, BVB) have good real-time; rural PostBus routes may be schedule-only.

## Entity Model

### Community API
- **Stationboard entry**: category (S/IC/IR/RE), number, operator, destination, departure time, delay, platform, prognosis, passList
- **Connection**: from/to sections with departure/arrival, duration, transfers, real-time adjustments
- **Location**: id (DIDOK number), name, coordinates

### Official Platform
- GTFS-RT standard entities: TripUpdate, VehiclePosition, Alert
- SIRI-SX: PtSituationElement with affected routes/stops, validity, message text
- OJP: TripRequest/TripResponse with real-time leg details

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Real-time delays for rail; prognosis data in community API    |
| Openness        | 3     | Community API: no auth. Official: free API key                |
| Stability       | 3     | Government-backed official platform; community API long-running|
| Structure       | 2     | Community API is clean JSON but unofficial; official uses OJP/SIRI |
| Identifiers     | 2     | DIDOK station numbers (Swiss standard); GTFS IDs in official feeds |
| Additive Value  | 2     | SIRI-SX is native SIRI; OJP is a rare CEN standard implementation  |
| **Total**       | **15/18** |                                                           |

## Notes

- The community API (transport.opendata.ch) is the easiest entry point — zero auth, clean JSON, returns real-time. But it's an unofficial wrapper and could change without notice.
- The official platform's SIRI-SX implementation makes Switzerland a candidate for the generic SIRI bridge alongside UK BODS, Trafiklab, and Entur.
- OJP (Open Journey Planner) is an interesting CEN standard — if we ever build an OJP bridge, Switzerland is the primary implementation to target.
- Real-time occupancy data (train crowding predictions by class) is a distinctive feature of the Swiss system — rare in open transit data.
- The INDEX.md previously listed the Swiss Transport API as "not pursued" due to limited real-time. The official opentransportdata.swiss platform addresses this with GTFS-RT and SIRI — this reassessment upgrades the candidate.
