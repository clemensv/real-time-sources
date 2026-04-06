# OCCTO — Organization for Cross-regional Coordination of Transmission Operators (Japan)

**Country/Region**: Japan
**Publisher**: OCCTO (Organization for Cross-regional Coordination of Transmission Operators)
**API Endpoint**: `https://occtonet3.occto.or.jp/public/dfw/RP11/OCCTO/SD/` (demand data)
**Documentation**: https://www.occto.or.jp/en/ (English), https://occtonet3.occto.or.jp/ (data portal, Japanese)
**Protocol**: Web portal with file downloads
**Auth**: None for public data (some datasets require registration)
**Data Format**: CSV (downloadable), HTML (portal display)
**Update Frequency**: Hourly (demand), daily (supply plan)
**License**: Publicly accessible (Japanese regulatory requirement)

## What It Provides

OCCTO coordinates Japan's ten regional electricity utilities (EPCOs) and manages cross-regional power interchange. Japan's grid is unique: split into 50 Hz (eastern) and 60 Hz (western) regions with limited frequency conversion capacity — a legacy of historical technology choices.

Available data:

- **Demand by area**: Hourly electricity demand for each of 10 utility service areas (Hokkaido, Tohoku, Tokyo, Chubu, Hokuriku, Kansai, Chugoku, Shikoku, Kyushu, Okinawa)
- **Supply plan**: Planned generation capacity and expected demand
- **Interchange**: Cross-regional power flows (especially 50Hz↔60Hz conversion)
- **Renewable output**: Solar and wind generation (aggregated)
- **Grid utilization**: Transmission line utilization rates
- **Imbalance**: Supply-demand imbalance data

Individual EPCOs also publish data:
- **TEPCO** (Tokyo): https://www.tepco.co.jp/forecast/html/
- **KEPCO** (Kansai): https://www.kepco.co.jp/
- **Kyushu Electric**: Real-time solar curtailment data (Kyushu leads Japan in solar)

## API Details

OCCTO's data is primarily available through their OCCTONET web portal:

```
https://occtonet3.occto.or.jp/public/dfw/RP11/OCCTO/SD/data_download.html
```

Data is downloadable as CSV files. The portal uses session-based authentication even for public data. Individual EPCO websites publish demand data in various formats:

```
TEPCO demand forecast:
https://www.tepco.co.jp/forecast/html/juyo_j.html
(HTML page with embedded data, updated hourly)
```

Japan's Electricity Grid Council (JEPX) provides wholesale market data:
- JEPX: https://www.jepx.org/en/ — Day-ahead and intraday spot prices

No formal REST API has been identified. Data access requires either web scraping or CSV file downloads.

## Freshness Assessment

Hourly demand data is published with ~1-hour lag. Supply plans are published day-ahead. JEPX spot prices are published after market clearing (around 10:00 JST for next day). Solar/wind generation data varies by EPCO — some publish 5-minute data.

## Entity Model

- **Area**: 10 utility service areas (Hokkaido, Tohoku, Tokyo, Chubu, Hokuriku, Kansai, Chugoku, Shikoku, Kyushu, Okinawa)
- **Frequency**: 50 Hz (eastern: Hokkaido, Tohoku, Tokyo) and 60 Hz (western: all others)
- **Price**: JPY/kWh (JEPX spot price)
- **Time**: JST (UTC+9)
- **Values**: MW (demand, generation), MWh (energy)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly data with ~1h lag |
| Openness | 2 | Public but portal-based, CSV downloads, session-dependent |
| Stability | 3 | Government-mandated coordination body, established institution |
| Structure | 1 | No REST API; CSV downloads and web scraping required |
| Identifiers | 2 | EPCO service area names, JEPX codes |
| Additive Value | 3 | Only source for Japan's grid — world's 3rd largest economy, unique 50/60Hz split |
| **Total** | **13/18** | |

## Notes

- Japan's 50Hz/60Hz split is one of the world's most fascinating grid engineering challenges. Three frequency conversion stations (Sakuma, Shin-Shinano, Higashi-Shimizu) with limited combined capacity (~1.2 GW) constrain east-west power flows.
- After Fukushima (2011), Japan shut down all nuclear reactors. Gradual restarts (primarily in western Japan) have reshaped the generation mix. Solar has grown dramatically, especially in Kyushu.
- Kyushu's solar curtailment data is particularly interesting — the island frequently curtails solar due to oversupply relative to demand and transmission capacity.
- JEPX (Japan Electric Power Exchange) data is the most structured source for Japanese market prices.
- The combination of OCCTO (grid coordination), individual EPCOs (regional data), and JEPX (prices) would provide comprehensive Japanese grid coverage.
