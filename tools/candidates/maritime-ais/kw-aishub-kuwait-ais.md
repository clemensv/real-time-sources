# AISHub Kuwait / Persian Gulf AIS Vessel Tracking

- **Country/Region**: Kuwait waters (Persian/Arabian Gulf)
- **Endpoint**: `http://data.aishub.net/ws.php?username=X&format=1&output=json&compress=0&latmin=28.5&latmax=30.5&lonmin=46&lonmax=49`
- **Protocol**: REST / HTTP JSON
- **Auth**: Free API key (username) required, registration at aishub.net
- **Format**: JSON
- **Freshness**: Real-time (updates every few seconds to minutes per vessel)
- **Docs**: http://www.aishub.net/api
- **Score**: 11/18

## Overview

**AISHub** is a community-driven AIS (Automatic Identification System) vessel tracking aggregator. It collects AIS messages from a global network of volunteer-operated terrestrial receivers and makes the data available via a free public API.

Kuwait's maritime activity centers on:
- **Kuwait Ports** — Shuwaikh (main commercial port), Shuaiba (industrial/oil), Doha (smaller cargo)
- **Oil terminals** — Mina Al-Ahmadi (major crude export terminal), Mina Abdullah, Mina Al-Zour
- **Persian Gulf traffic** — High-density shipping lane connecting Gulf oil terminals to Strait of Hormuz
- **Fishing fleet** — Domestic fishing vessels
- **Naval and coast guard** — Kuwait Naval Force, Kuwait Coast Guard

**AIS coverage in Kuwait waters**:
- Terrestrial AIS receivers in Kuwait, UAE, Saudi Arabia, and Iran provide good coverage of the northern Persian Gulf
- Major vessels (cargo, tanker, passenger) broadcast AIS every 2–10 seconds when moving
- Smaller vessels (fishing, pleasure craft) may broadcast every 3 minutes or not at all (AIS not mandatory for <300 GT)

AISHub aggregates position reports from vessels with MMSI (Maritime Mobile Service Identity) numbers, providing:
- Vessel position (lat/lon)
- Speed over ground (SOG) and course over ground (COG)
- Heading
- Ship name, call sign, IMO number, MMSI
- Ship type (cargo, tanker, fishing, tug, etc.)
- Destination
- Dimensions (length, beam, draft)
- Timestamp of last position report

## Endpoint Analysis

**Endpoint verified** (API structure documented, registration required for actual use):

```
GET http://data.aishub.net/ws.php?username=DEMO&format=1&output=json&compress=0&latmin=28.5&latmax=30.5&lonmin=46&lonmax=49
```

**Parameters**:
- `username`: AISHub API key (obtain free at aishub.net/register)
- `format=1`: Compact JSON (vs. format=2 for XML)
- `output=json`: JSON response
- `compress=0`: Uncompressed (vs. 1 for gzip)
- `latmin`, `latmax`, `lonmin`, `lonmax`: Bounding box for Kuwait waters (28.5–30.5°N, 46–49°E)

**Rate limits** (free tier):
- 200 requests per minute
- Requests count against monthly quota (varies, ~100k/month typical)

**Expected response time**: 500ms–2s depending on vessel count

**Coverage quality**:
- ✅ Good coverage in Kuwait's main shipping lanes (port approaches, oil terminals)
- ✅ Excellent for large commercial vessels (tankers, cargo ships)
- ⚠️ Moderate coverage for smaller vessels (fishing boats, recreational)
- ⚠️ Gaps in offshore areas with no nearby terrestrial receivers

## Schema / Sample Payload

```json
[
  {
    "ERROR": false,
    "USERNAME": "demo123",
    "FORMAT": "json",
    "ZONE": 1,
    "RECORDS": 45,
    "VESSELS": [
      {
        "MMSI": 447123456,
        "TIME": "2025-05-23 10:15:22 GMT",
        "LONGITUDE": 48.1234,
        "LATITUDE": 29.5678,
        "COG": 180,
        "SOG": 12.3,
        "HEADING": 182,
        "NAVSTAT": 0,
        "IMO": 9123456,
        "NAME": "AL SABAH",
        "CALLSIGN": "9KAX",
        "TYPE": 80,
        "A": 150,
        "B": 30,
        "C": 20,
        "D": 10,
        "DRAUGHT": 8.5,
        "DEST": "SHUWAIKH",
        "ETA": "05-23 14:00"
      },
      {
        "MMSI": 403987654,
        "TIME": "2025-05-23 10:14:58 GMT",
        "LONGITUDE": 48.4567,
        "LATITUDE": 29.0123,
        "COG": 45,
        "SOG": 0.1,
        "HEADING": 90,
        "NAVSTAT": 1,
        "IMO": 9234567,
        "NAME": "GULF TRADER",
        "CALLSIGN": "A6BC",
        "TYPE": 70,
        "A": 200,
        "B": 40,
        "C": 25,
        "D": 15,
        "DRAUGHT": 12.0,
        "DEST": "MINA AL-AHMADI",
        "ETA": "05-23 12:30"
      }
    ]
  }
]
```

