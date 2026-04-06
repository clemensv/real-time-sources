# USGS Earthquake Monitoring — Africa Bounding Box

- **Country/Region**: Pan-African (including North Africa, East African Rift, South Africa mining region)
- **Endpoint**: `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=-35&maxlatitude=35&minlongitude=-20&maxlongitude=55&limit=50&orderby=time`
- **Protocol**: REST (FDSN Web Service)
- **Auth**: None
- **Format**: GeoJSON, QuakeML (XML), CSV, text
- **Freshness**: Near real-time (events within minutes)
- **Docs**: https://earthquake.usgs.gov/fdsnws/event/1/
- **Score**: 17/18

## Overview

The USGS Earthquake Hazards Program provides comprehensive global earthquake monitoring.
By constraining the bounding box to Africa (lat -35 to 35, lon -20 to 55), we get a
focused feed of African seismicity.

Key seismic zones in Africa:
- **East African Rift**: Ethiopia, Kenya, Tanzania, Malawi, Mozambique — the continent
  is literally splitting apart
- **Atlas Mountains**: Morocco — Mediterranean tectonic boundary
- **South African mining regions**: Shallow induced seismicity from deep gold mining
- **Cameroon Volcanic Line**: Volcanic and tectonic activity

The USGS feed captures M2.5+ events globally and M4+ for Africa consistently.

## Endpoint Analysis

**Verified live** — returns GeoJSON FeatureCollection:

```json
{
  "type": "FeatureCollection",
  "metadata": {"status": 200, "api": "2.4.0"},
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": 4.4,
        "place": "17 km SSW of Āwash, Ethiopia",
        "time": 1775072763065,
        "type": "earthquake",
        "title": "M 4.4 - 17 km SSW of Āwash, Ethiopia"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [40.1227, 8.8301, 10]
      }
    },
    {
      "properties": {
        "mag": 4.5,
        "place": "Mozambique Channel",
        "time": 1774734517451
      }
    }
  ]
}
```

The existing `usgs-earthquakes` bridge in this repository already handles USGS data.
An Africa-specific instance just needs a bounding box parameter.

## Integration Notes

- **Reuse existing bridge**: The `usgs-earthquakes` bridge already exists. An Africa
  variant only needs different query parameters (bounding box).
- **Configuration, not code**: This could be a configuration option rather than a
  separate bridge — parameterize the bounding box.
- **Complement with EMSC**: The EMSC SeismicPortal has better coverage for South Africa
  (SASN network contribution) and may detect smaller events.
- **Mining seismicity filtering**: South African mining-induced events are scientifically
  interesting but may need flagging to distinguish from tectonic earthquakes.
- **Polling**: Every 5 minutes is adequate. Africa generates ~5–10 detectable events/day.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Events within minutes |
| Openness | 3 | No auth, US government public domain |
| Stability | 3 | USGS operational infrastructure |
| Structure | 3 | GeoJSON, FDSN standard |
| Identifiers | 3 | USGS event IDs, FDSN compliant |
| Richness | 2 | Full seismic parameters |
