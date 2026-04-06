# JPL SBDB Close Approach API

**Country/Region**: Global
**Publisher**: NASA Jet Propulsion Laboratory
**API Endpoint**: `https://ssd-api.jpl.nasa.gov/cad.api`
**Documentation**: https://ssd-api.jpl.nasa.gov/doc/cad.html
**Protocol**: REST (JSON)
**Auth**: None
**Data Format**: JSON (structured with fields array + data arrays)
**Update Frequency**: Continuously updated as new orbital solutions are computed
**License**: Public domain (US government work)

## What It Provides

The JPL Small-Body Database Close Approach API returns a list of asteroid and comet close approaches to Earth (or other bodies) within configurable distance and time parameters. Each record includes the object designation, approach date, nominal distance, minimum/maximum distance (uncertainty), relative velocity, and absolute magnitude. This is the "what's coming near Earth" API.

Combined with NEO risk assessment data, this gives you a real-time picture of the near-Earth asteroid traffic.

## API Details

- **Close approaches**: `GET /cad.api?date-min={YYYY-MM-DD}&date-max={YYYY-MM-DD}&dist-max={AU}&sort=date`
- **Filtering**: `dist-max` (AU), `dist-min`, `h-max` (absolute magnitude, proxy for size), `v-inf-max` (velocity)
- **Body selection**: `des` (designation), `spk` (SPK ID), `body` (close-approach body, default Earth)
- **Output control**: `fields` parameter to select specific columns, `limit` for max results
- **Response format**: `fields` array (column names) + `data` array (rows of values) — compact tabular format
- **No auth required**: Public API
- **Rate limit**: Reasonable use

## Freshness Assessment

Orbital solutions are recomputed as new observations arrive at the Minor Planet Center. For recently-discovered NEOs, approach parameters can change rapidly as the orbit is refined. The API always returns the latest orbital solution.

Confirmed live: queried April 2026 close approaches within 0.05 AU, received 31 objects. First entry: 2026 FV5 at 0.030 AU on April 1.

## Entity Model

- **Close approach**: `des` (designation), `cd` (close approach date/time), `dist` (nominal distance AU), `dist_min`/`dist_max`, `v_inf` (relative velocity km/s), `h` (absolute magnitude)
- **Object**: Designation (e.g., `2026 FV5`), orbit class (NEA, PHA, comet)
- **Temporal**: JD (Julian Date) and calendar date formats

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Updated with new orbital solutions; not real-time streaming |
| Openness | 3 | No auth, public domain, no rate limit |
| Stability | 3 | JPL infrastructure, long-running API |
| Structure | 3 | Clean JSON, tabular format, well-documented fields |
| Identifiers | 3 | Designations, SPK IDs, JD timestamps |
| Additive Value | 2 | Structured close-approach data complements NASA NEO and Horizons |
| **Total** | **16/18** | |

## Notes

- Confirmed live: 31 close approaches in April 2026 within 0.05 AU.
- The tabular format (fields + data arrays) is compact and efficient — each row is a positional array matching the fields array.
- `h` (absolute magnitude) is a proxy for size: H < 22 roughly corresponds to objects > 140m diameter.
- For the "is anything dangerous coming?" question, combine with JPL Sentry (impact risk) data.
- Pairs with NASA NEO (broader NEO context), CelesTrak (if the object has a spacecraft), and Horizons (detailed ephemeris).
