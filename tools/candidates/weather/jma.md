# JMA — Japan Meteorological Agency

**Country/Region**: Japan
**Publisher**: Japan Meteorological Agency (気象庁)
**API Endpoint**: `https://xml.kishou.go.jp/` (XML PULL), `https://www.data.jma.go.jp/stats/data/mdrr/` (CSV observations)
**Documentation**: https://www.data.jma.go.jp/developer/index.html
**Protocol**: Atom feed + XML PULL (for alerts/forecasts), HTTP file download (CSV for observations)
**Auth**: None (fully open, no registration required)
**Data Format**: XML (JMA Disaster Prevention XML format), CSV, GRIB2 (via subscription), Shapefile (GIS)
**Update Frequency**: Every minute (high-frequency Atom feed), hourly (observations), per model run (forecasts)
**License**: Free to use with attribution to JMA (Japan government open data policy)

## What It Provides

JMA offers a comprehensive set of meteorological data through multiple channels:

- **Disaster Prevention XML (防災情報XML)**: Real-time weather warnings, forecasts, earthquake/tsunami alerts, and volcanic information via Atom feed. Two feeds:
  - **High-frequency feed**: Updated every minute, contains at least the last 10 minutes of incoming messages.
  - **Long-term feed**: Updated hourly, retains several days of all messages.
  - Feed categories: Regular (定時 — scheduled forecasts), Ad-hoc (随時 — warnings/advisories), Earthquake/Volcano, Other.

- **AMeDAS Observations (CSV download)**: Latest observation data from ~1,300 AMeDAS (Automated Meteorological Data Acquisition System) stations. Parameters: precipitation, max/min temperature, max wind speed, snow depth.

- **GPV (Grid Point Value) Forecast Data**: Numerical weather prediction output (GRIB2 format). Sample data available; full access through the Japan Meteorological Business Support Center (JMBSC) for operational use.

- **GIS Data**: Forecast area boundaries in Shapefile format.
- **Multilingual Dictionary**: Weather terminology translated into 14 languages.

## API Details

The primary real-time mechanism is the **XML PULL system**:
- Poll the Atom feed at `https://xml.kishou.go.jp/` to discover new XML messages.
- Each Atom entry contains a link to the actual XML document.
- Documents use JMA's standardized Disaster Prevention XML schema, well-documented with technical references.

For observations:
- CSV files at `https://www.data.jma.go.jp/stats/data/mdrr/` provide latest daily/hourly AMeDAS data.
- Historical observations available via a separate download interface.

**Daily download limit**: 10 GB/day from the XML PULL service. IPs exceeding this are blocked.

## Freshness Assessment

- The high-frequency Atom feed updates every minute — among the freshest polling-based weather data sources globally.
- AMeDAS CSV data updates multiple times daily with latest observations.
- Warnings and special weather statements are issued in real-time as they are produced.

## Entity Model

- **XML Message**: Typed by category (forecast, warning, observation), with control/head/body structure
- **Station (AMeDAS)**: ~1,300 stations identified by station number, with lat/lon
- **Forecast Area**: Identified by area code with GIS boundaries
- **Observation**: Timestamped parameter values per station

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Minute-level Atom feed for alerts, frequent observation updates |
| Openness | 3 | No authentication, free access with attribution |
| Stability | 3 | National agency, operational since 2017, well-maintained |
| Structure | 2 | XML is verbose but well-documented; CSV for observations is simple |
| Identifiers | 3 | Station numbers, area codes, message type codes all standardized |
| Additive Value | 3 | Japan-only but covers earthquakes/tsunamis/volcanoes too — unique combo |
| **Total** | **17/18** | |

## Notes

- Documentation is primarily in Japanese. The developer portal and technical references require translation.
- The XML schema is JMA-specific (not WMO CAP standard), which requires custom parsing.
- Full GRIB2 GPV data requires a commercial arrangement with JMBSC; only samples are freely available.
- The Atom-feed-based PULL approach is similar to RSS polling but with a more formal XML structure.
- Japan's dense station network (1,300+ AMeDAS) provides exceptional spatial coverage for a relatively small land area.
- Earthquake and volcanic data in the same feed makes this a multi-hazard platform.
