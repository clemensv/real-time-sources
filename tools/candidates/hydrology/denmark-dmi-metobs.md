# Denmark DMI Meteorological Observations API

**Country/Region**: Denmark
**Publisher**: Danmarks Meteorologiske Institut (DMI) — Danish Meteorological Institute
**API Endpoint**: `https://dmigw.govcloud.dk/v2/metObs/collections`
**Documentation**: https://opendatadocs.dmi.govcloud.dk/
**Protocol**: REST (OGC API Features-style)
**Auth**: API key required (free registration)
**Data Format**: GeoJSON
**Update Frequency**: 10-minute observations
**Station Count**: ~80 meteorological stations
**License**: Open Government Licence Denmark

## What It Provides

Meteorological observations from the Danish weather station network. While primarily a weather API, this is included in the hydrology context because:
- it was an early Denmark fallback before a dedicated hydrometry API was found in [denmark-vandah.md](denmark-vandah.md)
- water level parameters may exist within the meteorological observation set (coastal stations)
- the API pattern (OGC API Features) is still useful as adjacent Danish environmental infrastructure

The API provides two collections:
- `observation` — actual measurements
- `station` — station metadata

## API Details

### Collections listing (no auth)
```
GET https://dmigw.govcloud.dk/v2/metObs/collections
```
Returns JSON with available collections and their links.

### Observations (API key required)
```
GET https://dmigw.govcloud.dk/v2/metObs/collections/observation/items?api-key={key}&limit=10
```
Returns GeoJSON FeatureCollection with observation data.

### Stations (API key required)
```
GET https://dmigw.govcloud.dk/v2/metObs/collections/station/items?api-key={key}&limit=10
```

### Authentication
- Register at https://confluence.govcloud.dk/pages/viewpage.action?pageId=26476690
- Obtain free API key
- Pass as query parameter `api-key={key}`

### Related API
DMI also provides `oceanObs` for ocean/coastal observations:
```
GET https://dmigw.govcloud.dk/v2/oceanObs/collections
```
This may include coastal water levels (tide gauges).

## Freshness Assessment

- Meteorological data is updated every 10 minutes
- API is well-maintained and actively developed by DMI
- Collection endpoints respond without auth; actual data requires API key
- The API returned HTTP 400 when probed without a valid key, confirming auth enforcement

## Entity Model

- **Station**: id, name, coordinates, parameters measured, operational status
- **Observation**: timestamp, parameterId, value, stationId
- Standard meteorological parameters (temperature, wind, pressure, precipitation)
- Potential water level parameters for coastal stations (not confirmed)

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 3 | OGC API Features, GeoJSON, well-designed REST endpoints |
| Data Richness | 1 | Primarily meteorological; hydrology-specific parameters not confirmed |
| Freshness | 3 | 10-minute updates |
| Station Coverage | 2 | ~80 stations across Denmark |
| Documentation | 3 | Excellent documentation at opendatadocs.dmi.govcloud.dk |
| License/Access | 2 | Free API key required; open government licence |
| **Total** | **14/18** | |

## Notes

- This is primarily a meteorological API, not a dedicated hydrology API
- Denmark now also has a dedicated hydrometry candidate in [denmark-vandah.md](denmark-vandah.md)
- The `oceanObs` collection at DMI may provide coastal water levels (tide gauge data)
- Denmark's flat terrain and extensive drainage network make water level data particularly relevant
- The API architecture is exemplary — OGC API Features with GeoJSON — and could serve as a template
- Danish environmental authorities (SDFI, Miljøstyrelsen) may have separate hydrology data not discovered here
- The DMI API gateway (dmigw.govcloud.dk) hosts multiple service APIs under the same infrastructure
- Free API key registration is straightforward
