# ISC — International Seismological Centre

## Source Identity

| Field            | Value |
|------------------|-------|
| **Full Name**    | International Seismological Centre — FDSN Event Service |
| **Operator**     | ISC, Thatcham, Berkshire, UK |
| **URL**          | http://www.isc.ac.uk/ |
| **API Base**     | `http://www.isc.ac.uk/fdsnws/event/1/query` |
| **Coverage**     | Global — definitive seismological bulletin |
| **Update Freq.** | Not real-time; reviewed bulletin has ~2 year delay; preliminary data weeks-months |

## What It Does

The ISC is the world's definitive global seismological bulletin. It collects arrival time readings from seismological agencies worldwide and produces a comprehensive, reviewed earthquake catalog. It's the gold standard for seismological research — but it's not built for real-time.

The ISC's FDSN event service is the recommended replacement for the now-retiring IRIS DMC event service (which shuts down June 2026). It provides standard FDSN query access to the ISC bulletin.

## Endpoints Verified

| Endpoint | Status | Notes |
|----------|--------|-------|
| `fdsnws/event/1/query?limit=2&format=text&orderby=time` | ⏱️ Timeout | Server did not respond within timeout |

### Notes on IRIS DMC

The IRIS DMC event service at `service.iris.edu/fdsnws/event/1/` is **deprecated and retiring June 1, 2026**. Their documentation explicitly redirects users to ISC and USGS as alternatives. IRIS returned HTTP 400 on test queries — likely already winding down.

## Authentication & Licensing

- **Auth**: None expected.
- **Rate Limits**: Unknown.
- **License**: ISC data is freely available for research use. Attribution required.

## Integration Notes

The ISC's primary value is completeness and accuracy, not speed. The reviewed bulletin runs ~24 months behind real-time. Even the preliminary bulletin has weeks-to-months of latency. This makes it unsuitable for a real-time bridge.

The server timeout during testing is concerning — it suggests the FDSN service may be overloaded or slow.

The ISC is recommended as the successor to IRIS DMC for users needing a comprehensive global event catalog for historical or research queries. For real-time earthquake alerting, USGS, EMSC, or GFZ are the correct choices.

## Feasibility Rating

| Dimension                    | Score | Notes |
|------------------------------|-------|-------|
| **API Maturity & Docs**      | 2     | FDSN standard; recommended IRIS replacement |
| **Data Freshness**           | 0     | Not real-time; months-to-years delay for reviewed data |
| **Format / Schema Quality**  | 3     | FDSN standard formats |
| **Auth / Access Simplicity** | 3     | Anonymous, open |
| **Coverage Relevance**       | 3     | Global, comprehensive |
| **Operational Reliability**  | 1     | Timeout during testing; uncertain production readiness |
| **Total**                    | **12 / 18** | |

## Verdict

Not suitable for a real-time bridge. The ISC's strength is completeness and accuracy for the definitive global bulletin, but the data latency (months to years) makes it fundamentally incompatible with real-time streaming. Noted for reference as the IRIS DMC successor for historical queries. Skip for this project.
