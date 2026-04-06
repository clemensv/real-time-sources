# Copernicus Marine Service — Water Quality Products

**Country/Region**: Global (focus on European seas; global ocean color products)
**Publisher**: Copernicus Marine Environment Monitoring Service (CMEMS), operated by Mercator Ocean International
**API Endpoint**: `https://data.marine.copernicus.eu/api/` (Marine Data Store API)
**Documentation**: https://marine.copernicus.eu/access-data ; https://help.marine.copernicus.eu/en/collections/9080063
**Protocol**: REST API + OPeNDAP + WMTS
**Auth**: Free registration required (Copernicus Marine account)
**Data Format**: NetCDF, GeoTIFF, JSON (API metadata), Zarr
**Update Frequency**: Daily to weekly (satellite products); near-real-time (model outputs)
**License**: Copernicus data policy (free and open, attribution required)

## What It Provides

Copernicus Marine Service provides satellite-derived and model-based ocean water quality products covering:

### Satellite Ocean Color Products
- **Chlorophyll-a concentration** — phytoplankton biomass indicator
- **Total Suspended Matter (TSM)** — turbidity proxy
- **Colored Dissolved Organic Matter (CDOM)** / diffuse attenuation
- **Phytoplankton functional types**
- **Ocean transparency** (Secchi disk depth equivalent)

### Model-Based Biogeochemistry
- **Dissolved oxygen** profiles
- **Nutrient concentrations** (nitrate, phosphate, silicate)
- **Primary productivity** estimates
- **pH and carbonate system** (ocean acidification)

### Harmful Algal Bloom (HAB) Products
- **HAB indicators** derived from satellite ocean color
- **Anomaly detection** for unusual phytoplankton blooms

Coverage: global ocean color at ~1 km resolution (daily composites); European regional models (Atlantic, Baltic, Mediterranean, Black Sea) at higher resolution.

## API Details

The Marine Data Store (MDS) API:

```python
# Python client (copernicusmarine package)
import copernicusmarine

# Download a subset
copernicusmarine.subset(
    dataset_id="cmems_obs-oc_glo_bgc-plankton_nrt_l4-gapfree-multi-4km_P1D",
    variables=["CHL"],
    minimum_longitude=-10, maximum_longitude=30,
    minimum_latitude=35, maximum_latitude=60,
    start_datetime="2025-01-01", end_datetime="2025-01-07"
)

# REST API for catalog
GET https://data.marine.copernicus.eu/api/datasets?q=chlorophyll
```

Also accessible via:
- **OPeNDAP**: Direct remote data access from Python/R/Matlab
- **WMTS**: Map tiles for visualization
- **FTP**: Bulk file downloads

The `copernicusmarine` Python package (pip installable) is the recommended programmatic access method.

## Freshness Assessment

Good. Near-Real-Time (NRT) satellite products are available within 24 hours of satellite pass. Multi-year reprocessed archives provide consistent historical baselines. Model forecasts extend days ahead for European seas. This is satellite/model data, not in-situ measurements — different use case from station-based monitoring.

## Entity Model

- **Product**: productId, title, description, processing level, temporal/spatial resolution
- **Dataset**: datasetId, variables, time range, geographic extent, file format
- **Variable**: name, standard_name (CF), units, long_name
- **Grid Cell**: latitude, longitude, time, depth, value, quality flag

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily satellite composites; NRT within 24h; model forecasts |
| Openness | 2 | Free but requires registration |
| Stability | 3 | EU Copernicus program; multi-billion euro infrastructure |
| Structure | 3 | REST API, OPeNDAP, WMTS; Python client; NetCDF/Zarr |
| Identifiers | 3 | Standard product/dataset IDs; CF variable names; DOIs |
| Additive Value | 3 | Global satellite coverage; HAB detection; ocean acidification; model forecasts |
| **Total** | **16/18** | |

## Notes

- Copernicus Marine is fundamentally different from in-situ monitoring — it provides spatially continuous satellite/model data rather than point measurements. This is complementary, not competitive, with station-based water quality data.
- The HAB (Harmful Algal Bloom) detection capability is particularly valuable — satellite is the only way to monitor bloom extent over large areas.
- Ocean acidification (pH) products are unique to model-based approaches — not measurable from satellites.
- The `copernicusmarine` Python package simplifies access enormously compared to raw API calls.
- European regional products (Baltic, Mediterranean) have higher resolution and more variables than global products.
- Copernicus is funded through 2027+ with EU commitment — among the most stable scientific data programs in the world.
- For drinking/recreational water quality, this is not the right source. For coastal/ocean ecological water quality (eutrophication, HABs, turbidity plumes), it's unmatched.
