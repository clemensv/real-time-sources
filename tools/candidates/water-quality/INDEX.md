# Water Quality — Candidate Data Sources

Research candidates for real-time and continuous water quality monitoring APIs.

**Already covered in repo**: USGS IV (`usgs-iv/`) includes some water quality parameters as part of instantaneous values

## Candidates

| Slug | Source | Country/Region | Score | Key Strength |
|------|--------|---------------|-------|-------------|
| [usgs-nwis-wq](usgs-nwis-wq.md) | USGS NWIS Water Quality (IV) | USA (3,000+ sites) | **18/18** | Same proven API as usgs-iv; just different parameter codes |
| [hubeau-france](hubeau-france.md) | Hub'Eau France Water Quality | France (25K+ stations) | **17/18** | Superb REST API; 265M analyses; drinking water included; no auth |
| [copernicus-marine-wq](copernicus-marine-wq.md) | Copernicus Marine Service WQ Products | Global (satellite/model) | **16/18** | Satellite ocean color; HAB detection; global coverage; Python client |
| [neon-water-quality](neon-water-quality.md) | NEON Water Quality | USA (34 aquatic sites) | **15/18** | Continuous multi-parameter sensors; 30-year NSF commitment; CC0 |
| [eea-waterbase](eea-waterbase.md) | EEA Waterbase / WISE | EU (39 countries) | **14/18** | Pan-European; WFD-standardized; annual not real-time |
| [eu-bathing-water](eu-bathing-water.md) | EU Bathing Water Quality | EU (22K+ beaches) | **14/18** | Tourism-relevant; E. coli/enterococci; 30 countries |
| [rijkswaterstaat-nl](rijkswaterstaat-nl.md) | Rijkswaterstaat Waterinfo | Netherlands | **14/18** | Rhine/Meuse delta; salt intrusion data; world's oldest water authority |
| [german-state-agencies](german-state-agencies.md) | German State Environment Agencies | Germany | **12/18** | Bavaria GKD has real-time continuous WQ; fragmented across 16 states |
| [nz-lawa](nz-lawa.md) | NZ LAWA Water Quality | New Zealand (national) | **12/18** | National trend analysis; recreational WQ; Southern Hemisphere |
| [uk-ea-water-quality](uk-ea-water-quality.md) | UK Environment Agency WQ Explorer | England | **11/18** | Platform in migration; old API endpoints returning 404 |
| [ireland-epa-hydronet](ireland-epa-hydronet.md) | Irish EPA HydroNet | Ireland | **10/18** | HydroNet portal unreachable during testing; Q-value unique |

## Recommendation

**Top pick**: USGS NWIS Water Quality (18/18) — this is the obvious winner. It uses the exact same API already integrated in usgs-iv/, just requesting water quality parameter codes (dissolved oxygen, temperature, pH, conductivity, turbidity, continuous nitrate). The extension is trivial and the data is gold-standard.

**Best European API**: Hub'Eau France (17/18) — a model for how national water quality data should be exposed. Clean REST, JSON/GeoJSON/CSV, no auth, 25K+ stations with 265M analyses. Includes both surface water and drinking water quality through the same platform. Covers French overseas territories (Caribbean, Indian Ocean, South America).

**Satellite/model approach**: Copernicus Marine Service (16/18) is complementary to all in-situ sources — provides spatially continuous ocean water quality (chlorophyll, turbidity, HAB detection) from satellite and model data. Different use case, different strengths.

**Research-grade**: NEON (15/18) provides 7-parameter continuous sensor data at 34 aquatic sites with a 30-year commitment. Not real-time (monthly releases), but unmatched for ecological trend analysis.

**Pan-European context**: EEA Waterbase (14/18) and EU Bathing Water (14/18) provide regulatory compliance frameworks. Not real-time, but standardized across 30+ countries. Rijkswaterstaat (14/18) adds unique Dutch delta water management data.

**Watch list**: UK EA Water Quality is in platform transition — revisit once the new API stabilizes. Bavaria GKD is the most promising individual European real-time continuous WQ source. NZ LAWA has excellent data but needs an API.

## Note on Water Quality Data

Real-time continuous water quality monitoring is significantly less common than real-time flow/level monitoring. Most water quality programs still rely on discrete grab samples with laboratory analysis. The USGS continuous WQ network is among the largest in the world. In Europe, real-time continuous WQ monitoring is growing but still primarily at a few hundred select stations per country.

Hub'Eau (France) and Copernicus Marine represent two different approaches to filling this gap: Hub'Eau by aggregating decades of grab sample data into a superb API; Copernicus by providing satellite-derived spatially continuous water quality data. Both are valuable for different use cases.
