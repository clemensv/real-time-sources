# California Data Exchange Center (CDEC)

**Country/Region**: United States — California
**Publisher**: California Department of Water Resources (DWR)
**API Endpoint**: `https://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet`
**Documentation**: https://cdec.water.ca.gov/dynamicapp/wsSensorData
**Protocol**: REST (JSON and CSV endpoints)
**Auth**: None
**Data Format**: JSON, CSV
**Update Frequency**: Real-time (hourly for reservoir storage, 15-minute for some sensors)
**License**: California public data (open/unrestricted)

## What It Provides

CDEC is California's central repository for real-time hydrologic data, collecting telemetry from over 2,600 stations statewide. For reservoir/dam monitoring, CDEC tracks:

- **Reservoir storage** (acre-feet) for all major California reservoirs
- **Reservoir elevation** (feet above sea level)
- **Inflow and outflow** (cfs)
- **Precipitation, snow water content**
- **River stages and flows**

Major reservoirs covered: Shasta (SHA), Oroville (ORO), Folsom (FOL), New Melones (NML), Don Pedro (DNP), Hetch Hetchy (HTC), Lake Sonoma (SON), Millerton (MIL), Pine Flat (PNF), and dozens more.

## API Details

**JSON endpoint**: `https://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet`

Parameters:
- `Stations` — station ID(s), comma-separated (e.g., `SHA`, `ORO,FOL,SHA`)
- `SensorNums` — sensor number (e.g., `15` = STORAGE, `6` = ELEVATION, `76` = INFLOW)
- `dur_code` — duration code: `H` (hourly), `D` (daily), `M` (monthly), `E` (event)
- `Start` — start date (YYYY-MM-DD)
- `End` — end date (YYYY-MM-DD)

**Example** (verified working):
```
https://cdec.water.ca.gov/dynamicapp/req/JSONDataServlet?Stations=SHA&SensorNums=15&dur_code=H&Start=2026-04-01&End=2026-04-05
```

Returns:
```json
[
  {"stationId":"SHA","durCode":"H","SENSOR_NUM":15,"sensorType":"STORAGE",
   "date":"2026-4-1 0:00","obsDate":"2026-4-1 0:00","value":4090763,
   "dataFlag":" ","units":"AF"},
  ...
]
```

**CSV endpoint**: Available via the web form or by appending format parameters.

**Station list**: `https://cdec.water.ca.gov/dynamicapp/staSearch`
**Sensor list**: `https://cdec.water.ca.gov/dynamicapp/req/SensorNums`

Common sensor numbers:
- 6 = ELEVATION (ft)
- 15 = STORAGE (AF — acre-feet)
- 76 = INFLOW (cfs)
- 23 = OUTFLOW (cfs)
- 1 = STAGE (ft)

## Freshness Assessment

Excellent. Data was verified live — Shasta Dam storage updated hourly with data through the current date. All times in Pacific Standard Time. Some sensors report at 15-minute intervals.

## Entity Model

- **Station**: station ID (3-4 letter code, e.g., `SHA`), name, county, river basin, lat/lon, elevation, operator
- **Sensor**: sensor number, sensor type name, duration code, units
- **Observation**: station ID, timestamp, value, units, data flag, duration code

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time hourly updates, verified working |
| Openness | 3 | No auth, no rate limits documented, public data |
| Stability | 3 | California state agency, critical water management infrastructure |
| Structure | 3 | Clean JSON API with documented parameters, predictable responses |
| Identifiers | 3 | Well-known station codes (SHA, ORO, FOL), standardized sensor numbers |
| Additive Value | 3 | Definitive source for California reservoir data — not replicated elsewhere |
| **Total** | **18/18** | |

## Notes

- This is a top-tier candidate. The API is clean, documented, returns real-time JSON data, and requires no authentication.
- California reservoirs are among the most closely-monitored in the world due to the state's water scarcity challenges and massive water infrastructure.
- Multi-station queries are supported (comma-separated station IDs), enabling efficient bulk data retrieval.
- The auto-complete feature on the web form helps discover station IDs and common sensors.
- Times are always PST (not PDT) — this is explicitly documented.
- Pairs naturally with USBR HydroData for comprehensive western US reservoir coverage.
