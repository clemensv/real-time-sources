# IVAO Whazzup Tracker API

**Country/Region**: Global (virtual aviation network)
**Publisher**: IVAO (International Virtual Aviation Organisation)
**API Endpoint**: `https://api.ivao.aero/v2/tracker/whazzup`
**Documentation**: https://wiki.ivao.aero/en/home/devops/api
**Protocol**: REST (JSON)
**Auth**: None for whazzup feed (OAuth2 available for member APIs)
**Data Format**: JSON
**Update Frequency**: Real-time (~15-30 second refresh)
**License**: IVAO data policy (open read access for tracker data)

## What It Provides

IVAO is the second-largest virtual aviation network (after VATSIM), connecting flight
simulation pilots and virtual air traffic controllers worldwide. The Whazzup API provides a
real-time snapshot of all connected clients — pilots with full position tracking and flight
plans, and controllers with frequencies and ratings.

At the time of probing: 425 pilots and 47 controllers connected. IVAO tends to have higher
activity during European evenings and organized events.

Data includes:
- **Pilots**: Position (lat/lon/alt), groundspeed, heading, transponder, flight state
  (Boarding, Departing, En Route, Approaching, Arrived), flight plan with full ICAO route,
  aircraft type, simulator type, arrival/departure distances
- **Controllers**: Callsign, frequency, ATIS, rating, position type
- **Servers**: Network server status and connections
- **Connection statistics**: Total, by type, 24h unique users

## API Details

Primary endpoint: `GET https://api.ivao.aero/v2/tracker/whazzup`

No authentication required. Returns a comprehensive JSON document.

Response structure:
```json
{
  "updatedAt": "2026-04-06T11:15:12Z",
  "servers": [...],
  "voiceServers": [...],
  "connections": {
    "total": 476,
    "supervisor": 3,
    "atc": 46,
    "observer": 4,
    "pilot": 426,
    "worldTour": 99,
    "followMe": 0,
    "uniqueUsers24h": 4279
  },
  "clients": {
    "pilots": [...],
    "atcs": [...]
  }
}
```

Pilot record (verified):
```json
{
  "id": 62071337,
  "userId": 776359,
  "callsign": "EK203",
  "serverId": "WS1-EUW2",
  "softwareTypeId": "altitude/win",
  "softwareVersion": "1.13.0.33",
  "rating": 2,
  "createdAt": "2026-04-05T20:25:30.000Z",
  "time": 53288,
  "pilotSession": {
    "simulatorId": "X-Plane11",
    "textureId": 23836
  },
  "lastTrack": {
    "altitude": 40029,
    "altitudeDifference": 0,
    "arrivalDistance": null,
    "departureDistance": null,
    "groundSpeed": 471,
    "heading": 231,
    "latitude": 28.649992,
    "longitude": 130.06421,
    "onGround": false,
    "state": "En Route",
    "timestamp": "2026-04-06T11:13:36.000Z",
    "transponder": 2000,
    "transponderMode": "N",
    "time": 53287
  },
  "flightPlan": {
    "aircraftId": "B772",
    "departureId": "LEMD",
    "arrivalId": "SAEZ",
    "alternativeId": "SAZB",
    "route": "CCS DCT KOMUT/M084F320 ...",
    "remarks": "PBN/A1B1C1D1L1O1S2 ...",
    "speed": "N0490",
    "level": "F310",
    "flightRules": "I",
    "eet": 45480,
    "endurance": 53040,
    "peopleOnBoard": 269,
    "aircraft": {
      "icaoCode": "B772",
      "model": "777-200ER",
      "wakeTurbulence": "H",
      "military": "civil"
    }
  }
}
```

Key differentiators from VATSIM:
- `lastTrack.state` field: Boarding, Departing, Climbing, Cruising, En Route, Descending,
  Approaching, Arrived — provides flight phase information
- `lastTrack.arrivalDistance` / `departureDistance` — distance to destination/origin in nm
- `lastTrack.altitudeDifference` — climb/descent rate indicator
- `pilotSession.simulatorId` — which flight simulator (MSFS, X-Plane, P3D)
- `flightPlan.aircraft` — nested object with ICAO code, model name, wake turbulence category
- `time` — session duration in seconds

## Freshness Assessment

Excellent. The `updatedAt` timestamp confirms the feed updates approximately every 15-30
seconds. Position tracks include individual timestamps per pilot. The network runs 24/7
with global participation.

Verified live: 423 pilots, 47 controllers, 4,279 unique users in 24h.

## Entity Model

- **Pilot**: id, userId, callsign, serverId, softwareTypeId, softwareVersion, rating,
  createdAt, time, pilotSession{}, lastTrack{}, flightPlan{}
- **Track**: altitude, altitudeDifference, arrivalDistance, departureDistance, groundSpeed,
  heading, latitude, longitude, onGround, state, timestamp, transponder, transponderMode
- **FlightPlan**: aircraftId, departureId, arrivalId, alternativeId, route, remarks, speed,
  level, flightRules, flightType, eet, endurance, peopleOnBoard, aircraft{}
- **ATC**: id, userId, callsign, serverId, rating, createdAt, atcSession{}, lastTrack{}, atis{}

Identifiers: IVAO user ID, session ID, callsign, ICAO airport codes, aircraft ICAO type codes.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | ~15-30 second updates, verified live |
| Openness | 3 | No auth for whazzup endpoint |
| Stability | 2 | IVAO operational since 1998, but smaller community than VATSIM |
| Structure | 3 | Excellent JSON structure, nested objects, flight phases |
| Identifiers | 3 | ICAO codes, user IDs, session IDs |
| Additive Value | 1 | Simulated aviation, but richer track metadata than VATSIM |

**Total: 15/18**

## Notes

- IVAO's data model is arguably richer than VATSIM's for tracking purposes — the flight
  state machine (Boarding → Departed → En Route → Approaching → Arrived), distance-to-
  destination, and altitude difference fields provide derived intelligence not available
  in the raw VATSIM feed.
- The nested `aircraft` object with model name and wake turbulence category is a nice touch
  that VATSIM doesn't provide in the data feed.
- IVAO uses a different client application (Altitude) from VATSIM (various: vPilot, xPilot,
  swift). The `softwareTypeId` and `softwareVersion` fields track this.
- Smaller network than VATSIM (~400 vs ~1,500 concurrent pilots typically), but still a
  substantial real-time data source.
- IVAO also provides a v2 tracker API with additional endpoints for specific users, sessions,
  and historical data, but those require API key registration.
- The `worldTour` connection count indicates event participation — IVAO runs organized
  multi-leg flight events that generate concentrated traffic bursts.
