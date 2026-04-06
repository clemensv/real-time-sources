# ECOBICI CDMX — Mexico City Bikeshare (GBFS)

**Country/Region**: Mexico (Mexico City / CDMX)
**Publisher**: Gobierno de la Ciudad de México / Lyft (operator)
**API Endpoint**: `https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json`
**Documentation**: https://ecobici.cdmx.gob.mx/en/informacion-del-servicio/open-data
**Protocol**: REST (GBFS 1.0)
**Auth**: None
**Data Format**: JSON (GBFS standard)
**Update Frequency**: ~10 seconds (TTL in response)
**License**: Open data

## What It Provides

ECOBICI is Mexico City's public bikeshare system — one of the largest in Latin America. The system publishes real-time availability data in the GBFS (General Bikeshare Feed Specification) standard, hosted by Lyft.

### Available GBFS Feeds

| Feed | URL | Description |
|------|-----|-------------|
| station_information | `.../station_information.json` | Static station metadata (location, capacity) |
| station_status | `.../station_status.json` | **Real-time** bike/dock availability per station |
| free_bike_status | `.../free_bike_status.json` | Free-floating bikes (if any) |
| system_information | `.../system_information.json` | System metadata |
| system_alerts | `.../system_alerts.json` | Active alerts |

Available in both English (`/en/`) and Spanish (`/es/`) language paths.

## API Details

### Discovery Endpoint
```
GET https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json
```

### System Information (verified)
```json
{
  "system_id": "MEX",
  "language": "en",
  "name": "Ecobici",
  "short_name": "Ecobici",
  "operator": "BKT",
  "url": "http://www.ecobici.cdmx.gob.mx",
  "timezone": "GMT-06:00"
}
```

### Station Status (verified live 2026-04-06)
```json
{
  "last_updated": 1775513375,
  "ttl": 10,
  "data": {
    "stations": [
      {
        "station_id": "1",
        "num_bikes_available": 17,
        "num_bikes_disabled": 2,
        "num_docks_available": 20,
        "num_docks_disabled": 0,
        "is_installed": 1,
        "is_renting": 1,
        "is_returning": 1,
        "last_reported": 1775513311
      }
    ]
  }
}
```

The `last_updated` and `last_reported` fields use Unix timestamps. TTL of 10 seconds indicates very frequent updates.

## Freshness Assessment

Exceptional freshness — TTL is 10 seconds, meaning the data is intended to be polled every 10 seconds. The `last_reported` timestamps confirmed stations reporting within seconds of the query. This is genuine real-time data.

## Integration Notes

- GBFS is an industry standard — the same adapter pattern used for Citi Bike NYC, Vélib' Paris, etc. applies here
- ECOBICI is one of the first bikeshare systems in Latin America (launched 2010)
- Mexico City's flat central area and bike infrastructure investments make this a growing system
- The Lyft hosting infrastructure is reliable (same platform as US bikeshare feeds)
- This is the first Latin American GBFS feed confirmed in the candidates
- Poll interval: respect TTL (10 seconds) for real-time, or 1-5 minutes for reduced load
- CloudEvents: one event per poll cycle with full station status snapshot, or delta events for station changes

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-second TTL; genuine real-time |
| Openness | 3 | No auth, GBFS standard, government open data directive |
| Stability | 3 | Lyft infrastructure; GBFS standard well-maintained |
| Structure | 3 | GBFS is a formal specification with strict schema |
| Identifiers | 3 | Stable station IDs, Unix timestamps |
| Additive Value | 2 | First Latin American GBFS; Mexico City is largest city in Western Hemisphere |
| **Total** | **17/18** | |

## Verdict

✅ **Build** — Trivial integration using existing GBFS adapter patterns. Same code that handles Citi Bike or Vélib' handles ECOBICI. Mexico City is the largest city in the Western Hemisphere by metro population — bikeshare data here is intrinsically valuable. Zero-cost addition to any GBFS aggregation.
