# Radiation Monitoring — Candidate Source Index

Research completed: 2026-04-06 (Round 1), 2026-04-06 (Round 2 — expanded non-European search)

## Overview

Environmental radiation monitoring (gamma dose rate / ambient radiation) is one of the most
internationally coordinated real-time monitoring domains. The European Radiological Data Exchange
Platform (EURDEP) aggregates data from 39 countries, making it the single most important endpoint.
National networks vary wildly in API accessibility — from the excellent German BfS WFS to
JavaScript-rendered portals with no programmatic access at all.

Round 2 research expanded the search to Asia-Pacific, Canada, and additional European networks
outside EURDEP. The IAEA's IRMIS system is confirmed closed to the public. Several national
networks (Korea KINS, Belgium Telerad, Spain CSN) have real-time data locked behind legacy
web portals with no discoverable APIs.

## Candidates

| Source | Region | Stations | API Quality | Score | File |
|--------|--------|----------|-------------|-------|------|
| **EURDEP** | Europe (39 countries) | 5,500+ | ★★★ WFS/GeoJSON | 17/18 | [eurdep.md](eurdep.md) |
| **BfS ODL** | Germany | ~1,700 | ★★★ WFS/GeoJSON | 17/18 | [bfs-odl.md](bfs-odl.md) |
| **EPA RadNet** | USA | ~140 | ★★☆ REST/CSV | 15/18 | [epa-radnet.md](epa-radnet.md) |
| **Ireland EPA Radiation** | Ireland | 41 | ★★☆ WFS/GeoJSON | 13/18 | [ireland-epa-radiation.md](ireland-epa-radiation.md) |
| **Health Canada FPS** | Canada | 85 | ★★☆ CKAN/CSV | 13/18 | [health-canada-fps.md](health-canada-fps.md) |
| **RIVM Netherlands** | Netherlands | 7 (installations) | ★★☆ WFS/GeoJSON | 13/18 | [rivm-netherlands.md](rivm-netherlands.md) |
| **Safecast** | Global | Crowdsourced | ★★☆ REST/JSON | 13/18 | [safecast.md](safecast.md) |
| **Japan NRA** | Japan | ~4,700 | ★☆☆ Portal/CSV | 13/18 | [japan-nra.md](japan-nra.md) |
| **STUK Finland** | Finland | ~255 | ☆☆☆ EURDEP only | 12/18 | [stuk-finland.md](stuk-finland.md) |
| **IRSN/RNM France** | France | ~460 | ☆☆☆ EURDEP only | 12/18 | [irsn-rnm-france.md](irsn-rnm-france.md) |
| **ARPANSA** | Australia | 12 (UV) | ★☆☆ CKAN/CSV (UV only) | 11/18 | [arpansa-australia.md](arpansa-australia.md) |
| **SURO/MonRaS Czech** | Czech Republic | ~169 | ☆☆☆ EURDEP only | 11/18 | [suro-czech.md](suro-czech.md) |
| **Belgium Telerad** | Belgium | ~200+ | ☆☆☆ ArcGIS SPA | 10/18 | [belgium-telerad.md](belgium-telerad.md) |
| **NADAM Switzerland** | Switzerland | ~76 | ☆☆☆ EURDEP only | 10/18 | [nadam-switzerland.md](nadam-switzerland.md) |
| **KINS IERNet** | South Korea | 251 | ☆☆☆ Legacy ASP/Flash | 8/18 | [kins-iernet-korea.md](kins-iernet-korea.md) |
| **Radmon.org** | Global | Small community | ☆☆☆ Minimal | 6/18 | [radmon-org.md](radmon-org.md) |

### Investigated But Not Catalogued (No Public Data)

