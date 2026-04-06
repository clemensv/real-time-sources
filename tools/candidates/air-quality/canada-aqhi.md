This documents the Canadian Air Quality Health Index (AQHI) data. Verified:

- The main portal at weather.gc.ca shows AQHI values for major Canadian cities with both observed and forecast values
- Cities include Calgary, Edmonton, Halifax, Montreal, Ottawa, Toronto, Vancouver, Winnipeg, etc.
- AQHI values are 1-10+ with risk categories (Low Risk, Moderate Risk, High Risk, Very High Risk)
- Data is provided by Environment and Climate Change Canada (ECCC) / Meteorological Service of Canada (MSC)
- MSC Datamart distributes open data via HTTPS and AMQP
- MSC GeoMet provides OGC WMS/WCS services

```
# Canadian AQHI (Air Quality Health Index)

**Country/Region**: Canada
**Publisher**: Environment and Climate Change Canada (ECCC) / Meteorological Service of Canada
**API Endpoint**: `https://dd.weather.gc.ca/` (MSC Datamart) and `https://geo.weather.gc.ca/geomet` (GeoMet WMS/WCS)
**Documentation**: https://eccc-msc.github.io/open-data/msc-data/aqhi/readme_aqhi_en/
**Protocol**: HTTP file distribution (Datamart); OGC WMS/WCS (GeoMet)
**Auth**: None
**Data Format**: CSV (Datamart), XML (ATOM feeds), GeoJSON/PNG (GeoMet)
**Update Frequency**: Hourly (observations), twice-daily (forecasts)
**License**: Open Government Licence - Canada

## What It Provides

The Air Quality Health Index (AQHI) is Canada's national air quality communication metric, jointly operated by ECCC and Health Canada. Unlike AQI, AQHI is explicitly health-risk based, calculated from the combined effects of O₃, NO₂, and PM2.5. The AQHI is reported for ~160 communities across all provinces and territories. Both observed (current) and forecast (today + tonight + tomorrow) values are provided. Data is distributed via the MSC Datamart (bulk file access) and GeoMet (OGC web services).

## API Details

- **MSC Datamart** (file distribution):
  - Base: `https://dd.weather.gc.ca/air_quality/aqhi/`
  - Structure: `/{province}/observation/realtime/csv/` and `/{province}/forecast/model/`
  - Files: CSV with AQHI values per station/community
- **GeoMet** (OGC services):
  - Base: `https://geo.weather.gc.ca/geomet`
  - Layers: AQHI observations and forecasts as WMS (map tiles) or WCS (data)
  - Format: GeoJSON, PNG, GeoTIFF
- **ATOM Feeds**: RSS/ATOM feeds per province for current AQHI and forecasts
- **AQHI Scale**: 1-3 (Low Risk), 4-6 (Moderate Risk), 7-10 (High Risk), 10+ (Very High Risk)
- **Variables**: AQHI composite index; individual pollutant concentrations not provided via AQHI endpoints

## Freshness Assessment

AQHI observations are updated hourly. Forecasts are issued twice daily (morning and afternoon). The MSC Datamart updates files in near-real-time. GeoMet WMS layers refresh automatically. No API key is needed for either access method.

## Entity Model

- **Community** → name, province, geographic location
- **AQHI Observation** → community × datetime → AQHI value (1-10+) + risk category
- **AQHI Forecast** → community × period (Today/Tonight/Tomorrow) → AQHI value + risk category
- **Province** → groups communities; used as URL path segment

## Feasibility Rating

| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 3 | Hourly observations, twice-daily forecasts |
| Openness | 3 | No auth, Open Government Licence - Canada |
| Stability | 3 | Environment Canada / Meteorological Service — long-standing |
| Structure | 2 | File-based distribution (CSV/XML); no simple REST JSON API |
| Identifiers | 2 | Community names; province-based file hierarchy |
| Additive Value | 2 | Canada-wide AQHI + forecasts; health-risk based index |
| **Total** | **15/18** | |

## Notes

- Canada does not provide a simple REST/JSON API for AQHI — data is distributed as files on the MSC Datamart and via OGC WMS/WCS. This requires file polling or WMS GetFeatureInfo queries.
- The AQHI is calculated differently from AQI: it uses a multi-pollutant health risk model, not the maximum-of-sub-indices approach. This makes it a unique health indicator.
- AQHI forecasts are a distinctive feature — few countries provide air quality forecasts via open data.
- The MSC Datamart also uses AMQP (Advanced Message Queuing Protocol) for push-based data delivery — a rare feature that enables event-driven architectures.
- GeoMet WMS layers can be integrated into web maps directly (Leaflet, OpenLayers) without processing the raw data.
- Individual pollutant concentrations (PM2.5, O₃, NO₂) are available through the National Air Pollution Surveillance (NAPS) program, but NAPS data is not real-time.
```
