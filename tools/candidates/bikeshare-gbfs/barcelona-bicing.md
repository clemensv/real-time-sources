# Barcelona Bicing

**Country/Region**: Spain — Barcelona
**Publisher**: Ajuntament de Barcelona / PBSC Urban Solutions
**API Endpoint**: `https://barcelona.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
**Documentation**: https://opendata-ajuntament.barcelona.cat/
**Protocol**: GBFS 3.0 (also supports 1.1, 2.3)
**Auth**: None
**Data Format**: JSON (GBFS)
**Update Frequency**: Real-time
**License**: CC BY 4.0 (Barcelona Open Data)

## What It Provides

Bicing is Barcelona's municipal bikeshare system with 543 stations across the city, operated on the PBSC Urban Solutions platform. It includes both mechanical and electric bikes. The system publishes full GBFS 3.0 feeds — the latest version of the standard — making it a good reference implementation for GBFS 3.0 support.

## API Details

**GBFS 3.0 auto-discovery:**
```
GET https://barcelona.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json
```

**GBFS 2.3 auto-discovery:**
```
GET https://barcelona.publicbikesystem.net/customer/gbfs/v2.3/gbfs.json
```

Available feeds include:
- `station_information` — 543 stations with coordinates, capacity, charging capability
- `station_status` — Real-time availability (mechanical bikes, e-bikes, docks)
- `vehicle_types` — Bike classifications (standard, electric)
- `system_information` — System metadata
- `system_pricing_plans` — Subscription tiers
- `system_regions` — City zones
- `geofencing_zones` — Operating boundaries

The PBSC platform powers the same GBFS interface for Buenos Aires, Rio de Janeiro, Toronto, and other cities — building against this platform pattern covers multiple systems.

## Freshness Assessment

Real-time station status with per-minute updates. The PBSC platform is production-grade and reliable. E-bike charging status is tracked separately from mechanical bikes. GBFS 3.0 is the most current version of the spec.

## Entity Model

- **Station**: Dock-based station with location, capacity, charging capability
- **Vehicle Type**: Mechanical bike vs. e-bike
- **Availability**: Bikes by type, empty docks, station status
- **Region**: City zones/districts
- **Geofence**: Operating area boundaries

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, per-minute updates |
| Openness | 3 | No auth, publicly accessible |
| Stability | 3 | PBSC platform, well-maintained |
| Structure | 3 | GBFS 3.0 — latest standard |
| Identifiers | 3 | Station IDs, vehicle type IDs |
| Additive Value | 2 | Covered by GBFS catalog; value is as GBFS 3.0 reference + PBSC platform pattern |
| **Total** | **17/18** | |

## Notes

- Barcelona Bicing is in the MobilityData GBFS catalog as `bike_barcelona`. A generic GBFS bridge handles it.
- The PBSC platform is shared with Buenos Aires, Rio de Janeiro, Toronto, and other cities — same URL pattern, same feed structure. Building support for one means supporting all.
- The legacy BSM API (`api.bsmsa.eu`) returns 503 and appears deprecated. The PBSC endpoint is the canonical source.
- Barcelona Open Data BCN portal also lists the dataset, but now requires authentication tokens. The GBFS endpoint is the better path.
- GBFS 3.0 support makes this a useful test case for validating next-generation GBFS parsing.
