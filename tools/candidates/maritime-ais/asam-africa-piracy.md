# ASAM — Anti-Shipping Activity Messages (African Waters)

- **Country/Region**: Pan-African maritime (Gulf of Guinea, Horn of Africa/Gulf of Aden, Mozambique Channel, Red Sea)
- **Endpoint**: `https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/services/ASAM_events_V1/FeatureServer/0/query`
- **Protocol**: ArcGIS REST API
- **Auth**: None
- **Format**: JSON, GeoJSON
- **Freshness**: Updated as reports come in (near real-time during active incidents)
- **Docs**: https://msi.nga.mil/Piracy
- **Score**: 14/18

## Overview

The National Geospatial-Intelligence Agency (NGA) publishes Anti-Shipping Activity
Messages (ASAM) documenting piracy, armed robbery, and suspicious approaches against
vessels worldwide. African waters are among the most dangerous:

- **Gulf of Guinea** (Nigeria, Ghana, Cameroon, Togo, Benin): The world's piracy
  hotspot — armed robbery, cargo theft, crew kidnapping
- **Horn of Africa/Gulf of Aden** (Somalia, Djibouti): Somali piracy — declined since
  2012 but still monitored
- **Mozambique Channel**: Emerging piracy linked to the Cabo Delgado insurgency
- **Red Sea/Gulf of Aden**: Houthi attacks on shipping (2023-present)

This data is directly relevant to maritime AIS tracking and African port operations.

## Endpoint Analysis

The ASAM Feature Service was discovered in the Esri ArcGIS Living Atlas:
```
https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/services/ASAM_events_V1/FeatureServer
```

Query for African waters (Gulf of Guinea example):
```
GET .../0/query?where=1%3D1
  &geometry=-5,-10,15,10
  &geometryType=esriGeometryEnvelope
  &spatialRel=esriSpatialRelIntersects
  &outFields=*&f=geojson
  &resultRecordCount=10
  &orderByFields=DateOfOccurrence+DESC
```

Expected fields: DateOfOccurrence, Latitude, Longitude, NavArea, SubRegion,
Description, Reference, Aggressor, Victim, HostilityType.

## Integration Notes

- **Spatial filtering**: Define African maritime zones (Gulf of Guinea, Horn of Africa,
  Mozambique Channel) and query each separately for focused monitoring.
- **Complement with AIS**: Pair ASAM events with AIS vessel tracking data from the
  existing `kystverket-ais` bridge or AISHub — match piracy events to vessel positions.
- **Incident enrichment**: The Description field contains narrative details (vessel type,
  attacker methods, response). Parse for structured metadata.
- **Historical context**: ASAM includes historical data going back decades. Use for
  spatial pattern analysis of African maritime security.
- **IMB Piracy Reporting Centre**: The ICC International Maritime Bureau also publishes
  piracy reports but without a public API.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Updated per incident |
| Openness | 3 | No auth, US government data |
| Stability | 3 | NGA operational system |
| Structure | 3 | ArcGIS Feature Service, GeoJSON |
| Identifiers | 1 | ASAM reference numbers |
| Richness | 2 | Incident details, location, vessel info |
