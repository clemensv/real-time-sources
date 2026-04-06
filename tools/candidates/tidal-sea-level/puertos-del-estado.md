# Puertos del Estado — REDMAR Tide Gauge Network (Spain)

**Country/Region**: Spain (Mediterranean, Atlantic, Canary Islands, Balearics)
**Publisher**: Puertos del Estado (Spanish Ports Authority)
**API Endpoint**: `https://opendap.puertos.es/thredds/catalog.html` (THREDDS/OPeNDAP)
**Documentation**: https://www.puertos.es/oceanografia ; https://opendap.puertos.es/thredds/
**Protocol**: OPeNDAP / THREDDS Data Server (TDS)
**Auth**: None
**Data Format**: NetCDF (via OPeNDAP), CSV
**Update Frequency**: Real-time (operational tide gauges)
**License**: Open data (Spanish government open data policy)

## What It Provides

Puertos del Estado operates the REDMAR (Red de Mareógrafos) tide gauge network as part of its oceanographic monitoring infrastructure. This includes 40+ tide gauges at Spanish ports covering:

- Atlantic coast (A Coruña, Vigo, Huelva, Bonanza)
- Cantabrian coast (Bilbao, Santander, Gijón, Avilés)
- Mediterranean coast (Barcelona, Valencia, Tarragona, Almería, Málaga)
- Strait of Gibraltar (Algeciras, Tarifa)
- Balearic Islands (Mallorca, Ibiza, Mahón, Formentera, Alcudia)
- Canary Islands (Tenerife, Las Palmas, Fuerteventura, Arrecife, La Palma, La Gomera, El Hierro)
- Ceuta and Melilla

The system also includes deep-water buoys, HF radar current measurements, satellite SST, and atmospheric/wave model outputs.

## API Details

Data is served via a THREDDS Data Server with OPeNDAP access:

**Tide gauge data** (Mareógrafos > Nivel del Mar):
- Catalog: `https://opendap.puertos.es/thredds/catalog.html`
- Individual station catalogs: `https://opendap.puertos.es/thredds/catalog/tidegauge_{code}/catalog.html`
- Station codes: `alge` (Algeciras), `bar2` (Barcelona), `bil3` (Bilbao), `ten2` (Tenerife), `val3` (Valencia), etc.

OPeNDAP enables subsetting — clients can request specific time ranges and variables without downloading entire files. NetCDF files are organized by station.

Additional data categories available via the same THREDDS server:
- HF Radar currents (Delta del Ebro, Gibraltar, NW Iberian, Cádiz, Vigo, Canarias)
- Satellite SST
- Atmospheric models (HARMONIE at 2.5km and 1km resolution)
- Wave models (WANA, local port models)

## Freshness Assessment

Good. Operational tide gauges report in real-time. The THREDDS server provides access to recent data files. The exact latency of the OPeNDAP-served data depends on the processing pipeline, but it's designed for operational use.

## Entity Model

- **Station**: code (e.g., `bar2`), name, port, latitude, longitude
- **Observation**: timestamp, sea level (m), sensor metadata
- **NetCDF File**: station-specific files with time-series data

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time operational tide gauges |
| Openness | 3 | Open access, no authentication required |
| Stability | 3 | Government agency, operational port infrastructure |
| Structure | 2 | THREDDS/OPeNDAP is well-structured but requires specialized clients |
| Identifiers | 2 | Station codes (short slugs); cross-refs to IOC/GLOSS available |
| Additive Value | 3 | 40+ stations including Canary Islands and Strait of Gibraltar — unique coverage |
| **Total** | **16/18** | |

## Notes

- The Canary Islands and Strait of Gibraltar coverage is the standout value — these are strategically important locations not well-served by other feeds.
- THREDDS/OPeNDAP requires NetCDF-aware clients (`xarray`, `netCDF4`, etc.) but provides efficient subsetting.
- The same server hosts a rich array of oceanographic data beyond tide gauges (currents, SST, waves, atmosphere models) — potential for a broader integration.
- The PORTUS web application (portus.puertos.es) provides a user-friendly interface to the same data, but was returning 503 errors during testing.
- Many of these stations also report to the IOC SLSMF via GTS.
- The imar mobile app provides consumer-facing access to the same data.
