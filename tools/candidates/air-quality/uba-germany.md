# UBA (Umweltbundesamt — German Federal Environment Agency)

**Country/Region**: Germany
**Publisher**: Umweltbundesamt (UBA)
**API Endpoint**: `https://www.umweltbundesamt.de/api/air_data/v3/`
**Documentation**: https://www.umweltbundesamt.de/en/data/air/air-data (short link: uba.de/n305659en)
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Hourly
**License**: Open data (German government, dl-de/by-2-0)

## What It Provides

UBA operates Germany's national air quality monitoring network and provides a clean REST API for accessing station metadata, measured components, and hourly measurement data. It covers PM10, PM2.5, O₃, NO₂, SO₂, CO, benzene (C₆H₆), and heavy metals across hundreds of stations in all German states (Bundesländer). Stations are classified by type (traffic, industrial, background) and setting (urban, suburban, rural).

## API Details

- **Base URL**: `https://www.umweltbundesamt.de/api/air_data/v3/`
- **Key Endpoints**:
  - `GET /stations/json` — all stations with metadata (code, name, city, lat/lon, network, type, setting)
  - `GET /components/json` — list of measured components with units (12 components)
  - `GET /measures/json` — measurement data filtered by station, component, date/time range
  - `GET /airquality/json` — air quality index data
  - `GET /scopes/json` — measurement averaging scopes
  - `GET /networks/json` — monitoring networks by Bundesland
- **Query Parameters**: `station`, `component`, `date_from`, `date_to`, `time_from`, `time_to`, `lang` (en/de)
- **Response Structure**: Indices array (column definitions) + data object (keyed by ID)
- **Components** (12): PM₁₀, CO, O₃, SO₂, NO₂, Pb in PM10, BaP in PM10, Benzene, PM₂.₅, As in PM10, Cd in PM10, Ni in PM10

## Freshness Assessment

Hourly measurements are available. The API returns data indexed by station and component for specified time ranges. Data may have a short delay (1-2 hours). The API is responsive and well-structured.

## Entity Model

- **Network** (Bundesland) → has many **Stations**
- **Station** → id, EoI code (e.g., `DEBB003`), name, city, lat/lon, type, setting, active period
- **Component** → id, code, symbol, unit, name
- **Measure** → station × component × datetime → value
- **Scope** → averaging period (hourly, daily, etc.)

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly data, responsive API |
| Openness | 3 | No auth, open government data |
| Stability | 3 | German federal agency, versioned API (v3) |
| Structure | 2 | JSON but custom index-based format, not standard REST resources |
| Identifiers | 3 | Stable station IDs + EoI codes, component IDs |
| Additive Value | 2 | Germany-only; partially in EEA/OpenAQ |
| **Total** | **16/18** | |

## Notes

- The API's response format is unusual: it returns column definitions in an `indices` array and data as a keyed object. This requires custom parsing but is consistent.
- Stations include EoI (European station) codes, enabling cross-referencing with EEA data.
- The `lang` parameter supports English and German responses.
- All 12 components (including heavy metals in PM10) are available — more granular than many other sources.
- Excellent candidate for a Germany-specific connector given the clean API and no auth requirement.
