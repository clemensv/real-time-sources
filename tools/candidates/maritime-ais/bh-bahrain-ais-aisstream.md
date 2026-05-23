# Bahrain Waters AIS Vessel Tracking - AISstream Coverage

- **Country/Region**: Bahrain territorial waters and approaches (Arabian Gulf)
- **Endpoint**: `wss://stream.aisstream.io/v0/stream` (AISstream WebSocket)
- **Protocol**: WebSocket (MQTT also available)
- **Auth**: Free API key required
- **Format**: JSON (NMEA sentences decoded to AIS message types)
- **Freshness**: Real-time (sub-second AIS message delivery)
- **Docs**: https://aisstream.io/documentation
- **Score**: 11/18 (if AISstream is operational; currently broken per repo notes)

## Overview

Bahrain is a major maritime hub in the Arabian Gulf with significant commercial port
activity. The Kingdom's primary port, Khalifa Bin Salman Port (KBSP), handles container
shipping, bulk cargo, and transshipment for the wider Gulf region. Bahrain also has:
- Mina Salman Port (general cargo, naval facilities)
- Sitra Oil Terminal (petroleum products)
- Ship repair and dry dock facilities
- Offshore oil/gas platform support

Bahrain's territorial waters are on major shipping lanes connecting the Gulf to the
Indian Ocean via the Strait of Hormuz. Vessel traffic includes:
- Container ships calling at KBSP
- Tankers loading/unloading at Sitra and offshore terminals
- Supply vessels servicing offshore oil/gas platforms
- Naval vessels (Bahrain hosts US Naval Forces Central Command / Fifth Fleet)
- Fishing vessels and small craft

AIS (Automatic Identification System) transponders on vessels broadcast position,
speed, course, heading, destination, and ship metadata. These VHF broadcasts are
received by coastal stations and satellites, then aggregated by platforms like
AISstream, which provides a global real-time WebSocket feed.

**Important caveat:** The repo's existing `aisstream` bridge is currently marked as
**broken** (per `maritime-ais` domain notes in SKILL.md). The AISstream platform may
have changed its API, introduced authentication issues, or become unreliable. This
assessment assumes AISstream will be fixed or an alternative global AIS source will
be used.

## Endpoint Analysis

**AISstream global coverage:**
AISstream receives AIS messages from ~3,500 terrestrial stations and satellite coverage
worldwide. The Arabian Gulf is well-covered due to high maritime traffic density and
coastal AIS station deployment in Saudi Arabia, UAE, Qatar, Kuwait, Bahrain, Iran, and
Oman.

**WebSocket endpoint (documented):**
```
wss://stream.aisstream.io/v0/stream
```

**Authentication:**
- Free API key required (register at aisstream.io)
- API key sent in WebSocket handshake or initial subscribe message

**Filtering:**
AISstream allows geographic bounding box filters to subscribe only to vessels within
a specific region. For Bahrain:
```json
{
  "type": "SubscriptionRequest",
  "messageTypes": [
    "PositionReport",
    "ShipStaticData"
  ],
  "boundingBoxes": [
    {
      "topLeft": { "latitude": 26.5, "longitude": 50.0 },
      "bottomRight": { "latitude": 25.5, "longitude": 51.0 }
    }
  ]
}
```

This bounding box covers Bahrain island, its territorial waters, and nearby shipping
lanes. Adjust coordinates to include approaches to Khalifa Bin Salman Port and Sitra
terminal.

**Message types:**
- **PositionReport**: Vessel position, speed, course, heading (every few seconds to
  minutes, depending on vessel speed and AIS class)
- **ShipStaticData**: Vessel name, call sign, MMSI, IMO number, ship type, dimensions,
  destination, ETA (broadcast every 6 minutes or on change)

**Stable identifier:**
- **MMSI** (Maritime Mobile Service Identity): 9-digit unique identifier assigned to
  each vessel's AIS transponder. Globally stable and used as Kafka key in the repo's
  existing AIS bridges.

## Integration Notes

**Overlap with existing coverage:**
The repo already has AIS bridges for:
- Norway (Kystverket — Norwegian Coastal Administration AIS)
- Finland/Baltic (Digitraffic — Finnish Transport Infrastructure Agency AIS)
- Global terrestrial (AISstream — currently broken)

Adding Bahrain-specific AIS via AISstream would:
- **Extend geographic coverage** to the Arabian Gulf (new region for AIS)
- **Leverage existing bridge pattern** (WebSocket, NMEA decoding, MMSI keying)
- **Reuse the global AISstream bridge** (if fixed) by simply documenting Bahrain as
  a covered region, rather than creating a separate Bahrain-only bridge
- **Fill a gap** in Gulf maritime tracking (no repo bridges for Saudi Arabia, UAE,
  Qatar, Kuwait AIS)

**Alternative: National AIS source (not found):**
Bahrain's Ports & Maritime Affairs directorate likely operates coastal AIS receivers,
but **no public API or data feed** was found during discovery. Search attempts:
- https://www.bpa.bh (Bahrain Port Authority — site failed to load)
- https://www.mtt.gov.bh (Ministry of Transportation — mentions AIS for small ships
  but no data portal)
- No documented REST API, WebSocket, or data download service

If Bahrain publishes AIS data directly in the future, it would be preferred over the
global AISstream aggregator (lower latency, authoritative source, likely better
coverage of small vessels and fishing boats that may not be picked up by AISstream's
satellite/terrestrial network).

**Recommendation:**
1. **Fix the existing global AISstream bridge** (or migrate to an alternative global
   AIS source if AISstream is permanently broken).
2. **Document Bahrain coverage** in the bridge README, noting that the Arabian Gulf
   is well-covered by AISstream's station network.
3. **Optionally add a geographic filter** to the bridge configuration to highlight
   Bahrain waters, Khalifa Bin Salman Port, and Sitra terminal as specific areas of
   interest.
4. **Monitor for national AIS feed**: If Bahrain Ports & Maritime Affairs publishes
   a direct AIS feed in the future, add it as a separate bridge with better local
   coverage.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time (sub-second to minute-level AIS messages) |
| Openness | 2 | Free API key required, generous limits |
| Stability | 1 | AISstream is operational but repo bridge currently broken; risk of API changes |
| Structure | 3 | JSON (decoded AIS messages), well-structured |
| Identifiers | 3 | MMSI is globally stable and perfect for Kafka keying |
| Additive value | 1 | Extends existing AISstream bridge to Gulf region; not a new domain, but new geography |

**Verdict**: **Promising**, but depends on fixing the existing global AISstream bridge.
If the global bridge is restored, Bahrain AIS coverage is automatic (Arabian Gulf is
well within AISstream's terrestrial and satellite network). Adding Bahrain-specific
documentation or a bounding box filter would make this explicit.

If AISstream remains broken, investigate alternative global AIS sources:
- **Barentswatch** (Norway — global satellite AIS, may have API)
- **Global Fishing Watch** (fishing vessel tracking, public API)
- **MarineTraffic / VesselFinder** (commercial APIs — likely paid)
- **National sources**: Saudi Arabia, UAE, Qatar AIS authorities (if public APIs exist)

Do **not** create a separate Bahrain-only AIS bridge until the global AISstream
situation is resolved or a Bahrain-specific national feed is discovered.
