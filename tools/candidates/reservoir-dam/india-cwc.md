# India CWC — Reservoir Storage Bulletin

**Country/Region**: India (130+ major reservoirs across all states)
**Publisher**: Central Water Commission (CWC), Ministry of Jal Shakti, Government of India
**API Endpoint**: `https://cwc.gov.in/reservoir-storage` (web portal); no documented public REST API
**Documentation**: https://cwc.gov.in/
**Protocol**: Web portal with weekly PDF/HTML bulletins
**Auth**: None for public bulletin access; API access appears restricted (401 observed)
**Data Format**: HTML tables, PDF bulletins
**Update Frequency**: Weekly (Reservoir Storage Bulletin published every Thursday)
**License**: Indian government open data policy

## What It Provides

CWC publishes the weekly Reservoir Storage Bulletin monitoring ~150 major reservoirs across India, covering:

- **Live storage** (BCM — billion cubic metres) for each reservoir
- **Percentage of capacity** filled
- **Comparison with last year** and 10-year average
- **State-wise and basin-wise aggregation**
- **Inflow and outflow** for selected reservoirs

India has over 5,000 large dams — the third highest number in the world after China and the USA. The CWC monitors the most critical ones that collectively account for ~250 BCM of live storage capacity, crucial for irrigation, drinking water, hydropower, and flood control across the subcontinent.

## API Details

No documented REST API. The web portal at `https://cwc.gov.in/reservoir-storage` returned HTTP 401 during testing, suggesting access controls may be in flux.

Data access methods:
- **Weekly Bulletin**: Published as HTML page with tabular data and downloadable PDF
- **India-WRIS** (Water Resources Information System): `https://indiawris.gov.in/wris/` — a geospatial portal that may offer WMS/WFS services
- **Open Government Data**: Some CWC datasets available on `https://data.gov.in/` with API access

The India-WRIS platform is the more promising programmatic access point, potentially offering geospatial web services for reservoir data.

## Freshness Assessment

Moderate. Weekly bulletins are timely for reservoir management (levels don't change dramatically day-to-day). Real-time telemetry exists internally at CWC but isn't exposed publicly through an API. The data.gov.in route may provide more structured access with some lag.

## Entity Model

- **Reservoir**: name, state, river basin, full reservoir level (FRL), live capacity (BCM)
- **Weekly Observation**: date, live storage (BCM), percentage full, last year comparison, 10-year average comparison
- **Basin**: name, number of monitored reservoirs, total capacity
- **State**: name, number of monitored reservoirs

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Weekly bulletins are timely for reservoir data; not real-time |
| Openness | 1 | Public bulletins but no REST API; 401 errors on direct access |
| Stability | 2 | Government institution but web infrastructure is inconsistent |
| Structure | 1 | HTML/PDF bulletins; no standardized API; India-WRIS may offer WFS |
| Identifiers | 1 | No standardized reservoir codes exposed; state/name only |
| Additive Value | 3 | 3rd largest dam inventory globally; monsoon dynamics; 1.4B people depend on this |
| **Total** | **10/18** | |

## Notes

- The biggest challenge is programmatic access. CWC data is publicly available but not through a modern API.
- India-WRIS (`indiawris.gov.in`) may be the better integration target — it's a GIS-based platform that likely offers WMS/WFS endpoints.
- The data.gov.in platform sometimes hosts CWC datasets with basic API access — worth checking for reservoir-specific datasets.
- During the monsoon season (June–September), Indian reservoir levels are a major economic indicator watched by farmers, power companies, and markets.
- Regional alternatives: individual state irrigation departments sometimes publish real-time reservoir data (e.g., Maharashtra, Karnataka).
- Consider pairing with IMD rainfall data for a complete monsoon water picture.
