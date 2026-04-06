# GRDC (Global Runoff Data Centre)

**Country/Region**: Global
**Publisher**: Global Runoff Data Centre, Federal Institute of Hydrology (BfG), Germany
**API Endpoint**: `https://portal.grdc.bafg.de/` (web portal)
**Documentation**: https://grdc.bafg.de/
**Protocol**: Web portal with download interface
**Auth**: Registration required for data access
**Data Format**: Various (download portal)
**Update Frequency**: Monthly to annual updates (historical archive)
**Station Count**: 10,000+ stations from 161 countries
**License**: GRDC data policy (free for non-commercial use, registration required)

## What It Provides

GRDC is the world's largest repository of river discharge data:
- **Daily and monthly river discharge** time series
- **10,000+ gauging stations** across 161 countries
- Historical records spanning decades to over a century
- Quality-controlled data contributed by national hydrological services
- Global coverage with best coverage in Europe, North America, and Australia

GRDC data is primarily historical/archival rather than real-time.

## API Details

### Web portal
```
GET https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser
```
Loading page for the GRDC data portal — a web application that provides:
- Station search and selection
- Data download in various formats
- Map-based station discovery

### No REST API
Probing of common API patterns (`/rest/`, `/api/`) returned 404 errors. The portal uses a KiWeb framework (Kisters) for data management.

### Data access
1. Register at https://grdc.bafg.de/
2. Search stations via web portal
3. Request data download
4. Receive data via email or direct download

### WMO WHOS integration
GRDC contributes data to the WMO WHOS system, potentially making some GRDC data accessible via the WHOS OpenSearch API.

## Freshness Assessment

- GRDC is an archival service, not a real-time monitoring system
- Data updates lag months to years behind real-time
- Latest data availability depends on contributing national services
- Some "near-real-time" capabilities may exist for recent data

## Entity Model

- **Station**: GRDC number, name, country, river, lat/lon, catchment area
- **Time series**: daily/monthly mean discharge (m³/s)
- **Metadata**: period of record, data quality flags, contributing agency

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | No public REST API; web portal only |
| Data Richness | 3 | World's largest river discharge archive, 161 countries |
| Freshness | 0 | Historical archive; not real-time data |
| Station Coverage | 3 | 10,000+ stations globally |
| Documentation | 2 | Data policy and metadata well documented; no API docs |
| License/Access | 1 | Free registration required; non-commercial use |
| **Total** | **9/18** | |

## Notes

- GRDC is the gold standard for historical river discharge data but unsuitable for real-time monitoring
- Managed under WMO auspices since 1988
- Data sharing depends on voluntary contributions from national hydrological services
- Uses Kisters KiWeb platform (same vendor as Australia BOM and Scotland SEPA)
- Integration would require batch download and periodic refresh, not streaming
- Could serve as a reference dataset for station metadata and historical context
- Alternative: GloFAS uses GRDC data for model calibration and provides near-real-time outputs
- The GRDC station catalogue itself is valuable as a global reference for gauging station locations
