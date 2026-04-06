# nextbike

**Country/Region**: Pan-European (30+ countries, 300+ cities)
**Publisher**: nextbike GmbH (TIER Mobility subsidiary)
**API Endpoint**: `https://gbfs.nextbike.net/maps/gbfs/v2/{system_id}/gbfs.json`
**Documentation**: https://github.com/MobilityData/gbfs (listed in systems.csv)
**Protocol**: GBFS 2.3
**Auth**: None
**Data Format**: JSON
**Update Frequency**: 60-second TTL
**License**: Varies by city/system

## What It Provides

nextbike is one of the largest bikeshare operators in Europe, running systems in 300+ cities across 30+ countries. Each city system publishes its own GBFS 2.3 feed via `gbfs.nextbike.net`. Systems include major cities like Vienna (WienMobil Rad), Leipzig, Cologne, Glasgow, Warsaw, and many more.

## API Details

Each nextbike system has a unique system ID. Example for nextbike Germany:

```
GET https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_dg/gbfs.json
```

Returns GBFS 2.3 manifest:
- `station_information.json` — station metadata with coordinates
- `station_status.json` — real-time bike counts per station
- `free_bike_status.json` — dockless bikes (where applicable)
- `vehicle_types.json` — bike type definitions
- `system_pricing_plans.json` — pricing info
- `system_hours.json` — operating hours
- `system_regions.json` — regional breakdown

Available in German and English (varies by system).

Known system IDs from the GBFS catalog include:
- `nextbike_dg` — nextbike Germany
- `nextbike_wr` — WienMobil Rad (Vienna)
- `nextbike_al` — city bike Linz
- `nextbike_si` — Stadtrad Innsbruck
- `nextbike_ka` — Klagenfurt
- `nextbike_la` — Niederösterreich
- And dozens more across Europe

## Freshness Assessment

TTL is 60 seconds. Real-time station status updates as bikes are rented and returned. The GBFS 2.3 implementation is current and well-maintained. nextbike feeds are consistently available.

## Entity Model

- **System**: City-level bikeshare system with unique system_id
- **Station**: Docking station with location, capacity
- **Vehicle**: Individual bike with type (standard, e-bike, cargo)
- **Vehicle Type**: Bike classification per GBFS 2.3 spec
- **Region**: City areas or zones

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 60s TTL, real-time |
| Openness | 3 | No auth, publicly accessible |
| Stability | 3 | GBFS 2.3, well-maintained infrastructure |
| Structure | 3 | Standard GBFS schema |
| Identifiers | 3 | System IDs, station IDs, vehicle IDs |
| Additive Value | 2 | Many nextbike systems are in the GBFS catalog; value is in the breadth (300+ cities from one operator) |
| **Total** | **17/18** | |

## Notes

- nextbike systems are all listed in the MobilityData GBFS catalog with their individual auto-discovery URLs. A generic GBFS bridge would cover all nextbike cities.
- nextbike was acquired by TIER Mobility in 2022, which also operates e-scooter fleets — some TIER GBFS feeds may share infrastructure.
- The `vehicle_types` feed is particularly useful as nextbike operates different bike types (standard, e-bike, cargo) across different cities.
- nextbike uses GBFS 2.3 (the latest stable version before 3.0), which is well-structured and includes vehicle types.
