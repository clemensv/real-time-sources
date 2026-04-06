# Geoscience Australia — Earthquakes@GA

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | Earthquakes@GA — Geoscience Australia Earthquake Monitoring |
| **Operator**     | Geoscience Australia (Australian Government) |
| **URL**          | https://earthquakes.ga.gov.au/ |
| **FDSN (AusPass)** | `https://auspass.edu.au/fdsnws/event/1/query` |
| **Coverage**     | Australia and surrounding region; also indexes global significant events |
| **Update Freq.** | Near-real-time for Australian events |

## What It Does

Geoscience Australia monitors, analyses, and reports on significant earthquakes to alert Australian governments and the public. Australia sits on a relatively stable continental plate, but it does experience intraplate seismicity — occasionally surprising events like the 2021 M5.9 near Melbourne.

The primary web interface at `earthquakes.ga.gov.au` is a JavaScript SPA with no documented public REST API. Direct API endpoint probing (`/api/quakes`, `/api/quakes/recent`) returned the SPA's HTML shell rather than JSON — the API appears to be internal or served through the SPA's backend routing.

However, Australian seismological data is available through the **AusPass** FDSN event service at `auspass.edu.au`. This returned valid FDSN text data, though the catalog appears to contain historical/processed events rather than a real-time feed (the sample data had future-dated entries, suggesting test or reprocessed data).

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `earthquakes.ga.gov.au/` | ✅ 200 | SPA; no REST API exposed |
| `earthquakes.ga.gov.au/api/quakes` | ❌ Returns HTML | Not a public API |
| `earthquakes.ga.gov.au/fdsnws/event/1/query` | ❌ Returns HTML | No FDSN service at this domain |
| `auspass.edu.au/fdsnws/event/1/query?limit=2&format=text` | ✅ 200 | FDSN text; GA-sourced events |

### Sample AusPass Response

```
#EventID|Time|Latitude|Longitude|Depth/km|Author|Catalog|Contributor|ContributorID|MagType|Magnitude|MagAuthor|EventLocationName|EventType
smi:local/d237c126-...|2036-11-12T06:28:16|0.0|0.0|0.0|GA (via ANU)||Geoscience Australia|...|...|0.0||Papua New Guinea|earthquake
```

## Authentication & Licensing

- **Auth**: None for AusPass. The GA website itself has no public API.
- **Rate Limits**: Unknown for AusPass.
- **License**: Australian government open data (Creative Commons Attribution 4.0).

## Integration Notes

The situation is messy. Geoscience Australia's primary earthquake portal doesn't expose a documented API — it's an Angular SPA that presumably fetches from internal endpoints. Reverse-engineering those endpoints is possible but fragile.

The AusPass FDSN service exists and returns GA-authored events, but it appears to be more of an academic data archive than a real-time monitoring feed. The sample data contained future-dated events and zero-valued coordinates, suggesting it's not a production-grade real-time catalog.

Australian seismicity is also captured in the USGS and EMSC global catalogs, making a dedicated Australian source less critical.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 1     | No documented public API from GA; AusPass exists but unclear status |
| **Data Freshness**           | 1     | AusPass data looks historical; no real-time feed found |
| **Format / Schema Quality**  | 2     | FDSN format via AusPass; but data quality is questionable |
| **Auth / Access Simplicity** | 3     | Anonymous access to AusPass |
| **Coverage Relevance**       | 1     | Australia — low seismicity continent; already in global catalogs |
| **Operational Reliability**  | 1     | No clear production API; AusPass appears academic |
| **Total**                    | **9 / 18** | |

## Verdict

Skip. The lack of a documented public API from Geoscience Australia makes this impractical. AusPass provides FDSN access to GA-authored events but the data quality and real-time capability are questionable. Australia's seismicity is already well-covered by USGS and EMSC global catalogs. Not worth the integration effort when better options exist.
