# USGS Earthquakes — Kuwait Region

- **Country/Region**: Kuwait + surrounding region
- **Endpoint**: `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=28.5&maxlatitude=30.5&minlongitude=46&maxlongitude=49`
- **Protocol**: REST / HTTP GeoJSON
- **Auth**: None
- **Format**: GeoJSON
- **Freshness**: Real-time (minutes after detection)
- **Docs**: https://earthquake.usgs.gov/fdsnws/event/1/
- **Score**: 5/18

## Overview

The USGS Earthquake Hazards Program publishes global seismic event data through the FDSN (International Federation of Digital Seismograph Networks) web service. The API supports geographic bounding box queries, allowing retrieval of earthquakes within Kuwait's territory and surrounding region.

Kuwait sits on the **Arabian Plate**, near the collision zone with the Eurasian Plate (Zagros Mountains fold-and-thrust belt to the northeast). While Kuwait itself has low seismicity, tremors from Iran, Iraq, and the Persian Gulf are occasionally felt.

**Seismic activity** (2020–2025, M≥2.0):
- 6 events detected within Kuwait's bounding box (28.5–30.5°N, 46–49°E)
- Most events are magnitude 2.0–3.5
- Larger regional earthquakes (Iran/Iraq, M≥5.0) are felt in Kuwait but epicentered outside the country

Kuwait does not operate a dense national seismic network. The **Kuwait National Seismic Network (KNSN)**, operated by the Kuwait Institute for Scientific Research (KISR), has a few stations but does not publish a public real-time API. USGS aggregates data from global networks including KNSN via FDSN data exchange.

## Endpoint Analysis

**Endpoint verified** — USGS FDSN Event Web Service:

```
GET https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=28.5&maxlatitude=30.5&minlongitude=46&maxlongitude=49&minmagnitude=2.0&starttime=2020-01-01
```

**Actual probe** (2025-05-23):
- HTTP 200 OK
- Content-Type: `application/json`
- Response: 6 earthquakes since 2020-01-01 (M≥2.0)
- Median response time: ~800ms
- Real-time latency: Events appear within minutes of detection

The response is GeoJSON FeatureCollection format. Each earthquake feature includes:
- `id`: USGS event ID (stable, globally unique)
- `properties.mag`: Magnitude
- `properties.place`: Human-readable location description
- `properties.time`: Origin time (epoch milliseconds)
- `properties.updated`: Last update time
- `properties.tz`: Timezone offset
- `properties.url`: USGS event page URL
- `properties.detail`: URL to detailed GeoJSON
- `properties.felt`: Number of felt reports (if any)
- `properties.cdi`: Community Decimal Intensity
- `properties.mmi`: Modified Mercalli Intensity
- `properties.alert`: Alert level (green/yellow/orange/red) for significant events
- `properties.status`: Review status (automatic/reviewed)
- `properties.tsunami`: Tsunami warning flag
- `properties.sig`: Event significance score
- `properties.net`: Contributing seismic network
- `properties.code`: Network-specific event code
- `properties.ids`: Comma-separated list of all IDs for this event
- `properties.sources`: Comma-separated list of contributing networks
- `properties.types`: Available product types (e.g., origin, shakemap, dyfi)
- `properties.nst`: Number of seismic stations used
- `properties.dmin`: Distance to nearest station (degrees)
- `properties.rms`: RMS travel time residual
- `properties.gap`: Largest azimuthal gap
- `properties.magType`: Magnitude type (e.g., ml, mb, mw)
- `geometry.coordinates`: [longitude, latitude, depth_km]

## Schema / Sample Payload

```json
{
  "type": "FeatureCollection",
  "metadata": {
    "generated": 1779522139000,
    "url": "https://earthquake.usgs.gov/fdsnws/event/1/query?...",
    "title": "USGS Earthquakes",
    "status": 200,
    "api": "2.4.0",
    "count": 6
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "mag": 3.2,
        "place": "23 km NE of Al Jahra, Kuwait",
        "time": 1642531200000,
        "updated": 1642545600000,
        "tz": null,
        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us6000abcd",
        "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=us6000abcd&format=geojson",
        "felt": 12,
        "cdi": 3.1,
        "mmi": null,
        "alert": null,
        "status": "reviewed",
        "tsunami": 0,
        "sig": 154,
        "net": "us",
        "code": "6000abcd",
        "ids": ",us6000abcd,",
        "sources": ",us,",
        "types": ",origin,phase-data,",
        "nst": 18,
        "dmin": 1.234,
        "rms": 0.45,
        "gap": 145,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 3.2 - 23 km NE of Al Jahra, Kuwait"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [47.8123, 29.5678, 10.0]
      },
      "id": "us6000abcd"
    }
  ]
}
```

## Why It's Weak for Kuwait

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| Freshness | 3 | Real-time (minutes), excellent |
| Openness | 3 | No auth, generous rate limits |
| Stability | 3 | FDSN standard, versioned, highly reliable |
| Structure | 3 | GeoJSON, well-documented |
| Identifiers | 3 | USGS event IDs are stable, globally unique |
| Additive value | 0 | Already covered by existing `usgs` global bridge |

## Limitations

- **Low seismicity** — Kuwait has minimal earthquake activity. Only 6 events M≥2.0 in 5 years within the country's bounding box. Most are unfelt or barely perceptible.
- **Already bridged globally** — The repo already has a `usgs` bridge that covers worldwide earthquakes. Adding a Kuwait-specific bounding box query is redundant.
- **Regional events more relevant** — Earthquakes felt in Kuwait typically originate in **Iran** (Zagros Mountains) or **Iraq**, outside Kuwait's borders. A "Middle East" or "Persian Gulf region" query would be more useful than a Kuwait-only filter.
- **No Kuwait-specific value** — USGS is a global service. There's no Kuwait-specific endpoint, schema, or enhancement that warrants a separate bridge.

## Alternative: KISR Seismic Network

The **Kuwait National Seismic Network (KNSN)**, operated by the Kuwait Institute for Scientific Research (KISR), monitors local and regional seismicity. If KISR publishes real-time seismic data through an API or FDSN-compatible service, it would provide:
- Higher sensitivity to local micro-seismicity
- Faster detection for Kuwait-region events
- Potential for induced seismicity monitoring (oil/gas fields)

**KISR investigation** (2025-05-23):
- Website: https://www.kisr.edu.kw (connection failed)
- KISR operates seismic stations but public API availability unknown
- FDSN station query for Kuwait region returned no results (stations may not be federated)

## Verdict

**Verdict**: ⏭️ **Reference** — Already covered by the existing `usgs` global earthquake bridge. Kuwait-specific seismic activity is too low to justify a separate bridge. Documented here for completeness as the only verified real-time seismic data source for Kuwait, but does not warrant a Kuwait-specific implementation.

**Recommendation**: If the existing `usgs` bridge doesn't already cover the Middle East region comprehensively, ensure it includes Kuwait's bounding box (28.5–30.5°N, 46–49°E) or better yet, the broader Persian Gulf / Zagros region (25–38°N, 44–60°E) to capture events felt in Kuwait.
