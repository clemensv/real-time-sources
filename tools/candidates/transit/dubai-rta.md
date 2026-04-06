# Dubai RTA — Roads and Transport Authority Open Data

**Country/Region**: United Arab Emirates (Dubai)
**Publisher**: Roads and Transport Authority (RTA Dubai)
**API Endpoint**: `https://data.dubai.gov.ae/` (Dubai Pulse) + RTA-specific endpoints
**Documentation**: https://www.rta.ae/wps/portal/rta/ae/home/rta-opendata
**Protocol**: REST/JSON
**Auth**: API key required (free registration via Dubai Pulse / data.dubai.gov.ae)
**Data Format**: JSON, CSV
**Update Frequency**: Near real-time — bus and metro schedules; traffic data real-time
**License**: Dubai Open Data Policy (free for commercial and non-commercial use)

## What It Provides

Dubai's RTA operates one of the most modern transit systems in the Middle East, and publishes open data through the Dubai Pulse (data.dubai.gov.ae) platform:

- **Dubai Metro**: Red and Green lines — schedule and station data
- **Dubai Tram**: real-time schedule
- **Dubai Bus**: 119 routes — schedule and route data
- **Dubai Ferry / Water Bus**: marine transit
- **nol Card**: transit smart card system data (aggregated)
- **Traffic**: real-time traffic flow data on Dubai roads
- **Taxi**: trip statistics
- **Parking**: availability data

## API Details

RTA publishes data through multiple channels:

### Dubai Pulse (data.dubai.gov.ae)
- CKAN-based open data portal with API access
- Transit datasets include bus routes, metro stations, bus stops, schedules
- `GET /api/3/action/package_search?q=rta+bus` — search for bus datasets
- `GET /api/3/action/datastore_search?resource_id={id}` — query specific datasets

### RTA Open Data
- Bus route information and stop locations
- Metro/tram station details
- Real-time traffic speed data
- Parking availability at transit hubs

The main data.dubai.gov.ae hostname was unreachable in testing — possibly requires VPN access or was temporarily down. RTA's own open data page (rta.ae) is the authoritative source for available datasets.

## Freshness Assessment

Mixed. Dubai's transit infrastructure is modern and well-instrumented, but the open data platform is more focused on static/reference data and traffic conditions than on real-time transit predictions. Metro and tram schedules are published but real-time deviation data is less clear. Traffic flow data (road speeds) is genuinely real-time. The platform is evolving — Dubai has ambitious smart city goals and the data offering is expanding.

## Entity Model

- **Bus Route**: route number, origin/destination, stops, schedule
- **Metro Station**: name, line (Red/Green), location, facilities
- **Bus Stop**: code, name, location, routes served
- **Traffic Flow**: road segment, speed, timestamp
- IDs follow RTA's internal numbering system

## Feasibility Rating

| Criterion       | Score | Notes                                                        |
|-----------------|-------|--------------------------------------------------------------|
| Freshness       | 1     | More static/reference data than real-time predictions         |
| Openness        | 2     | Free registration; platform accessibility varies              |
| Stability       | 2     | Government-backed; platform is evolving                       |
| Structure       | 2     | CKAN-based; some datasets are well-structured, others are CSV dumps|
| Identifiers     | 1     | RTA internal codes; no international standard alignment       |
| Additive Value  | 1     | Limited real-time; Middle East coverage is the main draw      |
| **Total**       | **9/18** |                                                            |

## Notes

- Dubai RTA is more of a future candidate — the platform is still maturing toward real-time API access.
- The traffic flow data (road speeds) is the most "real-time" offering and may be more interesting for automotive/navigation use cases than transit.
- Dubai is investing heavily in smart transport (autonomous vehicles, hyperloop studies, drone taxis) — the open data platform may improve significantly.
- For Middle East transit coverage, Dubai is the most likely to have usable open data, but it's currently behind the best European and Asian platforms.
- The nol card system (equivalent to Oyster/Octopus) generates rich ridership data, but only aggregated statistics are published.
