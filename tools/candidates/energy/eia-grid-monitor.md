# US EIA Hourly Electric Grid Monitor

**Country/Region**: United States (all balancing authorities)
**Publisher**: US Energy Information Administration (EIA)
**API Endpoint**: `https://api.eia.gov/v2/electricity/rto/`
**Documentation**: https://www.eia.gov/opendata/documentation.php
**Protocol**: REST
**Auth**: API Key (free registration at https://www.eia.gov/opendata/)
**Data Format**: JSON, XML
**Update Frequency**: Hourly (Form EIA-930)
**License**: US Government public domain

## What It Provides

The EIA Hourly Electric Grid Monitor covers the entire US electricity grid through Form EIA-930 data reported by every balancing authority. This is the single most comprehensive source for US-wide real-time electricity data.

Available sub-routes:

- `/rto/region-data` — Hourly demand, day-ahead demand forecast, net generation, and interchange by balancing authority
- `/rto/fuel-type-data` — Hourly net generation by balancing authority and energy source (solar, wind, natural gas, coal, nuclear, hydro, etc.)
- `/rto/region-sub-ba-data` — Hourly demand by subregion
- `/rto/interchange-data` — Hourly interchange between neighboring balancing authorities
- `/rto/daily-region-data` — Daily aggregations of the above
- `/rto/daily-fuel-type-data` — Daily generation by energy source

Balancing authorities include CAISO (CAL), ERCOT (ERCO), PJM, MISO, NYISO (NYIS), SPP, ISO-NE (ISNE), and dozens more.

## API Details

RESTful APIv2 with a tree-structured route hierarchy. Parameters are passed as query strings:

```
GET https://api.eia.gov/v2/electricity/rto/fuel-type-data
    ?api_key=YOUR_KEY
    &frequency=hourly
    &data[0]=value
    &facets[fueltype][]=SUN
    &facets[respondent][]=CAL
    &sort[0][column]=period
    &sort[0][direction]=desc
    &length=10
```

Response model:

```json
{
  "response": {
    "data": [
      { "period": "2026-04-05T05", "respondent": "CAL", "fueltype": "SUN", "value": "1234" }
    ]
  }
}
```

Key facets: `respondent` (balancing authority code), `fueltype` (SUN, WND, NG, COL, NUC, WAT, OTH, etc.). Values are in megawatthours (MWh). Pagination via `offset` and `length` (max 5000 rows). Supports `start` and `end` date parameters.

## Freshness Assessment

Data is reported hourly by balancing authorities with a lag of approximately 1-2 hours. The `endPeriod` in metadata shows data through the current day. Historical data goes back to 2019-01-01. This is genuinely near-real-time for a government statistical agency.

## Entity Model

- **Balancing Authority** (respondent): ~70 US balancing authorities identified by standard codes (CAL, ERCO, PJM, MISO, NYIS, etc.)
- **Energy Source** (fueltype): SUN, WND, NG, COL, NUC, WAT, OIL, OTH, ALL
- **Time Period**: Hourly UTC or local-hourly
- **Value**: Net generation or demand in MWh

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Hourly updates, ~1-2h lag |
| Openness | 3 | Free API key, no usage restrictions, public domain |
| Stability | 3 | Government agency, API versioned (v2.1.12), maintained since 2012 |
| Structure | 3 | Clean JSON, well-documented facets and routes |
| Identifiers | 3 | Standard BA codes, NERC-aligned respondent IDs |
| Additive Value | 3 | Covers ALL US balancing authorities in one API — unique breadth |
| **Total** | **18/18** | |

## Notes

- The DEMO_KEY works for testing but has rate limits. Register for a free key.
- This single API effectively covers CAISO, ERCOT, PJM, MISO, NYISO, SPP, and ISO-NE data, making separate integrations with those ISOs less critical.
- The fuel-type breakdown is particularly valuable for generation mix / carbon intensity calculations.
- APIv1 series IDs can still be used via the `/v2/seriesid/` compatibility route.
- Data values are returned as strings (since v2.1.6) to support leading zeroes in sub-BA codes.
