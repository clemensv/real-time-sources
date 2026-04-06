# Canada — ECCC Water Survey of Canada

**Country/Region**: Canada (nationwide)
**Publisher**: Environment and Climate Change Canada (ECCC) — Water Survey of Canada
**API Endpoint**: `https://api.weather.gc.ca/collections/hydrometric-realtime/items?f=json`
**Alternative Endpoint**: `https://wateroffice.ec.gc.ca/services/real_time_data/csv/inline`
**Documentation**: https://wateroffice.ec.gc.ca/services/index_e.html and https://eccc-msc.github.io/open-data/msc-geomet/readme_en/
**Protocol**: REST (OGC API Features + CSV service)
**Auth**: None
**Data Format**: GeoJSON, CSV
**Update Frequency**: Every 5 minutes
**License**: Open Government Licence — Canada

## What It Provides

Real-time water level and discharge data from over 2100 hydrometric monitoring stations across all Canadian provinces and territories. Parameters include water level (unit values, parameter 46), discharge (unit values, parameter 47), and daily means. The network covers major rivers, lakes, and tributaries from coast to coast.

## API Details

Two complementary access methods:

### OGC API Features (recommended)

- **Station list**: `GET https://api.weather.gc.ca/collections/hydrometric-stations/items?f=json&limit=100`
- **Real-time data**: `GET https://api.weather.gc.ca/collections/hydrometric-realtime/items?f=json&STATION_NUMBER=05BJ004&limit=100`
- Supports filtering by `STATION_NUMBER`, `PROV_TERR_STATE_LOC`, `DATETIME`, bounding box
- Returns GeoJSON FeatureCollection with geometry and properties

Sample response feature:
```json
{
  "type": "Feature",
  "geometry": {"type": "Point", "coordinates": [-114.56986, 50.94851]},
  "properties": {
    "IDENTIFIER": "05BJ004.2026-03-07T07:00:00Z",
    "STATION_NUMBER": "05BJ004",
    "STATION_NAME": "ELBOW RIVER AT BRAGG CREEK",
    "PROV_TERR_STATE_LOC": "AB",
    "DATETIME": "2026-03-07T07:00:00Z",
    "LEVEL": 0.669,
    "DISCHARGE": null
  }
}
```

### CSV Service

- **Real-time**: `GET https://wateroffice.ec.gc.ca/services/real_time_data/csv/inline?stations[]=05BJ004&parameters[]=46&start_date=2026-04-01%2000:00:00&end_date=2026-04-06%2000:00:00`
- **Recent (latest 5 min)**: `GET https://wateroffice.ec.gc.ca/services/recent_real_time_data/csv/inline?stations[]=05BJ004&parameters[]=46`
- Returns CSV with columns: ID, Date, Parameter, Value, Qualifier, Symbol, Approval, Grade

No documented rate limits, but large requests may need to be split.

## Freshness Assessment

Probed 2026-04-06: Real-time data returns 5-minute intervals. OGC API shows data from 2026-03-07 onward (30-day rolling window). CSV service confirmed returning data up to current date. Data is labeled "Provisional/Provisoire" — typical for real-time hydrometric data.

## Entity Model

- **Station ID**: `STATION_NUMBER` — alphanumeric code like `05BJ004`, following the WSC numbering scheme (2-digit major drainage area + letter + digits)
- **Observation ID**: `{STATION_NUMBER}.{ISO_DATETIME}` — composite key
- **Kafka key**: `stations/{STATION_NUMBER}`
- **CloudEvents subject**: `stations/{STATION_NUMBER}`

Station identifiers are extremely stable — some have been active since the 1800s.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 5-minute updates, 30-day rolling window |
| Openness | 3 | No auth, Open Government Licence |
| Stability | 3 | Federal government, OGC standard API |
| Structure | 3 | GeoJSON, CSV, well-documented schema |
| Identifiers | 3 | Stable WSC station numbers |
| Additive Value | 3 | Only real-time hydro source for all of Canada |
| **Total** | **18/18** | |

## Notes

- The OGC API Features endpoint is the modern, preferred access method — standards-compliant and returns GeoJSON
- The CSV service at wateroffice.ec.gc.ca is simpler but less structured
- Both APIs are free, unauthenticated, and well-documented
- The network covers approximately 2100 active real-time stations
- Historical data (HYDAT database) available via separate collections
- This is one of the best-documented and most accessible national hydrometric APIs globally
