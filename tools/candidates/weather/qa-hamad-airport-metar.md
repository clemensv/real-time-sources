# Qatar Hamad International Airport METAR

- **Country/Region**: Qatar
- **Endpoint**: `https://aviationweather.gov/api/data/metar?ids=OTHH&format=json&hours=2`
- **Protocol**: REST / JSON
- **Auth**: None
- **Format**: JSON
- **Freshness**: 30-minute updates (on the hour and half-hour)
- **Docs**: https://aviationweather.gov/data/api/
- **Score**: 14/18

## Overview

Hamad International Airport (OTHH) is Qatar's primary international airport and one of the busiest
in the Middle East. The FAA Aviation Weather Center provides free, public access to METAR
observations from OTHH via a documented JSON API. METARs are runway-level weather reports
issued every 30 minutes, containing temperature, wind, visibility, precipitation, cloud cover,
pressure, and weather phenomena.

The station (lat=25.273°N, lon=51.609°E, elevation=3m) sits on the coast of the Persian Gulf
and is representative of Doha's weather conditions. Qatar's climate is characterized by extreme
summer heat (40–50°C), high humidity, occasional dust storms (haboob), and minimal rainfall.

Additional Qatar METAR stations available via the same endpoint:
- **OTBD** (Doha International Airport, WMO=41170)
- **OTBH** (Al Udeid Air Base)

## Endpoint Analysis

**Live test successful** — API returned current METAR for OTHH:

```json
{
  "receiptTime": "2025-05-22T14:53:00Z",
  "obsTime": "2025-05-22T14:00:00Z",
  "reportTime": "2025-05-22T14:00:00Z",
  "temp": 36.6,
  "dewp": 22.0,
  "wdir": 330,
  "wspd": 24,
  "wgst": null,
  "visib": "9",
  "altim": 29.798,
  "slp": 1009,
  "qcField": 1,
  "wxString": "HZ",
  "presTend": null,
  "maxT": null,
  "minT": null,
  "precip": null,
  "name": "HAMAD INTL",
  "prior": 0,
  "lat": 25.273,
  "lon": 51.609,
  "elev": 3,
  "clouds": [
    {
      "cover": "FEW",
      "base": 3000
    }
  ],
  "icaoId": "OTHH",
  "wmo": null,
  "rawOb": "METAR OTHH 221400Z 33024KT 9000 HZ FEW030 37/22 Q1009 NOSIG",
  "most_recent": 1
}
```

The `rawOb` field provides the canonical METAR string. `wxString: "HZ"` = haze, common in Qatar
due to dust and humidity. Wind from 330° at 24 knots is typical NW shamal wind.

**Multi-station queries** work with comma-separated IDs:
```
GET /api/data/metar?ids=OTHH,OTBD,OTBH&format=json&hours=2
```

Returns array of observations.

## Integration Notes

- **Polling interval**: 30 minutes (update cadence matches METAR issuance)
- **CloudEvents subject**: `metar/{icaoId}` → `metar/OTHH`
- **Kafka key**: `icaoId` → `OTHH`
- **Entity model**: Airport weather station keyed by ICAO code
- **Alternative format**: `format=xml` for XML output
- **Time range**: `hours=N` parameter controls lookback (max 24 hours documented)
- **Overlap with existing bridges**: The repo does not currently have a METAR-specific bridge.
  NOAA NDBC covers buoy weather, USGS-IV covers river gauge weather, but airport METARs are
  a distinct entity class (runway-level observations, aviation-specific fields like altimeter
  setting, RVR, wind shear).
- **VATSIM mirror**: Alternative free endpoint at `https://metar.vatsim.net/OTHH` returns
  plain-text METAR (simpler but less structured).

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 30-minute updates |
| Openness | 3 | No auth, documented API, generous limits |
| Stability | 3 | FAA operational system, versioned API, status page |
| Structure | 2 | Typed JSON with schema (one level below Protobuf/formal spec) |
| Identifiers | 3 | ICAO codes are globally unique, perfect Kafka keys |
| Additive value | 1 | Global coverage exists but Qatar-specific METAR not in repo |

**Verdict**: Strong candidate for a generic **aviation-metar** bridge covering all global METAR
stations via aviationweather.gov. Qatar (OTHH, OTBD, OTBH) would be initial configuration.
The API also provides TAF (Terminal Area Forecast) at the same base URL.
