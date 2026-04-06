# CAP Alerts Feed — African Weather Warnings

- **Country/Region**: Pan-African (countries with WMO-registered CAP alert feeds)
- **Endpoint**: `https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/services/CAP_Alerts_Feed/FeatureServer/0/query`
- **Protocol**: ArcGIS REST API / CAP (Common Alerting Protocol) XML
- **Auth**: None
- **Format**: JSON, GeoJSON, CAP XML
- **Freshness**: Real-time (alerts issued as conditions warrant)
- **Docs**: https://cap-sources.alerting.wmo.int/
- **Score**: 13/18

## Overview

The Common Alerting Protocol (CAP) is an ITU/WMO standard for emergency alerting.
Several African countries now publish weather warnings in CAP format, accessible through
WMO's Alert Hub and aggregated into Esri's ArcGIS Living Atlas.

African countries with registered CAP feeds include:
- **South Africa** (SAWS): Severe weather warnings
- **Kenya** (KMD): Weather alerts
- **Morocco** (DMN): Meteorological warnings
- **Egypt** (EMA): Weather warnings
- **Nigeria** (NIMET): Severe weather
- **Tanzania** (TMA): Weather warnings
- **Ghana** (GMet): Weather warnings
- **Senegal** (ANACIM): Weather alerts
- **Ethiopia** (NMA): Weather warnings

The ArcGIS CAP Alerts Feed aggregates these into a single queryable Feature Service.

## Endpoint Analysis

The CAP Alerts Feed Feature Service was discovered in the Esri Living Atlas:
```
https://services9.arcgis.com/RHVPKKiFTONKtxq3/ArcGIS/rest/services/CAP_Alerts_Feed/FeatureServer
```

Expected query for African alerts:
```
GET .../0/query?where=1%3D1
  &geometry=-20,-35,55,37
  &geometryType=esriGeometryEnvelope
  &spatialRel=esriSpatialRelIntersects
  &outFields=*&f=geojson
```

CAP alert fields:
- `identifier`: Unique alert ID
- `sender`: Issuing authority
- `sent`: Timestamp
- `status`: Actual/Exercise/System/Test
- `msgType`: Alert/Update/Cancel
- `severity`: Extreme/Severe/Moderate/Minor
- `certainty`: Observed/Likely/Possible/Unlikely
- `urgency`: Immediate/Expected/Future/Past
- `event`: Event type description
- `areaDesc`: Affected area
- `onset`, `expires`: Time window

The WMO Alert Hub at `https://cap-sources.alerting.wmo.int/` catalogues all
registered national CAP sources (connection failed during probing, but the ArcGIS
aggregation should work).

## Integration Notes

- **Unified bridge**: A single bridge polling the ArcGIS CAP Alerts Feed covers all
  African countries with registered CAP sources.
- **CAP standard**: The Common Alerting Protocol is a well-defined XML standard (OASIS
  CAP v1.2). CloudEvents mapping is straightforward.
- **Severity filtering**: Focus on Extreme and Severe alerts for operational value.
  Moderate/Minor alerts are more frequent but less actionable.
- **Language**: Alerts may be in local languages (French for Francophone Africa, Arabic
  for North Africa). Include language metadata in CloudEvents.
- **Growing coverage**: More African met services are adopting CAP. Coverage will
  improve over time as WMO pushes the standard.
- **Complement with METAR**: CAP alerts provide the "severe weather warning" layer
  while METARs provide routine observations. Together they give a complete picture.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time as conditions warrant |
| Openness | 3 | No auth, WMO/Esri public data |
| Stability | 2 | Depends on national met services issuing alerts |
| Structure | 2 | CAP XML standard, ArcGIS wrapper |
| Identifiers | 2 | CAP alert IDs, sender-assigned |
| Richness | 1 | Alert metadata but limited quantitative data |
