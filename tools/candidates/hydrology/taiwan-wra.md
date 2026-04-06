# Taiwan Water Resources Agency (WRA)

**Country/Region**: Taiwan
**Publisher**: Water Resources Agency (WRA), Ministry of Economic Affairs
**API Endpoint**: `https://fhy.wra.gov.tw/WraApi/v1/Water/Station` (water level stations), `https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Daily` (reservoir data)
**Documentation**: https://fhy.wra.gov.tw/ (Flood Hydrology portal)
**Protocol**: REST (OData-style query parameters)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Daily (reservoir), Station metadata is reference data
**Station Count**: 100+ water level stations, 50+ reservoirs, 500+ rain stations
**License**: Taiwan government open data

## What It Provides

Hydrological data across Taiwan's river basins:
- **Water level stations** with warning thresholds (3 levels) and flood plan levels
- **Reservoir daily data** — storage capacity, inflow, outflow, rainfall accumulation
- **Rain stations** — station metadata across all basins
- **Reservoir station metadata** — capacity, water heights, importance classification

## API Details

### Water level stations
```
GET https://fhy.wra.gov.tw/WraApi/v1/Water/Station?$top=10&$format=JSON
```
Returns array of stations with:
- `StationNo`, `StationName` (Chinese)
- `Latitude`, `Longitude`
- `BasinNo`, `BasinName` (Chinese)
- `WarningLevel1`, `WarningLevel2`, `WarningLevel3` — three warning thresholds
- `TopLevel` — historical maximum level
- `PlanFloodLevel` — design flood level

### Reservoir daily data
```
GET https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Daily?$top=10&$format=JSON
```
Returns daily reservoir status:
- `StationNo`, `Time` (ISO 8601)
- `EffectiveCapacity`, `DeadWaterHeight`, `FullWaterHeight`
- `AccumulatedRainfall`, `InflowTotal`, `OutflowTotal`

### Reservoir stations
```
GET https://fhy.wra.gov.tw/WraApi/v1/Reservoir/Station?$top=10&$format=JSON
```
Returns reservoir metadata:
- `StationNo`, `StationName` (Chinese)
- `EffectiveCapacity`, `Storage`
- `FullWaterHeight`, `DeadWaterHeight`
- `ProtectionFlood`, `HydraulicConstruction`, `Importance` (flags)
- `BasinNo`, `BasinName`

### Rain stations
```
GET https://fhy.wra.gov.tw/WraApi/v1/Rain/Station?$top=10&$format=JSON
```
Returns rain gauge station list with addresses, coordinates, and basin associations.

### OData query support
All endpoints support OData-style parameters:
- `$top=N` — limit results
- `$skip=N` — pagination
- `$format=JSON` — output format
- `$filter=...` — filtering

### Example response (Reservoir Daily)
```json
[{
  "StationNo": "50201",
  "Time": "2026-04-05T07:00:00",
  "EffectiveCapacity": 148.08,
  "DeadWaterHeight": 10.9,
  "FullWaterHeight": 18.35,
  "AccumulatedRainfall": 13.5,
  "InflowTotal": 0.0,
  "OutflowTotal": 0.147
}]
```

## Freshness Assessment

- Reservoir daily data confirmed fresh (2026-04-05 readings available on 2026-04-06)
- Station metadata appears to be reference data (updated less frequently)
- Real-time water level observations may require additional endpoint discovery
- The main portal at fhy.wra.gov.tw provides real-time dashboards, suggesting more API endpoints exist

## Entity Model

- **Water Level Station**: StationNo, StationName, Latitude, Longitude, BasinNo, BasinName, CityCode, WarningLevel1-3, TopLevel, PlanFloodLevel
- **Reservoir Station**: StationNo, StationName, EffectiveCapacity, Storage, FullWaterHeight, DeadWaterHeight, ProtectionFlood, Importance
- **Reservoir Daily**: StationNo, Time, EffectiveCapacity, DeadWaterHeight, FullWaterHeight, AccumulatedRainfall, InflowTotal, OutflowTotal
- **Rain Station**: StationNo, StationName, Address, CityCode, Latitude, Longitude, BasinNo, BasinName

## Feasibility Rating

| Dimension | Score | Notes |
|-----------|-------|-------|
| API Quality | 3 | Clean REST with OData query support, JSON, no auth |
| Data Richness | 2 | Stations, reservoirs, rain gauges; real-time water level timeseries endpoint not confirmed |
| Freshness | 2 | Daily reservoir data confirmed; real-time water levels unclear |
| Station Coverage | 3 | Comprehensive coverage of Taiwan's basins: 100+ water stations, 50+ reservoirs |
| Documentation | 1 | No public API documentation; endpoints discovered via probing |
| License/Access | 3 | Open, no auth required, Taiwan government open data |
| **Total** | **14/18** | |

## Notes

- Station and basin names are in Chinese (Traditional) — may need translation layer
- OData-style parameters suggest a well-designed API framework
- Three-tier warning level system (WarningLevel1 > WarningLevel2 > WarningLevel3) provides flood risk context
- Real-time water level observation endpoints likely exist but were not discovered via probing — the portal shows live gauge readings
- Taiwan's typhoon season makes this data particularly valuable for flood monitoring
- `CityCode` field links to Taiwan administrative divisions for geographic grouping
- `ProtectionFlood` and `Importance` flags on reservoirs enable prioritization
