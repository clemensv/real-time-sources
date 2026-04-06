# OCHA ReliefWeb API — African Humanitarian Alerts

- **Country/Region**: Pan-African
- **Endpoint**: `https://api.reliefweb.int/v1/reports?appname=apidoc&filter[field]=country&filter[value][]=Kenya&filter[value][]=Nigeria&filter[value][]=Ethiopia&limit=5`
- **Protocol**: REST
- **Auth**: None (appname parameter recommended)
- **Format**: JSON
- **Freshness**: Daily (new reports published continuously)
- **Docs**: https://apidoc.rwlabs.org/
- **Score**: 14/18

## Overview

ReliefWeb, managed by OCHA (UN Office for the Coordination of Humanitarian Affairs),
is the world's largest humanitarian information portal. Its API provides access to
situation reports, assessments, and alerts from every humanitarian crisis on the
continent.

Africa accounts for a disproportionate share of global humanitarian crises — conflict,
displacement, drought, floods, epidemics. ReliefWeb captures all of this in a structured,
searchable API that enables systematic monitoring.

## Endpoint Analysis

The ReliefWeb API is well-documented:
```
# Search reports for African countries
GET https://api.reliefweb.int/v1/reports?appname=rts
  &filter[field]=country.iso3
  &filter[value]=KEN
  &sort[]=date:desc
  &limit=10

# Search by disaster type
GET https://api.reliefweb.int/v1/disasters?appname=rts
  &filter[field]=country.iso3
  &filter[value]=NGA
  &sort[]=date:desc

# Get specific report
GET https://api.reliefweb.int/v1/reports/{id}
```

Key entity types: Reports, Disasters, Countries, Sources, Jobs, Training.

Filter capabilities: country, source, theme, disaster type, date range, language,
format, status.

## Integration Notes

- **Disaster monitoring bridge**: Poll `/v1/disasters` for African countries to detect
  new humanitarian crises. Emit CloudEvents for new disasters.
- **Report stream**: Poll `/v1/reports` for situation updates. High volume — filter by
  disaster or country for manageable event rates.
- **Text enrichment**: Reports contain rich narrative text. NLP processing could
  extract structured data (casualty counts, displacement figures, affected areas).
- **Multi-language**: Reports come in English, French, Arabic, Portuguese, Spanish —
  all relevant for Africa's linguistic diversity.
- **GLIDE numbers**: Disasters have GLIDE identification numbers — an international
  standard for disaster identification. Include in CloudEvents.
- **Complement GDACS**: ReliefWeb covers human-caused crises (conflict, displacement)
  that GDACS doesn't track. Together they provide comprehensive crisis monitoring.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily updates, new reports continuously |
| Openness | 3 | No auth, UN public data |
| Stability | 3 | UN/OCHA infrastructure, operational for 25+ years |
| Structure | 3 | Well-documented JSON API |
| Identifiers | 2 | ReliefWeb IDs, GLIDE numbers |
| Richness | 1 | Report metadata, crisis categorization |
