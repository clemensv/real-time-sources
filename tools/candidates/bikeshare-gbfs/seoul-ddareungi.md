# Seoul Ddareungi (따릉이 / Seoul Bike)

**Country/Region**: South Korea — Seoul
**Publisher**: Seoul Metropolitan Government
**API Endpoint**: `http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/{start}/{end}/`
**Documentation**: https://data.seoul.go.kr/ (Korean)
**Protocol**: REST (proprietary JSON — not GBFS)
**Auth**: API key required (free registration at data.seoul.go.kr)
**Data Format**: JSON
**Update Frequency**: Real-time
**License**: Seoul Open Data

## What It Provides

Ddareungi (따릉이, "Seoul Bike") is Seoul's public bikeshare system with 3,223 stations across the city. It is one of Asia's largest bikeshare networks. The system uses Seoul's Open Data API platform with a proprietary JSON format — not GBFS. The MobilityData catalog has zero South Korean entries.

## API Details

**Real-time bike availability:**
```
GET http://openapi.seoul.go.kr:8088/{API_KEY}/json/bikeList/{start}/{end}/
```

The API is paginated — `{start}` and `{end}` specify record ranges (e.g., `1/1000`, `1001/2000`). A demo key `sample` works for limited results.

**Station metadata:**
```
GET http://openapi.seoul.go.kr:8088/{API_KEY}/json/tbCycleStationInfo/{start}/{end}/
```

Returns station details including address, coordinates, and rack count.

Expected response structure:
```json
{
  "rentBikeStatus": {
    "list_total_count": 3223,
    "row": [
      {
        "rackTotCnt": "15",
        "stationName": "이대역 1번출구 앞",
        "parkingBikeTotCnt": "3",
        "shared": "20",
        "stationLatitude": "37.55712",
        "stationLongitude": "126.94569",
        "stationId": "ST-4"
      }
    ]
  }
}
```

Key fields:
- `stationId` — Unique station ID (e.g., "ST-4")
- `stationName` — Station name (Korean)
- `rackTotCnt` — Total rack/dock count
- `parkingBikeTotCnt` — Available bikes
- `shared` — Sharing percentage
- `stationLatitude`, `stationLongitude` — Coordinates

## Freshness Assessment

Real-time availability data. The paginated API requires multiple calls to get all 3,223 stations (e.g., three calls of 1,000 records each). Updates reflect current bike availability at each station.

## Entity Model

- **Station**: Dock-based station with ID, name, coordinates
- **Availability**: Available bikes, total racks, sharing percentage
- **Geography**: District-level grouping

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time availability |
| Openness | 2 | Free but requires API key registration |
| Stability | 3 | Government-operated, well-established since 2015 |
| Structure | 2 | Proprietary JSON, Korean-only station names, paginated |
| Identifiers | 3 | Unique station IDs, coordinates |
| Additive Value | 3 | Largest Korean bikeshare; zero Korean GBFS entries exist |
| **Total** | **16/18** | |

## Notes

- API key registration at data.seoul.go.kr requires a Korean-language sign-up process. The `sample` demo key works for testing with limited results.
- South Korea has zero entries in the MobilityData GBFS catalog — this is entirely proprietary.
- Pagination requires 3-4 API calls to retrieve all stations. A bridge should aggregate these.
- Station names are in Korean only. Consider enriching with English district names.
- Seoul also operates e-bike variants within the Ddareungi system.
