# GFZ Potsdam Kp Index

**Country/Region**: Global (13 contributing observatories)
**Publisher**: GFZ German Research Centre for Geosciences, Potsdam
**API Endpoint**: `https://kp.gfz-potsdam.de/app/json/`
**Documentation**: https://kp.gfz-potsdam.de/en/, https://doi.org/10.1029/2020SW002641
**Protocol**: REST
**Auth**: None
**Data Format**: JSON
**Update Frequency**: Every 3 hours (Kp is a 3-hourly index); nowcast available
**License**: CC BY 4.0

## What It Provides

The Kp index is the planetary geomagnetic activity index, introduced in 1949 by Julius Bartels. It measures the disturbance of Earth's magnetic field caused by solar wind on a quasi-logarithmic scale from 0 (quiet) to 9 (extreme storm). GFZ Potsdam is the official provider of Kp and derived indices (ap, Ap, Cp, C9). The data series goes back to 1932, making it one of the longest continuous geophysical records.

GFZ also provides the newer Hpo indices (Hp30 and Hp60) with 30-minute and 60-minute resolution, and forecasts for Kp, ap, and related indices.

## API Details

- **JSON API**: `https://kp.gfz-potsdam.de/app/json/?start={YYYY-MM-DD}&end={YYYY-MM-DD}`
- **Note**: The JSON endpoint returned the website content (German) rather than JSON during probing — may require different URL format or the endpoint may have changed
- **Alternative source**: NOAA SWPC mirrors Kp at `https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json` — this endpoint was confirmed working with JSON data containing `time_tag`, `Kp`, `a_running`, `station_count`
- **NOAA data fields**: 3-hourly records with Kp (float, 0-9 scale), running `a` index, number of reporting stations
- **Indices provided**: Kp (quasi-logarithmic, 0-9), ap (linear, nT), Ap (daily average of ap), Cp, C9
- **Hpo indices**: Hp30 (30-min), Hp60 (60-min) — higher temporal resolution versions
- **Forecasts**: https://spaceweather.gfz.de/products-data/forecasts

## Freshness Assessment

Kp is inherently a 3-hourly index — new values appear every 3 hours with minimal delay. NOAA SWPC provides the near-real-time Kp as soon as it's computed. The Hpo indices (30-min, 60-min) provide higher temporal resolution. Historical data is available back to 1932. GFZ is the definitive source; NOAA SWPC is the most accessible real-time mirror.

## Entity Model

- **Kp Value**: Timestamp (3-hour bin start), Kp (0.00-9.00), ap equivalent
- **Station**: Contributing observatory (one of 13 worldwide)
- **Daily Summary**: Ap (daily average), Cp (daily character), C9 (integer 0-9)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | 3-hourly cadence; delivered promptly |
| Openness | 3 | CC BY 4.0; no auth; NOAA mirror confirmed working |
| Stability | 3 | GFZ and NOAA both provide; index since 1932 |
| Structure | 3 | Clean JSON from NOAA SWPC; well-defined numeric values |
| Identifiers | 2 | Time-binned index; no complex entity model |
| Additive Value | 3 | The canonical geomagnetic activity index; widely used |
| **Total** | **16/18** | |

## Notes

- The NOAA SWPC endpoint (`/products/noaa-planetary-k-index.json`) is the most reliable programmatic access point for real-time Kp.
- GFZ's own JSON API may require different URL construction than what was tested — the documentation suggests the data is available via their web application.
- Kp is used by space weather services, satellite operators, power grid operators, and aurora forecasters.
- The DOI-published dataset (https://doi.org/10.5880/Kp.0001) ensures citability and long-term availability.
- CC BY 4.0 is one of the most permissive licenses for scientific data.
