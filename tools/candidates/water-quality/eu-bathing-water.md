# EU Bathing Water Quality — European Environment Agency

**Country/Region**: EU/EEA member states (22,000+ bathing sites across ~30 countries)
**Publisher**: European Environment Agency (EEA), based on member state reporting under the EU Bathing Water Directive (2006/7/EC)
**API Endpoint**: `https://discodata.eea.europa.eu/sql` (Discodata SQL endpoint); download portal
**Documentation**: https://www.eea.europa.eu/en/topics/in-depth/water/european-bathing-water-quality
**Protocol**: SQL-over-HTTP (Discodata); file downloads
**Auth**: None
**Data Format**: JSON, CSV (via SQL endpoint); Excel (downloads)
**Update Frequency**: Annual (member states report by end of each bathing season)
**License**: EEA standard reuse policy (open, attribution required)

## What It Provides

Under the EU Bathing Water Directive, all member states must monitor and report the quality of designated bathing waters (beaches, lakes, rivers used for swimming). The EEA aggregates this into a pan-European dataset covering:

- **Microbiological quality**: Escherichia coli and intestinal enterococci concentrations
- **Classification**: Excellent, Good, Sufficient, or Poor — based on 4-year rolling percentile analysis
- **Site metadata**: location, type (coastal/inland), water body name
- **Country-level statistics**: percentage of bathing waters in each quality class

Coverage: ~22,000 bathing sites across EU/EEA countries, Albania, and Switzerland. Monitored annually during the bathing season (typically May–September in Northern Europe, longer in Mediterranean).

This is one of the most visible EU environmental datasets — beach quality ratings directly affect tourism and local economies.

## API Details

Data accessible through EEA Discodata SQL endpoint:

```
# Example query (table names may vary by reporting year)
GET https://discodata.eea.europa.eu/sql?query=SELECT TOP 10 * FROM [BathingWater].[latest].[BathingWater_Status]&type=CSV
```

Alternative access:
- **EEA DataHub**: Search and download at `https://www.eea.europa.eu/en/datahub`
- **Country profiles**: Per-country bathing water reports with interactive maps
- **WISE Bathing Water viewer**: `https://water.europa.eu/bathing/` — interactive map of all 22,000+ sites

The WISE viewer provides a map-based interface with per-site detail pages showing historical results and current classification.

## Freshness Assessment

Poor for real-time use. Annual reporting cycle — data is reported after each bathing season with several months delay. Classification is based on 4-year rolling datasets. This is a compliance/reporting dataset, not a real-time monitoring system.

However, individual member states increasingly publish near-real-time bathing water results during the season through national portals — the EEA dataset is the annual aggregation.

## Entity Model

- **Bathing Water**: EU ID, name, country, type (coastal/inland), coordinates, water body
- **Season Result**: year, E. coli percentile, enterococci percentile, classification
- **Sample**: date, E. coli count, enterococci count, other parameters
- **Classification**: Excellent/Good/Sufficient/Poor, based on Directive Annex I statistical criteria

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Annual reporting cycle with months of lag |
| Openness | 3 | Open data, no auth |
| Stability | 3 | EU Directive mandated; EEA institutional infrastructure |
| Structure | 2 | SQL endpoint + downloads; WISE viewer is well-structured |
| Identifiers | 3 | EU bathing water IDs; WFD water body codes; country codes |
| Additive Value | 3 | 22K+ sites across 30 countries; tourism-relevant; highly visible |
| **Total** | **14/18** | |

## Notes

- This dataset is a compliance/summary dataset — not for real-time beach water quality alerts. For real-time alerts, look at national systems.
- The political impact is significant — "Poor" classification can require beach closure and mandatory improvement measures.
- Tourism economics make this data commercially relevant — beach quality ratings affect property values and visitor numbers.
- Several EU countries now publish real-time bathing water results via apps and APIs during the season (e.g., Scotland's "SEPA bathing waters" page with near-real-time E. coli results).
- Climate change is increasing harmful algal bloom risks at bathing sites — expect monitoring to intensify.
- The 2006 Directive is under revision — new Directive expected to expand monitoring to additional parameters and potentially require real-time reporting.