| Source | Region | Result |
|--------|--------|--------|
| IAEA IRMIS | Global | Closed inter-governmental system, SSL-restricted nucleus.iaea.org |
| Spain CSN REA | Spain | No data endpoints; empty dataset on datos.gob.es |
| Russia Roshydromet | Russia | Not probed (geopolitical access constraints) |
| Pakistan PNRA | Pakistan | Not probed (expected portal-only) |
| South Africa NNR | South Africa | Not probed (expected portal-only) |
| India AERB | India | Not probed (expected portal-only) |

## Key Findings

### The EURDEP Supernode

EURDEP is the clear winner for European radiation data. A single WFS query to
`opendata:eurdep_latestValue` on the BfS GeoServer returns 17,963 measurement records from
stations across all 39 participating countries. This effectively subsumes Finland (STUK), France
(IRSN), Czech Republic (SURO), Switzerland (NADAM), Austria, Belgium, Netherlands, and dozens more.

**Implication**: Rather than building individual integrations for each European country, a single
EURDEP connector provides pan-European coverage with minimal effort. The Belgium Telerad and
Netherlands RIVM data is also available through EURDEP.

### Non-European Coverage Gaps

Outside Europe and the US, radiation monitoring data is remarkably difficult to access programmatically:

- **Canada** — Health Canada FPS provides quarterly batch data (not real-time) but it's the only open Canadian source.
- **South Korea** — 251-station IERNet network has real-time data, but it's locked behind Flash-based Korean-only legacy web interface.
- **Australia** — ARPANSA's ionizing radiation monitoring data is dashboard-only; only UV data is on the open data portal.
- **Japan** — NRA portal requires scraping (covered in Round 1).

### Verified Live Endpoints

| Endpoint | Format | Status |
|----------|--------|--------|
| BfS WFS `eurdep_latestValue` | GeoJSON | ✅ 17,963 features, hourly |
| BfS WFS `bfs_locations` | GeoJSON | ✅ 8 features |
| EPA RadNet CSV | CSV | ✅ Hourly data, 2026 |
| Health Canada FPS CSV | CSV | ✅ 2025 data, 1,022 rows |
| RIVM WFS nuclear installations | GeoJSON | ✅ 7 features |
| RIVM WFS evacuation zones | GeoJSON | ✅ Working |
| Safecast measurements API | JSON | ✅ Returns data (historical bias) |
| Radmon.org lastreading | Plain text | ✅ Live reading |

### Recommended Implementation Priority

1. **EURDEP via BfS WFS** — Single integration, pan-European coverage (5,500+ stations)
2. **EPA RadNet** — US coverage, straightforward CSV REST API (~140 stations)
3. **Safecast** — Global citizen data, JSON REST API, CC0 license
4. **Health Canada FPS** — Canadian nuclear perimeter monitoring, CKAN/CSV
5. **BfS ODL (Germany-specific)** — If higher-resolution German data needed beyond EURDEP
6. **Japan NRA** — High value data but poor API accessibility; consider Safecast as proxy

### Not Recommended for Direct Integration

- **STUK, IRSN, SURO, NADAM** — All accessible via EURDEP; direct integration would duplicate effort with worse API quality.
- **Belgium Telerad, RIVM (dose rates)** — Available via EURDEP. RIVM's own WFS provides nuclear infrastructure reference data, not real-time dose rates.
- **KINS IERNet** — Real-time data exists but Flash-based Korean-only interface makes extraction impractical.
- **ARPANSA** — Ionizing radiation data locked behind inaccessible portal. UV data available but different domain.
- **Radmon.org** — Hobby infrastructure, minimal API, no reliability guarantees.
- **IAEA IRMIS, Spain CSN** — No public access.

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
│  (Global)  │     │          │     │           │
├────────────┤     │          │     │           │
│Health CA   │────→│          │     │           │
│ (Canada)   │     └──────────┘     └───────────┘
└────────────┘
```

Four connectors would cover most of the world's accessible radiation monitoring data. The main gap
remains Asia-Pacific — Korea, Australia, and India have monitoring networks but no open APIs.
