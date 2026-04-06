# TomTom Traffic API

**Country/Region**: Global (200+ countries)
**Publisher**: TomTom International BV
**API Endpoint**: `https://api.tomtom.com/traffic/services/4/flowSegmentData/{style}/{zoom}/{format}?key={key}&point={lat},{lon}`
**Documentation**: https://developer.tomtom.com/traffic-api/documentation/traffic-flow/flow-segment-data
**Protocol**: REST
**Auth**: API key required (free tier: 2,500 requests/day)
**Data Format**: JSON, XML
**Update Frequency**: Real-time (~2 minutes)
**License**: Commercial (free tier available)

## What It Provides

TomTom's Traffic API provides global real-time traffic flow data and incident information. The Flow API returns current speeds, free-flow speeds, travel times, and road closure status for any road segment worldwide. The Incidents API returns accidents, construction, road closures, and other events. The free tier (2,500 transactions/day) is generous enough for monitoring key corridors.

## API Details

**Flow Segment Data:**
```
GET https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={key}&point=52.41072,4.84239
```

Returns:
```json
{
  "flowSegmentData": {
    "frc": "FRC3",
    "currentSpeed": 42,
    "freeFlowSpeed": 55,
    "currentTravelTime": 87,
    "freeFlowTravelTime": 67,
    "confidence": 0.95,
    "roadClosure": false,
    "coordinates": {
      "coordinate": [
        {"latitude": 52.411, "longitude": 4.842},
        {"latitude": 52.412, "longitude": 4.844}
      ]
    },
    "openlr": "CwOa9yUMoBNhAf2/4kMRGw=="
  }
}
```

Key fields:
- `currentSpeed` — Current speed (km/h)
- `freeFlowSpeed` — Expected speed without traffic
- `currentTravelTime` / `freeFlowTravelTime` — Seconds to traverse segment
- `confidence` — Data confidence (0-1)
- `frc` — Functional Road Class (FRC0 = motorway through FRC6 = local)
- `roadClosure` — Boolean closure status
- `openlr` — OpenLR location reference (standard road encoding)

**Incident Details (v5):**
```
GET https://api.tomtom.com/traffic/services/5/incidentDetails?key={key}&bbox=4.8,52.3,5.0,52.5
```

Returns GeoJSON FeatureCollection with incident type, geometry, delay magnitude, road numbers, start/end times, and TMC location codes.

**Incident categories:** Accident, Fog, DangerousConditions, Rain, Ice, Jam, LaneRestrictions, RoadClosed, RoadWorks, Wind, Flooding, Cluster.

**Free tier limits:**
- 2,500 free transactions/day
- Includes: Flow Segment Data, Incident Details, Traffic Flow Tiles, Incident Tiles
- No credit card required

## Freshness Assessment

Traffic flow data updates approximately every 2 minutes globally. TomTom processes data from 600+ million connected devices, GPS traces, and road sensors. Confidence scores indicate data quality per segment. The freshness is excellent for a global provider.

## Entity Model

- **Road Segment**: Segment with coordinates, FRC classification, OpenLR reference
- **Traffic Flow**: Current speed, free-flow speed, travel time, confidence
- **Incident**: Event with type, geometry, severity, delay, time window
- **Tile**: Map tile with pre-rendered flow/incident visualization

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | ~2 minute updates, real-time |
| Openness | 1 | Free tier available but commercial license, API key required |
| Stability | 3 | Major commercial provider, well-documented |
| Structure | 3 | Clean JSON/GeoJSON, OpenLR references, comprehensive schema |
| Identifiers | 3 | OpenLR codes, TMC references, road numbers |
| Additive Value | 3 | Global coverage, 200+ countries; benchmarking reference for traffic data |
| **Total** | **16/18** | |

## Notes

- TomTom's free tier (2,500 req/day) is practical for monitoring a set of key corridors or metropolitan areas, but insufficient for full-network continuous polling. Use strategically.
- The OpenLR location references are a standard encoding for road segments — the same format used by HERE and other traffic data providers. Supporting OpenLR enables cross-provider data fusion.
- TMC (Traffic Message Channel) codes in incident data enable correlation with European DATEX II traffic messages.
- TomTom is one of the two dominant global traffic data providers (alongside HERE). Including it — even as a commercial reference — gives context to the open data sources.
- The confidence field is valuable — it distinguishes between segments with rich sensor/probe data and those with interpolated estimates.
