# Global Solar Atlas API — Africa Solar Irradiance

- **Country/Region**: Pan-African
- **Endpoint**: `https://api.globalsolaratlas.info/data/lta?loc={lat},{lon}`
- **Protocol**: REST
- **Auth**: None (open access)
- **Format**: JSON
- **Freshness**: Static (long-term averages); useful as reference data
- **Docs**: https://globalsolaratlas.info/
- **Score**: 10/18

## Overview

The Global Solar Atlas, funded by the World Bank and developed by Solargis, provides
solar resource data for any location on Earth. Africa has the world's highest solar
irradiance potential — the Sahara alone receives enough solar energy to power the
entire world — yet has the lowest solar deployment.

This API provides long-term average solar irradiance data (GHI, DNI, DIF, GTI) and
photovoltaic power potential for any African location. While not real-time, it's the
essential reference layer for evaluating solar energy deployment across the continent.

## Endpoint Analysis

**Portal verified** — the Global Solar Atlas site is active with the API base URL at
`https://api.globalsolaratlas.info/`.

Key endpoints:
```
# Long-term average data for a location
GET /data/lta?loc=-1.29,36.82  (Nairobi)

# PV power potential
GET /data/pv-potential?loc=-33.92,18.42  (Cape Town)
```

Expected response includes:
- **GHI**: Global Horizontal Irradiance (kWh/m²/year)
- **DNI**: Direct Normal Irradiance
- **DIF**: Diffuse Horizontal Irradiance
- **GTI**: Global Tilted Irradiance (optimal angle)
- **PVOUT**: Photovoltaic power output potential (kWh/kWp/year)
- Monthly breakdowns

Typical African values:
- Sahara: GHI > 2,200 kWh/m²/year
- East Africa highlands: GHI ~1,800–2,100 kWh/m²/year
- Southern Africa: GHI ~1,900–2,300 kWh/m²/year
- West Africa coast: GHI ~1,500–1,900 kWh/m²/year

## Integration Notes

- **Reference data bridge**: While not real-time, a bridge could emit CloudEvents for
  solar potential assessments when queried for new locations. Useful as enrichment
  data for energy bridges.
- **Combine with weather**: Pair GSA long-term averages with real-time weather data
  (Open-Meteo cloud cover) to estimate current solar generation potential.
- **Site assessment**: For any new solar installation in Africa, this is the first API
  to consult. Embed in a CloudEvents workflow.
- **World Bank backing**: Excellent stability and data quality.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 0 | Static long-term averages |
| Openness | 3 | No auth, World Bank public data |
| Stability | 3 | World Bank/Solargis infrastructure |
| Structure | 2 | JSON API |
| Identifiers | 0 | Coordinate-based, no station IDs |
| Richness | 2 | GHI, DNI, DIF, PVOUT, monthly data |
