# CelesTrak

**Country/Region**: Global
**Publisher**: CelesTrak (Dr. T.S. Kelso) / AGI
**API Endpoint**: `https://celestrak.org/NORAD/elements/gp.php`
**Documentation**: https://celestrak.org/NORAD/documentation/gp-data-formats.php
**Protocol**: REST (HTTP GET with query parameters)
**Auth**: None
**Data Format**: TLE (Two-Line Element), JSON, XML, KVN, CSV
**Update Frequency**: Multiple times per day (TLEs updated as new data arrives from 18th SDS)
**License**: Free for non-commercial use; no explicit open data license

## What It Provides

CelesTrak is the primary public source for NORAD Two-Line Element (TLE) sets — the orbital parameters for all tracked objects in Earth orbit. TLEs are the standard input for satellite tracking and orbit prediction software (SGP4 propagator). CelesTrak provides GP (General Perturbations) data for 60,000+ cataloged objects, organized by satellite group (active, weather, communications, space stations, debris, etc.).

CelesTrak also provides supplemental GP data from commercial satellite operators with higher update frequency than the standard 18th Space Defense Squadron (18 SDS) catalog. The site is currently warning about the imminent 5-digit catalog number exhaustion (~July 2026), which will break TLE format compatibility.

## API Details

- **GP data query**: `https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT={format}`
- **By catalog number**: `gp.php?CATNR={number}&FORMAT=json`
- **By INTLDES**: `gp.php?INTDES={year-launch-piece}&FORMAT=json`
- **By name**: `gp.php?NAME={name}&FORMAT=json`
- **Formats**: `tle` (traditional 2-line), `3le` (3-line with name), `json`, `json-pretty`, `xml`, `kvn`, `csv`
- **Groups**: `stations`, `active`, `visual`, `weather`, `resource`, `sarsat`, `geo`, `intelsat`, `ses`, `iridium`, `starlink`, `oneweb`, `last-30-days`, `analyst`, `fengyun-1c-debris`, etc.
- **Supplemental data**: `/NORAD/elements/supplemental/` for operator-provided data (SpaceX, Planet, etc.)
- **Table view**: `table.php` with same parameters for HTML table rendering
- **No authentication required**
- **Note**: The GP API was returning 500 errors during probing — may be under maintenance or load; normally reliable

## Freshness Assessment

TLEs are updated as new observations are processed, typically several times per day for active satellites. High-interest objects (ISS, recently launched) may be updated multiple times per day. The underlying data comes from the 18th Space Defense Squadron (formerly JSpOC). Supplemental data from operators may update more frequently.

## Entity Model

- **Satellite/Object**: Catalog number (NORAD ID), international designator, name
- **TLE/GP Element Set**: epoch, mean motion, eccentricity, inclination, RAAN, argument of perigee, mean anomaly, Bstar drag term, element set number, revolution number
- **JSON format fields**: `OBJECT_NAME`, `OBJECT_ID`, `EPOCH`, `MEAN_MOTION`, `ECCENTRICITY`, `INCLINATION`, `RA_OF_ASC_NODE`, `ARG_OF_PERICENTER`, `MEAN_ANOMALY`, `EPHEMERIS_TYPE`, `CLASSIFICATION_TYPE`, `NORAD_CAT_ID`, `ELEMENT_SET_NO`, `REV_AT_EPOCH`, `BSTAR`, `MEAN_MOTION_DOT`, `MEAN_MOTION_DDOT`

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Updated multiple times/day; not real-time |
| Openness | 2 | No auth, but no formal open license; non-commercial use only |
| Stability | 3 | Running since 1985; pillar of space situational awareness |
| Structure | 3 | JSON/XML/CSV alongside legacy TLE; well-documented formats |
| Identifiers | 3 | NORAD catalog numbers are the global standard |
| Additive Value | 3 | Authoritative orbital data source; essential for space tracking |
| **Total** | **16/18** | |

## Notes

- CelesTrak is the most widely used public source for TLE data, operated by Dr. T.S. Kelso since 1985.
- The 5-digit catalog number limit (~July 2026) will force a transition to new formats — CelesTrak's JSON format already handles 6+ digit IDs.
- TLE format is from the 1960s with significant precision limitations. The JSON GP format provides higher precision.
- For authenticated access with more features (historical TLEs, conjunction data), use Space-Track.org instead.
- SGP4 propagator libraries are available in every major language (Python: `sgp4`, JS: `satellite.js`).
