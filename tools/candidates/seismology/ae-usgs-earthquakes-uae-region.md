# USGS Earthquake Data - UAE Region

- **Country/Region**: United Arab Emirates + Northern Oman (seismically active Zagros fold belt)
- **Endpoint**: `https://earthquake.usgs.gov/fdsnws/event/1/query`
- **Protocol**: FDSN Event Web Service (REST)
- **Auth**: None
- **Format**: GeoJSON, QuakeML, CSV
- **Freshness**: Real-time (earthquakes published within minutes of detection)
- **Docs**: https://earthquake.usgs.gov/fdsnws/event/1/
- **Score**: 11/18

## Overview

The UAE is located at the southeastern edge of the Zagros seismological zone, where the Arabian Plate collides with the Eurasian Plate. While the UAE interior experiences minimal seismicity, the northern emirates (Ras Al Khaimah, Fujairah) and adjacent areas of Oman's Musandam Peninsula experience regular low-to-moderate magnitude earthquakes.

The National Center of Meteorology (NCM) operates the UAE National Seismic Network with 14 seismic stations across the country. However, NCM does not currently publish a public real-time API. The USGS global catalog includes earthquakes detected in the UAE region, though with lower spatial density than NCM's national network.

**Historical context**: The UAE's strongest recorded earthquake was a 5.0 magnitude event in 2013 near Fujairah. Felt earthquakes (magnitude 3.0+) occur several times per year in the northern emirates and are closely monitored due to population density and critical infrastructure (Barakah Nuclear Power Plant is 250 km from the seismically active zone).

## Endpoint Analysis

**FDSN Event Web Service** — query by bounding box and time:

```
GET https://earthquake.usgs.gov/fdsnws/event/1/query
  ?format=geojson
  &minlatitude=22.0
  &maxlatitude=27.0
  &minlongitude=51.0
  &maxlongitude=57.0
  &minmagnitude=2.0
  &orderby=time
```

**UAE bounding box**:
- Southwest: 22.0°N, 51.0°E (southern UAE coast)
- Northeast: 27.0°N, 57.0°E (northern emirates + Oman border)

**Returns**: GeoJSON FeatureCollection with earthquake events.

**Sample event**:
```json
{
  "type": "Feature",
  "properties": {
    "mag": 3.2,
    "place": "15 km NE of Dibba, United Arab Emirates",
    "time": 1706014234000,
    "updated": 1706015123000,
    "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us7000m1ab",
    "status": "reviewed",
    "type": "earthquake",
    "magType": "mb"
  },
  "geometry": {
    "type": "Point",
    "coordinates": [56.2713, 25.6234, 10.0]
  },
  "id": "us7000m1ab"
}
```

**Update frequency**: USGS publishes earthquakes within **5–20 minutes** of detection for events globally. Regional events (UAE) are typically available within 10 minutes.

## Why This Is a Candidate

1. **Real-time updates** — sub-hourly for new events
2. **No auth** — open FDSN web service
3. **Stable identifiers** — USGS event IDs are globally unique and permanent
4. **Standardized format** — FDSN is an IRIS/USGS standard, GeoJSON/QuakeML
5. **Complements national network** — until NCM publishes an API, USGS is the only real-time source
6. **Strategic value** — earthquake monitoring near Barakah NPP, northern emirates population centers

## Limitations

- **Sparse coverage** — USGS catalog only includes events detected by global networks; NCM's national network has better coverage but is not open data
- **Detection threshold** — USGS typically catalogs UAE events only if M ≥ 2.5–3.0; smaller events (<M2.5) are missed
- **Not UAE-specific** — USGS is global; UAE events are a subset of a bounding box query
- **Low event rate** — UAE experiences ~10–30 felt earthquakes per year (M3+), and 100–300 M2+ events annually. This is not a high-volume stream.
- **Repo overlap** — the repo already has `usgs` as a global seismology source. This is a **geographic filter**, not a new source.

## Integration Notes

**This is NOT a new source**. The repo already has a `usgs` seismology bridge (global). The UAE use case is:

1. **Add UAE bounding box** as a configuration example or preset
2. **Document UAE seismic context** (Zagros belt, Barakah NPP proximity) in the README
3. **Optionally filter to M ≥ 2.5** for UAE-specific monitoring

If NCM (National Center of Meteorology) ever publishes a public API for their National Seismic Network, **that** would be a **Build** candidate as a distinct UAE-specific source with better coverage and lower detection thresholds.

**Alternative**: Check if NCM publishes FDSN-compatible web services:
```
https://www.fdsn.org/networks/detail/NC/
```

If NCM has an FDSN station or event endpoint, that would replace this USGS-filtered approach.

**Key model**: Event ID (USGS event code, e.g., `us7000m1ab`)

**Event families**:
- Telemetry: earthquake events (magnitude, location, depth, time, felt reports)

**CloudEvents subject**: `ae/seismology/earthquakes/{event_id}` or `global/seismology/usgs/earthquakes/{event_id}`

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time (10–20 min latency), but low event rate (hourly at best for UAE) |
| Openness | 3 | No auth, public FDSN service |
| Stability | 3 | USGS/FDSN is a mature, stable standard |
| Structure | 3 | GeoJSON, QuakeML (formal specs) |
| Identifiers | 3 | USGS event IDs are globally unique and stable |
| Additive value | -3 | **Duplicates existing `usgs` source** — only adds a geographic filter |

**Verdict**: **Skip** (as a separate UAE-specific source). Instead, **document UAE as a deployment scenario** for the existing `usgs` bridge with a bounding box filter.

**PRIORITY FOLLOW-UP**: Investigate whether NCM publishes an FDSN or custom API for the UAE National Seismic Network. If yes, that would be a **Build** candidate (unique, national-level, better coverage than USGS).
