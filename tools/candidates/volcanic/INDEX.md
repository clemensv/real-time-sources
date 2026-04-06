# Volcanic Activity — Candidate Data Sources

## Summary

| Source | Region | Protocol | Auth | Freshness | Total | Status |
|--------|--------|----------|------|-----------|-------|--------|
| [GeoNet NZ Volcanic](geonet-nz-volcanic.md) | New Zealand | REST (GeoJSON) | None | Event-driven | **16/18** | ✅ Recommended |
| [USGS HANS](usgs-volcano-hans.md) | USA | REST (JSON) | None | Event-driven | **16/18** | ✅ Recommended |
| [VAAC Ash Advisories](vaac-ash-advisories.md) | Global (Americas) | HTTP (XML/KML) | None | Every 6h during events | **15/18** | ✅ Recommended |
| [JMA Volcanic Warnings](jma-volcanic-japan.md) | Japan | HTTP (HTML) | None | Event-driven | **13/18** | ⚠️ HTML-only |
| [INGV Italy](ingv-italy.md) | Italy | Web + FDSN | None | Weekly bulletins | **13/18** | ⚠️ Fragmented access |
| [Smithsonian GVP](smithsonian-gvp.md) | Global | Web portal | None | Weekly reports | **12/18** | ⚠️ No API, 403 blocks |
| [MIROVA](mirova.md) | Global | Web portal | None | Near-real-time | **8/18** | ❌ Dismissed (no API) |
| [VolcanoDiscovery](volcanodiscovery.md) | Global | Website | None | Daily | **6/18** | ❌ Dismissed (no API) |

## Recommendations

**Tier 1 — Implement first:**
- **GeoNet NZ** — Exemplary REST/GeoJSON API for volcanic alert levels. Clean, documented, versioned. A model implementation.
- **USGS HANS** — Official US volcano monitoring with a JSON API. Covers 161 US volcanoes. API needs more exploration but the foundation is solid.
- **VAAC Ash Advisories** — Unique aviation-critical ash cloud data in XML/KML. ICAO-mandated, operationally essential.

**Tier 2 — Regional value:**
- **JMA Japan** — Critical for Pacific Rim coverage (111 active volcanoes), but HTML-based output requires parsing.
- **INGV Italy** — Premier volcanic monitoring institution, but web infrastructure issues and no unified API.

**Reference data:**
- **Smithsonian GVP** — The definitive volcano reference database (VNUM identifiers). Use for enrichment, not real-time monitoring.

**Dismissed:**
- **MIROVA** — Excellent science but unreachable website, no API.
- **VolcanoDiscovery** — Content aggregator, no original data or API.

## Notes

Volcanic monitoring data is inherently event-driven — APIs may return minimal data during quiescent periods. Unlike fire or lightning, eruptions are rare events with intense data bursts. The ideal architecture polls alert-level APIs regularly and increases monitoring frequency when levels change.
