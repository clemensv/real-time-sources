# Defra AURN (UK Automatic Urban and Rural Network)

**Country/Region**: United Kingdom
**Publisher**: Department for Environment, Food & Rural Affairs (Defra)
**API Endpoint**: `https://uk-air.defra.gov.uk/sos-ukair/api/v1/`
**Documentation**: https://uk-air.defra.gov.uk/data/
**Protocol**: REST (52°North SOS Timeseries API)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Hourly
**License**: Open Government Licence v3.0 (OGL)

## What It Provides

The UK AURN is the UK's primary ambient air quality monitoring network, operated by Defra. It measures O₃, NO₂, SO₂, PM2.5, PM10, and CO across ~170 stations covering urban, suburban, rural, and kerbside sites across England, Scotland, Wales, and Northern Ireland. The SOS API provides structured access to timeseries data.

## API Details

- **Base URL**: `https://uk-air.defra.gov.uk/sos-ukair/api/v1/`
- **Key Endpoints** (52°North Timeseries API):
  - `GET /stations` — list all monitoring stations with geometry
  - `GET /stations/{id}` — station detail
  - `GET /timeseries` — list available timeseries (station + parameter combos)
  - `GET /timeseries/{id}` — timeseries metadata
  - `GET /timeseries/{id}/getData` — actual measurement data with time range
  - `GET /phenomena` — list measured phenomena (pollutants)
  - `GET /categories` — data categories
- **Query Parameters**: `timespan` (ISO 8601 period), `limit`, `offset`
- **Response**: GeoJSON-like features with coordinates; timeseries values in `{timestamp, value}` pairs
- **Sample Response** (stations): `[{"properties":{"id":1,"label":"Belfast Centre-Arsenic in PM10"},"geometry":{"coordinates":[54.59,-5.93],"type":"Point"},"type":"Feature"}]`

## Freshness Assessment

Data is updated hourly. The web page at `uk-air.defra.gov.uk/latest/currentlevels` shows readings "for the hour up to" the current hour. The SOS API reflects this same hourly cadence. Data is preliminary and unratified.

## Entity Model

- **Station** → id, label, coordinates (GeoJSON Point)
- **Timeseries** → links a Station to a Phenomenon (pollutant) with unit of measurement
- **Phenomenon** → pollutant type (O₃, NO₂, PM2.5, etc.)
- **Data** → timestamp + value pairs for a given timeseries

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly updates, current hour data |
| Openness | 3 | OGL v3.0, no auth required |
| Stability | 3 | UK government, 52°North standard SOS platform |
| Structure | 3 | Clean JSON, standard Timeseries API pattern |
| Identifiers | 2 | Numeric IDs; station labels include pollutant — slightly odd |
| Additive Value | 2 | UK-specific; already partially in OpenAQ |
| **Total** | **16/18** | |

## Notes

- The 52°North SOS Timeseries API is a well-known standard for environmental data — the same pattern is used by other agencies.
- Station labels concatenate site name + pollutant, so one physical station appears as multiple "stations" in the API. This is a quirk of the SOS mapping.
- UK-AIR also offers CSV bulk downloads and an HTML data selector for custom queries.
- Defra also provides forecast data and DAQI (Daily Air Quality Index) via the website, though not easily via the SOS API.
- Already ingested by OpenAQ, but the direct API gives more granular timeseries access.
