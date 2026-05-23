# King Abdullah Petroleum Studies and Research Center (KAPSARC) - Energy Data Hub

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: `https://www.kapsarc.org` (research institute)
- **Protocol**: Unknown (likely none — KAPSARC publishes research, not real-time data)
- **Auth**: Unknown
- **Format**: PDF reports, Excel datasets (batch data)
- **Freshness**: Batch (monthly, quarterly, annual reports)
- **Docs**: https://www.kapsarc.org/research/publications/
- **Score**: 5/18

## Overview

The **King Abdullah Petroleum Studies and Research Center** (مركز الملك عبدالله للدراسات والبحوث البترولية, KAPSARC) is a Saudi think tank focused on energy economics and policy. Founded in 2010, KAPSARC conducts research on:

- **Oil and gas markets** — Global supply/demand, pricing dynamics
- **Energy policy** — Saudi Vision 2030, renewable energy, energy efficiency
- **Climate change** — Carbon pricing, emissions reduction strategies
- **Energy data** — Statistical analysis, forecasting models

**KAPSARC's role**: While KAPSARC is **not an operational data provider** (like SEC or SWCC), it **aggregates and analyzes energy data** from:
- **Saudi Aramco** — Oil production, refining capacity
- **Ministry of Energy** — National energy statistics
- **SEC (Saudi Electricity Company)** — Grid data
- **ECRA (Electricity and Cogeneration Regulatory Authority)** — Market structure
- **International sources** — IEA, OPEC, EIA

**Publications**: KAPSARC publishes:
- **Discussion papers** — Policy analysis, modeling studies
- **Data Insights** — Visualizations and datasets
- **Working papers** — Econometric models, forecasts
- **Workshops and conferences** — Energy policy dialogues

## Data Products

KAPSARC publishes **batch datasets** (not real-time):

1. **Saudi energy balance** — Annual energy consumption by sector (residential, industrial, transport)
2. **Oil production and exports** — Monthly crude oil output, refining, exports
3. **Electricity consumption** — Sectoral demand, peak load, capacity
4. **Renewable energy deployment** — Solar and wind capacity installed
5. **Fuel prices** — Gasoline, diesel, natural gas (subsidized domestic prices)
6. **Carbon emissions** — CO2 from oil/gas consumption

**Update frequency**: Most KAPSARC data is **annual or quarterly**. Some datasets (oil production) may be **monthly**, but this is still **batch**, not real-time.

## Endpoint Analysis

**KAPSARC website**: `https://www.kapsarc.org`

The website provides:
- **Publications library** — PDFs of research papers
- **Data portal** — Excel files and CSV downloads for select datasets
- **Visualizations** — Interactive charts (Tableau, Power BI embeds)

**No real-time API**: KAPSARC does not operate real-time sensors or publish streaming data. It is a **research institute**, not a data provider.

**Example datasets** (batch):
- Saudi Arabia Energy Balance (annual, Excel)
- Oil production and exports (monthly, Excel)
- Electricity consumption by sector (quarterly, Excel)

**Comparison with other energy research institutes**:

| Institute | Country/Region | Real-time data? | API? |
|-----------|----------------|-----------------|------|
| **KAPSARC** | Saudi Arabia | ❌ Batch only | ❌ None |
| IEA | Global | ❌ Batch only | ✅ REST (limited) |
| EIA | USA | ❌ Batch only | ✅ REST |
| ENTSO-E | Europe | ✅ Real-time grid | ✅ REST XML |
| Ember | Global | ❌ Batch only | ❌ None |

**Pattern**: Research institutes (KAPSARC, IEA, EIA, Ember) publish **historical and batch data**, not real-time streams. Real-time energy data comes from **operators** (ENTSO-E, CAISO, AEMO), not researchers.

## Integration Notes

- **KAPSARC is not a real-time source**: It aggregates and publishes **batch datasets** (annual, quarterly, monthly). This does not meet the "hourly or better" criterion for this repo.
- **Unique value**: KAPSARC datasets are valuable for **historical analysis** (energy transition trends, Vision 2030 progress), but are **not event streams**.
- **Alternative: Operational sources** — For real-time Saudi energy data, focus on:
  - **SEC (Saudi Electricity Company)** — Grid load (if published)
  - **GCCIA** — GCC grid cross-border flows (if published)
  - **NCM** — Weather (solar/wind conditions)
- **KAPSARC as a discovery tool**: KAPSARC reports may **reference operational data sources** or APIs. Review publications to identify where KAPSARC sources its data (e.g., SEC dashboards, Ministry of Energy portals).

**KAPSARC's role in this repo**: ⏭️ **Reference** — Not a build target, but useful for:
- Discovering operational data sources (cited in papers)
- Understanding Saudi energy infrastructure (background research)
- Validating bridge outputs (compare real-time to KAPSARC aggregates)

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 1 | Monthly at best, mostly annual/quarterly |
| Openness | 2 | Datasets are free to download (Excel, CSV) |
| Stability | 3 | KAPSARC is a well-funded research center, permanent institution |
| Structure | 2 | Excel and CSV (structured, but not streaming) |
| Identifiers | 1 | Aggregate data (national totals, sectors), no entity-level IDs |
| Additive value | 0 | Batch data, not real-time; does not meet repo criteria |

**Total: 9/18** (if data were real-time)  
**Actual: 5/18** (penalized for batch-only data)

**Verdict**: ❌ **Skip** — KAPSARC is a **research institute** that publishes **batch datasets** (monthly, quarterly, annual), not real-time streams. This does not meet the repo's "hourly or better" freshness requirement.

**Recommended action**:
1. **Use KAPSARC for discovery** — Review KAPSARC publications to identify operational data sources they cite (e.g., SEC dashboards, Ministry portals).
2. **Focus on operators** — Build bridges for **SEC** (grid load), **GCCIA** (cross-border flows), **NCM** (weather), not KAPSARC aggregates.
3. **Batch data integration** — If the repo ever supports batch datasets (e.g., monthly energy balances for validation), reassess KAPSARC as a **reference data** source.

Do not build a KAPSARC bridge — it is a research aggregator, not a real-time feed.
