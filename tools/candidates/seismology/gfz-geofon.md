# GFZ GEOFON — GeoForschungsZentrum Potsdam

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | GEOFON Program, GFZ German Research Centre for Geosciences |
| **Operator**     | Helmholtz Centre Potsdam — GFZ, Germany |
| **URL**          | https://geofon.gfz-potsdam.de/ |
| **API Base**     | `https://geofon.gfz-potsdam.de/fdsnws/event/1/query` |
| **Coverage**     | Global — focuses on significant events worldwide |
| **Update Freq.** | Near-real-time; automatic solutions within minutes |

## What It Does

GEOFON is GFZ Potsdam's global seismological observatory program. It operates a worldwide network of broadband seismic stations and runs an automatic earthquake detection system. The event catalog focuses on moderate-to-large earthquakes globally (typically M4+), though it also captures smaller events near its stations.

The FDSN event service provides standard query access. GFZ is also a key node in the European EIDA (European Integrated Data Archive) network, contributing waveform data and station metadata.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `fdsnws/event/1/query?limit=2&format=text&orderby=time` | ✅ 200 | FDSN pipe-delimited text |
| `fdsnws/event/1/query?format=xml` | ✅ Expected | QuakeML XML |

### Sample Response (FDSN text)

```
#EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|Contributor|ContributorID|MagType|Magnitude|MagAuthor|EventLocationName|EventType
gfz2026gsfn|2026-04-06T08:27:49.68|-4.479|153.544|116.9|||GFZ|gfz2026gsfn|mb|5.25||New Ireland Region, Papua New Guinea|earthquake
gfz2026gsfh|2026-04-06T08:19:51.72|-15.167|167.744|160.9|||GFZ|gfz2026gsfh|mb|4.93||Vanuatu Islands|earthquake
```

## Authentication & Licensing

- **Auth**: None. Anonymous access.
- **Rate Limits**: Not formally documented; reasonable use expected.
- **License**: Open data; GFZ data policy permits free use for research and applications. Attribution expected.

## Integration Notes

Another standard FDSN event service — same query interface as INGV and EMSC. The event IDs follow a `gfz{year}{sequence}` pattern that's easy to track for deduplication.

GFZ's catalog skews toward larger events (M4+) globally, which means lower event volume but higher signal relevance. This makes it a good complement to USGS rather than a replacement. The `EventLocationName` uses Flinn-Engdahl geographic region names — the same scheme EMSC uses.

The FDSN compliance means a single parser can handle GFZ, INGV, and EMSC data. A generic FDSN bridge would cover all three.

GFZ also provides moment tensor solutions for significant events, accessible via the extended QuakeML format.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 3     | Standard FDSN spec; major research institution |
| **Data Freshness**           | 2     | Near-real-time polling; no push |
| **Format / Schema Quality**  | 3     | FDSN standard formats |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 3     | Global, moderate-to-large events |
| **Operational Reliability**  | 3     | Major Helmholtz research center; long-running program |
| **Total**                    | **17 / 18** | |

## Verdict

Strong global source with institutional backing from one of Europe's premier geoscience centers. The FDSN compliance makes integration straightforward — especially as part of a multi-FDSN bridge. The focus on larger global events means this is genuinely complementary to USGS and EMSC. Recommended.
