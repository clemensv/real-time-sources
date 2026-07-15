# Oman National Seismic Network (FDSN OM)

> ⏭ **SKIP** · No working public Oman (SQU/EMQC) FDSN node; the region is already covered by the shipped EMSC feed.

- **Country/Region**: Sultanate of Oman
- **Endpoint**: FDSN web services via IRIS/GEOFON (network code `OM`)
- **Protocol**: FDSN web services (fdsnws-station, fdsnws-event, fdsnws-dataselect)
- **Auth**: None
- **Format**: Text, XML (QuakeML), miniSEED
- **Freshness**: Event-driven (earthquakes), stations updated as network changes
- **Docs**: https://www.fdsn.org/networks/detail/OM/ , http://www.squ.edu.om/emc
- **Score**: 14/18

## Overview

The **Earthquake Monitoring Center (EQMC)** at Sultan Qaboos University operates the **Oman National Seismic Network** (FDSN network code `OM`), established in 2001 as the **Earthquake Monitoring Program of Oman (EMPO)**. The network monitors seismic activity across the Sultanate of Oman and the broader Arabian Peninsula-Makran subduction zone region.

Oman sits at the southeastern edge of the Arabian Plate, with significant tectonic activity:
- **Makran Subduction Zone** (offshore southern Iran/Pakistan) — capable of generating magnitude 8+ earthquakes and tsunamis that threaten Oman's northern coast.
- **Zagros fold-and-thrust belt** (Iran) — frequent M4-5 earthquakes along the Gulf of Oman.
- **Intraplate seismicity** within Oman itself — lower magnitude but locally significant.
- **Owen Fracture Zone** (offshore eastern Oman, Indian Ocean) — transform boundary with occasional M5-6 events.

The 2013 M7.7 earthquake in Balochistan, Pakistan, was felt across Oman and raised awareness of the tsunami hazard from Makran events. EQMC's monitoring network is regionally important for both local earthquake early warning and contribution to the broader FDSN global seismology effort.

## Endpoint Analysis

**FDSN network confirmed** — the `OM` network is registered with the International Federation of Digital Seismograph Networks (FDSN) and archived/distributed via IRIS DMC (Incorporated Research Institutions for Seismology Data Management Center).

### Station Metadata

Standard FDSN station web service query:
```
GET https://service.iris.edu/fdsnws/station/1/query?network=OM&level=station&format=text
```

Alternative via GEOFON (GFZ Potsdam):
```
GET https://geofon.gfz-potsdam.de/fdsnws/station/1/query?network=OM&level=station&format=text
```

**Note**: During testing (2026-05-23), IRIS returned empty results for the OM network station query, suggesting either:
1. Station metadata is not currently published to IRIS (possible lag in archiving)
2. The network is registered but stations are only served via SQU's local FDSN node (if one exists)
3. Data availability is restricted or embargo period applies

The FDSN network detail page confirms the network exists and is operated by Sultan Qaboos University. The website listed is http://www.squ.edu.om/emc (Earthquake Monitoring Center), but the EQMC subdomain (eqmc.squ.edu.om) was unreachable during discovery testing.

### Event Data

Earthquakes detected by the OM network should be queryable via FDSN event services:
```
GET https://service.iris.edu/fdsnws/event/1/query?network=OM&starttime=2025-01-01&format=geojson
```

Or for regional events affecting Oman (latitude 16-27°N, longitude 52-60°E):
```
GET https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2026-01-01&minlatitude=16&maxlatitude=27&minlongitude=52&maxlongitude=60
```

**Testing result**: USGS FDSN query for the Oman region returned no events in the requested timeframe (April-May 2026), which is expected — Oman experiences infrequent local seismicity. Most M4+ events in the broader region are concentrated offshore in the Makran zone or along the Zagros mountains in southern Iran.

## Integration Notes

