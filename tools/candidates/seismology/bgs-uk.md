# BGS — British Geological Survey Seismology

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | BGS Earthquake Seismology |
| **Operator**     | British Geological Survey (part of UKRI), Edinburgh, UK |
| **URL**          | https://www.earthquakes.bgs.ac.uk/ |
| **Feed URL**     | `https://www.earthquakes.bgs.ac.uk/feeds/MhSeismology.xml` |
| **Coverage**     | UK and near-continental shelf |
| **Update Freq.** | Events appear within hours; RSS feed updated periodically |

## What It Does

BGS is the UK's national earthquake monitoring agency. They operate a network of seismic sensors across the UK and publish earthquake bulletins. The UK is not exactly a seismic hotspot — typical events are M0.5–3.0, with a M4+ event making national headlines maybe once a decade. But they diligently record everything.

The primary machine-readable output is an RSS/XML feed of recent UK earthquakes. Each item includes title, description (with parsed location, lat/lon, depth, magnitude), publication date, and GeoRSS coordinates.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `/feeds/MhSeismology.xml` | ✅ 200 | RSS 2.0 with GeoRSS extensions |
| `/feeds/WorldSeismicity.xml` | ❌ 404 | World feed appears retired |

### Sample RSS Item

```xml
<item>
  <title>UK Earthquake alert : M  1.1 :CAIRNDOW,ARGYLL AND BUTE, Tue, 31 Mar 2026 09:12:39</title>
  <description>Origin date/time: Tue, 31 Mar 2026 09:12:39 ;
    Location: CAIRNDOW,ARGYLL AND BUTE ;
    Lat/long: 56.248,-4.834 ; Depth: 8 km ; Magnitude:  1.1</description>
  <link>http://earthquakes.bgs.ac.uk/earthquakes/recent_events/20260331091125.html</link>
  <pubDate>Tue, 31 Mar 2026 09:12:39</pubDate>
  <category>EQUK</category>
  <geo:lat>56.248</geo:lat>
  <geo:long>-4.834</geo:long>
</item>
```

## Authentication & Licensing

- **Auth**: None. Public RSS feed.
- **Rate Limits**: None documented.
- **License**: UK Open Government Licence. Free to use with attribution.

## Integration Notes

This is an RSS feed, not a REST API — simpler but less flexible. No query parameters, no filtering by magnitude or time range. You get what the feed contains (roughly the last 10–20 UK events).

Parsing requires XML/RSS processing. The structured fields are split between the title/description text (needs string parsing) and the `geo:lat`/`geo:long` elements. There's no unique event ID in the feed beyond the link URL.

The world seismicity feed (`WorldSeismicity.xml`) appears to be retired (404), leaving only UK-focused data.

Low event volume — the UK records maybe 200-300 detected earthquakes per year, most of them micro-quakes. The feed had ~10 events spanning about a month.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 1     | RSS feed only; no REST API or query parameters |
| **Data Freshness**           | 2     | Events appear within hours; feed updates periodically |
| **Format / Schema Quality**  | 1     | RSS with text-in-description; needs string parsing; no JSON |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 1     | UK only; very low seismicity |
| **Operational Reliability**  | 2     | Government survey; reliable but minimal investment in API |
| **Total**                    | **10 / 18** | |

## Verdict

Low priority. The UK is one of the least seismically active regions we could cover, and the data delivery mechanism (RSS with embedded text descriptions) is the weakest format in this roundup. UK earthquakes are already captured by EMSC's global catalog. Only consider this if there's specific demand for UK-focused seismic monitoring. Skip for now.
