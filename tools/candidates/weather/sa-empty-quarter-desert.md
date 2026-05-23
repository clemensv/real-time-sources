# Empty Quarter (Rub' al Khali) - Desert Weather and Dust Storm Monitoring

- **Country/Region**: Saudi Arabia (southern Saudi Arabia, Empty Quarter desert)
- **Endpoint**: Part of NCM weather network (see separate NCM candidate)
- **Protocol**: REST (Meteomatics platform)
- **Auth**: API key required
- **Format**: JSON
- **Freshness**: Hourly+
- **Docs**: https://api-doc.ncm.gov.sa (NCM weather API)
- **Score**: 10/18

## Overview

The **Rub' al Khali** (الربع الخالي, "Empty Quarter") is the world's largest continuous sand desert, covering **650,000 km²** across southern Saudi Arabia, UAE, Oman, and Yemen. Key facts:

- **Largest sand desert** — Larger than France
- **Extreme conditions**:
  - **Temperature**: -12°C to +56°C (night lows in winter to extreme summer highs)
  - **Rainfall**: <30mm/year (one of Earth's driest places)
  - **Sand dunes**: Up to 250m tall
  - **No permanent human settlement** (except oil camps)
- **Oil reserves**: The Empty Quarter sits atop Saudi Arabia's largest oil fields (Shaybah, Ghawar)
- **Dust storms**: Major source of Middle East dust storms (haboobs)

**Meteorological significance**:
- **Dust storm formation** — Empty Quarter dunes are the primary source of dust that affects Riyadh, Kuwait, Qatar, UAE
- **Extreme desert climate** — Benchmark for climate models, heat stress research
- **Oil operations** — Saudi Aramco operates remote drilling camps requiring weather forecasting

## NCM Weather Stations in the Empty Quarter

The **National Center for Meteorology (NCM)** operates weather stations in and around the Empty Quarter, including:

- **Shaybah** — Oil field, 800 km southeast of Riyadh (24°31'N, 53°59'E)
- **Najran** — Southern border city, edge of Empty Quarter (17°37'N, 44°13'E)
- **Al-Ahsa** — Eastern oasis, northern edge (25°26'N, 49°38'E)
- **Remote automatic stations** — Solar-powered sensors in the deep desert (exact locations not public)

**Data products** (if accessible via NCM API):
1. **Temperature** — Extreme heat (50-56°C) in summer
2. **Humidity** — Very low (<10% in summer)
3. **Wind speed and direction** — Dust storm drivers
4. **Visibility** — Reduced during dust storms (<50m)
5. **Dust/PM10 concentrations** — Airborne sand
6. **Solar radiation** — Extreme (>1,000 W/m² peak)
7. **Rainfall** — Rare but intense (flash floods in wadis)

**Update frequency**: Hourly or better (NCM's Meteomatics platform supports sub-hourly).

## Endpoint Analysis

**NCM API**: `https://api-mm.ncm.gov.sa/`

See the separate **NCM Meteomatics API** candidate for full details. The Empty Quarter weather data would be a **subset of NCM's national coverage**, accessed via:

```
GET https://api-mm.ncm.gov.sa/{datetime}/{parameters}/{lat,lon}/json
```

Example (temperature at Shaybah oil field):
```
GET https://api-mm.ncm.gov.sa/2024-06-15T12:00:00Z/t_2m:C/24.52,53.98/json
```

**Auth barrier**: NCM's API requires an **API key** (401 Unauthorized without auth). See NCM candidate for details.

## Integration Notes

- **Subset of NCM weather API**: Empty Quarter data is **not a separate source** — it is part of NCM's national weather network. Building a dedicated Empty Quarter bridge would duplicate the NCM source.
- **Unique value**: Empty Quarter weather is **scientifically significant** for:
  - **Extreme desert climate** — Hottest surface temperatures on Earth (56°C recorded)
  - **Dust storm forecasting** — Empty Quarter dunes are the source of Gulf dust events
  - **Oil operations** — Weather data critical for remote drilling camps (heatstroke, helicopter operations)
- **Station sparsity**: Weather stations in the Empty Quarter are **extremely sparse** (one per 100,000 km²) due to remoteness. Most data is from **satellite** or **reanalysis models**, not ground stations.
- **Alternative: Satellite data** — For Empty Quarter weather, satellite-based products are more comprehensive:
  - **MODIS** (NASA) — Surface temperature, dust detection (daily)
  - **Sentinel-3** (ESA) — Land surface temperature (daily)
  - **CAMS** (Copernicus) — Dust aerosol forecasts (hourly)

**Comparison with other deserts**:

| Desert | Country | Public weather data? | API? |
|--------|---------|----------------------|------|
| **Rub' al Khali** | Saudi Arabia (+ UAE, Oman, Yemen) | ✅ Via NCM | ✅ NCM API (auth required) |
| Sahara | North Africa | ✅ Via national met services | ✅ Some (Egypt, Morocco) |
| Atacama | Chile | ✅ Via DMC | ✅ REST |
| Death Valley | USA | ✅ Via NOAA | ✅ REST |
| Gobi | Mongolia/China | ✅ Via national services | ✅ Some |

**Conclusion**: Empty Quarter weather is **accessible via NCM's national API** (if auth is obtained), but is **not a distinct source**.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly or better (NCM API) |
| Openness | 1 | API key required (NCM Meteomatics platform) |
| Stability | 3 | NCM is the official national met service |
| Structure | 2 | JSON (Meteomatics format) |
| Identifiers | 1 | Coordinates-based (no station IDs in NCM docs) |
| Additive value | 0 | **Duplicate of NCM source** (same API, subset of coverage) |

**Total: 10/18** (if NCM API is accessible)  
**Actual: 10/18** (no additional penalty; scored as part of NCM)

**Verdict**: ⏭️ **Reference** — Empty Quarter weather is **not a separate source**. It is a **geographic subset of the NCM national weather API**. If NCM API access is obtained (see NCM candidate), Empty Quarter stations are automatically included.

**Recommended action**:
1. **Focus on NCM national API** — Do not build a separate Empty Quarter bridge; it duplicates NCM.
2. **If NCM API is built**, document Empty Quarter stations as a **high-value subset** for:
   - Extreme temperature research (56°C records)
   - Dust storm forecasting (source region)
   - Oil industry operations (Shaybah, Ghawar fields)
3. **Satellite alternative** — For comprehensive Empty Quarter coverage, use **MODIS**, **Sentinel-3**, or **CAMS** dust products (global satellite data, no auth required).

Do not build a dedicated Empty Quarter bridge — it is redundant with NCM national coverage.
