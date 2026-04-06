# Entur — Norway National Real-Time Transit

**Country/Region**: Norway (national)
**Publisher**: Entur AS (government-owned company managing Norwegian transit data)
**API Endpoint**: `https://api.entur.io/realtime/v1/rest/{et|vm|sx}`
**Documentation**: https://developer.entur.org/pages-real-time-intro
**Protocol**: SIRI 2.0 (Norwegian Profile) + GTFS-RT + GraphQL journey planner
**Auth**: No API key required — only a client name header (`ET-Client-Name`)
**Data Format**: XML (SIRI 2.0), Protobuf (GTFS-RT), JSON (GraphQL)
**Update Frequency**: Real-time — SIRI updates per vehicle journey change; GTFS-RT refreshed every ~15 s
**License**: NLOD 2.0 (Norwegian Licence for Open Government Data) — essentially CC BY compatible

## What It Provides

Entur is Norway's national journey planner and transit data platform. It aggregates real-time data from every public transit operator in Norway — buses, trams, ferries, trains, metro — and exposes it through three parallel APIs:

- **SIRI 2.0 (Norwegian Profile)**: ET (Estimated Timetable), VM (Vehicle Monitoring), SX (Situation Exchange) — the canonical real-time format
- **GTFS-RT**: Trip Updates, Vehicle Positions, Service Alerts — derived from the SIRI feeds
- **GraphQL Journey Planner**: Rich query API for stops, departures, trip planning with real-time estimates baked in

Coverage spans the entire country: Ruter (Oslo), Kolumbus (Stavanger), Skyss (Bergen), AtB (Trondheim), Vy/SJ (national rail), Flytoget (airport express), Go-Ahead, plus 20+ regional operators.

## API Details

### SIRI Lite (REST)

- `GET /realtime/v1/rest/et` — Estimated Timetable (delays, cancellations, extra trips)
- `GET /realtime/v1/rest/vm` — Vehicle Monitoring (positions, progress)
- `GET /realtime/v1/rest/sx` — Situation Exchange (disruptions, messages)

Parameters:
- `?requestorId={uuid}` — returns only changes since last request (incremental updates)
- `?maxSize={n}` — limit response size
- `?datasource={codespace}` — filter by operator (e.g., `RUT` for Ruter, `NSB` for Vy)

Supports publish/subscribe mode: register an HTTP endpoint to receive POST callbacks with SIRI updates — a genuine push mechanism.

### GTFS-RT

- `GET /realtime/v1/gtfs-rt/trip-updates` — full dataset (~7 MB protobuf)
- `GET /realtime/v1/gtfs-rt/vehicle-positions`
- `GET /realtime/v1/gtfs-rt/service-alerts`
- Filter by `?datasource={codespace}`

### GraphQL Journey Planner (v3)

- `POST /journey-planner/v3/graphql`
- Real-time departure boards, journey planning, stop search
- Example: query estimated departures at any stop/quay with `estimatedCalls`

No rate limits published — Entur asks only for a descriptive `ET-Client-Name` header. No API key needed.

## Freshness Assessment

Excellent. The SIRI feeds are the primary real-time source for all Norwegian transit. The GTFS-RT trip-updates feed returned a 7 MB protobuf in testing — that's a huge, actively-updated dataset covering every active vehicle journey in Norway. Vehicle positions update at operator-defined intervals (typically 10–30 s). The incremental `requestorId` mechanism means you can efficiently poll for just the changes.

## Entity Model

- **EstimatedVehicleJourney** (ET): trip with estimated arrival/departure per call, cancellation flags, extra journey markers
- **MonitoredVehicleJourney** (VM): vehicle position, bearing, delay, route progress, occupancy
- **PtSituationElement** (SX): disruption with affected stops/lines, severity, validity period, multilingual text
- All references use NeTEx/NSR identifiers (`NSR:StopPlace:*`, `NSR:Quay:*`, `RUT:Line:*`)
- GraphQL entities: `StopPlace`, `Quay`, `EstimatedCall`, `ServiceJourney`, `Line`, `Authority`

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 3     | Full national real-time: ET, VM, SX for 30+ operators        |
| Openness        | 3     | No API key needed — just a client name header. NLOD license  |
| Stability       | 3     | Government-backed platform, versioned APIs, years of operation|
| Structure       | 3     | SIRI 2.0 Norwegian Profile + GTFS-RT + GraphQL — triple format|
| Identifiers     | 3     | NeTEx/NSR national stop registry, standardized line/operator refs|
| Additive Value  | 3     | Native SIRI with pub/sub — covers an entire country, no auth friction|
| **Total**       | **18/18** |                                                           |

## Notes

- This is arguably the most open and well-designed national transit API in the world. No API key, three parallel formats, pub/sub support, incremental updates, full national coverage.
- The Norwegian SIRI Profile is shared with Sweden (Trafiklab uses the same Nordic profile). A SIRI bridge built against Trafiklab would work against Entur with minimal changes.
- The pub/sub mechanism (register an HTTP POST endpoint) is architecturally interesting — it's a webhook-style push that could feed directly into a CloudEvents bridge.
- Ruter (Oslo) data is accessible both through Entur and through Ruter's own APIs, but Entur is the canonical aggregation point.
- Entur also provides a Geocoder API, NeTEx static data exports, and a national stop place registry (NSR).
- The GraphQL journey planner is powered by OpenTripPlanner 2 — one of the most advanced OTP deployments globally.
