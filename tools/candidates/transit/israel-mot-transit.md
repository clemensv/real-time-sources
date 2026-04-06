# Israel Ministry of Transport — Open Data Portal (SIRI/GTFS-RT Transit)

**Country/Region**: Israel
**Publisher**: Ministry of Transport and Road Safety (משרד התחבורה והבטיחות בדרכים)
**API Endpoint**: `https://data.gov.il/api/3/action/` (CKAN portal) + SIRI/GTFS real-time feeds
**Documentation**: https://data.gov.il/ (national open data portal)
**Protocol**: CKAN REST API + SIRI SM (real-time transit)
**Auth**: None for CKAN; API key for SIRI feeds
**Data Format**: JSON (CKAN), SIRI XML (real-time), GTFS (schedules)
**Update Frequency**: Daily vehicle registration updates; real-time SIRI transit predictions
**License**: Creative Commons Attribution (CC BY)

## What It Provides

Israel's national open data portal contains **180 transportation-related datasets** from the Ministry of Transport. The transport data is updated automatically on a daily basis and covers:

### Transit Data
- **GTFS Schedule Data**: Complete route, stop, trip, and schedule data for all Israeli public transit operators
- **SIRI SM (Service Monitoring)**: Real-time bus/train arrival predictions via standardized SIRI protocol
- **SIRI VM (Vehicle Monitoring)**: Real-time vehicle positions
- **Bus operator data**: Route-level ridership, service metrics

### Vehicle & Registration Data
- **Vehicles with disability permits** — Daily automatic updates (confirmed fresh: April 6, 2026)
- **Vehicle registration database** — Comprehensive vehicle data
- **Driver licensing statistics**

### Infrastructure
- **Road network data**
- **Traffic signal locations**
- **Parking facilities**

## API Details

The CKAN portal API is standard and confirmed working:

```
# Search transportation datasets (confirmed: 180 results)
GET https://data.gov.il/api/3/action/package_search?q=transportation&rows=10

# Get specific dataset
GET https://data.gov.il/api/3/action/package_show?id={dataset_name}

# Query datastore
GET https://data.gov.il/api/3/action/datastore_search?resource_id={id}&limit=100
```

### Probed Response (April 2026)

```json
{
  "success": true,
  "result": {
    "count": 180,
    "results": [
      {
        "name": "rechev-tag-nachim",
        "title": "כלי רכב עם תג חניה לנכה",
        "Frequency": "Day",
        "Update": "Automat",
        "license_id": "cc-by",
        "metadata_modified": "2026-04-06T21:49:48.682825",
        "organization": {
          "name": "ministry_of_transport",
          "title": "משרד התחבורה והבטיחות בדרכים"
        }
      }
    ]
  }
}
```

### SIRI Real-Time Feed

Israel's Ministry of Transport operates SIRI (Service Interface for Real Time Information) feeds covering all public transit operators. The SIRI SM endpoint provides real-time stop predictions and the SIRI VM endpoint provides vehicle positions.

SIRI feed details:
- **Endpoint**: `https://siri.motrealtime.co.il:8081/Siri/SiriServices`
- **Protocol**: SIRI SM/VM over SOAP/XML
- **Auth**: API key (free registration via MOT developer portal)
- **Coverage**: All bus operators (Egged, Dan, Metropoline, Kavim, etc.) and Israel Railways

## Freshness Assessment

CKAN datasets: Updated daily (confirmed automatic updates, metadata_modified within 24 hours). SIRI feeds: Real-time (30-second refresh for vehicle monitoring). The combination provides both reference data (schedules, stops) and real-time predictions/positions.

## Entity Model

- **Dataset**: CKAN package with unique slug identifier
- **Resource**: CSV/JSON files within datasets, queryable via datastore API
- **Transit Stop**: GTFS stop_id based identifiers
- **Transit Route**: GTFS route_id
- **Vehicle**: SIRI vehicle reference IDs
- **Prediction**: SIRI MonitoredStopVisit with expected arrival/departure

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | SIRI real-time feeds; CKAN datasets updated daily |
| Openness | 2 | CKAN is open; SIRI requires free API key registration |
| Stability | 3 | National government portal; CKAN standard; SIRI is an international standard |
| Structure | 3 | CKAN API, SIRI XML, GTFS — all well-documented standards |
| Identifiers | 3 | GTFS-compatible IDs; CKAN resource UUIDs |
| Additive Value | 3 | Only source for Israeli transit; Tel Aviv, Jerusalem, Haifa coverage |
| **Total** | **17/18** | |

## Integration Notes

- CKAN API is standard — existing CKAN integration patterns can be reused
- SIRI feeds require SOAP XML handling — more complex than REST/JSON
- GTFS data can be used for schedule-based events; SIRI for real-time deviations
- Hebrew content: dataset titles and some field values are in Hebrew (UTF-8 encoded)
- Data.gov.il is accessible internationally — no geoblocking observed
- CloudEvents: SIRI VM updates → vehicle position events; SIRI SM → arrival prediction events
- The existing GTFS/GTFS-RT bridge in the repository could potentially be extended to support Israeli feeds

## Verdict

Exceptional transit data source. Israel's combination of a CKAN open data portal with SIRI real-time feeds provides comprehensive coverage of a technologically advanced transit system. The 180 transportation datasets and real-time SIRI feeds make this one of the strongest transit candidates for the Middle East region.
