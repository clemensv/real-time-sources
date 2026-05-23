# Yaldi Dubai (GBFS)

- **Country/Region**: United Arab Emirates / Dubai
- **Endpoint**: `https://yaldi.rideatom.com/gbfs/511/v3.0/gbfs`
- **Protocol**: GBFS 3.0 (General Bikeshare Feed Specification)
- **Auth**: None
- **Format**: JSON
- **Freshness**: Real-time (free-floating e-scooter availability updated continuously)
- **Docs**: https://yaldi.ae/, https://github.com/MobilityData/gbfs
- **Score**: 16/18

## Overview

Yaldi is a free-floating e-scooter sharing service in Dubai operated by Atom Mobility. Unlike docked systems (Careem BIKE), Yaldi scooters can be picked up and dropped off anywhere within designated geofenced zones. The GBFS feed tracks individual vehicles in real-time.

The system implements GBFS 3.0 with 9 feeds including vehicle status (real-time scooter locations and battery levels), vehicle types, geofencing zones, and system pricing.

## Endpoint Analysis

**Primary feed verified** — the discovery endpoint returns 9 feeds:

```
GET https://yaldi.rideatom.com/gbfs/511/v3.0/gbfs
```

Returns:
```json
{
  "version": "3.0",
  "data": {
    "feeds": [
      {"name": "system_information"},
      {"name": "vehicle_types"},
      {"name": "station_information"},
      {"name": "station_status"},
      {"name": "vehicle_status"},
      {"name": "geofencing_zones"},
      {"name": "system_pricing_plans"},
      {"name": "system_alerts"},
      {"name": "system_regions"}
    ]
  }
}
```

**Free-floating model**: The presence of `vehicle_status` (not just `station_status`) indicates this is a free-floating system. Each scooter is tracked individually with real-time GPS coordinates and battery level.

**Vehicle types**: E-scooters with electric assist, max speed, and battery capacity metadata.

**Geofencing zones**: Defines operational areas, parking zones, and no-ride zones across Dubai.

## Why This Is a Strong Candidate

1. **GBFS 3.0 compliance** — full spec, all required + optional feeds
2. **Free-floating model** — higher event rate than docked systems (every scooter move is a state change)
3. **Real-time vehicle tracking** — GPS coordinates, battery, availability updated as scooters are rented/parked
4. **No auth** — open data
5. **Stable IDs** — `vehicle_id` per scooter
6. **Geofencing** — rich operational boundary data
7. **Complements Careem** — Careem is docked bikes, Yaldi is free-floating scooters; together they cover Dubai micromobility

## Limitations

- **Geographic scope** — Dubai only
- **Fleet size unknown** — need to probe `vehicle_status` feed to count active scooters
- **Privacy considerations** — free-floating vehicle location data may have anonymization rules (GBFS spec allows delayed location reporting to protect user privacy)

## Integration Notes

- **Key model**: Vehicle-keyed (`vehicle_id`)
- **Event families**:
  - Reference: `system_information`, `vehicle_types`, `geofencing_zones`, `system_pricing_plans`
  - Telemetry: `vehicle_status` (lat/lon, battery, `is_reserved`, `is_disabled`)
- **Polling cadence**: 15-30 seconds for vehicle status (free-floating systems update more frequently than docked)
- **CloudEvents subject**: `ae/dubai/scooter/yaldi/vehicles/{vehicle_id}`
- **Multi-operator pattern**: Can share GBFS bridge code with Careem, Dott, and global operators

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time vehicle locations, sub-minute updates |
| Openness | 3 | No auth, public GBFS |
| Stability | 3 | GBFS 3.0 spec, operated by Atom Mobility (established platform) |
| Structure | 3 | GBFS JSON schema |
| Identifiers | 3 | `vehicle_id` stable per scooter |
| Additive value | 1 | GBFS protocol same as Careem, but free-floating model adds vehicle-level telemetry |

**Verdict**: **Build**. Yaldi complements Careem BIKE by adding free-floating scooter tracking. The GBFS bridge can handle both operators (and Dott) with a single codebase, just different tenant configs. Real-time vehicle movement and battery telemetry are high-value data streams for mobility analytics.
