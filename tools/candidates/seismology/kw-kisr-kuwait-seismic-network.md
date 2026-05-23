# Kuwait Seismic Network (KISR / KNSN)

- **Country/Region**: Kuwait
- **Endpoint**: Unknown (no public API discovered)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown (likely QuakeML or FDSN if federated)
- **Freshness**: Unknown
- **Docs**: None publicly accessible
- **Score**: ?/18 (cannot evaluate — no API found)

## Overview

The **Kuwait National Seismic Network (KNSN)** is operated by the **Kuwait Institute for Scientific Research (KISR)** (معهد الكويت للأبحاث العلمية). KISR is Kuwait's premier research institution, conducting R&D in:

- Environmental sciences
- Water resources
- Energy and petroleum
- Food and agriculture
- **Geophysics and seismology**

**KNSN mission**:
- Monitor seismic activity within and near Kuwait
- Detect local earthquakes (rare) and regional events (Iran, Iraq, Zagros Mountains)
- Support earthquake early warning (not operational as of 2025)
- Contribute data to global seismological networks (FDSN, ISC)
- Research induced seismicity from oil/gas operations
- Seismic hazard assessment for infrastructure (buildings, oil facilities, desalination plants)

**Seismic context**:
- Kuwait sits on the **stable Arabian Plate**, with low intrinsic seismicity
- **Zagros Mountains** (Iran/Iraq border, ~300km northeast) generate M5–M7 earthquakes felt in Kuwait
- **Dibdibba aquifer** — shallow earthquakes (M<3) occasionally detected, possibly natural or induced
- **Oil field seismicity** — microseismic monitoring of reservoirs (Kuwait Oil Company), but data not public

**Network configuration** (estimated):
- ~5–10 seismic stations across Kuwait (exact count not public)
- Broadband seismometers
- Real-time telemetry to KISR data center
- Likely integrated with GCC seismic networks (Saudi Geological Survey, etc.)

## Endpoint Analysis

**KISR website probe** (2025-05-23):

```
GET https://www.kisr.edu.kw
GET https://kisr.edu.kw
GET https://www.kisr.edu.kw/en
GET https://www.kisr.edu.kw/seismic
GET https://www.kisr.edu.kw/earthquake
GET https://data.kisr.edu.kw
GET https://seismic.kisr.edu.kw
```

All attempts: Connection timeout or DNS failure

**FDSN station query** (2025-05-23):
```
GET https://service.iris.edu/fdsnws/station/1/query?net=*&sta=*&loc=*&cha=*&minlat=28.5&maxlat=30.5&minlon=46&maxlon=49&level=station&format=text
```

Result: **0 stations** returned

This indicates KNSN stations are **not federated** with the global FDSN (International Federation of Digital Seismograph Networks). Data is not shared publicly via FDSN web services.

**Alternative searches**:
- Searched "Kuwait seismic network API" — no results
- Searched "KISR earthquake data" — only research papers, no data portals
- Searched "Kuwait earthquake monitoring real-time" — no official feeds
- Searched Arabic: "الشبكة الزلزالية الكويتية" (Kuwait seismic network), "معهد الكويت للأبحاث الزلازل" (KISR earthquakes) — only academic publications

**USGS integration**:
- USGS Earthquake Hazards Program aggregates global seismic data
- Kuwait-region events (M≥2.5) appear in USGS catalog
- USGS likely receives Kuwait data via:
  - International Seismological Centre (ISC) bulletin exchange
  - Bilateral agreements with KISR (not public)
  - Regional Gulf seismic networks
- But **KNSN itself does not publish a public API**

## Schema / Sample Payload

**Cannot provide** — no accessible endpoint.

**Expected data model** (if FDSN-compliant API existed):

**QuakeML format**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<q:quakeml xmlns:q="http://quakeml.org/xmlns/quakeml/1.2">
  <eventParameters publicID="quakeml:kw.kisr/events">
    <event publicID="quakeml:kw.kisr/2025abcd">
      <preferredOriginID>quakeml:kw.kisr/origin/001</preferredOriginID>
      <preferredMagnitudeID>quakeml:kw.kisr/magnitude/001</preferredMagnitudeID>
      <type>earthquake</type>
      <description>
        <text>15km NE of Kuwait City</text>
      </description>
      <origin publicID="quakeml:kw.kisr/origin/001">
        <time>
          <value>2025-05-23T07:15:32.450Z</value>
        </time>
        <latitude>
          <value>29.4567</value>
        </latitude>
        <longitude>
          <value>48.1234</value>
        </longitude>
        <depth>
          <value>8000</value>  <!-- meters -->
        </depth>
      </origin>
      <magnitude publicID="quakeml:kw.kisr/magnitude/001">
        <mag>
          <value>2.8</value>
        </mag>
        <type>ML</type>  <!-- Local magnitude -->
      </magnitude>
    </event>
  </eventParameters>
