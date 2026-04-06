# HERE Traffic API

**Country/Region**: Global (200+ countries)
**Publisher**: HERE Technologies
**API Endpoint**: `https://data.traffic.hereapi.com/v7/flow?in=bbox:{bbox}&apiKey={key}`
**Documentation**: https://developer.here.com/documentation/traffic-api/dev_guide/index.html
**Protocol**: REST
**Auth**: API key or OAuth 2.0 bearer token (free tier: 1,000 requests/month)
**Data Format**: JSON, XML
**Update Frequency**: Real-time (~2 minutes)
**License**: Commercial (freemium tier available)

## What It Provides

HERE's Traffic API provides global real-time traffic flow data and incident information — a direct competitor to TomTom. The Flow API returns speeds, free-flow speeds, jam factors, and traversability for road segments. The Incidents API returns accidents, construction, closures, and hazards. The freemium tier is limited (1,000 requests/month) but useful for evaluation and reference.

## API Details

**Traffic Flow (v7):**
```
GET https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=bbox:13.3,52.5,13.4,52.6&apiKey={key}
```

Returns flow data per road segment:
```json
{
  "results": [
    {
      "location": {
        "shape": {"links": [{"points": [...]}]},
        "length": 450
      },
      "currentFlow": {
        "speed": 12.5,
        "freeFlow": 16.7,
        "jamFactor": 3.2,
        "confidence": 0.85,
        "traversability": "open"
      }
    }
  ]
}
```

Key fields:
- `speed` — Current speed (m/s)
- `freeFlow` — Free-flow speed (m/s)
- `jamFactor` — Congestion level (0 = free flow, 10 = standstill)
- `confidence` — Data quality (0-1)
- `traversability` — open, closed, reversibleNotRoutable

**Traffic Incidents (v7):**
```
GET https://data.traffic.hereapi.com/v7/incidents?in=bbox:13.3,52.5,13.4,52.6&apiKey={key}
```

Returns incidents with type, description, severity, geometry, road closures, and time windows.

**Location referencing options:**
- `shape` — Coordinate polylines
- `tmc` — TMC codes (European standard)
- `olr` — OpenLR (binary location reference)

**Freemium tier limits:**
- 1,000 transactions/month for traffic APIs
- Includes Flow and Incidents
- Requires HERE developer account (free)

## Freshness Assessment

Traffic data updates approximately every 2 minutes. HERE processes data from vehicle sensors, fleet telematics, and connected car platforms. The jam factor (0-10 scale) provides an intuitive congestion metric. Coverage is global but density varies by region.

## Entity Model

- **Road Segment**: Segment with shape geometry, length
- **Traffic Flow**: Speed, free-flow speed, jam factor, confidence, traversability
- **Incident**: Event with type, severity, geometry, time window
- **Location Reference**: Shape, TMC, or OpenLR encoding

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | ~2 minute updates, real-time |
| Openness | 1 | Freemium but commercial license, API key required, 1K/month is very limited |
| Stability | 3 | Major commercial provider, well-documented |
| Structure | 3 | Clean JSON, multiple location referencing options |
| Identifiers | 3 | TMC codes, OpenLR, shape references |
| Additive Value | 2 | Global coverage; lower free tier than TomTom (1K vs 2.5K/day) |
| **Total** | **15/18** | |

## Notes

- HERE's free tier (1,000 requests/month) is significantly more restrictive than TomTom's (2,500/day). HERE is better suited as a reference/evaluation source than for production polling.
- The `jamFactor` (0-10) is a useful pre-computed congestion metric — easier to work with than raw speed ratios.
- Multiple location referencing formats (shape, TMC, OpenLR) enable cross-system data fusion with DATEX II, TomTom, and other providers.
- HERE was formerly Nokia/Navteq and is now owned by a consortium of German automakers (BMW, Daimler, VW/Audi). Strong automotive industry ties mean good connected-car data.
- The documentation site uses heavy JavaScript rendering and may not be directly fetchable — use the developer console or static docs pages.
