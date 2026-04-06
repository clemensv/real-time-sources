# India data.gov.in — Real-Time Commodity Market Prices (Mandi)

**Country/Region**: India
**Publisher**: Department of Agriculture and Farmers Welfare, Ministry of Agriculture
**API Endpoint**: `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070`
**Documentation**: https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi
**Protocol**: REST (JSON)
**Auth**: API Key (free registration at data.gov.in)
**Data Format**: JSON
**Update Frequency**: Daily (market prices updated as mandis report)
**License**: India Government Open Data License (GODL)

## What It Provides

India's agricultural commodity market price feed — live from 2,500+ mandis (agricultural markets) across India. This isn't weather or environmental data, but it's a real-time economic data feed that intersects with weather impacts (drought, flood, monsoon) on food prices.

The feed covers:
- **17,833 daily price records** (at time of probe)
- **Commodities**: Potato, onion, tomato, wheat, rice, cotton, soybean, castor seed, and hundreds more
- **Markets**: Named mandis across all states (Roorkee APMC, KUKARMUNDA APMC, etc.)
- **Price data**: Min price, max price, modal price per commodity per market per day

### Probed Response (live, April 6, 2026)

```json
{
  "status": "ok",
  "total": 17833,
  "records": [
    {
      "state": "Gujarat",
      "district": "Surat",
      "market": "KUKARMUNDA APMC",
      "commodity": "Castor Seed",
      "variety": "Castor seed",
      "grade": "Local",
      "arrival_date": "06/04/2026",
      "min_price": 5975,
      "max_price": 6125,
      "modal_price": 6065
    }
  ]
}
```

### Why This Matters for Real-Time Sources

India's onion and tomato prices are literally political — governments have fallen over food price spikes. The correlation between monsoon performance, flood damage, and market prices creates a weather-agriculture data fusion opportunity:
- Monsoon failure → drought → price spike → food inflation
- Flood damage → supply disruption → localized price spikes
- Cross-referencing with IMD weather data and CPCB data creates a multi-domain picture

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Daily updates; confirmed live |
| Openness | 2 | Free API key; GODL license |
| Stability | 3 | data.gov.in is India's national open data platform; stable since 2012 |
| Structure | 3 | Clean JSON; filterable by state, district, market, commodity |
| Identifiers | 2 | Market names; commodity names; state/district hierarchy |
| Additive Value | 2 | Unique economic data; weather-agriculture correlation; political significance |
| **Total** | **14/18** | |

## Integration Notes

- Different domain from typical environmental data, but intersects with weather/hydrology impact assessment
- 17,833 daily records — manageable payload
- Prices in Indian Rupees (INR) per quintal (100 kg)
- Consider as complementary to India weather and agriculture data
- CloudEvents: one event per commodity-market-day price update

## Verdict

Novel economic real-time feed from India's agricultural markets. While not a traditional environmental data source, the weather-food price correlation makes this uniquely interesting. The data.gov.in platform provides clean, documented API access. Best used in combination with India's weather and water data for multi-domain impact analysis.
