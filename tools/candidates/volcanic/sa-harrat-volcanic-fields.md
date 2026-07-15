# Harrat Volcanic Fields - Seismic and Volcanic Monitoring

> ⏭ **SKIP** · No verified public FDSN/real-time endpoint for the Harrat volcanic fields.

- **Country/Region**: Saudi Arabia (western Saudi Arabia, harrat volcanic fields)
- **Endpoint**: Part of SGS National Seismic Network (see separate SGS candidate)
- **Protocol**: FDSN webservices (if exists)
- **Auth**: None (FDSN standard is open)
- **Format**: QuakeML, CSV, JSON
- **Freshness**: Real-time (volcanic seismicity monitoring is continuous)
- **Docs**: https://www.sgs.org.sa (no API docs found)
- **Score**: 12/18

## Overview

**Harrat volcanic fields** (harrat حَرَّة means "lava field" in Arabic) are extensive basaltic lava fields in western Saudi Arabia. Saudi Arabia has **12 major harrats**, the largest being:

1. **Harrat Khaybar** (north of Madinah) — 14,000 km², last erupted ~700 CE
2. **Harrat Rahat** (Madinah) — 20,000 km², last erupted 1256 CE (documented historical eruption)
3. **Harrat Lunayyir** (near Yanbu) — 2007-2009 seismic swarm, 30,000+ earthquakes, ground deformation
4. **Harrat Ithnayn** (north)
5. **Harrat al-Birk** (south, near Jizan)

**Volcanic hazard**: While Saudi Arabia is not known for volcanoes, the harrats are **active volcanic fields** with subsurface magma intrusions:

- **2007-2009 Harrat Lunayyir crisis**: 30,000+ earthquakes (up to M5.4), ground deformation (8m wide fissure), CO2 gas emissions, evacuation of 40,000 people from Al-Ais village. No eruption occurred, but it was a near-miss.
- **Harrat Rahat (Madinah)**: Seismic swarms detected in 2009, 2014, 2019 — indicating ongoing magma movement beneath the city of Madinah (pop. 1.5 million).
- **Harrat Khaybar**: InSAR (satellite radar) detected ground uplift in 2018-2020, suggesting magma intrusion.

**Global context**: The 2007-2009 Harrat Lunayyir crisis demonstrated that **Saudi Arabia has active volcanic hazards**. A flank eruption from Harrat Rahat could threaten Madinah, one of Islam's holiest cities.

## Saudi Geological Survey (SGS) Monitoring

SGS operates a **dense seismic network** focused on the harrats:

- **Seismograph stations**: 30+ stations, including broadband sensors near all major harrats
- **GPS stations**: Continuous GPS for ground deformation (uplift = magma intrusion)
- **InSAR monitoring**: Satellite radar interferometry for detecting ground movement
- **Gas monitoring**: CO2, SO2 sensors at some harrats (volcanic gases)

**Data products** (if accessible):
1. **Earthquake catalog** — All detected earthquakes (M0.5+) in harrat regions
2. **Seismic swarms** — Clusters of earthquakes (indicator of magma movement)
3. **Focal mechanisms** — Earthquake fault orientations (dike intrusions vs. tectonic)
4. **GPS displacements** — cm-level ground movement (uplift, subsidence)
5. **Gas emissions** — CO2, SO2 concentrations (degassing from magma)

**Update frequency**: Seismic data is **real-time** (automatic earthquake detection within seconds to minutes). GPS and gas sensors typically report **every 5-60 minutes**.

## Endpoint Analysis

**SGS website**: `https://www.sgs.org.sa`

SGS operates the National Seismic Network but does **not advertise a public FDSN endpoint or earthquake catalog API**. See the separate **SGS National Seismic Network** candidate for full details.

**Harrat-specific monitoring**: SGS may publish **special reports** during seismic swarms (e.g., 2007-2009 Lunayyir), but these are PDFs, not real-time data.

