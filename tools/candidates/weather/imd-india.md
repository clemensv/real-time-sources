# IMD (India Meteorological Department)

**Country/Region**: India
**Publisher**: IMD (India Meteorological Department, Ministry of Earth Sciences)
**API Endpoint**: No public REST API — data available through IITM data portal and mausam.imd.gov.in
**Documentation**: https://mausam.imd.gov.in, https://rds.imd.gov.in (real-time data), https://dsp.imd.gov.in
**Protocol**: Web portal + file downloads + some RSS feeds
**Auth**: Registration required for data portal access
**Data Format**: Mixed — CSV, binary (gridded), web pages, PDF bulletins
**Update Frequency**: 3-hourly synoptic observations, daily gridded products
**License**: Indian Government Open Data — varies by product

## What It Provides

IMD is one of the world's oldest meteorological services (established 1875) and serves 1.4 billion people — the largest population served by any single national met service:

- **Synoptic Observations**: Data from ~700+ surface observatories across India, reporting at standard synoptic hours.

- **Automatic Weather Stations**: Expanding network of AWS stations with more frequent reporting.

- **Cyclone Warnings**: IMD is the WMO Regional Specialized Meteorological Centre (RSMC) for tropical cyclones in the North Indian Ocean. Cyclone tracking, intensity forecasts, and warning bulletins.

- **Monsoon Monitoring**: India's monsoon is the world's most impactful seasonal weather system. IMD provides daily monsoon progress maps, onset/withdrawal dates, and rainfall anomaly monitoring.

- **Heat Wave / Cold Wave Alerts**: Critical for India's extreme temperature events.

- **Gridded Rainfall Data**: High-resolution daily gridded rainfall analysis covering all of India.

- **Satellite Imagery**: From INSAT-3D/3DR geostationary satellites.

- **NWP Products**: GFS, WRF model outputs for the Indian subcontinent.

- **Air Quality Monitoring**: In collaboration with CPCB (Central Pollution Control Board).

## API Details

IMD does **not** provide a modern REST API for real-time data. Data access is through:

1. **Real-time Weather Data Portal** (rds.imd.gov.in): Requires registration, provides station observations.
2. **Data Supply Portal** (dsp.imd.gov.in): Formal data request system for research/commercial use.
3. **IITM Pune Data Portal**: Some datasets available through the Indian Institute of Tropical Meteorology.
4. **Mausam website**: Forecasts and warnings published as web pages and PDF bulletins.
5. **RSS/XML feeds**: Some forecast text products available via RSS.

The main website (mausam.imd.gov.in) is primarily a news/press release portal with limited structured data access.

## Freshness Assessment

- Synoptic observations: 3-hourly at main stations.
- AWS data: More frequent but access is restricted.
- Cyclone bulletins: Issued every 3–6 hours during active systems.
- Monsoon monitoring: Daily updates during June–September.
- The data is generated in near-real-time, but programmatic access is the bottleneck.

## Entity Model

- **Station**: IMD station number (correlates with WMO block numbers for main stations).
- **Observation**: Standard synoptic parameters per station per observation time.
- **Cyclone**: Named cyclone with track, intensity, warnings by coastal zone.
- **Gridded Product**: 0.25° × 0.25° daily rainfall analysis over India.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Data exists in near-real-time, but access delays due to portal-based delivery |
| Openness | 1 | No public API; registration required; some data behind formal request process |
| Stability | 2 | 150-year-old institution, but digital infrastructure lags behind data richness |
| Structure | 1 | Mixed formats (web pages, PDFs, CSV, binary), no modern API |
| Identifiers | 2 | IMD/WMO station numbers for main stations |
| Additive Value | 3 | 1.4 billion people served, monsoon monitoring, RSMC for Indian Ocean cyclones |
| **Total** | **11/18** | |

## Notes

- The gap between IMD's data richness and its data accessibility is one of the largest in global meteorology.
- For 1.4 billion people, IMD's real-time data infrastructure is surprisingly limited compared to smaller nations (Singapore, Denmark, Austria).
- Cyclone tracking data from IMD is irreplaceable — they are the authoritative source for the North Indian Ocean basin.
- Monsoon monitoring data is globally unique and scientifically critical — the Indian monsoon affects weather patterns worldwide.
- India's Digital India initiative may drive improvements in API infrastructure — worth monitoring.
- For integration, consider accessing Indian station data through OGIMET (WMO GTS) or Open-Meteo (which aggregates some IMD data) as workarounds.
- The IITM (Indian Institute of Tropical Meteorology) in Pune sometimes provides more accessible data portals than IMD itself.
