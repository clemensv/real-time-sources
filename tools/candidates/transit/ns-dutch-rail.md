# NS (Nederlandse Spoorwegen) — Dutch Railways API

**Country/Region**: Netherlands
**Publisher**: NS (Nederlandse Spoorwegen)
**API Endpoint**: `https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/`
**Documentation**: https://apiportal.ns.nl/ (login required to browse full API docs)
**Protocol**: REST (JSON)
**Auth**: API Key (free registration, subscription required)
**Data Format**: JSON
**Update Frequency**: Real-time — live departures, disruptions updated continuously
**License**: NS Open Data (free for non-commercial use; commercial use requires agreement)

## What It Provides

NS provides a comprehensive REST API covering Dutch rail operations:

- **Live departures/arrivals** per station — real-time predicted times, platforms, delays
- **Disruptions** — current and planned service disruptions with affected routes
- **Journey planner** — multimodal trip planning with real-time awareness
- **Train positions** — GPS positions of trains (via the "Ns-App" API product)
- **Station information** — facilities, entrances, tracks
- **Pricing** — fare information

The API powers the official NS app and is the authoritative source for Dutch rail real-time data.

## API Details

Key endpoints (under the "Reisinformatie API" and "NS App" products):

- `GET /api/v2/departures?station={code}` — live departures for a station
- `GET /api/v2/arrivals?station={code}` — live arrivals for a station
- `GET /api/v2/disruptions` — current disruptions (type, cause, affected routes)
- `GET /api/v2/trips` — journey planning with real-time predictions
- Virtual train API (GPS positions) — available in NS App product

Response format is JSON. Station codes follow the NS/Dutch rail coding system (e.g., `UT` for Utrecht Centraal, `ASD` for Amsterdam Centraal).

The API portal uses Azure API Management — subscribe to a "product" (API bundle) to get keys. Multiple products:
- "Ns-App" — includes departures, arrivals, disruptions, trips, prices
- Free tier available; rate limits apply

## Freshness Assessment

Good. Departure/arrival predictions are real-time with sub-minute latency. Disruption feed is updated as events occur. GPS positions update every few seconds. However, the API is poll-based REST — no push or streaming option.

## Entity Model

- **Departure/Arrival**: trainNumber, direction, plannedTime, actualTime, delay, platform, routeStations, cancelled flag
- **Disruption**: id, type (calamity, disruption, maintenance), title, description, start/end times, affectedTrainSeries
- **Journey/Trip**: legs with departure/arrival stations, times, transfers, fare
- **Station**: code, name, lat/lon, country, facilities
- Train identified by train number + date; stations by NS station code

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Real-time departures, live train positions                    |
| Openness        | 2     | Free registration but non-commercial license; commercial needs agreement |
| Stability       | 3     | Official NS platform, well-maintained, versioned API          |
| Structure       | 2     | Proprietary JSON schema — clean but NS-specific               |
| Identifiers     | 2     | NS station codes (not UIC/IFOPT); train numbers standard      |
| Additive Value  | 2     | Unique Dutch rail source; REST/JSON is well-handled by GTFS bridge already |
| **Total**       | **14/18** |                                                           |

## Notes

- The licensing is the main concern — "free for non-commercial use" may limit some applications. Commercial use requires contacting NS.
- NS also publishes GTFS static data on the NDOV loket (Dutch national transport data warehouse), but the real-time API is the proprietary REST interface.
- The NDOV loket (`ndovloket.nl`) provides raw data feeds in KV6/KV17 (Dutch transit protocols) for bus/tram/metro operators — a separate, more complex data source.
- API documentation requires login to view, making initial exploration harder.
- Train positions (GPS) are a high-value differentiator not available in GTFS-RT for Dutch rail.
