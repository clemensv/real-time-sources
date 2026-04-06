# Finland STUK External Dose Rate Monitoring

**Country/Region**: Finland
**Publisher**: STUK — Radiation and Nuclear Safety Authority (Säteilyturvakeskus)
**API Endpoint**: Not confirmed (portal-based data access)
**Documentation**: https://www.stuk.fi/ (portal)
**Protocol**: Web portal / EURDEP contribution
**Auth**: None (public portal)
**Data Format**: HTML, maps; data shared via EURDEP
**Update Frequency**: Continuous (10-minute measurement cycle)
**License**: Finnish government open data

## What It Provides

STUK operates Finland's national external radiation monitoring network, consisting of approximately 255 automatic dose rate monitoring stations distributed across the country. These stations measure ambient gamma dose rate continuously and form part of Finland's nuclear emergency preparedness infrastructure.

The network provides:

- **External dose rate** — Ambient gamma dose equivalent rate in µSv/h
- **Radioactivity in outdoor air** — Aerosol and particulate monitoring
- **Environmental radioactivity** — Food, water, and environmental samples

Finland's monitoring network is particularly relevant due to its proximity to Russian nuclear facilities and the Kola Peninsula.

## API Details

### Direct API

STUK does not appear to expose a documented public REST API for real-time dose rate data. Multiple URL patterns tested returned 404:
- `https://www.stuk.fi/web/en/topics/environmental-radiation/...`
- `https://www.stuk.fi/avoindata`
- `https://opendata.stuk.fi`

### Data Access via EURDEP

Finland contributes its monitoring data to EURDEP. Finnish stations are accessible through the BfS EURDEP WFS endpoint with station IDs prefixed "FI" (e.g., FI0001, FI0002, etc.):

```
GET https://www.imis.bfs.de/ogc/opendata/ows?service=WFS&version=1.1.0
    &request=GetFeature
    &typeName=opendata:eurdep_latestValue
    &outputFormat=application/json
    &CQL_FILTER=id LIKE 'FI%'
```

### Open Data Catalog

STUK has indicated commitment to open data through Finnish government data portals, but a dedicated radiation data API was not discoverable during this research.

## Freshness Assessment

Finnish dose rate data is confirmed to be flowing through EURDEP as of 2026-04-06 (Finnish stations visible in EURDEP dataset). Direct access to STUK's own systems could not be confirmed — the website appears to have undergone restructuring. The EURDEP route provides hourly data with standard quality.

## Entity Model

- **Station** — Automatic dose rate monitoring station with ID (FIxxxx), coordinates, name.
- **Measurement** — Ambient gamma dose rate in µSv/h, typically at 10-minute or hourly intervals.
- **Network** — Part of STUK's broader environmental monitoring infrastructure.

## Feasibility Rating

| Criterion | Score | Notes |
|---|---|---|
| Freshness | 3 | Continuous monitoring, 10-min cycle internally |
| Openness | 1 | No direct public API found; data accessible only via EURDEP |
| Stability | 3 | Government nuclear safety authority infrastructure |
| Structure | 1 | No direct API; EURDEP provides structured access as proxy |
| Identifiers | 2 | Station IDs in FIxxxx format via EURDEP |
| Additive Value | 2 | ~255 stations, good coverage but accessible via EURDEP already |
| **Total** | **12/18** | |

## Notes

- Finland's radiation data is best accessed through the EURDEP WFS endpoint rather than directly from STUK.
- STUK's website appears to have undergone significant restructuring — many previously known URLs return 404. A new data portal may be in development.
- Finnish monitoring data is also contributed to IAEA's IRMIS (International Radiation Monitoring Information System).
- For a dedicated Finland-only integration, reverse-engineering the STUK web portal's data loading mechanism would be needed, but EURDEP provides a clean, stable alternative.
- STUK also monitors radioactivity in the Baltic Sea, which is unique supplementary data not available through EURDEP.
