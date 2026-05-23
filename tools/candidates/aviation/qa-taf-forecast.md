# Qatar Terminal Area Forecast (TAF)

- **Country/Region**: Qatar
- **Endpoint**: `https://aviationweather.gov/api/data/taf?ids=OTHH,OTBD&format=json&time=valid`
- **Protocol**: REST / JSON
- **Auth**: None
- **Format**: JSON (also XML)
- **Freshness**: Issued every 6 hours (00, 06, 12, 18 UTC), valid for 24-30 hours
- **Docs**: https://aviationweather.gov/data/api/
- **Score**: 13/18

## Overview

**Terminal Area Forecasts (TAFs)** are runway-level weather forecasts issued by airport
meteorological offices every 6 hours. TAFs provide detailed predictions for the next 24-30
hours, including:
- Wind speed and direction (critical for runway selection)
- Visibility (meters)
- Cloud cover and ceiling (flight level)
- Weather phenomena (rain, dust, thunderstorms, fog)
- Significant changes (TEMPO = temporary, BECMG = becoming)

TAFs are **mandatory** for aviation operations at international airports. Pilots use TAFs for
flight planning, fuel calculations, and alternate airport selection.

For **Qatar**, TAFs are available for:
- **OTHH** (Hamad International Airport) — Qatar's primary international hub
- **OTBD** (Doha International Airport) — former primary airport, now cargo/military

TAFs complement METARs (current observations) by providing **forecasts**. While METARs tell
you what's happening now, TAFs tell you what's expected over the next day.

**Qatar TAF significance**:
- **Shamal wind forecasts**: TAFs predict onset of strong north/northwest winds (20-40 kt)
  that bring dust and affect runway operations
- **Dust event forecasts**: TAFs include TEMPO HZ (haze from dust) or TEMPO DS (dust storm)
  forecasts when dust is expected
- **Rare precipitation**: When rain is forecast (unusual for Qatar), TAFs include TEMPO RA
  or SHRA (showers)

## Endpoint Analysis

**Live test successful** — API returned current TAF for OTHH:

```json
{
  "taf": [
    {
      "rawTAF": "TAF OTHH 221100Z 2212/2318 33020KT 9999 FEW030 TEMPO 2212/2218 33025G35KT 5000 HZ BKN025 BECMG 2300/2303 31015KT",
      "icaoId": "OTHH",
      "issueTime": "2025-05-22T11:00:00Z",
      "validTimeFrom": "2025-05-22T12:00:00Z",
      "validTimeTo": "2025-05-23T18:00:00Z",
      "lat": 25.273,
      "lon": 51.609,
      "elev": 3,
      "forecast": [
        {
          "fcstTime": "2025-05-22T12:00:00Z",
          "wdir": 330,
          "wspd": 20,
          "wgst": null,
          "visib": "9999",
          "altim": null,
          "clouds": [
            {
              "cover": "FEW",
              "base": 3000
            }
          ],
          "changeType": null,
          "probability": null,
          "wxString": null
        },
        {
          "fcstTime": "2025-05-22T12:00:00Z",
          "fcstTimeTo": "2025-05-22T18:00:00Z",
          "wdir": 330,
          "wspd": 25,
          "wgst": 35,
          "visib": "5000",
          "clouds": [
            {
              "cover": "BKN",
              "base": 2500
            }
          ],
          "changeType": "TEMPO",
          "probability": null,
          "wxString": "HZ"
        },
        {
          "fcstTime": "2025-05-23T00:00:00Z",
          "fcstTimeTo": "2025-05-23T03:00:00Z",
          "wdir": 310,
          "wspd": 15,
          "wgst": null,
          "visib": null,
          "clouds": [],
          "changeType": "BECMG",
          "probability": null,
          "wxString": null
        }
      ]
    }
  ]
}
```

**Key TAF elements**:
- `rawTAF`: Original ICAO-formatted TAF text
- `issueTime`: When the TAF was issued (UTC)
- `validTimeFrom` / `validTimeTo`: Forecast validity period (typically 24-30 hours)
- `forecast[]`: Array of forecast periods
  - **Base forecast**: First entry, represents prevailing conditions
  - **TEMPO**: Temporary fluctuations (duration <1 hour at a time, occurring during the period)
  - **BECMG**: Permanent change occurring during the period
