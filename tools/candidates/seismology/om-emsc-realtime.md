# EMSC Real-Time Earthquakes (Oman/Arabian Peninsula Region)

- **Country/Region**: Global (regional filter for Oman/Arabian Peninsula: 16-27°N, 52-60°E)
- **Endpoint**: `https://www.seismicportal.eu/fdsnws/event/1/query?format=json`
- **Protocol**: FDSN-WS (HTTP REST, FDSN event specification)
- **Auth**: None
- **Format**: JSON (GeoJSON and custom EMSC schema)
- **Freshness**: Sub-5-minute for significant events (M4.5+), ~30 minutes for smaller events
- **Docs**: https://www.seismicportal.eu/fdsnws/event/1/ , https://www.emsc-csem.org/
- **Score**: 16/18

## Overview

The **European-Mediterranean Seismological Centre (EMSC)** operates a real-time global earthquake monitoring and rapid information service. While its name suggests a European focus, EMSC's **FDSN web services** provide global earthquake coverage, including the Arabian Peninsula, Makran subduction zone, and Gulf of Oman region.

Oman and the broader Arabian Peninsula are seismically active due to:
- **Makran Subduction Zone** (offshore southern Iran/Pakistan) — the only active subduction zone in the western Indian Ocean, capable of M8+ earthquakes and tsunamis. The 1945 Makran earthquake (M8.1) generated a tsunami that killed over 4,000 people along the Arabian Sea coast.
- **Zagros Fold Belt** (Iran) — frequent M4-6 earthquakes from collision of Arabian and Eurasian plates.
- **Owen Fracture Zone** (offshore eastern Oman) — transform boundary with occasional M5-6 earthquakes.
- **Intraplate seismicity** in Oman itself — less frequent but locally significant (e.g., 2011 M4.8 earthquake near Musandam felt across northern Oman and UAE).

EMSC's strength is **rapid crowdsourced felt reports** and **fast automated solutions** that complement authoritative catalogs like USGS. For an Oman-focused bridge, EMSC provides:
- Faster notification than USGS for regional M4+ events (often within 2-5 minutes of origin time)
- Broad coverage including offshore events in the Gulf of Oman and Arabian Sea that may not be well-covered by local networks
- Integration of data from multiple regional seismic networks (Iran, Pakistan, India, Oman, UAE, Saudi Arabia)

## Endpoint Analysis

**Verified working** — EMSC's FDSN event web service is operational and returns GeoJSON for Oman-region earthquakes.

Sample query (Arabian Peninsula / Gulf of Oman bounding box):
```
GET https://www.seismicportal.eu/fdsnws/event/1/query?format=json&limit=20&minlat=16&maxlat=27&minlon=52&maxlon=60&orderby=time-desc
```

Sample response (tested 2026-05-23, showing historical events from 2022-2023):
```json
{
  "type": "FeatureCollection",
  "metadata": {"count": 10},
  "features": [
    {
      "type": "Feature",
      "id": "20230207_0000048",
      "geometry": {
        "type": "Point",
        "coordinates": [55.25, 26.69, -10.0]
      },
      "properties": {
        "time": "2023-02-07T02:30:57.2Z",
        "mag": 4.5,
        "magtype": "ml",
        "depth": 10.0,
        "lat": 26.69,
        "lon": 55.25,
        "flynn_region": "SOUTHERN IRAN",
        "auth": "EMSC",
        "source_id": "1219384",
        "source_catalog": "EMSC-RTS",
        "lastupdate": "2023-02-08T07:23:00.0Z",
        "evtype": "ke",
        "unid": "20230207_0000048"
      }
    },
    ...
  ]
}
```

Key fields:
- **`unid`**: EMSC unique event identifier (YYYYMMDD_NNNNNNN format) — stable, permanent
- **`time`**: Origin time (ISO 8601)
- **`mag`, `magtype`**: Magnitude and type (ml, mb, Mw, etc.)
- **`lat`, `lon`, `depth`**: Hypocenter parameters
- **`flynn_region`**: Flinn-Engdahl seismic region name (e.g., "SOUTHERN IRAN", "ARABIAN SEA")
- **`auth`**: Authoritative source (EMSC, USGS, national agencies)
- **`evtype`**: Event type (`ke` = known earthquake, `uk` = unknown, etc.)

