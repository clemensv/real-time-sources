# IESO (Independent Electricity System Operator — Ontario)

**Country/Region**: Ontario, Canada
**Publisher**: IESO (Independent Electricity System Operator)
**API Endpoint**: `http://reports-public.ieso.ca/public/{ReportName}/`
**Documentation**: https://www.ieso.ca/en/Power-Data/Data-Directory
**Protocol**: HTTP file download (XML reports)
**Auth**: None (fully public)
**Data Format**: XML
**Update Frequency**: 5 minutes to hourly (varies by report)
**License**: Open data, public access

## What It Provides

IESO publishes real-time and near-real-time reports covering Ontario's electricity system. Data is published as XML files on a predictable URL pattern.

Key reports:

- **RealtimeTotals** — Ontario and market demand totals (5-minute intervals)
- **GenOutputCapability** — Generator output and capability by unit
- **DAHourlyOntarioZonalPrice** — Day-ahead hourly zonal prices
- **Adequacy3** — System adequacy reports (supply/demand margin)
- **IntertieScheduleFlow** — Cross-border flows with neighboring systems (Quebec, Manitoba, Minnesota, Michigan, New York)
- **PredispatchSummary** — Pre-dispatch supply/demand forecasts

## API Details

Reports are published as XML files at predictable URLs with date-stamped filenames:

```
GET http://reports-public.ieso.ca/public/RealtimeTotals/PUB_RealtimeTotals_20260406.xml
GET http://reports-public.ieso.ca/public/GenOutputCapability/PUB_GenOutputCapability_20260406.xml
GET http://reports-public.ieso.ca/public/DAHourlyOntarioZonalPrice/PUB_DAHourlyOntarioZonalPrice_20260406.xml
GET http://reports-public.ieso.ca/public/Adequacy3/PUB_Adequacy3_20260406.xml
```

URL pattern: `http://reports-public.ieso.ca/public/{ReportName}/PUB_{ReportName}_{YYYYMMDD}.xml`

The XML contains structured market data with timestamps, values, and metadata. Files are typically available for the current day and several weeks of history.

## Freshness Assessment

RealtimeTotals updates every 5 minutes during the operating day. GenOutputCapability is published daily with hourly data. Day-ahead prices are published the day before. The URL-based file pattern means data is as fresh as the latest file posted — no caching headers to worry about.

## Entity Model

- **Market Participant**: Individual generators identified by name/code
- **Zone**: Ontario pricing zones (Ontario, Bruce, Northwest, Northeast, etc.)
- **Time**: Hourly or 5-minute intervals, Eastern Prevailing Time
- **Intertie**: Cross-border connections (Quebec, Manitoba, Michigan, Minnesota, New York)
- **Report Date**: One XML file per report per day

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 5-minute for demand, daily for generation — mixed |
| Openness | 3 | Fully public, no auth, no registration |
| Stability | 3 | Government-mandated market operator, stable URL patterns |
| Structure | 2 | XML only (no JSON), requires parsing |
| Identifiers | 2 | IESO-specific generator names, no universal codes |
| Additive Value | 2 | Ontario-specific; useful for Canadian grid coverage |
| **Total** | **14/18** | |

## Notes

- No REST API per se — this is a file-based publication system. But the predictable URL pattern makes it easy to poll.
- XML parsing is required; no JSON alternative available.
- The Data Directory page at ieso.ca is the canonical index of all available reports.
- Ontario's generation mix is interesting: ~60% nuclear, ~25% hydro, with growing wind/solar.
- Cross-border interchange data with Quebec (Hydro-Quebec) and US states adds interconnection visibility.
- Consider using EIA's `/rto/interchange-data` for the US side of the Ontario-US interchange.
