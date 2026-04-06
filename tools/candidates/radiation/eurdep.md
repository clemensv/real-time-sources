# EURDEP (European Radiological Data Exchange Platform)

**Country/Region**: Europe (39+ countries)
**Publisher**: European Commission Joint Research Centre (JRC), via national competent authorities
**API Endpoint**: `https://www.imis.bfs.de/ogc/opendata/ows` (WFS proxy hosted by German BfS)
**Documentation**: https://remap.jrc.ec.europa.eu/ (REMAP portal)
**Protocol**: OGC WFS 1.1.0
**Auth**: None
**Data Format**: GeoJSON, GML, CSV, KML, Shapefile
**Update Frequency**: Hourly (1h measurements), with 6h / 12h / 24h aggregation windows
**License**: Open data (Fees: NONE, Access Constraints: NONE per WFS GetCapabilities)

## What It Provides

EURDEP is the backbone of European radiological emergency preparedness. It aggregates ambient gamma dose rate measurements from over 5,500 monitoring stations across 39 European countries. The data flows from national networks — Austria, Germany, France, Finland, Czech Republic, and dozens more — into a single exchange platform maintained by the JRC.

Each station reports gross gamma ambient dose equivalent rate in µSv/h, typically at hourly intervals. The system was designed for nuclear emergency detection but operates continuously in routine monitoring mode.

## API Details

The EURDEP data is accessible through a WFS endpoint hosted on the BfS IMIS3 GeoServer (publicly accessible). Key feature types:

- **`opendata:eurdep_latestValue`** — Latest measurement values from all EURDEP stations (17,963 features as of April 2026)
- **`opendata:eurdep_maxValue`** — Maximum values in the analysis window

Example request (GeoJSON, 3 features):
```
GET https://www.imis.bfs.de/ogc/opendata/ows?service=WFS&version=1.1.0
    &request=GetFeature
    &typeName=opendata:eurdep_latestValue
    &outputFormat=application/json
    &maxFeatures=3
```

### Schema (eurdep_latestValue)

| Field | Type | Description |
|---|---|---|
| `id` | string | Station ID (e.g., "AT0001") |
| `name` | string | Station name (e.g., "Laa/ThayaAMS") |
| `site_status` | int | Operational status (1 = active) |
| `site_status_text` | string | Status text ("in Betrieb") |
| `height_above_sea` | number | Elevation in meters |
| `geom` | Point | WGS84 coordinates |
| `analyzed_range_in_h` | int | Time window (6, 12, or 24 hours) |
| `start_measure` | datetime | Measurement start (ISO 8601) |
| `end_measure` | datetime | Measurement end (ISO 8601) |
| `value` | number | Dose rate value |
| `unit` | string | Unit (µSv/h) |
| `validated` | int | Validation status |
| `nuclide` | string | Measurement type (e.g., "Gamma-ODL-Brutto") |
| `duration` | string | Measurement duration (e.g., "1h") |

### Sample Response

```json
{
  "type": "Feature",
  "id": "eurdep_latestValue.fid--441eacbf_19d62537822_-ea2",
  "geometry": { "type": "Point", "coordinates": [16.39, 48.73] },
  "properties": {
    "id": "AT0001",
    "name": "Laa/ThayaAMS",
    "site_status": 1,
    "height_above_sea": 183,
    "start_measure": "2026-04-06T07:00:00Z",
    "end_measure": "2026-04-06T08:00:00Z",
    "value": 0.08,
    "unit": "µSv/h",
    "nuclide": "Gamma-ODL-Brutto",
    "duration": "1h"
  }
}
```

## Freshness Assessment

Live data confirmed on 2026-04-06. Measurements timestamped within the last hour. The `eurdep_latestValue` layer returned 17,963 features — representing multiple time-window aggregations across ~5,500+ stations. Data flows continuously in routine mode.

## Entity Model

- **Station** — identified by country-prefixed code (e.g., AT0001, DE0123, FI0042). Has name, coordinates, elevation, operational status.
- **Measurement** — dose rate value with unit (µSv/h), timestamp range, analysis window, nuclide type, validation status.
- No explicit station metadata endpoint — station info embedded in measurement features.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Hourly updates confirmed, data is near-real-time |
| Openness | 3 | No auth required, no stated restrictions, WFS standard |
| Stability | 3 | EU JRC infrastructure, operational since ~2000 |
| Structure | 3 | Clean GeoJSON via WFS, well-defined schema |
| Identifiers | 2 | Station IDs exist (AT0001 etc.) but no formal URI scheme |
| Additive Value | 3 | Pan-European coverage, 5,500+ stations, 39 countries — unmatched scope |
| **Total** | **17/18** | |

## Notes

- The WFS endpoint is hosted by BfS (Germany) but serves pan-European EURDEP data — this is essentially the EURDEP data exchange materialized as a public WFS.
- The REMAP portal (remap.jrc.ec.europa.eu) provides the user-facing map view of this same data.
- The `totalFeatures: 17963` count suggests multiple measurements per station (different time windows: 6h, 12h, 24h).
- WFS supports CQL_FILTER for spatial/temporal queries, e.g., filtering by country prefix or time range.
- This single endpoint effectively covers Austria, Finland, France, Czech Republic, and all other participating European nations.
- Output formats include GeoJSON, CSV, GML, KML, Shapefile — excellent for integration.
