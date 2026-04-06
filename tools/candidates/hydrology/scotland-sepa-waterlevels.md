# Scotland — SEPA Water Level and Flow

**Country/Region**: Scotland, UK
**Publisher**: Scottish Environment Protection Agency (SEPA)
**API Endpoint**: `https://timeseries.sepa.org.uk/KiWIS/KiWIS`
**Documentation**: https://www2.sepa.org.uk/waterlevels/ (public portal)
**Protocol**: REST (Kisters WISKI Web Service)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Every 15 minutes
**License**: Open data (SEPA disclaimer; effectively open for reuse)

## What It Provides

Real-time river water level (stage), precipitation, groundwater level, and various derived statistics from hundreds of monitoring stations across Scotland. The network covers major Scottish rivers and tributaries, with stations providing 15-minute interval data. Parameters include stage (S), precipitation (Precip), water temperature (WT), discharge (Q), groundwater level (GWLVL), and many others.

## API Details

Uses the same Kisters WISKI protocol as BOM Australia, making it a familiar integration target.

### Station List
```
GET https://timeseries.sepa.org.uk/KiWIS/KiWIS
  ?service=kisters
  &type=queryServices
  &request=getStationList
  &datasource=0
  &format=json
  &returnfields=station_name,station_no,station_id
  &rows=100
```

Returns JSON array: `[["station_name","station_no","station_id"],["Abbey St Bathans","15018","36870"],...]`

### Time Series List (per station)
```
GET https://timeseries.sepa.org.uk/KiWIS/KiWIS
  ?service=kisters
  &type=queryServices
  &request=getTimeseriesList
  &datasource=0
  &format=json
  &station_no=15018
  &returnfields=station_name,station_no,ts_id,ts_name,parametertype_name
```

### Time Series Values
```
GET https://timeseries.sepa.org.uk/KiWIS/KiWIS
  ?service=kisters
  &type=queryServices
  &request=getTimeseriesValues
  &datasource=0
  &format=json
  &ts_id=56178010
  &from=2026-04-05
  &to=2026-04-06
  &returnfields=Timestamp,Value,Quality%20Code
```

Sample response:
```json
[{
  "ts_id": "56178010",
  "rows": "138",
  "columns": "Timestamp,Value,Quality Code",
  "data": [
    ["2026-04-05T00:00:00.000Z", 0.334, 254],
    ["2026-04-05T00:15:00.000Z", 0.333, 254],
    ["2026-04-05T00:30:00.000Z", 0.335, 254]
  ]
}]
```

### Available Parameter Types
Key parameters: S (Stage/Water Level), Q (Discharge), Precip (Precipitation), WT (Water Temperature), GWLVL (Groundwater Level), Evap (Evaporation), EC (Electrical Conductivity)

### Time Series Name Patterns
- `15minute` — raw 15-minute readings
- `Day.Mean`, `Day.Max`, `Day.Min` — daily aggregates
- `Month.Mean`, `Month.Max`, `Month.Min` — monthly aggregates
- `HydrologicalYear.Mean/Max/Min` — hydrological year stats

## Freshness Assessment

Probed 2026-04-06: Station 15018 (Abbey St Bathans) returned 15-minute data through 2026-04-05T23:00:00Z. Data for 2026-04-06 was in progress. Effectively real-time with ~1 day window of provisional data.

## Entity Model

- **Station Number**: `station_no` — numeric string, e.g., `15018`
- **Station ID**: `station_id` — internal numeric, e.g., `36870`
- **Time Series ID**: `ts_id` — numeric, e.g., `56178010`
- **Kafka key**: `stations/{station_no}`
- **CloudEvents subject**: `stations/{station_no}`

Station numbers are SEPA gauging station references — stable and well-documented.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15-minute intervals, near-real-time |
| Openness | 3 | No auth, open access, SEPA open data |
| Stability | 3 | Government agency, Kisters WISKI is enterprise software |
| Structure | 2 | JSON but Kisters array-of-arrays format |
| Identifiers | 3 | Stable SEPA station numbers |
| Additive Value | 2 | UK already partially covered by EA flood monitoring; Scotland adds distinct coverage |
| **Total** | **16/18** | |

## Notes

- Uses the exact same Kisters WISKI API protocol as BOM Australia — code can be shared
- SEPA covers Scotland specifically, while the existing EA Flood Monitoring source covers England
- Large station network with hundreds of sites
- Multiple parameter types available beyond just water level
- The API supports the full Kisters query vocabulary (getStationList, getTimeseriesList, getTimeseriesValues, getParameterTypeList, etc.)
- Data is provisional and subject to revision
- Scotland has unique hydrological characteristics (highland rivers, lochs) not well-represented in the EA England network
