# Dubai Ferry and Abu Dhabi Marine Transit (Real-Time Vessel Tracking)

- **Country/Region**: United Arab Emirates / Dubai + Abu Dhabi
- **Endpoint**: **UNKNOWN** — requires discovery
- **Protocol**: Unknown (likely GTFS-RT, REST API, or AIS)
- **Auth**: Unknown
- **Format**: Likely JSON or Protobuf (GTFS-RT)
- **Freshness**: Expected real-time (vessel positions updated every 30–60 seconds)
- **Docs**: 
  - Dubai Ferry: https://www.rta.ae/wps/portal/rta/ae/public-transport/marine
  - Abu Dhabi DoT: https://dot.abudhabi.ae/
- **Score**: **TBD** (cannot score without endpoint)

## Overview

The UAE operates multiple marine public transit services:

### Dubai Ferry (operated by RTA)
- **Routes**: 2 active routes
  - **Route 1**: Dubai Marina → JBR → Dubai Harbor → Bluewaters → Dubai Marina (circular)
  - **Route 2**: Dubai Marina → Al Ghubaiba (Old Dubai / Creek area)
- **Fleet**: 4 vessels (2 ferries + 2 water taxis)
- **Frequency**: Every 30–60 minutes (varies by route and time of day)
- **Stations**: 7 ferry stations across Dubai

### Abu Dhabi Marine Transit
- **Operated by**: Abu Dhabi Department of Transport (DoT)
- **Services**:
  - **Abu Dhabi Ferry**: Corniche → Yas Island → Saadiyat Island
  - **Water Taxi**: On-demand service across Abu Dhabi waterways
  - **Sightseeing cruises**: Dhow cruises, coastal tours
- **Fleet**: ~10 vessels (mix of ferries and water taxis)

### Other Emirates
- **Sharjah**: Sharjah Water Transport Authority operates limited ferry services (Sharjah Creek, Al Khan Lagoon)
- **Ras Al Khaimah**: Water taxi services (seasonal)

## Why Marine Transit Is a Candidate

1. **Real-time vessel tracking**: Ferry systems worldwide publish vessel positions via GTFS-RT or custom APIs
2. **GTFS-RT compatibility**: The General Transit Feed Specification (GTFS) has a real-time extension for ferries (same as buses/trains)
3. **AIS backup**: Larger ferries may broadcast AIS positions (already covered by global AIS sources, but ferry-specific metadata would add value)
4. **Smart city integration**: Dubai and Abu Dhabi market themselves as smart cities; real-time transit data fits this narrative

## Endpoint Discovery Required

### 1. Check for GTFS-RT Feeds

**Dubai Ferry (RTA)**:
- RTA may publish GTFS-RT for all public transport modes (Metro, Tram, Bus, Ferry)
- Search for:
  ```
  site:rta.ae gtfs
  site:rta.ae realtime
  site:rta.ae api ferry
  ```

- Check MobilityData catalog (done earlier for UAE; no RTA GTFS-RT found)

**Abu Dhabi Ferry (DoT)**:
- Similar search:
  ```
  site:dot.abudhabi.ae gtfs
  site:dot.abudhabi.ae ferry realtime
  site:dot.abudhabi.ae api
  ```

### 2. Check Mobile Apps

Both RTA and Abu Dhabi DoT have mobile apps:
- **RTA Dubai** app (iOS/Android): May show live ferry positions
- **Darb** app (Abu Dhabi): Integrated transport app for Abu Dhabi public transit
- **S'hail** app (RTA): Multi-modal journey planner for Dubai

**Reverse-engineering strategy**: Install apps, use Charles Proxy or mitmproxy to intercept API calls while viewing ferry locations. This could reveal internal REST API endpoints.

### 3. Check ArcGIS / Esri Platforms

Many UAE agencies use Esri ArcGIS for mapping and real-time data. Check for:
```
https://maps.rta.ae/
https://maps.dot.abudhabi.ae/
https://services.arcgis.com/ (search for "rta" or "dubai ferry")
```

If found, ArcGIS REST APIs (FeatureServer or MapServer) can be polled for real-time vessel positions.

### 4. Third-Party Aggregators

Check if Google Maps Transit, Apple Maps, or Moovit have integrated RTA or Abu Dhabi ferries. If they have, the data source might be discoverable via:
- Google Transit Partner Program dashboard (requires RTA partnership)
- Moovit API (if RTA publishes to Moovit)

## If Endpoint Is Found

If RTA or Abu Dhabi DoT publish real-time ferry positions, this would be a **Build** candidate with a score of **13–15/18**:

| Criterion | Expected Score | Notes |
|-----------|----------------|-------|
| Freshness | 3 | Real-time vessel positions (30–60 second updates) |
| Openness | 2–3 | TBD (may require API key or be fully open) |
| Stability | 3 | Public transport authorities; operational systems |
| Structure | 3 | GTFS-RT (Protobuf) or JSON REST API |
| Identifiers | 3 | Vessel IDs, trip IDs, route IDs (stable) |
| Additive value | 1–2 | Ferry domain exists in repo taxonomy; UAE would add a new region |

**Key model**: Vessel-keyed (vessel ID or trip ID)

**Event families**:
- Reference: routes, stops, vessels (GTFS static data)
- Telemetry: vehicle positions (lat/lon, bearing, speed, timestamp), trip updates (delays, cancellations)

**CloudEvents subject**: `ae/dubai/ferry/vessels/{vessel_id}` or `ae/abudhabi/ferry/trips/{trip_id}`

**Repo sibling**: The repo has a `ferry` domain in the taxonomy but no existing ferry source. This would be the **first ferry bridge** in the repo.

## If No Endpoint Is Found

If neither RTA nor Abu Dhabi DoT publish ferry data:

- **Status**: Skip (no public API)
- **Gap type**: Public transport agencies do not publish ferry real-time data
- **Alternative**: 
  - AIS (ferries broadcast AIS, but lack ferry-specific metadata like route, schedule, stops)
  - Manual tracking via mobile apps (not automatable)
- **Recommendation**: Contact RTA and Abu Dhabi DoT to request GTFS-RT endpoints or developer access

**Fleet size consideration**: Dubai Ferry has only 4 vessels, Abu Dhabi Ferry ~10 vessels. The low volume makes this a **low-priority** target compared to higher-volume sources (GBFS bikeshare, road traffic, weather). However, it would be a **unique addition** if found easily.

**Verdict**: **Maybe** (low priority, pending endpoint discovery). Check RTA and Abu Dhabi DoT websites and mobile apps. If found with minimal effort, it's a **Build**. If discovery requires >2 hours of reverse-engineering, **Skip** and focus on higher-value UAE targets.
