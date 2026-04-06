# INGV — Istituto Nazionale di Geofisica e Vulcanologia (Italy)

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | INGV FDSN Web Services |
| **Operator**     | Istituto Nazionale di Geofisica e Vulcanologia, Rome, Italy |
| **URL**          | https://www.ingv.it/ |
| **API Base**     | `https://webservices.ingv.it/fdsnws/event/1/query` |
| **Coverage**     | Italy and broader Euro-Mediterranean region |
| **Update Freq.** | Near-real-time; reviewed events within minutes |

## What It Does

INGV operates Italy's national seismic network and publishes earthquake data through a standard FDSN event web service. Italy is one of the most seismically active countries in Europe — the service catalogs thousands of events per year, from micro-quakes in the Apennines to significant events that make international news.

The FDSN endpoint supports the full parameter set: time range, geographic bounds, magnitude filters, depth, event type, and multiple output formats. The `SURVEY-INGV` author tag indicates reviewed events from their 24/7 monitoring room.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `fdsnws/event/1/query?limit=2&format=text&orderby=time` | ✅ 200 | FDSN pipe-delimited text |
| `fdsnws/event/1/query?format=xml` | ✅ Expected | QuakeML XML (FDSN standard) |

### Sample Response (FDSN text)

```
#EventID|Time|Latitude|Longitude|Depth/Km|Author|Catalog|Contributor|ContributorID|MagType|Magnitude|MagAuthor|EventLocationName|EventType
45520882|2026-04-06T09:42:57.000000|41.2542|19.546|10.0|SURVEY-INGV||||ML|3.0|--|Costa Albanese settentrionale (ALBANIA)|earthquake
45520352|2026-04-06T09:04:46.920000|42.9037|12.9183|10.4|SURVEY-INGV||||ML|0.4|--|2 km NW Sellano (PG)|earthquake
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not formally documented; standard FDSN service expectations.
- **License**: Open data. INGV earthquake catalog is freely available for research and operational use.

## Integration Notes

Standard FDSN event service — identical query parameters to EMSC, GFZ, and others implementing the spec. Supports `format=text` (pipe-delimited), `format=xml` (QuakeML), and likely `format=json` (though not all FDSN implementations support JSON).

The `EventLocationName` field contains Italian locality names (e.g., "2 km NW Sellano (PG)") which provides useful geographic context. The `EventType` field distinguishes earthquakes from other seismic events.

Polling strategy: query with `starttime` set to last-seen event time, `orderby=time`. Dedup on `EventID`. The numeric event IDs are simple integers.

For a bridge, the FDSN text format is trivially parseable (split on `|`), or use QuakeML for richer metadata including moment tensors when available.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 3     | Standard FDSN spec; well-established service |
| **Data Freshness**           | 2     | Near-real-time but poll-only |
| **Format / Schema Quality**  | 3     | FDSN standard formats (text, QuakeML) |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 2     | Italy + Euro-Med; high seismicity but regional |
| **Operational Reliability**  | 3     | National institute, 24/7 monitoring |
| **Total**                    | **16 / 18** | |

## Verdict

Solid FDSN-compliant source for Italian and Euro-Mediterranean seismicity. Italy's position as one of Europe's most seismically active countries makes this data genuinely interesting. The FDSN standard means we can share parsing logic across multiple sources. Worth building — especially if we create a generic FDSN bridge adapter that works for INGV, GFZ, EMSC, and others.
