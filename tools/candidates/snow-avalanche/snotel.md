# SNOTEL (SNOwpack TELemetry)
**Country/Region**: United States (Western states, Alaska)
**Publisher**: USDA Natural Resources Conservation Service (NRCS)
**API Endpoint**: `https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customSingleStationReport/hourly/start_of_period/{stationTriplet}/-1,0/WTEQ::value,PREC::value,TOBS::value,SNWD::value`
**Documentation**: https://www.nrcs.usda.gov/wps/portal/wcc/home/dataAccessHelp/webService/
**Protocol**: REST (Report Generator CSV API)
**Auth**: None
**Data Format**: CSV (with metadata header comments)
**Update Frequency**: Hourly (automated telemetry)
**License**: US Government public domain

## What It Provides
SNOTEL is a network of over 900 automated snow monitoring stations across the western United States and Alaska, reporting:
- **Snow Water Equivalent (SWE)** — depth of water if snowpack melted
- **Snow Depth** — total snow depth in inches
- **Precipitation Accumulation** — water-year cumulative precipitation
- **Air Temperature** — instantaneous observed temperature
- **Soil Moisture & Temperature** (at some stations)
- **Wind Speed/Direction** (at some stations)

## API Details
- **Report Generator**: `https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customSingleStationReport/{frequency}/start_of_period/{stationTriplet}/{timeRange}/{elements}`
- **Station triplet format**: `{stationId}:{state}:SNTL` (e.g., `838:CO:SNTL` for University Camp, CO)
- **Frequencies**: `hourly`, `daily`, `monthly`
- **Time range**: `-1,0` (last day), `-7,0` (last week), `POR_BEGIN,POR_END` (full record)
- **Elements**: `WTEQ::value` (SWE), `SNWD::value` (snow depth), `PREC::value` (precip), `TOBS::value` (temp), `TMAX::value`, `TMIN::value`
- **Station list**: `https://wcc.sc.egov.usda.gov/nwcc/inventory` (various formats)
- **AWDB Web Service**: SOAP service also available at `https://wcc.sc.egov.usda.gov/awdbWebService/services`

Confirmed working: station 838:CO:SNTL returned hourly data with SWE=8.9in, Precip=16.30in, Temp=21.7°F, Depth=28in.

## Freshness Assessment
Excellent. Stations report hourly via satellite telemetry (GOES/Meteor Burst). Data appears within minutes of collection. The Report Generator returns current-hour data. Quality flags indicate data may be Raw (R) initially, upgraded to Provisional (P) and Approved (A) after review.

## Entity Model
- **Station** (triplet ID, name, state, elevation, lat/lon, network type)
- **Observation** (datetime, element code, value, quality control flag, quality assurance flag)
- **Elements**: WTEQ (Snow Water Equivalent), SNWD (Snow Depth), PREC (Precipitation), TOBS (Air Temp), TMAX, TMIN, TAVG, SMS (Soil Moisture), STO (Soil Temp)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly automated telemetry |
| Openness | 3 | Public domain, no auth |
| Stability | 3 | USDA operational network since 1977 |
| Structure | 2 | CSV with comment headers, not JSON |
| Identifiers | 3 | Stable station triplet IDs |
| Additive Value | 3 | Unique 900+ station snowpack network |
| **Total** | **17/18** | |

## Notes
- CSV format requires parsing comment headers (lines starting with `#`)
- Known temperature bias in sensor data (documented by NRCS)
- AWDB SOAP service is older but provides more query flexibility
- Stations are mostly in mountainous western US — excellent for ski/avalanche/water supply monitoring
- Data includes quality flags (V=Valid, S=Suspect, M=Missing, etc.)