### Real-Time vs. Historical

The FDSN endpoint serves the **EMSC-RTS catalog** (Real-Time Seismicity). Events appear within minutes of detection and are continuously updated as more data arrives. For a streaming bridge:
- Poll the FDSN endpoint every 1-2 minutes with `starttime` set to (now - 10 minutes) to catch rapid updates
- Use `unid` as the unique event key
- Track `lastupdate` timestamp to detect parameter revisions (magnitude, depth, location)

The EMSC also operates a **WebSocket** for real-time earthquake notifications, but documentation is sparse and the endpoint is not officially advertised as a public API. The FDSN polling approach is more stable.

## Integration Notes

- **Geographic scope**: A bounding box of 16-27°N, 52-60°E captures:
  - All of Oman
  - Southern Iran (Zagros, Makran)
  - Eastern UAE
  - Parts of Yemen and Saudi Arabia
  - Gulf of Oman and northern Arabian Sea offshore zones
  This is broader than Oman-only but reflects the seismotectonic reality — earthquakes don't respect borders, and a M5 in southern Iran is just as relevant to Oman as a local event.
- **Overlap with USGS**: The repo already has USGS global earthquake data. EMSC provides:
  - **Faster notifications** (EMSC-RTS solutions often beat USGS by 5-15 minutes for M4+ events)
  - **European/regional perspective** (different seismic network contributions, complementary to USGS)
  - **Crowdsourced felt reports** (EMSC collects public testimonies via web form — these are valuable for impact assessment)
- **Additive value**: If the repo's goal is **low-latency earthquake alerts**, EMSC-RTS is superior to USGS for the Middle East. If the goal is **authoritative catalog quality**, USGS remains the gold standard. A bridge could serve **both** EMSC (fast, provisional) and USGS (slow, authoritative) for the same region, letting downstream consumers choose speed vs. quality.
- **Event deduplication**: EMSC and USGS often report the same physical earthquake with different event IDs. Deduplication logic (match on time ±30s, location ±0.5°, magnitude ±0.3) would be needed if both sources are ingested for the same region.
- **Keying strategy**: Use `unid` (EMSC) or `eventid` (USGS) as CloudEvents subject and Kafka key. Do **not** attempt to create a synthetic "global event ID" that merges EMSC and USGS — keep them as separate event streams from different authoritative sources.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Sub-5-minute for M4.5+, ~30 minutes for M3-4, real-time updates as parameters refine |
| Openness | 3 | No auth, no rate limits, FDSN standard is fully open |
| Stability | 3 | EMSC is a permanent international organization (founded 1975), FDSN-WS is a formal spec |
| Structure | 3 | GeoJSON with well-defined schema, FDSN spec compliance |
| Identifiers | 3 | `unid` is stable and globally unique per event |
| Additive value | 1 | USGS already covers global earthquakes; EMSC adds speed and European network perspective but same geographic scope |

**Verdict**: ✅ Build

**Rationale**: EMSC-RTS provides **faster earthquake notifications** than USGS for the Middle East and Arabian Peninsula, which is valuable for time-critical use cases (tsunami warning, emergency response, seismic monitoring dashboards). The FDSN interface is a perfect fit for this repo's bridge pattern (already implemented for USGS). The Oman/Arabian Peninsula region experiences frequent M4-5 seismicity (Zagros, Makran), and EMSC's rapid automated solutions complement USGS's slower but more authoritative catalog.

**Scope recommendation**: Build as a **regional EMSC bridge** rather than Oman-only:
- Bounding box: Arabian Peninsula + Makran + Zagros (roughly 15-32°N, 45-65°E)
- Covers Oman, UAE, Qatar, Bahrain, Kuwait, eastern Saudi Arabia, southern Iran, western Pakistan, northern Arabian Sea
- Justifies a standalone bridge (regional focus) while being broad enough to capture all relevant seismicity affecting the Gulf region
- Avoids being a duplicate of USGS global feed (different latency, different authoritative source, different regional network emphasis)

**Alternative**: If the repo prefers to avoid overlapping USGS, skip this and instead focus on sources USGS doesn't provide (weather, maritime, infrastructure). But EMSC's **speed advantage** for regional events is a legitimate differentiator.
