# Oman DGMET Aviation Weather (METARs)

- **Country/Region**: Sultanate of Oman
- **Endpoint**: `https://aviationweather.gov/api/data/metar?ids=OOMS,OOSA,OOSN,OOTH&format=json`
- **Protocol**: REST (Aviation Weather API)
- **Auth**: None
- **Format**: JSON
- **Freshness**: Hourly (standard METAR cadence)
- **Docs**: https://aviationweather.gov/data/api/
- **Score**: 11/18

## Overview

The Directorate General of Meteorology and Air Navigation (DGMET), part of Oman's Public Authority for Civil Aviation (PACA), operates meteorological observation stations at Oman's international airports. These stations produce standard METAR (Meteorological Aerodrome Reports) and TAF (Terminal Aerodrome Forecasts) messages following ICAO Annex 3 conventions.

Oman has four primary international airports with regular METAR publication:
- **OOMS** — Muscat International Airport (مطار مسقط الدولي)
- **OOSA** — Salalah Airport (مطار صلالة)
- **OOSN** — Sohar Airport
- **OOTH** — Thumrait Air Base

Oman is directly exposed to Arabian Sea tropical cyclones. Recent major impacts include Cyclone Shaheen (October 2021, first tropical cyclone to make landfall in Oman in recorded history), Cyclone Mekunu (May 2018, devastated Salalah with 230 mm rain in 24 hours), and Cyclone Hikaa (September 2019). Real-time airport METARs capture wind, pressure, visibility, and precipitation during cyclone approaches.

## Endpoint Analysis

**Verified working** — the new Aviation Weather Center API (launched 2024, replacing the legacy text-based ADDS system) provides JSON-formatted METAR observations for all global ICAO airports.

Sample request (tested 2026-05-23):
```
GET https://aviationweather.gov/api/data/metar?ids=OOMS,OOSA,OOSN,OOTH&format=json&taf=false&hours=6
```

Sample response (abbreviated):
```json
[
  {
    "receiptTime": "2026-05-23T07:04:33Z",
    "rawOb": "METAR OOMS 230650Z 03006KT 8000 NSC 40/14 Q1006 NOSIG",
    "icaoId": "OOMS",
    "reportTime": "2026-05-23T06:50:00Z",
    "temp": 40,
    "dewp": 14,
    "wdir": 30,
    "wspd": 6,
    "visib": "8000",
    "altim": 1006,
    ...
  },
  {
    "receiptTime": "2026-05-23T07:04:33Z",
    "rawOb": "METAR OOSA 230650Z 14007KT 110V170 9999 FEW025 32/25 Q1009 NOSIG",
    "icaoId": "OOSA",
    "reportTime": "2026-05-23T06:50:00Z",
    "temp": 32,
    "dewp": 25,
    "wdir": 140,
    "wspd": 7,
    ...
  }
]
```

Each observation includes:
- ICAO station identifier (stable key)
- Observation timestamp (ISO 8601)
- Temperature, dewpoint, wind direction/speed
- Visibility, pressure (QNH), sky condition
- Present weather phenomena (rain, dust, fog, etc.)
- Raw METAR string for full detail

## Integration Notes

- **Stable identifiers**: ICAO airport codes (4-letter: OOMS, OOSA, OOSN, OOTH) are globally standardized and permanent.
- **Update frequency**: METARs are issued hourly on the hour, with special reports (SPECI) issued when significant changes occur (e.g., wind gusts >25kt, visibility drops, thunderstorm onset). During cyclones, SPECI frequency increases.
- **Global vs. local source**: This uses the U.S. NOAA Aviation Weather API, which aggregates global ICAO METARs via WMO GTS (Global Telecommunication System). The data originates from Oman DGMET but is distributed globally through standard aeronautical channels.
- **Additive value vs. existing bridges**: The repo currently has no Middle East weather coverage. Oman METARs add:
  - Arabian Peninsula meteorology
  - Tropical cyclone landfall observations (Oman is one of the few GCC countries regularly hit by tropical cyclones)
  - Gulf of Oman and Arabian Sea maritime weather (Salalah is a major container port; Sohar is an industrial port)
  - Inland desert and mountain weather (OOTH at Thumrait captures interior desert conditions)
- **Alternative: Oman DGMET direct source**: The Oman met service (met.caa.gov.om) publishes Arabic-language weather bulletins on their homepage, but no machine-readable API was found. HTML parsing of their forecast text is possible but fragile. The Aviation Weather API is far more stable.
- **Cyclone warning integration**: Oman DGMET issues tropical cyclone warnings and advisories through the WMO Regional Specialized Meteorological Centre (RSMC) in New Delhi. These warnings are distributed via WMO alerting channels but do not appear to have a public API endpoint from Oman DGMET directly. GDACS (Global Disaster Alert and Coordination System) and RSMC New Delhi cover Arabian Sea cyclones in a machine-readable format, but those are global/regional aggregators, not Oman-specific.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Hourly (standard METAR), SPECI more frequent during significant weather |
| Openness | 3 | No auth required, no rate limits documented |
| Stability | 3 | Aviation Weather API is a U.S. government service with WMO data exchange backing |
| Structure | 2 | Typed JSON with schema documentation |
| Identifiers | 2 | ICAO codes are perfect keys, but only 4 stations in Oman |
| Additive value | 0 | NOAA AVN API is global — same data from same upstream as any other global METAR aggregator. Not Oman-specific. |

**Verdict**: ⏭️ Reference

This is a global METAR aggregator, not an Oman-specific feed. The Aviation Weather API provides the same data for Oman airports as it does for every other ICAO airport worldwide. While Oman METARs are valuable for cyclone tracking and maritime weather, they should be integrated via a **global METAR/TAF bridge** (covering all ICAO airports) rather than an Oman-specific source. The repo currently has no METAR bridge; if one is added, it should be global-scoped (similar to the existing NOAA NWS or USGS approach for U.S. data, but extended to all WMO-exchanged METARs via the Aviation Weather API).
