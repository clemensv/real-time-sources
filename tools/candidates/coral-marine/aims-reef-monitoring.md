# AIMS Reef Monitoring (Australian Institute of Marine Science)
**Country/Region**: Australia (Great Barrier Reef and tropical waters)
**Publisher**: Australian Institute of Marine Science (AIMS)
**API Endpoint**: `https://api.aims.gov.au/data/` (data services)
**Documentation**: https://www.aims.gov.au/data-technology
**Protocol**: REST / ERDDAP
**Auth**: API Key (free registration)
**Data Format**: JSON, CSV, NetCDF
**Update Frequency**: Near real-time (weather stations), periodic (reef surveys)
**License**: Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU)

## What It Provides
AIMS operates extensive marine monitoring programs for Australian tropical waters, particularly the Great Barrier Reef:
- **Weather stations**: Real-time meteorological and oceanographic data from stations on the GBR
  - Water temperature (sea surface and subsurface)
  - Air temperature, humidity, barometric pressure
  - Wind speed and direction
  - Rainfall, solar radiation
  - Wave height and period
  - Current speed and direction
- **Long-Term Monitoring Program (LTMP)**: Reef health surveys
  - Coral cover and composition
  - Fish assemblages
  - Crown-of-thorns starfish abundance
- **Sea Temperature Monitoring**: Network of subsurface temperature loggers on reefs
- **Water Quality**: Turbidity, chlorophyll, dissolved nutrients

## API Details
- **AIMS Data API**: `https://api.aims.gov.au/data/v1.0` — REST API for datasets
- **Weather station data**: Real-time and historical data from automated stations
- **ERDDAP**: `https://data.aims.gov.au/erddap/` — subset-capable data service
- **Metadata catalog**: `https://apps.aims.gov.au/metadata/` — dataset discovery
- **Key datasets**:
  - AIMS Weather Stations (real-time)
  - Sea Temperature Logger Program
  - Long-Term Monitoring Program surveys
  - Water Quality Monitoring
- **Registration**: Free API key required for programmatic access

Note: API returned 403 at probe time, suggesting authentication is required. AIMS data services may have usage policies.

## Freshness Assessment
Mixed. Weather station data is near real-time (reporting intervals of minutes to hours). Reef health surveys are periodic (annual or biennial). Sea temperature loggers download data at intervals. The weather station network provides the most real-time data.

## Entity Model
- **Station** (site ID, name, lat/lon, reef name, deployment info)
- **Weather Observation** (timestamp, parameter, value, quality flag)
- **Reef Survey** (site, date, transect, coral/fish/COTS data)
- **Temperature Logger** (deployment ID, site, depth, time series)
- **Water Quality** (site, date, parameter, value)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Real-time weather, periodic surveys |
| Openness | 2 | Free registration, CC BY license |
| Stability | 3 | AIMS is a major research institution (est. 1972) |
| Structure | 2 | REST API + ERDDAP, but auth required |
| Identifiers | 2 | Station/site IDs, dataset identifiers |
| Additive Value | 3 | Great Barrier Reef monitoring, unique |
| **Total** | **14/18** | |

## Notes
- AIMS weather stations on the Great Barrier Reef are a valuable real-time data source
- The Long-Term Monitoring Program provides the definitive reef health assessment for Australia
- API key registration is free but adds a step
- ERDDAP server may provide easier programmatic access than the REST API
- Great Barrier Reef Marine Park Authority (GBRMPA) may have additional data feeds
- The combination of real-time weather + reef health surveys is unique
