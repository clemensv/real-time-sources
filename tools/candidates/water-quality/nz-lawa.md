# New Zealand LAWA — Land, Air, Water Aotearoa

**Country/Region**: New Zealand (national coverage via 16 regional councils)
**Publisher**: LAWA (Land Air Water Aotearoa) — collaboration of regional councils, MfE, Stats NZ, and others
**API Endpoint**: `https://www.lawa.org.nz/` (web portal + data explorer)
**Documentation**: https://www.lawa.org.nz/explore-data/
**Protocol**: Web portal with interactive data explorer; no documented public REST API
**Auth**: None
**Data Format**: HTML, interactive charts, downloadable data (CSV via portal)
**Update Frequency**: Varies — annual reporting for water quality indicators; some near-real-time river data
**License**: Creative Commons (various, per regional council)

## What It Provides

LAWA is New Zealand's national environmental data portal, aggregating monitoring data from all 16 regional councils and unitary authorities. For water quality, it covers:

- **River water quality**: dissolved nutrients (nitrogen, phosphorus), E. coli, clarity, dissolved oxygen, pH, temperature — at ~1,100 monitoring sites
- **Lake water quality**: trophic state, chlorophyll-a, total nitrogen/phosphorus, clarity — ~120 lakes
- **Groundwater quality**: nitrate, E. coli, arsenic — ~1,200 wells
- **Recreational (bathing) water quality**: Suitability for contact recreation at ~800+ sites
- **Water quantity**: river flows, groundwater levels
- **Estuary health**: eutrophication, sedimentation

LAWA presents scientific monitoring data with trend analysis — whether water quality at a site is improving, stable, or degrading over time.

## API Details

No documented public REST API. Data is accessible through:

- **Interactive data explorer**: `https://www.lawa.org.nz/explore-data/` — visual maps and charts per topic
- **Downloadable summaries**: Regional and national reports in PDF
- **Open Data NZ**: Some LAWA-related datasets are published on `https://data.govt.nz/`
- **Regional council APIs**: Individual councils (e.g., Environment Canterbury, Greater Wellington) may have their own data APIs

The LAWA portal aggregates data from the national NEMS (National Environmental Monitoring Standards) framework, ensuring consistency across councils.

## Freshness Assessment

Mixed. River and groundwater monitoring data is typically updated quarterly or annually. Recreational water quality is updated weekly during swimming season (November–March). Real-time river flow data is available from some regional councils but not through LAWA itself.

## Entity Model

- **Monitoring Site**: name, regional council, lat/lon, water body type (river/lake/groundwater/coast)
- **Indicator**: parameter name, median value, trend direction (improving/stable/degrading), confidence
- **Water Body**: name, type, catchment, region
- **Regional Council**: name, region, number of monitoring sites

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Quarterly/annual for WQ indicators; weekly for bathing season |
| Openness | 2 | Public portal; data downloadable but no REST API |
| Stability | 3 | Multi-agency national collaboration; government-backed |
| Structure | 1 | Web portal only; no programmatic access; individual councils may have APIs |
| Identifiers | 2 | Site names; regional council-specific codes; NEMS standardization |
| Additive Value | 3 | Complete national WQ picture; includes trend analysis; Southern Hemisphere reference |
| **Total** | **12/18** | |

## Notes

- LAWA is a model for national environmental reporting — the trend analysis (improving/stable/degrading) adds significant value over raw data.
- New Zealand's clean/green brand depends on water quality — any degradation is politically significant.
- The biggest limitation is the lack of an API. Individual regional councils are the path for programmatic access.
- Environment Canterbury (`ecan.govt.nz`) has been a leader in making monitoring data available programmatically — a good pilot target.
- Recreational water quality monitoring is particularly well-organized — weekly E. coli sampling at 800+ sites during summer.
- The NEMS framework ensures comparability across councils — a rare achievement for a federated monitoring system.
