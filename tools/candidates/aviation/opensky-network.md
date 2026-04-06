# OpenSky Network
**Country/Region**: Global
**Publisher**: OpenSky Network Association (non-profit, academic)
**API Endpoint**: `https://opensky-network.org/api/states/all`
**Documentation**: https://openskynetwork.github.io/opensky-api/
**Protocol**: REST
**Auth**: None (anonymous, limited) / Account (free, higher limits)
**Data Format**: JSON
**Update Frequency**: Real-time (~5-second update intervals for state vectors)
**License**: CC BY-NC 4.0 (non-commercial), academic use encouraged

## What It Provides
The OpenSky Network is a community-driven ADS-B/Mode-S receiver network providing real-time aircraft tracking data:
- **State Vectors**: Real-time aircraft positions and velocity
  - ICAO24 transponder address
  - Callsign
  - Longitude, Latitude, Altitude (barometric and geometric)
  - Ground speed, track angle, vertical rate
  - On-ground flag
  - Squawk code
  - Position source (ADS-B, MLAT, other)
- **Flight tracking**: Departures and arrivals by airport
- **Historical data**: Track logs and state vector history (authenticated)

## API Details
- **All state vectors**: `GET /api/states/all` — all aircraft currently tracked
- **Bounding box filter**: `?lamin={lat}&lomin={lon}&lamax={lat}&lomax={lon}`
- **By ICAO24**: `?icao24={addr}` — specific aircraft
- **Time parameter**: `?time={unix_timestamp}` — state at specific time
- **Flights by aircraft**: `GET /api/flights/aircraft?icao24={addr}&begin={time}&end={time}`
- **Flights by airport**: `GET /api/flights/arrival?airport={icao}&begin={time}&end={time}`
- **Rate limits**:
  - Anonymous: 10-second update interval, limited requests
  - Registered: 5-second update interval, higher request limits
  - Research: Historical data access, bulk downloads

Response is a JSON object with `time` (unix timestamp) and `states` (array of arrays with fixed field positions).

## Freshness Assessment
Excellent. State vectors update every 5-10 seconds depending on authentication level. The network receives data from thousands of volunteer ADS-B receivers worldwide. Coverage is best over Europe and North America, with growing coverage globally.

## Entity Model
- **State Vector** (icao24, callsign, origin_country, time_position, last_contact, longitude, latitude, baro_altitude, on_ground, velocity, true_track, vertical_rate, sensors, geo_altitude, squawk, spi, position_source, category)
- **Flight** (icao24, firstSeen, estDepartureAirport, lastSeen, estArrivalAirport, callsign)
- **Airport** (ICAO code — used as filter parameter)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | 5-10 second update intervals |
| Openness | 2 | Free, but CC BY-NC license, rate limits |
| Stability | 3 | Academic non-profit, operational since 2013 |
| Structure | 3 | Clean JSON, well-documented API |
| Identifiers | 3 | ICAO24 transponder addresses, airport ICAO codes |
| Additive Value | 3 | Global aircraft tracking, academic-grade |
| **Total** | **17/18** | |

## Notes
- Non-commercial license (CC BY-NC 4.0) may limit some use cases
- Free registration significantly improves API access
- State vector response uses arrays (not objects) for bandwidth efficiency — field positions are fixed
- Coverage depends on volunteer receiver network density — some oceanic/remote areas have gaps
- Historical data access requires authenticated account
- Complements the existing mode-s/ bridge (which is for local receivers) — OpenSky aggregates globally
