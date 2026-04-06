# Nile Basin Water Monitoring

- **Country/Region**: Nile Basin (Egypt, Sudan, South Sudan, Ethiopia, Uganda, Kenya, Tanzania, Rwanda, Burundi, DRC, Eritrea)
- **Endpoint**: Various (satellite altimetry, USDA-FAS reservoir monitoring)
- **Protocol**: REST
- **Auth**: Varies
- **Format**: JSON, CSV
- **Freshness**: Daily to weekly
- **Docs**: https://ipad.fas.usda.gov/cropexplorer/global_reservoir/
- **Score**: 11/18

## Overview

The Nile is Africa's most politically significant river — 11 countries, 300 million
people, and the Grand Ethiopian Renaissance Dam (GERD) controversy that has defined
East African geopolitics for a decade. Real-time monitoring of Nile Basin water levels
is critical for:

- **GERD filling**: Ethiopia's mega-dam on the Blue Nile — Egypt considers this an
  existential threat
- **Lake Victoria levels**: The Nile's source, critical for Uganda and Kenya
- **Aswan Dam (Lake Nasser)**: Egypt's water security
- **Flood management**: Seasonal Nile floods still affect Sudan

## Endpoint Analysis

Direct Nile Basin Initiative (NBI) API: **Not found** (404 on nilebasin.org/nbi-data)

Alternative data sources for Nile monitoring:

1. **USDA Foreign Agricultural Service — Global Reservoir Monitoring**:
   ```
   https://ipad.fas.usda.gov/cropexplorer/global_reservoir/
   ```
   Tracks reservoir levels for major African dams including Aswan/Lake Nasser,
   Lake Victoria, and potentially GERD.

2. **DAHITI (Database for Hydrological Time Series of Inland Waters)**:
   ```
   https://dahiti.dgfi.tum.de/api/v1/
   ```
   Satellite altimetry-derived water levels for African lakes and reservoirs.

3. **Copernicus Global Land Service — Water Bodies**:
   ```
   https://land.copernicus.eu/global/products/wb
   ```
   Satellite-derived water body extent monitoring.

4. **USGS/NASA GRACE satellite**:
   Groundwater and total water storage anomalies — detects large-scale water depletion.

## Integration Notes

- **Multi-source fusion**: No single API provides comprehensive Nile monitoring.
  Combine satellite altimetry (DAHITI), reservoir monitoring (USDA), and in-situ
  stations where available.
- **Lake Victoria**: The most monitored body — multiple agencies track levels due to
  its role as Nile source and impact on hydropower.
- **GERD political sensitivity**: GERD filling data is politically sensitive. Ethiopia
  controls the data. Satellite altimetry provides independent estimates.
- **Seasonal patterns**: The Blue Nile has dramatic seasonal variation (Ethiopian
  rainy season June–September). This drives annual flood risk in Sudan.
- **Research collaboration**: Academic groups at Columbia (IRI), ICPAC, and Egyptian
  institutions monitor Nile flows. Their data may become API-accessible.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily to weekly (satellite revisit) |
| Openness | 2 | Mixed — some open, some require registration |
| Stability | 2 | Multiple institutional sources |
| Structure | 2 | Varies by source |
| Identifiers | 1 | No unified identifier system |
| Richness | 2 | Water levels, area extent, storage estimates |
