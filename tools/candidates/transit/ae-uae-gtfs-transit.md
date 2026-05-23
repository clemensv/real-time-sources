# UAE Public Transit GTFS-RT (Dubai Metro, Tram, Bus + Abu Dhabi Bus)

- **Country/Region**: United Arab Emirates / Dubai + Abu Dhabi
- **Endpoint**: **UNKNOWN** — requires discovery
- **Protocol**: GTFS-RT (General Transit Feed Specification - Realtime)
- **Auth**: Unknown
- **Format**: Protobuf over HTTP
- **Freshness**: Real-time (vehicle positions every 10–30 seconds, trip updates every 30–60 seconds)
- **Docs**:
  - Dubai RTA: https://www.rta.ae/
  - Abu Dhabi DoT: https://dot.abudhabi.ae/
  - GTFS-RT Spec: https://gtfs.org/realtime/
- **Score**: **TBD** (cannot score without endpoint; if found: 15–16/18)

## Overview

The UAE operates extensive public transit systems in Dubai and Abu Dhabi:

### Dubai (Roads and Transport Authority - RTA)

**Dubai Metro**:
- **Red Line**: 52 km, 29 stations (Rashidiya ↔ UAE Exchange, plus Jebel Ali extension)
- **Green Line**: 23 km, 20 stations (Etisalat ↔ Creek)
- **Technology**: Fully automated (driverless), world's longest driverless metro network
- **Ridership**: 200+ million passengers/year (pre-pandemic)

**Dubai Tram**:
- 10.6 km, 11 stops (Al Sufouh tram corridor along Jumeirah Beach)
- Integrated with Metro Red Line at DAMAC/Dubai Marina stations

**Dubai Bus**:
- 119 routes, 1,500+ buses
- Feeder buses for Metro, intercity buses to other emirates
- Includes airport shuttle routes

**Inter-modal Integration**:
- Nol card (contactless smart card) works across Metro, Tram, Bus
- Real-time trip planning via S'hail app (RTA's multi-modal journey planner)

### Abu Dhabi (Department of Transport - DoT)

**Abu Dhabi Bus**:
- "Darb" branded network: 80+ routes, 900+ buses
- Coverage: Abu Dhabi city, Al Ain, Al Dhafra region
- Integrated Transport Centre (ITC) operates the network

**Future**:
- **Etihad Rail**: Passenger rail network launching 2025–2026 (Abu Dhabi ↔ Dubai ↔ Northern Emirates)
- **Abu Dhabi Metro**: Planned but timeline unclear

### Other Emirates
- **Sharjah**: Limited bus network (Mowasalat)
- **Ajman, RAK**: Minimal public transit

## Why GTFS-RT Is a High-Value Candidate

1. **GTFS-RT is a global standard** — same protocol as 1,400+ transit agencies worldwide; repo already has a `gtfs` bridge
2. **Real-time vehicle positions** — Metro trains, Trams, and Buses broadcast GPS coordinates every 10–30 seconds
3. **Trip updates** — delays, cancellations, estimated arrival times
4. **Service alerts** — line closures, elevator outages, route changes
5. **High volume** — Dubai Metro alone has ~50 trains in operation during peak hours
6. **Strategic value** — Dubai Metro is an iconic infrastructure project (driverless, world records); Abu Dhabi is expanding transit
7. **Smart city alignment** — RTA and DoT market themselves as smart mobility leaders

## Endpoint Discovery Required

### 1. Check MobilityData GTFS Catalog

The global GTFS catalog at MobilityData was already checked (earlier in discovery). Result:
- **NO** UAE GTFS-RT feeds found in the public catalog
- This means RTA and Abu Dhabi DoT either:
  - Do not publish GTFS-RT
  - Publish GTFS-RT but only to partners (Google Maps, Moovit, etc.) under license
  - Have not registered with MobilityData

### 2. Check RTA / S'hail App

**S'hail** is RTA's official journey planning app (iOS/Android). It shows real-time Metro/Tram/Bus locations and ETAs. This proves RTA has real-time vehicle tracking internally.

**Reverse-engineering strategy**:
- Install S'hail app
- Use mitmproxy or Charles Proxy to intercept API calls while viewing Metro live map
- Look for endpoints returning vehicle positions in JSON or Protobuf

**Expected patterns**:
```
https://api.rta.ae/v1/metro/vehicle-positions
https://api.rta.ae/gtfs/realtime/vehicle-positions
https://api.rta.ae/transport/realtime/feed
```

