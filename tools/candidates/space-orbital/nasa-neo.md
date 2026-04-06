# NASA Near Earth Object (NEO) Web Service

**Country/Region**: Global
**Publisher**: NASA / JPL (Jet Propulsion Laboratory)
**API Endpoint**: `https://api.nasa.gov/neo/rest/v1/feed`
**Documentation**: https://api.nasa.gov/, https://neo.jpl.nasa.gov/
**Protocol**: REST
**Auth**: API Key (free, `DEMO_KEY` available)
**Data Format**: JSON
**Update Frequency**: Daily (orbital calculations updated as new observations arrive)
**License**: US Government public domain

## What It Provides

The NASA NEO Web Service (NeoWs) provides data on near-Earth objects — asteroids and comets whose orbits bring them close to Earth. The feed endpoint returns close approach data by date range, including estimated diameter, relative velocity, miss distance, and whether the object is potentially hazardous. Data comes from NASA's Center for Near Earth Object Studies (CNEOS) at JPL.

Live probe returned 32 NEOs for a 2-day window, including detailed orbital data: asteroid names/IDs, estimated diameters (min/max in km/mi/m/ft), close approach dates with relative velocities (km/s, km/h, mph) and miss distances (AU, lunar, km, miles), and hazard classification.

## API Details

- **Feed by date**: `GET /neo/rest/v1/feed?start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}&api_key={key}`
- **NEO lookup**: `GET /neo/rest/v1/neo/{asteroid_id}?api_key={key}` — full orbital data for one NEO
- **Browse**: `GET /neo/rest/v1/neo/browse?api_key={key}` — paginated list of all NEOs
- **Sentry**: `GET /neo/rest/v1/neo/sentry?api_key={key}` — objects on the Sentry impact monitoring list
- **Response fields**: `id`, `neo_reference_id`, `name`, `nasa_jpl_url`, `absolute_magnitude_h`, `estimated_diameter` (min/max in km/m/mi/ft), `is_potentially_hazardous_asteroid`, `close_approach_data` (date, velocity, miss_distance, orbiting_body), `is_sentry_object`, `orbital_data`
- **Pagination**: `links.next`/`links.previous` in feed response
- **Date range limit**: 7 days maximum per feed request

## Freshness Assessment

Orbital data is updated as new observations are processed, typically daily. Close approach predictions are computed from the latest orbit solutions. For newly discovered objects, data appears within hours of confirmation. The Sentry risk table is continuously updated.

## Entity Model

- **NEO**: `id`/`neo_reference_id` (integer), name, JPL URL, absolute magnitude, diameter estimates
- **Close Approach**: Date, relative velocity, miss distance, orbiting body (usually Earth)
- **Orbit**: Orbital elements (semi-major axis, eccentricity, inclination, etc.)
- **Sentry Entry**: Impact probability, Palermo/Torino scale ratings

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily updates; predictions computed from latest orbits |
| Openness | 3 | Free API key; US Gov public domain |
| Stability | 3 | NASA/JPL operated; long-running service |
| Structure | 3 | Rich JSON with multi-unit measurements and linked data |
| Identifiers | 3 | Stable NEO reference IDs; JPL Small-Body Database cross-references |
| Additive Value | 3 | Unique dataset — no other public source for NEO close approaches |
| **Total** | **17/18** | |

## Notes

- The `is_potentially_hazardous_asteroid` flag identifies PHAs (Potentially Hazardous Asteroids) — objects with MOID < 0.05 AU and H < 22.
- The Sentry endpoint is especially interesting — it lists objects with non-zero impact probabilities.
- Data ultimately comes from the Minor Planet Center (MPC) and JPL's orbit determination pipeline.
- DEMO_KEY works for testing; free registered keys allow 1000 req/hour.
- The 7-day feed window limit means you need multiple requests for longer ranges.
