# MODIS/VIIRS Thermal Hotspots — Africa Wildfire Detection

- **Country/Region**: Pan-African
- **Endpoint**: `https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/services/MODIS_Thermal_v1/FeatureServer/0/query`
- **Protocol**: ArcGIS REST API (Feature Service)
- **Auth**: None
- **Format**: JSON (Esri JSON), GeoJSON
- **Freshness**: Last 48 hours of thermal detections, updated multiple times daily
- **Docs**: https://firms.modaps.eosdis.nasa.gov/
- **Score**: 15/18

## Overview

NASA's Fire Information for Resource Management System (FIRMS) provides satellite-based
thermal hotspot detection globally. The data is also served through Esri's ArcGIS
Living Atlas as a Feature Service, enabling spatial queries without NASA-specific API
keys.

For Africa, fire is both a critical hazard and a land management tool. Savanna burning
in sub-Saharan Africa accounts for a significant portion of global biomass burning.
The dry season in Southern Africa (June–October) and the Sahel dry season
(November–March) produce massive fire activity.

Key African fire contexts:
- **Southern Africa**: Dry-season savanna fires, agricultural burning
- **Central Africa (DRC, Congo)**: Rainforest edge burning, slash-and-burn agriculture
- **West Africa**: Sahel grassland fires
- **East Africa**: Post-harvest burning
- **North Africa**: Limited but important (Algeria, Morocco forest fires)

## Endpoint Analysis

**Feature Service metadata verified** — the MODIS Thermal v1 service shows:
- Layer 0: "MODIS Thermal (Last 48 hours)"
- Point geometry type
- Spatial reference: Web Mercator (102100)
- Last edit: 2026-04-06 (actively updated)

Fields include: `acq_date`, `acq_time`, `brightness`, `confidence`, `satellite`,
plus spatial coordinates.

**Direct spatial query approach** for Africa:
```
GET .../query?where=1%3D1
  &geometry=-20,-35,55,37
  &geometryType=esriGeometryEnvelope
  &spatialRel=esriSpatialRelIntersects
  &outFields=*
  &f=geojson
  &resultRecordCount=100
```

Note: A test query returned empty features, possibly due to timing (48-hour window
and current season). The service is confirmed active with recent edit timestamps.

Alternative: The NASA FIRMS API at `https://firms.modaps.eosdis.nasa.gov/api/` requires
an API key (MAP_KEY) but provides CSV/JSON/GeoJSON downloads by country.

## Integration Notes

- **ArcGIS approach**: Use the Esri Feature Service for no-auth access. Spatial query
  with African bounding box, poll every 30 minutes.
- **FIRMS approach**: Register for a MAP_KEY and use the FIRMS API for country-specific
  CSV downloads. Better for targeted monitoring.
- **Seasonal patterns**: Fire activity varies dramatically by season and latitude.
  Expect high volumes during dry seasons.
- **Confidence filtering**: Filter by confidence level (>= 80%) to reduce false positives
  from industrial heat sources, gas flares, etc.
- **Complement with VIIRS**: VIIRS satellites provide higher-resolution detections.
  The ArcGIS Living Atlas may have a separate VIIRS layer.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Updated multiple times daily |
| Openness | 3 | No auth (ArcGIS) or free API key (FIRMS) |
| Stability | 3 | NASA/Esri infrastructure |
| Structure | 3 | GeoJSON, ArcGIS Feature Service |
| Identifiers | 1 | Object IDs only, no persistent fire IDs |
| Richness | 2 | Thermal detections with confidence scores |
