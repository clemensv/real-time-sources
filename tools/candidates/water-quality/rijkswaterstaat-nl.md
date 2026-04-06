# Rijkswaterstaat Waterinfo — Netherlands Water Quality

**Country/Region**: Netherlands (national water system)
**Publisher**: Rijkswaterstaat (Dutch Directorate-General for Public Works and Water Management)
**API Endpoint**: `https://waterinfo.rws.nl/` (web portal); `https://waterinfo.rws.nl/api/` (internal API)
**Documentation**: https://www.rijkswaterstaat.nl/water/waterdata-en-waterberichtgeving/waterdata
**Protocol**: Web portal + undocumented REST API
**Auth**: None for public web access
**Data Format**: JSON (internal API), HTML (portal)
**Update Frequency**: Real-time (water levels, waves); periodic (water quality)
**License**: Dutch government open data

## What It Provides

Rijkswaterstaat's Waterinfo platform is the Netherlands' central dashboard for all water-related monitoring data:

- **Water levels** (waterstanden) — real-time at ~200 stations
- **Water quality** (waterkwaliteit) — chemical and biological parameters
- **Water temperature**
- **Wave heights and periods**
- **Wind speed and direction** at water stations
- **Salinity** — critical for Dutch fresh/salt water management
- **Current speed and direction**

For water quality specifically, Rijkswaterstaat monitors the major rivers (Rhine, Meuse, Scheldt), estuaries (Wadden Sea, Western Scheldt), major lakes (IJsselmeer, Markermeer), and canals. Parameters include nutrients, heavy metals, pesticides, chlorophyll, turbidity, and dissolved oxygen.

Historical water quality and quantity data is available through the "expert" tab of Waterinfo and through the companion site Waterinfo Extra.

## API Details

The Waterinfo portal uses an internal JSON API that powers the web interface:

```
# Example API calls (undocumented, reverse-engineered)
GET https://waterinfo.rws.nl/api/chart/get?mapType=water-height&locationCode=HOEKVHLD&values=-48,0
GET https://waterinfo.rws.nl/api/nav/expertLocations/water-quality-chart
```

Note: The internal API returned 400/404 errors during testing — it may require specific headers, cookies, or session state from the web application.

Alternative access:
- **DDL (Distributie Laag)**: Rijkswaterstaat's data distribution layer — `https://waterwebservices.rijkswaterstaat.nl/` — SOAP/REST web services for bulk data
- **Waterinfo Extra**: `https://waterinfo-extra.rws.nl/` — project-based monitoring data
- **Open Data**: Some datasets available on `data.overheid.nl`

The DDL web services are the more robust programmatic access point, but use SOAP protocols and require understanding the Dutch water monitoring data model (Aquo standard).

## Freshness Assessment

Good. Water levels are real-time. Water quality data freshness varies — continuous sensors (turbidity, chlorophyll, temperature) are near-real-time; discrete sampling (metals, pesticides) has lab turnaround delays of days to weeks.

## Entity Model

- **Location**: code, name, type (river gauge, lake, estuary), coordinates
- **Parameter**: Aquo parameter code, name, unit, compartment (water/sediment/biota)
- **Observation**: timestamp, location, parameter, value, quality flag
- **Map Type**: category of data (water-height, water-quality, waves, wind, temperature)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Real-time for physical parameters; delayed for chemical WQ |
| Openness | 2 | Public portal; API is undocumented; DDL requires Aquo knowledge |
| Stability | 3 | Dutch government critical infrastructure |
| Structure | 1 | Undocumented web API; DDL uses SOAP; Aquo standard is complex |
| Identifiers | 3 | Aquo parameter codes; location codes; Dutch water body IDs |
| Additive Value | 3 | Rhine/Meuse delta monitoring; salt intrusion data unique; critical for Dutch water management |
| **Total** | **14/18** | |

## Notes

- The Netherlands' relationship with water is existential — 26% of the country is below sea level. Rijkswaterstaat is the world's oldest water management authority.
- Salt intrusion monitoring in the Rhine delta is globally unique and increasingly important under climate change.
- The Aquo standard (Dutch water data exchange standard) is comprehensive but complex — a barrier for non-Dutch developers.
- The DDL web services (`waterwebservices.rijkswaterstaat.nl`) are the proper programmatic interface but poorly documented in English.
- Water quality data from Rijkswaterstaat feeds into the European EEA Waterbase — but the national source has much more detail and better timeliness.
- For a pilot, focus on the continuous sensor data (chlorophyll, turbidity, temperature) which is closest to real-time.
