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


## Latin America  April 2026

| Source | Region | Score | File | Status |
|--------|--------|-------|------|--------|
| **INPE TerraBrasilis DETER** | Brazil (Amazon + Cerrado) | **17/18** | [inpe-terrabrasilis-deter.md](inpe-terrabrasilis-deter.md) |  **Build**  OGC WFS GeoJSON; 445K+ deforestation alerts; no auth |
| **INPE BDQueimadas WFS** | Brazil (all biomes) | **14/18** | [inpe-bdqueimadas-wfs.md](inpe-bdqueimadas-wfs.md) |  **Build**  Same GeoServer as DETER; fire hotspot data via WFS |

### Key Finding

INPE's TerraBrasilis GeoServer at 	errabrasilis.dpi.inpe.br is a goldmine. It serves deforestation alerts (DETER), annual deforestation (PRODES), and fire data (queimadas) for **all six Brazilian biomes** through standard OGC WFS. A single WFS adapter handles everything  change the workspace and layer name. The DETER Amazon dataset alone has 445,966 features. This is arguably the most environmentally consequential open geospatial dataset on Earth.

## Round 2026-05 — Gulf + Satellite EO sweep

Added in May 2026 by the Gulf (KW/AE/OM/SA/BH/QA/IQ) and satellite-EO (NASA/ESA/NOAA/EUMETSAT/JAXA/ISRO/KARI/CNSA/Other) research fleets.

| Candidate | File | Score | Verdict |
|---|---|---|---|
| Copernicus CAMS Global Fire Assimilation System (GFAS) | [esa-cams-gfas-emissions.md](esa-cams-gfas-emissions.md) | 11/18 | ⚠️ **Maybe |
| ESA EFFIS Active Fire Detection (VIIRS/MODIS) | [esa-effis-active-fires.md](esa-effis-active-fires.md) | 13/18 | ⚠️ **Maybe |
| EFFIS Fire Weather Index (FWI) Forecast | [esa-effis-fwi-forecast.md](esa-effis-fwi-forecast.md) | 13/18 | ✅ **Build |
| EUMETSAT LSA SAF Fire Radiative Power (FRP) | [eumetsat-lsa-saf-frp.md](eumetsat-lsa-saf-frp.md) | 15/18 | — |
| NASA FIRMS - Iraq Wildfire and Agricultural Fire Detection | [iq-nasa-firms-fires.md](iq-nasa-firms-fires.md) | 13/18 | ✅ |
| NASA FIRMS Wildfire Detection — Kuwait Region | [kw-nasa-firms-kuwait.md](kw-nasa-firms-kuwait.md) | 12/18 | ⏭️ |
| NASA EONET (Earth Observatory Natural Event Tracker) | [nasa-eonet.md](nasa-eonet.md) | 16/18 | ✅ |
| NASA FIRMS (Fire Information for Resource Management System) | [nasa-firms.md](nasa-firms.md) | ?/18 | — |
| NASA FIRMS VIIRS Active Fire (NOAA JPSS Satellites) | [noaasat-firms-viirs-fire.md](noaasat-firms-viirs-fire.md) | 13/18 | — |
| INPE DETER (Real-Time Deforestation Detection System) - Brazil | [spaceother-inpe-deter-deforestation.md](spaceother-inpe-deter-deforestation.md) | 15/18 | — |
| INPE Queimadas (Brazil Fire Hotspot Monitoring) | [spaceother-inpe-queimadas-fires.md](spaceother-inpe-queimadas-fires.md) | 16/18 | — |
| Planet NICFI Tropical Forest Monitoring Program | [spaceother-planet-nicfi.md](spaceother-planet-nicfi.md) | 12/18 | — |

