# Citi Bike NYC

**Country/Region**: United States — New York City
**Publisher**: Lyft (operator), NYC DOT (sponsor)
**API Endpoint**: `https://gbfs.citibikenyc.com/gbfs/gbfs.json`
**Documentation**: https://citibikenyc.com/system-data
**Protocol**: GBFS 1.1
**Auth**: None
**Data Format**: JSON
**Update Frequency**: 60-second TTL
**License**: Citi Bike data license (free for non-commercial use; see system data page)

## What It Provides

Real-time station availability for the largest bikeshare system in the United States. Citi Bike operates ~2,000 stations across Manhattan, Brooklyn, Queens, the Bronx, Jersey City, and Hoboken with 27,000+ bikes (including e-bikes). The feed provides station-level counts of available bikes, e-bikes, empty docks, and station operational status.

## API Details

The auto-discovery URL redirects to Lyft's GBFS infrastructure:

- `gbfs.json` → `https://gbfs.lyft.com/gbfs/1.1/bkn/gbfs.json`
- `station_information.json` — station metadata (name, lat, lon, capacity, region_id)
- `station_status.json` — real-time: `num_bikes_available`, `num_ebikes_available`, `num_docks_available`, `is_renting`, `is_returning`, `last_reported`
- `free_bike_status.json` — dockless e-bikes in the wild
- `system_information.json` — system_id: `lyft_nyc`, operator: Lyft, timezone: America/New_York
- `system_alerts.json` — service disruptions and notices

Available in English, French, and Spanish.

Sample station_status entry:
```json
{
  "station_id": "5526b855-dc09-4159-a20a-99651861a481",
  "num_bikes_available": 12,
  "num_ebikes_available": 3,
  "num_docks_available": 15,
  "is_renting": 1,
  "is_returning": 1,
  "last_reported": 1700000000
}
```

## Freshness Assessment

TTL is 60 seconds. Station status data updates in near real-time as bikes are docked and undocked. The `last_reported` timestamp per station indicates when the station last communicated — most report within the last 1–2 minutes. Excellent freshness.

## Entity Model

- **Station**: ~2,000 docking stations with UUID-based station_id and legacy numeric IDs
- **Bike counts**: Standard bikes + e-bikes available, docks available, disabled counts
- **Regions**: NYC, Jersey City, Hoboken
- **Alerts**: System-wide service notifications

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 60s TTL, near real-time station updates |
| Openness | 3 | No auth required, publicly accessible |
| Stability | 3 | Lyft GBFS infrastructure is highly reliable |
| Structure | 3 | Standard GBFS 1.1 JSON schema |
| Identifiers | 3 | UUID station IDs, legacy IDs, system_id |
| Additive Value | 2 | Covered by GBFS catalog approach; value as standalone is incremental |
| **Total** | **17/18** | |

## Notes

- If we build a generic GBFS bridge from the MobilityData catalog, Citi Bike is automatically included. A standalone bridge adds no incremental value beyond being a useful test case.
- Lyft operates Citi Bike, Bay Wheels, Capital Bikeshare, and others — all share the same `gbfs.lyft.com` infrastructure with the same schema. A single implementation covers all Lyft-operated systems.
- The e-bike data (`num_ebikes_available`, `ebikes_at_stations`) is a Lyft extension not in the base GBFS 1.1 spec.
