# IMGW-PIB Open Data — Poland

**Country/Region**: Poland
**Publisher**: IMGW-PIB (Instytut Meteorologii i Gospodarki Wodnej — Państwowy Instytut Badawczy)
**API Endpoint**: `https://danepubliczne.imgw.pl/api/data/synop/` (synoptic), `https://danepubliczne.imgw.pl/api/data/meteo/` (meteorological)
**Documentation**: https://danepubliczne.imgw.pl/apiinfo
**Protocol**: REST (JSON)
**Auth**: None (fully open, no API key required)
**Data Format**: JSON
**Update Frequency**: Hourly (synoptic data), 10-minute (meteorological/hydro)
**License**: Public domain / Polish Open Government Data

## What It Provides

IMGW-PIB publishes real-time weather observations through a simple JSON API — no auth, clean structure, immediate access:

- **Synoptic Data** (`/api/data/synop/`): Current observations from Poland's synoptic station network:
  - Station name and WMO station number
  - Temperature (°C)
  - Wind speed (m/s) and direction (degrees)
  - Relative humidity (%)
  - Total precipitation (mm)
  - Atmospheric pressure (hPa)
  - Visibility indicator

- **Meteorological Station Data** (`/api/data/meteo/`): More frequent observations from the broader meteorological network.

- **Hydrological Data** (`/api/data/hydro/`): River water levels and flows — IMGW is also Poland's hydrological institute.

- **Warning Data**: Meteorological and hydrological warnings (may be available through a separate endpoint or the website).

## API Details

Dead simple JSON endpoints:
```
GET https://danepubliczne.imgw.pl/api/data/synop/
GET https://danepubliczne.imgw.pl/api/data/synop/station/{station_name}
GET https://danepubliczne.imgw.pl/api/data/meteo/
```

Response is a flat JSON array of station observations. Each object includes station ID, name, observation timestamp, and all measured parameters.

Station-specific queries by station name are supported.

No authentication, no pagination, no rate limits documented. The API returns all available stations in a single request.

## Freshness Assessment

- Synoptic data updates hourly (standard synoptic reporting schedule).
- Meteorological data may update more frequently (10-minute intervals from some stations).
- Hydrological data updates at regular intervals.
- Poland's station network covers the entire country with synoptic stations at ~50 km spacing.

## Entity Model

- **Station**: Station name (Polish) + WMO station number (where applicable).
- **Observation**: Multi-parameter reading per station with timestamp.
- **Parameter**: Polish-language field names (e.g., "temperatura", "predkosc_wiatru", "wilgotnosc_wzgledna").

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly synoptic updates, possibly 10-min for meteo stations |
| Openness | 3 | No auth, direct JSON access |
| Stability | 3 | Government institute, `danepubliczne.imgw.pl` is the official public data platform |
| Structure | 2 | Simple JSON but flat structure with Polish field names |
| Identifiers | 2 | Station names (Polish), WMO numbers for synoptic stations |
| Additive Value | 2 | Poland coverage, fills Central/Eastern European gap |
| **Total** | **14/18** | |

## Notes

- IMGW-PIB is both the meteorological AND hydrological institute — weather + hydrology from one API.
- The API design is minimalist but effective — a single GET returns all stations, no auth needed.
- Field names are in Polish (e.g., `temperatura`, `predkosc_wiatru`, `wilgotnosc_wzgledna`), which requires a mapping table but is straightforward.
- This fills the Central/Eastern European gap in coverage (between DWD/Germany, GeoSphere/Austria, and the Nordics).
- The `chmi-hydro` already in the repo covers Czech hydrology — IMGW covers both weather AND hydrology for Poland.
- Documentation is in Polish, but the API itself is self-documenting through its simple JSON structure.
- The `danepubliczne` (public data) subdomain signals official commitment to open data.
