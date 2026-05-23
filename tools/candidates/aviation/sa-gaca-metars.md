# General Authority of Civil Aviation (GACA) - METARs and Aviation Weather

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: Unknown (no public METAR feed found)
- **Protocol**: IWXXM XML or TAC text (ICAO standard)
- **Auth**: Unknown
- **Format**: XML (IWXXM) or plain text (TAC)
- **Freshness**: Hourly (METARs) or as-needed (SPECIs)
- **Docs**: https://gaca.gov.sa (no API docs)
- **Score**: 9/18

## Overview

The **General Authority of Civil Aviation** (الهيئة العامة للطيران المدني, GACA) is Saudi Arabia's aviation regulator and air navigation services provider. GACA is responsible for:

- **Air traffic control** — All Saudi airspace
- **Meteorological services** — Aviation weather (METARs, TAFs, SIGMETs) for airports
- **Airport certification** — Safety and operations standards
- **Airline regulation** — Licensing and oversight

Saudi Arabia has **27 commercial airports**, including major international hubs:

- **King Abdulaziz International (OEJN/JED)** — Jeddah, serves Hajj pilgrims, 41M pax/year
- **King Khalid International (OERK/RUH)** — Riyadh, capital hub, 27M pax/year
- **King Fahd International (OEDF/DMM)** — Dammam, world's largest airport by land area (780 km²)
- **Prince Mohammad bin Abdulaziz (OEMA/MED)** — Madinah, Hajj pilgrims, 8M pax/year

**Hajj aviation**: During the annual Hajj pilgrimage, Jeddah and Madinah airports handle **~2 million international pilgrims** arriving by air (plus 1M+ domestic). This is one of the world's largest seasonal aviation surges.

## METAR and IWXXM Background

**METAR** (Meteorological Aerodrome Report) is the international standard for aviation weather observations. METARs are issued:
- **Hourly** at major airports (e.g., OEJN, OERK)
- **Half-hourly** at some hubs
- **Ad-hoc (SPECI)** when weather changes significantly (visibility drop, thunderstorms, etc.)

METARs include:
- Wind speed/direction
- Visibility
- Weather phenomena (rain, dust storms, fog)
- Cloud cover and ceiling
- Temperature and dewpoint
- Barometric pressure (QNH)

**IWXXM** (ICAO Meteorological Information Exchange Model) is the new XML-based format for aviation weather, replacing traditional TAC (text) format. ICAO mandates IWXXM adoption globally by 2025.

**Saudi Arabia-specific weather**: Saudi aviation METARs frequently report:
- **Dust storms (DS, BLDU)** — Haboobs reduce visibility to <1 km, close airports
- **High temperatures** — Summer temperatures at Riyadh/Jeddah airports exceed 45°C, affecting aircraft performance
- **Thunderstorms** — Rare but severe when they occur (Jeddah flash floods 2009, 2011)

## Endpoint Analysis

**GACA website**: `https://gaca.gov.sa`

GACA's website provides regulatory information, licensing, and news. **No public weather data portal or METAR feed** is advertised.

**ICAO OPMET (Operational Meteorological data)**: The global standard for distributing aviation weather is the ICAO OPMET Data Bank and SADIS (Satellite Distribution System). However, these are **restricted to registered aviation users** (airlines, ATC, flight planning services).

**Public METAR sources**: Most countries' METARs are available via:
1. **NOAA Aviation Weather Center** (aviationweather.gov) — Aggregates global METARs, including Saudi Arabia
2. **OGIMET** (ogimet.com) — European aggregator, includes Middle East
3. **National met services** — Some publish their own METAR APIs

**Saudi Arabia METARs on NOAA AWC**:
```
https://aviationweather.gov/data/metar/?id=OEJN  (Jeddah)
https://aviationweather.gov/data/metar/?id=OERK  (Riyadh)
https://aviationweather.gov/data/metar/?id=OEDF  (Dammam)
```

These endpoints work, but the **data source is NOAA**, not GACA. Building a "Saudi METAR" bridge would be redundant with NOAA's existing global coverage.

**GACA-specific API**: No evidence of a direct GACA METAR API exists. GACA likely contributes METARs to ICAO OPMET, which NOAA then redistributes.

## Integration Notes

- **Already covered by NOAA**: Saudi METARs are available via NOAA Aviation Weather Center, which is already a global source. A dedicated GACA bridge adds no value.
- **ICAO OPMET access**: If GACA publishes an IWXXM feed for Saudi airports (required by ICAO 2025 mandate), it may be restricted to registered aviation users, not public.
- **Dust storm value**: Saudi METARs are valuable for tracking **haboob dust storms**, which are frequent and disruptive. However, this data is already accessible via NOAA.
- **Alternative: NCM (National Center for Meteorology)**: NCM is the official met service for Saudi Arabia and provides weather data to GACA for aviation use. NCM may have dust storm / airport weather APIs (see separate NCM candidate).

**Comparison with other aviation authorities**:

| Authority | Country | Public METARs? | API? |
|-----------|---------|----------------|------|
| **GACA** | Saudi Arabia | ❌ Not directly | ❌ None found |
| FAA | USA | ✅ Via NOAA | ✅ REST |
| EASA / EUMETNET | Europe | ✅ Via OGIMET | ✅ OPMET |
| JCAB / JMA | Japan | ✅ Via JMA | ✅ XML |
| CASA / BOM | Australia | ✅ Via BOM | ✅ REST |

Most aviation authorities either delegate METAR distribution to their national met service or contribute to international aggregators (NOAA, OGIMET).

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | METARs are hourly or more frequent |
| Openness | 1 | Saudi METARs exist via NOAA, but no direct GACA API |
| Stability | 3 | GACA is the official aviation authority; ICAO standards are stable |
| Structure | 2 | TAC text or IWXXM XML (both are standards) |
| Identifiers | 3 | ICAO airport codes (OEJN, OERK, etc.) are globally stable |
| Additive value | 0 | Fully duplicated by NOAA Aviation Weather Center |

**Total: 12/18** (if direct API existed)  
**Actual: 9/18** (penalized for being redundant with NOAA)

**Verdict**: ❌ **Skip** — Saudi METARs are already available via **NOAA Aviation Weather Center** (aviationweather.gov), which aggregates global aviation weather. Building a GACA-specific bridge adds **zero value** unless GACA publishes:
1. **Faster updates** (sub-hourly SPECIs)
2. **Additional parameters** not shared with NOAA
3. **Dust storm details** (PM10, visibility sectors) beyond standard METAR

None of these are confirmed. **Use NOAA Aviation Weather Center** for Saudi METARs instead of building a dedicated bridge.

**Alternative**: If NCM (National Center for Meteorology) publishes an API with airport weather or dust storm data, that would be additive. Focus on **NCM**, not GACA.
