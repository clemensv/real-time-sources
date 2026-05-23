# Saline Water Conversion Corporation (SWCC) - Desalination Plant Telemetry

- **Country/Region**: Saudi Arabia (KSA)
- **Endpoint**: Unknown (likely internal-only)
- **Protocol**: Unknown
- **Auth**: Unknown
- **Format**: Unknown
- **Freshness**: Real-time (industrial SCADA systems report continuously)
- **Docs**: https://www.swcc.gov.sa (no public data)
- **Score**: 7/18

## Overview

The **Saline Water Conversion Corporation** (المؤسسة العامة لتحلية المياه المالحة, SWCC) is the world's largest producer of desalinated water, supplying **~50% of Saudi Arabia's drinking water**. SWCC operates:

- **27 desalination plants** (Red Sea and Arabian Gulf coasts)
- **Production**: ~5 million m³/day of desalinated water
- **Power cogeneration**: Many plants also generate electricity (~4,000 MW)
- **Pipeline network**: ~10,000 km of water transmission pipelines

**Largest plants**:
- **Ras Al-Khair** (Arabian Gulf) — 1.03 million m³/day, world's largest
- **Shoaiba** (Red Sea, near Jeddah) — 1 million m³/day
- **Jubail** (Arabian Gulf) — 800,000 m³/day

**Desalination technologies**:
- **Multi-Stage Flash (MSF)** — 60% of capacity, energy-intensive
- **Reverse Osmosis (RO)** — 40% and growing, more energy-efficient
- **Hybrid plants** — Combined MSF + RO

**Energy coupling**: SWCC plants consume **~10-15% of Saudi Arabia's total electricity** to desalinate water. This makes desalination a major driver of electricity demand (and oil consumption for power).

**Context**: Saudi Arabia has **no perennial rivers**. Groundwater is fossil aquifers (non-renewable). Desalination is the only scalable source of fresh water for a population of 35 million.

## Potential Data Products

If SWCC published telemetry, it could include:

1. **Water production** — m³/day per plant, real-time output
2. **Energy consumption** — MW consumed per plant, kWh per m³ (specific energy)
3. **Power generation** — MW generated (cogeneration plants)
4. **Feed water salinity** — TDS (total dissolved solids) of seawater intake
5. **Product water quality** — TDS, pH, chlorine of desalinated water
6. **Plant availability** — Uptime percentage, outages
7. **Pipeline flows** — m³/hour in transmission pipelines to cities

**Update frequency**: Industrial SCADA (Supervisory Control and Data Acquisition) systems typically log data every **1-60 seconds** and aggregate to **1-15 minute** intervals for dashboards.

## Endpoint Analysis

**SWCC website**: `https://www.swcc.gov.sa`

The SWCC website provides corporate information, news, tenders, and employment. **No public data portal or telemetry dashboard** is advertised.

**Comparison with other water utilities**:

| Utility | Country | Public telemetry? | API? |
|---------|---------|-------------------|------|
| **SWCC** | Saudi Arabia | ❌ None | ❌ None |
| DEWA | UAE (Dubai) | ❌ Limited | ❌ None |
| IDE Technologies | Israel | ❌ Commercial only | ❌ None |
| Sydney Water | Australia | ✅ Some | ✅ REST |
| Thames Water | UK | ✅ Limited | ❌ None |

**Pattern**: **Desalination plant data is almost never published** due to:
- **Commercial sensitivity** — Operating costs, efficiency metrics are competitive secrets
- **Security concerns** — Desalination plants are critical infrastructure (sabotage risk)
- **Infrastructure integrity** — Real-time pipeline pressure data could reveal weak points

## Integration Notes

- **No public data**: SWCC does not publish plant telemetry. This is universal for desalination operators (commercial + security reasons).
- **Alternative: Aggregate statistics** — SWCC publishes **annual reports** with total production, capacity, and efficiency. These are batch data (yearly), not real-time.
- **Research publications**: Academic papers on Saudi desalination may include efficiency data, but this is historical, not real-time.
- **Energy proxy**: If **SEC (Saudi Electricity Company)** publishes real-time grid load, SWCC's energy consumption could be inferred indirectly (desalination is ~10-15% of total load). However, this requires knowing which plants are online at any time.

**Unique value if data existed**:
- **Largest desalination fleet** — SWCC is the world's #1 desalination operator
- **Energy-water nexus** — Real-time energy consumption for water production (kWh per m³)
- **Climate impact** — Desalination will grow as Saudi population increases; tracking efficiency improvements is critical for sustainability

However, **publishing this data is extremely unlikely** due to commercial and security barriers.

## Scoring

| Criterion | Score | Notes |
|-----------|-------|-------|
| Freshness | 3 | SCADA systems are real-time (if data existed) |
| Openness | 0 | No public data, no API, no portal |
| Stability | 3 | SWCC is a government corporation, permanent infrastructure |
| Structure | 2 | Would likely be time-series JSON (SCADA standard) |
| Identifiers | 2 | Plant codes, pipeline IDs (if existed) |
| Additive value | 2 | Globally unique desalination data, but security-sensitive |

**Total: 12/18** (if data existed)  
**Actual: 7/18** (penalized for zero public data and security barriers)

**Verdict**: ❌ **Skip** — Desalination plant telemetry is **universally non-public** for commercial and security reasons. SWCC is extremely unlikely to publish real-time data. If water production data is needed, use **SWCC annual reports** (batch data, yearly totals).

**Alternative approach**: Focus on **SEC (Saudi Electricity Company)** grid load data. SWCC's energy consumption is a significant component (~10-15% of total load). If SEC publishes real-time load, SWCC's demand can be inferred indirectly. However, this requires correlation with plant outage schedules (also not public).

Do not pursue SWCC telemetry unless a formal open data initiative is announced (extremely unlikely).
