# Australia — BOM Water Data Online

**Country/Region**: Australia (nationwide)
**Publisher**: Bureau of Meteorology (BOM)
**API Endpoint**: `http://www.bom.gov.au/waterdata/services`
**Documentation**: https://data.gov.au/data/dataset/water-data-online
**Protocol**: REST (Kisters WISKI Web Service)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Hourly (some stations sub-hourly)
**License**: Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU)

## What It Provides

Water level and discharge time series from approximately 3500 monitoring stations across all Australian states and territories. Parameters include Water Course Level, Water Course Discharge, and Rainfall. Data is supplied by state and territory water agencies and aggregated nationally by the Bureau of Meteorology.

## API Details

The API uses the Kisters WISKI web service protocol with query-string parameters.

### Station List
```
GET http://www.bom.gov.au/waterdata/services
  ?service=kisters
  &type=queryServices
  &request=getStationList
  &datasource=0
  &format=json
  &returnfields=station_name,station_no,station_id
  &parametertype_name=Water%20Course%20Level
```

Returns a JSON array-of-arrays: `[["station_name","station_no","station_id"],["15 MILE @ GRETA STH","403213","2865255"],...]`

### Time Series List (per station)
```
GET http://www.bom.gov.au/waterdata/services
  ?service=kisters
  &type=queryServices
  &request=getTimeseriesList
  &datasource=0
  &format=json
  &station_no=410730
  &returnfields=station_name,station_no,ts_id,ts_name,parametertype_name
```

### Time Series Values
```
GET http://www.bom.gov.au/waterdata/services
  ?service=kisters
  &type=queryServices
  &request=getTimeseriesValues
  &datasource=0
  &format=json
  &ts_id=1597010
  &from=2026-04-01
  &to=2026-04-06
  &returnfields=Timestamp,Value,Quality%20Code
```

Sample response:
```json
[{
  "ts_id": "1597010",
  "rows": "115",
  "columns": "Timestamp,Value,Quality Code",
  "data": [
    ["2026-04-01T00:00:00.000+10:00", 0.544, 140],
    ["2026-04-01T01:00:00.000+10:00", 0.544, 140]
  ]
}]
```

No documented rate limits, but the service is clearly designed for programmatic access.

## Freshness Assessment

Probed 2026-04-06: Data for station 410730 (Cotter R. at Gingera) returned hourly values through 2026-04-05 — approximately 1 day old. Some time series have sub-hourly data (e.g., 15-minute "AsStored" series). Quality code 140 indicates provisional data.

## Entity Model

- **Station ID**: `station_no` — alphanumeric code like `410730` (AWRC station numbering)
- **Time Series ID**: `ts_id` — numeric, e.g., `1597010`
- **Time Series Name**: `ts_name` — descriptive, e.g., `DMQaQc.Merged.HourlyMean.HR`
- **Kafka key**: `stations/{station_no}`
- **CloudEvents subject**: `stations/{station_no}`

Station numbers follow the Australian Water Resources Council (AWRC) numbering scheme — highly stable.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly updates typical, some sub-hourly; ~1 day lag observed |
| Openness | 3 | No auth, CC BY 3.0 AU license |
| Stability | 3 | Federal Bureau of Meteorology, long-running service |
| Structure | 2 | JSON but Kisters WISKI format is array-based, not self-describing |
| Identifiers | 3 | Stable AWRC station numbers |
| Additive Value | 3 | Only real-time hydro source for Australia |
| **Total** | **16/18** | |

## Notes

- The Kisters WISKI web service protocol is widely used by water agencies globally — the same protocol powers systems in many countries
- The array-of-arrays JSON format (not key-value) requires a custom parser
- Multiple time series types per station (provisional, validated, daily, hourly) — need to select the right `ts_name` pattern
- Recommended ts_name patterns for real-time: `DMQaQc.Merged.HourlyMean.HR` (discharge/level hourly) or `Received.Provisionalbest.AsStored.1` (sub-hourly)
- Over 3500 stations with Water Course Level data alone
- Data pipeline: state agencies → BOM aggregation → public API
