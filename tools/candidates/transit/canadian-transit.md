# Canadian Transit GTFS-RT — TTC, TransLink, STM

**Country/Region**: Canada (Toronto, Vancouver, Montreal)
**Publishers**: TTC (Toronto), TransLink (Vancouver), STM (Montreal), and more
**API Endpoints**:
- TTC: `https://bustime.ttc.ca/gtfsrt/vehicles` (GTFS-RT)
- TransLink: `https://gtfs.translink.ca/v2/gtfsrealtime` (GTFS-RT)
- STM: GTFS-RT via API key portal
**Documentation**: https://open.toronto.ca/ (TTC), https://www.translink.ca/about-us/doing-business-with-translink/app-developer-resources (TransLink)
**Protocol**: GTFS-RT (Protobuf) + proprietary REST (TransLink RTTI)
**Auth**: TTC: no auth for GTFS-RT. TransLink: API key required. STM: API key required.
**Data Format**: Protobuf (GTFS-RT), JSON (TransLink RTTI)
**Update Frequency**: Real-time — vehicle positions every 15–30 s; predictions real-time
**License**: Open Government Licence (Canada/Ontario/BC)

## What It Provides

Canada's three largest cities all publish substantial real-time transit data:

### TTC (Toronto Transit Commission)
- **Subway**: 4 lines (including Line 5 Eglinton opening) — real-time train tracking
- **Bus**: 150+ routes — GTFS-RT vehicle positions and trip updates
- **Streetcar**: 10 routes — GTFS-RT real-time positions

### TransLink (Metro Vancouver)
- **SkyTrain**: 3 automated lines (Expo, Millennium, Canada) — real-time
- **Bus**: 200+ routes — GTFS-RT vehicle positions
- **SeaBus**: ferry — real-time
- **West Coast Express**: commuter rail

### STM (Société de transport de Montréal)
- **Metro**: 4 lines — real-time
- **Bus**: 200+ routes — GTFS-RT

## API Details

### TTC GTFS-RT
- `GET /gtfsrt/vehicles` — vehicle positions (standard protobuf)
- `GET /gtfsrt/tripupdates` — trip updates with delays
- `GET /gtfsrt/alerts` — service alerts

No authentication required. TTC also supports the NextBus API for legacy compatibility.

### TransLink RTTI (Real-Time Transit Information)
- `GET /rttiapi/v1/stops/{stopNo}/estimates?apikey={key}` — real-time bus arrivals
- `GET /rttiapi/v1/buses?apikey={key}` — all bus positions
- GTFS-RT feeds also available

### STM
- GTFS-RT feeds available through STM's developer portal (key required)
- Also publishes GTFS static data via open data portal

## Freshness Assessment

Good. TTC has solid real-time coverage — the GTFS-RT feeds are actively maintained and power several production apps (including Transit App). TransLink's automated SkyTrain has excellent real-time. Bus real-time varies in quality across all three systems but is generally reliable. The main challenge with the TTC endpoint was a timeout in testing (10 seconds) — likely returning a large protobuf feed.

## Entity Model

- **Standard GTFS-RT**: TripUpdate, VehiclePosition, Alert — all three cities use standard GTFS-RT entities
- **TransLink RTTI**: Stops (StopNo, StopName, Routes, AtStreet), Estimates (RouteNo, Direction, ExpectedLeaveTime, ExpectedCountdown, Schedules)
- IDs follow each agency's GTFS system

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Active GTFS-RT feeds across all three cities                  |
| Openness        | 2     | TTC: no auth; TransLink/STM: free API key                    |
| Stability       | 3     | Government-backed agencies; well-established feeds             |
| Structure       | 3     | Standard GTFS-RT protobuf                                     |
| Identifiers     | 3     | GTFS-compatible IDs                                           |
| Additive Value  | 1     | Covered by existing GTFS-RT bridge — no new protocol territory|
| **Total**       | **15/18** |                                                           |

## Notes

- All three major Canadian cities are best covered as curated feed entries in the existing GTFS-RT bridge — they don't introduce new protocol territory.
- TransLink's RTTI (JSON REST) API is a more developer-friendly alternative to the raw GTFS-RT protobuf, with countdown timers and human-readable estimates.
- TTC's NextBus support means it's also coverable by the existing NextBus bridge.
- Other Canadian GTFS-RT feeds: OC Transpo (Ottawa), Calgary Transit, Edmonton Transit (ETS), Winnipeg Transit — all publish GTFS-RT.
- Canada has high GTFS/GTFS-RT adoption nationwide — the MobilityData organization (which maintains the GTFS spec) is based in Montreal.
