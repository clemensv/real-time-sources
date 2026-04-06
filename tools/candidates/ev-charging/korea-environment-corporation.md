# Korea Environment Corporation — EV Charging Open Data

**Country/Region**: South Korea
**Publisher**: Korea Environment Corporation (한국환경공단) / Ministry of Environment
**API Endpoint**: `https://www.data.go.kr/` (Korean Open Data Portal — dataset ID 15076352)
**Documentation**: https://www.data.go.kr/data/15076352/openapi.do (Korean language)
**Protocol**: REST (Korean Open Data Portal API)
**Auth**: API Key (free registration on data.go.kr)
**Data Format**: JSON / XML
**Real-Time Status**: Yes — includes real-time charger status (available/charging/fault)
**Update Frequency**: Near real-time (status updates as chargers report)
**Station Count**: 200,000+ public charging points across South Korea (estimate)
**License**: Korean Open Data License (free use including commercial)

## What It Provides

South Korea has one of the world's densest EV charging networks, driven by aggressive government subsidies and the domestic EV industry (Hyundai, Kia, Samsung SDI). The Korea Environment Corporation maintains the national EV charging station database under the Ministry of Environment, which is published as an open API on South Korea's national data portal (data.go.kr).

The dataset includes:
- Station locations with GPS coordinates and addresses
- Charger specifications (connector types, power levels)
- Real-time charger status (available, charging, communication error, under maintenance)
- Operator/business information
- Supported connector types (DC Combo/CCS, CHAdeMO, AC slow, Type 2)
- Operating hours and access conditions

## API Details

The API is hosted on Korea's Open Data Portal (data.go.kr), dataset ID 15076352. Access requires free registration and API key issuance.

**Endpoint pattern:**
```
GET https://apis.data.go.kr/B552584/EvCharger/getChargerInfo?serviceKey={key}&pageNo=1&numOfRows=10&period=5&zcode=11
```

Key parameters:
- `serviceKey` — API key from data.go.kr registration
- `zcode` — area code (11 = Seoul, etc.)
- `period` — update period filter
- `pageNo`, `numOfRows` — pagination

Response fields typically include:
- `statNm` — station name
- `addr` — address
- `lat`, `lng` — GPS coordinates
- `chgerType` — charger type code (01=DC-fast-combo, 02=DC-fast-CHAdeMO, 03=AC-slow, 04=DC-combo+AC, etc.)
- `output` — power output (kW)
- `stat` — current status (1=communication error, 2=available, 3=charging, 4=operation suspended, 5=under maintenance, 9=not confirmed)
- `statUpdDt` — status update datetime
- `busiNm` — business/operator name
- `busiCall` — operator phone number

## Freshness Assessment

The Korean API provides genuine real-time charger status — the `stat` field shows whether each charger is currently available, charging, or faulted, with `statUpdDt` timestamps showing when the status was last updated. South Korea's centralized charging management system (operated by Korea Environment Corporation) receives real-time telemetry from connected chargers.

This is one of the few government-operated charging datasets worldwide that provides true real-time connector-level status — comparable to NOBIL Norway and NDL Netherlands.

## Entity Model

- **Station (충전소)**: Physical charging location with address and coordinates
- **Charger (충전기)**: Individual charging unit with type, power, and real-time status
- **Operator (사업자)**: Business entity operating the chargers
- **Status codes**: 1 (comm error), 2 (available), 3 (charging), 4 (suspended), 5 (maintenance), 9 (unconfirmed)
- **Charger types**: DC combo (CCS2), CHAdeMO, AC slow (Type 1), combined types

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time charger status with timestamps |
| Openness | 2 | Free API key; Korean language docs; registration on data.go.kr |
| Stability | 3 | Government-operated national platform |
| Structure | 2 | JSON/XML; proprietary schema (not OCPI); Korean field names |
| Identifiers | 2 | Station/charger IDs; Korean-specific scheme |
| Additive Value | 3 | Asia's most comprehensive open EV charging data; 200K+ points |
| **Total** | **15/18** | |

## Notes

- South Korea is a hidden gem for EV charging open data — real-time status, massive coverage, free API. The main barriers are Korean-language documentation and non-standard data format.
- Korea's 200K+ public charging points make it one of the world's densest networks — driven by Hyundai/Kia's home market and strong government incentives.
- Major operators include KEPCO (Korea Electric Power Corporation), Korea Environment Corporation, Chargepoint Korea, SK Energy, GS Caltex, and HD Hyundai Energy Solutions.
- The data.go.kr platform hosts many other Korean government open datasets — a useful pattern for discovering Asian government data sources.
- For international integration, field name translation and status code mapping would be needed — but the underlying data quality is high.
- Korea's EV charging connector landscape includes CCS2 (DC combo), CHAdeMO, and AC Type 2/Type 1 — similar to global standards but with Korea-specific connector combinations.
