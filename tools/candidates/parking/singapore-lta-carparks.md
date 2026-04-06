# Singapore LTA Carpark Availability

**Country/Region**: Singapore
**Publisher**: Land Transport Authority (LTA)
**API Endpoint**: `http://datamall2.mytransport.sg/ltaodataservice/CarparkAvailability`
**Documentation**: https://datamall.lta.gov.sg/content/datamall/en/dynamic-data.html
**Protocol**: REST (OData-style)
**Auth**: API key required (free registration at datamall.lta.gov.sg)
**Data Format**: JSON
**Update Frequency**: Real-time (1 minute)
**License**: Singapore Open Data Licence

## What It Provides

LTA DataMall provides real-time carpark availability across Singapore, covering HDB (Housing & Development Board) car parks, shopping mall car parks, and URA (Urban Redevelopment Authority) car parks. This is part of a comprehensive transport data platform that also includes traffic speeds, incidents, bus arrivals, and taxi availability.

## API Details

```
GET http://datamall2.mytransport.sg/ltaodataservice/CarparkAvailability
Header: AccountKey: {your_api_key}
```

Returns JSON with carpark lots and availability:
```json
{
  "odata.metadata": "...",
  "value": [
    {
      "CarParkID": "1",
      "Area": "Marina",
      "Development": "Suntec City",
      "Location": "1.29375 103.85718",
      "AvailableLots": 400,
      "LotType": "C",
      "Agency": "URA"
    }
  ]
}
```

Key fields:
- `CarParkID` — Unique identifier
- `Area` — Geographic area
- `Development` — Name of building/complex
- `Location` — Lat/lng coordinates
- `AvailableLots` — Current free spaces
- `LotType` — C (Car), H (Heavy Vehicle), Y (Motorcycle)
- `Agency` — HDB, URA, or LTA

## Freshness Assessment

Updated every 1 minute. The data comes from Singapore's national parking guidance system. Singapore's highly digitized infrastructure means comprehensive sensor coverage across the island.

## Entity Model

- **Carpark**: Facility with ID, name, area, coordinates
- **Availability**: Available lots by vehicle type
- **Agency**: Operating authority (HDB/URA/LTA)
- **Vehicle Type**: Car, heavy vehicle, motorcycle

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 1-minute updates |
| Openness | 2 | Free but requires API key registration |
| Stability | 3 | Government-operated, well-maintained |
| Structure | 3 | Clean OData JSON |
| Identifiers | 3 | Unique carpark IDs, area classification |
| Additive Value | 3 | Comprehensive Singapore coverage; part of LTA DataMall platform with traffic data |
| **Total** | **17/18** | |

## Notes

- Singapore LTA DataMall is a comprehensive transport data platform. The carpark API is just one of 15+ real-time datasets. A single LTA registration unlocks traffic speeds, incidents, images, bus arrivals, taxi availability, and more.
- The OData-style API is straightforward to consume. Pagination uses `$skip` parameter.
- Singapore has excellent sensor coverage — nearly every public car park in the city-state is monitored.
- The `LotType` field distinguishes car, motorcycle, and heavy vehicle parking — useful for multi-modal transport applications.
- This is also documented under road-traffic as `singapore-lta-traffic.md` for the traffic-specific datasets.
