# South Korea AirKorea

**Country/Region**: South Korea
**Publisher**: Korea Environment Corporation (K-eco) / Ministry of Environment (MOE)
**API Endpoint**: `https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/` (Korean Open Data Portal)
**Documentation**: https://airkorea.or.kr/eng (English portal), https://www.data.go.kr/ (API portal, Korean)
**Protocol**: REST
**Auth**: API Key (free registration at data.go.kr)
**Data Format**: JSON, XML
**Update Frequency**: Hourly
**License**: Korean Open Government License (Type 1 — free use with attribution)

## What It Provides

AirKorea is South Korea's national air quality information system, providing real-time CAI (Comprehensive Air Quality Index) and pollutant-level data from a dense network of monitoring stations across all metropolitan and provincial areas. It measures PM2.5, PM10, O₃, NO₂, CO, and SO₂. The Korean Open Data Portal (data.go.kr) provides the programmatic API.

## API Details

- **Base URL**: `https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/`
- **Key Endpoints** (via Korean Open Data Portal):
  - `getMsrstnAcctoRltmMesureDnsty` — real-time measurements by station
  - `getCtprvnRltmMesureDnsty` — real-time measurements by province
  - `getMinuDustFrcstDspth` — PM forecast
  - `getMsrstnList` — station list
  - `getUnityAirEnvrnIdexSnstiveAboveMsrstnList` — stations above threshold
- **Query Parameters**: `serviceKey` (API key), `returnType` (json/xml), `numOfRows`, `pageNo`, `stationName`, `sidoName`, `dataTerm`
- **Rate Limits**: Standard Korean open data limits (typically 1,000 calls/day for free tier)
- **English portal**: https://airkorea.or.kr/eng provides visual access but no API

## Freshness Assessment

Data is updated hourly. The English website states "the most current data is provided at the end of each hour" and notes data is "prior to approval for use" (preliminary). The data.go.kr API reflects the same hourly cadence.

## Entity Model

- **Sido** (province/metropolitan city) → has many **Stations**
- **Station** → name, address, coordinates
- **Measurement** → station × time → PM10, PM2.5, O₃, NO₂, CO, SO₂ values
- **CAI** (Comprehensive Air Quality Index) → composite index with grade
- **Forecast** → regional PM forecast

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly updates |
| Openness | 2 | Free API key via data.go.kr; Korean open data license |
| Stability | 2 | Government-backed; API on national open data platform |
| Structure | 2 | JSON/XML, but endpoint names are in romanized Korean |
| Identifiers | 2 | Station names (Korean); sido-based queries |
| Additive Value | 2 | South Korea-specific; partially in OpenAQ/AQICN |
| **Total** | **13/18** | |

## Notes

- The API is accessed through Korea's national open data portal (data.go.kr), which requires free registration and an API key (serviceKey).
- Endpoint names and parameters are in romanized Korean (e.g., `getMsrstnAcctoRltmMesureDnsty`), which can be challenging for non-Korean developers.
- The English website (airkorea.or.kr/eng) is read-only and does not expose the API.
- Data is also available through OpenAQ and AQICN, which may be preferable for non-Korean integrations.
- South Korea has very dense urban monitoring — useful for fine-grained spatial analysis.
