# SMHI — Sweden Sea Level Observations

**Country/Region**: Sweden (entire coastline, ~2,700 km)
**Publisher**: SMHI (Swedish Meteorological and Hydrological Institute)
**API Endpoint**: `https://opendata-download-ocobs.smhi.se/api/version/latest.json`
**Documentation**: https://opendata.smhi.se/apidocs/ocobs/
**Protocol**: REST API (JSON/XML/Atom)
**Auth**: None
**Data Format**: JSON, XML, Atom
**Update Frequency**: Real-time (hourly for standard; minute-values available)
**License**: CC BY 4.0

## What It Provides

SMHI's Open Data API for oceanographic observations provides real-time sea level and related marine measurements from Swedish coastal stations. The API follows a hierarchical structure: version → parameter → station → data period.

Sea level parameters (confirmed via API probe):
- **Parameter 6**: `Havsvattenstånd` — sea level (hourly, cm)
- **Parameter 12**: `Havsvattenstånd, RW timvärde` — sea level hourly reference values
- **Parameter 13**: `Havsvattenstånd, minutvärde` — sea level per-minute values
- **Parameter 14**: `Havsvattenstånd, RW minutvärde` — sea level minute reference values

Additional oceanographic parameters:
- **Parameter 5**: Sea temperature (°C)
- **Parameter 4**: Salinity (PSU)
- **Parameter 1**: Significant wave height (m)
- **Parameter 3**: Current speed

Geographic coverage spans lat 55.0–69.1°N, lon 11.2–26.1°E — the entire Swedish coast from Skagerrak to the Gulf of Bothnia.

## API Details

Clean hierarchical REST pattern:

```
# List all parameters
GET https://opendata-download-ocobs.smhi.se/api/version/latest.json

# List stations for sea level
GET https://opendata-download-ocobs.smhi.se/api/version/latest/parameter/6.json

# Station data (latest hour / 4 months / corrected archive)
GET https://opendata-download-ocobs.smhi.se/api/version/latest/parameter/6/station/{stationId}/period/latest-hour.json
GET https://opendata-download-ocobs.smhi.se/api/version/latest/parameter/6/station/{stationId}/period/latest-months.json
GET https://opendata-download-ocobs.smhi.se/api/version/latest/parameter/6/station/{stationId}/period/corrected-archive.json
```

Also available as XML and Atom feeds. Station metadata includes lat/lon, owner, active status, date range.

Verified: API responds with structured JSON listing all stations with coordinates and operational date ranges.

## Freshness Assessment

Excellent. Latest-hour data is effectively real-time. Minute-resolution values available (parameters 13, 14). Four months of recent data always available. Corrected historical archive goes back decades for some stations.

## Entity Model

- **Parameter**: key, title, unit, geographic bounding box
- **Station**: key (numeric ID), name, owner (SMHI or Sjöfartsverket), lat/lon, active flag, from/to dates
- **Observation**: timestamp (Unix epoch ms), value, quality code
- **Period**: latest-hour, latest-day, latest-months, corrected-archive

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time hourly + minute-resolution available |
| Openness | 3 | No auth, no registration, CC BY 4.0 |
| Stability | 3 | Swedish government institute, mature open data program |
| Structure | 3 | Clean REST/JSON hierarchy; multiple formats; well-organized |
| Identifiers | 2 | Numeric station IDs; no cross-references to IOC/PSMSL in API |
| Additive Value | 2 | Baltic Sea coverage; Gulf of Bothnia unique; complements Norwegian/Danish |
| **Total** | **16/18** | |

## Notes

- SMHI is arguably the gold standard for Nordic open data APIs. Clean, well-documented, no auth required.
- The same API pattern serves meteorological, hydrological, and oceanographic observations — learn one, use all three.
- Baltic Sea level dynamics differ fundamentally from tidal seas (wind-driven rather than tidal) — this dataset captures that unique regime.
- Minute-resolution data is unusual and valuable for storm surge analysis.
- Combined with Kartverket (Norway) and DMI (Denmark), these three APIs provide complete Scandinavian coastal coverage with zero authentication requirements (DMI needs a free key).
