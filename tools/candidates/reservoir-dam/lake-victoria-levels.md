# Lake Victoria Water Levels

- **Country/Region**: East Africa (Kenya, Uganda, Tanzania)
- **Endpoint**: Multiple satellite altimetry sources
- **Protocol**: REST / File download
- **Auth**: Varies (some open, some require registration)
- **Format**: CSV, JSON, NetCDF
- **Freshness**: Daily to weekly (satellite revisit cycle)
- **Docs**: https://dahiti.dgfi.tum.de/en/
- **Score**: 11/18

## Overview

Lake Victoria is the world's largest tropical lake, Africa's largest lake, and the
primary source of the White Nile. Its water level affects:
- **Hydropower**: Nalubaale (Owen Falls) Dam and Kiira Dam in Uganda
- **Fisheries**: 30+ million people depend on Lake Victoria fish
- **Transport**: Lake ferries connecting Kenya, Uganda, Tanzania
- **Flooding**: Lake level rise has displaced lakeside communities

The lake's level has risen dramatically since 2019, flooding communities and
infrastructure. Real-time monitoring is critical.

## Endpoint Analysis

Satellite altimetry sources for Lake Victoria:

1. **DAHITI (TU Munich)**:
   ```
   https://dahiti.dgfi.tum.de/api/v1/water-level-altimetry/
     ?lake=Victoria&format=json
   ```
   Provides satellite-derived water levels from Sentinel-3, Jason, etc.

2. **USDA Global Reservoir & Lake Monitor**:
   ```
   https://ipad.fas.usda.gov/cropexplorer/global_reservoir/
   ```
   Weekly area and level estimates from satellite data.

3. **Copernicus Global Land Service**:
   Water body extent monitoring using Sentinel-2.

4. **NASA/USDA GRACE-FO**:
   Total water storage anomalies for the Lake Victoria basin.

Historical context:
- Lake Victoria reached record highs in 2020-2021
- Levels respond to both rainfall (short-term) and climate patterns (ENSO)
- The Jinja dam releases control outflow but cannot fully regulate levels

## Integration Notes

- **DAHITI preferred**: Most accessible API for lake altimetry data. Registration
  required but free for research.
- **Multi-lake extension**: DAHITI covers 200+ African lakes and reservoirs. Build
  a bridge that works for all of them: Tanganyika, Malawi, Turkana, Volta, Kariba,
  Cahora Bassa, etc.
- **Event model**: Emit CloudEvents when lake levels exceed historical thresholds —
  early warning for flooding or drought.
- **Combine with river data**: Lake Victoria inflow comes from dozens of rivers.
  Combine with GloFAS river discharge forecasts for a complete picture.
- **Political significance**: Lake Victoria is shared by three countries with competing
  water use priorities. Level data informs transboundary negotiations.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily to weekly (satellite revisit) |
| Openness | 2 | Registration required for most sources |
| Stability | 2 | Academic sources, satellite dependent |
| Structure | 2 | CSV/JSON from APIs |
| Identifiers | 1 | Lake name/DAHITI ID |
| Richness | 2 | Water level, area, volume estimates |
