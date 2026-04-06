# EPEX SPOT — European Power Exchange

**Country/Region**: Central Western Europe and expanding
**Publisher**: EPEX SPOT SE (European Power Exchange, subsidiary of EEX Group)
**API Endpoint**: No public API — commercial data products only
**Documentation**: https://www.epexspot.com/en/market-data
**Protocol**: FTP/SFTP (data feeds), web portal
**Auth**: Commercial subscription required
**Data Format**: CSV, XML (data feeds)
**Update Frequency**: Hourly (day-ahead), 15-minute (intraday), continuous
**License**: Commercial (market data licensing)

## What It Provides

EPEX SPOT operates the power spot market (day-ahead and intraday) for some of the largest European electricity markets:

- **Germany/Luxembourg** (DE-LU) — Europe's largest electricity market
- **France** (FR) — Europe's second largest
- **Austria** (AT)
- **Netherlands** (NL)
- **Belgium** (BE)
- **Switzerland** (CH)
- **Great Britain** (GB)
- **Nordic countries** (via integration)

Products:

- **Day-ahead auction**: Hourly and block products for next-day delivery
- **Intraday continuous**: 15-minute, 30-minute, and hourly products for same-day delivery
- **Intraday auction**: Complements continuous trading
- **Local flexibility markets**: Emerging products

## API Details

EPEX SPOT does not offer a public API. All market data is:

1. **Published on their website** with ~15-minute delay for registered users
2. **Delivered via data feeds** (FTP/SFTP/API) to licensed subscribers
3. **Available through data vendors** (Bloomberg, Reuters, etc.)

However, EPEX SPOT market clearing prices are published via:
- **ENTSO-E Transparency Platform** (required by EU regulation REMIT)
- **Energy-Charts API** (aggregated from ENTSO-E/Bundesnetzagentur)
- **SMARD** (for German market)

So while EPEX itself doesn't provide public API access, their price data is legally required to be published through transparency platforms.

## Freshness Assessment

Day-ahead auction results are published around 12:30-13:00 CET (one hour before Nord Pool for overlapping zones). Intraday continuous trading updates in real-time. Final settlement data has various delays depending on the product.

## Entity Model

- **Market Area**: DE-LU, FR, AT, NL, BE, CH, GB
- **Product**: Day-ahead hourly, Intraday 15-min/30-min/hourly, Block products
- **Price**: EUR/MWh (GBP/MWh for GB)
- **Volume**: MWh
- **Order Book**: Bid/ask curves (commercial data only)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time intraday, daily day-ahead |
| Openness | 0 | No public API whatsoever; commercial subscription only |
| Stability | 3 | Major European exchange (EEX/Deutsche Börse group) |
| Structure | 2 | Commercial feeds are well-structured; no public access to evaluate |
| Identifiers | 3 | Standard European market area codes |
| Additive Value | 1 | Price data available via ENTSO-E and energy-charts.info (regulatory transparency) |
| **Total** | **12/18** | |

## Notes

- EPEX SPOT's own data is commercially licensed, but EU REMIT transparency regulations require the prices to be published via ENTSO-E — making the exchange data effectively available through public channels.
- For day-ahead and intraday prices in EPEX zones, use energy-charts.info's `/price` endpoint with the appropriate bidding zone code (e.g., `bzn=DE-LU`, `bzn=FR`, `bzn=NL`).
- The exchange itself adds value through order book depth, block product details, and real-time intraday continuous data that isn't available through transparency platforms.
- Unless you specifically need order book data or real-time intraday fills, ENTSO-E and energy-charts.info cover the price data adequately.
