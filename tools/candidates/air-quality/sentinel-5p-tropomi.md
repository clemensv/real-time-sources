# Sentinel-5P TROPOMI (Satellite Atmospheric Composition)

**Country/Region**: Global
**Publisher**: ESA (European Space Agency) / Copernicus
**API Endpoint**: `https://dataspace.copernicus.eu/` (Copernicus Data Space Ecosystem)
**Documentation**: https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-5p
**Protocol**: OData REST API / OpenSearch
**Auth**: Free registration required (Copernicus Data Space account)
**Data Format**: NetCDF (L2 products)
**Update Frequency**: Daily (14 orbits/day, ~daily global coverage)
**License**: Copernicus Sentinel Data Licence (free, open)

## What It Provides

Sentinel-5P carries the TROPOMI instrument, the most advanced satellite spectrometer for atmospheric trace gas monitoring. It provides near-real-time global maps of key air quality indicators: tropospheric NO₂, O₃ (total and tropospheric), SO₂, CO, CH₄ (methane), HCHO (formaldehyde), and aerosol properties. With a spatial resolution of 5.5 × 3.5 km (upgraded from 7 × 3.5 km), TROPOMI resolves individual cities, industrial complexes, and ship tracks. Products are available within 3 hours of measurement (near-real-time) or 5 days (offline, higher quality).

## API Details

- **Primary Access**: Copernicus Data Space Ecosystem — `https://dataspace.copernicus.eu/`
- **Search API**: OData catalog API for product discovery with spatial/temporal filters
- **Download**: Direct HTTPS download of NetCDF files
- **Key Products (L2)**:
  - `L2__NO2___` — Tropospheric NO₂ column density
  - `L2__O3____` — Total ozone column
  - `L2__O3_TCL` — Tropospheric ozone column
  - `L2__SO2___` — SO₂ column density
  - `L2__CO____` — CO total column
  - `L2__CH4___` — Methane total column
  - `L2__HCHO__` — Formaldehyde total column
  - `L2__AER_AI` — UV Aerosol Index
  - `L2__AER_LH` — Aerosol Layer Height
  - `L2__CLOUD_` — Cloud properties
- **Timeliness**: NRTI (Near-Real-Time, <3 hours), OFFL (Offline, ~5 days), RPRO (Reprocessed)
- **Spatial Coverage**: Global, 14 orbits/day, daily revisit at equator
- **Resolution**: 5.5 × 3.5 km (7 × 3.5 km for some products)

## Freshness Assessment

Near-real-time (NRTI) products are available within 3 hours of satellite overpass. Each point on Earth is covered approximately daily. The satellite overpass time is local solar noon (ascending node ~13:30 local time). Offline (OFFL) products with better calibration are available within ~5 days.

## Entity Model

- **Product** → product type (L2__NO2___, etc.), processing level, timeliness tier
- **Granule** → individual orbit file, with start/end times, spatial footprint
- **Pixel** → individual measurement at 5.5 × 3.5 km resolution with lat/lon, value, quality flag
- **Orbit** → 14 per day, each covering a swath of ~2600 km width

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | NRTI within 3h; daily revisit; but single overpass per day |
| Openness | 2 | Free but registration required; large data volumes |
| Stability | 3 | ESA/Copernicus flagship mission; operational since 2017 |
| Structure | 1 | NetCDF files with complex geolocation grids; not simple JSON |
| Identifiers | 2 | Standard product type codes; orbit/granule numbering |
| Additive Value | 3 | Global coverage where no ground stations exist; unique trace gas products (CH₄, HCHO) |
| **Total** | **13/18** | |

## Notes

- TROPOMI is the gold standard for satellite air quality: it resolves individual cities and has products for gases that ground networks rarely measure (HCHO, CH₄).
- Data volume is large: a single orbit's L2 NO₂ file is ~200 MB. Processing requires scientific Python libraries (xarray, netCDF4, cartopy).
- The satellite passes any given location approximately once per day around local noon — this is a snapshot, not continuous monitoring.
- Cloud cover blocks measurements: TROPOMI can only measure in clear-sky or thin-cloud conditions. Cloudy regions have data gaps.
- Ideal for: pollution trend analysis, industrial emission monitoring, wildfire plume tracking, methane leak detection, and areas with no ground monitoring.
- The old Sentinel-5P Hub (s5phub.copernicus.eu) is being deprecated in favor of the Copernicus Data Space Ecosystem.
- Google Earth Engine also provides Sentinel-5P data for cloud-based analysis without downloading files.
