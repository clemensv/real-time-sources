# KMA API Hub — South Korea

**Country/Region**: South Korea
**Publisher**: KMA (Korea Meteorological Administration / 기상청)
**API Endpoint**: `https://apihub.kma.go.kr/`
**Documentation**: https://apihub.kma.go.kr (Korean), https://data.kma.go.kr/cmmn/main.do (data portal)
**Protocol**: REST API
**Auth**: API Key (free registration required — Korean phone number may be needed)
**Data Format**: JSON, XML
**Update Frequency**: Real-time (observations), hourly (forecasts), per model run (NWP)
**License**: Korean Open Government Data License

## What It Provides

KMA operates one of the most comprehensive meteorological API platforms in Asia, covering 13 major data categories:

- **Surface Observations** (지상관측): Real-time ASOS station data from Korea's surface observation network. Temperature, humidity, wind, precipitation, pressure, visibility.

- **Marine Observations** (해양관측): Buoy and coastal station data from Korean waters.

- **Upper Air Observations** (고층관측): Radiosonde/upper-air data.

- **Radar** (레이더): Site-level and composite radar imagery/data for the Korean Peninsula.

- **Satellite** (위성): Chollian-2A (GEO-KOMPSAT-2A) satellite data — Korea's own geostationary weather satellite.

- **Earthquake/Volcano** (지진/화산): Seismic monitoring data for the Korean Peninsula and surrounding region.

- **Typhoon** (태풍): Western Pacific typhoon tracking and forecasts.

- **Numerical Weather Prediction** (수치모델): Output from KMA's NWP models including short/medium-range and ultra-short-range predictions.

- **Forecasts and Warnings** (예특보): Official forecasts at the neighborhood level ("동네예보") and severe weather warnings.

- **Convergent Weather** (융합기상): Combined/fused weather products.

- **Aviation Weather** (항공기상): METAR, TAF, SIGMET for Korean airspace.

- **World Weather** (세계기상): GTS (Global Telecommunication System) data.

- **Industry-Specific** (산업특화): Tailored weather data for specific sectors.

## API Details

The API Hub provides categorized endpoints. Registration on `apihub.kma.go.kr` provides an API key. Each category has its own set of endpoints accessible through the hub:
```
GET https://apihub.kma.go.kr/api/{category}/{endpoint}?serviceKey={API_KEY}&...
```

The older data portal at `data.kma.go.kr` provides a web interface for browsing and downloading data, while the API Hub is the programmatic access point.

Documentation and the portal interface are entirely in Korean. Some endpoints return JSON, others return XML.

## Freshness Assessment

- Surface observations: Real-time from ASOS network.
- Forecasts: Updated hourly (neighborhood-level).
- Radar: Near-real-time composite and site data.
- Satellite: Real-time from Chollian-2A.
- NWP models: Updated per run schedule.

## Entity Model

- **Station**: ASOS station identifiers.
- **Grid Point**: Neighborhood forecast grid coordinates.
- **Region**: Administrative division codes (Korean system).
- **Observation**: Multi-parameter readings per station with timestamps.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time observations, hourly forecasts, near-real-time radar/satellite |
| Openness | 1 | API key required; registration portal is Korean-only; may require Korean phone |
| Stability | 3 | National met agency, government infrastructure, long operational history |
| Structure | 2 | Mix of JSON and XML; Korean-language documentation; 13 categories to navigate |
| Identifiers | 2 | Station IDs, grid coordinates — Korean administrative codes |
| Additive Value | 3 | Korean Peninsula coverage, own satellite (Chollian-2A), typhoon tracking |
| **Total** | **14/18** | |

## Notes

- The scope of KMA's API Hub is impressive — 13 categories covering surface, marine, upper-air, radar, satellite, NWP, aviation, and more.
- The language barrier is significant. The entire API Hub, documentation, and registration process are in Korean.
- Registration may require a Korean phone number for verification, which would be a blocker for international developers.
- KMA's Chollian-2A satellite provides geostationary imagery over East Asia — unique data not available from Western met services.
- The "neighborhood forecast" (동네예보) system provides hyper-local forecasts at grid-point level, similar to how NWS provides point forecasts.
- Data from GTS (World Weather) category could provide global synoptic data — worth exploring if registration is achievable.
- Consider using the data portal's bulk download features as an alternative to the API if registration proves difficult.
