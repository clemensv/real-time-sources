# Veðurstofa Íslands (Icelandic Met Office)

**Country/Region**: Iceland
**Publisher**: Veðurstofa Íslands (Icelandic Meteorological Office / IMO)
**API Endpoint**: `https://xmlweather.vedur.is/` (legacy XML), `https://en.vedur.is/` (web)
**Documentation**: https://en.vedur.is/about-imo/open-data/ (formerly — may have moved)
**Protocol**: XML web service (legacy), web scraping required for some data
**Auth**: None documented
**Data Format**: XML (observations), web pages
**Update Frequency**: Hourly (observations), real-time (warnings, volcanic activity)
**License**: Icelandic Open Government Data

## What It Provides

The Icelandic Met Office provides weather observation data and, critically, volcanic and seismic monitoring for one of the world's most volcanically active countries:

- **Weather Observations**: Temperature, wind, humidity, pressure, precipitation from Iceland's station network.

- **Weather Warnings**: Regional weather alerts for Iceland's forecast areas (Reykjavik, South Iceland, Westfjords, Northeast, East, etc.). Color-coded alert system (yellow/orange/red).

- **Weather Forecasts**: Regional and local forecasts.

- **Volcanic Activity Monitoring**: Real-time information on eruptions (critical — the Sundhnúkur crater row has had 9 eruptions since 2023), aviation color codes, hazard maps.

- **Seismic Activity**: Earthquake monitoring (Iceland has thousands of earthquakes per year).

- **Avalanche Warnings**: Snow avalanche risk assessments for Icelandic regions.

## API Details

The legacy XML weather service at `xmlweather.vedur.is` appears to have been deprecated or restricted — probed endpoints returned error messages ("No more content available").

Current data access appears to be primarily through the vedur.is website. Weather observation tables and warnings are published on web pages.

The open data portal URL previously documented (https://en.vedur.is/about-imo/open-data/) returned 404, suggesting restructuring of the data access points.

Warnings are available on the website with structured regional areas.

## Freshness Assessment

- Weather observations: Updated hourly from Iceland's station network.
- Warnings: Real-time, with current yellow alerts observed for multiple regions.
- Volcanic monitoring: Continuously updated during active eruptions.
- The website shows current data, but programmatic access routes appear to have changed.

## Entity Model

- **Station**: Icelandic station identifiers.
- **Region**: Named forecast/warning areas (Reykjavik - Capital Region, South Iceland, Westfjords, etc.).
- **Warning**: Color-coded (yellow/orange/red) by region and hazard type.
- **Volcanic Event**: Crater row, eruption number, aviation color code, hazard map.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly observations, real-time warnings and volcanic alerts |
| Openness | 1 | Legacy API appears deprecated; current data access unclear |
| Stability | 2 | National met office, but API infrastructure in transition |
| Structure | 1 | Legacy XML endpoint broken; web scraping may be needed |
| Identifiers | 2 | Station IDs, regional names — limited documentation |
| Additive Value | 3 | Unique volcanic/seismic monitoring, Arctic/North Atlantic coverage |
| **Total** | **11/18** | |

## Notes

- The real value here is volcanic monitoring — Iceland's Sundhnúkur eruptions (9 since 2023) demonstrate the critical importance of this data.
- The legacy XML weather API (`xmlweather.vedur.is`) appears to have been decommissioned or restricted, significantly reducing programmatic access.
- Aviation color codes for volcanic ash (critical for transatlantic flight routing) are issued by IMO.
- Avalanche warnings are a unique product not available from most met services.
- Worth monitoring for API reconstruction — Iceland's government is generally pro-open-data.
- For weather observation data, consider using OGIMET or the IEM to access Iceland's WMO station reports as a workaround.
- The website itself provides valuable warning information but would require scraping for programmatic access.
