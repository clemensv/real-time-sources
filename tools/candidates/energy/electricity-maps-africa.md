# Electricity Maps — African Zones

- **Country/Region**: Pan-African (South Africa, Morocco, Egypt, Tunisia, Libya, Nigeria, Ghana, Kenya, Ethiopia, Tanzania, Senegal, Côte d'Ivoire, and 30+ more)
- **Endpoint**: `https://api.electricitymap.org/v3/zones`
- **Protocol**: REST
- **Auth**: API key (free tier for non-commercial use)
- **Format**: JSON
- **Freshness**: Real-time to hourly (varies by zone data availability)
- **Docs**: https://static.electricitymaps.com/api/docs/index.html
- **Score**: 13/18

## Overview

Electricity Maps (formerly electricityMap) tracks real-time electricity generation,
carbon intensity, and power flows for countries worldwide. Their zone list confirms
coverage for virtually every African country — from Angola to Zimbabwe.

For most African countries, the data is classified as `TIER_C` (estimated/modeled rather
than real-time metered), but key countries like South Africa (`ZA`) have better data
availability. This makes it the most comprehensive source for Africa-wide electricity
grid carbon intensity tracking.

## Endpoint Analysis

**Verified live** — the `/v3/zones` endpoint returns all supported zones including:

African zones confirmed:
| Zone | Country | Tier |
|------|---------|------|
| ZA | South Africa | TIER_C |
| MA | Morocco | TIER_C |
| EG | Egypt | TIER_C |
| TN | Tunisia | TIER_C |
| NG | Nigeria | TIER_C |
| GH | Ghana | TIER_C |
| KE | Kenya | TIER_C |
| ET | Ethiopia | TIER_C |
| TZ | Tanzania | TIER_C |
| SN | Senegal | TIER_C |
| CI | Côte d'Ivoire | TIER_C |
| AO | Angola | TIER_C |
| BF | Burkina Faso | TIER_C |
| BI | Burundi | TIER_C |

Key data endpoints (require API key):
- `GET /v3/carbon-intensity/latest?zone=ZA` — Current carbon intensity
- `GET /v3/power-breakdown/latest?zone=ZA` — Generation by source
- `GET /v3/carbon-intensity/history?zone=ZA` — Historical data

## Integration Notes

- **API key required**: Free non-commercial tier available. Register at
  https://api-portal.electricitymaps.com/
- **Tier C caveats**: Most African zones use estimated data from ENTSO-E-style capacity
  models, not real-time metered generation. The data is useful but less precise than
  European/North American zones.
- **South Africa focus**: ZA likely has the best African data quality due to Eskom's
  centralized reporting. Morocco (MA) may also be reasonable given ONEE's infrastructure.
- **Bridge design**: Poll `/v3/power-breakdown/latest` for each African zone every
  15–30 minutes. Emit CloudEvents with generation mix (coal, gas, solar, wind, hydro).
- **Carbon intensity**: The carbon intensity data enables tracking of Africa's energy
  transition — a growing area of interest.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time for some zones, modeled for most |
| Openness | 1 | API key required |
| Stability | 3 | Well-maintained commercial platform |
| Structure | 3 | Clean JSON API |
| Identifiers | 2 | ISO country codes |
| Richness | 2 | Generation mix, carbon intensity, imports/exports |
