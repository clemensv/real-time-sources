# Digital Earth Australia Hotspots (DEA Hotspots)

**Country/Region**: Australia
**Publisher**: Geoscience Australia (GA) / Digital Earth Australia
**API Endpoint**: `https://hotspots.dea.ga.gov.au/geoserver/public/wfs`
**Documentation**: https://hotspots.dea.ga.gov.au/
**Protocol**: OGC WFS 1.1.0
**Auth**: None
**Data Format**: GML, GeoJSON (application/json), CSV, KML, Shapefile
**Update Frequency**: Multiple times daily (each satellite pass)
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

## What It Provides

DEA Hotspots is Australia's national bushfire monitoring system — part of the Sentinel program. It provides satellite-detected thermal anomaly ("hotspot") data compiled from multiple satellite instruments:

- **MODIS** (Aqua/Terra)
- **VIIRS** (Suomi-NPP, NOAA-20)
- Processed with algorithms to detect areas of unusually high temperature

The system serves emergency service managers and critical infrastructure providers across Australia. Data is split into public and secure (authorized users only) tiers.

## API Details

Standard OGC WFS interface via GeoServer:

**GetCapabilities:**
```
https://hotspots.dea.ga.gov.au/geoserver/public/wfs?service=WFS&version=1.1.0&request=GetCapabilities
```

**Available Feature Types:**
- `public:hotspots` — All hotspot detections
- `public:hotspots_three_days` — Hotspots from last 3 days
- `public:satellite_pass_last_hotspot` — Most recent satellite pass data
- `public:satellite_pass_next_hotspot` — Next expected pass
- `public:multi_station_satellite_pass_last_hotspot` — Multi-station recent pass

**Query hotspots (GeoJSON):**
```
https://hotspots.dea.ga.gov.au/geoserver/public/wfs?service=WFS&version=1.1.0&request=GetFeature&typeName=public:hotspots_three_days&outputFormat=application/json&maxFeatures=100
```

**Supported output formats:** GML 3.1.1, GML2, KML, Shapefile (SHAPE-ZIP), GeoJSON (application/json), CSV.

Supports CQL_FILTER for spatial and attribute queries.

## Freshness Assessment

Good. Updated with each satellite pass over Australia — typically several times daily. MODIS provides ~4 passes/day, VIIRS adds additional coverage. The `hotspots_three_days` layer provides a rolling 72-hour window. Satellite pass timing metadata is also available.

## Entity Model

Hotspot features include:
- Geometry (point — latitude/longitude)
- Satellite identifier and sensor
- Detection datetime
- Brightness temperature
- Fire Radiative Power (FRP)
- Confidence level
- Satellite pass information
- Processing station

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Per-satellite-pass updates, several times daily |
| Openness | 3 | CC BY 4.0, no auth required |
| Stability | 3 | Australian government Geoscience Australia service |
| Structure | 3 | Standard WFS, multiple output formats including JSON |
| Identifiers | 1 | Point detections without persistent fire IDs |
| Additive Value | 2 | Australia-focused, regional value |
| **Total** | **14/18** | |

## Notes

- The WFS endpoint was slow/timing out during testing. May need generous timeouts for large queries.
- Use `hotspots_three_days` instead of `hotspots` for manageable response sizes.
- The satellite pass layers are a nice touch — showing when the last data arrived and when the next pass is expected.
- Coordinate reference system: EPSG:4326 (WGS 84).
- For Australia-specific fire monitoring, this is the authoritative national source.
- Consider as a complement to FIRMS for Australian emergency services integration.
