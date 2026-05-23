# USGS Earthquake Hazards Program - Iraq Coverage

- **Country/Region**: Global (includes Iraq and Zagros seismic zone)
- **Endpoint**: `https://earthquake.usgs.gov/fdsnws/event/1/query`
- **Protocol**: FDSN Web Service (HTTP/REST)
- **Auth**: None
- **Format**: GeoJSON, QuakeML, CSV, XML
- **Freshness**: Real-time (M4.5+ events appear within 5-10 minutes)
- **Docs**: https://earthquake.usgs.gov/fdsnws/event/1/
- **Score**: 17/18

## Overview

**Note**: This source is **already in the repository** (`usgs-earthquake-latest`), but it is worth documenting for Iraq coverage context.

The USGS Earthquake Hazards Program operates a global seismic monitoring network with excellent coverage of significant earthquakes worldwide, including Iraq and the Zagros seismic belt (Iran-Iraq border).

Iraq sits on the western edge of the Zagros fault zone, one of the most seismically active regions in the world. The USGS provides authoritative earthquake data for M4.5+ events that are felt across Iraq.

## Iraq-Specific Coverage

USGS covers Iraq and surrounding regions:
- Zagros fault belt (western Iran / Iraq border)
- Turkish-Iraqi-Iranian tri-border region
- Kurdish regions (Erbil, Sulaymaniyah, Duhok)

Major recent events:
- 2017 M7.3 Sarpol-e Zahab earthquake (Iran-Iraq border) — killed 600+, felt across Iraq
- Frequent M4-5 events along the Zagros that are felt in Kurdish cities

Sample request for Iraq bounding box:
```
GET https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=29&maxlatitude=38&minlongitude=38&maxlongitude=49&minmagnitude=2.5
```

## Endpoint Analysis

**Already implemented** — see `usgs-earthquake-latest` source in repo.

The USGS FDSN endpoint is the gold standard for global seismology. For Iraq specifically:
- **Real-time latency**: 5-10 minutes for M4.5+ events
- **Authoritative magnitude**: USGS is the global reference for earthquake magnitude
- **Stable identifiers**: Each event has a unique `id` (e.g., `us6000syqi`)

## Coverage vs EMSC

For Iraq earthquake monitoring, **both USGS and EMSC should be used**:

| Source | Strength | Weakness |
|--------|----------|----------|
| **USGS** | Authoritative global reference, M4.5+ very fast | Slower for smaller events (M2.5-4.5) in regional settings |
| **EMSC** | Faster regional detection for M2.5-4.5 Zagros events due to denser station network | Not authoritative for global magnitude (USGS is reference) |

**Recommendation**: Keep USGS (already in repo) as the authoritative source. Add EMSC as a complementary regional source for Iraq/Zagros to capture smaller felt earthquakes that USGS may detect later or at lower priority.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, 5-10 min for M4.5+ |
| Openness | 3 | No auth, no rate limits, FDSN standard |
| Stability | 3 | FDSN spec, versioned, authoritative |
| Structure | 3 | GeoJSON, QuakeML, formal schema |
| Identifiers | 3 | Unique event IDs, perfect keys |
| Richness | 2 | Global coverage, detailed event parameters |

**Verdict**: ✅ **Already in repo** — USGS provides authoritative global earthquake data including Iraq. For Iraq frontier discovery, note that **EMSC** (European-Mediterranean Seismological Centre) is a valuable **complementary source** for regional Zagros events (see `iq-emsc-fdsn-zagros.md`). Both should be used together for complete Iraq earthquake monitoring.
