# BOM Australian Baseline Sea Level Monitoring Project (ABSLMP)

**Country/Region**: Australia (14 standard monitoring stations around the coast)
**Publisher**: Bureau of Meteorology (BOM), Australian Government
**API Endpoint**: `https://www.bom.gov.au/oceanography/projects/abslmp/data/index.shtml` (file downloads)
**Documentation**: https://www.bom.gov.au/oceanography/projects/abslmp/abslmp.shtml
**Protocol**: HTTP file download (CSV)
**Auth**: None for ABSLMP data; some BOM tide services require registration
**Data Format**: CSV (hourly sea level + meteorological data)
**Update Frequency**: Monthly (data files updated on a monthly basis)
**License**: Crown Copyright, CC BY 3.0 AU

## What It Provides

The ABSLMP is Australia's primary high-quality sea level monitoring network, consisting of 14 tide gauge stations around the Australian coastline. These stations were established to measure long-term sea level change and provide geodetic-quality measurements tied to national levelling networks and GNSS.

Data includes:
- Hourly sea level observations (mm)
- Co-located meteorological data (atmospheric pressure, wind, temperature)
- Data from 1991 to present for most stations

Standard stations: Cape Ferguson (QLD), Rosslyn Bay (QLD), Port Kembla (NSW), Burnie (TAS), Spring Bay (TAS), Portland (VIC), Port Stanvac (SA), Thevenard (SA), Esperance (WA), Hillarys (WA), Broome (WA), Darwin (NT), Cocos/Keeling Islands, Groote Eylandt (NT).

## API Details

No REST API. Data is accessed via direct CSV file downloads organized by station and year:

URL pattern: `https://www.bom.gov.au/ntc/IDO7100{N}/IDO7100{N}_{YEAR}.csv`

Where `{N}` is the station number (1-16) and `{YEAR}` is the four-digit year.

Example: `https://www.bom.gov.au/ntc/IDO71001/IDO71001_2026.csv` for Cape Ferguson 2026 data.

Each file contains hourly records with columns for date/time, sea level, atmospheric pressure, and other met variables. Files are typically 692-694 KB per year.

For real-time operational tide data, BOM provides separate tide prediction and observation services, but these are not as well-structured for programmatic access.

## Freshness Assessment

Moderate. Data files are updated monthly. Not suitable for real-time operational use. For operational Australian tide data, the BOM Pacific Sea Level Monitoring project or the IOC SLSMF would provide faster updates (though with less QC).

## Entity Model

- **Station**: IDO station code, name, state, latitude, longitude, geodetic tie info
- **Observation**: timestamp (hourly), sea level (mm), atmospheric pressure, wind speed/direction, air temperature
- **Annual File**: station + year CSV

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Monthly updates only |
| Openness | 3 | Free download, CC BY 3.0 AU license |
| Stability | 3 | Government-operated since 1991, long-term commitment |
| Structure | 1 | File-based CSV downloads, no API; but predictable URL pattern |
| Identifiers | 2 | IDO codes; limited cross-referencing to international IDs |
| Additive Value | 2 | Australian coast + Cocos/Keeling Islands; co-located met data is a plus |
| **Total** | **12/18** | |

## Notes

- The BOM also operates the Pacific Sea Level and Geodetic Monitoring (PSLM) project covering Pacific island nations — see separate entry.
- For real-time Australian tide data, the BOM Water Data Online service (Kisters WISKI-based) may provide faster access, though it's oriented more toward river/inland water.
- The co-located meteorological data (pressure, wind) alongside sea level is valuable for surge analysis.
- The predictable URL pattern makes automated ingestion feasible despite the lack of a formal API.
- BOM charges fees for some tide prediction products — the ABSLMP observational data is free.
