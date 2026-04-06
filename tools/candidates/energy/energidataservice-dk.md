# Energi Data Service (Energinet)

**Country/Region**: Denmark (DK1, DK2 bidding areas) + Nordic/European price areas
**Publisher**: Energinet (Danish TSO)
**API Endpoint**: `https://api.energidataservice.dk/dataset/{dataset_name}`
**Documentation**: https://www.energidataservice.dk/guides/api-guides
**Protocol**: REST
**Auth**: None (fully open, no API key)
**Data Format**: JSON, CSV, Excel
**Update Frequency**: 1 minute (PowerSystemRightNow), 5 minutes (CO2), hourly (prices)
**License**: Open Data (Danish public sector)

## What It Provides

Energi Data Service is Energinet's open data platform providing real-time and historical power system data for Denmark and connected Nordic/European markets.

Key datasets:

- **PowerSystemRightNow** — Minute-by-minute snapshot of the Danish power system: CO2 emissions, solar/wind generation, offshore/onshore wind, exchange flows with DE/NL/GB/NO/SE, imbalance, frequency reserves (aFRR, mFRR)
- **ElspotPrices** — Day-ahead electricity spot prices for DK1, DK2, and other European bidding areas (DE, NO, SE, FI, etc.)
- **CO2Emission** — 5-minute CO2 emission intensity
- **DeclarationProduction** — Production declarations by fuel type
- **PowerSystemBalancingDK** — Balancing market data

## API Details

Simple RESTful GET API with query parameters:

```
GET https://api.energidataservice.dk/dataset/PowerSystemRightNow?limit=2
```

Returns:

```json
{
  "total": 3872866,
  "records": [{
    "Minutes1UTC": "2026-04-06T10:23:00",
    "CO2Emission": 81.13,
    "SolarPower": 1755.94,
    "OffshoreWindPower": 83.50,
    "OnshoreWindPower": 2581.98,
    "Exchange_DK1_DE": 2438.05,
    "Exchange_DK1_NO": -1287.00,
    "aFRR_ActivatedDK1": 2.92,
    "ImbalanceDK1": 18.79
  }]
}
```

Parameters: `start`, `end` (with dynamic timestamps like `now-P1D`), `filter` (JSON), `columns`, `sort`, `limit`, `offset`. Download endpoints available for CSV/Excel/JSON.

Spot prices example:

```
GET https://api.energidataservice.dk/dataset/ElspotPrices?limit=2
```

Returns price data in DKK and EUR for all bidding areas.

## Freshness Assessment

The PowerSystemRightNow dataset updates every minute — this is among the freshest grid data available anywhere. Spot prices are published day-ahead. CO2 data updates every 5 minutes. The platform explicitly documents update frequencies per dataset.

## Entity Model

- **Bidding Area**: DK1 (Western Denmark), DK2 (Eastern Denmark), DE, NO, SE, FI, etc.
- **Time Resolution**: 1-minute (power system), 5-minute (CO2), hourly (prices)
- **Generation Types**: Solar, onshore wind, offshore wind, production ≥100MW, production <100MW
- **Exchange Flows**: Per border (DK1-DE, DK1-NL, DK1-GB, DK1-NO, DK1-SE, DK2-DE, DK2-SE, Bornholm-SE)
- **Balancing**: aFRR activation, mFRR activation, imbalance per area

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 1-minute updates for real-time data |
| Openness | 3 | No auth, no API key, open data |
| Stability | 3 | Government TSO, well-documented API, production platform |
| Structure | 3 | Clean JSON, documented parameters, download options |
| Identifiers | 2 | Standard bidding areas but custom field naming |
| Additive Value | 3 | Unique minute-level Danish grid data with CO2, wind, solar, exchange flows |
| **Total** | **17/18** | |

## Notes

- Rate limit: 1 request per unique IP per dataset per minute. Request frequency should match dataset update frequency.
- Not meant as a direct source for high-volume vendor applications — download and cache locally.
- Dynamic timestamps (`now-P1D`, `startOfDay-P7D`) are very useful for polling.
- The platform also covers gas system data and district heating.
- Excellent for Nordic energy market analysis — covers all Scandinavian bidding areas in price data.
