# Bahrain Meteorological Directorate - Official Weather Data

- **Country/Region**: Bahrain (BH)
- **Endpoint**: `https://bahrainweather.gov.bh` (web portal)
- **Protocol**: Website only (no documented API found)
- **Auth**: N/A
- **Format**: HTML
- **Freshness**: Daily forecasts visible on website
- **Docs**: None (website only)
- **Score**: 3/18

## Overview

The Bahrain Meteorological Directorate operates under the Ministry of Transportation
and Telecommunications (MTT). The directorate is responsible for weather forecasting,
marine forecasts, aviation meteorology (METAR/TAF for Bahrain International Airport),
and climate monitoring for the Kingdom of Bahrain.

The main website (https://bahrainweather.gov.bh) displays current conditions, daily
and weekly forecasts, marine forecasts (wind, sea state), and weather warnings (e.g.,
for strong winds, dust storms, thunderstorms). The site shows hourly forecast icons,
temperature, wind direction, humidity ranges, and descriptive text for each day.

According to MTT announcements, the Meteorological Directorate has recently:
- Launched third-generation weather satellites system
- Installed two new automated weather stations across Bahrain
- Upgraded the Bahrain Weather mobile application
- Modernized the climatological database system

However, **no public API or machine-readable data endpoint was found** during discovery.
The website serves HTML content for human consumption only. No REST API, JSON/XML feeds,
RSS, or data download service is documented or discoverable.

## Endpoint Analysis

**Website probed:**
```
https://bahrainweather.gov.bh
https://bahrainweather.gov.bh/web/guest/api (404 - no API docs)
https://bahrainweather.gov.bh/web/guest/current-observation (404)
https://bahrainweather.gov.bh/web/guest/marine (404)
```

The main portal loads successfully and displays forecast data in HTML, but no
structured data endpoints are accessible. The site uses a Liferay CMS framework,
which could theoretically support REST services, but none are publicly exposed or
documented.

**Sample forecast data visible on website (May 2026):**
- Hourly forecast icons (clear sky, rising sand, etc.)
- Wind: "NW'ly 12 to 17kt reaching 20 to 25kt at times"
- Sea state: "1 to 3ft inshore, 3 to 6ft offshore"
- Warnings: "For strong winds"
- Humidity: min/max percentages (not shown in current view)
- Sunrise/sunset times
- Daily descriptive text: "Rather hot during the day and fine overnight with rising sand in places"

This data is rich and relevant (wind speed/direction, dust/sand warnings, marine
conditions, temperature descriptors), but it is **embedded in HTML and not available
via structured API**.

## Integration Notes

**Current state:**
- No machine-readable endpoint found
- No API documentation published
- No JSON/XML/CSV data feeds
- HTML scraping would be required

**Feasibility:**
- **Web scraping**: Technically possible to parse the forecast table HTML, but fragile
  (site redesigns would break the bridge). Scraping is against repo policy for sources
  without stable APIs.
- **METAR/TAF alternative**: Bahrain International Airport (OBBI) METAR and TAF data
  are available through the global Aviation Weather API (aviationweather.gov), which
  is a separate, stable, well-documented source. This covers airport-level observations
  and forecasts but not broader Bahrain weather or marine forecasts.
- **WMO data exchange**: Bahrain is a WMO member and contributes SYNOP observations to
  the Global Telecommunication System (GTS). These observations may be available through
  international aggregators (e.g., ECMWF open data, NOAA ISD), but not directly from
  Bahrain Meteorological Directorate.

**Potential future developments:**
The Ministry of Transportation and Telecommunications has announced modernization of
the climatological database and upgrade of the Bahrain Weather mobile application.
If these initiatives include a public API or open data portal, this source could
become viable. Monitor:
- MTT announcements: https://www.mtt.gov.bh
- IGA open data portal: https://data.gov.bh (CKAN-based, but current API appears down)
- Bahrain eGovernment initiatives

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Daily forecasts visible, but hourly detail present |
| Openness | 0 | No API, HTML only, would require scraping |
| Stability | 1 | Government website is stable, but no API contract |
| Structure | 0 | HTML only, no JSON/XML/CSV |
| Identifiers | 1 | Could key by station or forecast zone, but no formal IDs exposed |
| Additive value | 0 | METAR already covers airport; broader coverage unavailable via API |

**Verdict**: **Not viable** without a structured API. The Bahrain Meteorological
Directorate publishes rich weather and marine forecast data on its website, including
wind, sea state, dust/sand warnings, and temperature — all highly relevant for a Gulf
island nation. However, the data is HTML-only and not accessible via REST API,
JSON/XML feeds, or any documented machine-readable format. Scraping is not an acceptable
pattern for this repo.

**Recommendation**: Monitor for future API announcements from MTT or IGA. In the
meantime, use the Aviation Weather API for Bahrain International Airport (OBBI)
METAR/TAF as the structured weather data source for Bahrain. If Bahrain publishes
SYNOP observations to WMO/GTS, investigate international aggregators (NOAA ISD,
ECMWF open data) as alternative access paths.
