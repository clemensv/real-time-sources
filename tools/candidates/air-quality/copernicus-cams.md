# Copernicus Atmosphere Monitoring Service (CAMS)

**Country/Region**: Global / European
**Publisher**: ECMWF (European Centre for Medium-Range Weather Forecasts) for Copernicus/EU
**API Endpoint**: `https://ads.atmosphere.copernicus.eu/api`
**Documentation**: https://ads.atmosphere.copernicus.eu/how-to-api
**Protocol**: REST (CDS API)
**Auth**: Personal Access Token (free registration required)
**Data Format**: GRIB, NetCDF
**Update Frequency**: Daily forecasts; 6-hourly analysis; monthly reanalysis
**License**: Copernicus Licence (free, open, with attribution)

## What It Provides

CAMS is the atmospheric composition component of the EU's Copernicus Earth observation programme. It provides global and European air quality forecasts, near-real-time analyses, and reanalysis datasets. Products include PM10, PM2.5, O₃, NO₂, SO₂, CO, aerosol optical depth, UV index, pollen forecasts, greenhouse gases (CO₂, CH₄), and fire emissions. CAMS data fills the gap between ground-station measurements and satellite observations — it provides modelled, gridded air quality data covering the entire globe.

## API Details

- **Base URL**: `https://ads.atmosphere.copernicus.eu/api`
- **Access Method**: Python `cdsapi` library (preferred) or REST endpoints via `ecmwf-datastores-client`
- **Key Datasets**:
  - `cams-global-atmospheric-composition-forecasts` — global 5-day AQ forecasts (0.4° grid)
  - `cams-europe-air-quality-forecasts` — European high-resolution AQ forecasts (0.1° grid)
  - `cams-global-reanalysis-eac4` — global reanalysis (2003-present)
  - `cams-europe-air-quality-reanalyses` — European AQ reanalysis
  - `cams-global-radiative-forcings` — greenhouse gas forcing
  - `cams-solar-radiation-timeseries` — solar radiation
- **Request Pattern**: Dataset name + selection dict (variable, date, time, area, format) → download file
- **Output Formats**: GRIB2, NetCDF
- **Terms**: Must agree to dataset-specific Terms of Use before first download

## Freshness Assessment

Global forecasts are produced twice daily (00Z and 12Z) with 5-day lead time. European forecasts update daily with 4-day lead time at higher resolution. Near-real-time analysis products are available within hours. Reanalysis products are updated monthly with a ~2-month lag. This is not real-time station data — it's modelled gridded output.

## Entity Model

- **Dataset** → collection of variables at a given resolution and time range
- **Variable** → atmospheric constituent (pm2p5, pm10, go3, no2, so2, co, aod550, etc.)
- **Grid** → spatial resolution (0.4° global, 0.1° European)
- **Time** → forecast base time + step, or analysis time
- **Level** → surface, pressure levels, model levels

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily/6-hourly forecasts; not real-time station data |
| Openness | 2 | Free but requires registration + token; Terms per dataset |
| Stability | 3 | EU/ECMWF backed; core Copernicus service |
| Structure | 1 | GRIB/NetCDF require scientific data libraries (not simple JSON) |
| Identifiers | 2 | Grid-based; dataset/variable naming is standardised |
| Additive Value | 3 | Global gridded AQ forecasts — unique; fills gaps where no stations exist |
| **Total** | **13/18** | |

## Notes

- CAMS is fundamentally different from station-based APIs: it provides modelled, gridded data covering every point on Earth, not just where monitors are deployed.
- Output formats (GRIB, NetCDF) require scientific libraries (xarray, cfgrib, eccodes) to process — not a simple REST-to-JSON workflow.
- The Python `cdsapi` library is the standard access method. The newer `ecmwf-datastores-client` package supports async requests and REST API.
- CAMS European AQ forecasts at 0.1° (~10 km) resolution are among the highest-resolution operational AQ forecasts globally.
- Includes pollen forecasts (birch, grass, olive, ragweed, alder) — a unique product not available from station networks.
- Data can be subset by geographic area, reducing download sizes significantly.
- Ideal as a complement to ground-station networks: CAMS provides the background field, stations provide ground truth.
