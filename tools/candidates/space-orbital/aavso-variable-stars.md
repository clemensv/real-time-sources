# AAVSO — Variable Star Observations

**Country/Region**: Global
**Publisher**: American Association of Variable Star Observers
**API Endpoint**: `https://www.aavso.org/vsx/index.php?view=api.object`
**Documentation**: https://www.aavso.org/apis
**Protocol**: REST (JSON, CSV, VOTable)
**Auth**: None (VSX catalog), API Key (observation data)
**Data Format**: JSON (VSX), CSV/VOTable (observations)
**Update Frequency**: Near real-time — observations available within hours of submission
**License**: AAVSO data use policy (free for research; attribution required)

## What It Provides

AAVSO is the world's largest organization dedicated to variable star observations, with over 60 million observations spanning 100+ years. The Variable Star Index (VSX) catalogs over 2 million variable stars with their types, periods, magnitude ranges, and physical properties. Observers worldwide submit brightness measurements (visual estimates and CCD photometry), creating a near-real-time monitoring network for stellar variability.

When Betelgeuse dimmed dramatically in 2019-2020, AAVSO observers provided the continuous light curve that drove global scientific and media attention. That's the kind of signal this network captures.

## API Details

- **VSX object lookup**: `GET /vsx/index.php?view=api.object&format=json&ident={star_name}` — catalog data for a star
- **VSX search**: `GET /vsx/index.php?view=api.list&format=json&maxrecords={n}` — search/list variable stars
- **VSX fields**: `Name`, `AUID`, `RA2000`, `Declination2000`, `VariabilityType`, `Period`, `MaxMag`, `MinMag`, `SpectralType`, `Discoverer`
- **WebObs**: Web interface for observation retrieval (structured but requires session auth)
- **VOTable output**: Supported for interoperability with astronomical tools
- **No auth for VSX**: Catalog queries are unauthenticated
- **Observation data**: Requires AAVSO account for bulk access

## Freshness Assessment

VSX catalog data is continuously updated as new variable stars are discovered and characterized. Observation data is available within hours of submission — observers submit nightly, and during campaigns (like Betelgeuse monitoring), multiple observations per hour from distributed sites.

Confirmed live: VSX API returned full catalog entry for Betelgeuse (alf Ori) including AUID `000-BBK-383`, variability type SRC, period 423 days, magnitude range 0.0-1.6 V.

## Entity Model

- **Variable Star**: `AUID` (unique identifier), `Name` (designation), RA/Dec (J2000), `VariabilityType`, `Period` (days), `MaxMag`/`MinMag`, `SpectralType`
- **Observation**: `JD` (Julian Date), `magnitude`, `band` (V, B, R, I, visual), `observer_code`, `star` (AUID)
- **Observer**: Observer code, name, location
- **Variability types**: Eclipsing binaries, pulsating stars, cataclysmic variables, etc.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hours lag for new observations; VSX catalog updated continuously |
| Openness | 2 | VSX is no-auth; observation data requires account |
| Stability | 3 | Running since 1911; major astronomical institution |
| Structure | 3 | Clean JSON for VSX; structured formats for observations |
| Identifiers | 3 | AUID, star designations, observer codes, JD timestamps |
| Additive Value | 3 | Unique century-long variable star monitoring network |
| **Total** | **16/18** | |

## Notes

- Confirmed live: VSX API returned rich Betelgeuse data with all expected fields.
- The WebObs interface for observation data is web-first; bulk API access requires negotiation with AAVSO.
- AAVSO data has powered thousands of scientific papers and several major discoveries.
- The network's strength is sustained monitoring — some stars have been observed continuously for 100+ years.
- Real-time alerting: AAVSO issues Alert Notices for significant stellar events (novae, unusual behavior).
- Pairs with ZTF (automated survey detections trigger AAVSO follow-up campaigns) and GCN (counterparts to gravitational wave events).