If found, these could be:
- GTFS-RT Protobuf (standard)
- Custom JSON API (would need manual mapping to GTFS-RT schema)

### 3. Check Abu Dhabi Darb App

**Darb** is Abu Dhabi's multi-modal transport app (bus, taxis, cycling, parking). It shows real-time bus locations.

Same reverse-engineering approach:
```
https://api.darb.itc.gov.ae/realtime/buses
https://api.dot.abudhabi.ae/gtfs-rt
```

### 4. Check Google Maps Transit / Moovit

**Google Maps** shows Dubai Metro and Abu Dhabi bus schedules. If Google has real-time data, they must be receiving a GTFS-RT feed from RTA/DoT.

**Investigation**:
- Open Google Maps in Dubai (use VPN if needed)
- Check Metro/Bus live tracking
- If real-time data is present, Google Maps has a feed from RTA

**This does NOT mean the feed is public**, but it confirms it exists. RTA may gate GTFS-RT behind partnership agreements.

### 5. Check RTA Website for Developer Portal

Search for:
```
site:rta.ae developer
site:rta.ae api
site:rta.ae gtfs
site:rta.ae open data
site:dot.abudhabi.ae gtfs
site:darb.itc.gov.ae api
```

Many transit agencies publish GTFS-RT endpoints on developer portals (e.g., Transport for London, MBTA Boston, LA Metro).

### 6. Contact RTA / DoT Directly

Email RTA or DoT to request:
- GTFS static feeds (schedule data)
- GTFS-RT feeds (real-time vehicle positions, trip updates, service alerts)
- API keys or developer access

Contact points:
- RTA: ask@rta.ae (customer service may forward to IT)
- Abu Dhabi DoT: via website contact form

## If GTFS-RT Feeds Are Found

If RTA or Abu Dhabi DoT publish GTFS-RT feeds (and they are accessible), this would be a **Build** candidate with a score of **15–16/18**:

| Criterion | Expected Score | Notes |
|-----------|----------------|-------|
| Freshness | 3 | Real-time (vehicle positions every 10–30 seconds) |
| Openness | 2–3 | TBD (may require API key or be fully open) |
| Stability | 3 | RTA and DoT are government agencies; systems are operational |
| Structure | 3 | GTFS-RT Protobuf (formal spec) |
| Identifiers | 3 | Vehicle IDs, trip IDs, route IDs (stable) |
| Additive value | 1 | GTFS domain exists in repo; UAE adds new region (but low uniqueness) |

**Key model**: Vehicle-keyed (`vehicle_id`) or trip-keyed (`trip_id`)

**Event families**:
- Reference: GTFS static (routes, stops, trips, schedules)
- Telemetry: vehicle positions (lat/lon, bearing, speed, timestamp), trip updates (delays, ETAs), service alerts

**CloudEvents subject**: `ae/dubai/transit/rta/vehicles/{vehicle_id}` or `ae/abudhabi/transit/dot/trips/{trip_id}`

**Repo sibling**: The repo already has a `gtfs` bridge. UAE GTFS-RT would be a **configuration addition** to that bridge, not a new bridge. However, if RTA/DoT use non-standard formats, a UAE-specific bridge may be needed.

## If No GTFS-RT Is Found

If RTA and DoT do not publish GTFS-RT (or it is restricted to partners):

- **Status**: Skip (no public API)
- **Gap type**: Public transit agencies do not publish real-time data openly
- **Alternative**:
  - Google Maps Transit (has data but not accessible to third parties)
  - Moovit API (commercial, may have UAE coverage)
  - Manual app scraping (violates terms of service)
- **Recommendation**: 
  - Contact RTA and DoT to request GTFS-RT publication
  - Advocate for open transit data (citing global best practices: London, New York, Paris, Sydney all publish GTFS-RT)

**Verdict**: **Maybe** (high priority, pending app reverse-engineering). Dubai Metro + Tram + Bus is a **strategic target** because:
- High-volume, high-frequency transit (Dubai Metro is world-class)
- GTFS-RT is a standard protocol (easy integration)
- Real-time vehicle tracking proves the data exists
- Smart city narrative (RTA promotes itself as a digital leader)

**Recommended next steps**:
1. Reverse-engineer S'hail and Darb apps (2–3 hours)
2. If endpoints are found, test for GTFS-RT compliance
3. If custom JSON, assess whether mapping to GTFS-RT is feasible
4. If no endpoints or endpoints are heavily gated, contact RTA/DoT directly

**Priority**: **High** (after GBFS, this is the most likely high-quality transit data source in UAE).
