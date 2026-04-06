# Volcanic Activity — Candidate Data Sources

Scouted: 2026-04-06 (Round 1), 2026-04-06 (Round 2 — deep dive)

## Summary

| Source | Region | Protocol | Auth | Freshness | Total | Status |
|--------|--------|----------|------|-----------|-------|--------|
| [GeoNet NZ Volcanic](geonet-nz-volcanic.md) | New Zealand | REST (GeoJSON) | None | Event-driven | **16/18** | ✅ Recommended |
| [USGS HANS](usgs-volcano-hans.md) | USA | REST (JSON) | None | Event-driven | **16/18** | ✅ Recommended |
| [VAAC Ash Advisories](vaac-ash-advisories.md) | Global (Americas) | HTTP (XML/KML) | None | Every 6h during events | **15/18** | ✅ Recommended |
| [MAGMA Indonesia (PVMBG)](magma-indonesia-pvmbg.md) | Indonesia | HTML + API (auth) | API: Yes | Real-time VONAs | **14/18** | ⚠️ API requires auth |
| [Vedur.is Iceland](vedur-iceland.md) | Iceland | HTML (no API) | None | Real-time on web | **13/18** | ⚠️ No API; high value |
| [JMA Volcanic Warnings](jma-volcanic-japan.md) | Japan | HTTP (HTML) | None | Event-driven | **13/18** | ⚠️ HTML-only |
| [INGV Italy](ingv-italy.md) | Italy | Web + FDSN | None | Weekly bulletins | **13/18** | ⚠️ Fragmented access |
| [Toulouse VAAC + Survey](toulouse-vaac-survey.md) | Global (9 VAACs) | HTML | None | During events | **12/18** | ⏭️ Only Washington VAAC has feeds |
| [KVERT Kamchatka](kvert-kamchatka.md) | Russia (Kamchatka) | HTML | None | Weekly + VONAs | **12/18** | ⏭️ No API; fragile infrastructure |
| [Smithsonian GVP](smithsonian-gvp.md) | Global | Web portal | None | Weekly reports | **12/18** | ⚠️ No API, 403 blocks |
| [MIROVA](mirova.md) | Global | Web portal | None | Near-real-time | **8/18** | ❌ Dismissed (no API) |
| [VolcanoDiscovery](volcanodiscovery.md) | Global | Website | None | Daily | **6/18** | ❌ Dismissed (no API) |

## Recommendations

**Tier 1 — Implement first:**
- **GeoNet NZ** — Exemplary REST/GeoJSON API for volcanic alert levels. Clean, documented, versioned. A model implementation.
- **USGS HANS** — Official US volcano monitoring with a JSON API. Covers 161 US volcanoes. API needs more exploration but the foundation is solid.
- **VAAC Ash Advisories** — Unique aviation-critical ash cloud data in XML/KML. ICAO-mandated, operationally essential.

**Tier 2 — Regional value (new from deep dive):**
- **MAGMA Indonesia (PVMBG)** — 127 active volcanoes; API exists behind auth wall. If registration succeeds, this is a top-tier source. Indonesia has more active volcanoes than any other country.
- **Vedur.is Iceland** — Irreplaceable for Iceland volcanic monitoring (Reykjanes eruption sequence 2023–2026). No API found — the main risk. Revisit when new API launches.
- **JMA Japan** — Critical for Pacific Rim coverage (111 active volcanoes), but HTML-based output requires parsing.
- **INGV Italy** — Premier volcanic monitoring institution, but web infrastructure issues and no unified API.

**Tier 3 — Reference / Skip:**
- **Toulouse VAAC Survey** — Probed all 9 VAACs worldwide. Only Washington VAAC (already documented) provides machine-readable feeds. Tokyo VAAC has parseable HTML tables. All others are HTML-only or API-hostile.
- **KVERT Kamchatka** — 30+ active volcanoes, but no API, broken RSS, HTTP-only, mixed Russian/English. Tokyo VAAC covers Kamchatka for aviation purposes.
- **Smithsonian GVP** — The definitive volcano reference database (VNUM identifiers). Use for enrichment, not real-time monitoring.

**Dismissed:**
- **MIROVA** — Excellent science but unreachable website, no API.
- **VolcanoDiscovery** — Content aggregator, no original data or API.

## Candidates Not Reachable / Dismissed (Round 2)

| Candidate | Reason |
|-----------|--------|
| **SERNAGEOMIN Chile** | `rnvv.sernageomin.cl` connection timeout. Chilean volcanic monitoring unreachable. |

### Round 3 — SE Asia (Deep Dive Round 5)

| Source | Region | Protocol | Auth | Freshness | Total | Status |
|--------|--------|----------|------|-----------|-------|--------|
| [PHIVOLCS Volcanic](phivolcs-volcanic.md) | Philippines (24 active) | Web only | N/A | Event-driven | **8/18** | ⏭️ Connection failed |

**Key finding**: The Philippines has 24 active volcanoes monitored by PHIVOLCS but the website is consistently unreachable from outside the Philippines. This represents a significant Ring of Fire gap in programmatic volcanic monitoring data.

| Candidate | Reason |
|-----------|--------|
| **WOVO** | Website loads but is now "Oculus Group" — appears to have changed mission. No data API. |
| **Montserrat MVO** | Website loads (WordPress/LiteSpeed) but no data API found. |
| **HVO Hawaii** | Part of USGS Volcano Hazards Program — covered by USGS HANS. |
| **Buenos Aires VAAC** | 403 Forbidden. |
| **Montreal VAAC** | Connection timeout. |
| **Wellington VAAC** | Connection timeout. |
| **Tonga/Vanuatu/PNG** | No specific volcanic monitoring APIs found during probing. |

## Notes

Volcanic monitoring data is inherently event-driven — APIs may return minimal data during quiescent periods. Unlike fire or lightning, eruptions are rare events with intense data bursts. The ideal architecture polls alert-level APIs regularly and increases monitoring frequency when levels change.

### The VAAC Landscape

The deep dive surveyed all 9 Volcanic Ash Advisory Centers worldwide. Key finding: **only the Washington VAAC provides machine-readable data feeds** (XML/KML). The other 8 VAACs serve HTML websites with no public APIs. This is an ICAO/aviation industry data distribution problem — the real-time ash data flows through aviation weather wire services (SADIS/ISCS), not public web APIs. The Washington VAAC is the exception because NOAA follows US open data mandates.


## Latin America  April 2026

| Source | Region | Score | File | Status |
|--------|--------|-------|------|--------|
| **IGEPN Ecuador** | Ecuador + Galápagos | **5/18** | [igepn-ecuador.md](igepn-ecuador.md) |  **Skip**  403 on all endpoints; Galápagos uniqueness |
| **OVSICORI Costa Rica** | Costa Rica | **4/18** | [ovsicori-costa-rica.md](ovsicori-costa-rica.md) |  **Skip**  No working endpoints; 5 active volcanoes |
| **SERNAGEOMIN Chile** | Chile | **5/18** | [sernageomin-chile.md](sernageomin-chile.md) |  **Skip**  Server unreachable; 90 active volcanoes |

### Latin America Volcanic Summary

Latin America has 200+ active volcanoes across the Pacific Ring of Fire  but zero programmatic access. Ecuador (Galápagos!), Costa Rica (5 active volcanoes near San José), and Chile (90 volcanoes including Villarrica's lava lake) all monitor extensively, but none provide public APIs. MIROVA satellite thermal monitoring, Smithsonian GVP, and VAAC ash advisories provide partial coverage. The CENAPRED volcanic traffic light for Popocatépetl (Mexico) is documented in disaster-alerts/.