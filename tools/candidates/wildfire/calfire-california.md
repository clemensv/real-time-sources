# CAL FIRE (California Department of Forestry and Fire Protection)

**Country/Region**: California, United States
**Publisher**: CAL FIRE — California Department of Forestry and Fire Protection
**API Endpoint**: `https://www.fire.ca.gov/umbraco/api/IncidentApi/List` (observed, returns 403)
**Documentation**: https://www.fire.ca.gov/incidents
**Protocol**: REST (internal API) / ArcGIS Feature Service
**Auth**: Appears restricted (403 on direct API access)
**Data Format**: JSON
**Update Frequency**: Near real-time during active incidents
**License**: California public records

## What It Provides

CAL FIRE is the primary state agency responsible for fire protection in California. Their incident tracking system provides:

- **Active fire incidents** — Current wildfires and prescribed fires in California
- **Incident details** — Name, location, size (acres), containment percentage, structures threatened/destroyed
- **Historical incidents** — Archive of past fire seasons
- **Evacuation information** — Warnings and orders

## API Details

CAL FIRE's website is built on Umbraco CMS. An internal API endpoint has been observed:

```
https://www.fire.ca.gov/umbraco/api/IncidentApi/List?inactive=false
```

However, this endpoint returns HTTP 403 (Forbidden) when accessed directly — it appears to be protected by Cloudflare or similar WAF. The website itself renders incident data client-side from this API.

**Alternative access via NIFC:**
California fire incidents are also available through the NIFC ArcGIS service (see `nifc-usa-wildfires.md`) which includes all US incidents including California:
```
GET .../USA_Wildfires_v1/FeatureServer/0/query?where=POOState='US-CA'&outFields=*&f=geojson
```

**ArcGIS Hub:**
CAL FIRE also publishes some data through ArcGIS Online, but the specific feature service URLs change frequently.

## Freshness Assessment

The website shows near real-time incident updates during active fire events. However, programmatic access is blocked, making this unreliable as a data feed.

## Entity Model

Incident data includes:
- Incident name
- Location (county, lat/lon)
- Acres burned
- Percent contained
- Date started
- Structures threatened/destroyed
- Evacuation status
- Administrative unit
- Cooperating agencies

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Near real-time on website, but access blocked |
| Openness | 0 | API returns 403, WAF-protected |
| Stability | 1 | Internal API not meant for public consumption |
| Structure | 2 | JSON API exists but inaccessible |
| Identifiers | 2 | Incident IDs used internally |
| Additive Value | 1 | Covered by NIFC for federal/state incidents |
| **Total** | **8/18** | |

## Notes

- **Effectively dismissed** — the CAL FIRE API is not publicly accessible. Returns 403 on all tested endpoints.
- California fire incidents are fully covered by the NIFC USA Wildfires service (`POOState='US-CA'` filter).
- The CAL FIRE website is useful for human consumption but not for machine integration.
- Some community efforts have scraped this data, but that approach is fragile and likely violates ToS.
- **Recommendation:** Use NIFC for California incident data instead. It provides the same IRWIN-sourced data with a proper public API.
