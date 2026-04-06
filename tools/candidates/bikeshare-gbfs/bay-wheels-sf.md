# Bay Wheels San Francisco

**Country/Region**: United States — San Francisco Bay Area
**Publisher**: Lyft (operator)
**API Endpoint**: `https://gbfs.baywheels.com/gbfs/gbfs.json`
**Documentation**: https://www.lyft.com/bikes/bay-wheels/system-data
**Protocol**: GBFS 1.1
**Auth**: None
**Data Format**: JSON
**Update Frequency**: 60-second TTL
**License**: Lyft system data license

## What It Provides

Real-time station and dockless bike availability for the Bay Area's bikeshare system. Bay Wheels (formerly Ford GoBike) covers San Francisco, Oakland, Berkeley, San Jose, and surrounding areas with approximately 7,000 bikes including e-bikes. Operates as a hybrid system with both docked stations and dockless e-bikes.

## API Details

The auto-discovery URL redirects to Lyft's GBFS infrastructure:

- `gbfs.json` → `https://gbfs.lyft.com/gbfs/1.1/bay/gbfs.json`
- `station_information.json` — station metadata (name, lat, lon, capacity, region_id)
- `station_status.json` — real-time: bikes available, e-bikes, docks available
- `free_bike_status.json` — dockless e-bike positions and battery levels
- `system_information.json` — system_id: `lyft_bay`, timezone: America/Los_Angeles
- `system_regions.json` — SF, East Bay, San Jose regions

Same Lyft GBFS infrastructure as Citi Bike — identical schema, different system_id.

## Freshness Assessment

TTL is 60 seconds. Same Lyft infrastructure as Citi Bike, same freshness characteristics. Station status updates in near real-time; dockless bike positions update as vehicles report GPS fixes.

## Entity Model

- **Station**: Docking stations across Bay Area with UUID station IDs
- **Free bikes**: Dockless e-bikes with GPS positions and battery levels
- **Regions**: San Francisco, East Bay, San Jose
- **Vehicle types**: Standard bikes + e-bikes

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 60s TTL, near real-time |
| Openness | 3 | No auth required |
| Stability | 3 | Lyft GBFS infrastructure |
| Structure | 3 | Standard GBFS 1.1 |
| Identifiers | 3 | UUID station IDs |
| Additive Value | 1 | Covered by generic GBFS bridge; same Lyft infra as Citi Bike |
| **Total** | **16/18** | |

## Notes

- Included in the MobilityData GBFS catalog. Zero incremental effort if a generic GBFS bridge is built.
- Bay Wheels is interesting as a hybrid dock+dockless system — the `free_bike_status` feed is active and provides real-time GPS positions of dockless e-bikes, which is a richer data stream than dock-only systems.
- Same Lyft backend as Citi Bike, Capital Bikeshare, Divvy (Chicago), and others.
