# MobilityData GBFS Catalog

**Country/Region**: Global
**Publisher**: MobilityData (formerly NABSA)
**API Endpoint**: `https://raw.githubusercontent.com/MobilityData/gbfs/master/systems.csv`
**Documentation**: https://github.com/MobilityData/gbfs
**Protocol**: GBFS (General Bikeshare Feed Specification)
**Auth**: None
**Data Format**: CSV catalog → individual JSON GBFS feeds
**Update Frequency**: Catalog updated via GitHub PRs; individual feeds update every 15–60 seconds
**License**: MobilityData catalog is open; individual feed licenses vary by operator

## What It Provides

The MobilityData GBFS catalog is the canonical directory of every known bikeshare, scooter-share, and micromobility system that publishes a GBFS feed. The `systems.csv` file lists hundreds of systems across 50+ countries with their auto-discovery URLs. Each auto-discovery URL points to a `gbfs.json` manifest that in turn links to `station_information`, `station_status`, `free_bike_status`, `vehicle_types`, and other standardized feeds.

This is not a single data source — it is the discovery mechanism for the entire GBFS ecosystem.

## API Details

The catalog itself is a simple CSV hosted on GitHub:

```
Country Code,Name,Location,System ID,URL,Auto-Discovery URL,Supported Versions,...
US,Citi Bike,NYC,citi_bike,...,https://gbfs.citibikenyc.com/gbfs/gbfs.json,1.1,...
FR,Vélib' Métropole,Paris,velib,...,https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/gbfs.json,...
```

Each Auto-Discovery URL returns a `gbfs.json` manifest with feed URLs. The standard feeds are:

- `station_information.json` — static station metadata (name, lat/lon, capacity)
- `station_status.json` — real-time availability (bikes available, docks available)
- `free_bike_status.json` — dockless vehicle positions and battery levels
- `vehicle_types.json` — vehicle type definitions (GBFS 2.1+)
- `system_information.json` — system name, operator, timezone

GBFS versions range from 1.0 to 3.0. Most systems support 2.x; newer ones support 3.0.

## Freshness Assessment

Individual GBFS feeds are designed for real-time consumption. The `ttl` field in each response indicates the recommended polling interval — typically 15–60 seconds for `station_status` and `free_bike_status`. The catalog CSV is updated asynchronously as new systems register. This is as fresh as bike-share data gets.

## Entity Model

- **System**: A bikeshare/scooter system in a city or region
- **Station**: A docking station with a fixed location, capacity, and real-time bike/dock counts
- **Vehicle**: A dockless vehicle with GPS position, battery level, and type
- **Vehicle Type**: Classification of vehicles (standard bike, e-bike, scooter)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | TTL 15–60s on station_status; true real-time |
| Openness | 3 | Catalog is public; most feeds are open (some require API keys) |
| Stability | 3 | GBFS is a mature, versioned standard maintained by MobilityData |
| Structure | 3 | Strictly specified JSON schema per feed type |
| Identifiers | 3 | Station IDs, system IDs, vehicle IDs are standardized |
| Additive Value | 3 | Single catalog unlocks hundreds of systems worldwide |
| **Total** | **18/18** | |

## Notes

- The highest-value approach is to build a single GBFS bridge that reads the catalog, discovers feeds, and polls station_status/free_bike_status across all systems. One bridge, hundreds of cities.
- GBFS 3.0 introduced breaking changes (renamed fields, new structures). A robust bridge should handle both 2.x and 3.0 schemas.
- Some operators (notably Lime, Tier) require API keys or OAuth tokens — the catalog includes `Authentication Info URL` and `Authentication Type` columns for these.
- The catalog currently lists 800+ systems in 50+ countries, from Dubai to Buenos Aires to Vienna.
