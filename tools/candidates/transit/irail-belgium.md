# iRail Belgium Rail API

**Country/Region**: Belgium
**Publisher**: iRail (open Belgian rail data platform built on NMBS/SNCB data)
**API Endpoint**: `https://api.irail.be/`
**Documentation**: https://docs.irail.be/
**Protocol**: REST (JSON, XML, CSV)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time / near-real-time
**License**: Open Belgian rail data access; check iRail terms and attribution expectations

## What It Provides

iRail exposes Belgian national rail information through a simple public API with no authentication. It covers station metadata, live departure and arrival boards, train detail, point-to-point connections, and current disturbances. The API is already normalized enough to be pleasant to consume, but still retains stable rail identifiers such as NMBS station IDs and train IDs like `BE.NMBS.IC1832`.

This is a strong candidate because it is national in scope, zero-auth, operationally simple, and more direct than going through a generic GTFS-RT feed. It looks particularly good for a rail-focused bridge that emits liveboard updates, train movement state, and disruption events.

## API Details

Documented endpoints include:

- `GET /stations?format=json` - full station list with station IDs, names, and coordinates
- `GET /liveboard/?station={name}&format=json` - departures and arrivals for a station
- `GET /connections/?from={from}&to={to}&format=json` - trip connections with live timing
- `GET /vehicle/?id={train_id}&format=json` - train detail, stops, delays, platform information
- `GET /disturbances/?format=json` - current disruptions and works

Observed payload characteristics:

- Station identifiers like `BE.NMBS.008821006`
- Train identifiers like `BE.NMBS.IC3033`
- Delay values in seconds
- Platform and cancellation state included inline
- Disturbance payloads with titles, validity windows, and links

Operational note from the docs: the public rate limit is 3 requests per second per IP, with a small burst allowance. The docs also ask consumers to send a meaningful `User-Agent`.

## Freshness Assessment

Good. The API is used for liveboards and train details, so delay and platform data changes close to real time. It is still a poll-based API rather than a push feed, but it is fast enough for a low-latency rail bridge if station polling is scoped carefully and backed by caching and rate-limit awareness.

## Entity Model

- **Station** - NMBS station ID, multilingual names, coordinates
- **Liveboard entry** - station, train, direction, platform, delay, canceled/left flags
- **Vehicle** - train ID with ordered stop list, delays, and platform data
- **Connection** - journey from origin to destination with possible vias
- **Disturbance** - disruption or works notice with start/end validity

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Liveboards, vehicle detail, and disturbances are near-real-time |
| Openness | 3 | No auth, public docs, simple HTTPS API |
| Stability | 2 | Mature public API, but community-run rather than direct operator API management |
| Structure | 3 | Clean JSON with consistent nested entities |
| Identifiers | 3 | Strong station IDs and train IDs |
| Additive Value | 2 | National Belgian rail source; more targeted than generic GTFS-RT |
| **Total** | **16/18** | |

## Notes

- The API looks ideal for a poll-based rail bridge keyed by station ID or train ID.
- `disturbances` could be modeled as a separate event family from liveboard or train-state events.
- Because the API is rate-limited, a naive all-stations polling strategy would not scale. The right design is probably focused station sets, train detail enrichment from liveboard discoveries, or a disruption-first bridge.
- This is not a direct NMBS/SNCB operator API, which is both a strength and a limitation: the API is easy to consume, but there is one more layer between us and the upstream operational systems.
