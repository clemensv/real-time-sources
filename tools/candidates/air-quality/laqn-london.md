This documents the London Air Quality Network (LAQN) API operated by King's College London. Verified API data:

- Base URL: `http://api.erg.ic.ac.uk/AirQuality/`
- Confirmed working endpoints:
  - `GET /Information/MonitoringSites/GroupName=All/Json` → returns all sites: `{"Sites":{"Site":[{"@LocalAuthorityCode":"27","@LocalAuthorityName":"Richmond","@SiteCode":"TD0","@SiteName":"- National Physical Laboratory, Teddington","@SiteType":"Suburban","@DateOpened":"1996-08-08","@Latitude":"51.424","@Longitude":"-0.345","@DataOwner":"Richmond","@DataManager":"King's College London"}, ...]}}`
  - `GET /Daily/MonitoringIndex/Latest/GroupName=London/Json` → returns daily AQI per site with species breakdown: `{"DailyAirQualityIndex":{"@MonitoringIndexDate":"2026-04-05","LocalAuthority":[{..., "Site":[{"@SiteCode":"BX1","@SiteName":"Bexley - Slade Green","Species":[{"@SpeciesCode":"NO2","@AirQualityIndex":"1","@AirQualityBand":"Low"}, ...]}]}]}}`
- Auth: None required
- Data Format: JSON (and XML)
- Response uses @ prefix for attribute-style fields

```
# London Air Quality Network (LAQN)

**Country/Region**: United Kingdom (London and surrounding boroughs)
**Publisher**: King's College London / Environmental Research Group (ERG)
**API Endpoint**: `http://api.erg.ic.ac.uk/AirQuality/`
**Documentation**: http://www.londonair.org.uk/LondonAir/API/
**Protocol**: REST
**Auth**: None
**Data Format**: JSON and XML
**Update Frequency**: Hourly
**License**: Open Government Licence v2.0 (OGL)

## What It Provides

The London Air Quality Network (LAQN) is one of the most comprehensive urban air quality monitoring systems in the world. Managed by King's College London's Environmental Research Group, it covers ~200+ monitoring sites across London boroughs and some surrounding counties. The API provides real-time and historical data for NO₂, PM10, PM2.5, O₃, SO₂, and other species. It also calculates the Daily Air Quality Index (DAQI) per site with band classifications (Low/Moderate/High/Very High).

## API Details

- **Base URL**: `http://api.erg.ic.ac.uk/AirQuality/`
- **Key Endpoints**:
  - `GET /Information/MonitoringSites/GroupName={group}/Json` — list monitoring sites (All, London, etc.)
  - `GET /Daily/MonitoringIndex/Latest/GroupName={group}/Json` — latest daily AQI per site with species
  - `GET /Data/Site/SiteCode={code}/StartDate={date}/EndDate={date}/Json` — measurement data for a site
  - `GET /Data/SiteSpecies/SiteCode={code}/SpeciesCode={species}/StartDate={date}/EndDate={date}/Json` — specific pollutant data
  - `GET /Information/Species/Json` — list of measured species
  - `GET /Hourly/MonitoringIndex/SiteCode={code}/Json` — hourly index for a specific site
- **Response Format**: JSON with `@`-prefixed attribute fields (XML-derived structure)
- **Site Metadata**: LocalAuthorityCode/Name, SiteCode, SiteName, SiteType (Suburban/Kerbside/Roadside/Urban Background), DateOpened/Closed, Lat/Lon, DataOwner, DataManager
- **AQI Bands**: Low (1-3), Moderate (4-6), High (7-9), Very High (10)
- **Species**: NO₂, PM10, PM2.5, O₃, SO₂, CO and others

## Freshness Assessment

Data is updated hourly. The Daily Air Quality Index is recalculated with a `TimeToLive` field (typically 45 minutes). The API is responsive and has been operational for many years. Historical data is available going back to the 1990s for some sites.

## Entity Model

- **LocalAuthority** → code, name, centre lat/lon
- **Site** → SiteCode (e.g., `BX1`), name, type, date opened/closed, lat/lon, data owner, data manager
- **Species** → code (NO2, PM10, PM25, O3, SO2, CO), description
- **DailyIndex** → site × date → species-level AQI value + band + source (Measurement/Forecast)
- **Measurement** → site × species × datetime → value

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly data, daily AQI with TTL |
| Openness | 3 | No auth, OGL licence |
| Stability | 3 | Long-running (20+ years), King's College London backed |
| Structure | 2 | JSON but XML-derived `@`-prefix fields; nested structure |
| Identifiers | 3 | Stable SiteCode identifiers, SpeciesCode standards |
| Additive Value | 3 | Unique urban-scale detail for London; DAQI not in Defra AURN API |
| **Total** | **17/18** | |

## Notes

- The API is HTTP (not HTTPS) — `http://api.erg.ic.ac.uk/AirQuality/`. HTTPS may not be supported.
- JSON responses use `@`-prefixed field names (e.g., `@SiteCode`, `@Latitude`) because the API was originally XML-only. This requires special handling in some JSON parsers.
- Complements Defra AURN: while AURN covers the national network, LAQN provides London borough-level detail with ~4× the station density.
- Includes DAQI (Daily Air Quality Index) with per-species breakdown and band classification — this is the UK's official public-facing air quality communication metric.
- Historical data back to 1993 for some sites — excellent for long-term trend analysis.
- The `GroupName` parameter filters by network (London, All, Sussex, Kent, etc.) — the network extends beyond London.
```