</q:quakeml>
```

**Or GeoJSON** (FDSN query response format):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "kw2025abcd",
      "properties": {
        "mag": 2.8,
        "place": "15 km NE of Kuwait City, Kuwait",
        "time": 1716453332450,
        "updated": 1716453600000,
        "tz": null,
        "url": "https://www.kisr.edu.kw/events/kw2025abcd",
        "detail": "https://www.kisr.edu.kw/api/events/kw2025abcd",
        "felt": 5,
        "status": "reviewed",
        "tsunami": 0,
        "net": "kw",
        "code": "2025abcd",
        "magType": "ml",
        "type": "earthquake"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [48.1234, 29.4567, 8.0]
      }
    }
  ]
}
```

## Why This Would Be Valuable

If KNSN published real-time seismic data, it would provide:

1. **Local sensitivity** — KNSN stations detect smaller earthquakes (M<3) that global networks miss
2. **Faster alerts** — Local network detects Kuwait-region events seconds-to-minutes before global agencies
3. **Induced seismicity monitoring** — Track potential oil/gas-related micro-earthquakes
4. **Regional felt reports** — Earthquakes felt in Kuwait but epicentered in Iran/Iraq

**Use cases**:
- Early warning for critical infrastructure (oil refineries, desalination plants)
- Public safety (building codes, emergency response)
- Scientific research (Arabian Plate tectonics, reservoir geomechanics)

## Limitations

- **KISR website inaccessible** — Cannot verify existence of data portal
- **No FDSN federation** — KNSN stations not queryable via global FDSN services
- **Low seismicity** — Kuwait has minimal local earthquakes (rare M2–M3 events)
- **Data sharing barriers** — KISR may restrict data for research/security reasons
- **Regional events covered by USGS** — Large earthquakes (M≥4.5) felt in Kuwait are already captured by global networks

## Comparison to Alternatives

| Source | Coverage | Public API | Real-time |
|--------|----------|----------|-----------|
| **KNSN (KISR)** | Kuwait + region | ❌ None found | Unknown |
| **USGS** | Global | ✅ FDSN GeoJSON | ✅ Real-time |
| **EMSC** (Euro-Med) | Europe, Med, Middle East | ✅ GeoJSON, RSS | ✅ Real-time |
| **ISC** | Global | ⚠️ Reviewed (30-day lag) | ❌ No |
| **Saudi Geological Survey** | Saudi Arabia, Gulf | ❌ None found | Unknown |

For Kuwait earthquake monitoring, **USGS already provides the best public option** (see separate candidate file `kw-usgs-earthquakes-kuwait.md`).

## Verdict

**Verdict**: ❌ **Skip** — Kuwait National Seismic Network (KNSN/KISR) does not publish a public API or federate with global FDSN services. KISR website is inaccessible from external networks. For Kuwait seismic monitoring, the **USGS global earthquake feed** already provides adequate coverage (see `kw-usgs-earthquakes-kuwait.md`). Documented here as a **negative finding** to avoid redundant searches.

**Recommendation**:
- **For Kuwait earthquake monitoring**, rely on the existing **USGS global bridge** (already in repo)
- **For regional felt reports**, consider **EMSC** (European-Mediterranean Seismological Centre), which covers the Middle East
- **Long-term**, if KISR ever publishes an open data portal, revisit for local micro-seismicity (M<3 events not detected by global networks)

**Next steps** (if pursuing):
1. Attempt KISR website access from Kuwait IP (VPN/cloud instance)
2. Contact KISR directly: kisr@kisr.edu.kw (if functional) to inquire about data access
3. Check if Kuwait participates in regional seismic data-sharing initiatives (GCC seismic network?)
4. Monitor KISR research publications for mentions of real-time data portals
