# EUMETSAT Data Services

**Country/Region**: Europe and global (via geostationary and polar-orbiting satellites)
**Publisher**: EUMETSAT (European Organisation for the Exploitation of Meteorological Satellites)
**API Endpoint**: `https://data.eumetsat.int/` (Data Store), various product-specific APIs
**Documentation**: https://data.eumetsat.int/data/map, https://user.eumetsat.int/resources/user-guides
**Protocol**: HTTPS file download, OGC WMS/WCS, EUMETView
**Auth**: Registration required (free for most products)
**Data Format**: NetCDF, HDF5, BUFR, GRIB, GeoTIFF, PNG
**Update Frequency**: 5–15 minutes (Meteosat rapid scan), 1 hour (full disk), near-real-time
**License**: EUMETSAT Data Policy — free for most users, some restrictions on redistribution

## What It Provides

EUMETSAT operates Europe's meteorological satellites and distributes data from several satellite programs:

- **Meteosat (MSG/MTG)**: Geostationary satellites over Europe/Africa. The Spinning Enhanced Visible and InfraRed Imager (SEVIRI) provides 12-channel imagery every 15 minutes (full disk) or 5 minutes (rapid scan over Europe). The new Meteosat Third Generation (MTG) provides even higher resolution and new capabilities.

- **Metop**: Polar-orbiting satellites providing global coverage. Instruments include:
  - IASI (Infrared Atmospheric Sounding Interferometer): Temperature/humidity profiles
  - AVHRR: Land/sea surface temperature, vegetation indices
  - GOME-2: Ozone and atmospheric composition
  - ASCAT: Ocean surface wind vectors

- **Sentinel-3 (marine)**: Sea surface temperature, ocean color (shared with Copernicus).

- **Sentinel-6**: Radar altimetry for sea level monitoring.

- **Jason-CS**: Ocean topography.

- **Derived Products**: Cloud masks, precipitation estimates, atmospheric motion vectors, fire monitoring, dust/volcanic ash tracking.

## API Details

Data access through multiple channels:

1. **EUMETSAT Data Store** (data.eumetsat.int): Web interface and API for browsing and downloading products. Supports search by satellite, product type, time range, and geographic area.

2. **EUMETCast**: Broadcast-based (DVB-S2) data dissemination system — satellite broadcast to receiving stations.

3. **Data Tailor**: Web service for subsetting and reformatting products.

4. **OGC Services**: WMS/WCS for some products.

5. **EUMETView**: Web-based visualization tool.

Registration at user.eumetsat.int is required. Most data is free for research and operational meteorological use. Some restrictions apply to commercial redistribution.

## Freshness Assessment

- Meteosat SEVIRI: New image every 15 minutes (full disk), 5 minutes (rapid scan).
- Metop: Multiple orbits daily, providing global coverage with ~12-hour revisit.
- Products derived from satellite data are available within 30–60 minutes of acquisition.
- MTG (new generation) provides enhanced temporal and spatial resolution.

## Entity Model

- **Product**: Hierarchical product catalog (satellite → instrument → product level → specific product).
- **Collection**: Time series of a specific product type.
- **Granule**: Individual file/scene for a specific time and area.
- **Satellite**: MSG-1 through MSG-4, Metop-A/B/C, Sentinel-3A/B, MTG-I1, etc.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute rapid scan, 15-minute full disk, near-real-time products |
| Openness | 2 | Free registration, but not fully open — some products restricted |
| Stability | 3 | Intergovernmental organization, multi-billion € satellite programs |
| Structure | 1 | Complex satellite data formats (NetCDF, HDF5, BUFR), specialized tools needed |
| Identifiers | 2 | Product catalog IDs, satellite names, orbit/scene identifiers |
| Additive Value | 3 | Unique satellite-derived products, hemispheric coverage, volcanic ash tracking |
| **Total** | **14/18** | |

## Notes

- EUMETSAT is to European weather satellites what NASA is to American ones — the data is authoritative and irreplaceable.
- The data formats (NetCDF, HDF5, GRIB, BUFR) require specialized libraries and domain expertise.
- Meteosat imagery is the backbone of European weather forecasting — every TV weather map of Europe uses Meteosat data.
- The volcanic ash and dust tracking products are uniquely valuable for aviation safety.
- Fire radiative power products are important for wildfire monitoring.
- ASCAT ocean wind data is the primary source for sea surface wind measurements globally.
- Integration complexity is high — this is satellite data, not station observations. Consider using derived products (cloud masks, precipitation estimates) rather than raw imagery.
- The new MTG satellites (launched 2022+) significantly upgrade European weather monitoring capabilities with the Flexible Combined Imager (FCI) and Lightning Imager.
