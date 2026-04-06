# WattTime Marginal Emissions API

**Country/Region**: Global (US regions, Canada, Europe, Australia, India, others)
**Publisher**: WattTime (nonprofit subsidiary of Rocky Mountain Institute)
**API Endpoint**: `https://api.watttime.org/v3/`
**Documentation**: https://api.watttime.org/docs (ReDoc/OpenAPI)
**Protocol**: REST
**Auth**: HTTP Basic Auth for token, then Bearer token for data (free tier available)
**Data Format**: JSON
**Update Frequency**: 5 minutes
**License**: Free tier (limited to signal index), paid tiers for raw MOER data

## What It Provides

WattTime provides marginal operating emissions rate (MOER) data — the CO2 intensity of the marginal (next) unit of electricity on the grid. This is fundamentally different from average grid intensity: MOER tells you the emissions impact of consuming one additional MWh right now.

Endpoints (v3 API):

- `/v3/signal-index` — Real-time signal index (0-100 scale, where 0 = cleanest, 100 = dirtiest). Free tier.
- `/v3/forecast` — Marginal emissions forecast (24-72 hours ahead)
- `/v3/historical` — Historical MOER data
- `/v3/region-from-loc` — Look up WattTime region from latitude/longitude
- `/v3/maps` — Geospatial emissions maps

Regions cover:
- **US**: All major ISOs (CAISO, ERCOT, PJM, MISO, NYISO, SPP, ISO-NE, AESO) with sub-regional granularity
- **Canada**: Alberta, Ontario, British Columbia, Quebec
- **Europe**: Multiple countries
- **Australia**: NEM regions
- **India**: Regional grids

## API Details

Authentication flow:
```
1. Register at https://www.watttime.org/api-documentation/
2. Get token:
   POST https://api.watttime.org/v3/login
   Authorization: Basic base64(username:password)
   → {"token": "eyJ..."}
   
3. Query data:
   GET https://api.watttime.org/v3/signal-index?region=CAISO_NORTH
   Authorization: Bearer eyJ...
```

The API returned 401 during testing (expected — requires registration). The documentation is served via ReDoc at the API root.

Free tier limitations:
- Access to signal-index endpoint only (0-100 relative scale)
- No raw MOER values (lbs CO2/MWh)
- No forecast data
- No historical data beyond 30 days

Paid tiers:
- **Analyst**: Raw MOER values, forecasts, historical data
- **Pro/Enterprise**: Real-time MOER, sub-regional data, maps API

## Freshness Assessment

5-minute update frequency for real-time MOER data. Signal index updates every 5 minutes. Forecasts extend 24-72 hours into the future. This is as fresh as the underlying grid data from ISOs, with WattTime's emissions model applied.

## Entity Model

- **Region**: WattTime region codes (CAISO_NORTH, PJM_WEST, MISO_MI, etc.)
- **Signal Index**: Integer 0-100 (relative, unitless)
- **MOER**: Marginal emissions in lbs CO2/MWh (paid tiers)
- **Forecast**: Time series of predicted MOER values
- **Location**: Latitude/longitude for region lookup

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute real-time updates |
| Openness | 1 | Free tier very limited; full data requires paid subscription |
| Stability | 3 | Well-funded nonprofit (RMI), versioned API (v3), OpenAPI spec |
| Structure | 3 | Clean JSON, well-documented, OpenAPI/ReDoc |
| Identifiers | 2 | Custom WattTime region codes (not standard ISO/grid codes) |
| Additive Value | 3 | Only source for marginal emissions data — fundamentally different from average intensity |
| **Total** | **15/18** | |

## Notes

- Marginal emissions (MOER) vs. average emissions is a critical distinction. If you're deciding whether to charge an EV or run a data center workload *right now*, MOER is what matters — it tells you the emissions impact of your additional consumption.
- The free tier's signal-index (0-100) is useful for "shift your load to green times" applications but lacks the actual CO2 rate.
- WattTime powers Google Cloud's carbon-aware computing and Microsoft's emissions dashboard.
- The `/v3/region-from-loc` endpoint is clever — pass lat/lon and it tells you which grid region you're in.
- For open/free marginal emissions data, consider energy-charts.info's `/signal` endpoint for European countries or the UK Carbon Intensity API's forecast.
