# GeoSphere Austria Data Hub

**Country/Region**: Austria
**Publisher**: GeoSphere Austria (formerly ZAMG + GBA)
**API Endpoint**: `https://dataset.api.hub.geosphere.at/v1/datasets`
**Documentation**: https://data.hub.geosphere.at/
**Protocol**: REST
**Auth**: None (open access)
**Data Format**: GeoJSON, CSV, NetCDF
**Update Frequency**: 10 minutes (meteorological), varies by dataset
**Station Count**: ~260 meteorological stations
**License**: CC BY 4.0

## What It Provides

GeoSphere Austria operates the Austrian national meteorological network. The Data Hub provides an excellent REST API with 96 datasets. However, **these are meteorological datasets, not hydrological**:
- 10-minute, hourly, daily, monthly, annual climate observations
- INCA nowcasting (precipitation, temperature, wind)
- AROME NWP model forecasts
- SNOWGRID snow cover analysis
- WINFORE water balance indices (SPEI)

### Not a hydrology API
Austria's actual hydrological data (water levels, river discharge) is managed by eHYD (ehyd.gv.at), which remains an SPA-only portal with no public API. GeoSphere's datasets cover precipitation and evapotranspiration (inputs to the water cycle) but not river gauge readings.

## API Details

### Dataset catalogue (confirmed working)
```
GET https://dataset.api.hub.geosphere.at/v1/datasets
```
Returns JSON dictionary of all datasets with type, mode, response_formats, and URL.

### Station data access pattern
```
GET https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1h?parameters={param}&station_ids={id}&output_format=geojson
```

### Available dataset types
- `station/historical/klima-v2-10min` — 10-minute observations
- `station/historical/klima-v2-1h` — hourly climate data
- `grid/forecast/nwp-v1-1h-2500m` — NWP model output
- `grid/historical/snowgrid_cl-v2-1d-1km` — snow cover analysis
- `grid/historical/winfore-v2-1d-1km` — water balance (SPEI)

### Response formats
- GeoJSON (station data)
- NetCDF (grid data)
- CSV (timeseries data)

## Freshness Assessment

- 10-minute station updates confirmed
- API infrastructure is modern and well-maintained (DOI-registered datasets)
- Quality flags available for all parameters
- Data from 1992 to present

## Entity Model

- **Station**: id, name, lat/lon, elevation, parameters
- **Parameter**: code, name, unit, quality flag
- **Dataset**: type (station/grid/timeseries), mode (historical/forecast), resolution

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 3 | Excellent REST API, JSON catalogue, GeoJSON/CSV/NetCDF output |
| Data Richness | 1 | Meteorological only — no water levels or discharge |
| Freshness | 3 | 10-minute updates |
| Station Coverage | 2 | ~260 stations across Austria |
| Documentation | 3 | Well-documented with DOIs, descriptions, quality flags |
| License/Access | 3 | CC BY 4.0, no auth required |
| **Total** | **15/18** | |

## Notes

- Excellent API architecture but wrong domain — meteorological, not hydrological
- The WINFORE/SPEI dataset provides water balance indices that are hydrology-adjacent
- Precipitation data from this API could complement any future eHYD integration
- eHYD (the actual Austrian hydrology portal) remains API-less
- Consider as a meteorological data source that supports hydrological analysis
- The API design is exemplary and could serve as a reference implementation
- Austria's actual water level data remains one of the most frustrating gaps in European coverage
