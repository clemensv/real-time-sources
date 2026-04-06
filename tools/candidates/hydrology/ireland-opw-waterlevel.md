# Ireland — OPW waterlevel.ie

**Country/Region**: Ireland
**Publisher**: Office of Public Works (OPW)
**API Endpoint**: `https://waterlevel.ie/geojson/latest/`
**Documentation**: https://waterlevel.ie/
**Protocol**: REST
**Auth**: None
**Data Format**: GeoJSON, CSV
**Update Frequency**: Every 15 minutes
**License**: Creative Commons Attribution 4.0 International (CC BY 4.0)

## What It Provides

Real-time water level, water temperature, and rainfall data from hydrometric gauging stations across Ireland. The network covers rivers, lakes, and canals operated by the OPW and partner agencies. Data includes current water level readings (sensor_ref 0001), water temperature (0002), voltage (0003), and OD (Ordnance Datum) levels.

## API Details

### Latest Readings (all stations)
```
GET https://waterlevel.ie/geojson/latest/
```

Returns a GeoJSON FeatureCollection with the most recent reading from every station:
```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "id": 1458,
    "properties": {
      "station_ref": "0000001041",
      "station_name": "Sandy Mills",
      "sensor_ref": "0001",
      "region_id": 3,
      "datetime": "2026-04-06T10:15:00Z",
      "value": "0.502",
      "err_code": 99,
      "url": "/0000001041/0001/",
      "csv_file": "/data/month/01041_0001.csv"
    },
    "geometry": {
      "type": "Point",
      "coordinates": [-7.575758, 54.838318]
    }
  }]
}
```

### Historical Data (per station, rolling month)
```
GET https://waterlevel.ie/data/month/{station_short}_{sensor_ref}.csv
```

Example: `https://waterlevel.ie/data/month/15001_0001.csv`

Returns CSV with 15-minute intervals:
```csv
datetime,value
2026-03-02 10:00,1.268
2026-03-02 10:15,1.264
...
```

### Station Page
Each station has a web page at `https://waterlevel.ie/{station_ref}/{sensor_ref}/`

No documented rate limits. The site uses caching — data updates each time new telemetry arrives.

## Freshness Assessment

Probed 2026-04-06 ~12:30 UTC: The `/geojson/latest/` endpoint returned data timestamped `2026-04-06T10:15:00Z` — approximately 2 hours old, which is well within the 15-minute update cycle. Monthly CSV showed continuous 15-minute data.

## Entity Model

- **Station Reference**: `station_ref` — zero-padded 10-digit code, e.g., `0000001041`
- **Sensor Reference**: `sensor_ref` — `0001` (level), `0002` (temperature), `0003` (voltage), `OD` (Ordnance Datum)
- **Short Station ID**: First 5 significant digits, e.g., `01041` (used in CSV filenames)
- **Kafka key**: `stations/{station_ref}`
- **CloudEvents subject**: `stations/{station_ref}/sensors/{sensor_ref}`

Station references are stable OPW hydrometric station numbers.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15-minute intervals, data current within minutes |
| Openness | 3 | No auth, CC BY 4.0, explicit open data policy |
| Stability | 3 | Government agency (OPW), well-established service |
| Structure | 3 | Clean GeoJSON + CSV, simple and consistent |
| Identifiers | 3 | Stable OPW station references |
| Additive Value | 3 | Ireland not covered by any existing source |
| **Total** | **18/18** | |

## Notes

- One of the cleanest and simplest hydrometric APIs found — the GeoJSON endpoint returns everything in one call
- The `/geojson/latest/` endpoint is ideal for polling — returns all stations' latest readings at once
- Data is explicitly provisional and unchecked — standard for real-time telemetry
- CSV files provide a rolling month of 15-minute data per station/sensor combination
- The OPW disclaimer notes that some stations may cease recording
- Water level values appear to be in metres (stage height)
- Separate sensors per station for level, temperature, voltage, and OD height
