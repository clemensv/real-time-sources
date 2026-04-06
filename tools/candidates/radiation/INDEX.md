# Radiation Monitoring — Candidate Source Index

Research completed: 2026-04-06

## Overview

Environmental radiation monitoring (gamma dose rate / ambient radiation) is one of the most
internationally coordinated real-time monitoring domains. The European Radiological Data Exchange
Platform (EURDEP) aggregates data from 39 countries, making it the single most important endpoint.
National networks vary wildly in API accessibility — from the excellent German BfS WFS to
JavaScript-rendered portals with no programmatic access at all.

## Candidates

| Source | Region | Stations | API Quality | Score | File |
|--------|--------|----------|-------------|-------|------|
| **EURDEP** | Europe (39 countries) | 5,500+ | ★★★ WFS/GeoJSON | 17/18 | [eurdep.md](eurdep.md) |
| **BfS ODL** | Germany | ~1,700 | ★★★ WFS/GeoJSON | 17/18 | [bfs-odl.md](bfs-odl.md) |
| **EPA RadNet** | USA | ~140 | ★★☆ REST/CSV | 15/18 | [epa-radnet.md](epa-radnet.md) |
| **Safecast** | Global | Crowdsourced | ★★☆ REST/JSON | 13/18 | [safecast.md](safecast.md) |
| **Japan NRA** | Japan | ~4,700 | ★☆☆ Portal/CSV | 13/18 | [japan-nra.md](japan-nra.md) |
| **STUK Finland** | Finland | ~255 | ☆☆☆ EURDEP only | 12/18 | [stuk-finland.md](stuk-finland.md) |
| **IRSN/RNM France** | France | ~460 | ☆☆☆ EURDEP only | 12/18 | [irsn-rnm-france.md](irsn-rnm-france.md) |
| **SURO/MonRaS Czech** | Czech Republic | ~169 | ☆☆☆ EURDEP only | 11/18 | [suro-czech.md](suro-czech.md) |
| **NADAM Switzerland** | Switzerland | ~76 | ☆☆☆ EURDEP only | 10/18 | [nadam-switzerland.md](nadam-switzerland.md) |
| **Radmon.org** | Global | Small community | ☆☆☆ Minimal | 6/18 | [radmon-org.md](radmon-org.md) |

## Key Findings

### The EURDEP Supernode

EURDEP is the clear winner for European radiation data. A single WFS query to
`opendata:eurdep_latestValue` on the BfS GeoServer returns 17,963 measurement records from
stations across all 39 participating countries. This effectively subsumes Finland (STUK), France
(IRSN), Czech Republic (SURO), Switzerland (NADAM), Austria, and dozens more.

**Implication**: Rather than building individual integrations for each European country, a single
EURDEP connector provides pan-European coverage with minimal effort.

### Verified Live Endpoints

| Endpoint | Format | Status |
|----------|--------|--------|
| BfS WFS `eurdep_latestValue` | GeoJSON | ✅ 17,963 features, hourly |
| BfS WFS `bfs_locations` | GeoJSON | ✅ 8 features |
| EPA RadNet CSV | CSV | ✅ Hourly data, 2026 |
| Safecast measurements API | JSON | ✅ Returns data (historical bias) |
| Radmon.org lastreading | Plain text | ✅ Live reading |

### Recommended Implementation Priority

1. **EURDEP via BfS WFS** — Single integration, pan-European coverage (5,500+ stations)
2. **EPA RadNet** — US coverage, straightforward CSV REST API (~140 stations)
3. **Safecast** — Global citizen data, JSON REST API, CC0 license
4. **BfS ODL (Germany-specific)** — If higher-resolution German data needed beyond EURDEP
5. **Japan NRA** — High value data but poor API accessibility; consider EURDEP contribution or Safecast as proxy

### Not Recommended for Direct Integration

- **STUK, IRSN, SURO, NADAM** — All accessible via EURDEP; direct integration would duplicate effort with worse API quality.
- **Radmon.org** — Hobby infrastructure, minimal API, no reliability guarantees.

## Architecture Notes

A practical radiation monitoring connector would look like:

```
┌────────────┐     ┌──────────┐     ┌───────────┐
│ EURDEP WFS │────→│          │     │           │
│  (Europe)  │     │          │     │ Unified   │
├────────────┤     │ Adapter  │────→│ Radiation │
│ EPA RadNet │────→│  Layer   │     │ Feed      │
│   (USA)    │     │          │     │           │
├────────────┤     │          │     │           │
│  Safecast  │────→│          │     │           │
│  (Global)  │     └──────────┘     └───────────┘
└────────────┘
```

Three connectors would cover most of the world's accessible real-time radiation monitoring data.
