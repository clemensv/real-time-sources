# DMI Open Data — Denmark

**Country/Region**: Denmark (including Greenland and Faroe Islands)
**Publisher**: DMI (Danish Meteorological Institute)
**API Endpoint**: `https://dmigw.govcloud.dk/v2/metObs/` (observations), `https://dmigw.govcloud.dk/v2/climateData/` (climate)
**Documentation**: https://opendatadocs.dmi.govcloud.dk/
**Protocol**: OGC API — Features (GeoJSON)
**Auth**: API Key (free registration required)
**Data Format**: GeoJSON (application/geo+json)
**Update Frequency**: 10-minute observations, hourly summaries
**License**: Danish Open Government Licence / Creative Commons (terms at dmi.dk/friedata)

## What It Provides

DMI provides meteorological data via a modern OGC API — Features compliant interface:

- **Meteorological Observations** (`metObs`):
  - **Collections**: `observation` (individual readings) and `station` (station metadata)
  - Parameters: Temperature, humidity, wind speed/direction, precipitation, pressure, visibility, cloud cover, sunshine duration
  - Coverage: ~100 weather stations across Denmark, Greenland, and the Faroe Islands

- **Climate Data** (`climateData`):
  - Historical climate observations and normals
  - Quality-controlled long-term datasets

- **Ocean Observations** (`oceanObs`):
  - Sea level, water temperature, wave data from coastal stations

## API Details

The API follows OGC API — Features standard:

```
GET https://dmigw.govcloud.dk/v2/metObs/collections
```
Returns two collections: `observation` and `station`.

```
GET https://dmigw.govcloud.dk/v2/metObs/collections/observation/items?api-key={key}&datetime=2026-04-06T10:00:00Z/..
```
Returns GeoJSON FeatureCollection with observation features.

```
GET https://dmigw.govcloud.dk/v2/metObs/collections/station/items?api-key={key}
```
Returns station metadata as GeoJSON features.

The API conforms to OGC standards and provides:
- Links to `service-desc` (OpenAPI 3.0 definition)
- Links to `conformance` classes
- License reference to DMI terms of use
- ISO 19139 metadata records

Probed the base URL and received valid JSON with proper OGC API structure and links.

## Freshness Assessment

- Observations are available at 10-minute resolution.
- The API supports temporal filtering via `datetime` parameter (ISO 8601 intervals).
- Data typically available within minutes of observation.
- The GeoJSON format means data is immediately usable without format conversion.

## Entity Model

- **Station**: GeoJSON Feature with station ID, location, metadata
- **Observation**: GeoJSON Feature with temporal properties, parameter values, station reference
- **Collection**: OGC API collection with links and metadata

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 10-minute observation updates |
| Openness | 2 | Free registration required for API key |
| Stability | 3 | National met institute on government cloud infrastructure |
| Structure | 3 | OGC API — Features standard, GeoJSON output, OpenAPI spec |
| Identifiers | 3 | Station IDs, OGC standard resource identifiers |
| Additive Value | 3 | Greenland and Faroe Islands coverage is unique and valuable |
| **Total** | **17/18** | |

## Notes

- One of the most standards-compliant weather APIs available — full OGC API — Features implementation.
- Greenland coverage is particularly valuable — very few open data sources for Arctic meteorology.
- The `govcloud.dk` hosting suggests stable government infrastructure.
- GeoJSON output is immediately usable in web mapping applications.
- Denmark's small size means the ~100 station network provides excellent spatial density.
- The API also covers ocean observations, which could be valuable for maritime applications.
- Metadata links to ISO 19139 records for full dataset provenance.
