# EEA Waterbase — WISE (Water Information System for Europe)

**Country/Region**: European Union / EEA member states (39 countries)
**Publisher**: European Environment Agency (EEA)
**API Endpoint**: `https://discodata.eea.europa.eu/sql` (SQL endpoint); various download portals
**Documentation**: https://www.eea.europa.eu/en/datahub ; https://discodata.eea.europa.eu/
**Protocol**: SQL-over-HTTP (Discodata/Dremio), file downloads
**Auth**: None
**Data Format**: JSON, CSV (via SQL endpoint); Excel, CSV (downloads)
**Update Frequency**: Annual reporting cycle (member states report to EEA under Water Framework Directive)
**License**: EEA standard reuse policy (open, attribution required)

## What It Provides

Waterbase is the EEA's database of water quality and quantity data reported by EU member states under the Water Framework Directive (WFD) and related directives. It covers:

- **Surface water quality**: chemical and ecological status of rivers, lakes, transitional/coastal waters
- **Groundwater quality**: chemical status of groundwater bodies
- **Bathing water quality**: EU bathing water monitoring results
- **Urban waste water treatment**: UWWTD reporting data
- **Emissions to water**: pollutant release and transfer data

Key datasets:
- WISE SoE (State of Environment) — disaggregated monitoring data: individual measurements of determinands (nutrients, metals, pesticides, etc.) at specific monitoring points
- WISE WFD — aggregated assessments: status classifications of water bodies

The scope is vast — potentially millions of measurements across thousands of monitoring stations in 39 countries.

## API Details

**Discodata SQL endpoint**: `https://discodata.eea.europa.eu/sql`

Discodata is EEA's SQL-over-HTTP service built on Dremio. Queries use SQL Server-like syntax:

```
https://discodata.eea.europa.eu/sql?query=SELECT TOP 10 * FROM [WISE_SoE_WaterQuality].[latest].[DisaggregatedData]&type=CSV
```

Note: Testing returned "Invalid object name" errors — the exact table/schema names may have changed or require specific knowledge of the current data catalog. The Discodata web interface at `https://discodata.eea.europa.eu/` provides a database explorer to discover available tables.

**Alternative access**:
- EEA DataHub: `https://www.eea.europa.eu/en/datahub` — search and download datasets
- Direct dataset downloads: Excel/CSV files per reporting year
- SPARQL endpoint for linked data

## Freshness Assessment

Poor for real-time use. Waterbase is an annual reporting database — member states submit monitoring data annually with a 1-2 year delay. The latest available data is typically from 2+ years ago. This is a regulatory compliance database, not an operational monitoring system.

However, the historical depth and geographic breadth are unmatched — decades of standardized water quality data across all of Europe.

## Entity Model

- **Monitoring Site**: EEA monitoring point ID, country, water body name, water body type (river/lake/coastal/transitional/groundwater)
- **Water Body**: EU WFD water body code, name, type, river basin district
- **Measurement**: monitoring point, date, determinand (parameter), value, unit, LOQ, sample depth
- **Determinand**: EEA code, name, CAS number, group (nutrients/metals/pesticides/organics)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Annual reporting, 1-2 year delay — not real-time |
| Openness | 3 | Open data, no auth required |
| Stability | 3 | EU institutional infrastructure, legally mandated under WFD |
| Structure | 2 | SQL endpoint exists but table discovery is difficult; also file downloads |
| Identifiers | 3 | EEA monitoring point IDs, WFD water body codes, CAS numbers for determinands |
| Additive Value | 3 | Pan-European coverage, standardized parameters — nothing else provides this |
| **Total** | **14/18** | |

## Notes

- This is NOT a real-time monitoring system. It's a regulatory reporting database. Include it only if the goal extends to historical/reference water quality data.
- The Discodata SQL endpoint is powerful but requires knowing the exact table/schema names, which change between reporting versions. The web-based database explorer is needed for discovery.
- The real value is in cross-country comparisons — standardized water quality data from Iceland to Turkey, using common determinand codes and monitoring methodologies.
- For real-time European water quality data, look at individual member state systems (UK EA, Irish EPA, German state agencies) rather than EEA aggregated reporting.
- The Water Framework Directive mandates 6-year reporting cycles, with annual status updates for some parameters.
- Potential to combine with the existing tools/eurowater directory in this repository.
