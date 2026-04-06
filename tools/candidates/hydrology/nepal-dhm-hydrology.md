# Nepal DHM — Department of Hydrology and Meteorology (via BIPAD)

**Country/Region**: Nepal
**Publisher**: Department of Hydrology and Meteorology (DHM), Ministry of Energy, Water Resources and Irrigation
**API Endpoint**: `https://bipadportal.gov.np/api/v1/river-stations/` (via BIPAD), `http://daq.hydrology.gov.np/` (DHM data acquisition)
**Documentation**: https://www.dhm.gov.np/, https://bipadportal.gov.np/
**Protocol**: REST (JSON) via BIPAD; DAQ web interface via DHM
**Auth**: None (BIPAD anonymous access)
**Data Format**: JSON with GeoJSON geometry
**Update Frequency**: 15-30 minutes (telemetric stations)
**License**: Nepal government data

## What It Provides

Nepal's DHM operates the country's hydrometeorological observation network. The data is critical for:

### Glacier Lake Outburst Floods (GLOFs)
Nepal has ~3,200 glacial lakes, of which 21+ are classified as potentially dangerous. As Himalayan glaciers retreat due to climate change, GLOF risk is increasing. DHM monitoring of upstream river levels is the first line of defense.

### Transboundary Flood Early Warning
Nepal's rivers (Koshi, Gandaki, Karnali, Mahakali) flow into India's Ganges plain. DHM water level data feeds directly into:
- India CWC flood forecasting
- Bangladesh FFWC downstream warnings
- Affecting 300+ million people downstream

### Monsoon Season Monitoring (June-September)
During monsoon, DHM issues multiple daily bulletins. Nepal receives 80% of annual rainfall in 4 months, causing annual flooding in the Terai plains.

### Real-Time Access via BIPAD

DHM data is accessible through the BIPAD portal API (see `nepal-bipad-hydrology.md`):
```
GET https://bipadportal.gov.np/api/v1/river-stations/?format=json&limit=100
```

This endpoint returns real-time water levels from DHM telemetric stations with danger/warning thresholds.

### Direct DHM Access

The DHM's own data acquisition system at `daq.hydrology.gov.np` provides:
- Station images (gauge photos)
- Telemetric data feeds
- This is the upstream data source that BIPAD aggregates

## Entity Model

- **River Station**: ID, name, basin, coordinates (GeoJSON), water level, thresholds
- **Meteorological Station**: ~300+ stations (fewer with telemetric real-time capability)
- **Basin**: Major river basins (Koshi, Gandaki, Karnali, Mahakali, etc.)
- **Snow/Glacier**: High-altitude monitoring stations

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | 15-30 minute telemetric updates confirmed via BIPAD |
| Openness | 3 | BIPAD API is anonymous, no auth |
| Stability | 2 | Government data; BIPAD operational since 2020 |
| Structure | 3 | Clean JSON with GeoJSON; danger/warning thresholds |
| Identifiers | 2 | Station IDs linked to hydrology.gov.np series |
| Additive Value | 3 | GLOF monitoring; transboundary flood warning; Himalayan climate change |
| **Total** | **16/18** | |

## Integration Notes

- Primary access path: BIPAD API (see nepal-bipad-hydrology.md for detailed probe results)
- DHM weather data (temperature, rainfall) is available on the website but not via API
- The GLOF dimension adds unique climate-change-related value
- Transboundary significance: data affects flood forecasting for 300M+ people in India and Bangladesh
- Consider combining with India CWC data for Ganges basin coverage

## Verdict

Strong candidate accessed through BIPAD portal. Nepal DHM's hydrological data is operationally critical for Himalayan flood early warning and glacier monitoring. The BIPAD portal provides clean, anonymous API access to real-time water levels. One of the best finds from this research round — fills a unique niche in high-altitude/glacier hydrology.
