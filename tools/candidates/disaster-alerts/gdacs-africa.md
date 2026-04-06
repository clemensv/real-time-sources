# GDACS Africa Disaster Alerts

- **Country/Region**: Pan-African
- **Endpoint**: `https://gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?alertlevel=Green;Orange;Red&eventlist=EQ;TC;FL;DR;VO&country={ISO3}`
- **Protocol**: REST
- **Auth**: None
- **Format**: GeoJSON
- **Freshness**: Near real-time (updated within hours of disaster onset)
- **Docs**: https://www.gdacs.org/Knowledge/models.aspx
- **Score**: 15/18

## Overview

The Global Disaster Alerting Coordination System (GDACS) is a cooperation framework
between the UN, the European Commission, and disaster management agencies. It provides
real-time alerts for earthquakes, tropical cyclones, floods, droughts, and volcanic
activity worldwide — with excellent coverage of Africa.

Africa is disproportionately affected by floods and droughts, and GDACS is the most
structured, machine-readable source for these events. The API returns GeoJSON with rich
severity metadata and alert levels (Green/Orange/Red).

## Endpoint Analysis

**Verified live** with multiple African country queries:

Query for Kenya (`KEN`):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "properties": {
        "eventtype": "DR",
        "name": "Drought in Ethiopia, Kenya, Somalia",
        "alertlevel": "Orange",
        "fromdate": "2025-04-21T00:00:00",
        "todate": "2026-04-04T00:00:00",
        "source": "GDO",
        "severitydata": {
          "severity": 255174.0,
          "severitytext": "Medium impact for agricultural drought in 255174 km2"
        }
      }
    },
    {
      "properties": {
        "eventtype": "FL",
        "name": "Flood in Kenya",
        "alertlevel": "Green",
        "fromdate": "2026-03-18T01:00:00",
        "source": "GLOFAS"
      }
    }
  ]
}
```

Query for South Africa (`ZAF`) returned: drought events, multiple flood events,
including a cross-border Orange-level flood affecting Mozambique, South Africa, and
Zimbabwe (2026-01-19).

Supported event types: `EQ` (earthquake), `TC` (tropical cyclone), `FL` (flood),
`DR` (drought), `VO` (volcanic).

Can also query without country filter using bounding box or get all events globally.

## Integration Notes

- **Country-specific polling**: Query each African country ISO3 code separately, or
  use the global endpoint and filter by `affectedcountries[].iso3`.
- **Alert-level filtering**: Focus on Orange and Red alerts for actionable events.
  Green alerts are low-impact but useful for completeness.
- **Cross-border events**: A single disaster (like the Mozambique/SA/Zimbabwe flood)
  affects multiple countries. The `affectedcountries` array handles this.
- **Source attribution**: Events come from different upstream sources — `GLOFAS` for
  floods, `GDO` for droughts, `USGS` for earthquakes. Include this in CloudEvents metadata.
- **Geometry**: Use the `url.geometry` link to fetch detailed polygons for each event.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Updated within hours, not minutes |
| Openness | 3 | No auth, UN/EC public data |
| Stability | 3 | UN-backed infrastructure |
| Structure | 3 | GeoJSON with rich metadata |
| Identifiers | 2 | Event IDs are numeric, not globally unique |
| Richness | 2 | Multi-hazard coverage with severity scoring |
