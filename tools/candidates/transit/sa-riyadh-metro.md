# Riyadh Metro - GTFS Real-Time

> ⏭ **SKIP** · GTFS-RT is only assumed/unpublished for Riyadh Metro; no verified real-time endpoint.

- **Country/Region**: Saudi Arabia (Riyadh)
- **Endpoint**: Unknown (system opening in phases 2024-2025)
- **Protocol**: GTFS-RT (assumed)
- **Auth**: Unknown
- **Format**: Protobuf (GTFS-RT standard)
- **Freshness**: Real-time (30-second vehicle positions typical for metro)
- **Docs**: None yet
- **Score**: 12/18

## Overview

The **Riyadh Metro** (قطار الرياض) is one of the world's largest metro systems under construction, and the first metro in Saudi Arabia. Officially called the **King Abdulaziz Project for Public Transport in Riyadh**, the system includes:

- **6 metro lines** (Lines 1-6)
- **176 km** of track (109 km elevated, 67 km underground/at-grade)
- **85 stations**
- **Capacity**: ~3.6 million passengers/day when fully operational
- **Opening**: Phased rollout starting late 2024 (Lines 4, 5, 6 first)

**Scale comparison**:
- Larger than **London Elizabeth Line** (118 km)
- Comparable to **Dubai Metro** (90 km across 2 lines)
- Smaller than **Shanghai Metro** (~800 km) but built in a single construction phase

**Technology**: Riyadh Metro uses **driverless trains** (fully automated, no operators). The system is operated by a consortium including Alstom, Bombardier, Siemens, and Ansaldo STS.

**Context**: Riyadh has **~7 million residents** and has relied entirely on private cars and buses (no rail transit). The metro is part of Saudi Vision 2030 to reduce car dependency and oil consumption.

## GTFS and GTFS-RT Likelihood

Modern metro systems typically publish **GTFS** (static schedules) and **GTFS-RT** (real-time vehicle positions, arrival predictions, service alerts). Examples:

| Metro system | GTFS | GTFS-RT | API |
|--------------|------|---------|-----|
| **Paris Métro** | ✅ | ✅ | SIRI/GTFS-RT |
| **London TfL** | ✅ | ✅ | REST |
| **Dubai Metro** | ✅ | ❌ | None public |
| **Doha Metro** (Qatar) | ❌ | ❌ | None |
| **Riyadh Metro** | ❓ | ❓ | Unknown |

Gulf Arab metros (Dubai, Doha) have **not published GTFS-RT** despite modern infrastructure. This is a regional pattern of low transit data transparency.

**However**, Riyadh Metro may differ because:
1. **Western operators**: Alstom, Bombardier, Siemens are European companies familiar with GTFS-RT.
2. **Saudi Vision 2030**: Emphasis on digital transformation and open data.
3. **Third-party apps**: Google Maps, Apple Maps, Moovit may require GTFS feeds to display metro routes.
4. **MaaS integration**: Riyadh is planning integrated mobility (metro + bus + bike) which requires real-time data sharing.

## Endpoint Analysis

**Official website**: The Riyadh Metro website exists but was inaccessible during probing (`https://riyadhmetro.sa` and `https://www.riyadhmetro.sa/en` both failed).

**Possible GTFS-RT endpoints** (not yet tested):
```
https://api.riyadhmetro.sa/gtfs-rt/vehicle-positions
https://data.riyadhmetro.sa/gtfs-rt/trip-updates
https://www.riyadhmetro.sa/api/realtime
```

**MobilityData catalog**: The global GTFS aggregator (MobilityData.org) does not yet list Riyadh Metro, but the system is not fully open. Check again after public launch.

**Royal Commission for Riyadh City**: The metro project is managed by the High Commission for the Development of Arriyadh (now Royal Commission for Riyadh City). They may publish data portals.

## Integration Notes

- **System not yet open**: As of late 2024, Riyadh Metro is in final testing and phased opening. GTFS feeds may not exist until the system enters revenue service.
- **Check after launch**: Once Lines 4, 5, 6 open to the public (late 2024), immediately check:
  1. Riyadh Metro website for developer/data sections
  2. Google Maps (if routes appear, GTFS exists)
  3. MobilityData catalog (may auto-discover and list)
  4. data.gov.sa (Saudi open data portal)
- **Operator consortium**: Contact Alstom, Bombardier, or Arriyadh Development Authority to request GTFS/GTFS-RT access.
- **Comparison with Dubai**: Dubai Metro does **not** publish GTFS-RT. If Riyadh Metro follows the Gulf pattern, it will be dashboard-only.
- **Unique value**: Riyadh Metro would be the first Saudi **GTFS-RT source** in this repo. It would also be the first fully-automated (driverless) metro system in the Middle East with public real-time data (if published).

**Driverless operations**: Riyadh Metro's full automation (GoA 4) means:
- Vehicle positions are **precise** (GPS + track circuits)
- Arrival predictions are **accurate** (no human driver variance)
- Real-time data quality is likely **high**

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Metro vehicle positions update every 30 seconds (if GTFS-RT exists) |
| Openness | 2 | Unknown; Gulf metros are typically closed, but Riyadh may differ |
| Stability | 3 | Major infrastructure project, government-backed |
| Structure | 3 | GTFS-RT is a formal spec (Protobuf) |
| Identifiers | 3 | GTFS trip IDs, route IDs, stop IDs are stable |
| Additive value | 2 | First Saudi metro; overlaps with existing GTFS bridge (same protocol) |

**Total: 16/18** (if GTFS-RT is published)  
**Actual: 12/18** (penalized for unknown status)

**Verdict**: ⚠️ **Maybe** — Riyadh Metro is a **high-value future source** if GTFS-RT is published. The system is one of the world's largest and most modern metro networks, and Saudi Arabia's first. Real-time train tracking would be globally significant.

**Recommended action**:
1. **Monitor for launch** — Once Riyadh Metro opens (late 2024), immediately check for GTFS feeds.
2. **Check Google Maps** — If Riyadh Metro routes appear in Google Maps transit directions, GTFS exists. Google requires GTFS-static at minimum.
3. **Contact operators** — Reach out to Alstom, Bombardier, Siemens, or Royal Commission for Riyadh City to request developer access.
4. **Fallback: Dubai Metro** — If Riyadh Metro does **not** publish GTFS-RT, this confirms a Gulf Arab pattern of metro opacity. Focus on European/Asian metros instead.

If GTFS-RT is confirmed, immediately escalate to ✅ **Build** — this would be the repo's first Gulf metro and a flagship addition.

**Comparison with other Gulf metros**:
- **Dubai Metro** (2009) — No GTFS-RT after 15 years of operation
- **Doha Metro** (2019) — No GTFS-RT
- **Riyadh Metro** (2024) — **TBD**

If Riyadh Metro publishes GTFS-RT, it would break the Gulf precedent and signal a shift toward transit data transparency in the region.