- **Station identifiers**: FDSN uses `network.station.location.channel` naming (e.g., `OM.ABC.00.BHZ` for a broadband vertical channel at station ABC). These are globally unique and stable.
- **Update frequency**: 
  - **Stations**: Updated when network configuration changes (new stations, decommissioned sensors). Typically static for months/years.
  - **Events**: Earthquake catalog is event-driven. A magnitude 4.0+ event in Oman would appear in the FDSN event catalogs within minutes to hours of detection (automated picks), with refined parameters within days (analyst review).
- **Real-time vs. archival**: FDSN web services provide both near-real-time event notifications and archival waveform data (fdsnws-dataselect). For a real-time bridge, the **event service** is the target — it delivers earthquake parameters (time, location, depth, magnitude) as structured QuakeML or GeoJSON.
- **Data availability concern**: The inability to fetch station lists or confirm active FDSN nodes at SQU during testing is a **yellow flag**. Before building a bridge, the following must be verified:
  1. Does EQMC/SQU operate a public FDSN web services node (`http://eqmc.squ.edu.om/fdsnws/...` or similar)?
  2. Is OM network data embargoed, or only available through IRIS with a delay?
  3. Are OM-detected events reliably published to IRIS/EMSC/USGS catalogs, or does SQU maintain a separate internal catalog?
- **Alternative: EMSC for regional coverage**: The European-Mediterranean Seismological Centre (EMSC) publishes a real-time GeoJSON feed of global earthquakes via `https://www.seismicportal.eu/fdsnws/event/1/`. Testing confirmed EMSC serves earthquakes in the Oman region (mostly offshore or southern Iran). EMSC is already a strong global candidate and may provide better coverage than OM-network-specific queries if SQU's FDSN node is not publicly accessible.
- **Additive value**: The repo has USGS earthquake data (global coverage). An OM-network-specific bridge would only add value if:
  - SQU publishes events **faster** than USGS (unlikely for global catalog, but possible for local-only events below USGS reporting threshold)
  - OM network detects smaller local events (M2-3) that USGS global catalog does not include
  - Regional focus provides better-quality hypocenters for Oman/Gulf region than global catalogs

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Event-driven (earthquakes are unpredictable), but when they occur, FDSN serves within hours |
| Openness | 3 | FDSN spec is open, no auth for public data |
| Stability | 3 | FDSN is a formal international standard (IRIS, GEOFON, INGV all implement it) |
| Structure | 3 | QuakeML (XML), GeoJSON, Text — all strongly typed with formal schemas |
| Identifiers | 2 | Network.station codes are stable, event IDs are unique but vary by source (USGS vs EMSC vs SQU) |
| Additive value | 1 | Overlaps with USGS global earthquake coverage; unclear if SQU publishes OM-only catalog with better local detail |

**Verdict**: ⚠️ Maybe

The Oman National Seismic Network is **scientifically valuable** and the FDSN data model is a **perfect fit** for this repo (the existing USGS bridge already uses FDSN/GeoJSON). However, **data accessibility is uncertain**:
- SQU's EQMC website (eqmc.squ.edu.om) was unreachable during discovery.
- IRIS queries for OM network stations returned no results.
- No public FDSN node URL for SQU was found in documentation.

**Recommended next steps**:
1. Contact Sultan Qaboos University EQMC directly to confirm:
   - Is there a public FDSN web services endpoint?
   - Is OM network data available in real-time or under embargo?
   - Does SQU publish a local earthquake catalog that includes sub-M3 events not in USGS/EMSC?
2. If SQU does not operate a public FDSN node, **fallback to EMSC** as the regional source for Oman earthquakes. EMSC's real-time feed is working, well-documented, and already covers the Oman region (tested 2026-05-23 with recent M4+ events offshore in southern Iran).
3. Alternatively, build a **regional EMSC bridge** (Middle East / Arabian Peninsula bounding box) rather than an Oman-specific one — this would be additive to the existing USGS global feed by providing faster European-perspective earthquake detection.

**If SQU confirms a working public FDSN node with OM-network event catalog, upgrade this to ✅ Build.**
