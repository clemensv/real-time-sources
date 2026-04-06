# MBTA V3 API (Boston)

**Country/Region**: United States (Massachusetts)
**Publisher**: Massachusetts Bay Transportation Authority (MBTA)
**API Endpoint**: `https://api-v3.mbta.com/`
**Documentation**: https://www.mbta.com/developers/v3-api and https://api-v3.mbta.com/docs/swagger/index.html
**Protocol**: REST (JSON:API) with Server-Sent Events (SSE) streaming
**Auth**: API Key (free, recommended — 1,000 req/min with key)
**Data Format**: JSON (JSON:API specification)
**Update Frequency**: Real-time — predictions update every 10–30 seconds; SSE streaming available
**License**: Public domain (MassDOT open data)

## What It Provides

The MBTA V3 API is widely considered one of the best-designed public transit APIs in the world. It covers all MBTA services:

- **Subway** (Red, Orange, Blue, Green Lines) — real-time predictions, vehicle positions
- **Commuter Rail** — 12 lines, real-time predictions
- **Bus** — 170+ routes, real-time predictions and GPS positions
- **Ferry** — real-time
- **Alerts** — service disruptions, elevator/escalator outages, detours

The API presents GTFS and GTFS-RT data through a clean JSON:API interface with powerful filtering, sorting, includes, and — notably — **Server-Sent Events (SSE) streaming** for push-based real-time updates.

## API Details

Key endpoints:

- `GET /predictions?filter[stop]=place-sstat` — real-time predictions at South Station
- `GET /vehicles?filter[route]=Red` — vehicle positions on the Red Line
- `GET /alerts` — current service alerts
- `GET /schedules?filter[route]=Red` — planned schedule
- `GET /routes`, `/stops`, `/trips`, `/lines` — reference data

**Streaming (SSE)**: Any endpoint can be streamed by adding `Accept: text/event-stream` header. The server pushes incremental updates as `add`, `update`, `remove` events. This is a true push mechanism — no polling needed.

JSON:API features:
- `?include=stop,route,trip` — embed related resources
- `?filter[...]` — filter by route, stop, direction, time
- `?sort=...` — sort results
- `?fields[prediction]=arrival_time,departure_time` — sparse fieldsets

Rate limits: 1,000 req/min with API key (can request increase); 20 req/min without key.

## Freshness Assessment

Excellent. Predictions are derived from MBTA's real-time systems and update every 10–30 seconds. The SSE streaming option makes this one of the few transit APIs offering true push-based real-time. Vehicle positions include lat/lon, bearing, speed, and current stop.

## Entity Model

- **Prediction**: arrival/departure time, status, direction, schedule relationship — links to stop, route, trip, vehicle
- **Vehicle**: latitude, longitude, bearing, speed, current_status (in_transit_to, stopped_at), occupancy_status
- **Alert**: effect, severity, lifecycle, header/description text, informed entities (routes, stops, trips)
- **Schedule**: planned stop_time with arrival/departure
- **Route**, **Stop**, **Trip**, **Line** — reference entities following GTFS model
- All identified by GTFS-compatible IDs

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Real-time predictions + SSE streaming = true push            |
| Openness        | 3     | Public domain, free API key, generous limits                  |
| Stability       | 3     | Versioned API (V3), swagger-documented, long-running          |
| Structure       | 3     | JSON:API — standardized, self-describing, rich filtering     |
| Identifiers     | 3     | GTFS-compatible IDs throughout                                |
| Additive Value  | 2     | Architecturally interesting (SSE); but GTFS-RT bridge covers data |
| **Total**       | **17/18** |                                                           |

## Notes

- The SSE streaming capability is the standout feature — it turns a REST API into a real-time event stream. Each SSE event contains a JSON:API resource with an `event` type of `reset`, `add`, `update`, or `remove`. This maps naturally to CloudEvents.
- JSON:API is a formal spec (jsonapi.org) with libraries in every language — parsing is straightforward.
- The `include` mechanism is powerful: a single request for predictions can embed stop, route, trip, and vehicle data.
- MBTA also publishes raw GTFS-RT protobuf feeds (covered by the existing GTFS-RT bridge), but the V3 API adds value via SSE streaming, richer filtering, and the JSON:API structure.
- The API is well-documented with interactive Swagger UI.
- Good test bed for an SSE-to-CloudEvents bridge pattern.
