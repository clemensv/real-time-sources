# EFAS (European Flood Awareness System)
**Country/Region**: Europe
**Publisher**: Copernicus Emergency Management Service / European Commission
**API Endpoint**: `https://european-flood.emergency.copernicus.eu/` (CDS API for data access)
**Documentation**: https://www.efas.eu/en
**Protocol**: REST / WMS / CDS API
**Auth**: ECMWF/CDS account required
**Data Format**: NetCDF, GeoTIFF, JSON (via CEMS portal)
**Update Frequency**: Twice daily (forecasts), real-time (flash flood notifications)
**License**: Copernicus data policy (free, open for redistribution with attribution)

## What It Provides
EFAS provides pan-European flood forecasting and monitoring:
- Flood forecasts (up to 15 days ahead) for all European river basins
- Flash flood indicators
- Flood notifications to national authorities
- River discharge observations and forecasts
- Soil moisture and snow water equivalent data
- Historical flood event data

EFAS is the early warning component of the Copernicus Emergency Management Service (CEMS).

## API Details
- **EFAS Web Portal**: `https://european-flood.emergency.copernicus.eu/` — interactive map with current flood situation
- **CDS API**: `https://cds.climate.copernicus.eu/api/v2` — programmatic access to EFAS datasets
- **WMS/WFS Services**: Available for map layers (river network, flood extent)
- **EFAS Notifications**: Formal flood alerts to registered national authorities (not public API)
- **GloFAS (Global)**: `https://global-flood.emergency.copernicus.eu/` — global flood awareness
- **Datasets available via CDS**: `efas-forecast`, `efas-historical`, `efas-seasonal`, `efas-reanalysis`

## Freshness Assessment
Good. Forecasts are updated twice daily (00 and 12 UTC). Flash flood indicators update more frequently. The web portal shows near real-time situation. However, raw data access requires CDS API registration.

## Entity Model
- **River Reach** (identified by river segment ID)
- **Forecast** (river discharge, return period exceedance, valid time)
- **Alert Level** (informal/formal based on return period thresholds)
- **Grid Cell** (for flash flood and soil moisture products)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Twice-daily forecasts, not instantaneous |
| Openness | 2 | Free but requires CDS account registration |
| Stability | 3 | EU Copernicus programme, long-term funded |
| Structure | 2 | NetCDF/GeoTIFF primary, limited JSON |
| Identifiers | 2 | River segment IDs but complex grid system |
| Additive Value | 3 | Unique pan-European flood forecasting |
| **Total** | **14/18** | |

## Notes
- CDS API registration is free but mandatory
- Data volumes can be large (NetCDF grids covering all of Europe)
- Most useful for forecast/early warning rather than real-time observation
- GloFAS extends coverage globally but at lower resolution
- Consider pairing with national services (like pegelonline) for real-time water levels
