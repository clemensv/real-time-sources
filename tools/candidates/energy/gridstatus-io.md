# GridStatus.io (US Grid Data Aggregator)

**Country/Region**: United States (all major ISOs)
**Publisher**: GridStatus.io (commercial startup)
**API Endpoint**: `https://api.gridstatus.io/v1/`
**Documentation**: https://docs.gridstatus.io
**Protocol**: REST
**Auth**: API key (free tier with limits, paid plans for production)
**Data Format**: JSON, CSV
**Update Frequency**: 5 minutes (real-time from ISOs)
**License**: Commercial (data sourced from public ISO feeds)

## What It Provides

GridStatus.io is a data aggregator that normalizes real-time electricity data from all seven major US ISOs (CAISO, ERCOT, PJM, MISO, NYISO, SPP, ISO-NE) into a unified API. Think of it as the US equivalent of what energy-charts.info does for Europe.

Datasets include:

- **Fuel mix** — Real-time generation by fuel type across all ISOs
- **Load/demand** — System-wide and zonal demand
- **LMP (Locational Marginal Pricing)** — Nodal and zonal prices
- **Interchange** — Cross-ISO flows
- **Reserves** — Operating reserves and ancillary services
- **Curtailment** — Renewable curtailment data
- **Load forecasts** — Day-ahead and real-time forecasts

The key value proposition is normalization: each ISO publishes data in wildly different formats, and GridStatus maps them to a common schema.

## API Details

```
GET https://api.gridstatus.io/v1/datasets?iso=caiso
Headers:
  X-Api-Key: YOUR_KEY
```

During testing, the API returned 403 (Forbidden) without an API key, confirming authentication is required.

The API also has a Python client library (`gridstatus`) available on PyPI:

```python
import gridstatus
caiso = gridstatus.CAISO()
df = caiso.get_fuel_mix("today")
```

The open-source `gridstatus` Python package can also scrape ISO data directly without the commercial API.

## Freshness Assessment

5-minute real-time data mirroring the underlying ISO feeds. The service aggregates data as ISOs publish it, so freshness matches the primary sources. Historical data goes back years.

## Entity Model

- **ISO**: CAISO, ERCOT, PJM, MISO, NYISO, SPP, ISONE
- **Fuel Type**: Normalized fuel type names across ISOs
- **Zone/Node**: ISO-specific zonal and nodal identifiers
- **LMP**: Price in $/MWh with energy, congestion, and loss components
- **Time**: ISO 8601 timestamps

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute real-time |
| Openness | 1 | Commercial API, free tier limited |
| Stability | 2 | Startup — less certain longevity than government sources |
| Structure | 3 | Clean normalized JSON, well-documented |
| Identifiers | 3 | Standard ISO codes, normalized fuel types |
| Additive Value | 2 | Overlaps heavily with EIA Grid Monitor; value is normalization and speed |
| **Total** | **14/18** | |

## Notes

- The open-source `gridstatus` Python library (https://github.com/gridstatus/gridstatus) is arguably more valuable than the commercial API — it provides direct scrapers for each ISO with data normalization, and it's free.
- For our use case, EIA Grid Monitor already covers BA-level hourly data for all US ISOs. GridStatus adds value primarily for sub-hourly (5-min) data, nodal pricing, and normalized fuel mix across ISOs.
- The commercial API targets enterprise customers (energy traders, grid operators, researchers).
- Consider using the open-source library directly rather than the commercial API for a more sustainable integration.
