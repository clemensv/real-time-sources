# CAISO OASIS (California ISO)

**Country/Region**: California and parts of western US
**Publisher**: California Independent System Operator (CAISO)
**API Endpoint**: `https://oasis.caiso.com/oasisapi/SingleZip`
**Documentation**: https://oasis.caiso.com/ (OASIS portal)
**Protocol**: REST (parameterized ZIP/XML download)
**Auth**: None for public data (account required for some reports)
**Data Format**: XML (inside ZIP), CSV
**Update Frequency**: 5-minute intervals (real-time market), hourly (day-ahead)
**License**: Public data, no explicit open license

## What It Provides

CAISO OASIS (Open Access Same-time Information System) provides comprehensive real-time and day-ahead market data for California's electricity grid.

Key data categories:

- **Locational Marginal Prices (LMP)**: Day-ahead, real-time, and 15-minute market prices at thousands of pricing nodes (PNodes)
- **System Demand**: Actual and forecast system demand
- **Renewable Generation**: Solar, wind, and other renewable output
- **Supply and Demand Curves**: Aggregated supply curves
- **Interchange**: Scheduled and actual interchange at interties
- **Ancillary Services**: Regulation, spinning reserve, non-spinning reserve prices
- **Transmission**: Available Transfer Capability (ATC), transmission outages
- **Resource Listings**: Generator capabilities, PNode mappings

## API Details

OASIS provides data through parameterized URL downloads:

```
GET https://oasis.caiso.com/oasisapi/SingleZip?
    queryname=PRC_LMP
    &market_run_id=RTM
    &startdatetime=20260406T07:00-0000
    &enddatetime=20260406T08:00-0000
    &node=CAISO_SP15
    &resultformat=6
```

Query names include: `PRC_LMP` (prices), `SLD_FCST` (demand forecast), `ENE_SLRS` (renewables), `AS_RESULTS` (ancillary services). Format options: XML (6) or CSV.

The response is a ZIP file containing XML or CSV data. This is not a typical JSON REST API — it's a download-oriented system.

## Freshness Assessment

Real-time market data (5-minute LMPs) is published with approximately 5-10 minute lag. Day-ahead prices are published in the afternoon for the next day. Renewable generation data updates frequently. The system is operational 24/7 and is the canonical source for California grid data.

## Entity Model

- **PNode**: Pricing Node — thousands of locations on the grid (e.g., CAISO_SP15, CAISO_NP15)
- **Trading Hub**: Aggregated pricing points (SP15, NP15, ZP26)
- **Market Run**: DAM (Day-Ahead Market), RTM (Real-Time Market), HASP (Hour-Ahead)
- **Resource**: Individual generators and loads
- **Intertie**: Scheduling points for inter-BA flows

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute real-time LMPs, near-real-time |
| Openness | 2 | Public data but complex access, no explicit open license |
| Stability | 3 | Regulatory-mandated system, highly reliable |
| Structure | 1 | ZIP/XML format, complex query syntax, no JSON |
| Identifiers | 3 | Standard PNode IDs, well-defined market terminology |
| Additive Value | 2 | California-specific; EIA covers most of this data more cleanly |
| **Total** | **14/18** | |

## Notes

- The EIA Grid Monitor API (`respondent=CAL`) provides much of the same data in a cleaner JSON format. CAISO OASIS adds nodal-level LMP granularity that EIA doesn't have.
- The ZIP/XML format makes this harder to integrate than modern JSON APIs.
- CAISO also provides a "Today's Outlook" dashboard with renewable curtailment data that's not in OASIS.
- Consider CAISO primarily for nodal price data (thousands of LMP points) where EIA's BA-level data is insufficient.
- CAISO's grid is notable for very high solar penetration and the "duck curve" phenomenon.
