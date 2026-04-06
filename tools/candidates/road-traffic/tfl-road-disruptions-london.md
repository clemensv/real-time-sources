# TfL Road Disruptions (London)

**Country/Region**: UK — London
**Publisher**: Transport for London (TfL)
**API Endpoint**: `https://api.tfl.gov.uk/Road/all/Disruption`
**Documentation**: https://api.tfl.gov.uk/ (Swagger: https://api.tfl.gov.uk/swagger/docs/v1)
**Protocol**: REST
**Auth**: None required (optional API key for higher rate limits)
**Data Format**: JSON (with GeoJSON geometry)
**Update Frequency**: Real-time (minutes)
**License**: TfL Open Data

## What It Provides

Real-time road disruptions across London's road network — incidents, roadworks, closures, and planned works. Data includes full GeoJSON geometry (polygons and linestrings), affected corridors, severity levels, and detailed text descriptions of traffic impact. This is one of the best open traffic APIs available — zero auth, rich structured data, and excellent freshness.

## API Details

**All current disruptions:**
```
GET https://api.tfl.gov.uk/Road/all/Disruption
```

**Road network status (all corridors):**
```
GET https://api.tfl.gov.uk/Road
```

**Specific road disruptions:**
```
GET https://api.tfl.gov.uk/Road/{roadId}/Disruption
```

**Road-specific status:**
```
GET https://api.tfl.gov.uk/Road/{roadId}/Status
```

Sample disruption response:
```json
{
  "id": "TIMS-12345",
  "category": "RealTime",
  "subCategory": "TfL planned works",
  "severity": "Serious",
  "status": "Active",
  "closureText": "Road Closed",
  "comments": "A2 BOROUGH HIGH STREET SOUTHWARK...",
  "currentUpdate": "Road closed due to TfL planned works...",
  "corridorIds": ["a2"],
  "startDateTime": "2026-04-01T00:00:00Z",
  "endDateTime": "2026-04-30T23:59:00Z",
  "lastModifiedTime": "2026-04-06T10:30:00Z",
  "geography": {
    "type": "Point",
    "coordinates": [-0.091, 51.505]
  },
  "streets": [
    {
      "name": "Borough High Street",
      "closure": "Full",
      "directions": "Both Directions",
      "segments": [{"lineString": "[[...]]"}]
    }
  ]
}
```

Key fields:
- `id` — Unique disruption ID (TIMS-prefixed)
- `category` — RealTime, PlannedWork
- `subCategory` — TfL works, Utility works, Incident
- `severity` — Serious, Moderate, Minimal
- `geography` — GeoJSON Point or Polygon
- `streets[]` — Affected streets with closure type, direction, lineString geometry
- `corridorIds` — Road corridor identifiers (e.g., "a12", "a2")
- `currentUpdate` — Live description of traffic impact

**Road status response:**
```json
{
  "id": "a2",
  "displayName": "A2",
  "statusSeverity": "Serious",
  "statusSeverityDescription": "Serious Delays",
  "bounds": "[[-0.0857,51.4953],[-0.0705,51.5068]]"
}
```

## Freshness Assessment

Disruptions are updated in real-time as situations evolve. The `lastModifiedTime` field shows updates within minutes of changes. New incidents appear immediately. Road status aggregates disruption severity per corridor and updates continuously. This is genuinely real-time operational data, not batch-processed.

## Entity Model

- **Disruption**: Incident/works/closure with ID, category, severity, lifecycle
- **Geography**: GeoJSON Point, Polygon, or LineString per disruption
- **Street**: Affected street segments with closure details and directions
- **Corridor**: Named road (A-roads, major routes) with aggregate status
- **Status**: Severity level and description per corridor

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time, per-minute updates |
| Openness | 3 | No auth required |
| Stability | 3 | TfL Unified API — London's official transport data platform |
| Structure | 3 | Rich JSON with GeoJSON geometry, well-documented Swagger |
| Identifiers | 3 | TIMS disruption IDs, corridor IDs, street names |
| Additive Value | 3 | London road network coverage; complements Santander Cycles and parking in TfL ecosystem |
| **Total** | **18/18** | |

## Notes

- Part of the same TfL Unified API as Santander Cycles and car parks. A comprehensive TfL bridge can serve bikeshare, parking, and traffic data from one platform.
- The GeoJSON geometry is particularly valuable — disruptions include precise polygons and linestrings, not just point locations.
- No API key needed for basic access. Registration is free and grants higher rate limits.
- London's road network is extensive and heavily instrumented. Disruption data covers TfL roads, borough roads, and utility works.
- Street-level segment data with closure types (Full, Partial) and affected directions enables detailed routing impact analysis.