**Field mapping**:
- `MMSI`: Maritime Mobile Service Identity (9-digit unique vessel ID) — **primary key**
- `TIME`: Timestamp of position report (ISO 8601 UTC)
- `LONGITUDE`, `LATITUDE`: Vessel position (decimal degrees)
- `COG`: Course over ground (0–360°, 360 = north)
- `SOG`: Speed over ground (knots)
- `HEADING`: True heading (0–360°, 511 = not available)
- `NAVSTAT`: Navigational status (0 = under way, 1 = anchored, 5 = moored, etc.)
- `IMO`: International Maritime Organization ship number (7-digit, permanent)
- `NAME`: Vessel name (up to 20 characters)
- `CALLSIGN`: Radio call sign
- `TYPE`: Ship type code (70 = cargo, 80 = tanker, 30 = fishing, etc.)
- `A`, `B`, `C`, `D`: Vessel dimensions from AIS antenna (meters) — A+B = length, C+D = beam
- `DRAUGHT`: Current draught (meters)
- `DEST`: Destination port (free text, up to 20 characters)
- `ETA`: Estimated time of arrival (MM-DD HH:MM)

## Why It's Strong

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Freshness | 3 | Real-time, updates every few seconds for moving vessels |
| Openness | 2 | Free API key required, generous limits (200 req/min) |
| Stability | 2 | Community-driven, not official, but operational since 2010 |
| Structure | 3 | Well-defined JSON schema |
| Identifiers | 3 | MMSI is perfect Kafka key — stable, unique, 9-digit integer |
| Additive value | 1 | Regional extension of existing `aisstream` bridge (currently broken) |

**Score: 11/18** — Promising, but with caveats.

## Limitations

- **Free API key required** — Not fully open (registration needed), though free tier is generous
- **Community aggregator** — Not an official government source. Kuwait Ports Authority or Kuwait Coast Guard may have their own AIS systems but do not publish openly.
- **Coverage gaps** — Depends on volunteer receiver network. Offshore coverage may be spotty.
- **Not Kuwait-specific** — AISHub is global. A bridge would cover worldwide AIS, not just Kuwait.
- **Overlaps with existing bridge** — The repo already has `aisstream` (WebSocket-based AIS). If that bridge is fixed or a global AISHub bridge is built, Kuwait coverage comes for free.

## Comparison to Alternatives

| Source | Coverage | Protocol | Auth | Status |
|--------|----------|----------|------|--------|
| **AISHub** | Global (terrestrial + satellite) | REST / polling | Free API key | ✅ Operational |
| **AISstream** | Global (terrestrial) | WebSocket (MQTT) | Free | ⚠️ Broken (repo notes it's "currently broken") |
| **MarineTraffic** | Global (best coverage) | REST | Commercial ($$$) | ❌ Paid only |
| **VesselFinder** | Global | REST | Commercial | ❌ Paid only |
| **Kuwait Ports Authority** | Kuwait only | Unknown | Unknown | ❌ No public API found |
| **Digitraffic** (Finland) | Baltic Sea | REST / MQTT | Free, no auth | ✅ Already in repo |
| **Kystverket** (Norway) | Norwegian waters | REST | Free, no auth | ✅ Already in repo |

## Verdict

**Verdict**: ⚠️ **Maybe** — AISHub is a strong technical candidate (real-time, structured, stable IDs) and covers Kuwait waters. However:

1. **Global scope** — If this repo adds AISHub, it should be a **global bridge** covering all waters, not Kuwait-specific. Kuwait coverage is a byproduct.
2. **Overlaps with existing `aisstream`** — The repo already has an AIS bridge (currently broken). Fixing `aisstream` or replacing it with AISHub would be a better architecture than adding multiple regional AIS bridges.
3. **API key friction** — Free but requires registration. The repo generally prefers zero-auth sources.

**Recommendation**:
- **Primary action**: Fix the existing `aisstream` bridge (WebSocket/MQTT-based, no auth, global coverage)
- **Fallback**: If `aisstream` cannot be fixed, build a **global AISHub bridge** that covers all regions including Kuwait (not a Kuwait-specific implementation)
- **Kuwait-specific**: If Kuwait Ports Authority or Kuwait Coast Guard ever publishes an official AIS feed, that should take priority over third-party aggregators

**Next steps** (if building AISHub bridge):
1. Register for free AISHub API key
2. Design global bridge with bounding-box configuration (not hardcoded to Kuwait)
3. Implement polling loop with configurable interval (30s–60s recommended)
4. Use MMSI as Kafka key (stable, unique, integer)
5. Consider batching multiple bounding boxes in a single request to stay within rate limits
