# Australian State Fire Services — NSW RFS, VicEmergency, QLD QFD

**Country/Region**: Australia (New South Wales, Victoria, Queensland)
**Publishers**: NSW Rural Fire Service, Emergency Management Victoria, Queensland Fire Department
**Protocol**: REST (GeoJSON, GeoRSS, CAP-AU)
**Auth**: None — all feeds are public
**Update Frequency**: 30–60 minutes
**License**: CC-BY 4.0 (QLD); State copyright (NSW, VIC)

## What It Provides

Three Australian state fire services publish live incident feeds in standard formats. Together they cover the most bushfire-prone states on the continent, complementing the satellite-based DEA Hotspots with on-the-ground incident management data. Each feed provides active fire incidents with alert levels, geographic boundaries, responsible agency, and fire size.

## API Details

### NSW Rural Fire Service

| Endpoint | Format | Status |
|---|---|---|
| `https://www.rfs.nsw.gov.au/feeds/majorIncidents.json` | **GeoJSON** (FeatureCollection w/ GeometryCollection: Point + Polygon) | ✅ Verified |
| `https://www.rfs.nsw.gov.au/feeds/majorIncidents.xml` | **RSS 2.0 + GeoRSS** | ✅ Verified |

- **Update frequency**: TTL 60 minutes
- **License**: "State of New South Wales (NSW Rural Fire Service)"
- **Properties**: title, category (Advice / Watch and Act / Emergency Warning), alert level, location, council area, status, fire type, size (ha), responsible agency
- **Generator**: `NSWRFS.Feeds 1.0.0.0`

Note: `incidents.rfs.nsw.gov.au/api/v1/incidents` exists but returns 401 Unauthorized. The `/feeds/majorIncidents.*` URLs are the intended public interface.

### Victoria — VicEmergency (Emergency Management Victoria)

| Endpoint | Format | Status |
|---|---|---|
| `https://www.emergency.vic.gov.au/public/osom-geojson.json` | **GeoJSON** (all hazards) | ✅ Verified |

- **Covers**: All emergency types (fire, flood, storm, water quality) — filter for fire events
- **Properties**: CAP fields (category, event, urgency, severity, certainty), sourceOrg, feedType (warning/incident), status, name, location, timestamps, sizeFmt
- **Update frequency**: Near real-time
- **License**: Not explicitly stated

### Queensland — QLD Fire Department

All feeds hosted on AWS S3, registered on `data.qld.gov.au`:

| Endpoint | Format | Status |
|---|---|---|
| `https://publiccontent-gis-psba-qld-gov-au.s3.amazonaws.com/content/Feeds/BushfireCurrentIncidents/bushfireAlert.json` | **GeoJSON** (MultiPolygon 3D) | ✅ Verified |
| `...bushfireAlert_capau.xml` | **EDXL-DE 1.0 / CAP-AU 1.2** | ✅ Verified |
| `...bushfireAlert.xml` | **Atom + GeoRSS** | ✅ Verified |
| `...bushfireAlert.kmz` | **KMZ** | ✅ Verified |

- **Update frequency**: Every 30 minutes
- **License**: **Creative Commons Attribution 4.0** (CC-BY 4.0)
- **Properties**: WarningTitle, WarningLevel (Advice / Watch and Act / Emergency Warning), CallToAction, WarningText, Impacts
- **Generator**: FME(R) 2024.1.2.1

## Freshness Assessment

All feeds verified live on 2026-04-06. NSW and QLD update at 30–60 minute intervals. Victoria's all-hazards feed updates near real-time. QLD is the standout — four output formats including the formal CAP-AU/EDXL-DE alerting standard.

## Entity Model

- **Incident** — active fire incident with alert level, geographic boundary (polygon), location description, responsible agency, fire size
- **Alert Level** — three-tier system: Advice → Watch and Act → Emergency Warning
- All three states use similar but not identical schemas; a normalization layer would be needed for unified ingestion

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | 30–60 minute updates, near real-time for VIC |
| Openness | 3 | All public, no auth; QLD has explicit CC-BY 4.0 |
| Stability | 3 | State government infrastructure, long-running feeds |
| Structure | 3 | GeoJSON, GeoRSS, CAP-AU — excellent standards compliance |
| Identifiers | 2 | Incident titles but no formal persistent IDs |
| Additive Value | 3 | On-the-ground incident data complements satellite detection |
| **Total** | **17/18** | |

## Notes

- These feeds provide incident-level data (managed fires with alert levels, boundaries, responsible agencies) versus satellite-based detection (thermal anomaly points). Both perspectives are valuable.
- QLD is exemplary: four formats, explicit CC-BY 4.0, government open data portal registration, and CAP-AU compliance.
- VIC's feed covers all hazard types — useful for multi-hazard monitoring but requires filtering for fire events.
- DEA Hotspots (already catalogued) provides satellite-based thermal detections for all of Australia. These state feeds complement it with operational incident management data.
- Consider adding South Australia (CFS), Western Australia (DFES), and Tasmania (TFS) feeds for complete national coverage.
