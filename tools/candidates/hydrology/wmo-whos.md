# WMO WHOS (World Hydrological Observing System)

**Country/Region**: Global (multi-basin)
**Publisher**: World Meteorological Organization (WMO) / GEO DAB (ESSI-Lab)
**API Endpoint**: `https://whos.geodab.eu/gs-service/services/essi/view/{view}/opensearch`
**Documentation**: https://community.wmo.int/en/activity-areas/whos , https://whos.geodab.eu
**Protocol**: OpenSearch (XML) / REST
**Auth**: None (public OpenSearch descriptors)
**Data Format**: XML (OpenSearch), potentially WaterML
**Update Frequency**: Varies by contributing national service
**Station Count**: Varies by view/basin (WHOS aggregates multiple national networks)
**License**: WMO Resolution 40 / Resolution 60 (data sharing for non-commercial use)

## What It Provides

WHOS is the WMO's federated hydrological data sharing framework. It aggregates real-time and historical hydrological data from multiple national services through a common discovery and access API. Multiple "views" exist for different basins and regions:

- **WHOS-Plata** — La Plata basin (Argentina, Brazil, Uruguay, Paraguay, Bolivia)
- **WHOS-Arctic** — Arctic hydrological observing network
- Other regional WHYCOS programs may be accessible

## API Details

### OpenSearch descriptor
```
GET https://whos.geodab.eu/gs-service/services/essi/view/whos-plata/opensearch
```
Returns XML OpenSearchDescription with query templates. Supported parameters include:
- `si` — start index (pagination)
- `ct` — count (results per page)
- `st` — search terms
- `ts`, `te` — time start/end
- `sources` — filter by data source
- `observedPropertyURI` — observed variable
- `platformId`, `platformTitle` — station identifiers
- `organisationName` — contributing organization
- Geo bounding box parameters

### Available views
- `whos-plata` — La Plata basin
- `whos-arctic` — Arctic region
- Other views may exist (not exhaustively probed)

### Query endpoint template
```
GET https://whos.geodab.eu/gs-service/services/essi/view/{view}/query?si=1&ct=10&st=water+level
```
Note: Direct query returned 404 in testing — may require specific parameter combinations.

### Metadata format
Responses use the GI-Suite schema (`application/gs-schema+xml`) with support for WaterML, SOS, and other OGC standards.

## Freshness Assessment

- WHOS is a discovery/brokering layer — freshness depends on contributing national services
- The OpenSearch descriptor is live and maintained
- Query execution was not fully confirmed during testing (404 on generic queries)
- La Plata view aggregates data from ANA (Brazil), INA (Argentina), DINAGUA (Uruguay)

## Entity Model

- **View**: regional/basin scope (plata, arctic, etc.)
- **Platform**: station/gauge with identifier and title
- **Observed Property**: URI-based variable identification (water level, discharge, etc.)
- **Organization**: contributing national hydrological service
- **Observation**: time series via WaterML or similar encoding
- **Instrument**: sensor metadata

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 1 | OpenSearch descriptor works; actual query execution not confirmed |
| Data Richness | 2 | Potentially rich (aggregates multiple national networks) but access unverified |
| Freshness | 1 | Depends on contributing services; not directly tested |
| Station Coverage | 2 | Multi-country aggregation possible but extent unknown |
| Documentation | 2 | WMO documentation exists; technical API docs sparse |
| License/Access | 2 | Public descriptor; actual data access terms per WMO resolutions |
| **Total** | **10/18** | |

## Notes

- WHOS is a meta-platform, not a direct data source — it brokers access to national hydrological services
- The GI-Suite backend (ESSI-Lab) is a well-known geospatial brokering middleware
- OpenSearch is an older protocol; may be supplemented by OGC API standards in future
- For the La Plata basin, this could provide unified access to Argentine, Brazilian, and Uruguayan data
- The Arctic view is relevant for climate/cryosphere monitoring
- Integration complexity is high due to XML-heavy protocols and indirect data access
- Better suited as a discovery layer than a direct real-time feed
- WMO is actively developing WHOS as the backbone of international hydrological data exchange
