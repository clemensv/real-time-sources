# Thailand TMD — Thai Meteorological Department

**Country/Region**: Thailand
**Publisher**: Thai Meteorological Department (TMD / กรมอุตุนิยมวิทยา)
**API Endpoint**: `https://data.tmd.go.th/` (TMD open data portal)
**Documentation**: https://data.tmd.go.th/nwpapi/doc/apidoc/forecast/daily/at_forecast.html
**Protocol**: REST (JSON) — API Key required
**Auth**: API Key (free registration at data.tmd.go.th)
**Data Format**: JSON
**Update Frequency**: Observations every 3 hours; forecasts updated daily
**License**: Thai government open data

## What It Provides

TMD operates Thailand's national weather observation network — covering a tropical country of 70 million people that faces monsoon rainfall, tropical storms, and severe flooding (2011 floods caused $46 billion in damage).

The TMD Open Data API provides:
- **Current observations**: Temperature, humidity, wind, rainfall from ~100 synoptic stations
- **Forecasts**: Daily and 7-day forecasts for Thai provinces
- **Marine weather**: Gulf of Thailand and Andaman Sea conditions
- **Upper air**: Radiosonde observations
- **Radar**: Weather radar imagery

### API Structure

TMD has documented APIs at `data.tmd.go.th`:
- **Forecast API**: Daily and weekly forecasts by province
- **Observation API**: Current weather from automatic stations
- **Warning API**: Severe weather warnings

```
# Daily forecast
GET https://data.tmd.go.th/nwpapi/v1/forecast/location/daily/at?lat=13.75&lon=100.50&fields=tc,rh,rain

# Current observations
GET https://data.tmd.go.th/api/WeatherObservationData/...
```

### Connection Note

The API was not directly probed during this research session (requires API key registration). However, TMD's API documentation is publicly available and well-structured in English, which is unusual for Southeast Asian meteorological services.

### Relationship to Thaiwater

The existing `thailand-thaiwater.md` candidate covers Thailand's water monitoring (Thaiwater/HAII). TMD covers the atmospheric/weather side — different agency, different data type.

## Entity Model

- **Station**: TMD station IDs and WMO numbers (~100 synoptic + automatic stations)
- **Province**: 77 provinces with individual forecasts
- **Marine Zone**: Gulf of Thailand, Andaman Sea sub-zones
- **Warning Area**: Regional groupings for severe weather warnings

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 3-hourly observations; daily forecasts; API key needed to verify |
| Openness | 2 | Free API key; documented API; English documentation |
| Stability | 2 | Government meteorological service; structured API platform |
| Structure | 2 | JSON REST API; documented endpoints; but unverified response format |
| Identifiers | 2 | Station IDs; province codes; WMO numbers |
| Additive Value | 3 | Fills SE Asian weather gap; tropical monsoon climate; 70M population |
| **Total** | **13/18** | |

## Integration Notes

- Register at `data.tmd.go.th` for API key
- Complements existing Thailand Thaiwater coverage (hydrology) with atmospheric data
- Thai language in some fields; but API documentation is in English
- CloudEvents: weather observation events per station; forecast events per province
- Thailand's 2011 floods ($46B damage) underscore the importance of real-time weather data here

## Verdict

Promising documented API requiring registration. TMD is unusual among Southeast Asian met services in having a documented REST API with English documentation. The free API key registration is a minor barrier. Worth pursuing after registration — would fill a significant gap in SE Asian weather coverage alongside the existing Thaiwater hydrology candidate.
