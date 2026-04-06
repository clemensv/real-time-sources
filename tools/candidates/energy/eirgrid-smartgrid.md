# EirGrid / SONI Smart Grid Dashboard (Ireland)

**Country/Region**: Ireland and Northern Ireland (All-Island)
**Publisher**: EirGrid (Republic of Ireland TSO) / SONI (Northern Ireland TSO)
**API Endpoint**: `https://www.smartgriddashboard.com/DashboardService.svc/data`
**Documentation**: https://www.smartgriddashboard.com (no formal API docs — reverse-engineered WCF service)
**Protocol**: REST (WCF Data Service)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: 15 minutes
**License**: Publicly accessible (no explicit license stated)

## What It Provides

The Smart Grid Dashboard is EirGrid and SONI's public-facing real-time electricity system dashboard for the island of Ireland. It exposes a WCF service endpoint that returns JSON data for demand, generation, wind, CO2, frequency, and interconnection.

Known data areas:

- **windactual** — Actual wind generation (MW), 15-min intervals ✓ verified
- **windforecast** — Wind generation forecast
- **demandactual** — System demand (MW)
- **generationactual** — Total generation (MW)
- **co2intensity** — Carbon intensity (gCO2/kWh)
- **co2emission** — Total CO2 emissions
- **frequency** — System frequency (Hz)
- **interconnection** — Cross-border flows (Moyle interconnector to GB, EWIC)
- **snsp** — System Non-Synchronous Penetration (percentage of generation from non-synchronous sources — unique metric!)

Regions: `ALL` (all-island), `ROI` (Republic of Ireland), `NI` (Northern Ireland).

## API Details

WCF Data Service with query parameters:

```
GET https://www.smartgriddashboard.com/DashboardService.svc/data
    ?area=windactual
    &region=ALL
    &datefrom=2025-01-01+00:00
    &dateto=2025-01-01+01:00
```

Response:

```json
{
  "ErrorMessage": null,
  "LastUpdated": "01-Jan-2025 01:00:00",
  "Rows": [
    {"EffectiveTime": "01-Jan-2025 00:00:00", "FieldName": "WIND_ACTUAL", "Region": "ALL", "Value": 1989},
    {"EffectiveTime": "01-Jan-2025 00:15:00", "FieldName": "WIND_ACTUAL", "Region": "ALL", "Value": 2059},
    {"EffectiveTime": "01-Jan-2025 00:30:00", "FieldName": "WIND_ACTUAL", "Region": "ALL", "Value": 2144},
    {"EffectiveTime": "01-Jan-2025 00:45:00", "FieldName": "WIND_ACTUAL", "Region": "ALL", "Value": 2303}
  ],
  "Status": "Success"
}
```

Date format in requests: `YYYY-MM-DD+HH:MM` (URL-encoded spaces). Date format in responses: `DD-MMM-YYYY HH:mm:ss`.

The service is somewhat unreliable — during testing, `windactual` returned data successfully but `demandactual`, `generationactual`, `co2intensity`, `frequency`, and `interconnection` all returned 503 Service Unavailable. The dashboard web app may use additional endpoints or session management.

## Freshness Assessment

15-minute resolution, matching EirGrid's operational dispatch intervals. Data is close to real-time when the service is responding. The `LastUpdated` field in responses indicates actual data currency.

## Entity Model

- **Area**: Data category (windactual, demandactual, generationactual, co2intensity, frequency, interconnection, snsp)
- **Region**: ALL (all-island), ROI (Ireland), NI (Northern Ireland)
- **EffectiveTime**: Timestamp (DD-MMM-YYYY HH:mm:ss format, Irish local time)
- **FieldName**: Machine-readable area code (WIND_ACTUAL, etc.)
- **Value**: Numeric value in MW, Hz, gCO2/kWh, or percentage

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15-minute real-time updates |
| Openness | 3 | No auth required |
| Stability | 1 | Undocumented WCF service, intermittent 503 errors, no SLA |
| Structure | 2 | Clean JSON when working, but inconsistent field naming and date formats |
| Identifiers | 2 | Non-standard region codes (ALL/ROI/NI), custom area names |
| Additive Value | 3 | Only source for Ireland-specific grid data including unique SNSP metric |
| **Total** | **14/18** | |

## Notes

- Ireland is exceptionally interesting for energy data: world-leading wind penetration, the SNSP (System Non-Synchronous Penetration) metric is unique to the Irish grid, and the all-island approach (spanning two jurisdictions) is unusual.
- The 503 errors suggest the backend may be overloaded or rate-limiting. A scraper would need retry logic and backoff.
- The API is undocumented — the area names and region codes are reverse-engineered from the dashboard JavaScript.
- Ireland is also covered by energy-charts.info (country=ie, nie), but the Smart Grid Dashboard provides Ireland-specific metrics (SNSP, interconnector flows) not available elsewhere.
- Consider implementing alongside energy-charts.info for Ireland-specific detail that the pan-European API doesn't capture.
