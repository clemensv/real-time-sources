# Japan MLIT — Dam and Reservoir Monitoring (river.go.jp)

**Country/Region**: Japan (~550 major dams monitored)
**Publisher**: Ministry of Land, Infrastructure, Transport and Tourism (MLIT), River Bureau
**API Endpoint**: `https://www.river.go.jp/` (main portal)
**Documentation**: https://www.river.go.jp/ (Japanese only)
**Protocol**: Web portal; internal telemetry system; limited public API
**Auth**: None for public web access
**Data Format**: HTML (Japanese), some CSV/XML
**Update Frequency**: Real-time (10-minute intervals for dam operations)
**License**: Japanese government data (open use with attribution)

## What It Provides

MLIT's "川の防災情報" (River Disaster Prevention Information) system is Japan's national real-time water monitoring platform, covering:

- **Dam storage levels** (貯水位) — current water level
- **Dam storage rate** (貯水率) — percentage of capacity
- **Dam inflow** (流入量) and **outflow/discharge** (放流量)
- **River water levels** (水位) at thousands of gauging stations
- **Tidal levels** (潮位) at coastal stations
- **Water quality** (水質) monitoring
- **Precipitation** (雨量) from rain gauges
- **River cameras** — live CCTV feeds of river conditions

Japan has ~2,700 dams, with ~550 major dams operated by MLIT, prefectures, and power companies. The monitoring system was built for flood disaster prevention — Japan's monsoon season and typhoons make real-time dam operations life-critical.

## API Details

The public-facing web portal at `river.go.jp` provides interactive maps and data tables, but programmatic API access is limited:

- **Main portal**: Real-time dashboards for all monitored dams and rivers (Japanese interface)
- **XRAIN**: X-band radar rainfall data
- **Dam-specific pages**: individual dam operation data with storage, inflow, outflow graphs

No documented public REST API was found. However:
- Some prefectural dam operators publish data in CSV/XML formats
- Japan's e-Stat open data portal (`https://www.e-stat.go.jp/`) may have dam statistics
- MLIT's geospatial data platform may expose WMS/WFS services

The internal telemetry runs at 10-minute intervals — very high frequency by international standards.

## Freshness Assessment

Excellent internally — 10-minute real-time telemetry for dam operations during flood events. Public-facing web portal displays real-time data. However, programmatic access is the bottleneck — no public REST API means the real-time data is effectively locked behind the web portal.

## Entity Model

- **Dam**: name, river, prefecture, operator, dam type, height, capacity, purpose (flood control/irrigation/power/water supply)
- **Real-time Data**: timestamp (10-min), storage level (m), storage rate (%), inflow (m³/s), outflow (m³/s)
- **River Station**: station name, river, km marker, warning levels
- **Observation**: water level (m), flow (m³/s), precipitation (mm)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time 10-minute intervals for dam operations |
| Openness | 1 | Public web portal but no REST API; Japanese only |
| Stability | 3 | Critical national infrastructure; legally mandated flood prevention |
| Structure | 1 | Web portal only; no standardized API for programmatic access |
| Identifiers | 2 | Dam names and codes; river station identifiers |
| Additive Value | 3 | 4th largest hydropower producer; typhoon/monsoon flood management; ~2,700 dams |
| **Total** | **13/18** | |

## Notes

- Japan's dam monitoring is world-class in terms of data density and real-time frequency, but programmatic access is nearly non-existent.
- The language barrier (Japanese-only interfaces) adds significant integration complexity.
- During typhoon season, dam operations become front-page news — the 2018 Ehime flood disaster was partly attributed to dam discharge timing.
- Three Gorges-style large reservoir operators (J-Power, EPDC) may have their own data portals.
- For a pilot, focus on a specific prefecture that publishes dam data in CSV format, rather than trying to integrate the national portal.
- The combination of dam storage + river level + radar rainfall on one platform makes this conceptually the most comprehensive national water monitoring system.
