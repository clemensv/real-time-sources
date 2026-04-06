# Deutsche Bahn Timetables API (IRIS)

**Country/Region**: Germany
**Publisher**: DB Station&Service AG / Deutsche Bahn
**API Endpoint**: `https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/`
**Documentation**: https://developers.deutschebahn.com/db-api-marketplace/apis/product/timetables
**Protocol**: REST (proprietary XML)
**Auth**: API Key (free registration on DB API Marketplace)
**Data Format**: XML (custom DB schema)
**Update Frequency**: Real-time — changes streamed per station; plan data hourly
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

## What It Provides

The DB Timetables API (internally known as IRIS — Integriertes Reisenden-Informations-System) provides real-time train arrival and departure information for all stations operated by DB Station&Service AG across Germany. This covers:

- **Planned timetable** for a given station, date, and hour
- **Full changes** (`fchg`) — all accumulated real-time changes (delays, cancellations, platform changes, route modifications)
- **Recent changes** (`rchg`) — incremental real-time delta since last poll
- **Station search** by name pattern

The data covers ICE, IC/EC, RE, RB, S-Bahn — essentially all rail services stopping at DB stations.

## API Details

Four main endpoints:

- `GET /plan/{evaNo}/{date}/{hour}` — planned timetable for station EVA number, date (YYMMDD), hour (HH)
- `GET /fchg/{evaNo}` — full changes (all current real-time modifications)
- `GET /rchg/{evaNo}` — recent changes (delta since ~2 min ago)
- `GET /station/{pattern}` — station search (returns EVA numbers)

Rate limit: 60 calls/minute on the free plan.

The XML response uses a custom schema with `<timetable>` root containing `<s>` (stop) elements, each with:
- `<tl>` — trip label (category, train number, owner)
- `<dp>` / `<ar>` — departure/arrival with planned time (`pt`), changed time (`ct`), planned platform (`pp`), changed platform (`cp`), planned path (`ppth`), changed path (`cpth`)
- Status flags for cancellations, additional stops, etc.

## Freshness Assessment

Good. The `rchg` endpoint provides near-real-time deltas (updated every ~30 seconds). The `fchg` endpoint accumulates all changes. However, this is a poll-based REST API — no push/streaming — so clients must poll per station.

## Entity Model

- **Stop** (`<s>`): a train stopping at a station — identified by a unique ID within the timetable
- **TripLabel** (`<tl>`): identifies the service (train category, number, operator)
- **Arrival/Departure** (`<ar>`, `<dp>`): planned vs. real-time times, platforms, stop sequences
- Stations identified by EVA numbers (international station codes)
- Train services identified by category + number (e.g., ICE 123)

## Feasibility Rating

| Criterion       | Score | Notes                                                      |
|-----------------|-------|------------------------------------------------------------|
| Freshness       | 2     | Real-time deltas available, but poll-based per station     |
| Openness        | 2     | CC BY 4.0, free key, but 60 req/min limits bulk use       |
| Stability       | 3     | Official DB platform, API versioned (v1), long-running     |
| Structure       | 2     | Custom XML schema — well-defined but proprietary           |
| Identifiers     | 3     | EVA numbers (international), train numbers well-established|
| Additive Value  | 3     | Unique source for German rail real-time; not GTFS-RT       |
| **Total**       | **15/18** |                                                        |

## Notes

- The API is station-centric — you query per station, not per train. For network-wide monitoring you'd need to poll many stations.
- EVA numbers are the same identifiers used in GTFS feeds for German rail, making cross-referencing straightforward.
- The `rchg` (recent changes) endpoint is the key to incremental real-time updates — poll it every 30–60 seconds per station of interest.
- DB also publishes some GTFS-RT via DELFI, but the Timetables/IRIS API carries richer German-rail-specific data (wing trains, route changes, message codes).
- Usage terms reference the "Web Bahnhofstafel" conditions — essentially: use for information display, attribution required.
