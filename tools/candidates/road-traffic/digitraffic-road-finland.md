# Digitraffic Road (Finland)

**Country/Region**: Finland
**Publisher**: Fintraffic (formerly Finnish Transport Agency)
**API Endpoint**: `https://tie.digitraffic.fi/api/`
**Documentation**: https://www.digitraffic.fi/en/road-traffic/
**Protocol**: REST + MQTT (WebSocket)
**Auth**: None
**Data Format**: JSON (GeoJSON) / DATEX II
**Update Frequency**: Real-time (seconds for sensor data; minutes for messages)
**License**: Creative Commons 4.0 BY

## What It Provides

Digitraffic Road is the Finnish national road traffic data platform operated by Fintraffic. It provides comprehensive real-time traffic data including traffic measurement stations (TMS) with vehicle counts and speeds, traffic messages (roadworks, incidents, weight restrictions), road weather stations, road weather cameras, and variable message signs. The same platform that runs Digitraffic Maritime — already known to the project.

## API Details

**Traffic Measurement Stations (TMS):**
```
GET https://tie.digitraffic.fi/api/tms/v1/stations
```
Returns GeoJSON FeatureCollection with all TMS stations (500+ across Finland):
```json
{
  "type": "Feature",
  "id": 20002,
  "geometry": {"type": "Point", "coordinates": [24.637997, 60.220898]},
  "properties": {
    "id": 20002,
    "tmsNumber": 20002,
    "name": "vt1_Espoo_Hirvisuo",
    "collectionStatus": "GATHERING",
    "state": "OK"
  }
}
```

**TMS sensor data:**
```
GET https://tie.digitraffic.fi/api/tms/v1/stations/{id}/data
```

**Traffic messages (DATEX II):**
```
GET https://tie.digitraffic.fi/api/traffic-message/v1/messages?situationType=TRAFFIC_ANNOUNCEMENT
```
Returns GeoJSON with DATEX II-structured traffic announcements including:
- `situationId` — unique situation identifier (e.g., `GUID50459844`)
- `situationType` — TRAFFIC_ANNOUNCEMENT, ROAD_WORK, WEIGHT_RESTRICTION
- `announcements[]` — title, location, features (road closed, detour), time/duration
- Detailed road addressing (road number, section, distance)

**Road weather:**
```
GET https://tie.digitraffic.fi/api/weather/v1/stations
GET https://tie.digitraffic.fi/api/weather/v1/stations/{id}/data
```

**MQTT for real-time streaming:**
```
wss://tie.digitraffic.fi/mqtt
Topics: tms/+/+, weather/+/+, etc.
```

## Freshness Assessment

TMS sensor data updates every 5 minutes (vehicle counts aggregated over measurement periods). Traffic messages update in real-time as situations change — the `versionTime` timestamp shows updates within hours or days depending on the situation. MQTT provides sub-second push updates for sensor data. Road weather updates every 1–10 minutes. Excellent freshness across all data types.

## Entity Model

- **TMS Station**: Traffic measurement point with ID, name, road, coordinates
- **Sensor Data**: Vehicle counts, speeds, by vehicle class, per direction
- **Traffic Message**: Situation with type, location, announcements, lifecycle (version tracking)
- **Road Weather Station**: Weather measurement point with conditions
- **Weather Data**: Temperature, humidity, wind, precipitation, road surface conditions

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time via MQTT; 5-min via REST for TMS data |
| Openness | 3 | No auth, CC BY 4.0 |
| Stability | 3 | Government-operated, well-documented, versioned APIs |
| Structure | 3 | GeoJSON + DATEX II; consistent, well-defined schemas |
| Identifiers | 3 | TMS station IDs, situation GUIDs, road addresses |
| Additive Value | 3 | Comprehensive Finnish road data; same platform pattern as Digitraffic Maritime |
| **Total** | **18/18** | |

## Notes

- Digitraffic Road uses the same platform architecture as Digitraffic Maritime (already in the project). Code patterns, MQTT handling, and API conventions can be reused.
- The MQTT support is a standout feature — true push-based real-time data without polling. Few traffic data platforms offer this.
- Traffic messages use DATEX II structure, which aligns with European standards (also used by NDW Netherlands, Highways England, Trafikverket Sweden).
- Finland's road network is well-instrumented with 500+ TMS stations and 300+ weather stations.
- Data includes road addressing (road number, section, distance) which enables precise location mapping.
