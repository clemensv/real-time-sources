# NOAA CO-OPS Tides and Currents — Puget Sound

- **Country/Region**: US — Puget Sound / Pacific Northwest
- **Publisher**: NOAA Center for Operational Oceanographic Products and Services (CO-OPS)
- **Endpoint**: `https://api.tidesandcurrents.noaa.gov/api/prod/datagetter`
- **Protocol**: REST
- **Auth**: None
- **Format**: JSON, XML, CSV
- **Freshness**: Real-time (6-minute intervals for observations, predictions available for any date range)
- **Docs**: https://api.tidesandcurrents.noaa.gov/api/prod/ and https://tidesandcurrents.noaa.gov/web_services_info.html
- **Score**: 17/18

## Overview

NOAA CO-OPS operates the authoritative tidal and oceanographic observation network in the US. For Puget Sound, this includes water level stations, current prediction stations, and water temperature sensors. While the existing `noaa` bridge in the repo may cover general NOAA data, this candidate focuses specifically on the **tidal currents** and **water temperature** products that are uniquely relevant for Puget Sound navigation, swimming, kayaking, and boating — key use cases for a free-time advisor.

## API Details

**Base URL:** `https://api.tidesandcurrents.noaa.gov/api/prod/datagetter`

**Metadata API:** `https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/`

### Key Products for Puget Sound

| Product | Parameter | Description |
|---------|-----------|-------------|
| `water_level` | `product=water_level` | Real-time observed water level |
| `predictions` | `product=predictions` | Tide predictions (high/low) |
| `water_temperature` | `product=water_temperature` | Water temperature |
| `currents` | `product=currents` | Observed currents (limited stations) |
| `currents_predictions` | `product=currents_predictions` | Predicted tidal currents |
| `air_temperature` | `product=air_temperature` | Air temperature at station |
| `wind` | `product=wind` | Wind speed/direction |

### Puget Sound Stations

| Station ID | Name | Products |
|------------|------|----------|
| 9447130 | Seattle | Water level, predictions, air temp, wind |
| 9446484 | Tacoma | Water level, predictions |
| 9444900 | Port Townsend | Water level, predictions, water temp |
| 9447110 | Shilshole Bay | Water level |
| 9449880 | Friday Harbor | Water level, water temp |

### Puget Sound Current Stations

| Station | Name | Type |
|---------|------|------|
| PUG1515 | Admiralty Inlet | Current predictions |
| cb0101 | Bush Point | Current predictions |
| cb0601 | Rich Passage | Current predictions |
| PUG1621 | Tacoma Narrows | Current predictions |

### Example Queries

**Water Level at Seattle (latest):**
```
GET ?date=latest&station=9447130&product=water_level&datum=MLLW&units=metric&time_zone=gmt&format=json
```

**Verified Response:**
```json
{
  "metadata": {"id": "9447130", "name": "Seattle", "lat": "47.6026", "lon": "-122.3393"},
  "data": [{"t": "2026-04-08 18:48", "v": "1.874", "s": "0.019", "f": "1,0,0,0", "q": "p"}]
}
```

**Current Predictions at Admiralty Inlet:**
```
GET ?product=currents_predictions&begin_date=20260408&end_date=20260409&station=PUG1515&units=english&time_zone=gmt&format=json&interval=MAX_SLACK
```

**Verified Response:**
```json
{
  "current_predictions": {
    "units": "feet, knots",
    "cp": [
      {"Type": "flood", "meanFloodDir": 234, "Bin": "15", "meanEbbDir": 341, "Time": "2026-04-08 01:00", "Depth": "16", "Velocity_Major": 1.12},
      {"Type": "slack", "Time": "2026-04-08 04:34", "Velocity_Major": 0}
    ]
  }
}
```

**Station Discovery:**
```
GET https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json?state=WA
```

## Freshness Assessment

Excellent. Water level observations update every 6 minutes. Predictions are pre-computed and available for any future date. Current predictions are likewise pre-computed. Water temperature updates vary by station (6 minutes to hourly). This is a very reliable, well-maintained federal data service.

## Entity Model

- **Station** — Station ID, name, location, available products
- **Observation** — Timestamp, value, quality flags
- **Prediction** — Timestamp, predicted value (tides, currents)
- **Current** — Type (flood/ebb/slack), velocity, direction, depth
- **Datum** — Reference datum (MLLW, MHHW, MSL, etc.)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | 6-minute observations, predictions always available |
| Openness | 3 | No auth, US federal public domain |
| Stability | 3 | NOAA — operational since decades, extremely reliable |
| Structure | 3 | Clean REST JSON, well-documented parameters |
| Identifiers | 3 | Station IDs (numeric), product codes, datum codes — all stable |
| Additive Value | 2 | Extends existing NOAA bridges with tidal currents focus |
| **Total** | **17/18** | |

## Notes

- The repo has `noaa` and `noaa-ndbc` bridges. This candidate focuses on the CO-OPS currents and water temperature products specifically for Puget Sound, which are distinct from weather and buoy data.
- Tidal currents are critical for kayakers, sailors, and boaters in Puget Sound — ebb/flood cycles through Deception Pass, Tacoma Narrows, and Admiralty Inlet create dangerous conditions.
- Water temperature is relevant for swimming advisories (Lake Washington stays cold until July; Puget Sound rarely exceeds 55°F).
- The metadata API enables automated station discovery, making it possible to build a comprehensive Puget Sound station inventory.
- Python wrapper `noaa_coops` simplifies integration for prototyping.
