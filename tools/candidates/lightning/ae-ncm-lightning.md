# NCM Lightning Detection Network (UAE)

- **Country/Region**: United Arab Emirates (Federal)
- **Endpoint**: **UNKNOWN** — requires discovery
- **Protocol**: Unknown (likely REST API or WebSocket)
- **Auth**: Unknown
- **Format**: Likely JSON
- **Freshness**: Real-time (lightning strokes detected within 1–10 seconds)
- **Docs**: https://www.ncm.ae/
- **Score**: **TBD** (cannot score without endpoint; if found: 15–16/18)

## Overview

The National Center of Meteorology (NCM) operates a **Lightning Detection Network** covering the UAE. Lightning detection is critical for:

- **Aviation safety**: Thunderstorms and lightning ground flights at DXB and AUH
- **Outdoor safety**: Construction, oil & gas operations, public events
- **Fire risk**: Lightning strikes in dry brush areas (though UAE vegetation is sparse)
- **Cloud seeding operations**: NCM avoids seeding in thunderstorm cells
- **Early warning**: Lightning precedes severe weather (hail, microbursts, flash floods)

**Lightning in the UAE**:
- UAE experiences thunderstorms primarily during winter (November–March) when cold fronts interact with warm Gulf air
- Summer thunderstorms are rare but intense when they occur
- Lightning strikes are concentrated in the northern emirates (RAK, Fujairah) and interior mountains (Hajar range)
- Coastal areas (Dubai, Abu Dhabi) see less lightning but thunderstorms still disrupt aviation

**NCM's network**:
- NCM has mentioned lightning detection capabilities in press releases and annual reports
- Likely uses a network of sensors (VLF/LF radio receivers) to triangulate lightning strokes
- Technology: Possibly Vaisala or similar commercial lightning detection systems

## Why Lightning Data Is Valuable

1. **Real-time streaming**: Lightning strokes are point events (lat/lon, timestamp, polarity, peak current)
2. **High event rate during storms**: Thunderstorms can produce hundreds of strokes per hour
3. **Unique dataset**: Gulf region lightning patterns are scientifically interesting (rare but severe)
4. **Aviation correlation**: Link lightning data with DXB/AUH flight delays and diversions
5. **Early warning**: Lightning often precedes heavy rain and flash floods (UAE's flash flood risk is underestimated)

## Endpoint Discovery Required

### 1. NCM Website / Mobile App

If NCM publishes weather data (see earlier `ae-ncm-weather-network.md` candidate), lightning may be included. Check for:

```
site:ncm.ae lightning
site:ncm.ae thunderstorm
site:ncm.ae real-time weather
```

NCM's mobile app (if it exists) may show live lightning strikes. Reverse-engineering the app could reveal an API endpoint.

### 2. Blitzortung (Global Community Network)

**Blitzortung.org** is a global community lightning detection network (similar to ADSBexchange for lightning). Check if UAE has contributors:

```
https://map.blitzortung.org/ (zoom to UAE)
```

If UAE has Blitzortung receivers, the data is already flowing into Blitzortung's WebSocket feed:

```
wss://ws.blitzortung.org/
```

**Blitzortung coverage check**:
- View live map at map.blitzortung.org
- Zoom to UAE (Dubai, Abu Dhabi)
- Check if lightning strokes appear during UAE thunderstorm seasons (November–March)

**Blitzortung advantages**:
- Real-time WebSocket (sub-second latency)
- No auth, fully open
- Global coverage (if receivers exist in UAE or nearby)
- Structured JSON messages

**Blitzortung limitations**:
- Community network; coverage depends on volunteer receivers
- UAE may have sparse coverage (receivers need to be deployed by enthusiasts)
- Not an official NCM source

### 3. Third-Party Weather Services

**Wunderground**, **WeatherUnderground Personal Weather Stations (PWS)**: Some PWS owners deploy lightning detectors. Check for UAE stations with lightning sensors:

```
https://www.wunderground.com/pws (search UAE)
```

**Earth Networks** (commercial): Provides lightning data to weather apps. Check if UAE is covered.

**WWLLN** (World Wide Lightning Location Network): Academic network. Check if data is publicly accessible.

## If NCM Lightning Endpoint Is Found

If NCM publishes real-time lightning strike data, this would be a **Build** candidate with a score of **15–16/18**:

| Criterion | Expected Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time (lightning strokes detected within seconds) |
| Openness | 2–3 | TBD (NCM openness is unclear) |
| Stability | 3 | National met service; operational system |
| Structure | 3 | JSON or binary (structured point events) |
| Identifiers | 3 | Stroke ID (timestamp + coordinates can serve as composite key) |
| Additive value | 3 | New region (Gulf), new domain (lightning not yet in repo), scientifically valuable |

**Key model**: Stroke-keyed (composite key: `timestamp + lat/lon` or stroke UUID if NCM assigns one)

**Event families**:
- Telemetry: lightning strokes (lat, lon, timestamp, polarity, peak current kA, stroke type: CG/IC)

**CloudEvents subject**: `ae/weather/lightning/strokes/{stroke_id}` or `ae/weather/lightning/events/{timestamp}`

**Repo sibling**: The repo does not have a lightning source yet. This would establish the **lightning detection domain** in the repo, with NCM or Blitzortung as the reference implementation.

## If Only Blitzortung Is Available

If NCM does not publish lightning data, but Blitzortung covers UAE:

**Verdict**: **Build** (Blitzortung as the source)

Blitzortung would score **14–15/18** (loses 1 point for community network vs. official source, but gains from being fully open and real-time WebSocket).

**Note**: Blitzortung is global; UAE coverage would be a **geographic filter**, not a unique source. However, if no other repo source uses Blitzortung, this would establish the Blitzortung protocol pattern.

## If No Lightning Data Is Found

If neither NCM nor Blitzortung provide UAE coverage:

- **Status**: Skip (no public data)
- **Gap type**: Lightning detection network data not accessible
- **Alternative**: 
  - Satellite lightning detection (NASA LIS/GLM — sparse coverage, lower accuracy than ground networks)
  - Third-party commercial (Earth Networks — paid)
- **Recommendation**: Contact NCM to request lightning data API or advocate for Blitzortung receiver deployment in UAE

**Verdict**: **Maybe** (medium priority, pending Blitzortung coverage check and NCM search).

**Recommended next steps**:
1. **Check Blitzortung map** (5 minutes): If UAE coverage exists, this is a **Build**
2. **Search NCM website** (30 minutes): Look for lightning data endpoints
3. If neither found, **Skip** but document as a gap

**Priority**: Medium. Lightning data is scientifically interesting and operationally valuable (aviation safety), but it's a niche domain compared to higher-priority UAE targets (GBFS, weather, air quality, radiation).
