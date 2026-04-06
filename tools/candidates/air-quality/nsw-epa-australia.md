# NSW EPA Air Quality (Australia)

**Country/Region**: Australia (New South Wales)
**Publisher**: NSW Department of Climate Change, Energy, the Environment and Water
**API Endpoint**: `https://data.airquality.nsw.gov.au/` (API portal)
**Documentation**: https://airquality.nsw.gov.au/air-quality-data-services
**Protocol**: REST
**Auth**: Unknown (likely API key via registration)
**Data Format**: JSON (likely)
**Update Frequency**: Hourly
**License**: Creative Commons Attribution 4.0 (NSW Government open data)

## What It Provides

NSW EPA operates one of Australia's most comprehensive air quality monitoring networks, continuously measuring O₃, NO₂, SO₂, CO, PM10, PM2.5, and meteorological parameters (temperature, wind speed/direction, humidity, solar radiation) across the state. The network covers the Greater Sydney region, Hunter Valley, Illawarra, and regional NSW. An API portal exists at `data.airquality.nsw.gov.au`.

## API Details

- **API Portal**: `https://data.airquality.nsw.gov.au/docs` — appears to be a Swagger/OpenAPI documentation portal
- **Data Services**: Three access facilities mentioned:
  1. API (programmatic access)
  2. Data download tool
  3. Live data on the website
- **Website**: `airquality.nsw.gov.au` — real-time AQC (Air Quality Categories) updated hourly
- **Contact**: nswairAPI@environment.nsw.gov.au for accessibility or API issues
- **Other Australian States**: Victoria (EPA Victoria), Queensland, WA, SA have their own portals

## Freshness Assessment

Hourly observations with daily forecasts for Greater Sydney Metropolitan Region (issued at 4pm daily). Data is quality-assured before publication. The API portal suggests structured programmatic access is available.

## Entity Model

- **Region** → Greater Sydney, Hunter Valley, Illawarra, etc.
- **Station** → name, location, parameters measured
- **Measurement** → pollutant/met parameter, concentration/value, timestamp
- **AQC** (Air Quality Category) → Good/Fair/Poor/Very Poor/Hazardous

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly, with forecasts |
| Openness | 2 | CC BY 4.0; API may require registration |
| Stability | 2 | State government; API portal exists but not fully explored |
| Structure | 2 | API docs exist (Swagger-like); not fully probed |
| Identifiers | 2 | Station-based queries likely |
| Additive Value | 2 | Australia-specific; unique for southern hemisphere |
| **Total** | **13/18** | |

## Notes

- NSW is the most API-mature Australian state for air quality data. Other states (Victoria, Queensland) may have APIs but are less documented.
- The API portal at `data.airquality.nsw.gov.au/docs` could not be fully explored (JavaScript-rendered page) but its existence suggests a proper REST API.
- Australian air quality data fills a southern hemisphere gap — bushfire smoke monitoring is a key use case.
- For multi-state Australian coverage, OpenAQ aggregates data from several Australian state EPAs.
- Worth exploring further by registering for API access via the email contact.
