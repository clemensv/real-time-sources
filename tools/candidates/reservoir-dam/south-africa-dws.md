# South Africa DWS — Dam Levels

**Country/Region**: South Africa (~250 major dams monitored)
**Publisher**: Department of Water and Sanitation (DWS), Government of South Africa
**API Endpoint**: `https://www.dws.gov.za/Hydrology/Weekly/dam.aspx` (web portal)
**Documentation**: https://www.dws.gov.za/Hydrology/
**Protocol**: Web portal (ASP.NET); no documented REST API
**Auth**: None for public web access
**Data Format**: HTML tables, CSV downloads
**Update Frequency**: Weekly (some data reported daily via hydrological services)
**License**: South African government open data

## What It Provides

DWS publishes weekly dam level reports for South Africa's ~250 monitored dams, covering:

- **Storage volume** (million m³) and **percentage full**
- **Last year comparison**
- **River inflow** at major gauging stations
- **Grouped by water management area** (9 WMAs across South Africa)

South Africa is a water-scarce country where dam levels are a critical socioeconomic indicator. The 2015–2018 Cape Town water crisis ("Day Zero") demonstrated how dam storage data can become front-page news globally. Major systems include Vaal Dam (Gauteng/Johannesburg water supply), Theewaterskloof (Cape Town), and Sterkfontein (inter-basin transfer).

DWS also operates the national hydrological monitoring network with ~3,000 flow gauging stations.

## API Details

No documented REST API. The web portal at `https://www.dws.gov.za/Hydrology/Weekly/dam.aspx` returned 403 during testing, but the page is normally accessible through a browser.

Alternative access paths:
- **Hydrological Services Portal**: `https://www.dws.gov.za/Hydrology/` — flow and dam data downloads
- **Dam Safety Office reports**: Annual dam safety surveillance data
- **Verified CSV downloads**: Historical dam level data available as CSV files through the hydrology section

The DWS hydrological information system also serves river flow data via numbered station gauges (e.g., C2H007 for stations on the Vaal).

## Freshness Assessment

Moderate. Weekly dam level reports are standard for reservoir monitoring. The underlying telemetry network reports more frequently, but public-facing data is aggregated weekly. The web portal is sometimes slow or intermittently accessible.

## Entity Model

- **Dam**: name, river, water management area, full supply capacity (million m³), dam wall height
- **Weekly Report**: date, storage volume, percentage full, last year volume
- **Water Management Area**: name, code, major dams, total capacity
- **Gauging Station**: station number (e.g., C2H007), river, lat/lon

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Weekly dam reports; some daily river flow data |
| Openness | 1 | Public web portal but intermittent access (403 errors); no REST API |
| Stability | 1 | Government portal but infrastructure is unreliable; frequent downtime |
| Structure | 1 | ASP.NET web forms; HTML tables; no standardized API |
| Identifiers | 2 | Dam names; hydrological station numbers (standardized within SA) |
| Additive Value | 3 | Water-scarce nation; dam levels are critical socioeconomic indicator; Cape Town "Day Zero" context |
| **Total** | **10/18** | |

## Notes

- The data is critically important but poorly accessible. South Africa's dam levels are watched closely by analysts, farmers, and water managers.
- The "Day Zero" Cape Town crisis in 2017-2018 made global headlines and demonstrated the real-world impact of this data.
- Web scraping is likely required for automated access — the ASP.NET portal uses ViewState/postback patterns that complicate extraction.
- Third-party aggregators (e.g., `damlevels.co.za`) exist and may provide cleaner scraping targets.
- Consider pairing with South African Weather Service (SAWS) rainfall data for drought monitoring.
- The hydrological station numbering system (e.g., A2H012) encodes drainage region, sub-region, and station type — useful metadata.
