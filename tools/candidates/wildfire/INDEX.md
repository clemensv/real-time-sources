# Wildfire / Thermal Anomaly — Candidate Data Sources

Research completed: 2026-04-06 (Round 1), 2026-04-06 (Round 2 — European, Australian state, FWI expansion)

## Summary

| Source | Region | Protocol | Auth | Freshness | Total | Status |
|--------|--------|----------|------|-----------|-------|--------|
| [NASA FIRMS](nasa-firms.md) | Global | REST | API Key (free) | URT <60s / NRT ~3h | **17/18** | ✅ Recommended |
| [NIFC USA Wildfires](nifc-usa-wildfires.md) | USA | ArcGIS REST | None | Multi-daily | **17/18** | ✅ Recommended |
| [Australia State Fires](australia-state-fires.md) | Australia (3 states) | REST | None | 30–60 min | **17/18** | ✅ Recommended |
| [BEYOND/NOA FireHub](beyond-noa-greece.md) | Greece | OGC WFS | None | Satellite-pass | **16/18** | ✅ Recommended |
| [GWIS FWI Forecasts](gwis-fwi-forecasts.md) | Global | OGC WMS | None | Daily | **16/18** | ✅ Recommended |
| [EFFIS/GWIS](effis-gwis.md) | Europe/Global | OGC WFS | None | Daily | **15/18** | ✅ Recommended |
| [Fogos.pt Portugal](fogos-pt-portugal.md) | Portugal | REST | None → token | Near real-time | **14/18** | ✅ Viable |
| [DEA Hotspots Australia](dea-hotspots-australia.md) | Australia | OGC WFS | None | Per-satellite-pass | **14/18** | ✅ Viable |
| [CWFIS Canada](cwfis-canada.md) | Canada | File download | None | Daily (seasonal) | **12/18** | ⚠️ Limited API |
| [INPE Queimadas](inpe-queimadas-brazil.md) | Brazil/S.America | Web portal | None | Daily | **10/18** | ⚠️ No REST API |
| [CAL FIRE](calfire-california.md) | California | Internal API | Blocked (403) | Near real-time | **8/18** | ❌ Dismissed |
| [Africa MODIS/VIIRS Hotspots](africa-modis-viirs-hotspots.md) | Pan-African | ArcGIS REST | None | Last 48h | **15/18** | ✅ Recommended |

### Investigated But Not Catalogued

| Source | Region | Result |
|--------|--------|--------|
| Italian Protezione Civile | Italy | No public fire API; SPAs only. Use EFFIS for Italian coverage. |
| VIIRS beyond FIRMS | Global | Same data via FIRMS API, LANCE NRT, LAADS DAAC — multiple access channels documented in Round 1. |
| Russian FIRMS/Rosleskhoz | Russia | Not probed (geopolitical access constraints) |

## Recommendations

**Tier 1 — Implement first:**
- **NASA FIRMS** — Global coverage, excellent API, near-real-time. The foundation for any fire monitoring system.
- **NIFC USA Wildfires** — Authoritative US incident data with rich metadata. Complements FIRMS (incidents vs detections).
- **Australian State Fires** — NSW, VIC, QLD all publish GeoJSON/GeoRSS/CAP-AU feeds. QLD is exemplary (CC-BY 4.0, four formats). Complements DEA Hotspots with incident-level data.

**Tier 2 — High value additions:**
- **EFFIS/GWIS** — European focus with unique burnt area polygons. WFS is standard but may need reliability testing.
- **GWIS FWI Forecasts** — Only open global Fire Weather Index forecast API. Three independent models. Predictive complement to detection-based sources.
- **BEYOND/NOA FireHub** — Outstanding regional source for Greece. Full GeoServer WFS, fire propagation modeling, burned scar archive.

**Tier 3 — Regional value:**
- **DEA Hotspots** — Authoritative for Australia. Standard WFS interface.
- **Fogos.pt** — Best community fire tracker for Portugal. Watch for auth transition.
- **CWFIS** — Canada-specific, but limited programmatic access.

**Dismissed:**
- **CAL FIRE** — API blocked; use NIFC for California data instead.
- **INPE Queimadas** — No usable API; use FIRMS for South American fire data.
- **Italy Protezione Civile** — No public API; use EFFIS for Italian fire data.

## Architecture Notes

Round 2 expands the wildfire monitoring architecture from satellite-only to a three-layer model:

```
┌───────────────────────────────────┐
│  Layer 1: Satellite Detection     │
│  FIRMS (Global), DEA (AU), EFFIS  │
├───────────────────────────────────┤
│  Layer 2: Incident Management     │
│  NIFC (US), AU State Fires,       │
│  Fogos.pt (PT), BEYOND/NOA (GR)  │
├───────────────────────────────────┤
│  Layer 3: Fire Danger Forecast    │
│  GWIS FWI (Global, 3 models)     │
└───────────────────────────────────┘
```

The three layers provide: detection ("fire exists"), operational response ("fire is being managed"), and prediction ("conditions favor fire").
