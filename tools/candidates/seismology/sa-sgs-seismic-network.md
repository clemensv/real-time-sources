# Saudi Geological Survey (SGS) - National Seismic Network

> ⏭ **SKIP** · No verified public FDSN/real-time endpoint for the Saudi SGS network.

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: Unknown FDSN endpoint (not confirmed)
- **Protocol**: FDSN webservices (if exists)
- **Auth**: None (FDSN standard is open)
- **Format**: QuakeML, CSV, JSON
- **Freshness**: Minutes (automatic earthquake detection)
- **Docs**: https://www.sgs.org.sa (no API docs found)
- **Score**: 11/18

## Overview

The Saudi Geological Survey (هيئة المساحة الجيولوجية السعودية, SGS) operates Saudi Arabia's **National Seismic Network (NSN)**, monitoring earthquake and volcanic activity across the Arabian Peninsula. Saudi Arabia experiences:

- **Frequent seismicity** — The Red Sea rift is an active spreading center, causing earthquakes along the western coast (Jeddah, Yanbu, Jizan).
- **Harrat volcanic fields** — Saudi Arabia has 12 basaltic volcanic fields (harrats), including:
  - **Harrat Khaybar** (north of Madinah) — last erupted ~700 CE
  - **Harrat Lunayyir** (near Yanbu) — 2007-2009 seismic swarm with 30,000+ earthquakes, ground deformation, and evacuation of 40,000 people
  - **Harrat Rahat** (Madinah) — active subsurface magma intrusion detected
- **Induced seismicity** — Wadis (dry riverbeds) with dam reservoirs occasionally trigger earthquakes when filled.

The National Seismic Network includes **30+ seismograph stations** distributed across Saudi Arabia, focusing on:
- Western coast (Red Sea rift zone)
- Harrat fields (volcanic monitoring)
- Major cities (Riyadh, Jeddah, Dammam)
- Northern border (Syrian and Dead Sea fault systems)

**Global context**: The 2007-2009 Harrat Lunayyir crisis demonstrated that Saudi Arabia has **active volcanic hazards**. While the harrats have not had a major eruption in modern times, seismic monitoring is critical for early warning. A flank eruption could threaten Madinah (pop. 1.5M) or Yanbu (major industrial port).

## Endpoint Analysis

**SGS website**: `https://www.sgs.org.sa`

The SGS website provides information about the seismic network and volcanic monitoring, but **no public earthquake catalog or API is documented**.

**Known seismic stations** (per SGS website):
- The network includes broadband, short-period, and strong-motion seismometers.
- Station metadata page: `https://www.admin.sgs.org.sa/en/activities/geologic-hazards/earthquakes-and-volcanoes/earthquakes/seismic-stations/`

**FDSN probe**:
FDSN (International Federation of Digital Seismograph Networks) is the global standard for seismic data exchange. Major seismic networks publish data via FDSN webservices at standardized paths:

```
http://[domain]/fdsnws/event/1/query
http://[domain]/fdsnws/station/1/query
http://[domain]/fdsnws/dataselect/1/query
```

**Attempted FDSN probes** (not executed due to lack of confirmed domain):
```
Possible domains:
- https://earthquake.sgs.org.sa/fdsnws/event/1/
- https://seismic.sgs.org.sa/fdsnws/event/1/
- https://fdsn.sgs.org.sa/fdsnws/event/1/
- https://www.sgs.org.sa/fdsnws/event/1/
```

None of these were confirmed during initial research. SGS does **not advertise FDSN compliance** on its website.

**Alternative: IRIS DMC**:
The Incorporated Research Institutions for Seismology (IRIS) Data Management Center aggregates seismic data from global networks. SGS may contribute data to IRIS, in which case Saudi earthquakes are accessible via:

```
https://service.iris.edu/fdsnws/event/1/query?starttime=2024-01-01&endtime=2024-12-31&minlatitude=16&maxlatitude=33&minlongitude=34&maxlongitude=56&format=json
```

This would return earthquakes in the Saudi Arabia bounding box, but the data source would be "IRIS," not "SGS."

**Comparison with regional networks**:

| Network | Country | FDSN? | Public API? |
|---------|---------|-------|-------------|
| **SGS NSN** | Saudi Arabia | ❓ Unknown | ❌ None found |
| USGS | Global | ✅ Yes | ✅ REST/FDSN |
| GeoNet | New Zealand | ✅ Yes | ✅ FDSN |
| INGV | Italy | ✅ Yes | ✅ FDSN |
| EMSC | Europe/Med | ✅ Partial | ✅ REST |
| JMA | Japan | ✅ Yes | ✅ XML feeds |

SGS is an outlier in not publishing a public earthquake catalog or FDSN endpoint.

## Integration Notes

- **FDSN endpoint unknown**: The primary blocker is the lack of a documented FDSN webservice. SGS may operate one internally without advertising it, or may only share data bilaterally with research institutions.
- **IRIS fallback**: If SGS contributes to IRIS, Saudi earthquakes are already accessible via the USGS/IRIS global feed (which is **already in this repo**). Building an SGS-specific bridge adds value only if SGS provides:
  - **Lower latency** than IRIS (automatic vs. reviewed catalogs)
  - **More events** (smaller magnitudes not shared internationally)
  - **Volcanic monitoring** (gas emissions, deformation, seismic swarms specific to Harrat fields)
- **Volcanic monitoring gap**: The **Harrat Lunayyir** seismic swarm (2007-2009) was a near-miss for a major volcanic crisis. SGS's real-time swarm detection would be globally significant if published. No other source tracks Arabian Peninsula volcanic seismicity in detail.
- **Outreach opportunity**: SGS is part of Saudi Arabia's Vision 2030 digital transformation. Contact SGS to request FDSN webservice publication or a developer API.
- **King Abdulaziz University**: KAU operates a seismology research lab that may have independent data access or partnerships with SGS.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Earthquake detection is real-time (automatic picks) |
| Openness | 1 | No public API found; FDSN status unknown |
| Stability | 3 | SGS is the official national geological survey |
| Structure | 3 | Would be FDSN standard (QuakeML/CSV/JSON) |
| Identifiers | 2 | Event IDs, station codes (if FDSN) |
| Additive value | 2 | Overlaps with USGS for large events; unique for Harrat volcanoes |

**Total: 14/18** (if FDSN exists)  
**Actual: 11/18** (penalized for unknown API)

**Verdict**: ⚠️ **Maybe** — High-value dataset for **volcanic hazard monitoring** (Harrat fields) and Red Sea rift seismicity. The 2007-2009 Harrat Lunayyir crisis demonstrated the need for real-time seismic monitoring of Saudi volcanoes. 

**Recommended action**:
1. **Probe for FDSN**: Systematically test `earthquake.sgs.org.sa`, `seismic.sgs.org.sa`, `fdsn.sgs.org.sa` for FDSN webservices.
2. **Contact SGS**: Email SGS or KAU seismology lab to request API access or FDSN endpoint details.
3. **IRIS check**: Query IRIS DMC for Saudi earthquakes to confirm SGS data is (or isn't) already aggregated there.

If an FDSN endpoint exists or can be negotiated, this becomes ✅ **Build** — Saudi Arabian volcanic seismicity is a unique dataset not available elsewhere in real-time.
