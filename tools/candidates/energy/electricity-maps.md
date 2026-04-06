# Electricity Maps API

**Country/Region**: Global (~200 zones across 70+ countries)
**Publisher**: Electricity Maps (formerly electricityMap, by Tomorrow)
**API Endpoint**: `https://api.electricitymap.org/v3/`
**Documentation**: https://static.electricitymaps.com/api/docs/index.html
**Protocol**: REST
**Auth**: API Key (free tier available, commercial tiers for production)
**Data Format**: JSON
**Update Frequency**: ~5 minutes (real-time), hourly (historical)
**License**: Proprietary / Commercial (free tier with attribution)

## What It Provides

Electricity Maps is a global aggregator that collects, normalizes, and enriches electricity data from TSOs worldwide. It provides a unified API for carbon intensity and power breakdown data across ~200 electricity zones.

Key data offerings:

- **Carbon intensity** — Real-time and historical carbon intensity (gCO2eq/kWh) per zone, using lifecycle emission factors
- **Power breakdown** — Generation mix by source (wind, solar, hydro, nuclear, gas, coal, oil, biomass, geothermal, unknown)
- **Power consumption/production** — Total consumption and production per zone
- **Import/export** — Cross-zone electricity flows
- **Forecasts** — Carbon intensity forecasts (24-48h ahead)

Coverage spans Europe, North America, Australia, parts of Asia, and South America.

## API Details

```
GET https://api.electricitymap.org/v3/carbon-intensity/latest?zone=DE
Headers:
  auth-token: YOUR_TOKEN
```

Key endpoints:
- `/v3/carbon-intensity/latest?zone={zone}` — Latest carbon intensity
- `/v3/carbon-intensity/history?zone={zone}` — 24h history
- `/v3/power-breakdown/latest?zone={zone}` — Current generation mix
- `/v3/zones` — List all available zones
- Health check: `/health` returns `{"status":"UP"}`

Zone codes follow ISO 3166 with subdivisions (e.g., DE, FR, US-CAL-CISO, AU-NSW, JP-TK, BR-S).

## Freshness Assessment

Data freshness varies by zone — well-covered zones (most of Europe, US, Australia) update every 5-15 minutes. Less-covered zones may have longer delays. The API aggregates from primary sources (ENTSO-E, EIA, AEMO, etc.) and adds carbon intensity calculations. The health endpoint confirmed the service is running.

## Entity Model

- **Zone**: ~200 electricity zones identified by ISO-ish codes (DE, FR, US-CAL-CISO, etc.)
- **Carbon Intensity**: gCO2eq/kWh (lifecycle, not direct)
- **Power Sources**: wind, solar, hydro, nuclear, gas, coal, oil, biomass, geothermal, unknown, battery discharge
- **Flow**: Import/export between adjacent zones
- **Time**: UTC timestamps

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 5-15 min depending on zone; aggregator lag adds delay |
| Openness | 1 | Free tier exists but commercial license for production use |
| Stability | 3 | Well-funded company, production API, health endpoint UP |
| Structure | 3 | Clean JSON, well-documented, consistent zone model |
| Identifiers | 3 | Standardized zone codes, consistent global model |
| Additive Value | 3 | Unique global coverage and carbon intensity calculation |
| **Total** | **15/18** | |

## Notes

- The key value proposition is global normalization — one API to rule them all. For individual country coverage, primary TSO APIs will be fresher and more detailed.
- Electricity Maps discontinued their marginal emission data offering in 2025, citing concerns about accuracy and verifiability. Only average/lifecycle intensity is now provided.
- The free tier requires attribution and has rate limits. Commercial tiers start at ~$250/month.
- The open-source model underlying the data is at github.com/electricitymaps/electricitymaps-contrib — the data processing pipeline is transparent.
- Zone definitions can change; some zones are sub-national (US states, Australian states, Japanese regions).
- For this project, primary TSO APIs are likely more appropriate than Electricity Maps, unless global coverage is specifically needed.
