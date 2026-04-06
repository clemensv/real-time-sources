# India CWC / India-WRIS

**Country/Region**: India
**Publisher**: Central Water Commission (CWC), Ministry of Jal Shakti
**API Endpoint**: `https://cwc.gov.in/` (401 Unauthorized), `https://indiawris.gov.in/wris/` (connection failures)
**Documentation**: https://cwc.gov.in/ , https://indiawris.gov.in/
**Protocol**: Unknown (auth-gated / unreachable)
**Auth**: Required (401 on cwc.gov.in)
**Data Format**: Unknown
**Update Frequency**: Real-time (CWC telemetry)
**Station Count**: 1500+ telemetric stations, 5000+ overall
**License**: Indian government data

## What It Provides

India has one of the world's largest hydrological monitoring networks:

### CWC (Central Water Commission)
- Real-time flood monitoring and forecasting
- River water level and discharge at 1500+ telemetric stations
- Reservoir monitoring (140+ major reservoirs)
- Flood forecasting for major river basins

### India-WRIS (Water Resources Information System)
- Comprehensive water resources geospatial database
- Basin-level water accounting
- Dam and reservoir inventory
- Groundwater, surface water, and water quality

## API Details

### CWC endpoints
- `https://cwc.gov.in/` — returns 401 Unauthorized (JSON response)
- Authentication required but mechanism unknown
- CWC data historically available via waterdata portal

### India-WRIS endpoints
- `https://indiawris.gov.in/wris/` — connection timeout
- `https://ffs.india-water.gov.in/` — connection timeout
- India-WRIS provides WMS/WFS services for registered users

### Flood forecasting
CWC publishes daily flood bulletins and operates a flood forecasting network for major rivers (Ganga, Brahmaputra, Godavari, Krishna, Mahanadi, etc.)

## Freshness Assessment

- CWC operates real-time telemetry (15-minute to hourly updates)
- Both CWC and India-WRIS portals inaccessible during testing
- India's monsoon season flood monitoring is a critical real-time application
- Data has been historically available through dedicated portals

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 0 | 401 Unauthorized / connection failures |
| Data Richness | 3 | Comprehensive: rivers, reservoirs, groundwater, floods |
| Freshness | 2 | Real-time telemetry exists; API access blocked |
| Station Coverage | 3 | 5000+ stations covering India's vast river network |
| Documentation | 1 | Website documentation exists |
| License/Access | 0 | Auth required; connectivity issues |
| **Total** | **9/18** | |

## Notes

- India's hydrological data would be enormously valuable — 1.4 billion people dependent on these rivers
- CWC's 401 response suggests an API exists behind authentication
- India-WRIS is a well-funded government initiative that should have API capabilities
- Access restrictions may be related to security concerns around critical water infrastructure
- Previously dismissed with same findings — revisited and confirmed inaccessible
- India's open data initiatives (data.gov.in) may have some hydrological datasets
- The monsoon-dependent hydrology makes real-time data particularly critical
