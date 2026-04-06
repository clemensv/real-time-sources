# RIVM Netherlands — National Radioactivity Monitoring Network

**Country/Region**: Netherlands
**Publisher**: RIVM (Rijksinstituut voor Volksgezondheid en Milieu / National Institute for Public Health and the Environment)
**API Endpoint**: `https://data.rivm.nl/geo/alo/wfs?service=WFS&version=2.0.0&request=GetCapabilities`
**Documentation**: https://data.overheid.nl/datasets?search=radioactiviteit
**Protocol**: OGC WFS 2.0.0
**Auth**: None
**Data Format**: GeoJSON, GML
**Update Frequency**: Annual averages (dataset last updated 2025-01-24)
**License**: CC-0 (Creative Commons Zero / Public Domain)

## What It Provides

RIVM operates the Nationaal Meetnet Radioactiviteit (National Radioactivity Monitoring Network) under the EURATOM treaty. The network collects annual average radioactivity measurements from multiple monitoring locations across the Netherlands. The data includes ambient gamma dose rates and is complemented by nuclear infrastructure reference data — installation locations, evacuation zones, iodine prophylaxis zones, and shelter zones.

## API Details

### WFS — Nuclear Infrastructure Layers

```
GET https://data.rivm.nl/geo/alo/wfs?service=WFS&version=2.0.0&request=GetFeature
    &typeName=alo:rivm_01092021_nucleaire_installaties
    &outputFormat=application/json
    &count=5
```

Available WFS feature types:

| Layer | Description | Features |
|---|---|---|
| `alo:rivm_01092021_nucleaire_installaties` | Nuclear installations | 7 |
| `alo:rivm_01092021_evacuatiezone` | Evacuation zones | — |
| `alo:rivm_01092021_jodiumprofylaxezone` | Iodine prophylaxis zones | — |
| `alo:rivm_01092021_schuilzone` | Shelter zones | — |

### Sample Response (Nuclear Installations)

```json
{
  "type": "FeatureCollection",
  "features": [
    {"properties": {"naam": "Borssele (KCB)", "type": "Kerncentrale"}},
    {"properties": {"naam": "Doel (KCD)", "type": "Kerncentrale"}},
    {"properties": {"naam": "Emsland (KKE)", "type": "Kerncentrale"}},
    {"properties": {"naam": "Tihange (KCT)", "type": "Kerncentrale"}},
    {"properties": {"naam": "Mol (SCK)", "type": "Onderzoeksreactor"}}
  ],
  "totalFeatures": 7
}
```

### Dutch Open Data Portal

Radioactivity datasets registered on data.overheid.nl — 2 datasets from RIVM's National Radioactivity Monitoring Network, published as OGC WFS and WMS layers via NationaalGeoregister.nl.

## Freshness Assessment

Annual average data, last updated 2025-01-24. Not real-time. The nuclear infrastructure and emergency zone data is static reference data. The actual radioactivity measurement WFS layers were not reachable during probing (geodata.rivm.nl server issues), but their existence is confirmed in the NationaalGeoregister catalog.

## Entity Model

- **Nuclear Installation** — named facility with type (Kerncentrale/power plant, Onderzoeksreactor/research reactor), point geometry.
- **Emergency Zone** — polygon geometries for evacuation, iodine prophylaxis, and shelter zones around nuclear facilities.
- **Measurement** — annual average radioactivity values (specific layer names to be discovered from geodata.rivm.nl when accessible).

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 1 | Annual averages only |
| Openness | 3 | CC-0 license, no auth, standard WFS |
| Stability | 3 | Dutch government infrastructure (RIVM) |
| Structure | 3 | GeoJSON via WFS, well-typed features |
| Identifiers | 2 | Installation names but no formal ID scheme |
| Additive Value | 1 | Nuclear infrastructure context; measurement data TBD |
| **Total** | **13/18** | |

## Notes

- The primary value here is the nuclear infrastructure context data — installation locations and emergency zones are useful reference layers for any radiation monitoring system.
- Actual radioactivity measurement layers exist in the NationaalGeoregister but the geodata.rivm.nl WFS server was unreachable during probing. The `data.rivm.nl/geo/alo/wfs` endpoint works but carries different layer sets.
- Netherlands radiation monitoring data is also available via EURDEP, which would be the preferred route for real-time Dutch dose rate data.
- CC-0 license is maximally permissive — no attribution requirements.
