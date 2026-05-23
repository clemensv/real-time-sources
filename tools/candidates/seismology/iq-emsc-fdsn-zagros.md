# EMSC FDSN - Iraq/Zagros Seismic Region

- **Country/Region**: Iraq, Iran-Iraq border, Turkey-Iraq-Iran tri-border (Zagros fault zone)
- **Endpoint**: `https://www.seismicportal.eu/fdsnws/event/1/query`
- **Protocol**: FDSN Web Service (HTTP/REST)
- **Auth**: None
- **Format**: JSON, QuakeML, XML, text
- **Freshness**: Real-time (events appear within 5-15 minutes of detection)
- **Docs**: https://www.seismicportal.eu/fdsn-wsevent.html
- **Score**: 17/18

## Overview

The European-Mediterranean Seismological Centre (EMSC) operates a global real-time earthquake monitoring network with excellent coverage of the Zagros seismic belt that runs through western Iran and the Iran-Iraq border region. The Zagros fault zone is one of the most seismically active regions in the world, resulting from the collision of the Arabian and Eurasian plates.

Iraq sits on the western edge of this zone and experiences frequent earthquakes, particularly in the Kurdistan region (Erbil, Sulaymaniyah, Duhok) and along the Iranian border. Major cities including Baghdad, Basra, and Mosul can feel tremors from larger events. The area has experienced several devastating earthquakes, including the 2017 M7.3 Sarpol-e Zahab event that killed over 600 people.

The EMSC FDSN service provides standardized access to earthquake catalogs with sub-minute latency for larger events.

## Endpoint Analysis

**FDSN Web Service verified** — the endpoint follows the FDSN specification (federated seismological data network standard).

Sample request for Iraq bounding box:
```
GET https://www.seismicportal.eu/fdsnws/event/1/query?format=json&minlatitude=29&maxlatitude=38&minlongitude=38&maxlongitude=49&minmagnitude=2.5
```

Response includes:
```json
{
  "type": "FeatureCollection",
  "metadata": {"count": 10},
  "features": [{
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [47.7391, 34.0218, -10.0]},
    "id": "20260519_0000161",
    "properties": {
      "source_id": "1997143",
      "source_catalog": "EMSC-RTS",
      "lastupdate": "2026-05-19T12:52:52.757783Z",
      "time": "2026-05-19T11:50:29.34Z",
      "flynn_region": "WESTERN IRAN",
      "lat": 34.0218,
      "lon": 47.7391,
      "depth": 10.0,
      "evtype": "ke",
      "auth": "EMSC",
      "mag": 4.8,
      "magtype": "mb",
      "unid": "20260519_0000161"
    }
  }]
}
```

Events are keyed by `unid` (unique identifier in `YYYYMMDD_NNNNNNN` format).

Flynn regions covering Iraq:
- "TURKEY-IRAQ BORDER REGION"
- "TURKEY-IRAN-IRAQ BORDER REGION"  
- "TURKEY-SYRIA-IRAQ BORDER REGION"
- "WESTERN IRAN" (many events affect Iraq)
- "SYRIA" (some events felt in western Iraq)

## Integration Notes

- **Polling bridge recommended**: Query every 60 seconds with `starttime` parameter to get incremental events.
- **Bounding box**: lat 29-38°N, lon 38-49°E covers Iraq plus the full Zagros seismic zone.
- **Magnitude threshold**: 2.5+ to capture felt earthquakes; 4.0+ for significant events.
- **Stable identifiers**: The `unid` field is the perfect Kafka key — stable, unique, monotonic.
- **FDSN standard**: This is the same protocol used by USGS (already in repo), so bridge pattern is well understood.
- **Real-time stream**: EMSC also offers a WebSocket stream at `https://www.seismicportal.eu/realtime.html` (would be a streaming bridge alternative).
- **Coverage vs USGS**: EMSC has faster detection for smaller events in the Zagros region due to regional network density. USGS is authoritative for M4.5+ globally. Both should be kept — they complement each other.
- **Regional importance**: Iraq has no functioning national seismological network as of 2025. EMSC (and USGS) are the only real-time earthquake data sources available.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, 5-15 minute latency for detection |
| Openness | 3 | No auth, no rate limits, FDSN standard |
| Stability | 3 | FDSN spec, versioned, operational since 2004 |
| Structure | 3 | JSON/QuakeML/XML, formal FDSN schema |
| Identifiers | 3 | Unique `unid` per event, perfect key |
| Richness | 2 | Location, magnitude, depth, agency, flynn region |

**Verdict**: ✅ **Strong candidate** — Real-time seismology for Iraq and the Zagros fault zone. FDSN standard bridge pattern. Critical data for a seismically active frontier region with no national monitoring. Better regional coverage than USGS alone for smaller felt earthquakes. Ready for bootstrap.
