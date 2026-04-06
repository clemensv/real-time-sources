# Finland Digitraffic Maritime REST API

**Country/Region**: Finland (+ Baltic Sea coverage)
**Publisher**: Fintraffic / Finnish Transport Infrastructure Agency
**API Endpoint**: `https://meri.digitraffic.fi/api/ais/v1/locations`
**Documentation**: https://meri.digitraffic.fi/ (Finnish), https://www.digitraffic.fi/en/marine-traffic/
**Protocol**: REST (+ MQTT WebSocket for streaming, already covered separately)
**Auth**: None (fully open, no registration required)
**Data Format**: JSON (GeoJSON FeatureCollections)
**Update Frequency**: Real-time (seconds-level for REST polls, continuous for MQTT)
**License**: CC 4.0 BY (Creative Commons Attribution)

## What It Provides

The Finnish Digitraffic Maritime platform exposes AIS vessel data for the Baltic Sea region
via both MQTT (already covered in `digitraffic-maritime/`) and REST APIs. The REST API provides
complementary snapshot access to the same data: vessel positions, vessel metadata, and port
call information.

REST endpoints cover:
- **AIS positions**: All current vessel locations as GeoJSON
- **AIS vessel metadata**: Static vessel data (name, callsign, IMO, type, dimensions)
- **Port calls**: Real-time port visit data with ETAs, berth assignments, agent info
- **SSE locations**: Server-Sent Events endpoint for real-time position streaming

## API Details

Key REST endpoints (no auth required):

| Endpoint | Description | Verified |
|---|---|---|
| `GET /api/ais/v1/locations` | All vessel positions (GeoJSON FeatureCollection) | ✅ Live |
| `GET /api/ais/v1/locations?mmsi=NNNNNNNNN` | Single vessel position | ✅ Live |
| `GET /api/ais/v1/vessels` | All vessel metadata (name, type, IMO, etc.) | ✅ Live |
| `GET /api/port-call/v1/port-calls` | Current port calls with ETA/ATA | ✅ Live |

Position response (GeoJSON):
```json
{
  "type": "FeatureCollection",
  "dataUpdatedTime": "2026-04-06T10:23:33Z",
  "features": [
    {
      "mmsi": 241930000,
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [20.86432, 58.478048]
      },
      "properties": {
        "mmsi": 241930000,
        "sog": 10.2,
        "cog": 208.8,
        "navStat": 0,
        "rot": 1,
        "posAcc": false,
        "raim": false,
        "heading": 210,
        "timestamp": 41,
        "timestampExternal": 1774756004058
      }
    }
  ]
}
```

Vessel metadata response:
```json
{
  "callSign": "SVDX9",
  "destination": "DKSKA",
  "draught": 126,
  "eta": 258240,
  "imo": 9987029,
  "mmsi": 241930000,
  "name": "AISOPOS",
  "posType": 1,
  "referencePointA": 211,
  "referencePointB": 39,
  "referencePointC": 33,
  "referencePointD": 11,
  "shipType": 80,
  "timestamp": 1774743475357
}
```

Port call data is exceptionally rich — includes vessel details, agent information, berth
assignments, actual/estimated arrival and departure times, IMO declarations, cargo info,
passenger/crew counts, and security levels.

## Freshness Assessment

Excellent. The REST API returns the same real-time data as the MQTT streams. The
`dataUpdatedTime` field confirms data is updated within seconds. The `timestampExternal` on
position records indicates the actual time the AIS message was received.

The port call data is also live — ATA (Actual Time of Arrival) and ATD (Actual Time of
Departure) are updated in real-time by agents and port systems.

## Entity Model

Positions (GeoJSON Feature):
- `mmsi`, `sog`, `cog`, `navStat`, `rot`, `posAcc`, `raim`, `heading`, `timestamp`, `timestampExternal`

Vessel metadata (flat JSON):
- `mmsi`, `name`, `callSign`, `imo`, `shipType`, `destination`, `eta`, `draught`
- `referencePointA/B/C/D` (vessel dimensions), `posType`

Port calls (nested JSON):
- `portCallId`, `vesselName`, `mmsi`, `imoLloyds`, `nationality`
- `portToVisit`, `prevPort`, `nextPort`
- `portAreaDetails[]`: berth, ETA/ETD, ATA/ATD with sources and timestamps
- `agentInfo[]`: name, EDI number, role
- `imoInformation[]`: crew/passenger counts, cargo declarations

Identifiers: MMSI (primary key for positions), IMO (`imoLloyds` in port calls), callsign, UN/LOCODE for ports.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Real-time, verified live with current timestamps |
| Openness | 3 | No auth needed, CC 4.0 BY license |
| Stability | 3 | Government infrastructure, part of national transport data platform |
| Structure | 3 | GeoJSON for positions, rich nested JSON for port calls |
| Identifiers | 3 | MMSI, IMO, callsign, UN/LOCODE all present |
| Additive Value | 2 | MQTT already covered; REST adds port call data + snapshot access |

**Total: 17/18**

## Notes

- The REST API complements the MQTT integration already in `digitraffic-maritime/`. While MQTT
  gives continuous streaming, REST enables:
  - One-shot snapshots of all vessels (useful for initialization)
  - Rich port call data (not available via MQTT)
  - Per-vessel lookups by MMSI
- The port call API is exceptionally detailed — arguably the richest open port call dataset
  available anywhere. It includes agent information, cargo declarations, crew counts, berth
  assignments, and security levels.
- Coverage extends across the Baltic Sea (not just Finnish territorial waters) — the AIS
  positions include vessels from Sweden, Estonia, Russia, Denmark, Germany, Poland, and Latvia.
- The `dataUpdatedTime` field was confirmed live: `2026-04-06T10:23:33Z` — data is fresh.
- Consider integrating the REST endpoints alongside the existing MQTT integration for the
  port call enrichment alone — that data is uniquely valuable.
