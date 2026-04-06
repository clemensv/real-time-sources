# Singapore LTA Traffic

**Country/Region**: Singapore
**Publisher**: Land Transport Authority (LTA)
**API Endpoint**: `http://datamall2.mytransport.sg/ltaodataservice/`
**Documentation**: https://datamall.lta.gov.sg/content/datamall/en/dynamic-data.html
**Protocol**: REST (OData-style)
**Auth**: API key required (free registration at datamall.lta.gov.sg)
**Data Format**: JSON
**Update Frequency**: Real-time (1–5 minutes depending on dataset)
**License**: Singapore Open Data Licence

## What It Provides

LTA DataMall is Singapore's comprehensive transport data platform providing real-time traffic speeds, incidents, travel times, traffic images, variable message signs, road works, and more. The platform covers the entire island-state's road network. Combined with the carpark availability API (documented separately), this is one of the most complete single-platform transport datasets available.

## API Details

All endpoints require the `AccountKey` header:
```
Header: AccountKey: {your_api_key}
```

**Traffic speed bands (real-time):**
```
GET http://datamall2.mytransport.sg/ltaodataservice/TrafficSpeedBandsv2
```

Returns speed bands for expressway and arterial road segments:
```json
{
  "value": [
    {
      "LinkID": "103014756",
      "RoadName": "AYER RAJAH EXPRESSWAY (AYE)",
      "RoadCategory": "A",
      "SpeedBand": 5,
      "MinimumSpeed": "41",
      "MaximumSpeed": "50",
      "Location": "1.27066 103.79454 1.26872 103.79283"
    }
  ]
}
```

**Traffic incidents (real-time):**
```
GET http://datamall2.mytransport.sg/ltaodataservice/TrafficIncidents
```

**Estimated travel times (real-time):**
```
GET http://datamall2.mytransport.sg/ltaodataservice/EstTravelTimes
```

**Traffic images (real-time):**
```
GET http://datamall2.mytransport.sg/ltaodataservice/TrafficImages
```

**Variable message signs:**
```
GET http://datamall2.mytransport.sg/ltaodataservice/VMS
```

**Additional real-time datasets:**
- `FaultyTrafficLights` — Currently faulty traffic signals
- `RoadWorks` — Approved road works
- `RoadOpenings` — Planned road openings
- `CarparkAvailability` — Carpark occupancy (see parking docs)
- `TaxiAvailability` — Real-time taxi locations

Key fields (speed bands):
- `LinkID` — Road segment identifier
- `RoadName` — Road name
- `RoadCategory` — A (Expressway), B (Major arterial), C (Arterial), etc.
- `SpeedBand` — 1 (≤20 km/h) through 8 (>70 km/h)
- `MinimumSpeed`, `MaximumSpeed` — Speed range for the band
- `Location` — Start and end coordinates of the segment

## Freshness Assessment

Speed bands update every 5 minutes. Incidents update in real-time. Traffic images refresh every 1-2 minutes. Travel times are computed in real-time. Singapore's compact geography (720 km² total) means comprehensive sensor coverage. The entire expressway and major arterial network is monitored.

## Entity Model

- **Road Segment**: Link with ID, road name, category, geometry
- **Speed Band**: Current speed classification (8 levels)
- **Incident**: Traffic event with type, location, description
- **Travel Time**: Segment or route-level travel time estimate
- **Traffic Image**: Camera snapshot with location
- **VMS Message**: Variable message sign content

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 1–5 minute updates, real-time |
| Openness | 2 | Free but requires API key registration |
| Stability | 3 | Government-operated, well-documented |
| Structure | 3 | Clean OData JSON, comprehensive documentation |
| Identifiers | 3 | Link IDs, road names, camera IDs |
| Additive Value | 3 | Comprehensive city-state coverage; 10+ real-time datasets from one platform |
| **Total** | **17/18** | |

## Notes

- LTA DataMall is a single-platform goldmine — one API key unlocks traffic, parking, transit, and taxi data. Building an LTA bridge should support multiple dataset types from day one.
- The OData-style pagination uses `$skip` for paging through large result sets.
- Speed bands are a pre-processed classification (1-8) rather than raw speeds — this simplifies congestion analysis at the cost of precision.
- Singapore's compact size means the dataset is comprehensive but not enormous — practical for full-network polling.
- The combination of speed bands, incidents, images, and VMS provides a complete traffic operational picture.
- Also documented under parking as `singapore-lta-carparks.md` for the carpark availability dataset.
