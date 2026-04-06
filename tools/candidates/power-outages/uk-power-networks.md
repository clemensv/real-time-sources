# UK Power Networks
**Country/Region**: United Kingdom (South East England, East England, London)
**Publisher**: UK Power Networks (UKPN)
**API Endpoint**: `https://www.ukpowernetworks.co.uk/power-cut/map` (web portal)
**Documentation**: https://www.ukpowernetworks.co.uk/power-cut (power cut information)
**Protocol**: Web / JSON (internal API behind portal)
**Auth**: None (public portal)
**Data Format**: JSON (internal), HTML (portal)
**Update Frequency**: Near real-time (outages reported as they occur)
**License**: Open data (UK power network obligation)

## What It Provides
UK Power Networks serves ~8.4 million customers across London, South East and East England. Their power cut portal provides:
- Current power cut locations and status
- Estimated time of restoration (ETR)
- Number of customers affected per incident
- Incident cause and category
- Planned maintenance outages
- Historical power cut data

UKPN is one of six Distribution Network Operators (DNOs) in the UK. Other DNOs (Western Power Distribution, Scottish Power, Northern Powergrid, Electricity North West, SSE Networks) have similar portals.

## API Details
- **Power Cut Map**: `https://www.ukpowernetworks.co.uk/power-cut/map` — interactive map
- **Internal API**: The map loads data via internal JSON APIs (not publicly documented)
- **Open Data Portal**: UKPN publishes some data on UK open data platforms
- **Other UK DNOs with similar portals**:
  - Western Power Distribution: `https://www.westernpower.co.uk/power-cuts-map`
  - Scottish Power: `https://www.spenergynetworks.co.uk/pages/power_cuts_map.aspx`
  - Northern Powergrid: `https://www.northernpowergrid.com/power-cuts`
  - SSE Networks: `https://www.ssen.co.uk/power-cuts/`
  - Electricity North West: `https://www.enwl.co.uk/power-cuts/`

## Freshness Assessment
Good. Power cuts are reported in near real-time through the portal. The underlying data is updated as network management systems detect outages. However, the lack of a public REST API is a significant limitation.

## Entity Model
- **Incident** (reference number, postcode area, start time, ETR, status)
- **Status** (Under Investigation, Engineer On Way, Engineer On Site, Restored)
- **Cause** (weather, equipment failure, planned, third-party damage)
- **Impact** (number of customers, geographic area/postcodes)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Near real-time outage reporting |
| Openness | 1 | Public portal, but no documented public API |
| Stability | 3 | Regulated utility, legally required to report |
| Structure | 1 | Internal JSON, not publicly documented |
| Identifiers | 2 | Incident reference numbers, postcode areas |
| Additive Value | 2 | One of six UK DNOs, not comprehensive alone |
| **Total** | **12/18** | |

## Notes
- UK power distribution is split across six DNOs — UKPN is the largest
- Each DNO has its own outage portal with different technology stacks
- Ofgem (regulator) mandates outage reporting, creating some standardization
- Some DNOs may publish outage data as open data under UK government initiatives
- A comprehensive UK solution would need to aggregate all six DNOs
- The underlying technology platforms (e.g., GE PowerOn) may offer API capabilities that aren't publicly documented
