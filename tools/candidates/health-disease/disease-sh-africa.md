# disease.sh — African Disease Surveillance Data

- **Country/Region**: Pan-African (all 54 African countries)
- **Endpoint**: `https://disease.sh/v3/covid-19/countries/ZA,KE,NG,EG,GH,ET`
- **Protocol**: REST
- **Auth**: None
- **Format**: JSON
- **Freshness**: Daily updates
- **Docs**: https://disease.sh/docs/
- **Score**: 13/18

## Overview

disease.sh is an open API that aggregates disease surveillance data from multiple
authoritative sources (Johns Hopkins, WHO, Worldometers). While initially focused on
COVID-19, it provides a template for African disease surveillance data delivery.

For Africa, disease surveillance is critically important. The continent faces endemic
diseases (malaria, cholera, Ebola, Lassa fever, Rift Valley fever) alongside emerging
threats. The Africa CDC has been building regional surveillance capacity, and machine-
readable data access is growing.

## Endpoint Analysis

**Verified live** — returns structured JSON for African countries:

```json
{
  "country": "South Africa",
  "countryInfo": {
    "iso2": "ZA",
    "iso3": "ZAF",
    "lat": -29,
    "long": 24
  },
  "cases": 4076463,
  "todayCases": 0,
  "deaths": 102595,
  "recovered": 3912506,
  "active": 61362,
  "critical": 192,
  "population": 60756135,
  "continent": "Africa"
}
```

Additional endpoints:
| Endpoint | Description |
|---|---|
| `/v3/covid-19/countries/{iso2}` | Single country data |
| `/v3/covid-19/continents/Africa` | Africa aggregate |
| `/v3/covid-19/historical/{iso2}?lastdays=30` | 30-day history |
| `/v3/influenza/ihn/who?country=ZA` | Influenza surveillance |

Countries tested and verified: ZA (South Africa), KE (Kenya), NG (Nigeria), EG (Egypt),
GH (Ghana), ET (Ethiopia) — all returned live data.

## Integration Notes

- **Multi-disease bridge**: While COVID-19 data is the current focus, the API structure
  supports expansion to other disease surveillance feeds.
- **Africa CDC complement**: The Africa CDC publishes weekly outbreak reports but lacks
  a structured API. disease.sh provides the structured data layer.
- **WHO AFRO integration**: WHO African Regional Office data could complement this for
  diseases like cholera, measles, and Ebola outbreaks.
- **Polling frequency**: Daily is sufficient for epidemiological surveillance data.
- **Historical trends**: The `/historical` endpoint enables trend analysis — detect
  when daily case counts exceed thresholds.
- **Population normalization**: The `population` field enables per-capita calculations,
  essential for comparing countries of vastly different sizes.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily updates |
| Openness | 3 | No auth, open API |
| Stability | 2 | Community-maintained, not government-backed |
| Structure | 3 | Clean JSON, well-documented |
| Identifiers | 2 | ISO country codes |
| Richness | 1 | COVID-focused currently, expandable |
