# UK Environment Agency — Water Quality Explorer

**Country/Region**: United Kingdom (England)
**Publisher**: Environment Agency (EA), Department for Environment, Food and Rural Affairs (DEFRA)
**API Endpoint**: `https://environment.data.gov.uk/water-quality/` (web app + API)
**Documentation**: https://environment.data.gov.uk/water-quality/
**Protocol**: REST (Linked Data API); Web application
**Auth**: None
**Data Format**: JSON-LD, CSV, HTML
**Update Frequency**: Varies — discrete sampling results uploaded after lab analysis (days to weeks); some continuous monitoring
**License**: Open Government Licence (OGL)

## What It Provides

The EA Water Quality Explorer provides access to water quality monitoring data for rivers, lakes, canals, estuaries, and coastal waters across England. The system covers:

- **Chemical determinands**: nutrients (nitrate, phosphate, ammonia), metals (lead, cadmium, zinc), BOD, COD
- **Biological monitoring**: invertebrate indices, fish surveys, macrophyte assessments
- **Physical parameters**: temperature, pH, dissolved oxygen, conductance, turbidity
- **Continuous monitoring**: some sites have continuous multi-parameter sondes

The archive contains millions of measurements spanning decades, from thousands of sampling points.

## API Details

The EA has rebuilt their Water Quality platform as a modern Next.js web application (version v1.23.2 as of April 2026). The previous Linked Data API endpoints (e.g., `/water-quality/id/sampling-point`) appear to have been deprecated or restructured.

**Current access**:
- Web map explorer at `https://environment.data.gov.uk/water-quality/`
- The application uses internal API endpoints that power the map and data views
- Google Analytics tag: G-12JL3WT6ZY

**Previous API** (may be deprecated):
- `https://environment.data.gov.uk/water-quality/id/sampling-point?_limit=N` — list sampling points
- `https://environment.data.gov.uk/water-quality/data/measurement?_limit=N` — list measurements
- Both returned 404 during testing

**Alternative EA data services**:
- Hydrology API: `https://environment.data.gov.uk/hydrology/` — real-time river levels and flows (working)
- Flood monitoring API: `https://environment.data.gov.uk/flood-monitoring/` — real-time flood data (working)

The water quality service appears to be in a transition period between the old Linked Data API and the new web application.

## Freshness Assessment

Mixed. The underlying data is a mix of:
- Discrete samples: collected on scheduled monitoring programs, results available after lab analysis (days/weeks delay)
- Continuous monitoring: some sites have real-time multi-parameter sondes
- Historical archive: decades of data

The freshness of the API itself is uncertain due to the apparent platform migration.

## Entity Model

- **Sampling Point**: EA identifier, name, easting/northing (OSGB), water body, catchment
- **Sample**: sampling point, date/time, purpose (routine/investigation/compliance), sample type
- **Measurement**: sample, determinand, result value, unit, qualifier, compliance status
- **Determinand**: EA code, name, unit, CAS number (for chemicals)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Mostly discrete samples with lab delay; some continuous monitoring |
| Openness | 3 | OGL license, no auth required |
| Stability | 2 | Platform appears to be in migration; old API endpoints returning 404 |
| Structure | 1 | Old API seems deprecated; new API not yet documented |
| Identifiers | 2 | EA sampling point IDs; WFD water body references |
| Additive Value | 2 | England-only but extensive historical record |
| **Total** | **11/18** | |

## Notes

- The EA Water Quality platform appears to be in active migration from a Linked Data API to a new Next.js web application. This makes it a risky target for integration right now.
- The EA's other data services (Hydrology, Flood Monitoring) have stable, well-documented APIs — the Water Quality service may eventually reach the same standard.
- For real-time English water quality data, the EA Hydrology API provides some continuous WQ parameters (temperature, conductivity) at river monitoring stations.
- Scotland (SEPA), Wales (NRW), and Northern Ireland (NIEA) have separate water quality monitoring systems.
- The historical archive is extensive and valuable — once the new API stabilizes, this could become a strong candidate.
- Recommend: wait for the new platform to mature and document its API before investing in integration.
