# Ember — Global Electricity Data

**Country/Region**: Global (200+ countries)
**Publisher**: Ember (independent energy think tank, formerly Ember Climate)
**API Endpoint**: `https://ember-data-api-scg3n.ondigitalocean.app/ember/` (historical; may have migrated)
**Documentation**: https://ember-climate.org/data/data-tools/
**Protocol**: REST / bulk downloads
**Auth**: API key for programmatic access (data explorer is free)
**Data Format**: JSON, CSV
**Update Frequency**: Monthly (generation), annual (capacity and emissions)
**License**: CC BY 4.0

## What It Provides

Ember is a global energy think tank that produces the most comprehensive open dataset of electricity generation, capacity, and emissions data worldwide. Their Global Electricity Review and yearly data releases are widely cited by governments, media, and researchers.

Datasets:

- **Electricity generation** (monthly) — By country and fuel type, going back decades. Covers 200+ countries with standardized methodology.
- **Electricity capacity** (annual) — Installed capacity by fuel type and country
- **Electricity demand** (monthly) — Total electricity consumption by country
- **Power sector emissions** (annual) — CO2 emissions from electricity generation by country
- **Electricity intensity** — Carbon intensity of electricity (gCO2/kWh) by country

Data is derived from:
- National statistical offices
- ENTSO-E and European TSOs
- IEA data
- US EIA
- IRENA
- Custom research and verification

## API Details

Ember's data is available through multiple channels:

1. **Data Explorer** (web interface): https://ember-climate.org/data/data-tools/data-explorer/
2. **GitHub releases**: Annual data packages as CSV on GitHub
3. **API**: Historical API at `ember-data-api-scg3n.ondigitalocean.app` (returned 404 during testing — may have migrated or been deprecated)

The API endpoint format (when working):

```
GET https://ember-data-api-scg3n.ondigitalocean.app/ember/electricity_generation_monthly.json
    ?entity=Germany
    &start_date=2025-01
```

Current recommended access path is bulk CSV download from their data catalog or the GitHub repository.

## Freshness Assessment

Monthly electricity generation data is published with a ~2-month lag (e.g., January data available by March). Annual datasets are published in Q1 for the previous year. This is not real-time data — it's analytical/statistical data with rigorous methodology and cross-country comparability.

## Entity Model

- **Entity**: Country name or aggregate (World, EU, OECD, etc.)
- **Variable**: Generation, Capacity, Demand, Emissions, Intensity
- **Fuel Type**: Coal, Gas, Oil, Nuclear, Hydro, Wind, Solar, Bioenergy, Other Renewables, Other
- **Time**: Monthly or annual (YYYY-MM or YYYY)
- **Value**: TWh (generation), GW (capacity), MtCO2 (emissions), gCO2/kWh (intensity)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Monthly data with ~2-month lag; annual for emissions |
| Openness | 3 | CC BY 4.0, bulk downloads freely available |
| Stability | 3 | Established think tank, consistent methodology, widely cited |
| Structure | 2 | CSV bulk downloads are clean; API status uncertain |
| Identifiers | 3 | ISO country codes, standardized fuel type taxonomy |
| Additive Value | 3 | Only global cross-country comparable electricity dataset at this quality |
| **Total** | **15/18** | |

## Notes

- Ember data is reference-grade, not real-time. Its value is in cross-country comparison and historical trend analysis, not operational grid monitoring.
- The standardized methodology across 200+ countries makes this uniquely valuable for global comparisons.
- Ember's annual "Global Electricity Review" report is the definitive source for tracking the global energy transition.
- The API may have been deprecated in favor of bulk downloads — check their GitHub for the latest access method.
- Consider using Ember data as a contextual/reference layer alongside real-time APIs (e.g., understanding that Germany's renewable share has grown from 20% to 52% over a decade gives context to real-time generation data).
