# Copernicus European Drought Observatory (EDO)

- **Country/Region**: Europe
- **Endpoint**: https://drought.emergency.copernicus.eu/tumbo/edo/map/
- **Protocol**: WMS (visualization), no public API
- **Auth**: None (WMS), API unavailable
- **Format**: PNG tiles (WMS)
- **Freshness**: 10-day updates
- **Score**: 8/18

## Overview

EDO monitors agricultural and hydrological drought across Europe using:

- **SPI** (Standardized Precipitation Index) — meteorological drought
- **Soil Moisture Anomaly** — agricultural drought
- **Low Flow Index** — hydrological drought
- **Combined Drought Indicator (CDI)** — integrates all three
- **fAPAR Anomaly** — vegetation stress from satellite

Products updated every **10 days** (dekadal).

## Verdict

❌ **Skip** — EDO has **no public data API**. Only WMS visualization service (PNG tiles).
10-day update frequency is too slow for real-time streaming. Data access requires manual
download or institutional agreement.

| Criterion | Score |
|-----------|-------|
| Value | 2 |
| Freshness | 1 (10-day) |
| Openness | 1 (WMS only, no API) |
| Schema | 1 |
| Machine-readability | 0 (PNG tiles) |
| Repo fit | 3 (Europe-wide, grid cells could map to regions) |

**Total: 8/18** — **Skip**. Not viable without public API.
