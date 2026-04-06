# Open Charge Map

**Country/Region**: Global (180+ countries)
**Publisher**: Open Charge Map community / Open Energy Foundation
**API Endpoint**: `https://api.openchargemap.io/v3/poi/`
**Documentation**: https://openchargemap.org/site/develop/api
**Protocol**: REST
**Auth**: API Key (free registration required)
**Data Format**: JSON / GeoJSON / KML / XML
**Update Frequency**: Near real-time (community-contributed data + aggregated feeds)
**License**: Open Data Commons Open Database License (ODbL)

## What It Provides

Open Charge Map (OCM) is the world's largest open registry of EV charging locations, with over 300,000 locations globally. It aggregates data from government registries, charging networks, and community contributions. Includes station metadata (location, connector types, power levels, networks, usage costs) and some real-time availability data via OCPI integrations.

## API Details

```
GET https://api.openchargemap.io/v3/poi/?output=json&countrycode=DE&maxresults=100&compact=true&verbose=false&key={API_KEY}
```

Key parameters:
- `countrycode` — ISO country code filter
- `latitude`, `longitude`, `distance`, `distanceunit` — geographic bounding
- `maxresults` — pagination (max 5000 per request)
- `compact` — reduces payload size
- `modifiedsince` — delta updates since a given date
- `statustypeid` — filter by operational status
- `connectiontypeid` — filter by connector type (CCS, CHAdeMO, Type 2, etc.)
- `levelid` — filter by power level (1=slow, 2=fast, 3=rapid)

Response includes:
- `ID`, `UUID` — unique identifiers
- `AddressInfo` — location, coordinates, country
- `Connections[]` — connector types, power (kW), current type, quantity
- `OperatorInfo` — charging network name
- `StatusType` — operational status
- `UsageCost` — pricing information (free text)
- `DateLastStatusUpdate` — freshness indicator

## Freshness Assessment

OCM is primarily a registry of locations rather than a real-time availability feed. `DateLastStatusUpdate` indicates when a location was last verified — this can range from days to years old for community-contributed data. However, OCM increasingly integrates real-time OCPI feeds from networks, which provide up-to-the-minute connector status. The `modifiedsince` parameter enables efficient delta polling.

For location/metadata purposes: excellent. For real-time availability: partial and improving.

## Entity Model

- **POI (Point of Interest)**: A charging location with address, coordinates, operator
- **Connection**: Individual connector with type, power level, current type, quantity
- **Operator**: Charging network (e.g., Tesla, ChargePoint, Ionity)
- **Status Type**: Operational, planned, decomissioned, temporarily unavailable
- **Usage Type**: Public, membership required, pay-at-location

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Location data is comprehensive; real-time availability is partial |
| Openness | 3 | ODbL license, free API key registration |
| Stability | 3 | Well-established API, versioned, active community |
| Structure | 3 | Rich JSON schema with nested objects for connections, operators |
| Identifiers | 3 | UUID-based, cross-referenced with network-specific IDs |
| Additive Value | 3 | Global coverage, aggregates multiple sources, one API for everything |
| **Total** | **17/18** | |

## Notes

- API key is free but required — register at https://openchargemap.org/site/profile/register
- Rate limit: 20 requests per second with API key.
- The `modifiedsince` parameter is key for building an efficient bridge — poll for changes rather than full snapshots.
- OCM data quality varies by region. Northern/Western Europe and North America have the best coverage. Government registries (NOBIL, BNA, NDL) tend to be more authoritative for their respective countries.
- OCM can serve as the "GBFS catalog equivalent" for EV charging — one source that covers the world, even if individual country registries offer higher quality.
