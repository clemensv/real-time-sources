# ICIMOD — International Centre for Integrated Mountain Development

**Country/Region**: Hindu Kush-Himalaya (HKH) — Afghanistan, Bangladesh, Bhutan, China, India, Myanmar, Nepal, Pakistan
**Publisher**: ICIMOD (International Centre for Integrated Mountain Development)
**API Endpoint**: `https://www.icimod.org/` (organizational website — no data API)
**Documentation**: https://www.icimod.org/, https://rds.icimod.org/ (Regional Database System)
**Protocol**: Web portals
**Auth**: Various (registration for data downloads)
**Data Format**: GeoTIFF, Shapefile, CSV (research datasets)
**Update Frequency**: Variable — research publications; some near-real-time fire monitoring
**License**: ICIMOD data use policy (mostly open with attribution)

## What It Provides

ICIMOD is an intergovernmental knowledge center serving the Hindu Kush-Himalaya (HKH) region — the "Third Pole" and "Water Tower of Asia." The HKH contains the largest volume of ice outside the polar regions, and its rivers supply water to 1.9 billion people.

### Key Data Products

- **Glacier monitoring**: Mass balance, retreat rates for HKH glaciers
- **Glacial Lake Inventory**: Monitoring of potentially dangerous glacial lakes (GLOF risk)
- **Forest fire monitoring**: MODIS/VIIRS-based fire detection across HKH
- **Land cover change**: Deforestation, urbanization, agricultural conversion
- **Snow cover**: Satellite-derived snow extent monitoring
- **Air quality**: Trans-Himalayan air pollution monitoring
- **Climate data**: High-altitude weather station network

### Regional Database System (RDS)

ICIMOD's RDS at `rds.icimod.org` provides downloadable datasets. However, these are primarily research datasets (periodic updates) rather than real-time feeds.

### Probe Results

The ICIMOD website at `icimod.org/mountain/` loaded successfully, showing organizational content about HKH research. No real-time data API was discovered.

## Entity Model

- **Glacier**: Named glaciers with mass balance measurements
- **Glacial Lake**: GPS-located lakes with hazard classification
- **Fire Detection**: Hotspot locations from satellite thermal anomalies
- **Snow Cover**: Grid-cell snow extent (satellite-derived)
- **Weather Station**: High-altitude automatic weather stations

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Research datasets; some near-real-time fire detection via satellite |
| Openness | 2 | Many datasets freely available; registration required for downloads |
| Stability | 2 | Established intergovernmental institution (since 1983); 8 member countries |
| Structure | 1 | Research formats (GeoTIFF, Shapefile); no REST API |
| Identifiers | 1 | Glacier names; station IDs for weather stations |
| Additive Value | 3 | Unique: Third Pole glacier monitoring; 1.9B people depend on HKH water; GLOF risk |
| **Total** | **10/18** | |

## Integration Notes

- ICIMOD data is primarily research-grade rather than real-time operational data
- The GLOF (Glacial Lake Outburst Flood) risk monitoring component has the most real-time potential
- Fire detection via MODIS/VIIRS can be accessed through NASA FIRMS (already in candidate pool)
- Nepal's BIPAD portal provides operational real-time hydrology that complements ICIMOD research
- ICIMOD's member countries overlap with RIMES members — coordination opportunities
- The "Third Pole" framing makes this scientifically unique — no other data source covers Himalayan glaciology

## Verdict

Research institution rather than operational data source. ICIMOD provides valuable but primarily periodic research datasets about one of the most climate-sensitive regions on Earth. For real-time operational data, the Nepal BIPAD portal is a better entry point for HKH hydrological monitoring. ICIMOD's GLOF risk assessments and glacier inventories are unique but not real-time API-compatible.
