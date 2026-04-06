# VATSIM Live Data Feed

**Country/Region**: Global (virtual aviation network)
**Publisher**: VATSIM (Virtual Air Traffic Simulation Network)
**API Endpoint**: `https://data.vatsim.net/v3/vatsim-data.json`
**Documentation**: https://github.com/vatsimnetwork/developer-info/wiki, https://status.vatsim.net/
**Protocol**: REST (JSON polling)
**Auth**: None (fully open, no registration required for data feed)
**Data Format**: JSON
**Update Frequency**: Real-time (~15-second refresh cycles)
**License**: Open (see VATSIM data policy)

## What It Provides

VATSIM is the world's largest virtual aviation network, connecting flight simulation pilots
and virtual air traffic controllers in a shared, real-time simulated airspace. At any given
moment, 1,000–2,000+ "aircraft" are flying realistic routes with accurate flight plans,
transponder codes, and ATC assignments. Controllers staff virtual positions from clearance
delivery to center/ARTCC.

This is not real aviation — but the data feed is an extraordinarily rich real-time streaming
source with the same structure as real ATC data. For real-time data integration projects,
it's a goldmine: always active, always available, no auth, structured JSON.

Data includes:
- **Pilots**: Position (lat/lon/alt), groundspeed, heading, transponder, QNH, full flight
  plans (departure, arrival, alternate, route, cruise altitude, EET, fuel endurance,
  persons on board), callsign, rating, logon time
- **Controllers**: Callsign, frequency, facility type, ATIS text, logon time, rating
- **ATIS stations**: Airport ATIS text and frequency
- **Prefiles**: Filed flight plans not yet active
- **Servers**: Network infrastructure status
- **General**: Connected clients count, update timestamp

## API Details

Status file: `https://status.vatsim.net/` — lists data feed URLs.

Primary data feed: `GET https://data.vatsim.net/v3/vatsim-data.json`

No authentication. No rate limit documentation, but the `reload` field (value: 1) suggests
a 1-minute minimum poll interval is recommended. The feed updates approximately every 15 seconds.

VATSIM METAR: `https://metar.vatsim.net/metar.php?id={ICAO}` — returns real-world METARs used
in the simulation.

Verified live response:
```json
{
  "general": {
    "version": 3,
    "reload": 1,
    "update": "20260406111230",
    "update_timestamp": "2026-04-06T11:12:30.685Z",
    "connected_clients": 1791,
    "unique_users": 1699
  },
  "pilots": [...],
  "controllers": [...],
  "atis": [...],
  "prefiles": [...],
  "servers": [...]
}
```

Pilot record structure (verified):
```json
{
  "cid": 1575954,
  "callsign": "JAL24",
  "server": "GERMANY3",
  "pilot_rating": 0,
  "military_rating": 0,
  "latitude": 35.70999,
  "longitude": 141.44817,
  "altitude": 39990,
  "groundspeed": 335,
  "transponder": "0275",
  "heading": 282,
  "qnh_i_hg": 29.91,
  "qnh_mb": 1013,
  "flight_plan": {
    "flight_rules": "I",
    "aircraft": "A35K/H-SDE2E3GHIJ3J4J5LM1ORWXY/LB1D1",
    "aircraft_short": "A35K",
    "departure": "ESSA",
    "arrival": "RJAA",
    "alternate": "RJSN",
    "cruise_tas": "501",
    "altitude": "34000",
    "deptime": "2130",
    "enroute_time": "1411",
    "fuel_time": "1607",
    "remarks": "PBN/A1B1C1D1L1O1S2 DOF/260405 REG/JA01WJ ...",
    "route": "RESNA DCT UMLAX DCT OSKOK ..."
  },
  "logon_time": "2026-04-05T19:05:03Z",
  "last_updated": "2026-04-06T11:12:26Z"
}
```

Controller record includes: cid, callsign, frequency, facility, rating, text_atis[], logon_time, last_updated.

## Freshness Assessment

Excellent. The data feed updates approximately every 15 seconds. The `update_timestamp` in
the response confirms the exact moment the snapshot was generated. Pilot positions update
in near-real-time as simulators report to the VATSIM servers.

Verified live: 1,552 pilots, 145 controllers, 91 ATIS stations, 169 prefiled flight plans
at time of probe.

## Entity Model

- **Pilot**: cid, callsign, server, latitude, longitude, altitude, groundspeed, heading,
  transponder, qnh_i_hg, qnh_mb, pilot_rating, military_rating, logon_time, last_updated,
  flight_plan{}
- **Flight Plan**: flight_rules, aircraft, aircraft_short, departure, arrival, alternate,
  cruise_tas, altitude, deptime, enroute_time, fuel_time, remarks, route, revision_id,
  assigned_transponder
- **Controller**: cid, callsign, frequency, facility, rating, text_atis[], logon_time,
  last_updated, server
- **ATIS**: cid, callsign, frequency, atis_code, text_atis[]

Identifiers: CID (VATSIM member ID), callsign (airline/flight designator), ICAO airport
codes (departure/arrival/alternate), aircraft type codes (ICAO format).

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | ~15-second update cycles, verified live |
| Openness | 3 | No auth, no registration for data feed |
| Stability | 3 | VATSIM operational since 2001, v3 JSON feed is stable |
| Structure | 3 | Clean JSON, well-structured pilot/controller records |
| Identifiers | 3 | CID, callsigns, ICAO codes throughout |
| Additive Value | 1 | Simulated aviation — interesting but not real traffic |

**Total: 16/18**

## Notes

- The flight plan data is remarkably detailed — these are realistic ICAO-format flight plans
  with SIDs, STARs, airways, waypoints, equipment suffixes, PBN capabilities, and RALT
  (re-clearance alternates). Many use SimBrief for planning, producing professional-grade
  route data.
- At ~1,500 concurrent pilots, the data volume is comparable to a small country's domestic
  aviation. Traffic patterns follow real-world airline schedules and event-driven surges.
- The VATSIM METAR endpoint returns real-world weather data — this is the same actual weather
  that real pilots use, injected into the simulation.
- Virtual ATC staffing creates realistic controlled airspace — controllers staff positions
  from clearance delivery through center, mirroring real-world facility structures.
- The feed uses VATSIM v3 JSON format. An older text-based format exists but is deprecated.
- Could serve as an excellent test data source for aviation data processing pipelines —
  the structure mirrors real-world ATC data without privacy/security concerns.
- VATSIM also operates an OAuth2-based API for member data, but the live data feed requires
  no authentication whatsoever.
