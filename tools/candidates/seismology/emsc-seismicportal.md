# EMSC / SeismicPortal — European-Mediterranean Seismological Centre

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | European-Mediterranean Seismological Centre — SeismicPortal |
| **Operator**     | EMSC (Centre Sismologique Euro-Méditerranéen), Arpajon, France |
| **URL**          | https://www.seismicportal.eu/ |
| **API Base**     | `https://www.seismicportal.eu/fdsnws/event/1/query` |
| **WebSocket**    | `wss://www.seismicportal.eu/standing_order/websocket` |
| **Coverage**     | Global (aggregated from 90+ contributing networks) |
| **Update Freq.** | Near-real-time — WebSocket pushes within seconds of event creation/update |

## What It Does

EMSC aggregates earthquake bulletins from national seismological agencies worldwide — USGS, INGV, GFZ, KOERI, and dozens more — into a single, unified catalog. SeismicPortal is their public data portal. The standout feature is a **WebSocket endpoint** that pushes new or updated events the moment they land in the EMSC-RTS catalog. That's not polling on a timer. That's real-time push.

The FDSN event web service provides the REST query side: filter by time, magnitude, region, depth. Supports `json`, `text`, and `xml` output formats. The JSON responses are GeoJSON FeatureCollections — a format we already handle for USGS.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `fdsnws/event/1/query?limit=2&format=json&orderby=time` | ✅ 200 | GeoJSON FeatureCollection |
| `fdsnws/event/1/query?limit=2&format=text&orderby=time` | ✅ 200 | Pipe-delimited FDSN text |
| WebSocket `wss://www.seismicportal.eu/standing_order/websocket` | ✅ Documented | SockJS/native WS, pushes JSON on insert/update |

### Sample JSON Response (trimmed)

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "id": "20260406_0000204",
    "geometry": { "type": "Point", "coordinates": [126.4, 1.41, -26.0] },
    "properties": {
      "source_catalog": "EMSC-RTS",
      "time": "2026-04-06T10:11:03.0Z",
      "flynn_region": "MOLUCCA SEA",
      "lat": 1.41, "lon": 126.4, "depth": 26.0,
      "auth": "BMKG", "mag": 2.7, "magtype": "m",
      "unid": "20260406_0000204",
      "lastupdate": "2026-04-06T10:21:21.533148Z"
    }
  }]
}
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not formally documented; reasonable use expected.
- **License**: EMSC data policy — free for research and non-commercial use. Attribution required.

## Integration Notes

The WebSocket is the killer feature here. A SockJS client or plain WebSocket connection to `wss://www.seismicportal.eu/standing_order/websocket` yields JSON messages on every event insert or update. The Python sample code on their site uses Tornado, but any WS library works. Each message includes an `action` field (`create` or `update`) and the full event properties.

For polling fallback, the FDSN endpoint supports standard parameters: `starttime`, `endtime`, `minmagnitude`, `maxmagnitude`, `minlatitude`, `maxlatitude`, `minlongitude`, `maxlongitude`, `mindepth`, `maxdepth`, `limit`, `orderby`, `format`.

The GeoJSON schema is structurally similar to USGS but with different property names — `flynn_region` instead of `place`, `unid` as the event ID, `lastupdate` for change tracking.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 3     | FDSN standard + documented WebSocket with code samples |
| **Data Freshness**           | 3     | WebSocket push = seconds-level latency |
| **Format / Schema Quality**  | 3     | GeoJSON FeatureCollection, FDSN text, QuakeML XML |
| **Auth / Access Simplicity** | 3     | Anonymous, no keys |
| **Coverage Relevance**       | 3     | Global aggregation from 90+ networks |
| **Operational Reliability**  | 2     | Institutional service; no formal SLA; some downtime reported historically |
| **Total**                    | **17 / 18** | |

## Verdict

Top-tier candidate. The WebSocket makes this arguably the most attractive seismology source for a real-time bridge — no polling loop needed, just connect and receive. The GeoJSON format overlaps heavily with our existing USGS bridge code. Global coverage from a European perspective means it complements USGS nicely (often faster for Euro-Med events). Build it.
