# Hong Kong Transit Open Data — KMB, MTR, and More

**Country/Region**: Hong Kong SAR, China
**Publisher**: KMB (Kowloon Motor Bus), MTR Corporation, DATA.GOV.HK, various operators
**API Endpoints**:
- KMB: `https://data.etabus.gov.hk/v1/transport/kmb/`
- MTR: `https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php`
- Citybus/NWFB: `https://rt.data.gov.hk/v1/transport/citybus/`
**Documentation**: https://data.gov.hk/en-data/dataset/ (search for transport)
**Protocol**: REST/JSON
**Auth**: None — all endpoints are open, no API key required
**Data Format**: JSON
**Update Frequency**: Real-time — ETAs update every 30–60 s
**License**: Open data (Hong Kong Government Open Data License)

## What It Provides

Hong Kong has a remarkably open transit data ecosystem, with multiple operators publishing real-time APIs through DATA.GOV.HK:

- **KMB (Kowloon Motor Bus)**: Hong Kong's largest bus operator — real-time ETAs for every stop, route data, stop locations. ~400 routes.
- **MTR (Mass Transit Railway)**: next-train times for all metro lines (Tuen Ma, Island, Tsuen Wan, Kwun Tong, etc.), delay status
- **Citybus / NWFB**: second-largest bus operator — real-time ETAs
- **Light Rail**: MTR Light Rail real-time schedule
- **Green Minibuses**: some real-time data available

## API Details

### KMB Bus API (confirmed working)

- `GET /v1/transport/kmb/route/` — all routes (returned full route list, 500+ entries)
- `GET /v1/transport/kmb/stop` — all bus stops
- `GET /v1/transport/kmb/stop-eta/{stopId}` — real-time ETA at a stop
- `GET /v1/transport/kmb/route-eta/{route}/{direction}/{service_type}` — ETA for a route

Clean JSON with versioned response: `{ "type": "StopETA", "version": "1.0", "generated_timestamp": "...", "data": [...] }`

### MTR Schedule API (confirmed working)

- `GET /v1/transport/mtr/getSchedule.php?line={line}&sta={station}` — next-train times
- Returns trains by direction (UP/DOWN) with platform, destination, minutes until arrival (`ttnt`), validity flag
- Lines: TML (Tuen Ma), TKL (Tseung Kwan O), EAL (East Rail), etc.

### Citybus/NWFB API

- `GET /v1/transport/citybus/route-eta/Citybus/{route}/{direction}` — real-time bus ETAs
- Same pattern as KMB

All APIs return JSON, no authentication required, no rate limits published.

## Freshness Assessment

Good. KMB and MTR ETAs are actively updated with live train/bus tracking data. MTR schedule returned next-train predictions with minute-level accuracy (tested: trains showing 4, 10, 16, 22 minute intervals). KMB ETAs are GPS-derived with good coverage across the network. The `generated_timestamp` in responses confirms data freshness.

## Entity Model

- **KMB Route**: route number, bound (O/I), service_type, orig/dest names (en/tc/sc trilingual)
- **KMB Stop ETA**: route, direction, stop sequence, ETA timestamp, remarks (en/tc/sc)
- **MTR Schedule**: line, station, direction (UP/DOWN), sequence, destination, platform, time, minutes_to_next_train, validity, delay status
- All entities include trilingual names: English, Traditional Chinese, Simplified Chinese
- **No standard IDs** — uses operator-specific stop/route identifiers

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Active real-time ETAs for bus and metro; confirmed live       |
| Openness        | 3     | No auth required — fully open APIs, no rate limits published  |
| Stability       | 2     | Government-backed (DATA.GOV.HK) but APIs can be informal     |
| Structure       | 2     | Clean JSON but multiple operator APIs with different schemas  |
| Identifiers     | 2     | Operator-specific IDs; no national standard                   |
| Additive Value  | 2     | Unique Asian megacity coverage; trilingual data                |
| **Total**       | **14/18** |                                                           |

## Notes

- The zero-auth, no-rate-limit approach makes Hong Kong's transit APIs among the most accessible in the world for prototyping and testing.
- Trilingual responses (English + Traditional Chinese + Simplified Chinese) are unique and valuable for international applications.
- MTR also publishes line status (normal/delay) and estimated wait times — useful for real-time disruption detection.
- Multiple operator APIs with different schemas is the main challenge — a bridge would need per-operator adapters or a unified wrapper.
- The Octopus card (Hong Kong's smart transit card) does not have a public API, but journey data through government sources covers the key real-time use cases.
- DATA.GOV.HK is the central portal for all Hong Kong government open data — transit is one of its strongest datasets.
