# Hong Kong EPD Air Quality Health Index (AQHI)

**Country/Region**: Hong Kong SAR, China
**Publisher**: Environmental Protection Department (EPD)
**API Endpoint**: `https://www.aqhi.gov.hk/epd/ddata/html/out/24aqhi_Eng.xml`
**Documentation**: https://www.aqhi.gov.hk/en/what-is-aqhi/about-aqhi.html
**Protocol**: HTTP/XML feed
**Auth**: None
**Data Format**: XML
**Update Frequency**: Hourly
**License**: Hong Kong government open data (terms apply)

## What It Provides

Hong Kong's Environmental Protection Department publishes the Air Quality Health Index (AQHI), a health-risk based index that replaced the older Air Pollution Index (API) in 2013. The XML feed provides 24-hour rolling AQHI values for 16 monitoring stations across Hong Kong, categorized as General Stations and Roadside Stations. The AQHI scale runs from 1-10+ with health risk categories (Low/Moderate/High/Very High/Serious).

## API Details

- **Endpoint**: `https://www.aqhi.gov.hk/epd/ddata/html/out/24aqhi_Eng.xml`
- **Response Structure**:
  - Root: `<AQHI24HrReport>`
  - Metadata: `<title>`, `<link>`, `<description>`, `<lastBuildDate>`
  - Items: `<item>` with `<type>` (General/Roadside), `<StationName>`, `<DateTime>`, `<aqhi>` (integer 1-10+)
- **Station Names**: Central/Western, Eastern, Kwai Chung, Kwun Tong, Sham Shui Po, Sha Tin, Tai Po, Tap Mun, Tseung Kwan O, Tsuen Wan, Tuen Mun, Tung Chung, Yuen Long, Mong Kok, Causeway Bay, Central
- **Station Types**: General Stations (~13), Roadside Stations (~3)
- **AQHI Scale**: 1-3 (Low), 4-6 (Moderate), 7 (High), 8-10 (Very High), 10+ (Serious)

## Freshness Assessment

Data updates hourly. The XML feed provides a rolling 24-hour window of AQHI values per station with `<lastBuildDate>` timestamp. Feed is responsive and consistently available. No authentication needed.

## Entity Model

- **Station** → name (text), type (General/Roadside)
- **AQHI Reading** → station × datetime → aqhi value (integer 1-10+)
- **Report** → title, link, description, lastBuildDate, collection of items

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly AQHI values, rolling 24h window |
| Openness | 3 | No auth, publicly accessible XML feed |
| Stability | 2 | Government-operated; XML feed URL may change without notice |
| Structure | 2 | Simple XML but not a proper REST API; no station metadata endpoint |
| Identifiers | 1 | Station names only (no stable IDs); no coordinates in feed |
| Additive Value | 2 | Hong Kong-specific; AQHI is a health-based index not widely available |
| **Total** | **13/18** | |

## Notes

- The AQHI is calculated from cumulative health risks of NO₂, SO₂, O₃, and PM2.5 — it differs from AQI used in most other countries.
- XML feed format is RSS-like but custom — not standard RSS/Atom. Simple to parse but requires custom handling.
- No coordinates are provided in the feed itself. Station locations must be hardcoded or obtained from the AQHI website.
- Hong Kong also publishes individual pollutant concentrations on the EPD website, but these are not available through a structured data feed.
- Roadside stations (Mong Kok, Causeway Bay, Central) typically show higher readings due to traffic emissions.
- The Chinese-language version is at `24aqhi_ChT.xml` (Traditional Chinese).
