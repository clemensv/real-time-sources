# EEA Up-to-Date Air Quality

**Country/Region**: Europe (EU/EEA member states)
**Publisher**: European Environment Agency (EEA)
**API Endpoint**: `https://eeadmz1-downloads-webapp.azurewebsites.net/` (download service)
**Documentation**: https://www.eea.europa.eu/en/datahub
**Protocol**: REST (download service) / SOS (Sensor Observation Service)
**Auth**: None
**Data Format**: CSV, JSON (via download webapp)
**Update Frequency**: Hourly (E1a up-to-date data)
**License**: EEA Standard Reuse Policy (open, attribution required)

## What It Provides

The EEA Air Quality portal aggregates near-real-time (E1a "up-to-date") and validated (E2a) air quality data from all EU/EEA member state monitoring networks. It covers NO₂, PM10, PM2.5, O₃, SO₂, CO, C₆H₆ (benzene), and heavy metals across thousands of stations. The E1a data stream provides hourly unvalidated measurements — the freshest available from European national networks.

## API Details

- **Download Service**: `https://eeadmz1-downloads-webapp.azurewebsites.net/`
  - Web app for filtering and downloading CSV bulk data by country, pollutant, year, station
- **Legacy FME Service** (being retired): `https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw`
  - Parameters: CountryCode, Pollutant, Year_from, Year_to, Source (E1a/E2a), Output
- **SPARQL / Linked Data**: EEA provides RDF endpoints for station metadata
- **Airbase codes**: Stations identified by EoI codes (e.g., `DEBB003`)
- **No real REST API**: Data access is primarily through download services and bulk files, not a stateless REST API

## Freshness Assessment

E1a (up-to-date) data is reported hourly by member states and published with a delay of 1-2 hours. This is unvalidated, preliminary data. Validated E2a data has a ~1 year delay. The download service is the primary access mechanism — there is no lightweight real-time JSON API.

## Entity Model

- **Country** → has many **Stations**
- **Station** → EoI code, coordinates, type (traffic/industrial/background), area (urban/suburban/rural)
- **Station** → measures **Pollutants** via **Sampling Points**
- **Sampling Point** → time-series of **Measurements** (concentration + timestamp)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Hourly E1a data, but 1-2 hr delay and bulk access only |
| Openness | 3 | Free, no auth, EEA open reuse policy |
| Stability | 3 | EU institutional backing, long-running program |
| Structure | 1 | Bulk CSV downloads, no clean REST API |
| Identifiers | 2 | EoI station codes, but query interface is clunky |
| Additive Value | 2 | Pan-European; already partially in OpenAQ |
| **Total** | **13/18** | |

## Notes

- The EEA data is the authoritative pan-European source, but the access mechanism (bulk download webapp) makes real-time integration cumbersome.
- OpenAQ already ingests EEA E1a data, so using OpenAQ may be preferable for programmatic access.
- The download service is hosted on Azure and is a React SPA — not a pure API.
- Individual member states often provide better direct APIs for their own data (see UBA Germany, Defra UK).
- The legacy FME streaming endpoint now requires authentication and may be retired.
