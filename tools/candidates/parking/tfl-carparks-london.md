# TfL Car Parks (London)

**Country/Region**: UK — London
**Publisher**: Transport for London (TfL)
**API Endpoint**: `https://api.tfl.gov.uk/Place/Type/CarPark`
**Documentation**: https://api.tfl.gov.uk/ (Swagger: https://api.tfl.gov.uk/swagger/docs/v1)
**Protocol**: REST
**Auth**: None required (optional API key for higher rate limits)
**Data Format**: JSON
**Update Frequency**: Near real-time (occupancy via `/Occupancy/CarPark`)
**License**: TfL Open Data (free registration for key)

## What It Provides

TfL publishes data for car parks at London Underground and rail stations — primarily Park & Ride facilities. The Place API provides car park locations, metadata, capacities, and opening hours. The Occupancy API (when available) provides real-time space counts. This is part of the same TfL Unified API that serves Santander Cycles, bus arrivals, and Tube status.

## API Details

**Car park locations and metadata:**
```
GET https://api.tfl.gov.uk/Place/Type/CarPark
```

Returns JSON array of Place objects:
```json
{
  "id": "CarParks_800491",
  "commonName": "Barkingside Stn (LUL)",
  "placeType": "CarPark",
  "lat": 51.585,
  "lon": 0.088,
  "additionalProperties": [
    {"key": "NumberOfSpaces", "value": "46"},
    {"key": "OpeningHours", "value": "Mo-Su 24 Hr;"},
    {"key": "PostCode", "value": "IG6 1NB"},
    {"key": "SmartParkingLocationCode", "value": "BarkingsideLUL"}
  ]
}
```

**Occupancy data (real-time):**
```
GET https://api.tfl.gov.uk/Occupancy/CarPark/{id}
GET https://api.tfl.gov.uk/Occupancy/CarPark
```

Returns bay counts and occupancy levels. Note: This endpoint has been intermittently unavailable (HTTP 500 in testing) — it may require an API key or may have reliability issues.

## Freshness Assessment

Car park metadata (locations, capacity, hours) is relatively static. The Occupancy endpoint is intended to be real-time but showed reliability issues during testing. The SmartParking integration suggests sensor-based occupancy tracking at equipped stations.

## Entity Model

- **Car Park**: Location with name, postcode, coordinates, capacity
- **Properties**: Number of spaces, opening hours, SmartParking codes
- **Occupancy**: Bay type counts, occupancy levels (when available)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Metadata is static; occupancy is intermittently available |
| Openness | 3 | No auth required for basic access |
| Stability | 2 | Occupancy endpoint unreliable; Place API is solid |
| Structure | 3 | Clean JSON, well-documented Swagger |
| Identifiers | 3 | Unique car park IDs, postcodes, SmartParking codes |
| Additive Value | 2 | London coverage; same TfL API platform as Santander Cycles |
| **Total** | **15/18** | |

## Notes

- Part of the same TfL Unified API used for Santander Cycles — a single TfL bridge can serve both bikeshare and parking data.
- The `/Occupancy/CarPark` endpoint returned HTTP 500 during testing. This may improve with an API key, or may indicate a backend issue. Worth periodic rechecking.
- Car parks are primarily at Tube/rail stations — this is Park & Ride data, not general city parking.
- TfL's API rate limits are generous without a key, and even more so with a free registered key.
