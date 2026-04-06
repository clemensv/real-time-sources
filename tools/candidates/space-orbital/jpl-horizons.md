# JPL Horizons

**Country/Region**: Global
**Publisher**: NASA Jet Propulsion Laboratory
**API Endpoint**: `https://ssd.jpl.nasa.gov/api/horizons.api`
**Documentation**: https://ssd-api.jpl.nasa.gov/doc/horizons.html
**Protocol**: REST (JSON wrapper around text ephemeris)
**Auth**: None
**Data Format**: JSON envelope with text-formatted ephemeris data
**Update Frequency**: Ephemeris computed on-demand; orbital elements updated as new observations arrive
**License**: Public domain (US government work)

## What It Provides

JPL Horizons is the gold standard for solar system ephemeris computation. It provides precise positions, velocities, and physical properties for over 1.3 million objects: planets, moons, asteroids, comets, spacecraft, and dynamical points. Given a target body, observer location, and time span, Horizons computes apparent or geometric positions with sub-arcsecond precision.

This isn't a streaming feed — it's an on-demand computation engine. But it's essential infrastructure for anything involving orbital mechanics, asteroid tracking, or spacecraft position calculation.

## API Details

- **Ephemeris request**: `GET /api/horizons.api?format=json&COMMAND='{target}'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&START_TIME='{start}'&STOP_TIME='{stop}'&STEP_SIZE='{step}'`
- **Object data only**: `GET /api/horizons.api?format=json&COMMAND='{target}'&OBJ_DATA='YES'&MAKE_EPHEM='NO'`
- **Target selection**: Body ID (e.g., `499` for Mars), name (`Mars`), designation (`2024 PT5`), or wildcard search
- **No auth required**: Completely public API
- **Rate limit**: Reasonable use; JPL asks for a descriptive `User-Agent`
- **Output format**: JSON envelope with `result` field containing formatted text ephemeris (legacy text format)

## Freshness Assessment

Orbital elements are updated as new astrometric observations are processed — for asteroids this can be daily. The ephemeris computation itself is instantaneous. For tracking near-Earth objects or upcoming close approaches, Horizons provides the authoritative trajectory data.

Confirmed live: queried Mars (ID 499), received full physical data including radius, mass, density, flattening, with revision date June 2025.

## Entity Model

- **Body**: ID number, name, aliases, orbital elements, physical properties
- **Ephemeris**: Time, RA/Dec (or other coordinate system), distance, light-time, magnitude, phase angle, etc.
- **Orbital Elements**: Semi-major axis, eccentricity, inclination, node, argument of perihelion, mean anomaly, epoch
- **Observer**: Geocentric, topocentric, or spacecraft reference frame

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | On-demand computation; orbital elements updated daily-ish |
| Openness | 3 | No auth, public domain data, no rate limit |
| Stability | 3 | JPL infrastructure, running for decades (web version since 1996) |
| Structure | 2 | JSON envelope but text-formatted ephemeris inside (parsing required) |
| Identifiers | 3 | IAU body IDs, SPK IDs, designations, names |
| Additive Value | 3 | Authoritative solar system ephemeris — irreplaceable |
| **Total** | **16/18** | |

## Notes

- Confirmed live with Mars query — rich physical data and precise orbital elements.
- The text-formatted ephemeris inside the JSON envelope is a legacy format — parsing it requires understanding the column layout. Not ideal, but well-documented.
- For close approach data, the JPL SBDB Close Approach API (`ssd-api.jpl.nasa.gov/cad.api`) provides structured JSON — confirmed: 31 close approaches in April 2026 within 0.05 AU.
- Horizons covers spacecraft too — you can get positions of Voyager, JWST, Parker Solar Probe, etc.
- Pairs with CelesTrak for artificial satellites and NASA NEO for asteroid-specific risk assessment.
