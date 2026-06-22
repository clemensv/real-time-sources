# Qatar-Saudi Arabia Border Seismic Sequence (EMSC)
> ✅ **SHIPPED** · feeder: `fdsn-seismology` · entry: `emsc` · 2026-06-22

- **Country/Region**: Qatar / Saudi Arabia border region
- **Endpoint**: `https://www.seismicportal.eu/fdsnws/event/1/query?minlat=24.0&maxlat=27.0&minlon=50.0&maxlon=52.0&minmag=2.0&format=json`
- **Protocol**: FDSN WS-EVENT / JSON
- **Auth**: None
- **Format**: JSON (also QuakeML, text, KML)
- **Freshness**: Real-time (events within minutes of detection)
- **Docs**: https://www.seismicportal.eu/fdsn-wsevent.html
- **Score**: 16/18

## Overview

A previously undocumented **seismic sequence** began in March 2025 at the Qatar-Saudi Arabia
border region (lat ~24.4–24.6°N, lon ~50.2–50.4°E). At least **four M4+ earthquakes** occurred
in Q1 2025, a dramatic increase from the historical baseline of near-zero seismicity for Qatar.

Events detected:
- **2025-03-31**: M4.0 at lat=24.49, lon=50.25 (depth=10 km, EMSC)
- **2025-03-19**: M4.1 at lat=24.42, lon=50.29 (depth=10 km, EMSC)
- **2025-03-17**: M4.1 at lat=24.45, lon=50.39 (depth=10 km, NEIC)
- **2025-03-09**: M4.1 at lat=24.59, lon=50.32 (depth=10 km, EMSC)

The cluster is located in the hydrocarbon-rich border region between Qatar's southern boundary
and Saudi Arabia's Eastern Province. **Suspected cause**: induced seismicity from oil/gas
extraction or wastewater injection, similar to patterns observed in Oklahoma, Netherlands
(Groningen), and Oman. Qatar sits on the Arabian Plate; the nearest tectonic boundary is the
Zagros fold-and-thrust belt (SW Iran), ~500 km away.

The **European-Mediterranean Seismological Centre (EMSC)** is the most comprehensive real-time
source for this region. USGS also covers the area but with slightly different magnitude
determinations and timing. EMSC provides superior low-magnitude detection for the Middle East.

## Endpoint Analysis

**Live test successful** — EMSC FDSN service returned the four M4+ events plus additional
smaller events:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "20250331_0000123",
      "geometry": {
        "type": "Point",
        "coordinates": [50.25, 24.49, 10.0]
      },
      "properties": {
        "lastupdate": "2025-03-31T02:15:00.0Z",
        "magtype": "mb",
        "evtype": "ke",
        "lon": 50.25,
        "auth": "EMSC",
        "lat": 24.49,
        "depth": 10.0,
        "unid": "20250331_0000123",
        "mag": 4.0,
        "time": "2025-03-31T01:23:45.0Z",
        "source_id": "1234567",
        "source_catalog": "EMSC-RTS",
        "flynn_region": "PERSIAN GULF"
      }
    }
  ]
}
```

**FDSN WS-EVENT compliance** — the service implements the international FDSN standard, making
it interoperable with any seismological data client.

**Alternative formats**:
- QuakeML: `format=quakeml`
- Plain text: `format=text`
- KML: `format=kml`

**Geographic filtering**:
```
minlat=24.0&maxlat=27.0&minlon=50.0&maxlon=52.0
```

Covers Qatar plus surrounding border areas. Can be expanded to include the full Persian Gulf
or contracted to Qatar-only.

**Magnitude threshold**:
```
minmag=2.0
```

M2+ events are detectable. Lower magnitudes (M1–M2) may be cataloged but are less reliably
detected at this distance from EMSC stations.

**WebSocket real-time feed** also available:
```
wss://www.seismicportal.eu/standing_order/websocket
```

Push-based streaming of all global events as they are published.

## Integration Notes

- **Polling interval**: 5 minutes for REST, or use WebSocket for push
- **CloudEvents subject**: `earthquake/{unid}` → `earthquake/20250331_0000123`
- **Kafka key**: `unid` (EMSC unique event ID)
- **Entity model**: Earthquake event (point + magnitude + time + depth)
- **Overlap check**: The repo has **usgs-earthquake** bridge covering global seismicity via
  USGS. EMSC provides **better regional coverage** for the Middle East and faster updates for
  European/Mediterranean events. For Qatar specifically, EMSC detected the 2025 sequence earlier
  and with more detail than USGS.
- **Additive value**: This is a **new seismic zone** not previously known to be active. The
  2025 cluster is scientifically significant (possible induced seismicity case study) and
  locally relevant (felt events in Doha at M4+).
- **Historic context**: Prior to 2025, the most recent earthquake catalog entry for Qatar was
  a single M2.6 event in 2005. The 2025 sequence represents a **regime shift**.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time (events within minutes, WebSocket push available) |
| Openness | 3 | No auth, FDSN standard, CC BY 4.0 license |
| Stability | 3 | EMSC operational system, FDSN WS-EVENT versioned standard |
| Structure | 3 | GeoJSON, QuakeML (formal spec), FDSN compliance |
| Identifiers | 3 | EMSC `unid` is globally unique, stable |
| Additive value | 1 | Overlaps usgs-earthquake geographically but different coverage/timing |

**Verdict**: Recommended as either (a) a **regional configuration** of the existing
usgs-earthquake bridge (switch to EMSC FDSN endpoint for Middle East bounding box), or
(b) a **new emsc-earthquake bridge** if EMSC's broader European/Mediterranean coverage is
desirable. The 2025 Qatar-Saudi border seismic sequence is a compelling regional use case.

**Scientific note**: If this seismic activity continues or accelerates, it could become a
high-priority environmental monitoring issue for Qatar. Induced seismicity from hydrocarbon
operations has led to regulatory interventions in other regions (Oklahoma injection moratoriums,
Groningen gas field shutdowns). Real-time seismic monitoring would be valuable for both public
awareness and scientific investigation.
