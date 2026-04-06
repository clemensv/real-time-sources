# Turkey DSİ — State Hydraulic Works (Hydrology Update)

**Country/Region**: Turkey
**Publisher**: Devlet Su İşleri (DSİ — State Hydraulic Works)
**API Endpoint**: `https://sis.dsi.gov.tr/` (SPA-based portal)
**Documentation**: https://www.dsi.gov.tr/
**Protocol**: Web SPA
**Auth**: Unknown
**Data Format**: SPA (backend API undocumented)
**Update Frequency**: Daily for reservoir levels; sub-daily for river flows
**License**: Turkish government data

## Context

The existing `turkey-dsi.md` candidate covers Turkey's State Hydraulic Works hydrology data. This update documents the regional significance of Turkish hydrological monitoring for the broader Middle East research scope.

### Why Turkey DSİ Matters for This Region

Turkey controls the headwaters of the Tigris and Euphrates — the two rivers that sustain Iraq and Syria. The GAP (Southeastern Anatolia Project) dams on these rivers give Turkey enormous influence over downstream water availability. Real-time monitoring of Turkish dam releases and river flows is geopolitically critical.

Key infrastructure:
- **Atatürk Dam**: 48.7 km³ reservoir; 4th largest in the world by volume
- **Keban Dam**: 31 km³ on the Euphrates
- **Ilısu Dam**: Completed 2020 on the Tigris; controversial due to downstream impacts
- **GAP Project**: 22 dams, 19 hydroelectric plants on Tigris-Euphrates

### Transboundary Impact

- Iraq depends on Tigris-Euphrates flows for agriculture and drinking water
- Syria's eastern provinces rely on Euphrates water
- Climate change is reducing Anatolian snowpack — the source of these rivers
- Water scarcity is increasingly a conflict driver in the Middle East

## Feasibility Rating

Unchanged from existing `turkey-dsi.md` assessment. The SPA-based portal at `sis.dsi.gov.tr` hides its data behind a JavaScript application. No documented REST API.

## Verdict

Geopolitically critical but API-inaccessible. Turkey's control of Tigris-Euphrates headwaters makes DSİ data regionally important beyond Turkey itself. The SPA portal suggests data infrastructure exists but isn't publicly exposed. This is a data source where official partnership channels may be the only viable access path.
