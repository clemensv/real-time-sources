# PJM Data Miner 2

**Country/Region**: Eastern US (13 states + DC — Pennsylvania, New Jersey, Maryland, Virginia, Ohio, etc.)
**Publisher**: PJM Interconnection LLC
**API Endpoint**: `https://dataminer2.pjm.com/feed/{feed_name}/definition`
**Documentation**: https://www.pjm.com/markets-and-operations/data-dictionary
**Protocol**: REST (Data Miner 2 API)
**Auth**: Free pjm.com account for API queries (manual download without account)
**Data Format**: JSON, CSV
**Update Frequency**: Hourly to daily (varies by feed)
**License**: Public data

## What It Provides

PJM is the largest electricity market operator in North America, serving 65 million people across 13 states and the District of Columbia. Data Miner 2 is PJM's public data access tool.

Key data feeds:

- **rt_hrl_lmps** — Real-time hourly Locational Marginal Prices for all bus locations
- **da_hrl_lmps** — Day-ahead hourly LMPs
- **hrl_load_estimated** — Estimated hourly load by zone
- **load_frcstd_hist** — Historical metered load data
- **ops_sum_prev_period** — Operations summary (capacity, reserves, peak demand)
- **rt_scheduled_interchange** — Real-time scheduled interchange
- **act_sch_interchange** — Actual vs. scheduled interchange by tie line
- **day_inc_dec_utc** — Daily cleared virtual transactions

Additional reports (non-API):
- Capacity by fuel type
- Forecasted generation outages
- RPM auction results
- FTR model information

## API Details

Data Miner 2 provides a web interface and API for automated queries:

```
GET https://dataminer2.pjm.com/feed/rt_hrl_lmps/definition
```

The definition endpoint describes the feed structure. Data retrieval requires a pjm.com account and subscription key. Feeds support date range filtering, pagination, and format selection (JSON, CSV).

Key feeds and their update frequency:
- `rt_hrl_lmps` — Daily (hourly data)
- `da_hrl_lmps` — Daily
- `hrl_load_estimated` — Weekly (Tuesday/Friday)
- `ops_sum_prev_period` — Daily
- `sync_reserve_prelim_bill` — Daily

## Freshness Assessment

Real-time LMP data is published daily with hourly granularity. Estimated load data is published twice weekly. The operations summary is daily. This is not truly minute-level real-time, but it's the authoritative source for the PJM market and has good hourly coverage.

## Entity Model

- **Pricing Node (PNode)**: Thousands of bus locations across the PJM footprint
- **Zone**: Load zones (PECO, PSEG, BGE, ComEd, AEP, etc.)
- **LMP Components**: Energy, congestion, and loss components
- **Tie Line**: Interconnections with NYISO, MISO, and others
- **Time**: Hourly, Eastern Prevailing Time (EPT)

## Feasibility Rating

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 2 | Hourly LMPs published daily, not minute-level real-time |
| Openness | 2 | Free account required, public data |
| Stability | 3 | Regulatory-mandated, largest US ISO, well-maintained |
| Structure | 2 | JSON/CSV available but Data Miner SPA makes direct API access tricky |
| Identifiers | 3 | Standard PNode IDs, well-defined zones |
| Additive Value | 2 | EIA covers PJM demand/generation; PJM adds nodal LMPs |
| **Total** | **14/18** | |

## Notes

- PJM covers the most populous and industrialized region of the US — this is the world's largest competitive wholesale electricity market.
- The Data Miner 2 web app is an Angular SPA, making the API harder to discover than traditional REST APIs. Feed definitions and data access require inspecting network traffic or using the account-based API.
- The EIA Grid Monitor (`respondent=PJM`) provides hourly demand, generation, and interchange for PJM in a much cleaner format. Use PJM Data Miner primarily for nodal LMP data.
- PJM also publishes marginal emission data, though they explicitly caveat that accuracy cannot be guaranteed.
