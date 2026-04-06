# Melbourne On-Street Parking Sensors

**Country/Region**: Australia — Melbourne
**Publisher**: City of Melbourne
**API Endpoint**: `https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/on-street-parking-bay-sensors/records`
**Documentation**: https://data.melbourne.vic.gov.au/explore/dataset/on-street-parking-bay-sensors/
**Protocol**: REST (Opendatasoft API)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Real-time (per-event sensor updates)
**License**: CC BY 4.0

## What It Provides

Melbourne operates one of the world's largest on-street parking sensor networks — 3,309 in-ground sensors embedded in individual parking bays across the CBD and inner suburbs. Each sensor reports whether its bay is occupied or unoccupied, with timestamps. This is true bay-level granularity, not garage-level aggregates.

## API Details

```
GET https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/on-street-parking-bay-sensors/records?limit=100
```

Returns Opendatasoft records:
```json
{
  "status_description": "Unoccupied",
  "status_timestamp": "2025-04-14T03:01:40+00:00",
  "zone_number": 7218,
  "kerbsideid": 57940,
  "location": {"lon": 144.954, "lat": -37.820},
  "st_marker_id": "C5081",
  "bay_id": 5081
}
```

Key fields:
- `bay_id` / `st_marker_id` — Unique bay identifier
- `status_description` — "Present" (occupied) or "Unoccupied"
- `status_timestamp` — Last status change time
- `zone_number` — Parking zone
- `kerbsideid` — Kerbside identifier (links to restriction data)
- `location` — WGS84 coordinates

The Opendatasoft API supports:
- Pagination (`limit`, `offset`)
- Filtering (`where` parameter)
- Geo-distance queries (`within_distance(location, geom'POINT(lon lat)', dist)`)
- Export formats: JSON, CSV, GeoJSON

**Additional datasets** (23 parking-related datasets on the portal):
- Historical sensor data by year (2011–2019) — massive CSV archives
- Parking restriction data — links bay IDs to time limits, metered zones
- Off-street parking facilities

## Freshness Assessment

Sensors update on state change — each time a vehicle arrives or departs, the sensor fires an event. The `status_timestamp` field shows the moment of last change. For frequently used bays, updates happen every few minutes. For less-used bays, the timestamp may be hours old (reflecting a parked vehicle). The data is genuinely real-time at the individual bay level.

## Entity Model

- **Parking Bay**: Individual on-street parking space with sensor
- **Status**: Occupied/Unoccupied with timestamp
- **Zone**: Parking zone grouping
- **Kerbside**: Links to restriction/regulation data
- **Location**: WGS84 coordinates per bay

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time per-event sensor updates |
| Openness | 3 | No auth, CC BY 4.0, Opendatasoft API |
| Stability | 3 | City-operated, running since 2011 |
| Structure | 3 | Clean JSON, well-structured, rich metadata |
| Identifiers | 3 | Bay IDs, marker IDs, zone numbers, kerbside IDs |
| Additive Value | 3 | Unique: individual bay-level sensors (not garage aggregates); reuses Opendatasoft pattern |
| **Total** | **18/18** | |

## Notes

- Melbourne's parking sensors are a unique dataset — most parking data sources report garage-level occupancy. Melbourne provides individual bay-level status for 3,309 on-street bays. This is rare and valuable.
- The Opendatasoft platform is the same used by Ghent (parking garages). Building an Opendatasoft parking pattern covers both cities.
- The 3,309-record dataset fits in a single paginated query (a few calls with limit=1000). Update polling is efficient.
- Historical data back to 2011 enables occupancy pattern analysis, though the real-time API is the primary value.
- Kerbside IDs link to restriction data — a bridge could enrich bay status with time-limit and metered-zone information.
