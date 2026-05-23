# Careem BIKE Dubai (GBFS)

- **Country/Region**: United Arab Emirates / Dubai
- **Endpoint**: `https://careem.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json`
- **Protocol**: GBFS 3.0 (General Bikeshare Feed Specification)
- **Auth**: None
- **Format**: JSON
- **Freshness**: Real-time (station status updated every few seconds, `last_reported` timestamp per station)
- **Docs**: https://www.careem.com/en-ae/careem-bike/, https://github.com/MobilityData/gbfs
- **Score**: 16/18

## Overview

Careem BIKE is Dubai's largest docked bikeshare system, operated by Careem (an Uber subsidiary). The system has 223 stations across Dubai with a mix of traditional bikes and e-bikes (EFIT model). Stations are concentrated in key areas including Dubai Marina, JBR, Dubai Mall, Downtown Dubai, City Walk, Al Khawaneej (Quranic Park), and residential communities.

The GBFS feed is a full implementation of GBFS 3.0, including station information, station status, system information, vehicle types, geofencing zones, system pricing plans, system alerts, and system hours.

## Endpoint Analysis

**Primary feed verified** — the discovery endpoint returns 8 feeds:

```
GET https://careem.publicbikesystem.net/customer/gbfs/v3.0/gbfs.json
```

Returns:
```json
{
  "version": "3.0",
  "data": {
    "feeds": [
      {"name": "system_information", "url": ".../system_information.json"},
      {"name": "station_information", "url": ".../station_information.json"},
      {"name": "station_status", "url": ".../station_status.json"},
      {"name": "vehicle_types", "url": ".../vehicle_types.json"},
      {"name": "geofencing_zones", "url": ".../geofencing_zones.json"},
      {"name": "system_pricing_plans", "url": ".../system_pricing_plans.json"},
      {"name": "system_alerts", "url": ".../system_alerts.json"},
      {"name": "system_hours", "url": ".../system_hours.json"}
    ]
  }
}
```

**Station information** (223 stations as of 2025-01-23):
- Each station has stable `station_id` (numeric, incremental)
- Geographic coordinates (lat/lon)
- Capacity (docks per station, typically 14-28)
- Multilingual names (English, Arabic, Dutch)
- Rental methods: key, transitcard, creditcard, phone
- Deep links for iOS/Android apps

**Station status** (real-time availability):
- `last_reported` timestamp (ISO 8601, updated every few seconds)
- `num_vehicles_available` — bikes currently available
- `num_docks_available` — open docks for return
- `vehicle_types_available` — breakdown by vehicle type (EFIT e-bikes, AUH Bike, ICONIC, BOOST)
- Operational flags: `is_installed`, `is_renting`, `is_returning`

**Sample station**:
```json
{
  "station_id": "2",
  "name": [{"text": "Quranic Park", "language": "en"}],
  "lat": 25.2362939,
  "lon": 55.4721851,
  "address": "KHAWANEEJ",
  "capacity": 28,
  "is_charging_station": true
}
```

**Sample status**:
```json
{
  "station_id": "2",
  "num_vehicles_available": 12,
  "num_docks_available": 15,
  "last_reported": "2025-01-23T07:44:24.935Z",
  "is_renting": true,
  "is_returning": true,
  "vehicle_types_available": [
    {"vehicle_type_id": "EFIT", "count": 12}
  ]
}
```

## Why This Is a Strong Candidate

1. **GBFS 3.0 compliance** — full spec implementation, all required and most optional feeds
2. **Real-time updates** — `last_reported` timestamps show sub-minute freshness
3. **No auth** — open data, no API key
4. **Stable IDs** — `station_id` is perfect for Kafka keys and CloudEvents subjects
5. **Rich metadata** — vehicle types, pricing plans, geofencing zones, alerts, hours
6. **Mature system** — 223 stations, operational since ~2020, well-maintained
7. **Standard protocol** — GBFS is a MOBILITY_DATA standard, same as GTFS-RT
8. **Multilingual** — Arabic, English, Dutch (reflects Dubai's demographics)

## Limitations

- **Geographic scope** — Dubai only (not Abu Dhabi, Sharjah, or other emirates)
- **Docked system** — only tracks station-based bikes; free-floating vehicles (if any) are not in GBFS
- **Vehicle types evolving** — the system lists 12 vehicle type IDs but most stations only have EFIT e-bikes available
- **Geofencing** — the geofencing zones feed may restrict operational areas; needs inspection

## Integration Notes

- **Key model**: Station-keyed (`station_id`)
- **Event families**: 
  - Reference: `station_information`, `vehicle_types`, `system_information`, `system_pricing_plans`, `geofencing_zones`
  - Telemetry: `station_status`, `system_alerts`
- **Polling cadence**: 30-60 seconds for status, hourly for reference data
- **CloudEvents subject**: `ae/dubai/bikeshare/careem/stations/{station_id}`
- **Repo sibling**: Existing `gtfs` bridge handles GTFS-RT; this would be a new GBFS bridge (protocol pattern)
- **Expansion opportunity**: Add Dott, Yaldi (other UAE GBFS operators) as multi-tenant

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Sub-minute `last_reported`, streaming-quality |
| Openness | 3 | No auth, public GBFS endpoint |
| Stability | 3 | GBFS 3.0 spec, versioned, stable operator (Careem/Uber) |
| Structure | 3 | GBFS JSON schema, formal spec |
| Identifiers | 3 | `station_id` stable, hierarchical subject possible |
| Additive value | 1 | GBFS protocol is new to repo, but bikeshare domain overlaps transit |

**Verdict**: **Build**. Careem BIKE Dubai is a textbook-quality GBFS feed with real-time updates, no auth, stable IDs, and rich metadata. This would establish the GBFS protocol pattern in the repo and can be extended to other UAE operators (Dott, Yaldi) and global GBFS systems. Dubai is a high-profile smart city; this data set is strategically valuable.
