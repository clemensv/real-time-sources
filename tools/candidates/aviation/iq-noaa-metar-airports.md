# NOAA Aviation Weather - Iraq Airport METARs

- **Country/Region**: Iraq
- **Endpoint**: `https://aviationweather.gov/api/data/metar`
- **Protocol**: HTTP REST API
- **Auth**: None
- **Format**: JSON, XML, raw text
- **Freshness**: Hourly (standard METAR frequency), some airports report every 30 minutes
- **Docs**: https://aviationweather.gov/data/api/
- **Score**: 14/18

## Overview

Aviation METARs (Meteorological Aerodrome Reports) are the only **accessible real-time weather data** for Iraq, since the Iraqi Meteorological Organization's public infrastructure is offline.

METARs provide standardized weather observations from major Iraqi airports:
- **ORBI** — Baghdad International Airport (capital, largest airport)
- **ORMM** — Basra International Airport (southern Iraq, oil region)
- **ORNI** — Al Najaf International Airport (central Iraq, Shia pilgrimage hub)
- **ORBB** — Erbil International Airport (Kurdistan Region capital) — *data gaps observed*
- **ORSU** — Sulaymaniyah International Airport (Kurdistan Region) — *data gaps observed*
- **ORNS** — Al Asad Airbase (US military, may not publish civilian METAR)

Iraq experiences severe dust storms that close airports, reduce visibility to zero, and cause respiratory health crises. METARs capture:
- Visibility (critical for dust detection — "CAVOK" means >10km, but dust events drop visibility to <1km)
- Present weather codes (DU = dust, DS = duststorm, SS = sandstorm)
- Wind (dust storms are often preceded by strong winds from the northwest)
- Temperature and dewpoint

These are the **only structured, real-time, machine-readable weather observations** available for Iraq.

## Endpoint Analysis

**NOAA Aviation Weather API verified** — new API launched in 2024/2025 replaces legacy text endpoint.

Sample request:
```
GET https://aviationweather.gov/api/data/metar?ids=ORBI,ORMM,ORNI&format=json
```

Response:
```json
[{
  "icaoId": "ORBI",
  "receiptTime": "2026-05-23T07:01:07.787Z",
  "obsTime": 1779519600,
  "reportTime": "2026-05-23T07:00:00Z",
  "temp": 32,
  "dewp": 9,
  "wdir": "VRB",
  "wspd": 4,
  "visib": "6+",
  "altim": 1014,
  "metarType": "METAR",
  "rawOb": "METAR ORBI 230700Z VRB04KT CAVOK 32/09 Q1014",
  "lat": 33.263,
  "lon": 44.235,
  "elev": 37,
  "name": "Baghdad Intl, BG, IQ",
  "cover": "CAVOK",
  "clouds": [],
  "fltCat": "VFR"
}]
```

Key fields:
- `icaoId` — stable identifier (ICAO airport code)
- `reportTime` — ISO 8601 observation timestamp
- `visib` — visibility in statute miles (or "6+" for >6mi, CAVOK for >10km)
- `rawOb` — full METAR text (includes present weather codes like DU/DS/SS for dust)
- `temp`, `dewp`, `wdir`, `wspd` — numeric weather parameters
- `lat`, `lon`, `elev` — station coordinates

## Integration Notes

- **Polling bridge**: Query every 10-15 minutes for the list of Iraq ICAOs.
- **Kafka key**: Use `icaoId` (ICAO code is the global standard station identifier).
- **Dust storm detection**: Parse `rawOb` for DU/DS/SS codes and visibility <5000m to flag dust events.
- **Coverage limitation**: Only airports, no inland weather stations. Baghdad, Basra, Najaf, Erbil, Sulaymaniyah covered. Many rural areas have no data.
- **Data gaps**: Erbil (ORBB) and Sulaymaniyah (ORSU) sometimes do not report (possible station outages or non-publication). Al Asad (ORNS) is a military airbase and may not publish.
- **Alternative ICAO sources**: If NOAA is incomplete, check ICAO global METAR aggregators or VATSIM/IVAO (flight simulation networks that mirror real METARs).
- **Already in repo?**: The repo has no existing METAR bridge. This would be a new aviation weather domain for Iraq (and globally extendable to any ICAO station).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly (some 30-min), standard aviation cadence |
| Openness | 3 | No auth, no rate limits, official NOAA API |
| Stability | 3 | ICAO standard, NOAA operational, versioned API |
| Structure | 3 | JSON with schema, METAR format documented |
| Identifiers | 3 | ICAO codes, globally unique, perfect keys |
| Richness | 0 | Limited spatial coverage (airports only), no inland dust monitoring |

**Verdict**: ✅ **Acceptable** — The **only accessible real-time weather data for Iraq**. Critical for dust storm monitoring (a major Iraq crisis). Limited to airports but Baghdad/Basra/Najaf/Erbil cover the major population centers. ICAO standard makes this globally extendable. Freshness is hourly (not sub-minute), but for weather observations this is standard. Ready for bootstrap if a METAR bridge pattern is added to the repo (would serve Iraq + globally).

**Note**: This is a **partial substitute** for the missing IMOS weather network. Iraq needs ground-based dust monitoring across the country, not just airports, but that data does not exist in accessible form.