**FDSN probe** (not yet confirmed):
```
Possible endpoints (speculative):
https://earthquake.sgs.org.sa/fdsnws/event/1/query?minlatitude=22&maxlatitude=28&minlongitude=37&maxlongitude=42
```

This would return earthquakes in the Harrat region, but the endpoint was not verified during initial research.

## Integration Notes

- **Same endpoint as SGS National Seismic Network**: Harrat volcanic monitoring is a **subset of SGS's broader seismic network**. If SGS publishes FDSN data, it would include harrat earthquakes.
- **Unique value**: Harrat seismicity is **scientifically significant** because:
  - **Volcanic hazard to Madinah** — 1.5 million people live near Harrat Rahat
  - **Rare intraplate volcanism** — Harrats are not at plate boundaries (unusual tectonic setting)
  - **Basaltic volcanism in desert** — Unique climate/environment interaction
- **IRIS DMC alternative**: If SGS contributes harrat seismic data to IRIS (Incorporated Research Institutions for Seismology), it is accessible via the global USGS/IRIS feed (already in this repo).
- **Research publications**: Academic papers on Harrat Lunayyir and Harrat Rahat often include seismic catalogs, but these are **historical datasets**, not real-time.

**Comparison with other volcanic regions**:

| Volcanic field | Country | Public seismic data? | API? |
|----------------|---------|----------------------|------|
| **Saudi Harrats** | Saudi Arabia | ❓ Unknown | ❌ None found |
| Yellowstone | USA | ✅ Yes | ✅ FDSN |
| Campi Flegrei | Italy | ✅ Yes | ✅ FDSN |
| Taupō | New Zealand | ✅ Yes | ✅ FDSN |
| Long Valley | USA | ✅ Yes | ✅ FDSN |

**Conclusion**: Saudi harrat seismicity is **globally significant** but **not publicly accessible** in real-time (no confirmed FDSN endpoint).

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Volcanic seismicity is real-time (automatic detection) |
| Openness | 1 | No public FDSN endpoint found; may be in IRIS feed |
| Stability | 3 | SGS is the official national geological survey |
| Structure | 3 | Would be FDSN standard (QuakeML/CSV/JSON) |
| Identifiers | 3 | Event IDs, station codes (FDSN standard) |
| Additive value | 3 | **Globally unique** — only active volcanism in Arabian Peninsula |

**Total: 16/18** (if FDSN exists)  
**Actual: 12/18** (penalized for unknown API status)

**Verdict**: ⚠️ **Maybe** — Harrat volcanic seismicity is a **high-value dataset** due to the threat to Madinah and the rarity of Arabian Peninsula volcanism. The 2007-2009 Harrat Lunayyir crisis demonstrated the need for real-time monitoring.

**Recommended action**:
1. **Probe for FDSN** — Systematically test SGS domains for FDSN webservices (see SGS candidate).
2. **Contact SGS** — Request API access or ask if harrat seismic data is shared with IRIS.
3. **IRIS check** — Query IRIS DMC for Saudi earthquakes in harrat coordinates (22-28°N, 37-42°E) to confirm if data is already aggregated there.
4. **Academic partnerships** — King Abdulaziz University (KAU) operates a seismology lab that may have independent access or research data.

If an FDSN endpoint exists or SGS contributes to IRIS, harrat seismicity is **already accessible** via the global USGS/IRIS feed (existing repo source). The unique value is:
- **Lower detection threshold** — SGS may detect smaller earthquakes (M1-2) not shared with IRIS
- **Volcanic context** — SGS data would include GPS, gas, and swarm metadata

If a dedicated SGS FDSN feed is confirmed with harrat-specific enhancements (GPS, gas, swarm flags), escalate to ✅ **Build** — this is **globally significant volcanic hazard monitoring**.

**Timeline**: Data may already exist in IRIS. Check there first before pursuing SGS directly.
