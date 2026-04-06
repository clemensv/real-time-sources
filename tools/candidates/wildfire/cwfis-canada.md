# CWFIS (Canadian Wildland Fire Information System)

**Country/Region**: Canada
**Publisher**: Natural Resources Canada, Canadian Forest Service
**API Endpoint**: `https://cwfis.cfs.nrcan.gc.ca/datamart/download/activefires`
**Documentation**: https://cwfis.cfs.nrcan.gc.ca/datamart
**Protocol**: File download (CSV, SHP) / WMS
**Auth**: None
**Data Format**: CSV, Shapefile, KML
**Update Frequency**: Daily during fire season (April–October)
**License**: Open Government Licence – Canada

## What It Provides

CWFIS is Canada's national wildland fire information system, providing:

- **Active Fire locations** — Point data of currently burning fires across Canada
- **Fire Weather Index (FWI)** — Daily fire weather calculations
- **Fire Behaviour Prediction (FBP)** — Fire spread predictions
- **National Fire Database (NFDB)** — Historical fire records (point and polygon)
- **Hotspot detections** — Satellite-detected thermal anomalies

The system integrates data from all provincial/territorial fire agencies and satellite sources.

## API Details

CWFIS uses a datamart model for data distribution:

**Active Fires download:**
```
https://cwfis.cfs.nrcan.gc.ca/datamart/download/activefires
```
Available in CSV, Shapefile, and KML formats.

**WMS Service (for map layers):**
```
https://cwfis.cfs.nrcan.gc.ca/geoserver/public/wms?service=WMS&request=GetCapabilities
```

**National Fire Database (historical):**
```
https://cwfis.cfs.nrcan.gc.ca/downloads/nfdb/fire_pnt/current_version/
```

The CWFIS datamart is primarily a JavaScript SPA, making direct API probing difficult. Data appears to be served through download links rather than a queryable REST API.

## Freshness Assessment

Moderate. Active fire data is updated daily during fire season. The system is seasonal — primarily operational from April through October. Outside fire season, updates are minimal. Not a real-time streaming service.

## Entity Model

Active fire records typically include:
- Fire ID (provincial/territorial identifier)
- Location (latitude, longitude)
- Fire size (hectares)
- Status (active, being held, under control, out)
- Discovery date
- Province/territory
- Cause (human, lightning, unknown)
- Agency reporting

NFDB historical records add:
- Fire year, month
- Fire type
- Reporting agency
- Size class

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Daily file updates, seasonal availability |
| Openness | 3 | Open Government Licence, no auth |
| Stability | 2 | Government-run but SPA-based datamart, limited API |
| Structure | 2 | CSV/SHP files, no queryable REST endpoint |
| Identifiers | 2 | Provincial fire IDs exist but not standardized |
| Additive Value | 2 | Canada-specific, complements FIRMS |
| **Total** | **12/18** | |

## Notes

- The CWFIS website is heavily JavaScript-rendered, making automated data access challenging. The datamart pages require JS execution.
- The most reliable programmatic access is through direct file downloads or the WMS/WFS geoserver endpoints.
- For real-time Canadian hotspot data, NASA FIRMS coverage of Canada may be more accessible programmatically.
- Fire season focus means the system is less useful year-round.
- Integration with CIFFC (Canadian Interagency Forest Fire Centre) provides the authoritative national picture.
- Historical NFDB dataset is excellent for research but updated annually, not in real-time.
