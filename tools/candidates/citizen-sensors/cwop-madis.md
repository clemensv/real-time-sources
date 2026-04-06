# CWOP/MADIS (Citizen Weather Observer Program)

**Country/Region**: Global (strongest in North America)
**Publisher**: NOAA/NWS (MADIS) / CWOP volunteer network
**API Endpoint**: `https://madis-data.ncep.noaa.gov/` (MADIS); CWOP via APRS-IS `rotate.aprs2.net:14580`
**Documentation**: https://madis.ncep.noaa.gov/, https://www.wxqa.com/
**Protocol**: APRS-IS (TCP/text stream) for CWOP; HTTP/FTP for MADIS
**Auth**: MADIS requires free account; CWOP/APRS-IS read access with passcode `-1`
**Data Format**: APRS packets (text); MADIS provides netCDF, XML, CSV
**Update Frequency**: 5-15 minutes (per station); MADIS hourly aggregation
**License**: US Government public domain (MADIS); CWOP data is freely shared

## What It Provides

CWOP (Citizen Weather Observer Program) is a network of thousands of personal weather stations contributing data via the APRS (Automatic Packet Reporting System) network. MADIS (Meteorological Assimilation Data Ingest System) aggregates CWOP data along with other sources and provides quality-controlled observations. Together they represent the largest citizen weather network feeding into operational meteorology.

CWOP stations report temperature, humidity, barometric pressure, wind speed/direction/gust, rainfall, and sometimes solar radiation and UV index.

## API Details

- **APRS-IS stream**: Connect to `rotate.aprs2.net:14580` with filter `r/LAT/LON/RANGE` or `p/CW`/`p/DW` for CWOP stations
- **Authentication**: Send `user N0CALL pass -1 vers MyApp 1.0 filter r/38/-97/500` — passcode `-1` grants read-only access
- **CWOP data**: Station IDs prefixed with CW or DW followed by numbers
- **MADIS portal**: https://madis-data.ncep.noaa.gov/ — register for free account, download hourly files
- **MADIS API**: XML/CSV feeds via `https://madis-data.ncep.noaa.gov/madisPublic1/data/` (after authentication)
- **Quality flags**: MADIS adds QC flags (validity, temporal consistency, spatial consistency)
- **Mesonet API**: `https://mesonet.agron.iastate.edu/` provides MADIS data in more accessible formats

## Freshness Assessment

CWOP via APRS-IS is real-time — packets arrive within seconds of station transmission. MADIS aggregates hourly with quality control. For real-time applications, the APRS-IS stream is superior but requires TCP socket handling. MADIS provides curated data with some delay.

## Entity Model

- **Station**: CWOP ID (e.g., CW1234), lat/lon, elevation, equipment type
- **Observation**: Timestamp, temperature, humidity, pressure, wind (speed/dir/gust), rain (1h/24h/midnight), solar radiation
- **APRS Packet**: Raw text packet with encoded position and weather data
- **QC Flag** (MADIS): Quality control level per parameter

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time via APRS-IS; hourly via MADIS |
| Openness | 2 | APRS-IS is open-read; MADIS needs free account |
| Stability | 3 | NOAA/NWS infrastructure; APRS running since 1990s |
| Structure | 1 | APRS is a legacy text format; MADIS netCDF is specialized |
| Identifiers | 2 | CWOP station IDs; no formal URI scheme |
| Additive Value | 2 | Citizen weather is widely available; unique as APRS real-time stream |
| **Total** | **13/18** | |

## Notes

- APRS-IS is a fascinating legacy system — a TCP text stream of ham radio packets routed over the internet.
- The APRS protocol dates back to 1992 and is still actively used by thousands of amateur radio operators.
- CWOP data is ingested by the US National Weather Service for forecast initialization.
- MADIS also ingests data from commercial weather networks, airports, and marine stations — CWOP is one of many sources.
- The Iowa State Mesonet (mesonet.agron.iastate.edu) provides more accessible web APIs for MADIS data.
