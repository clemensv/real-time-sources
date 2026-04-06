# SMARD — Strommarktdaten (Bundesnetzagentur, Germany)

**Country/Region**: Germany (also DE-LU bidding zone)
**Publisher**: Bundesnetzagentur (German Federal Network Agency)
**API Endpoint**: `https://smard.de/app/chart_data/{filter_id}/{region}/{index_or_data}.json`
**Documentation**: https://smard.de (no formal API docs — internal JSON API backing the web portal)
**Protocol**: REST (static JSON files)
**Auth**: None
**Data Format**: JSON
**Update Frequency**: 15 minutes (quarter-hourly) to hourly
**License**: Public data from German federal agency

## What It Provides

SMARD (Strommarktdaten) is the Bundesnetzagentur's official energy market data platform for Germany. It provides comprehensive electricity generation, consumption, market, and price data. The web portal at smard.de is backed by a static JSON API serving chart data.

Data categories (filter IDs):

- **Generation by source**: Solar (1225), Wind Onshore (1226), Wind Offshore (1227), Biomass (4066), Hydro (1228), Pumped Storage (4069), Gas (4071), Hard Coal (4072), Lignite (4073), Nuclear (1224), Other conventional (4070), Other renewables (4074)
- **Total generation**: Conventional (410), Renewables (4068)
- **Consumption**: Total electricity consumption (410 with DE region)
- **Market data**: Day-ahead prices, intraday prices
- **Cross-border**: Import/export physical flows

The data is served as pre-computed JSON files indexed by weekly timestamps.

## API Details

Two-step access pattern:

1. **Get index** (list of available weekly timestamps):
```
GET https://smard.de/app/chart_data/410/DE/index_hour.json
→ {"timestamps": [1419807600000, 1420412400000, ...]}
```

2. **Get data** for a specific week:
```
GET https://smard.de/app/chart_data/{filter_id}/{region}/{filter_id}_{region}_{resolution}_{timestamp}.json
```

The index endpoint was verified working and returned timestamps going back to 2015. The data endpoint URL pattern uses the filter ID, region code, resolution (hour/quarterhour), and a weekly start timestamp from the index.

Regions: `DE` (Germany), `AT_LU` (Austria/Luxembourg), and German TSO zones: `50Hertz`, `Amprion`, `TenneT`, `TransnetBW`.

Filter IDs map to specific generation types or market data categories. The resolution can be `hour` or `quarterhour`.

## Freshness Assessment

Quarter-hourly resolution for generation data, hourly for some market data. Data is published with a delay of approximately 1-2 hours. The index timestamps update weekly, but data within each week file includes the most recent available data points.

## Entity Model

- **Filter ID**: Numeric category (1224=Nuclear, 1225=Solar, 1226=Wind Onshore, etc.)
- **Region**: DE, AT_LU, 50Hertz, Amprion, TenneT, TransnetBW
- **Resolution**: hour, quarterhour
- **Timestamp**: UNIX milliseconds (weekly boundaries for file addressing, individual timestamps within data)
- **Value**: MW or EUR/MWh

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | Quarter-hourly updates |
| Openness | 3 | No auth, government data |
| Stability | 2 | Undocumented internal API, URL patterns may change with portal redesigns |
| Structure | 2 | Clean JSON but file-based access pattern requires two-step lookup |
| Identifiers | 2 | Numeric filter IDs are not self-describing, need mapping table |
| Additive Value | 2 | Germany-specific; overlaps significantly with energy-charts.info which is cleaner |
| **Total** | **14/18** | |

## Notes

- SMARD is the authoritative source — energy-charts.info actually cites SMARD/Bundesnetzagentur as a data source for price data.
- The main advantage over energy-charts.info is the German TSO zone breakdown (50Hertz, Amprion, TenneT, TransnetBW) — useful for understanding the four German control areas individually.
- The file-based pattern (index → weekly JSON file) is somewhat cumbersome compared to a query-based API, but it enables efficient caching.
- The data endpoint URL pattern was not fully verified during testing (404 responses for attempted URL constructions). The exact pattern likely requires inspecting the web portal's JavaScript.
- For most use cases, energy-charts.info provides the same German data in a much friendlier API format.
