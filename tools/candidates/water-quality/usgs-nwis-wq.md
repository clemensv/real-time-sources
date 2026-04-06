# USGS NWIS Water Quality (Instantaneous Values)

**Country/Region**: United States
**Publisher**: US Geological Survey (USGS), Department of the Interior
**API Endpoint**: `https://waterservices.usgs.gov/nwis/iv/`
**Documentation**: https://waterservices.usgs.gov/docs/instantaneous-values/
**Protocol**: REST
**Auth**: None
**Data Format**: JSON (WaterML 2.0), XML, RDB (tab-delimited)
**Update Frequency**: Real-time (5–15 minute intervals)
**License**: US Government public domain

## What It Provides

The USGS NWIS Instantaneous Values service provides real-time continuous water quality monitoring data from thousands of sites equipped with multi-parameter sondes and continuous monitors. While the USGS IV service is already covered in the repository (usgs-iv/) for streamflow/stage, the water quality parameters are a distinct and valuable data domain.

Continuous water quality parameters available:
- **00010** — Water temperature (°C)
- **00300** — Dissolved oxygen (mg/L)
- **00400** — pH
- **00095** — Specific conductance (µS/cm)
- **63680** — Turbidity (FNU)
- **00065** — Gage height (not WQ per se, but related)
- **32316** — fChl (chlorophyll fluorescence)
- **99133** — Nitrate + nitrite (mg/L as N) — from continuous nitrate sensors
- **00045** — Precipitation
- **72279** — Tidal elevation

Approximately 3,000+ sites report at least one continuous water quality parameter.

## API Details

Same API as USGS IV (already in repo) but with water quality parameter codes:

**Example** (verified working — Potomac River, DO + temperature):
```
https://waterservices.usgs.gov/nwis/iv/?format=json&sites=01646500&parameterCd=00300,00010&period=PT2H
```

Returns real-time 5-minute dissolved oxygen (8.8 mg/L) and water temperature (17.0°C) data.

**Key query parameters**:
- `parameterCd` — comma-separated parameter codes (00300, 00010, 00400, 00095, 63680, 99133)
- `sites` — USGS site numbers
- `stateCd` — filter by state
- `siteType` — `ST` (stream), `LK` (lake), `ES` (estuary)
- `period` — ISO 8601 duration (e.g., `PT2H`, `P7D`)
- `startDT` / `endDT` — date range

**Discovery endpoint** — find sites with specific WQ parameters:
```
https://waterservices.usgs.gov/nwis/iv/?format=json&stateCd=MD&parameterCd=00300&siteStatus=active
```

## Freshness Assessment

Excellent. Verified live data at 5-minute intervals. The same rock-solid USGS infrastructure that serves streamflow data. Data is provisional but operationally reliable.

## Entity Model

- **Site**: USGS site number (8-15 digits), name, agency code, lat/lon, HUC code, site type
- **Variable**: parameter code, name, description, units, statistical code
- **Method**: method ID, description (e.g., "From multiparameter sonde")
- **Observation**: timestamp (ISO 8601 with timezone), value, qualifier (P=provisional), method ID

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Real-time 5-minute data, verified working |
| Openness | 3 | US Government public domain, no auth |
| Stability | 3 | USGS — gold standard for hydrologic data services |
| Structure | 3 | Clean REST API, JSON/XML/RDB output, well-documented |
| Identifiers | 3 | USGS site numbers are globally unique and well-known |
| Additive Value | 3 | Extends existing usgs-iv/ integration to water quality domain |
| **Total** | **18/18** | |

## Notes

- This is a natural extension of the existing usgs-iv/ integration. The same API, same site identifiers, same data format — just different parameter codes.
- The continuous nitrate sensor data (parameter 99133) is particularly valuable — these are expensive sensors deployed at key monitoring sites, providing real-time nutrient loading data.
- Dissolved oxygen (00300) and temperature (00010) are the most widely deployed continuous WQ parameters.
- Turbidity (63680) is increasingly deployed for sediment transport monitoring and as a surrogate for other parameters.
- The USGS also provides discrete (grab sample) water quality data through the NWIS-Web QW service (`https://nwis.waterdata.usgs.gov/nwis/qwdata`) — these are lab-analyzed samples, not continuous monitoring, and use a different API.
- The WaterML 2.0 JSON format includes rich metadata about methods, qualifiers, and site properties.
