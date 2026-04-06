# South Korea K-water / Water Information Portal

**Country/Region**: South Korea
**Publisher**: K-water (한국수자원공사), Ministry of Environment
**API Endpoint**: `https://www.water.or.kr/` (portal), WAMIS (wamis.go.kr) — connectivity issues
**Documentation**: https://www.water.or.kr/
**Protocol**: Web portal with Ajax endpoints
**Auth**: Session-based (portal login for full access)
**Data Format**: HTML / JSON (Ajax)
**Update Frequency**: Real-time (10-minute to hourly)
**Station Count**: 1500+ stations nationwide
**License**: Korean government open data (공공데이터)

## What It Provides

South Korea has one of Asia's most extensive water monitoring networks:

### water.or.kr (K-water portal)
- Real-time dam and reservoir status
- Water supply monitoring
- Water quality data
- Flood/drought early warning

### WAMIS (Water Resources Management Information System)
- Comprehensive water resources data
- River water level and discharge
- Groundwater monitoring
- National water balance

### OpenAPI (openapi.kwater.or.kr)
- Mentioned in Korean government open data catalogs
- DNS failure during testing — may be intermittently available

## API Details

### Web portal
The K-water portal at `water.or.kr` uses jQuery-based Ajax calls:
```
POST https://www.water.or.kr/kor/main/ajaxProc.do
```
With parameters like `mode=getWaterInfo`, `mode=getMainInfo`. These endpoints returned data in prior agent testing but 404 during direct probing.

### WAMIS
```
GET https://www.wamis.go.kr/wkw/wkw_bsidx_lst.do
```
TLS timeout during testing — service may be available within Korean networks only.

### Korean Open Data Portal
Korean government open data (data.go.kr) likely has hydrology APIs with API key registration:
- OpenAPI keys available for Korean residents/organizations
- Documentation primarily in Korean

## Freshness Assessment

- K-water operates real-time monitoring across South Korea
- Portal shows current data when accessible
- Network accessibility from outside Korea may be limited
- WAMIS is a well-known system in the Asian hydrology community

## Entity Model

- **Dam**: name, capacity, current storage, inflow, outflow
- **Station**: name, river, location, monitoring parameters
- **Water quality**: pH, DO, BOD, SS, etc.
- **Observation**: timestamp, water level, discharge

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 1 | Ajax endpoints exist but inconsistent accessibility |
| Data Richness | 3 | Comprehensive: water level, discharge, quality, dams, groundwater |
| Freshness | 2 | Real-time data exists; API access unreliable from outside Korea |
| Station Coverage | 3 | 1500+ stations covering entire Korean peninsula |
| Documentation | 1 | Korean-language documentation; limited English |
| License/Access | 1 | Korean API key registration system; limited international access |
| **Total** | **11/18** | |

## Notes

- South Korea has excellent water monitoring infrastructure but limited international API access
- Korean-language barriers affect both documentation and data interpretation
- API key registration on data.go.kr may require Korean credentials
- Network accessibility issues suggest geographic restrictions or firewall policies
- K-water is a major government-owned corporation with significant technical resources
- WAMIS has been operational since the 1990s and is well-established
- Worth revisiting with a Korean network perspective
- Consider partnering with Korean developers for API investigation
