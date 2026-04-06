# Nord Pool — European Power Exchange

**Country/Region**: Nordic, Baltic, and expanding European coverage
**Publisher**: Nord Pool AS (European power exchange, owned by Euronext)
**API Endpoint**: Historical `https://www.nordpoolgroup.com/api/marketdata/` (deprecated — returned 410 Gone)
**Documentation**: https://www.nordpoolgroup.com/en/market-data-services/
**Protocol**: REST (legacy), FTP/SFTP (data feeds), web portal
**Auth**: Commercial API requires subscription; web portal data is public
**Data Format**: JSON (legacy API), CSV (downloads), XML (data feeds)
**Update Frequency**: Hourly (day-ahead), continuous (intraday)
**License**: Commercial (market data licensing applies)

## What It Provides

Nord Pool operates the leading power exchange for the Nordic and Baltic electricity markets, and increasingly for other European markets. It facilitates:

- **Day-ahead market (Elspot)**: Hourly prices for next-day delivery, settled by auction. Covers Nordic (NO1-5, SE1-4, DK1-2, FI), Baltic (EE, LV, LT), and other zones.
- **Intraday market (Elbas)**: Continuous trading for same-day delivery, 15-minute to hourly products.
- **System price**: Reference price for the Nordic power market.
- **Volumes**: Traded volumes by bidding zone.
- **Flow**: Cross-border traded capacities.

## API Details

The historical public API at `nordpoolgroup.com/api/marketdata/` returned HTTP 410 Gone during testing:

```
GET https://www.nordpoolgroup.com/api/marketdata/page/10?currency=EUR&endDate=2025-06-01
→ 410 Gone
```

This indicates the legacy public API has been decommissioned. Current data access options:

1. **Nord Pool website**: Market data pages with day-ahead prices viewable online
2. **Data-as-a-Service**: Commercial API product requiring subscription
3. **FTP/SFTP feeds**: For market participants and licensed data consumers
4. **ENTSO-E Transparency Platform**: Day-ahead prices for all European bidding zones (including Nord Pool zones) are available via ENTSO-E
5. **Energy-Charts API**: Day-ahead prices for Nordic/Baltic zones available at `api.energy-charts.info/price?bzn=NO1` (verified working)

## Freshness Assessment

Day-ahead prices are published around 12:30-13:00 CET for the next day (24 hourly prices). Intraday trading is continuous. The data is inherently event-driven — prices are published once per day for day-ahead, continuously for intraday.

## Entity Model

- **Bidding Zone**: NO1-NO5 (Norway), SE1-SE4 (Sweden), DK1-DK2 (Denmark), FI (Finland), EE, LV, LT (Baltics)
- **Product**: Hourly (day-ahead), 15-min/hourly (intraday)
- **Price**: EUR/MWh or local currency (NOK, SEK, DKK)
- **Volume**: MWh traded
- **System Price**: Nordic reference price (area-weighted)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Day-ahead prices published daily, intraday continuous |
| Openness | 1 | Legacy public API decommissioned (410 Gone); commercial API only |
| Stability | 3 | Major exchange (Euronext-owned), decades of operation |
| Structure | 2 | Commercial API is clean; public access now requires ENTSO-E or energy-charts |
| Identifiers | 3 | Standard European bidding zone codes |
| Additive Value | 1 | Price data available via energy-charts.info and ENTSO-E |
| **Total** | **13/18** | |

## Notes

- The 410 Gone response confirms Nord Pool has fully deprecated their public API. This is a significant change from prior years when `nordpoolgroup.com/api/marketdata/` was a widely used free data source.
- For day-ahead prices in Nordic/Baltic zones, use energy-charts.info (`/price?bzn=NO1`) or ENTSO-E Transparency Platform instead.
- Nord Pool's commercial Data-as-a-Service product is aimed at energy traders and market participants, not general data consumers.
- The Nordic day-ahead prices are also published by Energi Data Service (DK zones) — already documented in energidataservice-dk.md.
- Unless Nord Pool launches a new public API, this source is effectively superseded by energy-charts.info and ENTSO-E for our purposes.
