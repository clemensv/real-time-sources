# Japan MOE SORAMAME (Atmospheric Environmental Regional Observation System)

**Country/Region**: Japan
**Publisher**: Ministry of the Environment, Japan (MOE)
**API Endpoint**: `https://soramame.env.go.jp/` (web application; no public REST API)
**Documentation**: https://soramame.env.go.jp/ (Japanese only)
**Protocol**: Web scraping / undocumented internal API
**Auth**: None (public website)
**Data Format**: HTML / JavaScript-rendered (Vue.js SPA)
**Update Frequency**: Hourly (24-hour continuous monitoring)
**License**: Japanese government open data (implied, but no explicit license)

## What It Provides

SORAMAME (そらまめくん) is Japan's nationwide atmospheric monitoring system, operated by the Ministry of the Environment. It provides 24-hour continuous monitoring of SO₂, NO, NO₂, CO, Ox (photochemical oxidants), NMHC (non-methane hydrocarbons), CH₄, SPM (suspended particulate matter), PM2.5, and wind/temperature data from ~1,900 monitoring stations across all 47 prefectures.

## API Details

- **No public REST API**: SORAMAME is a Vue.js single-page application that loads data dynamically
- **Internal endpoints**: The SPA likely calls internal API endpoints (e.g., under `/soramame/`) but these are undocumented and not intended for public programmatic access
- **Web scraping**: Would require rendering JavaScript (headless browser) or reverse-engineering XHR calls
- **Data download**: Historical CSV data may be available through Japan's open data portal (data.go.jp)
- **Alternative**: SORAMAME data is partially available through AQICN/WAQI and OpenAQ

## Freshness Assessment

Data is updated hourly and displayed in near-real-time on the website. The site title says "24時間情報提供" (24-hour information provision). However, without a public API, programmatic freshness depends on scraping frequency.

## Entity Model

- **Prefecture** (47 prefectures) → has **Stations**
- **Station** → location, measurement capabilities
- **Measurement** → pollutant, concentration, timestamp (hourly)
- **Pollutants**: SO₂, NO, NO₂, CO, Ox, NMHC, CH₄, SPM, PM2.5

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Hourly data exists, but no API to access it |
| Openness | 1 | Public website, but no documented API; scraping required |
| Stability | 1 | SPA could change without notice; no API contract |
| Structure | 0 | No structured API; JavaScript-rendered HTML |
| Identifiers | 1 | Station identifiers exist on the site but are not exposed via API |
| Additive Value | 2 | Japan's authoritative source; unique for Japan-specific pollutants |
| **Total** | **7/18** | |

## Notes

- SORAMAME is the authoritative source for Japanese air quality, but the lack of a public API makes direct integration impractical.
- The website is Japanese-only (no English interface).
- Better to access Japanese air quality data through OpenAQ or AQICN, which aggregate SORAMAME data.
- Japan's data.go.jp portal may provide downloadable datasets but not real-time API access.
- The unique pollutants (Ox, NMHC, CH₄) measured by SORAMAME are not commonly available elsewhere.
- Consider this a low-priority candidate unless web scraping of the SPA is acceptable.
