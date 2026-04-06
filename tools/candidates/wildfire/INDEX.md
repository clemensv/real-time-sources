# Wildfire / Thermal Anomaly — Candidate Data Sources

## Summary

| Source | Region | Protocol | Auth | Freshness | Total | Status |
|--------|--------|----------|------|-----------|-------|--------|
| [NASA FIRMS](nasa-firms.md) | Global | REST | API Key (free) | URT <60s / NRT ~3h | **17/18** | ✅ Recommended |
| [NIFC USA Wildfires](nifc-usa-wildfires.md) | USA | ArcGIS REST | None | Multi-daily | **17/18** | ✅ Recommended |
| [EFFIS/GWIS](effis-gwis.md) | Europe/Global | OGC WFS | None | Daily | **15/18** | ✅ Recommended |
| [DEA Hotspots Australia](dea-hotspots-australia.md) | Australia | OGC WFS | None | Per-satellite-pass | **14/18** | ✅ Viable |
| [CWFIS Canada](cwfis-canada.md) | Canada | File download | None | Daily (seasonal) | **12/18** | ⚠️ Limited API |
| [INPE Queimadas](inpe-queimadas-brazil.md) | Brazil/S.America | Web portal | None | Daily | **10/18** | ⚠️ No REST API |
| [CAL FIRE](calfire-california.md) | California | Internal API | Blocked (403) | Near real-time | **8/18** | ❌ Dismissed |

## Recommendations

**Tier 1 — Implement first:**
- **NASA FIRMS** — Global coverage, excellent API, near-real-time. The foundation for any fire monitoring system.
- **NIFC USA Wildfires** — Authoritative US incident data with rich metadata. Complements FIRMS (incidents vs detections).

**Tier 2 — High value additions:**
- **EFFIS/GWIS** — European focus with unique burnt area polygons. WFS is standard but may need reliability testing.

**Tier 3 — Regional value:**
- **DEA Hotspots** — Authoritative for Australia. Standard WFS interface.
- **CWFIS** — Canada-specific, but limited programmatic access.

**Dismissed:**
- **CAL FIRE** — API blocked; use NIFC for California data instead.
- **INPE Queimadas** — No usable API; use FIRMS for South American fire data.
