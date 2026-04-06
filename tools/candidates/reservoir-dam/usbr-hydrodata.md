# US Bureau of Reclamation — HydroData

**Country/Region**: United States (Western states — Upper/Lower Colorado, Columbia, Missouri, Klamath basins)
**Publisher**: US Bureau of Reclamation (USBR), Department of the Interior
**API Endpoint**: `https://www.usbr.gov/uc/water/hydrodata/` (data navigator with JSON/CSV endpoints)
**Documentation**: https://www.usbr.gov/uc/water/hydrodata/
**Protocol**: REST (static JSON/CSV files served via structured URL paths)
**Auth**: None
**Data Format**: JSON, CSV
**Update Frequency**: Real-time to daily (depending on station and parameter)
**License**: US Government public domain

## What It Provides

The Bureau of Reclamation's HydroData system provides telemetry data from hundreds of monitoring stations across the western United States. USBR manages major dams and reservoirs including:

- Lake Powell, Lake Mead, Flaming Gorge (Colorado River)
- Grand Coulee, Hungry Horse (Columbia Basin)
- Klamath Basin facilities

Data parameters include:
- **Reservoir storage** (acre-feet)
- **Water surface elevation** (feet)
- **Inflow/outflow** (cfs)
- **Releases and diversions**
- **Water temperature**
- **Meteorological data** (precipitation, evapotranspiration, wind, temperature)

## API Details

Data is organized by basin and site, accessed via a structured URL hierarchy:

**Pattern**: `https://www.usbr.gov/uc/water/hydrodata/{basin_data}/{site_id}/json/{param_id}.json`

Example endpoints:
- Klamath basin metadata: `https://www.usbr.gov/uc/water/hydrodata/klamath_basin_data/meta.csv`
- Site dashboard: `https://www.usbr.gov/uc/water/hydrodata/klamath_basin_data/{site_id}/dashboard.html`
- JSON data: `https://www.usbr.gov/uc/water/hydrodata/klamath_basin_data/{site_id}/json/{param_id}.json`
- CSV data: `https://www.usbr.gov/uc/water/hydrodata/klamath_basin_data/{site_id}/csv/{param_id}.csv`

Parameter IDs are numeric codes (e.g., 19 = FLOW, 17 = RESERVOIR STORAGE, 8 = AVE AIR TEMP, etc.).

Each basin has its own site map and metadata CSV. The navigator page (`nav.html`) provides the full hierarchy.

Data sources: BOR (Bureau of Reclamation), USGS, NRCS, CDEC, CASS, COOP, ACIS — the system aggregates from multiple agencies.

## Freshness Assessment

Good. Data is typically updated daily or sub-daily for operational parameters (flow, storage). The navigator shows "Last updated" timestamps. Some stations report on 15-minute intervals for flow data.

## Entity Model

- **Basin**: basin identifier (e.g., `klamath_basin_data`, `Upper_Colorado_River`)
- **Site**: site ID (numeric), code (e.g., `ACHO`), name, type (Reservoir/Canal/Reach/Diversion/Stream Gage/Climate Site)
- **Parameter**: parameter ID (numeric), name (FLOW, STORAGE, ELEVATION, etc.), units
- **Observation**: timestamp, value, data flag

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily to sub-daily updates for most operational parameters |
| Openness | 3 | US Government public domain, no auth required |
| Stability | 3 | Federal agency, critical water infrastructure management |
| Structure | 2 | Structured URLs with JSON/CSV but no formal API spec; predictable patterns |
| Identifiers | 2 | Numeric site and parameter IDs; cross-refs to USGS/NRCS sites |
| Additive Value | 3 | Major western US reservoirs (Powell, Mead) not available elsewhere in one feed |
| **Total** | **15/18** | |

## Notes

- This is the authoritative source for operational data from major Bureau of Reclamation facilities. Lake Powell and Lake Mead data are among the most closely-watched water metrics in the US.
- The data navigator is organized around static file trees rather than a queryable API — scraping the `nav.html` or `meta.csv` is needed to discover available stations and parameters.
- The system aggregates data from multiple agencies (USGS, NRCS, CDEC), making it a convenient single access point for western water data.
- Some basin data directories return 403 errors — access may vary by region/basin. The Klamath basin data was confirmed accessible.
- For reservoir-specific data, pair with California CDEC (which covers state reservoirs) for comprehensive western US coverage.
