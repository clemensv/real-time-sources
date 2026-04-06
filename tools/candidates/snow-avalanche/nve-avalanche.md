# NVE Avalanche Warnings (Varsom)
**Country/Region**: Norway
**Publisher**: Norwegian Water Resources and Energy Directorate (NVE) / varsom.no
**API Endpoint**: `https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/api/AvalancheWarningByRegion/Simple/{regionId}/{languageId}/{startDate}/{endDate}`
**Documentation**: https://api01.nve.no/hydrology/forecast/avalanche/v6.3.0/swagger/index.html
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Daily (during winter season)
**License**: Norwegian Licence for Open Government Data (NLOD)

## What It Provides
NVE provides official avalanche warnings for Norway through the Varsom platform:
- Avalanche danger levels (1-5 European scale) by region
- Avalanche problems (wind slab, persistent slab, wet snow, storm slab, etc.)
- Danger descriptions and travel advice
- Mountain weather forecasts
- Snow conditions and observations
- Ice conditions (for ice climbing, etc.)

## API Details
- **Warning by region**: `GET /api/AvalancheWarningByRegion/Simple/{regionId}/{languageId}/{startDate}/{endDate}`
- **All regions**: `GET /api/AvalancheWarningByRegion/Simple/0/{languageId}/{startDate}/{endDate}` (regionId=0 for all)
- **Languages**: 1 = Norwegian, 2 = English
- **Date format**: `yyyy-MM-dd`
- **Detailed warnings**: `GET /api/AvalancheWarningByRegion/Detail/{regionId}/{languageId}/{startDate}/{endDate}`
- **Region list**: `GET /api/Region/{regionId}/{languageId}`
- **Swagger docs**: Full API documentation available at the swagger endpoint

Note: API returned HTTP 500 at probe time, but this is documented as a known REST API with Swagger documentation. It may be seasonal or experiencing temporary issues.

## Freshness Assessment
Good (seasonal). During winter season (typically December through May), warnings are published daily. The API provides forecasts for current and upcoming days. Outside season, the API may not return data.

## Entity Model
- **AvalancheWarning** (RegionId, RegionName, DangerLevel, ValidFrom, ValidTo, PublishTime, Author)
- **AvalancheProblem** (AvalancheProblemId, AvalancheType, DestructiveSize, Probability, Trigger, Distribution, ExposedHeight, ValidExpositions)
- **Region** (RegionId, RegionName, RegionType, geometry)
- **DangerLevel** (1=Low, 2=Moderate, 3=Considerable, 4=High, 5=Very High)

## Feasibility Rating
| Criterion | Score (0-3) | Notes |
|-----------|-------------|-------|
| Freshness | 2 | Daily during winter season |
| Openness | 3 | NLOD license, no auth |
| Stability | 2 | Government API, but seasonal availability |
| Structure | 3 | Clean JSON with Swagger docs |
| Identifiers | 3 | Stable region IDs, problem type IDs |
| Additive Value | 3 | Norway's official avalanche service |
| **Total** | **16/18** | |

## Notes
- This repo already has `nve-hydro/` for NVE hydrological data — same agency
- Varsom.no is the public-facing platform
- The API follows European Avalanche Warning Services (EAWS) standards
- Swagger documentation provides full schema details
- May need to handle seasonal unavailability gracefully
