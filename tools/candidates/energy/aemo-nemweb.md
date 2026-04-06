# AEMO NEMWeb (Australia)

**Country/Region**: Australia (National Electricity Market — Queensland, NSW, Victoria, South Australia, Tasmania)
**Publisher**: Australian Energy Market Operator (AEMO)
**API Endpoint**: `https://nemweb.com.au/Reports/Current/` (file-based)
**Documentation**: https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem
**Protocol**: HTTP file download (CSV inside ZIP)
**Auth**: None (public data)
**Data Format**: CSV (inside ZIP archives)
**Update Frequency**: 5 minutes (dispatch data)
**License**: Open data (AEMO Terms of Use)

## What It Provides

AEMO operates Australia's National Electricity Market (NEM), one of the world's longest interconnected power systems. NEMWeb publishes 5-minute dispatch data and market reports.

Key data categories:

- **Dispatch data** — 5-minute dispatch intervals: regional prices, demand, generation, interconnector flows
- **Trading interval data** — 30-minute trading interval prices and quantities
- **Generator output** — Individual generator dispatch targets and output
- **Interconnector flows** — Flows between NEM regions (QLD-NSW, NSW-VIC, VIC-SA, VIC-TAS)
- **Demand forecasts** — Pre-dispatch and short-term forecasts
- **Rooftop solar estimates** — Estimated distributed solar PV generation
- **Market notices** — Operational alerts and constraint notices

## API Details

NEMWeb uses a file-based publication model. ZIP files containing CSV data are published at predictable URLs:

```
https://nemweb.com.au/Reports/Current/Dispatch_SCADA/
https://nemweb.com.au/Reports/Current/TradingIS_Reports/
https://nemweb.com.au/Reports/Current/Next_Day_Actual_Gen/
```

Each directory contains timestamped ZIP files. Inside each ZIP is one or more CSV files following the AEMO MMS (Market Management System) data model.

AEMO also provides:
- **AEMO Data Dashboard**: Interactive web visualizations
- **AEMO API (newer)**: A RESTful API is under development but access was returning 403 during testing

The MMS data model CSV format has a header row identifying the report type, followed by data rows with standard column structures.

## Freshness Assessment

Dispatch data is published every 5 minutes — this is among the freshest grid data globally. Australia's NEM operates as a single price pool with 5-minute dispatch intervals, so the data matches the market's native resolution. Trading interval data follows at 30-minute boundaries.

## Entity Model

- **Region**: QLD1, NSW1, VIC1, SA1, TAS1 (NEM regions)
- **Generator (DUID)**: Dispatch Unit Identifier — unique per generator
- **Interconnector**: Standard NEM interconnector IDs (N-Q-MNSP1, V-SA, etc.)
- **Dispatch Interval**: 5-minute intervals
- **Trading Interval**: 30-minute intervals
- **Price**: Regional Reference Price (RRP) in AUD/MWh

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute dispatch intervals, very fresh |
| Openness | 2 | Public but file-based, newer API returning 403 |
| Stability | 3 | Government-mandated market operator, critical infrastructure |
| Structure | 2 | CSV-in-ZIP format, complex MMS data model |
| Identifiers | 3 | Standard DUID, region codes, interconnector IDs |
| Additive Value | 3 | Unique Australian NEM data, 5-min granularity, high renewables |
| **Total** | **16/18** | |

## Notes

- The NEM is a fascinating market: one of the world's first 5-minute settlement markets, with very high variable renewable penetration (especially solar in SA and QLD).
- The file-based publication model requires polling directories and parsing ZIP/CSV files — not a clean REST API.
- Python libraries like `nempy` and `NEMOSIS` exist to simplify NEMWeb data access.
- South Australia frequently reaches 100% renewable generation — unique real-time data for energy transition research.
- Rooftop solar estimation is particularly interesting as distributed PV is invisible to traditional metering.
- The AEMO API appears to be under development; a cleaner REST interface may become available.
