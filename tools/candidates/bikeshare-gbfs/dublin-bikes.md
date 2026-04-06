# Dublin Bikes (JCDecaux CycloCity)

**Country/Region**: Ireland — Dublin
**Publisher**: JCDecaux Ireland / Dublin City Council
**API Endpoint**: `https://api.cyclocity.fr/contracts/dublin/gbfs/gbfs.json`
**Documentation**: https://developer.jcdecaux.com/ (JCDecaux global developer portal)
**Protocol**: GBFS 2.3
**Auth**: None
**Data Format**: JSON (GBFS)
**Update Frequency**: Real-time
**License**: Open data

## What It Provides

Dublin Bikes is Dublin's municipal bikeshare with 117 stations, operated by JCDecaux through their CycloCity platform. The JCDecaux GBFS endpoint serves multiple European cities — Dublin, Nantes, Lyon, Toulouse, Seville, and others — through a single `api.cyclocity.fr` platform with city-specific paths.

## API Details

```
GET https://api.cyclocity.fr/contracts/dublin/gbfs/gbfs.json
```

Returns GBFS 2.3 manifest with feeds:
- `system_information` — System metadata
- `station_information` — 117 stations with coordinates
- `station_status` — Real-time availability
- `vehicle_types` — Bike type definitions
- `gbfs_versions` — Supported GBFS versions

**Other JCDecaux CycloCity cities (same platform pattern):**
```
https://api.cyclocity.fr/contracts/nantes/gbfs/gbfs.json
https://api.cyclocity.fr/contracts/lyon/gbfs/gbfs.json
https://api.cyclocity.fr/contracts/toulouse/gbfs/gbfs.json
https://api.cyclocity.fr/contracts/seville/gbfs/gbfs.json
```

## Freshness Assessment

Real-time station status. JCDecaux's platform is commercially operated and reliable. Station data updates as bikes are rented and returned. The feed language defaults to French (JCDecaux's home base) but station names are in the local language.

## Entity Model

- **Station**: Dock-based station with location, capacity
- **Vehicle Type**: Bike classification
- **Availability**: Bikes available, docks available per station

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time |
| Openness | 3 | No auth, publicly accessible |
| Stability | 3 | JCDecaux commercial infrastructure |
| Structure | 3 | GBFS 2.3, standard schema |
| Identifiers | 3 | Station IDs, vehicle type IDs |
| Additive Value | 2 | Covered by GBFS catalog; value is JCDecaux CycloCity platform pattern covering 6+ cities |
| **Total** | **17/18** | |

## Notes

- Dublin Bikes is in the MobilityData GBFS catalog. A generic GBFS bridge handles it.
- The key value is the JCDecaux CycloCity platform pattern — one `api.cyclocity.fr/contracts/{city}/gbfs/` URL template covers Dublin, Nantes, Lyon, Toulouse, Seville, and potentially more cities.
- JCDecaux also offers a separate developer API at `developer.jcdecaux.com` with an API key model — but the GBFS endpoint requires no key.
- With 117 stations, Dublin is small compared to other systems. The platform pattern is the real value here.
- JCDecaux is the world's largest outdoor advertising company and operates bikeshare as part of street furniture contracts — the business model is different from pure mobility operators.
