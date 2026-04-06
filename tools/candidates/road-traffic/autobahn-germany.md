# Autobahn API (Germany)

**Country/Region**: Germany
**Publisher**: Die Autobahn GmbH des Bundes
**API Endpoint**: `https://verkehr.autobahn.de/o/autobahn`
**Documentation**: https://autobahn.api.bund.dev/
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Current state snapshots (ETag support for conditional requests)
**License**: German government open data

## What It Provides

The Autobahn API provides current state data for the German motorway (Autobahn) network including roadworks, traffic warnings, closures, entry/exit closures, weight-limit restrictions, lorry parking metadata, electric charging station metadata, and webcam feeds. Covers all German Autobahns.

## API Details

See the existing `autobahn/` directory in this repository for full details.

```
GET https://verkehr.autobahn.de/o/autobahn
```
Returns list of all Autobahn roads (A1, A2, A3, ...).

Per-road resources:
```
GET https://verkehr.autobahn.de/o/autobahn/{road}/services/roadworks
GET https://verkehr.autobahn.de/o/autobahn/{road}/services/warning
GET https://verkehr.autobahn.de/o/autobahn/{road}/services/closure
GET https://verkehr.autobahn.de/o/autobahn/{road}/services/electric_charging_station
GET https://verkehr.autobahn.de/o/autobahn/{road}/services/parking_lorry
GET https://verkehr.autobahn.de/o/autobahn/{road}/services/webcam
```

## Freshness Assessment

Current state snapshots with ETag support for conditional GETs. The existing bridge in `autobahn/` handles polling, diffing, and change event generation.

## Entity Model

See `autobahn/EVENTS.md` for the full event model.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Current state snapshots; no push/streaming |
| Openness | 3 | No auth, open data |
| Stability | 3 | Government API |
| Structure | 3 | Clean JSON |
| Identifiers | 3 | Stable upstream identifiers |
| Additive Value | 3 | Already implemented |
| **Total** | **17/18** | |

## Notes

- **ALREADY PLANNED AND IMPLEMENTED** — A full bridge exists in the `autobahn/` directory of this repository. This document is included for completeness and cross-reference only.
- The bridge supports CloudEvents output to Kafka, Azure Event Hubs, and Fabric Event Streams.
- Uses ETag-based conditional GETs and local state diffing to generate appeared/updated/resolved events.
