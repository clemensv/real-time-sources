# Aviation Dust SIGMETs (Qatar FIR)

- **Country/Region**: Qatar / Persian Gulf region
- **Endpoint**: `https://aviationweather.gov/api/data/isigmet?format=json&hazard=DUST&bbox=20,45,32,58`
- **Protocol**: REST / JSON
- **Auth**: None
- **Format**: JSON (also XML, GeoJSON)
- **Freshness**: Real-time (updated within minutes of issuance by operational met offices)
- **Docs**: https://aviationweather.gov/data/api/
- **Score**: 15/18

## Overview

International SIGMETs (Significant Meteorological Information) are aviation weather warnings
issued by **Flight Information Region (FIR)** meteorological offices when hazardous conditions
exist or are forecast. For Qatar and the Persian Gulf, the most common SIGMET type is **DUST**
— severe dust storms (haboobs) that reduce visibility below aviation minimums.

**SIGMET types**:
- **DUST** / DS (dust storm, sand storm) — **most frequent for Qatar**
- **TS** (thunderstorm) — rare in Qatar (low precipitation climate)
- **TC** (tropical cyclone) — rare but Arabian Sea cyclones occasionally affect Qatar
- **VA** (volcanic ash) — extremely rare for this region
- **WS** (wind shear) — occasional with shamal winds
- **MT** (mountain obscuration) — not applicable to Qatar (flat terrain)
- **ICE**, **TURB** (icing, turbulence) — less common in hot climates

**Qatar FIR** (Flight Information Region) covers Qatar's airspace and is managed by Qatar
Civil Aviation Authority. SIGMETs are issued by Qatar Meteorological Department (qweather.gov.qa)
and disseminated internationally via FAA Aviation Weather Center.

**Dust storm context for Qatar**:
- **Shamal winds** (spring/summer) can lift massive dust plumes from Iraqi/Saudi deserts
- Visibility can drop from 10+ km to <500m in minutes
- Aviation impact: flight delays/diversions at Hamad International Airport (OTHH)
- Health impact: respiratory issues, outdoor activity restrictions
- Economic impact: disrupted logistics, LNG shipping delays

## Endpoint Analysis

**API confirmed working** — tested with bounding box covering Qatar and surrounding FIRs:

```
GET /api/data/isigmet?format=json&hazard=DUST&bbox=20,45,32,58
```

**Bounding box**: `minlat=20, minlon=45, maxlat=32, maxlon=58` covers:
- Qatar FIR
- UAE FIR
- Oman FIR
- Saudi Arabia (eastern FIRs)
- Bahrain FIR
- Kuwait FIR
- Southern Iraq FIR

