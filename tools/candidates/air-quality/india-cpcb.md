# India CPCB (Central Pollution Control Board)

**Country/Region**: India
**Publisher**: Central Pollution Control Board (CPCB), Ministry of Environment, Forest and Climate Change
**API Endpoint**: `https://app.cpcbccr.com/ccr/` (web application; limited public API)
**Documentation**: https://app.cpcbccr.com/ccr/ (CAAQMS dashboard)
**Protocol**: Web application / undocumented internal API
**Auth**: None for website; API access unclear
**Data Format**: HTML / JSON (internal)
**Update Frequency**: Hourly to 15-minute intervals
**License**: Indian government open data (implied, but no explicit API license)

## What It Provides

CPCB operates India's Continuous Ambient Air Quality Monitoring System (CAAQMS) with 400+ stations across major Indian cities. It measures PM2.5, PM10, SO₂, NO₂, CO, O₃, NH₃, benzene, toluene, xylene, and other pollutants. The CPCB portal also aggregates data from state PCBs (DPCC Delhi, HSPCB Haryana, UPPCB Uttar Pradesh, RPCB Rajasthan, etc.) and publishes the National Air Quality Index (NAQI).

## API Details

- **No documented public REST API**: The CAAQMS dashboard at `app.cpcbccr.com` is a web application
- **Internal APIs**: The dashboard makes XHR calls to internal endpoints for station data, but these are undocumented
- **SAFAR**: India's System of Air Quality and Weather Forecasting (SAFAR) at `safar.tropmet.res.in` provides forecast data for select cities (Delhi, Mumbai, Pune, Ahmedabad)
- **data.gov.in**: India's open data portal has some historical AQI datasets but not real-time API access
- **OpenAQ**: Indian CPCB data is partially available through OpenAQ (via AirNow partner feed)

## Freshness Assessment

CAAQMS stations report at 15-minute to hourly intervals. The dashboard shows near-real-time data. However, without a public API, access is limited to web scraping. Some state-level dashboards have slightly different update schedules.

## Entity Model

- **State** → **State PCB** → has many **Stations**
- **Station** → name, city, coordinates, operating agency
- **Measurement** → pollutant, concentration, timestamp, AQI sub-index
- **NAQI** → National Air Quality Index (composite, 0-500 scale)
- **Pollutants**: PM2.5, PM10, SO₂, NO₂, CO, O₃, NH₃, C₆H₆, toluene, xylene

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Real-time data exists on dashboard, but no API |
| Openness | 1 | No documented API; web scraping or reverse engineering needed |
| Stability | 1 | Dashboard has changed multiple times; no API contract |
| Structure | 0 | No structured API |
| Identifiers | 1 | Station names on dashboard; no stable API identifiers |
| Additive Value | 2 | Authoritative for India; unique pollutants (NH₃, benzene, toluene) |
| **Total** | **7/18** | |

## Notes

- India's CPCB data is critically important (India has some of the world's worst air quality) but programmatic access is poor.
- Best accessed via OpenAQ, which ingests CPCB data through the AirNow partner feed, or via AQICN.
- SAFAR (safar.tropmet.res.in) provides forecasts and AQI for 4 major cities but also lacks a documented API.
- The CAAQMS dashboard is a React/Next.js app that could potentially be reverse-engineered, but this is fragile.
- India measures unique pollutants not commonly available elsewhere: ammonia (NH₃), benzene, toluene, xylene.
- Consider low priority for direct integration; use OpenAQ or AQICN as intermediaries.
