# Bahrain International Airport (OBBI) METAR - Aviation Weather API

- **Country/Region**: Bahrain (BH)
- **Endpoint**: `https://aviationweather.gov/api/data/metar?ids=OBBI&format=json`
- **Protocol**: REST / HTTP GET
- **Auth**: None
- **Format**: JSON, XML, CSV, GeoJSON, Raw text
- **Freshness**: Sub-hourly (typically every 30-60 minutes, aligned with METAR reporting schedule)
- **Docs**: https://aviationweather.gov/data/api/
- **Score**: 15/18

## Overview

Bahrain International Airport (ICAO: OBBI) is the primary aviation gateway for the
Kingdom of Bahrain and a major hub in the Gulf region. The airport publishes routine
METARs (Meteorological Aerodrome Reports) following ICAO standards, typically every
30-60 minutes or when significant weather changes occur.

The Aviation Weather Center (operated by NOAA/NWS) aggregates global METAR observations
from airports worldwide and provides them through a modern REST API with multiple output
formats. The service is fully open (no authentication), well-documented with OpenAPI
spec, and includes historical data access (up to 15 days).

Bahrain experiences unique meteorological phenomena including shamal winds (strong
northwesterly winds), rising sand/dust events (especially in summer), and high
temperatures. The airport METAR captures these conditions in real-time, making it
valuable for aviation, weather monitoring, and climatology research in the Gulf region.

## Endpoint Analysis

**Tested endpoint:**
```
GET https://aviationweather.gov/api/data/metar?ids=OBBI&format=json
```

**Sample response (2026-05-23 07:30 UTC):**
```json
{
  "icaoId": "OBBI",
  "receiptTime": "2026-05-23T07:32:50.324Z",
  "obsTime": 1779521400,
  "reportTime": "2026-05-23T07:30:00Z",
  "temp": 32,
  "dewp": 16,
  "wdir": 350,
  "wspd": 19,
  "visib": "6+",
  "altim": 1011,
  "metarType": "METAR",
  "rawOb": "METAR OBBI 230730Z 35019KT CAVOK 32/16 Q1011 NOSIG",
  "lat": 26.271,
  "lon": 50.634,
  "elev": 6,
  "name": "Bahrain Intl, MU, BH",
  "cover": "CAVOK",
  "clouds": [],
  "fltCat": "VFR"
}
```

The API returns structured JSON with parsed METAR fields (temperature, dewpoint, wind
direction/speed, visibility, pressure, cloud cover) alongside the raw METAR text.
Each observation includes geographic coordinates, elevation, and flight category (VFR/IFR).

**Alternative formats available:**
- `format=xml` - XML representation
- `format=csv` - CSV flat format
- `format=geojson` - GeoJSON with Point geometry
- `format=raw` - Raw METAR text only
- Omit format parameter for default raw text

**Cache file (global METARs, updated every minute):**
```
https://aviationweather.gov/data/cache/metars.cache.csv.gz
https://aviationweather.gov/data/cache/metars.cache.xml.gz
```

The cache files contain all current METARs worldwide (thousands of stations) in
compressed format. For a single-station bridge, querying by `ids=OBBI` is more
efficient than downloading and parsing the global cache.

## Integration Notes

- **Polling interval**: 5-10 minutes is appropriate. METARs are typically issued every
  30-60 minutes (or on significant weather change), but polling more frequently ensures
  prompt detection of special reports (SPECI).
- **Stable identifier**: ICAO airport code `OBBI` is globally stable and permanent.
  Use as Kafka key and CloudEvents subject.
- **Historical access**: The API supports `startTime` and `endTime` parameters to
  query up to 15 days of historical METARs. Useful for backfilling or replay scenarios.
- **TAF integration**: Terminal Area Forecasts (TAF) for OBBI are also available at
  `https://aviationweather.gov/api/data/taf?ids=OBBI&format=json`. Consider combining
  METAR observations and TAF forecasts into a unified aviation weather bridge.
- **Rate limiting**: The API documentation mentions rate limiting for frequent requests.
  A 5-minute polling interval with single-station queries should be well below limits.
  For batch queries, use the cache files instead.
- **Overlap with existing coverage**: This repo already has local Mode-S ADS-B receiver
  bridge but no global METAR bridge. This would be additive — a new domain (airport
  weather observations) for Bahrain, and extensible to other airports worldwide.
- **Data quality**: NOAA/NWS is authoritative for aviation weather. METAR data is
  quality-controlled and follows ICAO standards. The parsed JSON fields are reliable
  for numeric analysis; the raw METAR text preserves all metadata and special conditions.

**Regional expansion potential:**
The same endpoint pattern works for all Gulf airports: Kuwait (OKBK), UAE (OMDB Dubai,
OMAA Abu Dhabi), Qatar (OTHH), Oman (OOMS), Saudi Arabia (OERK Riyadh, OEJN Jeddah).
A Gulf aviation weather bridge could cover 10-20 major airports with a single polling
loop and unified contract.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Sub-hourly (30-60 min typical METAR cadence) |
| Openness | 3 | No auth, no API key, fully open |
| Stability | 3 | NOAA/NWS operational system, OpenAPI spec, versioned |
| Structure | 3 | JSON with typed fields, GeoJSON, XML, CSV all available |
| Identifiers | 3 | ICAO airport code (OBBI) is globally stable |
| Additive value | 1 | New domain (airport weather) but single station initially |

**Verdict**: **Strong candidate** — proceed to bootstrap as `obbi-metar` or generalize
to `aviationweather-metar` for multi-airport coverage. The API is production-ready,
well-documented, and requires no authentication. Polling pattern is straightforward.
Consider expanding to cover Gulf-wide aviation weather (Bahrain, UAE, Qatar, Kuwait,
Oman, Saudi Arabia) in a single bridge for higher additive value (score 15+).
