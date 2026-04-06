# GeoNet New Zealand — Earthquake API

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | GeoNet — New Zealand Geological Hazard Monitoring |
| **Operator**     | GNS Science / EQC, New Zealand |
| **URL**          | https://www.geonet.org.nz/ |
| **API Base**     | `https://api.geonet.org.nz/` |
| **Coverage**     | New Zealand and surrounding Pacific region |
| **Update Freq.** | Near-real-time; automatic locations within minutes |

## What It Does

GeoNet is New Zealand's official earthquake monitoring system. The API is clean, well-documented, and returns GeoJSON with versioned Accept headers. It exposes quake lists, individual quake details, quake history (location revisions), intensity data (measured and felt reports), strong motion records, volcanic alert levels, and CAP (Common Alerting Protocol) feeds.

The `/quake?MMI=` endpoint returns up to 100 quakes from the last 365 days that exceeded a given shaking intensity in NZ. The `/quake?MMI=-1` variant returns all detected quakes regardless of felt intensity — essentially the raw automatic catalog.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/quake?MMI=3` | ✅ 200 | GeoJSON FeatureCollection, felt quakes |
| `/quake?MMI=-1` | ✅ 200 | All quakes including sub-felt, up to 100 |
| `/quake/{publicID}` | ✅ Documented | Single quake detail |
| `/quake/history/{publicID}` | ✅ Documented | Location revision history |
| `/intensity?type=measured` | ✅ Documented | Seismograph MMI readings |
| `/intensity?type=reported` | ✅ Documented | Felt reports from public |
| `/quake/stats` | ✅ Documented | Magnitude count summaries |
| `/cap/1.2/GPA1.0/quake/{ID}` | ✅ Documented | CAP XML alert format |

### Sample JSON Response (trimmed)

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [172.66, -43.57] },
    "properties": {
      "publicID": "2026p257482",
      "time": "2026-04-06T06:26:38.989Z",
      "depth": 3.99,
      "magnitude": 2.44,
      "mmi": 3,
      "locality": "5 km south-east of Christchurch",
      "quality": "best"
    }
  }]
}
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not explicitly stated; Accept header versioning encouraged.
- **License**: GeoNet Data Policy — freely available for any use with attribution. CC BY 4.0 equivalent.

## Integration Notes

The API is REST-only — no WebSocket or streaming. Polling `/quake?MMI=-1` at intervals would capture new events. Deduplication by `publicID` is straightforward; the `quality` field (`automatic` → `preliminary` → `best` → `deleted`) tracks the event lifecycle.

The Accept header versioning (`application/vnd.geo+json;version=2`) is a nice touch. GeoJSON output is standard and clean. The `locality` field gives human-readable descriptions that are unique to NZ context.

Compression via `Accept-Encoding: gzip` is supported and recommended.

CAP feed at `/cap/1.2/GPA1.0/quakefeed` provides an Atom feed of alerting-grade quake notifications — useful for significant event filtering.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 3     | Excellent docs, versioned API, GitHub issue tracker |
| **Data Freshness**           | 2     | Near-real-time but poll-only; no push mechanism |
| **Format / Schema Quality**  | 3     | Clean GeoJSON, well-defined properties |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 2     | NZ-regional; important seismic zone but limited geography |
| **Operational Reliability**  | 3     | Government-backed, long-running service |
| **Total**                    | **16 / 18** | |

## Verdict

Excellent regional source. The API is one of the cleanest in the seismology space — well-documented, GeoJSON-native, no auth friction. New Zealand sits on the Pacific Ring of Fire, making it a high-activity zone worth covering. The only drawback is the lack of streaming/WebSocket. Recommended for a poll-based bridge.
