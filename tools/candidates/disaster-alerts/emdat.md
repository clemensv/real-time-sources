# EM-DAT International Disaster Database
**Country/Region**: Global
**Publisher**: Centre for Research on the Epidemiology of Disasters (CRED), Université catholique de Louvain
**API Endpoint**: `https://api.emdat.be/`
**Documentation**: https://doc.emdat.be/ (GraphQL schema)
**Protocol**: GraphQL
**Auth**: Likely required for full access (free tier available)
**Data Format**: JSON (GraphQL)
**Update Frequency**: Continuous (as disaster events are recorded/updated)
**License**: Academic use free, commercial license available

## What It Provides
EM-DAT is the world's most comprehensive international disaster database, maintained since 1988. It records:
- Natural disasters: earthquakes, floods, storms, droughts, wildfires, volcanic eruptions, epidemics
- Technological disasters: industrial accidents, transport accidents, miscellaneous
- Impact data: deaths, injuries, affected population, economic damage
- Temporal coverage: 1900 to present (systematic from 1988)
- Over 26,000 disaster events recorded

Inclusion criteria: ≥10 deaths, ≥100 affected, declaration of emergency, or call for international assistance.

## API Details
- **GraphQL endpoint**: `https://api.emdat.be/`
- **GraphQL Explorer**: Interactive GraphiQL interface at root URL (confirmed working, HTTP 200)
- **Query capabilities**:
  - Filter by disaster type, country, date range, severity
  - Aggregate statistics (deaths, damage, frequency by region/type/year)
  - Trend analysis across decades
  - Country-level disaster profiles
- **Server**: nginx/1.20.1
- **Expected query patterns**:
  ```graphql
  query {
    disasters(country: "USA", year: 2024, type: "Flood") {
      disNo, country, type, subtype, startDate, endDate,
      totalDeaths, totalAffected, totalDamageUSD
    }
  }
  ```

## Probe Results
```
Root URL: HTTP 200 OK
Content-Type: text/html (GraphiQL explorer)
Server: nginx/1.20.1
Assessment: GraphQL endpoint operational with interactive explorer
```

## Freshness Assessment
Good for historical and recent events. EM-DAT is continuously updated as disasters are recorded and validated. Data for recent events may have a delay of days to weeks as impact numbers are confirmed. Not real-time alerting — this is a disaster impact database rather than a warning system.

## Entity Model
- **Disaster** (disNo — EM-DAT disaster number, country, ISO3, region, continent)
- **Classification** (group, subgroup, type, subtype)
- **Temporal** (startDate, endDate, year)
- **Impact** (totalDeaths, totalAffected, totalDamage, insuredDamage)
- **Geographic** (country, ISO3, location, lat, lon)
- **Source** (data sources, validation status)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 1 | Historical database, not real-time alerts |
| Openness | 2 | GraphQL available, may need registration |
| Stability | 3 | 36+ years of operation, academic institution |
| Structure | 3 | GraphQL with typed schema |
| Identifiers | 3 | Stable disaster numbers (disNo), ISO3 country codes |
| Additive Value | 3 | Only comprehensive global disaster impact database |
| **Total** | **15/18** | |

## Notes
- Complements real-time alerting sources (GDACS, NINA) with historical context and impact data
- GraphQL interface enables flexible querying without multiple endpoint variants
- EM-DAT disaster numbers are widely used in academic literature and policy
- Economic damage figures are normalized to USD
- Used by UN, World Bank, IPCC, and hundreds of academic institutions
- May require CRED account registration for programmatic access beyond the explorer
