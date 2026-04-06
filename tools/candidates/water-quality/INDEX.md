# Water Quality — Candidate Data Sources

Research candidates for real-time and continuous water quality monitoring APIs.

**Already covered in repo**: USGS IV (`usgs-iv/`) includes some water quality parameters as part of instantaneous values

## Candidates

| Slug | Source | Country/Region | Score | Key Strength |
|------|--------|---------------|-------|-------------|
| [usgs-nwis-wq](usgs-nwis-wq.md) | USGS NWIS Water Quality (IV) | USA (3,000+ sites) | **18/18** | Same proven API as usgs-iv; just different parameter codes |
| [eea-waterbase](eea-waterbase.md) | EEA Waterbase / WISE | EU (39 countries) | **14/18** | Pan-European; WFD-standardized; annual not real-time |
| [german-state-agencies](german-state-agencies.md) | German State Environment Agencies | Germany | **12/18** | Bavaria GKD has real-time continuous WQ; fragmented across 16 states |
| [uk-ea-water-quality](uk-ea-water-quality.md) | UK Environment Agency WQ Explorer | England | **11/18** | Platform in migration; old API endpoints returning 404 |
| [ireland-epa-hydronet](ireland-epa-hydronet.md) | Irish EPA HydroNet | Ireland | **10/18** | HydroNet portal unreachable during testing; Q-value unique |

## Recommendation

**Top pick**: USGS NWIS Water Quality (18/18) — this is the obvious winner. It uses the exact same API already integrated in usgs-iv/, just requesting water quality parameter codes (dissolved oxygen, temperature, pH, conductivity, turbidity, continuous nitrate). The extension is trivial and the data is gold-standard.

**For European coverage**: EEA Waterbase (14/18) provides the broadest geographic scope but is a regulatory reporting database with 1-2 year lag, not a real-time monitoring system. Best used as a reference/historical dataset.

**Watch list**: UK EA Water Quality is in platform transition — revisit once the new API stabilizes. Bavaria GKD is the most promising individual European real-time continuous WQ source.

## Note on Water Quality Data

Real-time continuous water quality monitoring is significantly less common than real-time flow/level monitoring. Most water quality programs still rely on discrete grab samples with laboratory analysis. The USGS continuous WQ network is among the largest in the world. In Europe, real-time continuous WQ monitoring is growing but still primarily at a few hundred select stations per country.
