# Minor Planet Center

**Country/Region**: Global
**Publisher**: International Astronomical Union (hosted at Smithsonian Astrophysical Observatory)
**API Endpoint**: `https://www.minorplanetcenter.net/iau/MPCORB/`
**Documentation**: https://www.minorplanetcenter.net/iau/services/
**Protocol**: HTTP (text files), some REST endpoints
**Auth**: None
**Data Format**: Fixed-width text (MPC packed format), some JSON
**Update Frequency**: Daily (orbital elements); alerts within hours of discovery
**License**: Public (IAU data)

## What It Provides

The Minor Planet Center is the global clearinghouse for asteroid and comet observations. Every new asteroid discovery, every orbit update, every potential impact assessment starts here. The MPC receives astrometric observations from surveys worldwide (Pan-STARRS, Catalina Sky Survey, ATLAS, ZTF, etc.), computes orbits, assigns designations, and publishes orbital elements.

The NEA (Near Earth Asteroid) catalog file provides orbital elements for all known near-Earth objects, updated daily. New discoveries are announced via MPC Electronic Circulars (MPECs).

## API Details

- **NEA orbital elements**: `GET /iau/MPCORB/NEA.txt` — full NEA catalog in MPC packed orbit format
- **Full catalog**: `GET /iau/MPCORB/MPCORB.DAT.gz` — all ~1.3 million minor planets (compressed)
- **MPECs**: Discovery announcements published as web pages with structured data
- **MPEC format**: Fixed-width text columns: designation, magnitude, epoch, orbital elements, observations count, arc length
- **No auth required**: Public data files
- **Bulk download**: Full catalog ~250MB compressed
- **New discoveries**: Appear in MPEC circulars within hours of confirmation

## Freshness Assessment

Orbital elements are recomputed daily. New asteroid discoveries are announced via MPECs within hours of confirmation. The NEA.txt file is regenerated daily.

Confirmed live: NEA.txt downloaded successfully (8MB file), containing entries including (433) Eros and (719) Albert with orbital elements epoch 2026-04-01.

## Entity Model

- **Minor planet**: Packed designation, absolute magnitude (H), slope parameter (G), epoch, orbital elements (M, ω, Ω, i, e, n, a)
- **Observation arc**: First and last observation dates, number of observations, number of oppositions
- **Designation**: Packed MPC format (e.g., `K25BL` = 2025 BL)
- **Named object**: Number + name (e.g., `(433) Eros`)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily catalog updates; MPECs within hours of discovery |
| Openness | 3 | No auth, public data, IAU mandate |
| Stability | 3 | IAU infrastructure, running since 1947 |
| Structure | 1 | Fixed-width text format (legacy, requires positional parsing) |
| Identifiers | 3 | Packed designations, numbered objects, IAU designations |
| Additive Value | 3 | Authoritative asteroid/comet catalog — single point of truth |
| **Total** | **15/18** | |

## Notes

- Confirmed live: NEA.txt downloaded with fresh orbital elements (epoch April 2026).
- The fixed-width text format is a relic of punch-card era astronomy — parsing it requires knowing exact column positions (documented in MPC format specification).
- The MPC is transitioning some services; the `/iau/lists/` directory returned 404 for some previously-available pages.
- For structured JSON access to close approach data, JPL's SBDB Close Approach API is preferable.
- The MPC and JPL are complementary: MPC is the observation clearinghouse; JPL computes refined orbits and risk assessments.
- Pairs with JPL Horizons (ephemeris for any MPC object), JPL SBDB Close Approach (upcoming encounters), NASA NEO (risk assessment), and ZTF (survey that feeds discoveries to MPC).
