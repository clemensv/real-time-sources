# Fingrid Open Data (Finland)

**Country/Region**: Finland
**Publisher**: Fingrid Oyj (Finnish TSO)
**API Endpoint**: `https://data.fingrid.fi/api/datasets/{id}/data`
**Documentation**: https://data.fingrid.fi/
**Protocol**: REST
**Auth**: API Key (free registration required)
**Data Format**: JSON, CSV
**Update Frequency**: 3 minutes (real-time), hourly (forecasts)
**License**: Creative Commons CC-BY 4.0

## What It Provides

Fingrid's Open Data platform provides real-time and historical data from Finland's power system. It covers generation, consumption, cross-border flows, and market data.

Key datasets (by variable ID):

- **Electricity production** — Total and by type (nuclear, hydro, wind, solar, CHP, condensing)
- **Electricity consumption** — Real-time total consumption
- **Cross-border flows** — Imports/exports with Sweden (SE1, SE3), Norway, Estonia, Russia
- **Wind power generation** — Real-time wind output and forecasts
- **Solar power generation** — Real-time solar output
- **Frequency** — Grid frequency (50 Hz ± deviations)
- **Reserve activations** — FCR-N, FCR-D, aFRR, mFRR
- **Electricity spot prices** — Finnish bidding area prices

## API Details

REST API requiring a free API key:

```
GET https://data.fingrid.fi/api/datasets/{variableId}/data
    ?startTime=2026-04-06T00:00:00Z
    &endTime=2026-04-06T23:59:59Z
    &format=json
    &pageSize=1000
    
Headers:
  x-api-key: YOUR_KEY
```

The API returns 401 without a valid API key. Registration is free at data.fingrid.fi.

Variable IDs are numeric (e.g., 192 for wind power production, 124 for electricity consumption). The full list of datasets and their IDs is browsable on the website.

Response structure includes timestamped value pairs with metadata about the dataset, update frequency, and units.

## Freshness Assessment

Real-time measurement data updates every 3 minutes. Forecast data (wind, solar, consumption) updates hourly or more frequently. Grid frequency data is near-instantaneous. The platform is operated by the TSO itself, so data freshness matches the operational systems.

## Entity Model

- **Variable ID**: Numeric dataset identifier (e.g., 192 = wind power production)
- **Time**: ISO 8601 timestamps, typically UTC
- **Value**: Measurement in MW (generation/consumption) or Hz (frequency) or €/MWh (prices)
- **Bidding Area**: FI (Finland)
- **Border**: SE1, SE3, EE, NO, RU connections

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 3-minute real-time updates |
| Openness | 2 | Free API key required (not fully open) |
| Stability | 3 | Government TSO, production platform |
| Structure | 3 | Clean JSON, well-structured, paginated |
| Identifiers | 2 | Numeric variable IDs (not self-describing) |
| Additive Value | 2 | Finland-specific; Nordic context with ENTSO-E overlap |
| **Total** | **15/18** | |

## Notes

- The website is primarily in Finnish (data.fingrid.fi), but the API and some documentation are in English.
- API key registration is free and straightforward.
- Finland's grid is interesting: significant nuclear, hydro, and rapidly growing wind power.
- Grid frequency data at sub-minute resolution is unusual and valuable for power systems research.
- Cross-border flows with Sweden and Estonia provide Nordic/Baltic interconnection visibility.
- Consider whether ENTSO-E Transparency Platform already covers this data adequately — Fingrid contributes to ENTSO-E but the direct API may be fresher.