- `wdir`, `wspd`, `wgst`: Wind direction (°), speed (kt), gusts (kt)
- `visib`: Visibility (meters; "9999" = 10 km or more = unlimited visibility)
- `clouds[]`: Cloud layers with coverage (FEW, SCT, BKN, OVC) and base (feet AGL)
- `wxString`: Weather phenomena (HZ = haze, RA = rain, TS = thunderstorm, DS = dust storm, FG = fog, etc.)

**Interpretation of example TAF**:
- **Base forecast** (2212/2318): Wind 330° at 20 kt, visibility unlimited, few clouds at 3000 ft
- **TEMPO** (2212/2218, 12:00-18:00 UTC on May 22): Wind increases to 25 kt gusting 35 kt,
  visibility drops to 5000 m, **HZ (haze from dust)**, broken clouds at 2500 ft
  → **This is a dust event forecast** — shamal winds bringing dust, reducing visibility
- **BECMG** (2300/2303, 00:00-03:00 UTC on May 23): Wind shifts to 310° at 15 kt (weakening)

**Multi-station queries**:
```
GET /api/data/taf?ids=OTHH,OTBD&format=json&time=valid
```

Returns array of TAFs for both airports.

**Alternative format**: `format=xml` for XML output.

## Integration Notes

- **Polling interval**: 6 hours (TAFs issued at 00, 06, 12, 18 UTC; poll shortly after issuance)
- **CloudEvents subject**: `taf/{icaoId}` → `taf/OTHH`
- **Kafka key**: `icaoId` (OTHH, OTBD)
- **Entity model**: Airport weather forecast (time series of forecast periods)
- **Overlap check**: The repo does not currently have a TAF bridge. TAFs are **complementary**
  to METARs (observations). Both are aviation weather, but TAFs are forecasts.
- **Use case**: TAFs are critical for:
  - Flight planning and fuel calculations
  - Alternate airport selection (if weather deteriorates below minimums)
  - Crew briefing
  - Ground operations planning (ramp closures during high winds)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Issued every 6 hours (not as frequent as METARs, but acceptable for forecasts) |
| Openness | 3 | No auth, documented FAA API, free |
| Stability | 3 | FAA Aviation Weather Center operational system |
| Structure | 2 | Typed JSON with schema (one level below Protobuf) |
| Identifiers | 2 | ICAO codes are stable, but TAF issuance time must be part of key |
| Additive value | 1 | New data type (forecast vs observation) but same domain as METAR |

**Verdict**: **Optional candidate** to complement the METAR bridge. If a **generic aviation
weather bridge** is implemented, it should include both METARs (observations) and TAFs
(forecasts) from aviationweather.gov. Qatar (OTHH, OTBD) would be part of the initial
configuration.

**Qatar-specific TAF value**:
- **Dust storm forecasting**: TEMPO HZ or TEMPO DS in TAFs provide early warning (6-12 hours
  ahead) of dust events before they appear in METARs
- **Shamal wind prediction**: TAFs forecast wind speed increases associated with shamal events,
  which is valuable for:
  - Offshore platform operations (helicopter access restricted in high winds)
  - LNG tanker berthing at Ras Laffan (wind limits for safe berthing)
  - Outdoor events at FIFA-legacy stadiums
- **Rare rain events**: When rain is forecast (uncommon in Qatar), TAFs provide advance notice
  for flood preparedness

**Integration with other Qatar sources**:
- Combine TAF with:
  - METAR (cross-check forecast vs actual observation)
  - Open-Meteo weather forecast (TAF is airport-specific, Open-Meteo is city-wide)
  - Open-Meteo dust concentration (quantitative dust forecast vs TAF qualitative HZ)
  - DUST SIGMETs (TAF forecasts dust, SIGMET confirms severe dust event)

**TAF vs METAR comparison**:
| Aspect | METAR | TAF |
|--------|-------|-----|
| Type | Observation (actual) | Forecast (predicted) |
| Frequency | 30 minutes | 6 hours |
| Validity | Snapshot (current time) | 24-30 hours ahead |
| Use case | Real-time conditions | Flight planning |
| Phenomena | What's happening now | What's expected |

Both are essential for complete aviation weather coverage.
