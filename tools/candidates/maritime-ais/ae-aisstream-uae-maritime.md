# AISstream - UAE Maritime Traffic

- **Country/Region**: United Arab Emirates (Dubai, Abu Dhabi ports) / Global
- **Endpoint**: `wss://stream.aisstream.io/v0/stream`
- **Protocol**: WebSocket (NMEA AIS messages wrapped in JSON)
- **Auth**: API key (free tier: 15,000 messages/month)
- **Format**: JSON (AIS sentences decoded)
- **Freshness**: Real-time (sub-second vessel position updates)
- **Docs**: https://aisstream.io/documentation
- **Score**: 12/18

## Overview

AISstream is a global terrestrial AIS aggregator that streams vessel positions in real-time via WebSocket. The service covers all major UAE ports including:

- **Dubai**: Jebel Ali (world's 9th busiest container port), Port Rashid, Dubai Maritime City
- **Abu Dhabi**: Khalifa Port, Zayed Port, Mussafah Port
- **Sharjah**: Port Khalid, Hamriyah Port
- **Fujairah**: Port of Fujairah (world's 2nd largest bunkering hub)
- **Ras Al Khaimah**: RAK Maritime City

UAE is a major maritime logistics hub; Dubai's Jebel Ali alone handles 5,000+ vessel calls per year. Real-time AIS tracking covers cargo ships, tankers, container vessels, and offshore support vessels serving the region's oil & gas industry.

## Endpoint Analysis

**WebSocket stream** — subscribe to geographic bounding boxes or vessel MMSIs:

```
wss://stream.aisstream.io/v0/stream
```

Requires API key in query string: `?apikey=YOUR_KEY`

**Filter by UAE bounding box**:
```json
{
  "BoundingBoxes": [[
    [22.0, 51.0],  // Southwest corner (southern UAE coast)
    [26.5, 56.5]   // Northeast corner (northern UAE + Oman border)
  ]]
}
```

**Message types**:
- Position reports (Types 1, 2, 3): lat/lon, speed, course, heading, timestamp
- Static voyage data (Type 5): vessel name, MMSI, IMO, callsign, destination, ETA, ship type
- Aids to navigation (Type 21): buoys, lighthouses

**Sample position report**:
```json
{
  "MessageType": "PositionReport",
  "MetaData": {
    "MMSI": 470123456,
    "ShipName": "EXAMPLE VESSEL",
    "time_utc": "2025-01-23T08:00:00Z"
  },
  "Message": {
    "PositionReport": {
      "Latitude": 25.2854,
      "Longitude": 55.3644,
      "Cog": 135.5,
      "Sog": 12.3,
      "TrueHeading": 137
    }
  }
}
```

## Why This Is a Strong Candidate

1. **Real-time streaming** — WebSocket push, sub-second updates during vessel movement
2. **Global coverage, UAE focus** — can filter to UAE waters
3. **Stable identifiers** — MMSI (9-digit unique vessel ID) is perfect for Kafka keys
4. **Rich metadata** — position, speed, course, heading, vessel type, destination, ETA
5. **Mature protocol** — AIS is an ITU/IMO standard; data quality is high
6. **High volume** — UAE ports handle thousands of vessels; active stream during peak hours
7. **Strategic value** — maritime logistics, supply chain visibility, port congestion monitoring

## Limitations

- **API key required** — free tier is 15,000 messages/month (about 500/day), may need paid tier for continuous coverage
- **Free tier limits** — may not be sufficient for full UAE vessel traffic (Jebel Ali alone has 100+ vessels in port at any time)
- **Repo overlap** — the repo already has `aisstream` (global) and `kystverket-ais` (Norway); adding UAE-specific config would be a **geographic extension**, not a new source
- **Terrestrial coverage gaps** — AISstream relies on land-based receivers; coverage may be sparse in UAE offshore areas (Strait of Hormuz approaches)

## Integration Notes

**This is NOT a new source**. The repo already has `aisstream` as a global AIS bridge (currently broken per SKILL.md notes). The UAE use case is:

1. **Fix the existing `aisstream` bridge** (if broken)
2. **Add UAE bounding box** as a configuration example in the README
3. **Document UAE ports** as a deployment scenario

If the existing bridge is unsalvageable, this could justify a **UAE-specific AIS** bridge that:
- Focuses on UAE bounding box only
- Includes UAE port reference data (port names, berth locations from Dubai Ports World, Abu Dhabi Ports, etc.)
- Potentially combines AISstream with local UAE maritime authority feeds (if they exist)

**Key model**: MMSI-keyed (9-digit vessel identifier)

**Event families**:
- Reference: vessel static data (IMO, name, type, dimensions)
- Telemetry: position reports (lat/lon, speed, course, heading every 2-10 seconds for moving vessels)

**CloudEvents subject**: `ae/maritime/ais/vessels/{mmsi}` or `global/maritime/ais/vessels/{mmsi}`

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time WebSocket, sub-second updates |
| Openness | 2 | Free API key with limits; paid tier for full coverage |
| Stability | 3 | AISstream is established, AIS protocol is ITU standard |
| Structure | 2 | JSON wrapper around NMEA sentences (some decoding needed) |
| Identifiers | 3 | MMSI is globally unique, stable |
| Additive value | -1 | **Duplicates existing `aisstream` source** — geographic focus, not a new protocol or domain |

**Verdict**: **Skip** (as a separate UAE-specific source). Instead, **document UAE as a deployment scenario** for the existing `aisstream` bridge. If that bridge is broken and needs a rewrite, use UAE (Jebel Ali, Fujairah) as the reference implementation and include the UAE bounding box filter in the default config.

If Dubai Ports World, Abu Dhabi Ports, or UAE's Federal Transport Authority publish their **own** real-time AIS or port operations API (berth assignments, container handling, vessel ETAs), that would be a **Build** candidate as a distinct source. But AISstream alone is just a configuration of an existing global service.
