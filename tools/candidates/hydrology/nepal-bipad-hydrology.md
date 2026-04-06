# Nepal BIPAD Portal — Real-Time River Monitoring

**Country/Region**: Nepal
**Publisher**: Government of Nepal, National Disaster Risk Reduction and Management Authority (NDRRMA) via BIPAD Portal
**API Endpoint**: `https://bipadportal.gov.np/api/v1/river-stations/`
**Documentation**: https://bipadportal.gov.np/ (portal with map interface)
**Protocol**: REST (JSON)
**Auth**: None (anonymous access)
**Data Format**: JSON with GeoJSON geometry
**Update Frequency**: 15–30 minutes (aligned with telemetric station reporting)
**License**: Nepal government open data

## What It Provides

Nepal's BIPAD (Building Information Platform Against Disasters) portal provides real-time water level monitoring from river stations across Nepal's major river basins: Bagmati, Narayani, Koshi, Karnali, Mahakali, and Babai. This is operationally critical data — Nepal sits at the headwaters of rivers that flood Bangladesh and India, and glacial lake outburst floods (GLOFs) are a growing climate risk.

Each station record includes:
- **Water level** (meters, current reading)
- **Danger level** and **warning level** thresholds
- **Status**: BELOW WARNING LEVEL, WARNING, DANGER
- **Trend**: STEADY, RISING, FALLING
- **Basin**: River basin name
- **Geographic coordinates**: GeoJSON Point geometry
- **Elevation**: Station altitude where available
- **Last observation time**: Timestamp of most recent reading

The data source is Nepal's Department of Hydrology and Meteorology (DHM) via telemetric stations, aggregated through the BIPAD portal.

## API Details

Standard Django REST Framework pagination:

```
GET https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=100&offset=0
```

### Probed Response (live, April 7, 2026)

```json
{
  "count": 9223372036854775807,
  "next": "...?limit=5&offset=5",
  "results": [
    {
      "id": 121,
      "title": "Babai at Bhada Bridge",
      "basin": "Babai",
      "point": {
        "type": "Point",
        "coordinates": [81.356944, 28.1925]
      },
      "waterLevel": 2.56499958038,
      "dangerLevel": 8.0,
      "warningLevel": 7.0,
      "waterLevelOn": "2026-04-07T03:30:00+05:45",
      "status": "BELOW WARNING LEVEL",
      "elevation": null,
      "steady": "STEADY",
      "description": "Hydrological station with RLS",
      "stationSeriesId": 642,
      "dataSource": "hydrology.gov.np",
      "ward": 4841,
      "municipality": 58005,
      "district": 65,
      "province": 5
    },
    {
      "id": 249,
      "title": "Bauligad River",
      "basin": "Mahakali",
      "point": {
        "type": "Point",
        "coordinates": [81.1964, 29.557]
      },
      "waterLevel": 0.307199478149,
      "warningLevel": 2.6,
      "waterLevelOn": "2026-04-07T03:30:00+05:45",
      "status": "BELOW WARNING LEVEL",
      "elevation": 1311,
      "steady": "FALLING",
      "stationSeriesId": 29711,
      "dataSource": "hydrology.gov.np"
    }
  ]
}
```

Key observations:
- Data freshness confirmed: `waterLevelOn` timestamps are within 30 minutes of probe time
- GeoJSON Point geometry included for each station
- Clear danger/warning thresholds enable alerting logic
- The `count` returns max int (quirk of the API) — paginate to get all stations
- Station images available via `image` field (photos of the gauge stations)
- Administrative hierarchy: ward → municipality → district → province

## Freshness Assessment

Excellent. Water level readings update every 15–30 minutes from telemetric stations. The probe confirmed data timestamped within 30 minutes. During monsoon season (June–September), these readings become life-or-death data for flood early warning in downstream communities.

## Entity Model

- **Station**: Identified by `id` (integer) and `stationSeriesId`; linked to DHM hydrology.gov.np
- **Basin**: River basin name (Babai, Mahakali, Narayani, Bagmati, Koshi, etc.)
- **Water Level**: Current reading in meters with danger/warning thresholds
- **Status**: Categorical (BELOW WARNING LEVEL, WARNING, DANGER)
- **Administrative**: Province → district → municipality → ward hierarchy
- **Trend**: STEADY, RISING, FALLING — critical for flood prediction

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15–30 minute updates; confirmed live |
| Openness | 3 | No auth, no rate limits observed, anonymous REST |
| Stability | 2 | Government platform; Django REST API; operational since ~2020 |
| Structure | 3 | Clean JSON with GeoJSON geometry; well-defined fields |
| Identifiers | 2 | Numeric station IDs; linked to hydrology.gov.np series IDs |
| Additive Value | 3 | Unique: Nepal Himalayan rivers; GLOF monitoring; transboundary flood early warning |
| **Total** | **16/18** | |

## Integration Notes

- Poll every 15 minutes to match station reporting frequency
- Paginate through all stations (limit/offset pagination)
- The `count` field returns max long — don't trust it; paginate until empty results
- Dedup by `id` + `waterLevelOn` timestamp
- The `steady` field (RISING/FALLING/STEADY) is operationally critical — include in CloudEvents
- Administrative codes (ward, municipality, district, province) use Nepal's federal hierarchy
- Image URLs at `http://daq.hydrology.gov.np/images/` provide gauge station photos
- CloudEvents mapping: one event per station-reading; include status and trend as extensions
- Consider alerting when `status` changes to WARNING or DANGER

## Verdict

Outstanding find. Real-time Himalayan river monitoring with no authentication, clean JSON, and GeoJSON geometry. Nepal's rivers feed the Ganges and Brahmaputra — this data has transboundary significance for 600+ million people downstream. The warning/danger level thresholds built into the API make it ready for alerting use cases. The GLOF dimension adds unique value. Strong candidate for integration.
