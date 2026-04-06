# National Highways England (WebTRIS)

**Country/Region**: United Kingdom — England
**Publisher**: National Highways (formerly Highways England)
**API Endpoint**: `https://webtris.highwaysengland.co.uk/api/v1/`
**Documentation**: https://webtris.highwaysengland.co.uk/api/swagger/ui/index
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: 15-minute intervals (sensor data); daily aggregations available
**License**: Open Government Licence v3.0

## What It Provides

National Highways operates the WebTRIS (Web-based Traffic Information System) API providing traffic count and speed data from sensors across England's strategic road network (motorways and major A-roads). Covers approximately 8,000 monitoring sites across 25 areas. Data includes vehicle volumes by size class, average speeds, and time-period breakdowns.

## API Details

**Areas (regions):**
```
GET https://webtris.highwaysengland.co.uk/api/v1/areas
```
Returns 25 operational areas covering England's strategic road network:
```json
{
  "areas": [
    {"Id": "1", "Name": "A1 Darrington to Dishforth DBFO"},
    {"Id": "9", "Name": "Area 1"},
    {"Id": "22", "Name": "M25 DBFO"}
  ]
}
```

**Sites (sensors):**
```
GET https://webtris.highwaysengland.co.uk/api/v1/sites
GET https://webtris.highwaysengland.co.uk/api/v1/sites?area={areaId}
```

**Daily reports:**
```
GET https://webtris.highwaysengland.co.uk/api/v1/reports/daily?sites=5688&start_date=01012024&end_date=02012024
```
Returns:
```json
{
  "Rows": [{
    "Site Name": "M602/6051A",
    "Report Date": "2024-01-01",
    "Time Period Ending": "00:14:00",
    "0 - 520 cm": "134",
    "521 - 660 cm": "1",
    "661 - 1160 cm": "0",
    "1160+ cm": "0",
    "Avg mph": "57",
    "Total Volume": "135"
  }]
}
```

Vehicle size classes: 0–520cm, 521–660cm, 661–1160cm, 1160+cm
Speed bands: 0–10mph through 80+mph in 5mph increments

**Report types available:**
- `daily` — daily breakdown by time period
- `monthly` — monthly aggregates
- `annual` — annual summaries

## Freshness Assessment

WebTRIS provides data in 15-minute time periods. The API is primarily designed for historical analysis rather than real-time streaming — you query by date range. Near-real-time data is available with a short delay (minutes to hours). For truly real-time incident data in England, the NTIS (National Traffic Information Service) DATEX II feeds are more appropriate, but those require registration.

## Entity Model

- **Area**: Operational region (DBFO concession or National Highways area)
- **Site**: Individual sensor/monitoring point on a specific carriageway
- **Traffic Count**: Vehicle volume by size class per 15-minute period
- **Speed**: Average speed and speed band distribution per 15-minute period
- **Quality**: Data quality indicators (missing periods, sensor faults)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 15-minute periods with short delay; not true real-time streaming |
| Openness | 3 | No auth, OGL v3.0 |
| Stability | 3 | Government-operated, Swagger-documented API |
| Structure | 3 | Clean JSON with consistent schema; Swagger docs |
| Identifiers | 3 | Site IDs, area IDs, structured naming |
| Additive Value | 2 | England strategic roads; NTIS DATEX II provides richer real-time data |
| **Total** | **16/18** | |

## Notes

- WebTRIS is best for traffic volume analytics rather than real-time event streaming. The query-by-date model is suited to periodic polling for historical/analytical use cases.
- For real-time traffic events (incidents, roadworks, queue warnings), National Highways also provides NTIS DATEX II feeds. These require registration and provide genuine real-time situation data.
- Vehicle classification by length (cm) rather than type is unusual but practical for automated sensor data.
- The strategic road network covers motorways (M1, M25, M6, etc.) and major A-roads — not local/urban roads.
- Speed data in mph (miles per hour) — UK-specific unit. Conversion needed for metric standardization.
- 25 operational areas align with road maintenance contracts (DBFO = Design, Build, Finance, Operate).
