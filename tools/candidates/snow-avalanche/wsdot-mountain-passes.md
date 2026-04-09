# WSDOT Mountain Pass Conditions

- **Country/Region**: US — Washington State
- **Publisher**: Washington State Department of Transportation (WSDOT)
- **Endpoint**: `https://data.wsdot.wa.gov/arcgis/rest/services/TravelInformation/TravelInfoMtPassReports/FeatureServer/0`
- **Protocol**: REST (ArcGIS FeatureServer + WSDOT Traveler API)
- **Auth**: API Access Code (free) for Traveler API; none for ArcGIS FeatureServer
- **Format**: JSON, GeoJSON
- **Freshness**: Real-time (updated multiple times daily during winter, as conditions change)
- **Docs**: https://www.wsdot.wa.gov/traffic/api/Documentation/class_mountain_pass_conditions.html
- **Score**: 15/18

## Overview

WSDOT monitors and reports conditions for 15 major mountain passes in Washington State, including Snoqualmie Pass (I-90), Stevens Pass (US-2), and White Pass (US-12). The data includes road conditions, weather, temperature, visibility, chain requirements, and closures. This is essential for a free-time advisor: mountain pass conditions directly determine access to ski areas, trailheads, and cross-Cascades recreation.

## API Details

**Two Access Methods:**

### 1. ArcGIS FeatureServer (No Auth)
**Base URL:** `https://data.wsdot.wa.gov/arcgis/rest/services/TravelInformation/TravelInfoMtPassReports/FeatureServer/0`

```
GET /query?where=1=1&outFields=*&f=json
```

**Key Fields:**
- `PassName` — e.g., "Snoqualmie Pass", "Stevens Pass"
- `Elevation` / `ElevationUnit`
- `Weather` — Current weather conditions text
- `RoadCondition` — Current road surface conditions
- `TemperatureInFahrenheit`
- `TravelAdvisory` — Active advisories (chain requirements, closures)
- `RestrictionOne`, `RestrictionTwo` — Specific restrictions
- `DateUpdated` — Timestamp of last update

### 2. WSDOT Traveler API (Requires Free Key)
**Base URL:** `https://www.wsdot.wa.gov/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/`

```
GET /GetMountainPassConditionsAsJson?AccessCode={key}
```

**Passes Covered:**
| Pass | Highway | Elevation | Key For |
|------|---------|-----------|---------|
| Snoqualmie | I-90 | 3,022 ft | Summit at Snoqualmie ski area |
| Stevens | US-2 | 4,061 ft | Stevens Pass ski area |
| White | US-12 | 4,500 ft | White Pass ski area |
| Chinook | SR-410 | 5,432 ft | Mt. Rainier NP access |
| Cayuse | SR-123 | 4,694 ft | Mt. Rainier NP access |
| North Cascades | SR-20 | 5,477 ft | North Cascades NP |
| Blewett | US-97 | 4,102 ft | Central WA access |
| Manastash | (various) | (various) | |

## Freshness Assessment

Very good. During winter weather events, pass conditions are updated every 15-30 minutes. During clear weather, updates are less frequent but still multiple times daily. The ArcGIS FeatureServer provides the latest snapshot on every query. A snowfall report tool also tracks daily/seasonal accumulation.

## Entity Model

- **Pass** — PassName, location (point geometry), elevation
- **Condition** — Weather, road condition, temperature, restrictions, advisory text
- **Restriction** — Chain requirements, closures, speed limits
- **Update** — DateUpdated timestamp

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Frequently updated during winter events |
| Openness | 3 | ArcGIS endpoint: no auth; Traveler API: free key |
| Stability | 3 | WSDOT official data service |
| Structure | 2 | ArcGIS JSON wrapper requires unwrapping; inner data is clean |
| Identifiers | 2 | Pass names are stable but no formal ID scheme in FeatureServer |
| Additive Value | 2 | Complements WSDOT traffic (already built); unique mountain access data |
| **Total** | **15/18** | |

## Notes

- The repo already has a `wsdot` bridge for traffic data. Mountain pass data uses the same Traveler API access code. Could be folded into the existing bridge or be a separate candidate.
- The ArcGIS FeatureServer endpoint requires no authentication at all, making it simpler for a bridge.
- Seasonal relevance: critical November–April for ski/snow recreation; less relevant in summer (though pass closures for rockslides/fires occur year-round).
- Could be combined with NWAC avalanche data for a comprehensive mountain conditions picture.
- Snowfall report data (`wsdot.com/travel/real-time/mountainpasses/snowfallreport`) provides historical accumulation but is not a clean API.
