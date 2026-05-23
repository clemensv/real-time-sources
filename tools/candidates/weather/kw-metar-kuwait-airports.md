# Kuwait Airport METAR Data (Aviation Weather)

- **Country/Region**: Kuwait
- **Endpoint**: `https://aviationweather.gov/api/data/metar?ids=OKBK,OKAS,OKAJ&format=json`
- **Protocol**: REST / HTTP JSON
- **Auth**: None
- **Format**: JSON
- **Freshness**: Hourly (standard METAR cadence)
- **Docs**: https://aviationweather.gov/data/api/
- **Score**: 8/18

## Overview

Kuwait has three major airports with METAR (Meteorological Aerodrome Report) observations published through the US Aviation Weather Center's public API:

- **OKBK** — Kuwait International Airport (primary hub)
- **OKAS** — Ali Al Salem Air Base
- **OKAJ** — Ahmed Al Jaber Air Base

METAR observations include temperature, dewpoint, wind speed/direction, visibility, pressure (QNH), cloud coverage, and weather phenomena. Data updates hourly (or more frequently during significant weather changes) as part of the global WMO network.

This is a **universal fallback** for countries lacking dedicated meteorological APIs. Kuwait's Meteorological Department (www.met.gov.kw) publishes forecasts and current conditions on their website but does not expose a documented public API for real-time station data.

## Endpoint Analysis

**Endpoint verified** — Aviation Weather API v1 (NOAA/NWS service):

```
GET https://aviationweather.gov/api/data/metar?ids=OKBK&format=json
```

**Actual probe** (2025-05-23):
- HTTP 200 OK
- Content-Type: `application/json`
- Response time: ~500ms
- Sample observation count: 1 per airport

The response is a JSON array with one object per METAR observation. Each observation includes:
- `icaoId`: Airport ICAO code (e.g., "OKBK")
- `receiptTime`, `obsTime`: ISO 8601 timestamps
- `rawOb`: Raw METAR string
- `temp`, `dewp`: Temperature and dewpoint (°C)
- `wspd`, `wdir`: Wind speed (kt) and direction (°)
- `visib`: Visibility (statute miles)
- `altim`: Altimeter setting (inHg)
- `slp`: Sea-level pressure (hPa) when available
- `clouds`: Array of cloud layer objects
- `wxString`: Present weather phenomena (if any)
- `lat`, `lon`, `elev`: Station coordinates and elevation

## Schema / Sample Payload

```json
[
  {
    "icaoId": "OKBK",
    "receiptTime": "2025-05-23T07:27:00Z",
    "obsTime": "2025-05-23T07:00:00Z",
    "rawOb": "OKBK 230700Z 35016KT CAVOK 35/21 Q1014 NOSIG",
    "temp": 35.0,
    "dewp": 21.0,
    "wspd": 16,
    "wdir": 350,
    "visib": "10.0+",
    "altim": 29.94,
    "slp": 1014.0,
    "lat": 29.23,
    "lon": 47.97,
    "elev": 206,
    "clouds": [],
    "wxString": "CAVOK"
  }
]
```

## Why It's Weak

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Freshness | 1 | Hourly updates — slow for real-time use |
| Openness | 3 | No auth required, public NOAA API |
| Stability | 3 | Versioned API, WMO standard, reliable |
| Structure | 2 | JSON, but schema is lightly documented |
| Identifiers | 2 | ICAO codes are stable, but only 3 stations |
| Additive value | 0 | Already covered by `aviationweather` bridge in repo |

## Limitations

- **Hourly cadence only** — METAR observations update every hour (or on significant weather change via SPECI), which is too slow for minute-level real-time streaming.
- **Airport-only coverage** — Only 3 stations in Kuwait, all at airports. No inland or coastal weather stations outside aviation infrastructure.
- **Already bridged globally** — The `aviationweather` source in this repo already covers worldwide METAR/TAF data including Kuwait airports. Adding a Kuwait-specific METAR bridge would be redundant.
- **No Kuwait-specific value** — This is a universal WMO service. There's no Kuwait-specific endpoint or extension that isn't already available through the global bridge.

## Verdict

**Verdict**: ⏭️ **Reference** — Already covered by existing `aviationweather` global bridge. Documented here for completeness as Kuwait's only verified real-time weather API, but does not warrant a separate Kuwait-specific implementation. If the existing bridge doesn't already poll Kuwait airports, add `OKBK`, `OKAS`, `OKAJ` to its station list.