**No active SIGMETs at test time**, but structure confirmed from docs:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[51.0, 24.0], [51.0, 26.0], [52.0, 26.0], [52.0, 24.0], [51.0, 24.0]]]
      },
      "properties": {
        "hazard": "DUST",
        "severity": "SEV",
        "issueTime": "2025-05-22T12:00:00Z",
        "validTimeFrom": "2025-05-22T12:00:00Z",
        "validTimeTo": "2025-05-22T18:00:00Z",
        "phenomenon": "DS",
        "base": null,
        "top": null,
        "speed": null,
        "direction": null,
        "intensity": "SEV",
        "rawSigmet": "OTHH SIGMET 1 VALID 221200/221800 OTHH- OTHH FIR SEV DS OBS AT 1200Z N OF LINE N2400 E05100 - N2400 E05200 MOV E 20KT INTSF=",
        "icaoId": "OTHH",
        "firId": "OTHH",
        "firName": "DOHA FIR"
      }
    }
  ]
}
```

**Key fields**:
- `hazard`: DUST, TS, TC, VA, WS, MT, ICE, TURB
- `severity`: SEV (severe), MOD (moderate), LGT (light)
- `validTimeFrom` / `validTimeTo`: SIGMET validity period (typically 4-6 hours)
- `geometry`: Polygon or line defining affected area
- `rawSigmet`: Original ICAO-formatted SIGMET text
- `icaoId`: Issuing FIR (OTHH = Doha/Qatar)
- `phenomenon`: DS (dust/sand storm), TS (thunderstorm), etc.

**Filtering**:
- By hazard: `hazard=DUST` (or TS, TC, VA, etc.)
- By bounding box: `bbox=minlat,minlon,maxlat,maxlon`
- By time: `date=YYYY-MM-DD` (defaults to current + next 24 hours)
- By FIR: No direct FIR filter, but bounding box effectively selects FIRs

**Alternative formats**:
- XML: `format=xml`
- GeoJSON: Implicit in JSON response (features array)

**Update frequency**: Real-time. SIGMETs are issued as soon as hazardous conditions are
detected or forecast by met offices. Polling every 5-10 minutes is appropriate.

## Integration Notes

- **Polling interval**: 5-10 minutes (SIGMETs are time-critical aviation safety warnings)
- **CloudEvents subject**: `sigmet/{icaoId}/{phenomenon}` → `sigmet/OTHH/DUST`
- **Kafka key**: `{icaoId}_{validTimeFrom}_{phenomenon}` → `OTHH_20250522T1200Z_DUST` (unique per SIGMET issuance)
- **Entity model**: Aviation weather warning (polygon + time + hazard type)
- **Overlap check**: The repo does not currently have a SIGMET bridge. This would be a **new domain** complementing METAR/TAF aviation weather.
- **Comparison with METAR**: METARs report **current conditions** at airports. SIGMETs report **forecast hazards** over broader regions (entire FIRs). Both are complementary.
- **Comparison with air quality data**: Open-Meteo dust concentration (μg/m³) is quantitative but modeled. SIGMETs are **operational warnings** issued by trained meteorologists based on observations + models. SIGMETs are what trigger actual flight delays/cancellations.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time (issued within minutes of hazard detection) |
| Openness | 3 | No auth, documented FAA API, free |
| Stability | 3 | FAA Aviation Weather Center operational system, ICAO standard |
| Structure | 2 | JSON/GeoJSON with schema (one level below Protobuf) |
| Identifiers | 2 | SIGMET ID is embedded in rawSigmet; combine icaoId + validTimeFrom for unique key |
| Additive value | 2 | New domain (aviation warnings); complements METAR/TAF |

**Verdict**: Recommended as an **aviation-sigmet** bridge covering all global SIGMETs via
aviationweather.gov. Qatar (bounding box 24-27°N, 50-52°E) would be the initial configuration
to capture OTHH FIR, but the bridge could extend to any FIR worldwide.

**Use cases**:
- Aviation safety alerts for Hamad International Airport (OTHH)
- Dust storm early warning for Qatar (cross-reference with METAR visibility and Open-Meteo dust concentration)
- Public health alerts (dust storms trigger respiratory advisories)
- Logistics planning (dust events delay cargo flights, affect supply chains)
- Climate/environmental monitoring (frequency and severity of dust SIGMETs over time)

**Qatar-specific value**:
- **Dust SIGMETs are the most operationally relevant SIGMET type for Qatar**. Thunderstorm
  SIGMETs are rare (Qatar gets <80mm rain/year). Tropical cyclone SIGMETs are very rare
  (Arabian Sea cyclones occasionally bring strong winds but rarely make landfall in Qatar).
  Dust is the persistent, frequent hazard.
- **Shamal dust events** occur multiple times per year, especially May-July. A SIGMET bridge
  would provide real-time alerts that are currently not publicly accessible outside aviation
  users.
- **FIFA 2022 legacy**: Major sporting events at Qatar's stadiums (e.g., Lusail Iconic Stadium)
  can be affected by dust storms. Real-time SIGMET data would enable event organizers to
  issue air quality warnings or postponements.

**Integration with other Qatar sources**:
- Combine DUST SIGMETs with:
  - Open-Meteo dust concentration (μg/m³) → quantitative + qualitative warning
  - METAR visibility (m) → airport-specific ground truth
  - Open-Meteo wind speed/direction (km/h, °) → identify shamal wind onset
  - AIS maritime data (if available) → dust affects visibility at sea, impacts LNG tanker navigation
