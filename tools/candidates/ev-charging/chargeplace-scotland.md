# ChargePlace Scotland

**Country/Region**: United Kingdom — Scotland
**Publisher**: Transport Scotland / ChargePlace Scotland
**API Endpoint**: `https://chargeplacescotland.org/api/v3/poi/` (suspected; endpoint requires investigation)
**Documentation**: https://chargeplacescotland.org/
**Protocol**: REST (based on Open Charge Map compatible API)
**Auth**: API Key (registration required)
**Data Format**: JSON
**Update Frequency**: Near real-time (network-connected chargers report status)
**License**: Open Government Licence (Scotland)

## What It Provides

ChargePlace Scotland operates the Scottish government's EV charging network with 3,000+ charge points across Scotland. The platform provides both a consumer-facing app/website and an API for accessing charge point locations and real-time availability. ChargePlace Scotland is interesting because it's a government-operated network (not just a registry) — they manage the actual charging infrastructure.

## API Details

ChargePlace Scotland has historically provided API access to charge point data. The API is believed to follow the Open Charge Map API format (as ChargePlace Scotland contributes data to OCM). Specific endpoint details:

- Location search by proximity (lat/lon/radius)
- Filter by connector type, availability status
- Real-time connector status (available, in use, out of service)

The exact API endpoint and documentation require registration. The public-facing website shows real-time status of all chargers on a map.

Data includes:
- Charge point location (address, coordinates)
- Connector types and power levels
- Real-time status per connector
- Network operator
- Usage type (public/restricted)

## Freshness Assessment

As a network operator (not just a registry), ChargePlace Scotland has direct telemetry from its charge points. Real-time status is updated as chargers report state changes. This provides genuine real-time connector availability — better freshness than registries that aggregate data from multiple sources.

## Entity Model

- **Charge Point**: Physical charging location with address, coordinates
- **Connector**: Individual connector with type, power, real-time status
- **Status**: Available, Occupied, Out of Service, Unknown

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Direct network telemetry, real-time status |
| Openness | 2 | API key required; registration process unclear; coverage limited to Scotland |
| Stability | 2 | Government-backed but API documentation is limited |
| Structure | 2 | Likely OCM-compatible but needs verification |
| Identifiers | 2 | Charge point IDs present but format needs verification |
| Additive Value | 1 | Scotland-only coverage; OCM already aggregates this data |
| **Total** | **12/18** | |

## Notes

- ChargePlace Scotland data is already available via Open Charge Map as a contributed source. The direct API adds value only if real-time status is richer than what OCM provides.
- Scotland is rolling out rapid charging hubs along major routes — the network is actively expanding.
- Registration process for API access is unclear from public documentation. May require contacting Transport Scotland directly.
- Lower priority than NOBIL, NDL, or OCM due to limited geographic scope and uncertain API access.
