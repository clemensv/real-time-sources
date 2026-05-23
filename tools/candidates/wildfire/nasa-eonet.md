# NASA EONET (Earth Observatory Natural Event Tracker)

- **Country/Region**: Global
- **Endpoint**: `https://eonet.gsfc.nasa.gov/api/v3/events`
- **Protocol**: REST (JSON / GeoJSON)
- **Auth**: None
- **Format**: JSON, GeoJSON
- **Freshness**: Near real-time (hours to 1 day, varies by event source)
- **Docs**: https://eonet.gsfc.nasa.gov/docs/v3
- **Score**: 16/18

## Overview

The Earth Observatory Natural Event Tracker (EONET) is NASA's curated feed of natural hazard and environmental events worldwide. Maintained by NASA's Earth Science Data and Information System (ESDIS) project, EONET aggregates reports from multiple authoritative sources — including USGS, NOAA, US Forest Service (InciWeb/IRWIN), volcano observatories, and satellite detection systems — into a single global catalog.

EONET covers a broad spectrum of event categories: wildfires, severe storms, floods, volcanoes, sea/lake ice extent, drought, dust/haze, landslides, manmade events (oil spills, etc.), snow, temperature extremes, and water color anomalies. Each event is assigned a unique EONET ID, categorized, timestamped, and geolocated with either point or polygon geometry. Events remain open (continuously updated with new geometry observations) until they end, at which point they receive a closed timestamp.

The API provides both chronological event lists and category-filtered views. Bounding box searches, date ranges, magnitude filters (e.g., wildfire acreage, hurricane wind speed), and source-specific queries are all supported. The GeoJSON endpoint returns Feature Collections compatible with standard GIS tooling.

## Endpoint Analysis

The events API was probed on 2026-05-23:

```
GET https://eonet.gsfc.nasa.gov/api/v3/events?limit=1&days=30
```

**Sample event (truncated):**

```json
{
  "id": "EONET_20230",
  "title": "DeSoto BB 8374 S RX Prescribed Fire, Harrison, Mississippi",
  "description": null,
  "link": "https://eonet.gsfc.nasa.gov/api/v3/events/EONET_20230",
  "closed": null,
  "categories": [
    {
      "id": "wildfires",
      "title": "Wildfires"
    }
  ],
  "sources": [
    {
      "id": "IRWIN",
      "url": "https://irwin.doi.gov/observer/incidents/0aa79001-67d5-4ffb-aa44-82feeb972f29"
    }
  ],
  "geometry": [
    {
      "magnitudeValue": 1535.0,
      "magnitudeUnit": "acres",
      "date": "2026-05-20T11:12:00Z",
      "type": "Point",
      "coordinates": [
        -89.035278,
        30.673333
      ]
    }
  ]
}
```

**Key observations:**
- Event ID (`EONET_XXXXX`) is stable and unique
- Geometry is an array of observations, each with its own timestamp (events that move/evolve get multiple points or a track)
- Categories use stable IDs (`wildfires`, `volcanoes`, `severeStorms`, etc.)
- Source references link back to upstream authoritative systems (IRWIN, GVP, USGS, etc.)
- Magnitude values and units are event-type specific (acres for wildfires, kt for tropical cyclones, M for earthquakes)
- Open events (`"closed": null`) continue to receive geometry updates

## Why Strong

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hours to 1 day latency depending on upstream source; not sub-minute but fast for event onset |
| Openness | 3 | No auth, no rate limits, no registration |
| Stability | 3 | NASA/ESDIS operational system, v3 API stable since 2016 |
| Structure | 3 | Well-documented JSON/GeoJSON with consistent schema |
| Identifiers | 3 | EONET IDs are stable and globally unique |
| Richness | 2 | Event metadata (category, source, magnitude) + geometry array; some events lack detailed descriptions |

**EONET excels as a multi-domain event discovery layer.** The event ID provides a natural Kafka key. The geometry array structure (one event, multiple timestamped observations) maps cleanly to a time series of CloudEvents with the same subject. Multiple categories can be handled via separate message groups or a single group with category as a subject component.

**Complements existing repo sources:** EONET aggregates signals from sources already in or adjacent to this repo (USGS earthquakes, NOAA storms, wildfire feeds). It adds value by cross-linking related events and providing a normalized global view. For wildfire specifically, EONET pulls from InciWeb/IRWIN (US prescribed burns and wildfires) — the same source that FIRMS (NASA's active fire pixels) references for incident context.

**Event evolution model is natural for streaming:** Each geometry update can emit a new CloudEvent with the same event ID as subject. The bridge can poll `/events?status=open&days=7` every 10–30 minutes, diff against previously seen geometry, and emit incremental updates.

## Limitations

- **Latency varies by event type and upstream source.** Wildfire observations from satellite (MODIS/VIIRS active fire) appear within hours; manually reported prescribed burns or volcanic activity bulletins may lag by a day. This is not sub-minute streaming.
- **No WebSocket or SSE feed.** The API is REST-only; polling is required. Typical polling interval would be 10–30 minutes for open events.
- **Event descriptions are often null or minimal.** Title is always present, but narrative detail depends on the upstream source. For many events, the source link is the only path to richer metadata.
- **Geometry arrays grow unbounded for long-lived events.** A multi-month volcanic eruption or a slow-moving iceberg could accumulate hundreds of geometry observations. The bridge must handle incremental updates to avoid re-processing entire arrays on each poll.
- **Category overlap.** A single wildfire-induced haze event might appear in both `wildfires` and `dustHaze` categories. Deduplication logic may be needed if bridging multiple categories to the same Kafka topic.

**No breaking limitations.** All are manageable with standard polling bridge patterns (state tracking, delta detection). The REST-only design means this is a poller, not a WebSocket bridge.

## Final Verdict

**Verdict**: ✅ **Build**

EONET is a high-value, multi-domain natural hazard feed with clean identifiers, stable schema, and no auth barriers. It aggregates authoritative sources into a single global catalog, making it ideal for event discovery and cross-domain correlation. The event ID → geometry array structure maps naturally to Kafka keying (event ID as key, each geometry as a separate CloudEvent). Polling latency (hours to 1 day) is acceptable for natural hazard onset tracking, and the API is production-grade with NASA/ESDIS operational backing.

**Recommended message groups:**
- One group per category (wildfires, volcanoes, severeStorms, etc.), OR
- Single group with category ID in the subject template (`eonet/{category}/{id}`)

**Bridge type:** Poller (REST, 10–30 minute interval recommended)

**Keying:** Event ID (`EONET_XXXXX`)

**Reference data:** Categories and sources metadata (one-time fetch at startup, or cache from static endpoints `/api/v3/categories` and `/api/v3/sources`)
