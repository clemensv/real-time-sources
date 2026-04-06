# Transport for London (TfL) Unified API

**Country/Region**: United Kingdom (London)
**Publisher**: Transport for London (TfL)
**API Endpoint**: `https://api.tfl.gov.uk/`
**Documentation**: https://api-portal.tfl.gov.uk/ and https://api.tfl.gov.uk/swagger/docs/v1
**Protocol**: REST (JSON)
**Auth**: API Key (free registration recommended; unauthenticated access available with lower limits)
**Data Format**: JSON
**Update Frequency**: Real-time — line arrivals update every 30 seconds
**License**: Open Government Licence v2.0 (TfL Transport Data terms)

## What It Provides

The TfL Unified API is one of the most comprehensive urban transit APIs in the world, covering all TfL-operated modes in London:

- **Tube** (Underground) — 11 lines, real-time arrival predictions at every station
- **Bus** — 675+ routes, countdown predictions
- **DLR, Overground, Elizabeth Line, Tram** — real-time arrivals
- **River Bus, Cable Car** — arrivals
- **Cycle Hire** (Santander Cycles) — dock availability
- **Road disruptions, traffic cameras** — ancillary data

The API provides arrival predictions with vehicle location ("Between Seven Sisters and Finsbury Park"), destination, platform, time-to-station in seconds, and bearing.

## API Details

Key real-time endpoints (verified live — returns data without auth):

- `GET /Line/{lineId}/Arrivals` — all predicted arrivals for a line (e.g., `/Line/victoria/Arrivals`)
- `GET /Line/{lineId}/Arrivals/{stopPointId}` — arrivals at a specific stop on a line
- `GET /StopPoint/{naptanId}/Arrivals` — arrivals at a stop across all lines
- `GET /Line/{lineId}/Status` — service status (good service, minor delays, etc.)
- `GET /Line/{lineId}/Disruption` — current disruption details
- `GET /Vehicle/{vehicleId}/Arrivals` — predictions for a specific vehicle

Response fields per prediction:
- `vehicleId`, `naptanId`, `stationName`, `lineId`, `lineName`
- `platformName`, `direction`, `bearing`
- `destinationNaptanId`, `destinationName`
- `currentLocation` (human-readable text)
- `expectedArrival` (ISO 8601), `timeToStation` (seconds)
- `timestamp` (when prediction was generated)

Modes available: `bus`, `tube`, `dlr`, `overground`, `elizabeth-line`, `tram`, `river-bus`, `cable-car`, `national-rail`, `coach`, `cycle-hire`.

Rate limits: 500 requests/min with API key; lower without.

## Freshness Assessment

Excellent. Predictions are generated from TfL's iBus (bus) and TUMIS/TrackerNet (tube) systems. Arrival data for the Tube is refreshed approximately every 30 seconds. Bus countdown data is similarly frequent. The API can be called without authentication, making it trivially easy to probe.

## Entity Model

- **Prediction**: core entity — one per vehicle per stop — with vehicle location, expected arrival, platform, direction
- **Line**: route identifier (e.g., `victoria`, `jubilee`, route number for buses)
- **StopPoint**: station/stop identified by NaPTAN ID
- **Mode**: transport mode (tube, bus, dlr, etc.)
- **LineStatus**: current service status per line
- **Disruption**: details of current service disruptions

## Feasibility Rating

| Criterion       | Score | Notes                                                         |
|-----------------|-------|---------------------------------------------------------------|
| Freshness       | 3     | ~30 s updates, live predictions verified                       |
| Openness        | 3     | OGL v2, works without auth, generous rate limits               |
| Stability       | 3     | Major government API, Swagger-documented, running for 10+ years|
| Structure       | 3     | Clean REST/JSON, Swagger spec available, consistent schema     |
| Identifiers     | 3     | NaPTAN stop IDs, standard line IDs, vehicle IDs                |
| Additive Value  | 2     | REST/JSON — similar pattern to existing bridges; but very high volume |
| **Total**       | **17/18** |                                                            |

## Notes

- The TfL API is essentially open-access — it returns full JSON responses even without an API key (just rate-limited). This is rare for transit APIs and makes it excellent for prototyping.
- Verified live: `GET https://api.tfl.gov.uk/Line/victoria/Arrivals` returns detailed prediction JSON with vehicle positions, platforms, countdown timers.
- Covers an enormous network — the bus arrivals alone generate massive data volume (675+ routes, thousands of stops).
- The `currentLocation` field provides human-readable position text ("Between Seven Sisters and Finsbury Park") — a nice touch not available in GTFS-RT.
- Could be implemented as a periodic poll bridge (every 30 s) generating CloudEvents per arrival prediction.
- TfL also publishes GTFS for static timetables and some GTFS-RT, but the Unified API is the authoritative real-time source with richer data.
