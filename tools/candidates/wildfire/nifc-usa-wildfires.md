# NIFC USA Wildfires (National Interagency Fire Center)

**Country/Region**: United States
**Publisher**: National Interagency Fire Center (NIFC) via ArcGIS Online
**API Endpoint**: `https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/USA_Wildfires_v1/FeatureServer/0/query`
**Documentation**: https://data-nifc.opendata.arcgis.com/
**Protocol**: ArcGIS REST API (Feature Service)
**Auth**: None
**Data Format**: JSON (Esri JSON), GeoJSON
**Update Frequency**: Near real-time (updated as incident reports come in, typically multiple times daily)
**License**: US Government public domain

## What It Provides

The NIFC open data hub provides authoritative US wildfire incident data through ArcGIS Feature Services. The primary service `USA_Wildfires_v1` contains two layers:

- **Layer 0: Current_Incidents** — Point locations of active fire incidents with rich metadata
- **Layer 1: Current_Perimeters** — Polygon boundaries of active fire perimeters

This is the official US interagency fire incident data, sourced from the IRWIN (Integrated Reporting of Wildland-Fire Information) system.

## API Details

Standard ArcGIS Feature Service query API:

**Query active incidents:**
```
GET https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/USA_Wildfires_v1/FeatureServer/0/query?where=1%3D1&outFields=*&f=json&resultRecordCount=100
```

**Query with spatial filter:**
```
GET .../query?where=POOState='US-CA'&outFields=*&f=geojson
```

**Query perimeters:**
```
GET .../FeatureServer/1/query?where=1%3D1&outFields=*&f=geojson
```

Supports: `where` clauses, spatial queries, `outFields`, `resultRecordCount`, `orderByFields`, `returnGeometry`, GeoJSON output (`f=geojson`).

Max record count: 18,000 per request.

## Freshness Assessment

Good. Data is updated as incident management teams submit reports through IRWIN. Major incidents typically updated multiple times daily. The `ModifiedOnDateTime` field indicates last update. Some smaller incidents may have delays of 1-2 days.

## Entity Model

Each incident record includes:
- `OBJECTID` — Record ID
- `IrwinID` / `GlobalID` — Persistent unique identifier (GUID)
- `UniqueFireIdentifier` — Formatted fire ID (e.g., `2025-IDBOF-000208`)
- `IncidentName` — Fire name
- `IncidentTypeCategory` — WF (wildfire), RX (prescribed), etc.
- `FireDiscoveryDateTime` — When fire was discovered
- `DailyAcres`, `CalculatedAcres`, `FinalAcres` — Size estimates
- `PercentContained` — Containment status
- `POOState`, `POOCounty` — Point of origin location
- `FireCause`, `FireCauseGeneral` — Cause classification
- `GACC` — Geographic Area Coordination Center
- `TotalIncidentPersonnel`, `Injuries`, `Fatalities`
- `ResidencesDestroyed`, `OtherStructuresDestroyed`
- `FireMgmtComplexity` — Incident complexity level
- `PredominantFuelGroup`, `PredominantFuelModel`
- `ContainmentDateTime`, `ControlDateTime`, `FireOutDateTime`
- Point geometry (lon/lat)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Updated multiple times daily, but not streaming |
| Openness | 3 | No auth, public domain |
| Stability | 3 | Official US government service, ArcGIS hosted |
| Structure | 3 | Clean JSON schema, well-typed fields |
| Identifiers | 3 | IRWIN GUIDs, unique fire identifiers |
| Additive Value | 3 | Rich incident metadata, perimeters, official source |
| **Total** | **17/18** | |

## Notes

- This is the authoritative source for US fire incident data — not just thermal detections but managed incident records with containment status, personnel counts, and damage assessments.
- The perimeters layer (Layer 1) provides fire boundary polygons, which are extremely valuable for spatial analysis.
- ArcGIS Feature Service API is well-documented and supports complex queries including spatial filters.
- Historical data also available through the NIFC open data hub (archived incidents, perimeter history).
- Complements FIRMS nicely: FIRMS provides satellite detections, NIFC provides the managed incident context.
