# RDW Netherlands Parking Specifications

**Country/Region**: Netherlands
**Publisher**: RDW (Dienst Wegverkeer — Netherlands Vehicle Authority)
**API Endpoint**: `https://opendata.rdw.nl/resource/b3us-f26s.json` (specifications) and related datasets
**Documentation**: https://opendata.rdw.nl/
**Protocol**: REST (Socrata / SODA API)
**Auth**: None (app token recommended for higher rate limits)
**Data Format**: JSON / CSV / GeoJSON
**Update Frequency**: Periodically updated (not real-time)
**License**: Dutch government open data (CC0)

## What It Provides

The RDW publishes comprehensive parking data for the Netherlands through the Socrata open data platform. Multiple datasets cover parking area specifications (capacity, height restrictions, disabled access, charging points), usage rights, tariffs, and geographic boundaries. This is primarily static/administrative data rather than real-time occupancy, but it provides the reference dataset for Dutch parking infrastructure.

## API Details

**Parking specifications:**
```
GET https://opendata.rdw.nl/resource/b3us-f26s.json?$limit=100
```
Returns:
```json
{
  "areamanagerid": "153",
  "areaid": "010106",
  "capacity": "335",
  "chargingpointcapacity": "0",
  "disabledaccess": "0",
  "maximumvehicleheight": "200",
  "limitedaccess": "N"
}
```

Related datasets:
- `t49b-isb7` — Open data parking: recalls/status
- `b3us-f26s` — Parking specifications (capacity, access)
- `nsk3-v9n7` — Parking area geometry (GeoJSON)
- `figd-gux7` — Parking tariffs

The Socrata SODA API supports:
- `$where` — SQL-like filtering
- `$select` — field selection
- `$order` — sorting
- `$limit` / `$offset` — pagination
- `$q` — full-text search
- GeoJSON export via `$format=geojson`

## Freshness Assessment

This is primarily a reference/registry dataset — capacity, specifications, tariffs. Not real-time occupancy data. Updates happen periodically as parking areas change. For real-time Dutch parking data, NDW truck parking or city-specific APIs are needed. The value here is in the completeness of the static reference data.

## Entity Model

- **Area Manager**: Municipality or parking operator (by ID)
- **Parking Area**: Identified by area manager + area ID
- **Specifications**: Capacity, vehicle height limit, disabled access, EV charging points, access restrictions
- **Tariffs**: Pricing rules per area
- **Geometry**: Parking area boundaries

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Static reference data, not real-time |
| Openness | 3 | Open data, Socrata API, no auth required |
| Stability | 3 | Government-operated Socrata platform |
| Structure | 3 | Well-structured API with SQL-like queries |
| Identifiers | 3 | Standardized area manager + area IDs |
| Additive Value | 2 | Comprehensive reference data for Dutch parking |
| **Total** | **15/18** | |

## Notes

- This is a complementary dataset to NDW parking — RDW provides the static reference (where parking exists, how much capacity) while NDW provides real-time occupancy for truck parking.
- The Socrata SODA API is well-documented and widely used by data platforms worldwide. Familiar pattern for developers.
- EV charging point capacity per parking area is a useful cross-reference with NDL charging data.
- Lower priority as a standalone candidate due to lack of real-time data, but valuable as enrichment for other parking data sources.
