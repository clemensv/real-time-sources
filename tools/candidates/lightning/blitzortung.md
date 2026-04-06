# Blitzortung.org (Community Lightning Detection Network)

**Country/Region**: Global (best coverage in Europe, Americas, Asia-Pacific)
**Publisher**: Blitzortung.org (community/volunteer project, founded by Prof. Egon Wanke)
**API Endpoint**: WebSocket `wss://ws1.blitzortung.org/` (multiple server instances)
**Documentation**: https://www.blitzortung.org/en/cover_your_area.php (station setup), community forums
**Protocol**: WebSocket (real-time streaming)
**Auth**: None for map viewing; station operators get data access
**Data Format**: JSON (via WebSocket)
**Update Frequency**: Real-time (sub-second, as strikes are detected)
**License**: Community project — free for non-commercial use, restricted redistribution

## What It Provides

Blitzortung.org is a community-based, crowd-sourced lightning location network. Volunteers operate detection stations worldwide that receive VLF radio signals from lightning discharges. The network uses time-of-arrival (TOA) algorithms to geolocate lightning strikes in real-time.

- **Real-time lightning strike locations** — Latitude, longitude, timestamp
- **Strike characteristics** — Signal strength, polarity (cloud-to-ground vs intra-cloud where detectable)
- **Global coverage** — ~2,000+ active stations worldwide
- **Historical data** — Archive available to station operators

## API Details

The real-time data is delivered via WebSocket connections:

**WebSocket endpoint (live strikes):**
```
wss://ws1.blitzortung.org/
```
(Also `ws3`, `ws7`, `ws8`, etc. — multiple server instances)

After connection, the server streams JSON messages for each detected lightning strike:
```json
{
  "time": 1680000000000000000,
  "lat": 48.123,
  "lon": 11.456,
  "alt": 0,
  "pol": 0,
  "mds": 12345,
  "mcg": 0,
  "sig": [
    {"sta": 1234, "time": 12, "diff": 0.5}
  ]
}
```

Fields:
- `time` — Nanosecond Unix timestamp
- `lat`, `lon` — Strike location
- `alt` — Altitude (usually 0)
- `pol` — Polarity
- `mds` — Max deviation span
- `mcg` — Max circle gap
- `sig` — Array of station signals that detected the strike

**Historical data API (for station operators):**
```
https://data.blitzortung.org/
```

**lightningmaps.org** provides the consumer-facing real-time map visualization using this data.

## Freshness Assessment

Excellent — this is as real-time as it gets. Lightning strikes appear on the WebSocket feed within seconds of occurrence. The WebSocket protocol provides true push-based streaming, not polling. Coverage quality depends on station density in a given region.

## Entity Model

Each lightning event:
- Nanosecond-precision timestamp
- Geographic coordinates (lat/lon)
- Polarity indicator
- Signal quality metrics (deviation, circle gap)
- Contributing station signals with timing data
- No persistent event ID (timestamp + location serves as natural key)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | True real-time WebSocket streaming |
| Openness | 2 | WebSocket accessible, but ToS restrict redistribution |
| Stability | 2 | Community project, no SLA, but long-running (since 2003) |
| Structure | 3 | Clean JSON messages, consistent schema |
| Identifiers | 1 | No event IDs; timestamp+location is the key |
| Additive Value | 3 | Unique real-time lightning data, global coverage |
| **Total** | **14/18** | |

## Notes

- This is a community/volunteer project — there is no formal SLA or guarantee of availability.
- The WebSocket endpoints are not officially documented as a public API. They are the transport used by lightningmaps.org.
- Terms of use restrict commercial redistribution of the data.
- Station operators who contribute hardware get enhanced data access and historical archives.
- Coverage is excellent in Europe, good in the Americas, and growing in Asia-Pacific and Africa.
- The nanosecond timestamp precision is remarkable for a community network.
- Alternative commercial services (Vaisala, WWLLN) exist but are paid and not openly accessible.
- Consider pairing with meteorological service data for validated lightning observations.
