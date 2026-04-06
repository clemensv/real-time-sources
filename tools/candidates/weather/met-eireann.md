# Met Éireann — Ireland Open Weather Data

**Country/Region**: Ireland
**Publisher**: Met Éireann (Irish Meteorological Service)
**API Endpoint**: `https://www.met.ie/Open_Data/json/`
**Documentation**: https://data.gov.ie/dataset?q=met+eireann (via Ireland Open Data Portal)
**Protocol**: Static JSON files over HTTPS
**Auth**: None (fully open, no API key required)
**Data Format**: JSON
**Update Frequency**: Multiple times daily (forecasts), real-time (warnings)
**License**: Creative Commons Attribution 4.0 (CC BY 4.0)

## What It Provides

Met Éireann publishes weather forecasts and warnings as simple static JSON files — no API keys, no query parameters, just fetch a URL and parse:

- **National Forecast** (`National.json`): Today, tonight, tomorrow, and extended outlook as structured text with issue timestamp.

- **Regional Forecasts**: Province-level forecasts for Connacht, Leinster, Munster, and Ulster. Same structure as national.

- **Dublin Forecast** (`Dublin.json`): City-specific forecast.

- **Weather Warnings** (`warning_ALL.json`): All current weather warnings for Ireland. Per-county warnings available via `warning_EI{XX}.json` files (e.g., EI01 through EI31 for each county). Marine warnings via `warning_EI8XX.json`.

- **Coastal Forecast** (`coastal.json`): Coastal waters forecast.

- **Sea Area Forecast** (`Met-Sea-area.json`): Open sea forecast (Irish Sea, Atlantic).

- **Inland Lake Forecast** (`Inland_Lake_Forecast.json`): Lake weather conditions.

- **Outlook** (`Outlook.json`): Extended outlook beyond the standard forecast period.

## API Details

Every endpoint is a direct file download:
```
GET https://www.met.ie/Open_Data/json/National.json
```

The directory listing at `https://www.met.ie/Open_Data/json/` shows all available files with timestamps. The JSON structure wraps forecasts in a `forecasts` array with `regions` containing named key-value pairs for `region`, `issued`, `today`, `tonight`, `tomorrow`, and `outlook`.

Warning files contain structured CAP-like alert data. County warning files are tiny (3 bytes = `[]`) when no warnings are active.

No authentication, no API keys, no query parameters. Each file updates independently on its own schedule.

## Freshness Assessment

- Forecast files show update timestamps (e.g., `2026-04-06T09:00:00Z` for national forecast).
- Warning files update as conditions change (observed recent update: 2026-04-05).
- Dublin and regional forecasts update independently.
- The directory listing includes file timestamps and sizes, useful for polling.

## Entity Model

- **Region**: Named (National, Connacht, Leinster, Munster, Ulster, Dublin).
- **Forecast Period**: today, tonight, tomorrow, outlook — each containing free-text forecast.
- **Warning**: County-based (EI01–EI31 codes), marine areas (EI805–EI813).
- **Issue Time**: ISO 8601 timestamp.

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Multiple daily updates, but primarily text forecasts not observational data |
| Openness | 3 | No auth, CC BY 4.0, direct file access |
| Stability | 3 | National met service, part of Ireland's official open data program |
| Structure | 2 | Simple JSON, but free-text forecasts require NLP for structured extraction |
| Identifiers | 2 | County codes (EI01–EI31), region names — stable but limited |
| Additive Value | 2 | Ireland/Atlantic coverage, marine forecasts, but text-heavy |
| **Total** | **14/18** | |

## Notes

- The simplicity is both the strength and weakness — fetching data requires zero setup, but the data is mostly text forecasts rather than structured observations.
- Met Éireann also provides observation data through a separate portal (met.ie observations page), but the structured API access is primarily these JSON forecast files.
- Excellent for weather warning monitoring via the per-county warning files — polling 31 small files to detect new warnings is straightforward.
- Marine forecasts (coastal and sea area) are valuable for shipping/sailing applications in the North Atlantic and Irish Sea.
- The `issued` timestamp in each forecast enables change detection.
- Met Éireann also contributes to EUMETNET and participates in WMO data exchange.
