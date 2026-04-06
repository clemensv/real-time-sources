# FEWS NET Famine Early Warning Data API

- **Country/Region**: Sub-Saharan Africa (plus Central America, Central Asia, Haiti)
- **Endpoint**: `https://fdw.fews.net/api/`
- **Protocol**: REST (Django REST Framework)
- **Auth**: None
- **Format**: JSON
- **Freshness**: Weekly to monthly updates (market prices weekly, IPC classifications quarterly)
- **Docs**: https://fews.net/fews-data/333
- **Score**: 14/18

## Overview

FEWS NET — the Famine Early Warning Systems Network — is a USAID-funded activity that
monitors food security conditions in 30+ countries, predominantly in Africa. The API
provides market food prices, IPC food security classifications, trade flows, and price
indices for hundreds of markets across the continent.

For Africa, food prices are a leading indicator of humanitarian crises. When the price
of maize in a Kenyan market doubles in a month, that's an early warning signal. This
data is critical for humanitarian response and makes an excellent CloudEvents source.

## Endpoint Analysis

**API root verified live** — returns full endpoint directory:

Key endpoints:
| Endpoint | Description | Data |
|---|---|---|
| `/api/market/` | Market locations | Coordinates, admin regions |
| `/api/marketprice/` | Price observations | Product, unit, price, date |
| `/api/marketpricefacts/` | Flattened price data | Optimized for analysis |
| `/api/ipcphase/` | IPC classifications | Phase 1–5 by region |
| `/api/ipcpopulation/` | Population in IPC phases | Affected population counts |
| `/api/country/` | Country metadata | ISO codes, regions |
| `/api/exchangerate/` | Currency exchange rates | For price normalization |

Market data sample (Kenya):
```json
{
  "id": 254229,
  "fnid": "KE0000M0104",
  "name": "Ahero",
  "country": "Kenya",
  "admin_1": "Kisumu",
  "admin_2": "Nyando",
  "fewsnet_region": "East Africa",
  "latitude": -0.17444,
  "longitude": 34.92034,
  "urban_rural": "Urban"
}
```

Query filters: `?country=KE`, `?format=json`, `?limit=N`

**Performance note**: The `ipcphase` and `marketpricefacts` endpoints can be slow
(timeouts observed during probing). Use `limit` parameters and cache aggressively.

## Integration Notes

- **Market price bridge**: Poll `/api/marketpricefacts/` weekly for each country. Emit
  a CloudEvent per market-product-date combination with price, unit, and currency.
- **IPC classification bridge**: Poll `/api/ipcphase/` quarterly. Emit events when
  classifications change — an escalation from Phase 2 to Phase 3 is a significant signal.
- **Country coverage**: ~20 African countries with active monitoring including Kenya,
  Ethiopia, Somalia, Nigeria, Niger, Mali, Chad, Sudan, South Sudan, DRC, Mozambique,
  Madagascar, Malawi, Zimbabwe, Burkina Faso, Senegal.
- **Data volume**: Hundreds of markets × dozens of products × weekly observations =
  substantial data. Design the bridge for batch processing.
- **Deduplication**: Use `fnid` (FEWS NET ID) as the stable identifier for markets.

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Weekly to monthly updates |
| Openness | 3 | No auth, USAID public data |
| Stability | 3 | USAID-funded, operational since 1985 |
| Structure | 3 | Clean JSON REST API |
| Identifiers | 2 | FNID system, but not globally recognized |
| Richness | 2 | Rich multi-dimensional food security data |
